# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Projekt-Dokumentation

Immer alle fünf verlinkten Dateien lesen wenn `projekt.md` geöffnet wird:
- `projekt-ziele.md` — Funktionsspezifikation und Kernlogik
- `projekt-regeln.md` — Deployment-Regeln
- `projekt-log.md` — Änderungshistorie
- `projekt-arbeitspakete.md` — Offene Aufgaben / App-Store-Checkliste
- `projekt-json-konsolidierung.md` — Datei-Architektur

## Deployment

```bash
# Entwicklung auf dev-Branch, deploy via merge nach main
git checkout main && git merge dev && git push origin main && git checkout dev
# dev wird nie direkt gepusht
```

Vor jedem Deploy: `sw.js` Cache-Name (`bible-full-vXXXX`) und `APP_VERSION` in `index.html` hochzählen. APP_VERSION immer mit `b`-Suffix (z.B. `1.10.20b`).

Für iOS-Build: `./sync_www.sh` (spiegelt root → `www/` → `ios/` via Capacitor). `www/` und `ios/` nie manuell bearbeiten.

## Architektur

**Eine einzige Datei:** `index.html` enthält die gesamte App (React via Babel-Standalone, kein Build-Schritt). Kein Framework-Overhead, kein npm run.

**Daten-Laufzeit:**
- `data/words.json` — Single Source of Truth: Vokabel-Pool + Lückentext-Übungen (5086 Wörter, `VOCAB_POOL` + `CLOZE_EXERCISES` werden daraus abgeleitet)
- `data/examples.json` — Beispielsätze-Index (207 KB, lazy)
- `bibles/` — Bibeltexte + Annotationen pro Buch (lazy geladen)
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

**Familiarity-Werte:** `-1` = ungesehen, `0` = unbekannt, `1` = bekannt, `2` = gut bekannt, `3` = sehr gut bekannt

**Session-Ablauf:** 1 Einheit = 15 Wörter → Ergebnis + ggf. Retry → Levelanpassung. "Weiter" startet neue Session.

**Wortauswahl-Priorität (laut Spec):**
1. `fam=0` + `lasttrained >24h` auf aktuellem Level (bekannte Schwächen)
2. `fam=-1` auf aktuellem Level (neue Wörter)
3. `fam=0` + `lasttrained >24h` auf höheren Levels
4. `fam=-1` auf höheren Levels

Zusätzlich: 1 ungeübtes Wort tieferer Levels pro Einheit als Beimischung.

**Levelanpassung (First-Pass-Score):** `<85%` → Step −1 · `≥85%` → Step +1 · `100%` → Step +2

**Lernfokus:**
- `level` (CEFR): `activeStep = trainStep`, Wörter aus `VOCAB_POOL[lvl]`
- `freq` (Häufigkeit): `activeStep = freqStep`, Wörter aus `FREQ_POOL` nach `freqStep`

**Häufigkeitsmodus-Abschluss:** Nach Step 17 (C2.3) → freqComplete-Screen → schrittweise Review tieferer Steps (C2.2, C2.1, …). Nach vollständigem Abschluss → freqAllDone.

## Keine Browser-Dialoge

Nie `alert()`, `confirm()`, `prompt()` verwenden — immer Custom-Dialoge mit Ja/Nein-Buttons.
