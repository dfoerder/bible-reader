# Nestle 1904 (griechisches NT)

Erzeugt mit `python3 convert_n1904.py <macula-greek-Nestle1904.tsv> bibles/grc/n1904`
aus **MACULA Greek** (`Nestle1904/tsv/macula-greek-Nestle1904.tsv`, https://github.com/Clear-Bible/macula-greek).

- `<nr>_n1904.json` — Text je Buch (`{name, chapters:{kap:{vers:text}}}`), Bücher 40–66
- `anno/<nr>_n1904_multi.json` — je Wort `pos`, `form`, `lemma`, `en` (Glosse), `strong` (G…), `morph`

Lizenzen / Namensnennung (Pflicht bei Veröffentlichung):
- Text: Nestle 1904 (Eberhard Nestle, British and Foreign Bible Society 1904), gemeinfrei;
  Transkription Diego Santos, Morphologie Ulrik Sandborg-Petersen, Markup Jonathan Robie.
- MACULA Greek Linguistic Datasets © 2022–2024 Biblica, Inc., CC BY 4.0.
- Englische Glossen (`en`): Berean Interlinear Bible, gemeinfrei seit 30.4.2023.
- Nicht übernommen: MARBLE-Wortbedeutungen (nur mit Erlaubnis), Cherith-Glossen.

In der App Teil der Bibel `urtext` (AT: `bibles/hbo/wlc/`). Noch offen: `de`/`es`/`fr`/`it`-Glossen, CEFR-`level`, griechische Buchnamen.
