#!/usr/bin/env python3
"""Erzeugt train/examples.json einer Edition: pro Lemma ein schlanker Index von
Vers-Referenzen (ohne Verstext), damit der Nutzer bei einer falsch beantworteten
Kontext-Übung über "Weitere Beispiele" das Wort in weiteren Sätzen sieht. Der
Verstext wird in der App on-the-fly aus den Bibeltext-Dateien geholt.

Format (kompakt):  { "<lemma>": [ [<bookNr>, <chapter>, <verse>, <wortindex>], ... ] }
Lazy in der App geladen (nicht beim Start).

Der Schlüssel ist das Lemma wie in words.json (`en`). Für Editionen, deren
Annotations-Lemmata normalisiert werden mussten (z.B. Spanisch: Rand-Satzzeichen,
"(se)", Plural→Singular), wird das Anno-Lemma vor dem Abgleich normalisiert.

Aufruf:  python3 generate_examples.py [edition-id]   (Default: eng-web)
"""
import json, os, sys, re, glob

MAX_PER_LEMMA = 5
MIN_WORDS, MAX_WORDS = 5, 30
EDGE = r'[.,;:!?…"\'«»‹›„‚“”‘’`´¿¡]'

LANGS = {
    "eng-web": {"bible_dir": "bibles/eng/web", "suffix": "_web",
                "anno_suffix": "_web_deu", "normalize": False},
    "spa-rv1909mod": {"bible_dir": "bibles/spa/rv1909mod", "suffix": "_rv1909mod",
                      "anno_suffix": "_rv1909mod_eng", "normalize": True},
}


def normalize_lemma(lem):
    s = re.sub(r'\(se\)$', '', lem.strip())
    s = re.sub(r'\([^)]*\)', '', s)
    return re.sub(r'^' + EDGE + r'+|' + EDGE + r'+$', '', s.strip()).strip()


def main():
    ed = sys.argv[1] if len(sys.argv) > 1 else "eng-web"
    cfg = LANGS[ed]
    norm = cfg["normalize"]
    train = os.path.join(cfg["bible_dir"], "train")
    WORDS = os.path.join(train, "words.json")
    OUT = os.path.join(train, "examples.json")

    # Curated-Refs je Lemma (words.json `en`) — Übungssatz nicht doppeln
    curated = {}
    for arr in json.load(open(WORDS, encoding="utf-8")).values():
        for e in arr:
            curated[e["en"]] = e.get("ref")

    def canon(lem):
        """Anno-Lemma → Pool-Schlüssel (normalisiert + Plural→Singular-Fallback)."""
        c = normalize_lemma(lem) if norm else lem
        if c in curated:
            return c
        if norm:
            if c.endswith("es") and c[:-2] in curated:
                return c[:-2]
            if c.endswith("s") and c[:-1] in curated:
                return c[:-1]
        return None

    by_lemma = {}
    for nr in range(1, 67):
        ap = os.path.join(cfg["bible_dir"], "anno", f"{nr}{cfg['anno_suffix']}.json")
        tp = os.path.join(cfg["bible_dir"], f"{nr}{cfg['suffix']}.json")
        if not (os.path.exists(ap) and os.path.exists(tp)):
            continue
        anno = json.load(open(ap, encoding="utf-8"))
        text = json.load(open(tp, encoding="utf-8"))
        name = text.get("name") or anno.get("name") or f"Book {nr}"
        vtext = {str(cn): {str(vn): t for vn, t in verses.items()}
                 for cn, verses in text["chapters"].items()}
        for cn, verses in anno["chapters"].items():
            for vn, anns in verses.items():
                vt = vtext.get(str(cn), {}).get(str(vn))
                if not vt:
                    continue
                wc = len(vt.split())
                if wc < MIN_WORDS or wc > MAX_WORDS:
                    continue
                ref = f"{name} {cn}:{vn}"
                seen = set()
                for a in anns:
                    if a.get("pos_end") is not None:
                        continue
                    lem, pos = a.get("lemma"), a.get("pos")
                    if not lem or pos is None:
                        continue
                    key = canon(lem)
                    if key is None or key in seen:
                        continue
                    seen.add(key)
                    if ref == curated.get(key):
                        continue
                    by_lemma.setdefault(key, []).append([nr, int(cn), int(vn), pos])

    out = {}
    for lem, occ in by_lemma.items():
        if len(occ) <= MAX_PER_LEMMA:
            out[lem] = occ
        else:
            step = len(occ) / MAX_PER_LEMMA
            out[lem] = [occ[int(i * step)] for i in range(MAX_PER_LEMMA)]

    json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    total = sum(len(v) for v in out.values())
    print(f"{ed}: {len(out)} Lemmas, {total} Beispiele -> {OUT}  ({os.path.getsize(OUT)/1024:.0f} KB)")


if __name__ == "__main__":
    main()
