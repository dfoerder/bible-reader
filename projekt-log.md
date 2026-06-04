# Projekt-Log

## Branches

- **dev** — Hauptentwicklungsbranch
- **main** — Produktionsbranch, wird auf GitHub Pages deployed
- **automodus** — Auto-Modus Feature ausgelagert (von dev abgezweigt)
- **french** — Französische Version (Segond), separat aufbewahrt

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
