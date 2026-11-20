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

Entwickelt wird auf `dev` (liegt auch auf GitHub; Push auf `dev` → Vorschau unter `/bible-reader/dev/`). Deploy mit `./deploy.sh "Changelog-Zeile"` (Mac) oder der Action „Deploy (dev → main)“ (`.github/workflows/deploy.yml`, auch vom iPhone) — bumpt Version/Cache, schreibt den Log-Eintrag, merged `dev` → `main` und pusht. Details: `projekt-regeln.md`.

Für iOS-Build: `./sync_www.sh` (spiegelt root → `www/` → `ios/` via Capacitor). `www/` und `ios/` nie manuell bearbeiten.

## Bug-Melder (Testen auf dem iPhone)

Beim Testen kann auf jeder Ansicht ein 🐞-Knopf eingeblendet werden: Bug tippen,
Ansicht/Buch/Kapitel/Version/letzte JS-Fehler werden automatisch mitgespeichert.
Die Bugs liegen in `localStorage['bible-bugs']`. Ohne eingetragenen Empfänger gehen sie als vorausgefülltes GitHub-Issue raus (geht vom iPhone ohne Mac), sonst per POST an `/bugs` (bugserver.py).

- **Einschalten am Gerät:** App-URL einmal mit `?bugs=1` öffnen (bleibt an), `?bugs=0` schaltet aus.
  In einer vom Homescreen gestarteten PWA geht das nicht (eigener localStorage) — dort fünfmal auf
  die Versionszeile unten in den Einstellungen tippen; dieselben fünf Tipps schalten ihn wieder aus
- **Der komplette Reset (Entwickler-Einstellungen) lässt `bible-bugs`, `bible-bugmode` und
  `bible-bug-endpoint` als einzige Schlüssel stehen** — die Bug-Liste überlebt ihn also
- **Empfänger auf dem Mac:** `python3 bugserver.py` — serviert zugleich die App aus dem
  Repo-Root; auf dem iPhone `http://<mac-ip>:8765` öffnen, dann braucht der Sync keine Adresse
- **Eingegangene Bugs:** `bugs/bugs.json` (gitignored) — `--list` zeigt sie, `--done <id>` hakt ab,
  `--import <datei>` liest eine per AirDrop geteilte Liste ein
- **Unterwegs / Pages-Version:** `./bugtunnel.sh` — startet den Empfänger und einen
  cloudflared-Quick-Tunnel; die angezeigte `https://…trycloudflare.com/?bugs=1` auf dem iPhone
  öffnen, dann kommen App und Empfänger wieder von derselben Adresse (Auto-Upload ohne Eintrag).
  Die Tunnel-Adresse ist öffentlich und wechselt bei jedem Start.
- Nur wenn die App wirklich von GitHub Pages geladen wird, blockiert Safari den Empfänger
  (Mixed Content): dann Tunnel-Adresse ins Empfänger-Feld eintragen oder im Melder
  „Exportieren / Teilen" (AirDrop) + `bugserver.py --import` nutzen

Code: früher Script-Block (Fehler-Ringpuffer `window.__bugLog`, `?bugs=`-Schalter),
`window.__bugCtx` (von `App` gepflegt) und die Komponente `BugReporter` in `index.html`.

## Architektur

**Eine einzige Datei:** `index.html` enthält die gesamte App (React via Babel-Standalone, kein Build-Schritt). Kein Framework-Overhead, kein npm run.

**Bibeldaten getrennt von der App:** Texte, `anno/` und `train/` liegen im Repo **`dfoerder/free-bible-translations`** (GitHub Pages) und werden nicht mit der App ausgeliefert. Lokal ist `bibles/` ein **Symlink auf `../free-bible-translations`** (gitignored) — Skripte schreiben also direkt ins Daten-Repo; dort committen und pushen, die Action „Katalog für die Bibel-App“ erzeugt `catalog.json` (Version je Übersetzung) neu, die App bietet dann ein Update an. In der App: `DATA_BASE` + `dataFetch` (Cache zuerst), `loadCatalog`/`downloadTranslation`/`removeTranslation`, Komponente `TranslationManager` (Onboarding-Phase `download` nach der Bibelwahl, Einstellungen „Bibeln offline“). Caches `bd-<id>-<version>` und `bd-ondemand` überstehen Deploys (`sw.js` löscht nur `bible-full-*`). App lokal mit lokalen Daten testen: `?data=local` (zurück: `?data=remote`). Buchliste bleibt in der App: `books-index.json`. Notfall-Sicherung je Übersetzung: `backupTranslation`/`restoreBackup` (gzip-NDJSON, Kopfzeile + je Datei `{p,d}`, zeilenweise; Teilen in zwei Tipps wegen `navigator.share`).

**Daten-Laufzeit:** (Trainingsdaten gehören zur jeweiligen Bibel-Edition und liegen pro Edition unter `bibles/<edition>/train/`; die Pfade stehen in der `BIBLES`-Registry als `wordsPath`/`examplesPath`)
- `bibles/eng/web/train/words.json` — Single Source of Truth der WEB-Bibel: Vokabel-Pool + Lückentext-Übungen (5615 Wörter, `VOCAB_POOL` + `CLOZE_EXERCISES` werden daraus abgeleitet)
- `bibles/eng/web/train/examples.json` — Beispielsätze-Index (207 KB, lazy)
- `bibles/<edition>/train/lemma_freq.json` — Lemma → Vorkommen in der ganzen Bibel (lazy, `lemmaFreqPath`); erzeugt mit `python3 generate_lemma_freq.py` — nach jeder Annotationsänderung neu laufen lassen
- `bibles/` — Bibeltexte + Annotationen (`anno/`) + Trainingsdaten (`train/`) pro Buch/Edition (lazy geladen)
- **Urtext-Bibel** (`urtext`): AT hebräisch `bibles/hbo/wlc/` (STEPBible TAHOT, `convert_tahot.py`), NT griechisch `bibles/grc/n1904/` (MACULA Greek, `convert_n1904.py`). Registry-Felder `otBibleDir`/`otAnnoDir`/… laden das AT aus eigenem Verzeichnis (`bookSrc`), `otRtl` stellt das AT rechts nach links dar, `license` ersetzt „Public Domain“ in der Fusszeile. Alte ID `grc-n1904` → `BIBLE_ID_ALIASES`. Je Wort `strong`/`morph`, Glossen bisher nur `en`. Vorlesen: `otTtsLang` (he-IL, Stimme Carmit) fürs AT, sonst `ttsLang` (el-GR); `ttsCfg()` wählt nach `TTS_BOOK_NR`, `hebrewForSpeech` entfernt Akzente/Maqaf und liest יהוה als Adonai (mit Hiriq: Elohim); `greekForSpeech` macht das polytonische NT monotonisch (sonst überspringt die neugriechische Stimme Wörter wie ὁ).
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

## Hilfetexte

Philosophie: Alles, was Fragen wecken könnte, hat eine Hilfe — **ohne sichtbare Kennzeichnung**. Begriff mit
`<HelpText help={t('helpXyz')}>…</HelpText>` umschliessen; Antippen klappt die Erklärung darunter auf (in einem
`<label>` ohne den Schalter umzuschalten). Auffinden: einmaliger Tipp auf der Startseite (`bible-help-tip-seen`)
und der ?-Knopf im Kopf der Einstellungen (`flashHelpSpots` hebt alle `[data-help]` 3,5 s gelb hervor).
Lücken vermeiden: Wer gelernt hat, dass Antippen hilft, erwartet es überall.

**Begriffs-Register `TERM_HELP`** (I18N-Schlüssel des Begriffs → Hilfe-Schlüssel) und **`tl(key[, text])`**:
Begriffe, die an mehreren Stellen vorkommen, immer mit `{tl('yourLevel', stepInfo)}` statt `{t('yourLevel')…}`
ausgeben — so hat derselbe Begriff überall dieselbe Hilfe. Neuer Begriff: Eintrag in `TERM_HELP` + Hilfetext
`help…` in allen fünf Sprachen. Nie in `<button>`/`<option>`/Attributen oder in Elementen mit eigener
`onClick`-Aktion (die Hilfe würde den Tipp abfangen). Abgedeckt: Training, Level/Stufe, Lernfokus,
Übungsarten (Quiz/Im Kontext), Wiederholungen, Lernzustände (geübt/gelernt/gefestigt/sicher/vergessen/
bekannt/unbekannt/ungeübt), Antwort-Knöpfe („zu einfach“/„ich rate“), Einheiten, Vorkommen, Annotationen,
Einstufungstest, Haupt-/Hilfsbibel, Wortübersetzungen. Texte als I18N-Schlüssel `help…` in allen fünf
App-Sprachen (de/en/es/it/fr). Hilfen zu Knöpfen kommen an die Abschnittsüberschrift (z.B. „Training“: Einstufungstest + Zurücksetzen). Eingesetzt:
Startseite (Haupt-/Hilfsbibel inkl. „KI“/Urtext, Inline-Übersetzungen), Leseansicht Training-Reiter (Zähler,
Wort antippen, Glossen nach Level), Einstellungen (Bibeln offline, Einstufungstest, Grundform, Sprachlevel/CEFR,
Stufen in Übungen, Level-Anpassung, Lückentext, Fortschritt zurücksetzen, Hilfsbibel-Verse, Übersetzungen
automatisch). Früher feste Hinweistexte (`levelPolicyHint`, `germanTranslationHint`, …) sind jetzt aufklappbar.

Der Bereich „Entwickler“ in den Einstellungen erscheint nur im Test-Modus (`DEV_TOOLS` = `bible-bugmode`,
also `?bugs=1` oder fünfmal auf die Versionszeile tippen).

## Keine Browser-Dialoge

Nie `alert()`, `confirm()`, `prompt()` verwenden — immer Custom-Dialoge mit Ja/Nein-Buttons.
