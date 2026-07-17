#!/usr/bin/env python3
"""Pipeline-Nachschritt nach generate_deform.py: überschreibt deterministisch die
wenigen deutschen Übersetzungen, die Opus bei echt adjektivischen/präfix-artigen
englischen Wörtern falsch erzeugt (kein eigenständiges Wort, z.B. fellow->'Mit',
facial->'Gesichts') mit einer geprüften eigenständigen Übersetzung.

Reihenfolge:  generate_training_data.js -> generate_pos.py -> generate_deform.py
              -> fix_hyphen_de.py

Run:  python3 fix_hyphen_de.py
"""
import json

PATH = "bibles/eng/web/train/words.json"

# en-Lemma -> (de = Grundform, deForm = Form passend zur Wortform im Satz)
OVERRIDES = {
    "fellow": ("Gefährte", "Gefährte"),
    "facial": ("Gesicht", "Gesicht"),
    "batter": ("Sturmbock", "Sturmbock"),
    "chief": ("oberster", "oberster"),
}


def main():
    w = json.load(open(PATH))
    fixed = 0
    for arr in w.values():
        for e in arr:
            ov = OVERRIDES.get(e["en"])
            if ov:
                de, deform = ov
                if e.get("de") != de or e.get("deForm") != deform:
                    e["de"], e["deForm"] = de, deform
                    fixed += 1
    json.dump(w, open(PATH, "w"), ensure_ascii=False, separators=(",", ":"))
    print(f"{fixed} Übersetzung(en) überschrieben -> {PATH}")


if __name__ == "__main__":
    main()
