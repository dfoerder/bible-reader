#!/usr/bin/env python3
"""Trainingsdaten-Builder — Schritt 3: Finalisierung zu words.json.

Verbindet das Extraktions-Intermediate (train/lemmas_raw.json) mit den
Opus-Enrichment-Ausgaben (enrich_dir/out_*.json: pro Lemma level/pos/base_en/
form_en/form_tag) zu bibles/<edition>/train/words.json im App-Schema:
  { "A1":[{en,de,sub,occ,text,answer,ref,book,pos,deForm,form}], ... }

Filter/Cleanup:
- nur Inhaltswörter (pos in noun/verb/adj/adv); Funktionswörter, Eigennamen
  (propn), Zahlen, Interjektionen raus.
- Mehrwort-„Lemmata" (enthalten Leerzeichen) raus.
- Lemma normalisieren: Rand-Satzzeichen und angehängtes „(se)" strippen.
- Drop-Liste aus enrich_dir/_suspects_decided.json (obskure Gentilizia/
  Transliterationen, keep==false) + fest kodierte Maß-/Transliterations-Einheiten.
- Dubletten je normalisiertem Lemma zusammenführen; Plural→Singular mergen,
  wenn der Singular schon im Pool ist.
- Level aus dem Enrichment; Sublevel (1–3) nach Häufigkeit je Level (Drittel).

Aufruf:  python3 finalize_training.py spa-rv1909mod <enrich_out_dir>
"""
import json, os, sys, re, glob
from collections import defaultdict

# plural_merge: die Regel „Wort endet auf -s/-es und der Stamm steht schon im Pool"
# passt nur zu romanischen Pluralen. Deutsche Plurale werden anders gebildet, und
# die Regel würde dort echte Wörter verschlucken (Gottes → Gott) — deshalb aus.
LANGS = {
    "spa-rv1909mod": {"bible_dir": "bibles/spa/rv1909mod", "suffix": "_rv1909mod",
                      "plural_merge": True},
    # lead = Leitsprache: füllt die einsprachigen Altfelder de/deForm, damit
    # Editionen ohne Sprachwahl unverändert funktionieren.
    "deu-l1912mod": {"bible_dir": "bibles/deu/l1912mod", "suffix": "_l1912mod",
                     "plural_merge": False, "lead": "en"},
}
LEVELS = ["A1", "A2", "B1", "B2", "C1", "C2"]
CONTENT_POS = {"noun", "verb", "adj", "adv"}
# Transliterierte Maß-/Kult-Einheiten & Fremdwörter (keine allgemeine Vokabel).
# Sprachgebunden: die Liste stammt aus der spanischen Edition.
UNIT_DROP_BY_ED = {
    "spa-rv1909mod": {"hin", "homer", "gomer", "gera", "log", "efa", "efá", "seah",
                      "sela", "corbán", "maranata", "efatá", "cum", "lama",
                      "sabactani", "ayin", "tsade", "racá", "raca", "mammón",
                      "mamón", "aleluya"},
}
EDGE = r'[.,;:!?…"\'«»‹›„‚“”‘’`´¿¡]'


def normalize_lemma(lem):
    s = re.sub(r'\(se\)$', '', lem.strip())          # "acordar(se)" → "acordar"
    s = re.sub(r'\([^)]*\)', '', s)                   # sonstige Klammer-Notation
    s = re.sub(r'^' + EDGE + r'+|' + EDGE + r'+$', '', s.strip())
    return s.strip()


def guess_form_tag(base, form, pos):
    """Formkategorie (sg/pl/inf/pres/past/part/base) über die englische Achse.

    Die Lückentext-Ablenker werden nach (Wortart, Formkategorie) gebündelt, damit
    zu „ging" nicht „gehen" und „gegangen" als Alternativen erscheinen. Die
    Kategorie beschreibt die Form des Studienworts; ermittelt wird sie hier am
    englischen Paar Grundform/Kontextform — dieselbe Regel wie clozeFormOf() in
    der App, nur eben zur Bauzeit.
    """
    b = re.sub(r'^to\s+', '', (base or "").lower())
    b = re.sub(r'[^a-z]', '', b)
    f = re.sub(r'[^a-z]', '', (form or "").lower())
    if not b or not f or pos not in ("noun", "verb"):
        return "base"
    if pos == "noun":
        if f != b and (f == b + "s" or f == b + "es"
                       or (b.endswith("y") and f == b[:-1] + "ies")
                       or (f.endswith("s") and not b.endswith("s") and len(f) > len(b))):
            return "pl"
        return "sg"
    if f.endswith("ing"):
        return "part"
    if f == b:
        return "inf"
    if f in (b + "s", b + "es"):
        return "pres"
    return "past"


def book_names(cfg):
    names = {}
    for f in glob.glob(os.path.join(cfg["bible_dir"], f"*{cfg['suffix']}.json")):
        try:
            nr = int(os.path.basename(f).split("_")[0])
        except ValueError:
            continue
        names[nr] = json.load(open(f, encoding="utf-8")).get("name", f"Book {nr}")
    return names


def main():
    if len(sys.argv) < 3 or sys.argv[1] not in LANGS:
        print("Aufruf: python3 finalize_training.py <edition-id> <enrich_out_dir>")
        sys.exit(1)
    ed, enrich_dir = sys.argv[1], sys.argv[2]
    cfg = LANGS[ed]

    raw = json.load(open(os.path.join(cfg["bible_dir"], "train", "lemmas_raw.json"), encoding="utf-8"))

    enrich = {}
    for f in sorted(glob.glob(os.path.join(enrich_dir, "out_*.json"))):
        for o in json.load(open(f, encoding="utf-8")):
            enrich[o.get("lemma")] = o

    drop = set(UNIT_DROP_BY_ED.get(ed, ()))
    dec_path = os.path.join(enrich_dir, "_suspects_decided.json")
    if os.path.exists(dec_path):
        for o in json.load(open(dec_path, encoding="utf-8")):
            if not o.get("keep"):
                drop.add(o["lemma"])
    print(f"Enrichment: {len(enrich)} · Drop-Liste: {len(drop)}")

    names = book_names(cfg)

    # ── Einträge sammeln, je normalisiertem Lemma zusammenführen ──
    pool = {}   # clean_lemma → entry
    stats = defaultdict(int)
    for lem, r in raw.items():
        if r["is_cap"]:
            stats["cap"] += 1; continue
        if lem in drop:
            stats["droplist"] += 1; continue
        e = enrich.get(lem)
        if not e:
            stats["no_enrich"] += 1; continue
        if e.get("pos") not in CONTENT_POS:
            stats["pos"] += 1; continue
        clean = normalize_lemma(lem)
        if not clean or " " in clean:
            stats["multiword_or_empty"] += 1; continue
        level = e.get("level") if e.get("level") in LEVELS else r["level"]
        cz = r.get("cloze")
        # Mehrsprachige Anreicherung: `base` ist ein Sprach-Dict. Die flektierte
        # Formübersetzung kommt dann NICHT aus dem Modell, sondern direkt von der
        # Cloze-Fundstelle — dort steht die kontextuell korrekte Glosse schon.
        base = e.get("base") if isinstance(e.get("base"), dict) else None
        if base:
            form_tr = dict((cz or {}).get("gl") or {})
            for l, v in base.items():
                form_tr.setdefault(l, v)
            lead = cfg.get("lead") or next(iter(base))
            cand = {
                "en": clean, "de": base.get(lead) or r.get("gloss_ctx") or clean,
                "tr": base, "trForm": form_tr,
                "occ": r["freq"], "level": level, "pos": e["pos"],
                "deForm": form_tr.get(lead) or base.get(lead) or clean,
                "form": e.get("form_tag") or guess_form_tag(base.get("en"),
                                                            form_tr.get("en"), e["pos"]),
                "_cloze": cz,
            }
        else:
            cand = {
                "en": clean, "de": e.get("base_en") or r.get("gloss_ctx") or clean,
                "occ": r["freq"], "level": level, "pos": e["pos"],
                "deForm": e.get("form_en") or e.get("base_en") or clean,
                "form": e.get("form_tag") or "base",
                "_cloze": cz,
            }
        cur = pool.get(clean)
        if cur is None:
            pool[clean] = cand
        else:
            cur["occ"] += r["freq"]                      # Häufigkeiten summieren
            if not cur.get("_cloze") and cz:             # Eintrag mit Cloze bevorzugen
                cur["_cloze"] = cz
                cur.update({k: cand[k] for k in ("de", "deForm", "form", "tr", "trForm")
                            if k in cand})

    # ── Plural→Singular zusammenführen, wenn Singular existiert ──
    merged = 0
    for lem in (list(pool.keys()) if cfg.get("plural_merge", True) else []):
        if lem not in pool:
            continue
        base = None
        if lem.endswith("es") and lem[:-2] in pool:
            base = lem[:-2]
        elif lem.endswith("s") and lem[:-1] in pool:
            base = lem[:-1]
        if base and base != lem:
            pool[base]["occ"] += pool[lem]["occ"]
            if not pool[base].get("_cloze") and pool[lem].get("_cloze"):
                pool[base]["_cloze"] = pool[lem]["_cloze"]
            del pool[lem]; merged += 1

    # ── Nach Level bucketen, Sublevel nach Häufigkeit (Drittel) ──
    by_level = defaultdict(list)
    for e in pool.values():
        by_level[e["level"]].append(e)
    words = {lvl: [] for lvl in LEVELS}
    for lvl in LEVELS:
        arr = sorted(by_level[lvl], key=lambda w: (-w["occ"], w["en"]))
        third = max(1, -(-len(arr) // 3))
        for i, w in enumerate(arr):
            sub = 1 if i < third else 2 if i < 2 * third else 3
            # Mehrsprachige Editionen: die einsprachigen Altfelder de/deForm werden in
            # der App aus tr/trForm gefüllt und stehen deshalb nicht in der Datei —
            # das spart bei vier Sprachen rund ein Drittel. trForm entfällt zusätzlich,
            # wenn die flektierte Form der Grundform gleicht (der Normalfall bei
            # Substantiven im Nominativ Singular).
            tr = w.get("tr")
            entry = {"en": w["en"], "sub": sub, "occ": w["occ"]}
            if tr:
                entry["tr"] = tr
            else:
                entry["de"] = w["de"]
            cz = w.get("_cloze")
            if cz:
                entry.update({"text": cz["text"], "answer": cz["answer"],
                              "ref": f"{names.get(cz['ref_book'], 'Book')} {cz['ch']}:{cz['vn']}",
                              "book": cz["ref_book"]})
            entry.update({"pos": w["pos"], "form": w["form"]})
            if tr:
                tf = w.get("trForm")
                if tf and tf != tr:
                    entry["trForm"] = tf
            else:
                entry["deForm"] = w["deForm"]
            words[lvl].append(entry)

    out_path = os.path.join(cfg["bible_dir"], "train", "words.json")
    json.dump(words, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))

    # Eigennamen-Liste: in Sprachen, in denen Grossschreibung nichts über Eigennamen
    # sagt (Deutsch), braucht der Laufzeit-Filter der Kapitelübungen eine echte Liste
    # statt der Schreibungs-Heuristik. Erst vollständig, wenn ALLE Lemmata
    # angereichert sind — vorher nicht in der Registry verdrahten.
    propn = sorted(l for l, e in enrich.items() if e.get("pos") == "propn")
    pn_path = os.path.join(cfg["bible_dir"], "train", "propnames.json")
    json.dump(propn, open(pn_path, "w", encoding="utf-8"), ensure_ascii=False,
              separators=(",", ":"))
    print(f"✓ {pn_path} ({len(propn)} Eigennamen)")

    total = sum(len(v) for v in words.values())
    with_cloze = sum(1 for v in words.values() for w in v if "text" in w)
    print(f"✓ {out_path}")
    print(f"  Gefiltert: Eigennamen={stats['cap']}, Drop-Liste={stats['droplist']}, "
          f"Funktionswort/propn={stats['pos']}, Mehrwort={stats['multiword_or_empty']}, "
          f"ohne Enrichment={stats['no_enrich']} · Plural-Merges={merged}")
    print(f"  Pool: {total} Wörter, mit Cloze: {with_cloze}")
    print("  Level: " + ", ".join(f"{lvl}={len(words[lvl])}" for lvl in LEVELS))


if __name__ == "__main__":
    main()
