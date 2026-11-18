# Westminster Leningrad Codex (hebräisches AT)

Erzeugt mit `python3 convert_tahot.py "<STEPBible-Data>/Translators Amalgamated OT+NT" bibles/hbo/wlc bibles/index.json`
aus **STEPBible TAHOT** (Translators Amalgamated Hebrew OT, https://github.com/STEPBible/STEPBible-Data).

- `<nr>_wlc.json` — Text je Buch (`{name, chapters:{kap:{vers:text}}}`), Bücher 1–39, **englische Verszählung**
  (wie die übrigen Bibeln der App; z.B. Mal 4,1 = hebr. 3,19). Psalm-Überschriften stehen vorne in Vers 1.
- `anno/<nr>_wlc_multi.json` — je Wort `pos`, `form`, `lemma`, `en` (Glosse), `strong` (H…), `morph`
- Wörter des Leningrad-Kodex inkl. Qere-Lesungen; Jos 21,36–37 (im Kodex fehlend) aus TAHOT „restored“.
  Zusätze anderer Handschriften (TAHOT-Typ X/V) sind ausgelassen.
- Nach dem Maqaf (־) steht ein Leerzeichen und die Absatzzeichen פ/ס/׆ fehlen: die App ordnet Wort-Daten
  über Leerzeichen zu (geprüft: in allen 23'145 Versen gleich viele Wörter wie Annotationen).

Lizenzen / Namensnennung (Pflicht bei Veröffentlichung):
- Hebräischer Text: Westminster Leningrad Codex, frei verwendbar (tanach.us).
- TAHOT: STEPBible.org, auf Grundlage der Arbeit von Tyndale House, Cambridge — CC BY 4.0.

In der App Teil der Bibel `urtext` (zusammen mit `bibles/grc/n1904/`).
