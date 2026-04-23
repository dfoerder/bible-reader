# Zusammenfassung Session 16./17. April 2026

## Branches

- **dev** — Hauptentwicklungsbranch
- **main** — Produktionsbranch, wird auf GitHub Pages deployed
- **automodus** — Auto-Modus Feature ausgelagert (von dev abgezweigt, enthält den vollen Auto-Modus Code)
- **french** — Französische Version (Segond), separat aufbewahrt

## Was wurde gemacht

### 1. Auto-Modus aus dev entfernt
- Der gesamte Auto-Modus Code (174 Zeilen) wurde aus `dev` entfernt
- Der Code ist auf dem Branch `automodus` vollständig erhalten
- Ziel: Die App ohne Auto-Modus erst stabil machen, bevor Auto-Modus weiterentwickelt wird

### 2. Settings-Screen eingebaut
- Erreichbar über ⚙-Symbol auf dem Nav-Screen
- Einstellungen:
  - **Vocabulary Level** (A2/B1/B2/C1)
  - **Vorlesegeschwindigkeit** (Slider + Presets)
  - **Schriftgröße** (A−/A+ Buttons, 12–30px, mit Vorschau)
  - **Fortschritt zurücksetzen**
  - **Statistik-Seite konfigurieren** (Checkboxen: Text, Vocabulary, Progress)
- Alle Einstellungen werden in localStorage gespeichert

### 3. Statistik-Seite eingebaut
- Erreichbar über 📊-Symbol auf dem Nav-Screen
- Abschnitte (ein-/ausblendbar über Settings):
  - **Text**: Bücher, Kapitel, Verse, Wörter
  - **Vocabulary Total**: Gesamtzahl unique words + Aufschlüsselung nach CEFR-Level
  - **Vocabulary pro Buch**: Jedes annotierte Buch einzeln mit unique words, Schwierigkeitsgrad und CEFR-Verteilung
  - **Your Progress**: Gelernte Wörter + Prozent

### 4. Schwierigkeitsgrad pro Buch
- Berechnung: gewichteter Durchschnitt der CEFR-Level (A1=1 bis C2=6)
- Anzeige: Score groß (z.B. 3.8), Label klein in Klammern (z.B. B1/B2)

### 5. Gesamtes NT annotiert
- **27 Bücher, 260 Kapitel, 35.105 Annotationen**
- Jedes Wort ab CEFR B1 hat: Wortform, Lemma, CEFR-Level, kontextabhängige deutsche Übersetzung
- Annotierungsskript: `annotate_nt_en.py` (nutzt Claude Sonnet API)
- `ONLY_BOOKS = None` → annotiert alle NT-Bücher

## PWA
- War bereits eingerichtet (manifest.json, sw.js, Icons)
- App kann auf dem iPhone über "Teilen → Zum Home-Bildschirm" installiert werden
- Funktioniert offline
- Update auf iPhone: Seite neu laden; bei Cache-Problemen Website-Daten für dfoerder.github.io löschen

## Aktuelle Version
- **v1.0.9b**

## Datenbestand
- `bible_nt_en.json` — World English Bible, NT
- `nt_annotations_en.json` — Wort-für-Wort Annotationen (alle 27 Bücher)

## Gespeicherte Nutzerdaten (localStorage)
- `nt-reader-state` — Phase, Level, Position, unbekannte/gelernte Wörter
- `unk-en-{buch}-{kapitel}` — Unbekannte Wörter pro Kapitel
- `tts-speed` — Vorlesegeschwindigkeit
- `nt-font-size` — Schriftgröße
- `nt-stats-visible` — Welche Statistik-Abschnitte sichtbar sind
