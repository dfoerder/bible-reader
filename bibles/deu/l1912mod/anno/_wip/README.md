# Angefangene Kapitel (nicht von der App geladen)

Hier liegen **unvollständige** Kapitel-Fragmente der deutschen Annotation —
Teilarbeit aus Agentenläufen, die durch Verbindungsabbrüche beendet wurden.
Sie stehen hier, damit sie nicht verlorengehen, und werden von der App nie
geladen: `index.html` holt ausschließlich `<buchNr>_l1912mod_multi.json`.

## Format

Dateiname `<buchNr>_ch<kapitel>_verse<von>-<bis>.json`, Inhalt
`{"<vers>": [<eintraege>]}` — dasselbe Format, das die Agenten nach
`scratchpad/.../out/<buchNr>/` liefern. (Die Buchnummer stand früher nicht im
Namen; sie ist nötig, seit hier Fragmente aus mehreren Büchern liegen können.)

Jeder enthaltene Vers wurde einzeln gegen den Quelltext validiert
(Positionsabdeckung, Formen, Spannen, vier Sprachen). Fehlerhafte Verse sind
beim Sichern verworfen worden.

## Wiederaufnahme

Ein Agent, der das Kapitel fertigstellt, soll diese Datei als Vorlage lesen —
Terminologie, Level-Vergabe und Namensformen des Kapitels stehen darin schon
fest — und nur die fehlenden Verse ergänzen. Danach wandert das vollständige
Kapitel in den normalen Ablauf (`out/<buchNr>/ch<N>.json` → `buildbook.py`),
und die Datei hier kann gelöscht werden.

## Aktueller Inhalt

Zurzeit leer — alle geretteten Fragmente sind in fertige Kapitel eingegangen.

## Wo die Kapitelquellen liegen

Nicht hier und nicht in diesem Repository, sondern in
`../bibles-translations/anno-quellen/deu/l1912mod/`. Der Grund steht im README
dort: `sync_www.sh` spiegelt `bibles/` vollständig ins iOS-Bundle, die Quellen
wären hier toter Ballast. Matthäus und Markus haben keine Quellen mehr und
lassen sich nicht neu bauen.
