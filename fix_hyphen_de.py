#!/usr/bin/env python3
"""Pipeline-Nachschritt: korrigiert die deutschen Übersetzungen, die als
abgehängtes Kompositum-Präfix mit Bindestrich aus den Vers-Annotationen kamen
(z.B. spider->'Spinnen-'), zu einer sauberen eigenständigen Grundform.

Der Generator behält Bindestriche bewusst (echte Komposita), daher würden diese
Präfix-Fragmente bei jeder Neugenerierung erneut entstehen. Diese Overrides sind
einmalig per Opus + manueller Prüfung erstellt und hier deterministisch fixiert.

Reihenfolge in der Pipeline:
  generate_training_data.js  ->  generate_pos.py  ->  fix_hyphen_de.py

Run:  python3 fix_hyphen_de.py
"""
import json

PATH = "data/words.json"

# en-Lemma -> saubere eigenständige deutsche Grundform (statt Präfix mit '-')
HYPHEN_FIX = {
    "main": "hauptsächlich",
    "spider": "Spinne",
    "wedding": "Hochzeit",
    "force": "Kraft",
    "wave": "Welle",
    "string": "Saite",
    "fellow": "Gefährte",
    "chief": "oberster",
    "olive": "Olive",
    "boiling": "kochend",
    "ewe": "Mutterschaf",
    "batter": "Sturmbock",
    "storage": "Vorrat",
    "foster": "Pflege",
    "utility": "Dienst",
    "facial": "Gesicht",
}


def main():
    w = json.load(open(PATH))
    fixed = 0
    for arr in w.values():
        for e in arr:
            repl = HYPHEN_FIX.get(e["en"])
            if repl and e["de"] != repl:
                e["de"] = repl
                fixed += 1
    json.dump(w, open(PATH, "w"), ensure_ascii=False, separators=(",", ":"))
    print(f"{fixed} Übersetzung(en) korrigiert -> {PATH}")


if __name__ == "__main__":
    main()
