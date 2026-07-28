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

## `quellen_<buchNr>/` — Sicherungskopie der Kapitelquellen

Neu seit 28.07.2026. Die gebauten `<buchNr>_l1912mod_multi.json` entstehen bei
jedem Build aus den Kapiteldateien im Scratchpad. Für **Matthäus und Markus
sind diese Quellen verloren**, weil ihr Scratchpad nicht mehr existiert — die
beiden Bücher lassen sich nicht mehr neu bauen, und korpusweite Korrekturen
müssen dort direkt in der gebauten Datei erfolgen.

Damit das bei den noch unfertigen Büchern nicht wieder passiert, liegen ihre
bereits abgenommenen Kapitel hier als Kopie. Sie sind **nicht** unvollständig
und werden von der App genauso wenig geladen wie der Rest des Ordners; sie
existieren nur, damit ein späterer Lauf `buildbook.py` ohne den ursprünglichen
Scratchpad ausführen kann. Sobald ein Buch fertig gebaut und committet ist,
kann sein `quellen_`-Ordner weg.

## Aktueller Inhalt

| Datei | Inhalt | Stand |
|---|---|---|
| `61_ch2_verse1-11.json` | 2. Petrus 2, Verse 1–11 von 22 | Fragment, Agent am Nutzungslimit abgebrochen |
| `quellen_61/` | 2. Petrus 1 | fertig, gebaut |
| `quellen_62/` | 1. Johannes 1–3 | fertig, gebaut |
| `quellen_65/` | Judas | fertig, gebaut |

Offen sind damit: 2. Petrus 2 (ab Vers 12) und 3, 1. Johannes 4 und 5,
2. Johannes, 3. Johannes.
