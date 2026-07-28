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

Die gebauten `<buchNr>_l1912mod_multi.json` entstehen bei jedem Build aus
Kapiteldateien, die **nicht im Repository** liegen, sondern im Scratchpad des
jeweiligen Agentenlaufs. Für **Matthäus und Markus sind sie verloren** — die
beiden Bücher lassen sich nicht mehr neu bauen, korpusweite Korrekturen müssen
dort direkt in der gebauten Datei erfolgen. Für die Bücher 42–66 existieren sie
zurzeit noch (rund 23 MB), aber nur in einem temporären Verzeichnis.

Ob sie ins Repository sollen, ist eine offene Entscheidung: sie verdoppeln die
Datenmenge unter `bibles/deu/l1912mod/`, sichern aber die Fähigkeit, das ganze
NT neu zu bauen. Siehe `projekt-annotation-deutsch.md`, Abschnitt „Offen".
