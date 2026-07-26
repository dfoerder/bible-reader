# Angefangene Kapitel (nicht von der App geladen)

Hier liegen **unvollständige** Kapitel-Fragmente der deutschen Annotation —
Teilarbeit aus Agentenläufen, die durch Verbindungsabbrüche beendet wurden.
Sie stehen hier, damit sie nicht verlorengehen, und werden von der App nie
geladen: `index.html` holt ausschließlich `<buchNr>_l1912mod_multi.json`.

## Format

Dateiname `ch<kapitel>_verse<von>-<bis>.json`, Inhalt `{"<vers>": [<eintraege>]}`
— dasselbe Format, das die Agenten nach `scratchpad/.../out/<buchNr>/` liefern.

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

| Datei | Buch | Kapitel | Verse | Einträge | fehlt noch |
|---|---|---|---|---|---|
| `ch1_verse1-30.json` | Lukas (42) | 1 | 1–30 von 80 | 604 | 31–80 |
| `ch12_verse1-20.json` | Lukas (42) | 12 | 1–20 von 59 | 486 | 21–59 |
| `ch22_verse1-8.json` | Lukas (42) | 22 | 1–8 von 71 | 136 | 9–71 |
