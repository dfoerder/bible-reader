# Projekt-Log

## Branches

- **dev** — Hauptentwicklungsbranch
- **main** — Produktionsbranch, wird auf GitHub Pages deployed
- **automodus** — Auto-Modus Feature ausgelagert (von dev abgezweigt)
- **french** — Französische Version (Segond), separat aufbewahrt

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

### Lerneinheiten für Kapitel-Training
- „Schwierige Wörter trainieren" teilt die Übung in Einheiten zu je 15 Fragen auf
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
