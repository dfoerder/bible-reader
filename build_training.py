#!/usr/bin/env python3
"""Trainingsdaten-Builder (sprachparametrisiert) — Schritt 1: Extraktion.

Liest die Wort-für-Wort-Annotationen einer Edition und leitet daraus die
eindeutigen Einzelwort-Lemmata ab: Häufigkeit, vorläufiges Level (Mehrheit),
bester Lückentext-Satz (Cloze) und die kontextuellen Glossen. Ausgabe ist ein
Intermediate (train/lemmas_raw.json), das im nächsten Schritt via Opus
angereichert (sauberes CEFR-Level, Wortart, Basis-/Form-Übersetzung) und dann zu
words.json finalisiert wird.

Anders als der englische generate_training_data.js braucht es hier KEINE
Flexions-Heuristik — die Annotationen liefern bereits `lemma`. Eigennamen
(großgeschriebene Lemmata) werden markiert; das eigentliche Content-Word-Filtern
passiert im Finalisierungsschritt anhand der Opus-Wortart.

Aufruf:  python3 build_training.py spa-rv1909mod
"""
import json, os, sys, re, glob
from collections import Counter, defaultdict

# gloss_fields — alle Glossensprachen der Edition; die erste ist die Leitsprache
# (Rückfallwert und Pivot der Anreicherung). caps_are_names: taugt Grossschreibung
# als Eigennamen-Hinweis? Im Deutschen nicht — dort ist jedes Substantiv gross,
# das Aussortieren übernimmt allein die Wortart aus der Anreicherung.
LANGS = {
    "spa-rv1909mod": {
        "bible_dir": "bibles/spa/rv1909mod", "suffix": "_rv1909mod",
        "anno_suffix": "_rv1909mod_eng", "gloss_fields": ["en"],
    },
    "eng-web": {
        "bible_dir": "bibles/eng/web", "suffix": "_web",
        "anno_suffix": "_web_deu", "gloss_fields": ["de", "es", "fr", "it"],
    },
    "deu-l1912mod": {
        "bible_dir": "bibles/deu/l1912mod", "suffix": "_l1912mod",
        "anno_suffix": "_l1912mod_multi", "gloss_fields": ["en", "es", "fr", "it"],
        "caps_are_names": False,
    },
}

LEVELS = ["A1", "A2", "B1", "B2", "C1", "C2"]
MAX_CLOZE_WORDS = 15
EDGE = r'[.,;:!?…(){}\[\]"\'«»‹›„‚“”‘’`´¿¡]'


def load_text(cfg, book_nr):
    """Einheitliches dict-Format → {ch_str: {v_str: text}}."""
    path = os.path.join(cfg["bible_dir"], f"{book_nr}{cfg['suffix']}.json")
    if not os.path.exists(path):
        return None
    d = json.load(open(path, encoding="utf-8"))
    out = {}
    for cn, verses in d["chapters"].items():
        out[str(cn)] = {str(vn): t for vn, t in verses.items()}
    return out


def extract_cloze(verse_text, pos, form):
    """Portiert aus generate_training_data.js: satzbegrenzter Lückentext um das
    Zielwort (pos), Randsatzzeichen bleiben außen, max. 15 Wörter."""
    words = verse_text.split()
    if pos >= len(words):
        return None
    sentences = re.split(r'(?<=[.!?…;:])\s+', verse_text)
    target_sentence, sent_offset, target_in_sent = None, 0, -1
    for sent in sentences:
        sw = sent.split()
        if sent_offset <= pos < sent_offset + len(sw):
            target_sentence, target_in_sent = sent, pos - sent_offset
            break
        sent_offset += len(sw)
    if target_sentence is None or target_in_sent < 0:
        return None
    # Wörtliche-Rede-Anfang abschneiden (wie im JS)
    m = re.search(r'["„«“]', target_sentence)
    if m and 0 < m.start() < len(target_sentence) / 2:
        before = target_sentence[:m.start()]
        before_words = len([w for w in before.split() if w])
        target_sentence = target_sentence[m.start():]
        target_in_sent -= before_words
        if target_in_sent < 0:
            return None
    sent_words = target_sentence.split()
    if len(sent_words) < 3:
        return None
    if len(sent_words) > MAX_CLOZE_WORDS:
        end = max(MAX_CLOZE_WORDS, target_in_sent + 2)
        sent_words = sent_words[:end]
        sent_words[-1] = re.sub(r'[.!?;,]*$', '', sent_words[-1]) + ' …'
    if target_in_sent >= len(sent_words):
        return None
    tok = sent_words[target_in_sent]
    lead = (re.match(r'^' + EDGE + r'+', tok) or [''])
    lead = lead.group(0) if hasattr(lead, "group") else ''
    trail = re.search(EDGE + r'+$', tok)
    trail = trail.group(0) if trail else ''
    sent_words[target_in_sent] = lead + '___' + trail
    text = ' '.join(sent_words)
    return text if '___' in text else None


def strip_edge(s):
    return re.sub(r'^' + EDGE + r'+|' + EDGE + r'+$', '', s)


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in LANGS:
        print("Aufruf: python3 build_training.py <edition-id>")
        print("  verfügbar:", ", ".join(LANGS))
        sys.exit(1)
    ed = sys.argv[1]
    cfg = LANGS[ed]
    gfs = cfg["gloss_fields"]
    gf = gfs[0]

    lemmas = defaultdict(lambda: {"level_counts": Counter(),
                                  "gloss_counts": defaultdict(Counter),
                                  "freq": 0, "occ": []})
    anno_files = sorted(glob.glob(os.path.join(cfg["bible_dir"], "anno", f"*{cfg['anno_suffix']}.json")),
                        key=lambda p: int(os.path.basename(p).split("_")[0]))
    text_cache = {}
    for af in anno_files:
        book_nr = int(os.path.basename(af).split("_")[0])
        anno = json.load(open(af, encoding="utf-8"))
        for cn, verses in anno.get("chapters", {}).items():
            for vn, anns in verses.items():
                for a in anns or []:
                    # Phrasen überspringen: zusammenhängend (pos_end) UND die
                    # deutsche Satzklammer (parts), die kein pos_end trägt.
                    if a.get("pos_end") is not None or a.get("parts"):
                        continue
                    lem = a.get("lemma")
                    lvl = a.get("level")
                    if not lem or lvl not in LEVELS:
                        continue
                    gl = {l: a.get(l) for l in gfs if a.get(l)}
                    d = lemmas[lem]
                    d["level_counts"][lvl] += 1
                    for l, g in gl.items():
                        d["gloss_counts"][l][g] += 1
                    d["freq"] += 1
                    d["occ"].append({"book": book_nr, "ch": cn, "vn": vn,
                                     "pos": a.get("pos"), "form": a.get("form"), "gl": gl})

    # bester Cloze-Satz je Lemma (Ziel ~15 Wörter)
    results = {}
    no_cloze = 0
    for lem, d in lemmas.items():
        best, best_score = None, 10**9
        for o in d["occ"]:
            if book_nr not in text_cache:
                pass
            txt = text_cache.get(o["book"])
            if txt is None:
                txt = load_text(cfg, o["book"]) or {}
                text_cache[o["book"]] = txt
            vt = txt.get(o["ch"], {}).get(o["vn"])
            if not vt:
                continue
            wc = len(vt.split())
            if wc < 5 or o["pos"] is None:
                continue
            cloze = extract_cloze(vt, o["pos"], o["form"])
            if not cloze:
                continue
            score = abs(wc - 15)
            if score < best_score:
                best_score, best = score, {
                    "text": cloze, "answer": strip_edge(o["form"] or ""),
                    "ref_book": o["book"], "ch": o["ch"], "vn": o["vn"],
                    "form": o["form"],
                    # Glossen GENAU dieser Fundstelle — kontextuell korrekt flektiert,
                    # daraus wird später die Antwortanzeige des Lückentexts je Sprache.
                    "gl": o.get("gl") or {},
                }
            if score == 0:
                break
        level = d["level_counts"].most_common(1)[0][0]
        # Mehrheitsglosse je Sprache: Rückfall, wenn die Anreicherung nichts liefert
        gloss_by = {l: c.most_common(1)[0][0] for l, c in d["gloss_counts"].items() if c}
        gloss = gloss_by.get(gf)
        if best is None:
            no_cloze += 1
        results[lem] = {
            "lemma": lem, "level": level, "freq": d["freq"],
            "gloss_ctx": gloss, "gloss_by": gloss_by, "cloze": best,
            "is_cap": bool(lem[:1].isupper()) if cfg.get("caps_are_names", True) else False,
        }

    out_dir = os.path.join(cfg["bible_dir"], "train")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "lemmas_raw.json")
    json.dump(results, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    # ── Statistik ──
    total = len(results)
    cap = sum(1 for r in results.values() if r["is_cap"])
    low = total - cap
    lvl_low = Counter(r["level"] for r in results.values() if not r["is_cap"])
    with_cloze = sum(1 for r in results.values() if r["cloze"])
    print(f"✓ {out_path}")
    print(f"  Eindeutige Einzelwort-Lemmata: {total}")
    print(f"  davon großgeschrieben (Eigennamen-Kandidaten): {cap}")
    print(f"  → Pool-Kandidaten (kleingeschrieben): {low}")
    print(f"  mit Cloze-Satz: {with_cloze} ({total - with_cloze} ohne)")
    print(f"  Level-Verteilung (kleingeschrieben): {dict(sorted(lvl_low.items()))}")


if __name__ == "__main__":
    main()
