# Projekt-Log

## Branches

- **dev** — Hauptentwicklungsbranch
- **main** — Produktionsbranch, wird auf GitHub Pages deployed
- **automodus** — Auto-Modus Feature ausgelagert (von dev abgezweigt)
- **french** — Französische Version (Segond), separat aufbewahrt

## v1.10.43b (05.07.2026)

- Dev-Werkzeug 'Frischer Start': alles ungeübt ab Startstufe — sauberer Ausgangspunkt für beschleunigte Tests (ohne synthetische Verteilung)

## v1.10.42b (05.07.2026)

- Beschleunigter Test-Modus (Entwickler): alle Lern-Fristen ÷96 (24h→15min), nur ¼ des Wortpools mit erhaltenen Level-Verhältnissen

## v1.10.41b (05.07.2026)

- Test-Backups sichern jetzt den vollständigen Lernstand (Stufen, Lernfokus, Lese-Level, Historie, Kapitel-Markierungen) statt nur der Wortdaten

## v1.10.40b (05.07.2026)

- Test-Backups zeitgestempelt: mehrere Backups statt einem Slot, Auswahl beim Wiederherstellen (Entwickler-Werkzeug)

## v1.10.39b (05.07.2026)

- Übungsart-Umschalter (Quiz / Im Kontext) zentriert unter dem Titel

## v1.10.38b (05.07.2026)

- Kapitel-Training vereinheitlicht: Wörter Quiz + Wörter im Kontext zu einem 'Wörter üben'-Block mit Übungsart-Umschalter (Wechsel mitten in der Einheit)

## v1.10.37b (03.07.2026)

- Lese-Level jetzt sublevel-genau (18 Stufen) — Kapitel-Übungen und Wort-Hervorhebung unterscheiden C2.1/C2.2/C2.3 statt nur grobes C2

## v1.10.36b (03.07.2026)

- Übungsart-Umschalter (Quiz / Im Kontext) in die laufende Übung verlegt — Wechsel jederzeit mitten in der Einheit

## v1.10.35b (03.07.2026)

- Einheitliches Training: ein Button mit Übungsart-Umschalter (Quiz / Im Kontext), gemeinsame Wortauswahl für beide Übungsarten

## v1.10.34b (03.07.2026)

- Wiederholungen nur für aktiv gelernte Wörter (learned>0) — per ✓ markierte Wörter werden nicht mehr wiederholt

## v1.10.33b (03.07.2026)

- Training 2.0: Spaced Repetition — Leitner-Treppe (Wiederholungen nach 2/7/60 Tagen), neuer Einheiten-Mix, automatischer Level-Aufstieg, Wiederholungs-Zähler und Stufen-Panel

## v1.9.43b – v1.10.31b (18.–23.06.2026) — Sammel-Eintrag

Rekonstruiert am 03.07.2026 aus der Git-History (Commit-Messages bis v1.9.77b, danach Deploy-Diffs), da das Log in diesem Zeitraum nicht geführt wurde. ~90 deployte Versionen, thematisch zusammengefasst:

### Trainingslogik: Wortauswahl umgebaut (v1.9.78b–v1.10.20b)
- **v1.9.78b — Kernumbau:** Die alte 4-Stufen-Priorität (aktuelles + *höhere* Levels) ersetzt durch drei gemischte Quellen: `unknown24h` (fam=0, >24h), `lowerUnexercised` (fam=-1 *tieferer* Levels, 1 pro Einheit als Beimischung), `currentUnexercised` (fam=-1 aktueller Step). Höhere Levels werden nicht mehr einbezogen. Einheiten-Aufbau: max. 3 unknown24h am Anfang + 1 tieferes Wort, Rest neue Wörter
- v1.9.82b–v1.9.88b: mehrfach iteriert (Beimischung nur noch Bonus, fam<1-Erweiterung wieder zurückgenommen)
- v1.9.93b: fam=0-Wörter tieferer Levels (>24h) fließen im CEFR-Modus zusätzlich in den unknown24h-Pool
- v1.10.19b/20b: Session erst auf 2, dann auf genau **1 Einheit (15 Wörter)** gekappt — Levelanpassung nach jeder Session (gemäß Spec)

### Levelanpassung: 5-stufiges Delta-System (v1.10.24b)
- **v1.10.24b:** Neue Regeln — vorher `<85%` → −1 · `≥85%` → +1 · `100%` → +2; neu: `100%` → +2 · `>80%` → +1 · `70–80%` → ±0 · `40–69%` → −1 · `<40%` → −2 (geklemmt auf Step 0–17)
- v1.9.81b: Beigemischte Lower-Level-Wörter werden aus der Prozentrechnung herausgerechnet (`adjTotal`)
- v1.10.23b: `userLevel` wird auch im Frequenz-Modus bei Levelwechsel aktualisiert (konsistente Lese-Schwierigkeit)
- v1.10.30b: Bugfix — `reviewModeRef`-Reset in startCloze (Levelanpassung wurde nach Review-Session bei Cloze übersprungen)

### Abschluss- und Review-Flow (v1.9.85b–v1.10.12b)
- v1.9.85b: freqComplete-/freqAllDone-Screens eingeführt (nach C2.3 Weitermachen mit ungeübten Wörtern tieferer Stufen)
- v1.9.88b: Umbau auf schrittweisen Review pro Step (nächsttieferer Step mit fam<1-Wörtern), ohne Levelanpassung
- v1.9.94b/97b: `nowords`-Screen im CEFR-Modus, bietet Weitermachen mit tieferem Level an
- v1.10.12b: Abschluss-Flow greift auch im CEFR-Modus nach Step 17 (C2.3)
- Feinschliffe: freqComplete-Trigger präzisiert (v1.9.91b/92b), Done-Screen nach Review übersprungen (v1.9.96b), reviewMode für alle Fokus-Modi (v1.9.98b), Gratulation nur auf oberstem Level + „Review läuft"-Hinweis (v1.10.9b–11b)

### Cloze-Übungen angeglichen (v1.10.25b–29b)
- Session auf 1 Einheit gekappt (v1.10.25b), Pool im CEFR-Modus über VOCAB_POOL-Lemmata vereinheitlicht (v1.10.26b), Empty-Pool-Handling wie Vokabeln → nowords-Screen (v1.10.28b/29b)

### Vokabelpool erweitert: 5.086 → 5.878 Wörter
- v1.9.53b: **+710 Eigennamen** in den Trainingspool
- v1.9.54b–58b: Namens-Adjektive, Kurzwort-Filter auf 1 Zeichen, -ful/-less/-ment/-ity als eigenständige Wörter, vocab-only-Wörter (ohne Cloze)
- danach: US-Schreibvarianten (+12), partielle DE-Übersetzungen in Annotationen gefixt (+9) → 5.878
- Datenqualität: Annotationsfehler bereinigt (Em-Dashes, /f-Genusmarker, +/Zahlen-Lemmata, v1.9.57b); `opus_deform.json`/`opus_pos_levels.json` für den erweiterten Pool aktualisiert
- Neue Verteilung: A1 1.257 · A2 548 · B1 798 · B2 1.503 · C1 1.208 · C2 564

### Einstufungstest
- C2 ergänzt: 6×5 Fragen (A1–C2), Scoring und Ergebnisanzeige angepasst
- Test setzt jetzt auch `bible-train-step` und `bible-freq-step`; Skip-Button → „Abbrechen"
- v1.9.83b: Wörter-Level-Picker aus den Einstellungen entfernt; Default-Level B2 → B1; v1.10.17b: Fortschritts-Reset setzt userLevel auf B1 zurück

### Session-Ergebnis und Zähler
- v1.9.43b–47b: Session-Gesamtergebnis über Runden hinweg, „Einheit X von Y", Einheiten werden vorab gebaut
- Zähler „verfügbare Wörter" mehrfach exakt an den tatsächlichen Trainingspool angeglichen (v1.9.79b–95b, v1.10.27b); v1.9.84b: globalTotal zählt nur geübte Wörter
- v1.10.21b/22b: „X/Y gelernt"-Fortschrittsanzeige unter Vokabel-/Cloze-Button; v1.10.31b: Done-Screen zeigt aktuelles Level immer an; v1.10.8b: numerische Step-Anzeige im Frequenz-Modus

### UI-Bereinigung
- Statistikseite: „Dein Fortschritt"-Sektion entfernt, „Nicht gesehen" → „Ungeübt", Schwierigkeit aus Buchstatistik entfernt
- „Wörter im Kontext nach Buch"-Button von der Trainingsseite entfernt
- Kopf-Bild (kopf.jpg/kopf2.jpg) statt Brain-Emoji in den Trainings-Buttons, Icongrößen angepasst
- Beschriftungen präzisiert („Wörter zum Üben auf deinem Level" u.a.)

### Werkzeuge
- `deploy.sh`: automatischer Version-/Datum-/Cache-Bump beim Deploy
- Test-Daten-Loader in den Einstellungen (simulierte Familiarity-Verteilungen mit Backup, v1.9.99b–v1.10.18b iteriert)
- `CLAUDE.md` mit Codebase-Guidance angelegt

## App Store Plan (18.06.2026)

Detaillierte Checkliste für die App-Store-Einreichung in `projekt-arbeitspakete.md` festgehalten:
- **Design & Assets:** Icon (alle Größen), Launch Screen, Screenshots (6.7"/6.5"/5.5"), Preview-Video
- **Apple Developer Setup:** Account (99$/Jahr), App Store Connect, Bundle ID `de.biblereader.app`, Signing
- **Metadaten:** Name/Beschreibung DE+EN, Keywords, Datenschutzerklärung, Support-URL, Altersfreigabe (4+), Kategorie Bildung/Bücher
- **Technisch:** Tip-Jar via StoreKit (1.99/4.99/9.99 $), Spendenhinweis bei Sprachpaket-Downloads, Gerätetest, Barrierefreiheit (Dynamic Type, VoiceOver)
- **TestFlight & Review** → Veröffentlichung → danach Android/Play Store

## v1.9.42b (18.06.2026)

### Fortschritt-Statistik ins Training verschoben
- Fortschritt-Unterabschnitt aus den Einstellungen entfernt (Reset-Knopf bleibt)
- Neues 📊-Icon neben dem Titel „Training" — öffnet Modal mit vollständiger Fortschritt-Statistik (Geübt/Bekannt/Unbekannt/Ungeübt + Aufschlüsselung) und Reset-Knopf; Klick außerhalb schließt es
- Bugfixes: Panel musste innerhalb des `phase==='training'`-early-return-Blocks stehen (sonst nicht gerendert); Icon-Ausrichtung via Flex-Zeile statt absoluter Positionierung

## v1.9.38b (18.06.2026)

### Bugfix: Leerer Bildschirm nach Reload
- `parseInt(null)` gibt `NaN` zurück wenn `bible-train-step`/`bible-freq-step` noch nie im localStorage gesetzt wurden
- `NaN != null` ist in JavaScript `true` → `stepToLevel(NaN)` wurde aufgerufen → `SUBSTEPS[NaN] = undefined` → `.split('.')` TypeError → React-Render crashte → leerer Bildschirm nach „Loading data…"
- Fix: `!isNaN()` Guard statt `!= null` (eingeführt in v1.9.37b)

## v1.9.37b (18.06.2026)

### Bugfixes

#### Familiarity steigt nicht mehr durch Retry in derselben Session
- **Bug:** Wort falsch beantwortet → am Ende der Übung nochmals richtig beantwortet → Familiarity wurde auf 1 gesetzt und als „gelernt" gezählt
- **Fix:** 24h-Regel direkt in `trainWord` verankert: Familiarity kann nur erhöht werden, wenn `lasttrained` null oder >24h zurückliegt. Erniedrigen (falsche Antwort → 0) ist immer erlaubt. Gilt zentral für alle Pfade.

#### „Unter deinem Niveau" zeigte 0 nach Trainings-Aufstieg
- **Bug:** Im Frequenz-Modus wird `userLevel` beim Aufsteigen nicht aktualisiert → `belowLevel` war immer 0
- **Fix:** `globalWordStats` nimmt jetzt das höchste der drei Level-Quellen: `userLevel`, `stepToLevel(trainStep)` (Level-Modus), `stepToLevel(freqStep)` (Frequenz-Modus) — jeweils aus LS gelesen

## v1.9.34b (18.06.2026)

### Lernfortschritt-Statistik überarbeitet
- **Fortschritt** ist jetzt ein Unterabschnitt von Training (kein eigenständiger Bereich)
- Neue Gliederung: Geübt (= Bekannt + Unbekannt) · Ungeübt (= alle Wörter − Geübt)
  - Bekannt → davon gelernt (fam 0→>0)
  - Unbekannt → davon vergessen (fam >0→0)
  - Ungeübt aufgeteilt in: unter deinem Niveau (wahrscheinlich bekannt) / auf und über deinem Niveau (eventuell unbekannt) — berechnet aus VOCAB_POOL + userLevel, passt sich automatisch bei Level-Änderung an

### Ergebnisscreen: gelernt vs. geübt
- Nach Cloze-Übungen: „X gelernt" (grün, fam 0→>0) und „Y geübt" (fam -1→>0) separat angezeigt
- `preFam`-Snapshot beim Start der Übung für alle drei Cloze-Pfade (allgemein, Buch, Kapitel)

### Cloze-Wortauswahl verbessert
- Kapitel-Cloze priorisiert jetzt fam=0 (bekannte Schwächen) vor fam=-1 (neue Wörter) — wie allgemeine und Buch-Cloze bereits

### Schriftgrösse
- Bereich „Schriftgröße" mit Unterabschnitten Bibeltext / Übersetzungen / Übungen
- Separate Schriftgröße für Übungstexte (Default = Bibeltext-Größe)
- Bibeltext-Default auf 16 px (Kindle-Standard)

## v1.9.30b (18.06.2026)

### Übungs-Features und Verbesserungen
- **POS-Distraktoren überall einheitlich**: `posWrongDe` zu gemeinsamem `formWrong`-Helfer ausgebaut, der Wortart **und** Form (Numerus/Tempus) matcht — gilt jetzt für alle 8 Distraktoren-Stellen (allgemeine + kapitelspezifische Cloze, Wiederholung, Retry)
- **Kapitel-Cloze angeglichen**: `clozeFormOf`-Helfer leitet Form-Kategorie (sg/pl/pres/past/part) aus englischer Wortform + Lemma ab; `genOpts` nutzt jetzt denselben `formWrong`-Pool
- **Kontext-Einstellung**: Schalter „Satz | Ganzer Vers" im Kapitel-Lückentext (Inline-Panel im Abschnitt **und** im laufenden Training neben dem Titel)
- **„Weitere Beispiele für \<wort\>"**: Bei falscher Antwort in beiden Cloze-Übungen; schlanker Refs-Index (207 KB, `data/examples.json`), Verstext on-the-fly via `fetchBook`; Einzelbeispiel-Stepper mit „Nächstes Beispiel" + „Zurück"
- **Separate Schriftgröße für Übungstexte**: Einstellungsbereich „Schriftgröße" mit Unterabschnitten Bibeltext / Übersetzungen / Übungen; Bibeltext-Default auf 16 px (Kindle-Standard)

### Datenqualität
- **Flexions-Übersetzungen** (`deForm`/`form`): Via Opus-Batch für alle 5086 Wörter erzeugt — Lückentext zeigt/prüft jetzt flektierte Form (Männer, kamen), Distraktoren passen in Numerus/Tempus; behebt nebenbei Lemma-Fehler (be→„sein", tell→„erzählen")
- **Randzeichen-Bereinigung**: Satzzeichen (incl. typografische Quotes), Bindestrich-Präfixe aus `answer`/`de` entfernt; 16 Präfix-Fragmente per Opus + Review durch saubere Grundformen ersetzt (`fix_hyphen_de.py`)

## v1.9.9b (17.06.2026)

### JSON-Konsolidierung: vocab_pool + context_exercises → words.json
- Befund: Die beiden Datendateien waren eine perfekte 1:1-Bijektion (5.086 Wörter, identische `de`/`pos`/`sub`/`level`)
- Zu einer Single Source of Truth `data/words.json` zusammengeführt (1 Eintrag/Wort, alle Felder)
- `index.html` lädt jetzt **einen** Fetch und leitet daraus `VOCAB_POOL` + `CLOZE_EXERCISES` (mit `lemma`-Alias) ab
- ~23 % kleiner (1.214 KB → 935 KB), ein Fetch statt zwei
- `generate_training_data.js` (Phase 4) und `generate_pos.py` schreiben jetzt `words.json`
- Alt-Dateien als lokale Build-Intermediates gitignored; Verifikation per Round-trip + Node-Simulation der App-Ladelogik (Feld-für-Feld-Gleichheit)
- Teil eines größeren Konsolidierungsplans → siehe [[projekt-json-konsolidierung]]

### Konsolidierungs-Aufräumarbeiten (AP1/AP2)
- Legacy-Datenblobs in `alt/` (~37 MB, unreferenziert) aus dem Git-Tracking entfernt, gitignored
- `sync_www.sh` ergänzt: spiegelt root → `www/` → `ios/` reproduzierbar (`npx cap sync`); behebt Drift zwischen Quelle und Capacitor-Bundle. Root ist alleinige Quelle, `www/`/`ios/` reine Ableitungen

### Repo-History bereinigt (Wartung)
- `git filter-repo`: 15 unreferenzierte Legacy-Datenpfade aus der gesamten History aller Branches entfernt
- **`.git`: 116 MB → 38 MB** (−67 %); `alt/`-Provenienz-Skripte und App-Daten unangetastet
- `main`-Tip-Inhalt unverändert (nur SHAs neu) → GitHub-Pages-Seite identisch; `main` force-gepusht
- Lokale Branches (`dev`/`automodus`/`french`/`multilingual`) haben neue SHAs → ein evtl. Zweit-Klon müsste neu geklont werden
- Werkzeuge gitignored: `rewrite_history.sh`, `purge_paths.txt`; Original-Backup als Tar gesichert

## v1.9.8b (17.06.2026)

### Wortarten (POS) für alle Vokabeln
- Für alle 5.086 Cloze-Lemmata via Opus Batch API die Wortart bestimmt (`pos`-Feld)
- POS-Tagging-Skripte `generate_pos.py` (Submit/Poll/Write) und `resume_pos.py` (laufenden Batch fortsetzen)

### POS-basierte Distraktoren
- Lückentext-Distraktoren bevorzugen jetzt die **gleiche Wortart** wie das Zielwort
- Bei zu wenigen gleichartigen Kandidaten Auffüllung mit beliebigen Wörtern
- `DE_POS`/`EN_POS`-Lookup-Maps und `posOf()` in `index.html`

## v1.9.7b (07.06.2026)

### Bugfix: Luther 1912 mod nicht ausklappbar
- Bei gewählter Übersetzung „Luther 1912 mod" ließ sich der deutsche Vers nicht über Klick auf die Versnummer ausklappen (bei Schlachter funktionierte es)
- Ursache: Die 66 `bibles/deu/l1912mod/`-Dateien waren nie committet/deployt → Fetch lieferte 404, `deBook` blieb null, Versnummer nicht klickbar
- Fix: l1912mod-Daten committet und deployt (App-Logik war korrekt)

## v1.9.6b (07.06.2026)

### Bugfix: Doppelte Wörter nach Level-Anhebung
- Bei „Wörter anschauen" erschienen nach dem Anheben des Levels bereits angeschaute Wörter erneut
- Ursache: Review-Index wurde auf 0 zurückgesetzt, während die neu berechnete (kleinere) `quizWords`-Liste an den Anfang sprang
- Fix: Fortsetzung an der Anzahl der bereits angeschauten Wörter, die im neuen Level verbleiben — Review läuft mit dem ersten noch nicht gesehenen Wort weiter
- `reviewCheckBase` ebenfalls auf den neuen Index gesetzt (korrekter 20-Wörter-Schwellenwert für den nächsten Level-Vorschlag)

## v1.9.5b (05.06.2026)

### Einheitlicher Vokabelpool
- Zwei-Pool-System (Oxford + Bibel) durch einen einzigen Pool ersetzt
- 1.488 Bibel-Wörter durch Opus 4.7 unabhängig CEFR-Level zuordnen lassen (nicht im Bibelkontext, sondern allgemeines Englisch)
- Level-Priorität: Oxford 5000 > Kaggle CEFR > Opus 4.7 > Annotations-Level
- Inflektionsfilter prüft jetzt auch gegen Kaggle-Wörter (nicht nur Oxford)
- Einheitlicher Pool: 5.086 Wörter (Oxford: 2.654, Kaggle: 945, Opus: 1.488)

### Annotations-Levels angeglichen
- Alle 66 Annotations-Dateien an die neuen CEFR-Levels angepasst (Oxford/Kaggle/Opus)
- 142.501 von 772.783 Annotationen aktualisiert
- Lesen und Training zeigen jetzt konsistente Levels

### Lernfokus-Einstellung
- Umschalter im Training: „CEFR-Level (A1→C2)" oder „Häufigkeit in der Bibel"
- Frequenz-Modus: 5.086 Wörter nach Bibel-Häufigkeit sortiert, in 18 Stufen aufgeteilt
- Separater Step-Tracker für jeden Modus
- Zeigt Wörteranzahl pro Stufe im Frequenz-Modus

### UI-Bereinigung
- Bibel-Vokabular-Sektion aus dem Training entfernt
- Separater Step-Tracker (`bibleStep`) und `exSourceRef` entfernt
- Statistikseite zeigt nur noch einen Pool
- Service Worker cacht keine bible_vocab/bible_exercises mehr

### EFLLex entfernt
- EFLLex als CEFR-Referenz entfernt (zu verrauscht, z.B. „moor" als A1 aus einzelnem Graded Reader)

## v1.9.4b (04.06.2026)

### Kaggle CEFR als zweite Referenz
- Kaggle-CEFR-Wortliste (8.653 Wörter, davon 4.338 nicht in Oxford 5000) als Fallback für Bibel-Wörter
- 421 Level-Anpassungen bei Bibel-Wörtern durch Kaggle

### EFLLex als dritte CEFR-Referenz (wieder entfernt in v1.9.5b)
- EFLLex-Wortliste (15.280 Lemmata aus Graded Readers) als Fallback
- Mindest-Schwellenwert: nur Wörter mit ≥3 Dokumenten
- Level-Priorität: Oxford 5000 > Kaggle > EFLLex > Annotations-Level

### Erweiterte Filterung
- US/UK-Schreibvarianten: -or→-our (auch interior), -ize→-ise
- Derivationssuffixe: -ness, -ful, -less, -ment, -ity, -ous, -ings, -y (Adjektiv)
- Kompositum-Erkennung mit min. 3 Buchstaben pro Teil und Ausnahmeliste für Scheinkomposita (forsake, bondage, perverse etc.)
- Basisformen: Wort + -d/-ed/-ing ergibt Oxford-Eintrag → filtern
- Reflexivpronomen (oneself), eigennamenbezogene Adjektive (jewish, egyptian etc.), caesar
- Case-Varianten zusammengeführt: "After"+"after" → "after" (Eigennamen-Check auf häufigste Originalschreibung)

### Occurrence Counts und Statistik
- Jedes Wort in beiden Pools hat jetzt ein `occ`-Feld (Anzahl Vorkommen in der WEB-Bibel)
- Statistikseite zeigt min–max Vorkommen pro Level (z.B. „1–56.635×")

### Aktuelle Zahlen
- Oxford 5000: 2.654 Wörter (A1–C1)
- Bibel-Vokabular: 2.327 Wörter (A1–C2, davon 421 Kaggle-korrigiert)

## v1.9.3b (04.06.2026)

### Oxford 5000 CEFR-Abgleich
- Vokabeln mit Oxford 5000 Liste verglichen und alle übereinstimmenden Wörter auf Oxford-CEFR-Level angepasst
- 1514 von 2708 Wörtern level-korrigiert, 0 Mismatches
- `compare_levels.js` als Analyseskript erstellt

### Zwei-Pool-Vokabelsystem (Oxford + Bibel)
- Vokabular aufgeteilt in Oxford 5000 (2708 allgemeine Wörter, A1–C1) und Bibel-spezifisch (2665 Wörter, B1–C2)
- Eigene Datendateien: `bible_vocab.json` und `bible_exercises.json`
- Separate Trainings-UI mit eigenem Step-Tracking (`bibleStep`)
- `exSourceRef` zur Unterscheidung des aktiven Pools während Übungen
- `maxStepFor(src)` begrenzt Level-Progression pro Pool

### Bibel-Vokabel-Filterung
- Irreguläre Verbformen über IRREGULAR_MAP (~60 Einträge) erkannt
- Reguläre Flexionen über Suffix-Stripping (-s, -ed, -ing, -er, -est, -ly, -en, -th)
- Eigennamen-Erkennung über Präfix-Ähnlichkeit mit y/j-Äquivalenz
- Gefiltert: Eigennamen, Leerzeichen, Sonderzeichen, kurze Wörter, zusammengesetzte Zahlen, fehlende Übersetzungen, Kontraktionen, Groß-/Kleinschreibungsvarianten, Teilübersetzungen, flektierte Formen, Reflexivpronomen, eigennamenbezogene Adjektive, Oxford-Wörter mit Bindestrich

### Sublevel-Aufschlüsselung in Statistik
- Vokabelstatistik zeigt Wörter aufgeschlüsselt nach Sublevel für Oxford und Bibel

### Vereinfachte Trainingsanzeige
- Info-Text zeigt nur noch „N Wörter verfügbar" statt „N von M (X Einheiten)"

### Cloze-Bug behoben
- Lückentext-Übung blieb bei letzter Frage hängen wenn Retry pending war
- Familiarity-Lookup nutzte Wortform statt Lemma

## v1.7.0b (02.06.2026)

### C2-Sublevels im Vokabeltraining
- 2.101 C2-Lemmata aus den Bibel-Annotationen in `vocab_pool.json` aufgenommen
- 3 Sublevels (C2.1, C2.2, C2.3) nach Häufigkeit, insgesamt nun 18 Schwierigkeitsstufen
- Step-Maximum dynamisch aus SUBSTEPS-Array statt hardcoded

## v1.6.0b (29.05.2026)

### Kapitel-Lückentext-Übungen (Wörter im Kontext üben)
- Lückentext-Übungen aus den Versen des aktuellen Kapitels generiert
- Schwieriges Wort im Satz hervorgehoben, 3 deutsche Übersetzungsoptionen
- Phrasen werden als Ganzes ersetzt, Einzelwörter innerhalb von Phrasen übersprungen
- Lerneinheiten zu je 15 Fragen mit Zwischenergebnis und Fehler-Wiederholung
- Nutzt die bestehende chapTrain-Infrastruktur mit `type:'cloze'`-Flag

### Learned/Forgotten-Zähler
- Pro Wort: `learned` (+1 bei fam 0→>0), `forgotten` (+1 bei fam >0→0)
- Wechsel fam -1→>0 zählt nicht als „gelernt" (Wort war bereits bekannt)
- Rückwärtskompatibel zu bestehenden Wortdaten

### Wortstatistik pro Buch und global
- Globaler Lernfortschritt: bekannte, unbekannte, nicht gesehene, gelernte und vergessene Wörter
- Pro-Buch-Statistik über 📊-Icon neben jedem Buchnamen in der Navigation
- Zeigt: Kapitelanzahl, Wörter gesamt, noch nicht angeschaut, bekannte (davon neu gelernt), unbekannte (davon vergessen)
- Annotationen werden lazy geladen beim ersten Öffnen der Statistik
- Kapitelanzahl neben dem Buchnamen entfernt (wird in Statistik angezeigt)

### UI-Umbenennung und Neuordnung
- „Wörter trainieren" → „Wörter Quiz"
- Reihenfolge im Vocab-Panel: Wörter anschauen → Wörter im Kontext üben → Wörter Quiz
- Am Kapitelende nur „Wörter Quiz"-Link

## v1.5.4b (26.05.2026)

### Familiarity-System (Lernfortschritt)
- Wortdaten von String-basiertem `learnstatus` auf numerisches `familiarity`-System migriert
- Werte: -1 (undefiniert), 0 (unbekannt), 1 (bekannt), 2 (gut bekannt), 3 (sehr gut bekannt)
- Rückwärtskompatible Migration bestehender localStorage-Daten beim App-Start
- Review-Buttons (✓/?) setzen familiarity auf 1 bzw. 0
- Training: Spaced-Repetition-Regeln mit 2-Tage-Schwelle für Levelaufstieg
- Retry-Durchgang: richtig → keine Änderung, falsch → familiarity = 0

### Familiarity-Priorisierung im Vokabeltraining
- Wortauswahl nach 4-Stufen-Priorität: fam=0 auf Level → fam=-1 auf Level → fam=0 höher → fam=-1 höher
- 7-Tage-Cooldown-System (`bible-vocab-log`) durch Familiarity-Filterung ersetzt
- „Zu einfach" setzt familiarity=3 (statt 100-Tage-Cooldown)
- Richtig → familiarity=1, falsch → familiarity=0
- Wörter mit familiarity ≥ 1 erscheinen nicht mehr im Training
- 100% richtig → Doppelsprung (+2 Sublevels), ≥85% → +1 Sublevel
- Zwischenergebnis nach 15 Fragen mit Score, dann Wiederholung der Fehler
- Endergebnis zeigt First-Pass-Score + „Alle Fehler korrigiert"

### Lerneinheiten für Kapitel-Training
- „Wörter Quiz" teilt die Übung in Einheiten zu je 15 Fragen auf
- Ablauf pro Einheit: 15 Fragen → Zwischenergebnis → Wiederholung der Fehler → Einheitsergebnis mit „Wiederholen"/„Weiter"
- Einheitsanzeige im Quiz-Header („Einheit X von Y")
- Nur unbekannte Wörter werden trainiert (nach „Schwierige Wörter anschauen")
- Wird die Review-Übung übersprungen, werden alle Wörter über dem Level trainiert

## v1.5.3b (23.05.2026)

### Opus 4.7 Review aller 66 Bücher
- Alle Annotationen mit Opus 4.7 über Batch API reviewt (~$1.500)
- Transparente Phrasal Verbs entfernt (z.B. "came out", "went up")
- ~30.000 Eigennamen mit deutschen Entsprechungen annotiert
- Annotations-Prompt in `review_common.py` als Single Source of Truth

### Wörtliche DE-Übersetzung (web_deu)
- 66 JSON-Dateien unter `bibles/eng/web/web_deu/`
- Automatisch aus Annotationen generiert (Phrase-Übersetzungen bevorzugt)
- Satzzeichen aus englischem Quelltext übernommen

### Übersetzungswahl in Einstellungen
- 3 deutsche Übersetzungen: Schlachter 1951, Luther 1912 mod, Wörtlich WEB→DE
- Auswahl in Einstellungen, wirkt auf die einblendbare Parallelübersetzung
- Verschiedene Dateiformate werden zur Laufzeit normalisiert

### Weitere Änderungen
- Home-Button führt wieder zur echten Startseite (nicht "zurück zum Lesen")
- Versionsnummer mit Datum (dd.mm.yyyy) in der App angezeigt
- review_common.py: Eigennamen-Annotation als Pflicht im Prompt verankert

## v1.5.2b und früher

### Volltextsuche
- Suche über alle 66 Bücher mit Kontext und Hervorhebung

### Luther 1912 modernisiert (l1912mod)
- Komplette modernisierte Luther-Bibel unter `bibles/deu/l1912mod/`
- Stil: würdevoll aber klar, kurze Sätze

### Batch-Review-Skripte
- `review_batch_submit.py` — Bücher an Anthropic Batch API senden
- `review_batch_collect.py` — Ergebnisse abholen und validieren
- `review_common.py` — Shared Logic (Prompt, Validierung)

### Multi-Wort-Ausdrücke
- Idiome und Phrasal Verbs als Mehrwortausdrücke annotiert
- Zwei-Klick-Feature: erst Phrase-Übersetzung, dann Einzelwörter

### Vokabeltraining
- 15 Schwierigkeitsstufen, adaptives System
- Spaced Repetition, Selbsteinschätzung

### TTS (Text-to-Speech)
- Kapitel/Vers vorlesen mit Wort-Hervorhebung
- Geschwindigkeit anpassbar, Übungsmodus

### Einstufungstest
- CEFR-Einstufung (A1–C1) per Multiple-Choice

### PWA
- Service Worker mit Network-first (HTML) und Cache-first (Daten)
- Offline nutzbar nach erstem Laden
- Installierbar auf iOS und Android

## v1.0.9b (April 2026)

### Initiale Version
- Settings-Screen (Level, TTS-Geschwindigkeit, Schriftgröße)
- Statistik-Seite (Text, Vocabulary, Progress)
- Gesamtes NT annotiert (27 Bücher)
- Auto-Modus auf eigenen Branch ausgelagert
