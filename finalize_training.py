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

LANGS = {"spa-rv1909mod": {"bible_dir": "bibles/spa/rv1909mod", "suffix": "_rv1909mod"}}
LEVELS = ["A1", "A2", "B1", "B2", "C1", "C2"]
CONTENT_POS = {"noun", "verb", "adj", "adv"}
# Transliterierte Maß-/Kult-Einheiten & Fremdwörter (keine allgemeine Vokabel)
UNIT_DROP = {"hin", "homer", "gomer", "gera", "log", "efa", "efá", "seah", "sela",
             "corbán", "maranata", "efatá", "cum", "lama", "sabactani", "ayin",
             "tsade", "racá", "raca", "mammón", "mamón", "aleluya"}
EDGE = r'[.,;:!?…"\'«»‹›„‚“”‘’`´¿¡]'


def normalize_lemma(lem):
    s = re.sub(r'\(se\)$', '', lem.strip())          # "acordar(se)" → "acordar"
    s = re.sub(r'\([^)]*\)', '', s)                   # sonstige Klammer-Notation
    s = re.sub(r'^' + EDGE + r'+|' + EDGE + r'+$', '', s.strip())
    return s.strip()


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

    drop = set(UNIT_DROP)
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
                cur.update({"de": cand["de"], "deForm": cand["deForm"], "form": cand["form"]})

    # ── Plural→Singular zusammenführen, wenn Singular existiert ──
    merged = 0
    for lem in list(pool.keys()):
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
            entry = {"en": w["en"], "de": w["de"], "sub": sub, "occ": w["occ"]}
            cz = w.get("_cloze")
            if cz:
                entry.update({"text": cz["text"], "answer": cz["answer"],
                              "ref": f"{names.get(cz['ref_book'], 'Book')} {cz['ch']}:{cz['vn']}",
                              "book": cz["ref_book"]})
            entry.update({"pos": w["pos"], "deForm": w["deForm"], "form": w["form"]})
            words[lvl].append(entry)

    out_path = os.path.join(cfg["bible_dir"], "train", "words.json")
    json.dump(words, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))

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
