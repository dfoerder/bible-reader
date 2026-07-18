#!/usr/bin/env python3
"""Leitet pro Bibel-Edition die Keep-Eigennamen aus der ZENTRALEN, mehrsprachigen
Kanon-Liste (names/keep_names.json) ab — und ergänzt die Liste dabei um die
Formen der jeweiligen Sprache.

Prinzip: Alle nicht-englischen Annotationen glossieren nach Englisch (`en`).
Für jedes großgeschriebene Lemma (Eigenname) wird seine englische Glosse (oder
das Lemma selbst) gegen den kanonischen `en`-Namen der Master-Einträge gematcht.
Passt es, wird
  (a) die Sprachform in den Master-Eintrag geschrieben (Liste wird mehrsprachig), und
  (b) das Lemma in bibles/<edition>/train/keepnames.json aufgenommen
      (der Laufzeit-Filter KEEP_NAMES lädt diese Datei).

So genügt EINE zentrale Liste für alle Sprachen; eine neue Sprache einführen =
dieses Skript einmal laufen lassen.

Aufruf:  python3 build_keepnames.py spa-rv1909mod
         python3 build_keepnames.py --all
"""
import json, os, sys, re, glob

CENTRAL = "names/keep_names.json"

# Edition → (Annotationsordner, Studiensprach-Code = Formschlüssel in der Master-Liste)
EDITIONS = {
    "spa-rv1909mod": ("bibles/spa/rv1909mod/anno", "es"),
    "fra-lsg1910mod": ("bibles/fra/lsg1910mod/anno", "fr"),
    "ita-riv1927mod": ("bibles/ita/riv1927mod/anno", "it"),
    # eng-web annotiert keine Eigennamen → kein keepnames nötig
}

_EDGE = r'[.,;:!?()\[\]"\'«»„“”‘’¿¡]'


def norm(s):
    s = (s or "").strip().lower()
    s = re.sub(r'^' + _EDGE + r'+|' + _EDGE + r'+$', '', s).strip()
    s = re.sub(r'^(the|a|an)\s+', '', s)
    return s


def is_proper(lemma):
    c = lemma[:1]
    return bool(c) and c == c.upper() and c != c.lower()


def build(edition):
    anno_dir, lang = EDITIONS[edition]
    master = json.load(open(CENTRAL, encoding="utf-8"))
    entries = master["entries"]
    # Lookup: normalisierter kanonischer en-Name (und bereits vorhandene Formen) → Eintrag
    lookup = {}
    for e in entries:
        lookup.setdefault(norm(e["en"]), e)
        for k, v in e.items():
            if k not in ("en", "type") and isinstance(v, str):
                lookup.setdefault(norm(v), e)

    keep = set()
    considered = 0
    for af in glob.glob(os.path.join(anno_dir, "*.json")):
        anno = json.load(open(af, encoding="utf-8"))
        for verses in anno.get("chapters", {}).values():
            for anns in verses.values():
                for a in anns or []:
                    if a.get("pos_end") is not None:
                        continue
                    lem = a.get("lemma", "")
                    if not is_proper(lem):
                        continue
                    considered += 1
                    ent = lookup.get(norm(a.get("en", ""))) or lookup.get(norm(lem))
                    if ent is not None:
                        ent[lang] = lem          # Sprachform in die Master-Liste eintragen
                        lookup.setdefault(norm(lem), ent)
                        keep.add(lem)

    # Master mit den ergänzten Formen zurückschreiben
    json.dump(master, open(CENTRAL, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    out_dir = os.path.join(os.path.dirname(anno_dir), "train")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "keepnames.json")
    json.dump(sorted(keep), open(out_path, "w", encoding="utf-8"), ensure_ascii=False)
    filled = sum(1 for e in entries if lang in e)
    print(f"  {edition}: {len(keep)} Keep-Namen → {out_path}  (Master-Formen '{lang}' gefüllt: {filled}/{len(entries)})")


def main():
    if len(sys.argv) < 2:
        print("Aufruf: python3 build_keepnames.py <edition-id> | --all"); sys.exit(1)
    targets = list(EDITIONS) if sys.argv[1] == "--all" else [sys.argv[1]]
    for ed in targets:
        if ed not in EDITIONS:
            print(f"  ⚠ unbekannte Edition: {ed}"); continue
        build(ed)


if __name__ == "__main__":
    main()
