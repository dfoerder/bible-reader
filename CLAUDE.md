# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Projekt-Dokumentation

Immer alle sechs verlinkten Dateien lesen wenn `projekt.md` geöffnet wird:
- `projekt-ziele.md` — Funktionsspezifikation und Kernlogik
- `projekt-regeln.md` — Deployment-Regeln
- `projekt-log.md` — Änderungshistorie
- `projekt-arbeitspakete.md` — Offene Aufgaben / App-Store-Checkliste
- `projekt-json-konsolidierung.md` — Datei-Architektur
- `projekt-annotation-deutsch.md` — Deutsche Annotation (l1912mod → en/es/fr/it)

## Deployment

Deploy mit `./deploy.sh "Changelog-Zeile"` — bumpt Version/Cache, schreibt den Log-Eintrag, merged `dev` → `main` und pusht. `dev` wird nie direkt gepusht. Details: `projekt-regeln.md`.

Für iOS-Build: `./sync_www.sh` (spiegelt root → `www/` → `ios/` via Capacitor). `www/` und `ios/` nie manuell bearbeiten.

## Architektur

**Eine einzige Datei:** `index.html` enthält die gesamte App (React via Babel-Standalone, kein Build-Schritt). Kein Framework-Overhead, kein npm run.

**Daten-Laufzeit:** (Trainingsdaten gehören zur jeweiligen Bibel-Edition und liegen pro Edition unter `bibles/<edition>/train/`; die Pfade stehen in der `BIBLES`-Registry als `wordsPath`/`examplesPath`)
- `bibles/eng/web/train/words.json` — Single Source of Truth der WEB-Bibel: Vokabel-Pool + Lückentext-Übungen (5615 Wörter, `VOCAB_POOL` + `CLOZE_EXERCISES` werden daraus abgeleitet)
- `bibles/eng/web/train/examples.json` — Beispielsätze-Index (207 KB, lazy)
- `bibles/` — Bibeltexte + Annotationen (`anno/`) + Trainingsdaten (`train/`) pro Buch/Edition (lazy geladen)
- `localStorage` — Nutzerstand: `bible-word-data`, `bible-freq-step`, `bible-train-step`, `bible-train-focus`, `bible-reader-state`, u.a.

**Globale JS-Variablen (nach words.json-Load):**
- `VOCAB_POOL` — `{A1:[...], A2:[...], ..., C2:[...]}` — nach CEFR-Level
- `FREQ_POOL` — alle Wörter nach Häufigkeit sortiert, jedes mit `.freqStep` (0–17)
- `CLOZE_EXERCISES` — Lückentext-Übungen nach CEFR-Level
- `SUBSTEPS` — 18 Einträge: `['A1.1', 'A1.2', ..., 'C2.3']`

**React-Komponenten (in index.html):**
- `App` — Haupt-Component, verwaltet Phase (`nav`, `training`, `settings`, `stats`, `leveltest`, `quiz`), `wordData`, `userLevel`
- `Training` — Vokabeltraining, verwaltet `trainFocus` ('level'|'freq'), `trainStep`, `freqStep`, `activeStep`, alle Übungs-States
- `LevelTest` — Einstufungstest

## Vokabeltraining-Kernlogik

Die verbindliche Beschreibung der Trainingslogik (Familiarity-System, Wortauswahl, Levelanpassung, Session-Ablauf, Lernfokus-Modi, Abschluss-Flows) steht in `dokumentation.md` → Abschnitte „Lernfortschritt (Familiarity-System)" und „Vokabeltraining". Dort pflegen — hier nicht duplizieren.

## Keine Browser-Dialoge

Nie `alert()`, `confirm()`, `prompt()` verwenden — immer Custom-Dialoge mit Ja/Nein-Buttons.
