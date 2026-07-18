# Bible Reader PWA — Dokumentation

## Überblick

**Bible Reader** ist eine Progressive Web App (PWA), die deutschsprachigen Christen hilft, die englische Bibel zu lesen und dabei ihren Wortschatz zu erweitern. Die App bietet wortgenaue deutsch-englische Annotationen, Vokabeltraining und Text-to-Speech.

- **Aktuelle Version:** 1.10.76b (18.07.2026)
- **Architektur:** Single-File React-App (`index.html`, ~3000 Zeilen), kein Build-Step
- **Bibeltext:** World English Bible (WEB) — gemeinfrei
- **Deutsche Übersetzungen:** Schlachter 1951, Luther 1912 (modernisiert), Wörtliche WEB→DE-Übersetzung
- **Zielgruppe:** Deutschsprachige mit Englisch-Niveau ab A2
- **Hosting:** GitHub Pages

---

## Features

### Bibellesen

- Vollständige Bibel (66 Bücher, 1189 Kapitel)
- Wort-für-Wort Annotationen mit deutscher Übersetzung
- CEFR-Schwierigkeitsstufen (A1–C2) pro Wort
- Wörter oberhalb des Benutzerniveaus werden automatisch mit Übersetzung angezeigt — das Lese-Level ist sublevel-genau (18 Stufen A1.1…C2.3), sodass sich Text-Hervorhebung und schwierige Wörter feinstufig anpassen
- Tippen auf ein Wort zeigt die deutsche Übersetzung
- Deutsche Parallelübersetzung ein-/ausblendbar pro Vers
- Wahl zwischen 3 deutschen Übersetzungen: Schlachter 1951, Luther 1912 (modernisiert), Wörtlich (WEB→DE)
- Eigennamen mit deutschen Entsprechungen annotiert (Christ→Christus, Moses→Mose, Egypt→Ägypten)
- Automatische Lesezeichen (merkt sich Position pro Buch)
- Volltextsuche über alle 66 Bücher

### Multi-Wort-Ausdrücke

Idiome, Phrasal Verbs und feste Wendungen werden als Mehrwortausdrücke annotiert:

- **Erster Klick** auf ein Wort des Ausdrucks: zeigt die Phrase-Übersetzung (z.B. „give birth to" → „gebären")
- **Zweiter Klick**: zeigt die wörtliche Einzelwort-Übersetzung (z.B. „give" → „geben", „birth" → „Geburt")

### Text-to-Speech (TTS)

- Kapitelweise Vorlesefunktion mit Wort-für-Wort-Hervorhebung
- Einstellbare Geschwindigkeit (0.2x–1.0x)
- Einzelvers-Vorleseoption
- Übungsmodus für unbekannte Wörter

### Schwierige Wörter (kapitelweise)

- **Wörter anschauen:** Alle Wörter über dem Lese-Level werden einzeln angezeigt. Der Nutzer markiert jedes als bekannt (✓) oder unbekannt (?). Nur Wörter mit familiarity ≤ 0 werden angezeigt. ✓ setzt familiarity=1, ? setzt familiarity=0. Das Lese-Level ist ein 18-Stufen-Wert (`userStep` 0–17); ein Wort gilt als „über Level", wenn seine Sublevel-Stufe (aus `words.json` level+sub; für Wörter ohne Pool-Eintrag Fallback auf das obere Band-Ende) größer als `userStep` ist. Dadurch verschwinden die schwierigen Wörter nicht mehr schlagartig beim Eintritt in ein grobes CEFR-Band, sondern feinstufig.
- **Wörter üben:** Ein Übungsblock mit zwei umschaltbaren Übungsarten (Umschalter im Übungs-Header, geteilt mit dem allgemeinen Training via `bible-ex-mode`):
  - **Quiz:** Multiple-Choice, englisches Wort → deutsche Übersetzung.
  - **Im Kontext:** Lückentext, live aus den Versen des aktuellen Kapitels generiert — Position des Wortes im Vers, enthaltender Satz (oder ganzer Vers, per ⚙ umstellbar), Zielwort hervorgehoben; lange Sätze gekürzt, bei direkter Rede die Einleitung übersprungen, Phrasen als Ganzes.

  Beide Übungsarten nutzen dieselbe Wortauswahl (die schwierigen Wörter des Kapitels; nach „Wörter anschauen" nur die als unbekannt markierten, fam=0 vor fam=−1), denselben Lernstand und dieselbe Einheiten-/Retry-Logik (je 15 Fragen, Zwischenergebnis, Fehler-Wiederholung). Der Wechsel ist **jederzeit mitten in der Einheit** möglich; die restlichen Fragen werden in die andere Darstellung konvertiert, Fortschritt und Fehlerliste bleiben erhalten. Wörter ohne Kontextübung bleiben im Kontext-Modus als Quiz-Frage (gemischte Einheit).

### Lernfortschritt (Familiarity-System)

Jedes Wort hat einen numerischen `familiarity`-Wert (Leitner-Treppe, Wiederholungs-Intervalle siehe Klammern):
- **-1** = undefiniert (noch nie gesehen)
- **0** = unbekannt (fällig nach >24h)
- **1** = gelernt (fällig nach 2 Tagen)
- **2** = gefestigt (fällig nach 7 Tagen)
- **3** = sicher (seltene Stichprobe nach 60 Tagen)

**Zusätzliche Zähler pro Wort:**
- `learned`: Anzahl Male, die fam von 0 → >0 gewechselt hat (aktiv gelernt mit der App)
- `forgotten`: Anzahl Male, die fam von >0 → 0 gewechselt hat (vergessen)
- Wechsel von fam -1 → >0 zählt nicht als „gelernt" (Wort war bereits bekannt)

**Regeln Wörter Quiz / Wörter im Kontext:** Richtige Antwort: fam ≤ 0 → 1; fam=1 → 2 (nach >2 Tagen); fam=2 → 3 (nach >7 Tagen; zentraler Intervall-Guard in `trainWord`). Falsche Antwort → fam=0. Retry: richtig → keine Änderung, falsch → fam=0.

### Vokabeltraining

Einheitlicher Wortpool mit 5.684 Wörtern (A1–C2). Eigennamen (Level A1) sind auf die **wichtigsten mit Lernwert** kuratiert (englische Form ≠ deutsche): Bibelbuch-Autoren/Propheten, Erzväter, Könige, Apostel, Kernorte — obskure Namen (Genealogien) wurden entfernt (v1.9.53b: +710 Eigennamen ergänzt, später auf ~90 relevante reduziert):

**CEFR-Level-Quellen** (Priorität):
1. Oxford 5000 (2.654 Wörter, handkuratiert)
2. Kaggle CEFR (945 Wörter, nicht in Oxford)
3. Opus 4.7 (1.488 Wörter, unabhängig von Bibel-Kontext zugeordnet)

**Filterung:** Eigennamen, Flexionsformen, Derivationen, US/UK-Varianten, Komposita von Oxford-/Kaggle-Wörtern
- Jedes Wort hat ein `occ`-Feld (Anzahl Vorkommen in der WEB-Bibel)

**Lernfokus** (umschaltbar im Training):
- **CEFR-Level (A1→C2):** Wörter nach Schwierigkeitsstufe, von einfach nach schwer
- **Häufigkeit in der Bibel:** Wörter nach Vorkommenshäufigkeit, häufigste zuerst
- Beide Modi nutzen 18 Stufen mit separatem Step-Tracking

**Training-Mechanik (Spaced Repetition, Konzept siehe `projekt-training-konzept.md`):**
- Ein Trainings-Button mit zwei **Übungsarten** (localStorage `bible-ex-mode`): **Quiz** (englisches Wort → deutsche Übersetzung) oder **Im Kontext** (Lückentext mit Bibelvers). Beide nutzen dieselbe Wortauswahl und denselben Lernstand
- Der Übungsart-Umschalter erscheint **in der laufenden Übung** (Header) — Wechsel jederzeit mitten in der Einheit: die restlichen Fragen werden in die andere Darstellungsform konvertiert; Score, Fortschritt, Fehlerliste und Levelanpassung bleiben erhalten. Die zuletzt gewählte Übungsart wird für den nächsten Start gemerkt
- Wörter ohne Kontextübung (13 Stück) bleiben im Kontextmodus als Quiz-Frage in der Einheit (gemischte Darstellung); startet man im Kontextmodus und es sind auf einer Stufe *nur noch* solche Wörter übrig, erscheint ein Hinweis mit Wechsel-Button zum Quiz-Modus (der Level-Aufstieg misst sich immer am vollen Pool)
- 18 Schwierigkeitsstufen, zwei Lernfokus-Modi (CEFR-Level / Häufigkeit)
- Leitner-Treppe: richtige Antwort hebt fällige Wörter stufenweise (fam −1/0 → 1 → 2 → 3), falsche Antwort → fam=0 (vergessen). Gelernte Wörter kommen also wieder — nach 2 Tagen (fam=1), 7 Tagen (fam=2) bzw. als Stichprobe nach 60 Tagen (fam=3)
- Wiederholt werden **nur aktiv gelernte Wörter** (`learned` > 0, waren also mindestens einmal fam=0). Direkt als bekannt markierte Wörter (✓ bei „Wörter anschauen") oder beim ersten Versuch richtig beantwortete neue Wörter brauchen keine Festigung und bleiben draußen
- Einheiten-Mix (15 Wörter, Slots A–E, danach gemischt) — eine gemeinsame Auswahl-Funktion (`selectUnit`) für beide Übungsarten:
  - **A**: bis 4 fällige Wiederholungen (fam=1/2 mit `learned`>0, am längsten überfällige zuerst; + max. 1 fam=3-Stichprobe) — level-unabhängig
  - **B**: bis 3 fällige Unbekannte (fam=0, >24h; aktuelles + tiefere Levels), Vergessene zuerst
  - **C**: 1 ungeübtes Wort (fam=−1) tieferer Levels
  - **D**: 1 ungeübtes Wort aus Step+1
  - **E**: neue Wörter (fam=−1) des aktuellen Levels — füllt auf 15 auf; bei Knappheit Auffüllen aus A, dann B, dann C/D
- Ablauf: 15 Fragen → Zwischenergebnis mit Score → Wiederholung der Fehler → Endergebnis (First-Pass-Score + „Alle Fehler korrigiert")
- Adaptive Schwierigkeit (5-stufig): 100% = Doppelsprung (+2 Sublevels) · > 80% = +1 · 70–80% = Level halten (±0) · 40–69% = −1 · < 40% = −2. Zählt nur Wörter der Slots B/E des aktuellen Levels (A/C/D herausgerechnet); eine Anpassung erfolgt erst ab **5 gewerteten Wörtern** — kurz vor Stufen-Erschöpfung bestehen Einheiten fast nur aus Wiederholungen, und auf 1–3 Wörtern wäre die Quote reines Rauschen (Level wird dann gehalten, bis der Erschöpfungs-Aufstieg greift)
- Level-Aufstieg bei Erschöpfung: hat der aktuelle Step keine neuen und keine fälligen unbekannten Wörter mehr → automatischer Step+1 mit 🎉-Gratulations-Screen; fällige Wiederholungen blockieren den Aufstieg nicht
- Review als „Level 18": Auf der obersten Stufe (C2.3) gibt es keinen höheren Step. Wird dort eine Einheit **aufstiegswürdig** absolviert (>80% = normalerweise +1/+2), springt der Ergebnis-Screen direkt in die Review über („🎉 Oberste Stufe gemeistert!", Weiter-Button startet die erste Review-Einheit ab B2.2) — man muss also nicht erst ganz C2.3 durchüben. Bei Halten (70–80%) oder Abstieg (<70%) bleibt/sinkt das Level normal
- Nutzer-Feedback: „zu einfach" → familiarity=3, „nur geraten" → Wiederholung am Ende
- Intervall-Guard zentral in `trainWord`: Erhöhen nur nach Ablauf des Stufen-Intervalls (24h / 2 Tage / 7 Tage), Erniedrigen immer erlaubt — gilt für alle Übungspfade inkl. Kapitel-Training
- Anzeige: „X Wörter zum Üben" + „Y Wiederholungen fällig" unter dem Trainings-Button (passend zur gewählten Übungsart); dieselbe Zahl (gemeinsame Funktion `computeCounts`) erscheint auch auf dem Ergebnis-Screen nach jeder Einheit („Noch X Wörter auf dieser Stufe zu üben", bezogen auf die — nach evtl. Levelanpassung — aktuelle Stufe; bei 0 → „Alle Wörter dieser Stufe geübt!"). Fortschritts-Panel schlüsselt Bekannt nach Stufen auf (gelernt/gefestigt/sicher)
- Abschluss (oberste Stufe C2.3 erreicht): **Review-Phase** über die restlichen ungeübten Wörter, geordnet nach **CEFR-Nützlichkeit** (nicht nach Häufigkeit) — Reihenfolge als Zickzack-Spirale um B2.2 (die nützlichsten Wörter zuerst): `B2.2, B2.3, B2.1, C1.1, B1.3, C1.2, B1.2, C1.3, B1.1, C2.1, A2.3, C2.2, A2.2, C2.3, A2.1, A1.3, A1.2, A1.1` (`REVIEW_ORDER`/`reviewNextStep`). Jedes CEFR-Sublevel wird in 15er-Einheiten vollständig durchgearbeitet, bevor zum nächsten gewechselt wird; gilt für beide Fokus-Modi, Anzeige als CEFR-Label. Fällige Wiederholungen (Slot A) laufen auch in der Review mit (wie im normalen Training), damit während der langen Review-Phase Gelerntes nicht verblasst. Sobald alle Wörter familiarity ≥ 1 haben → freqAllDone
  - **Nur heute offene Wörter je Sublevel:** ein Sublevel gilt als „für heute erledigt", wenn nur noch fam=0-Wörter übrig sind, die heute schon geübt wurden — der Intervall-Guard lässt sie am selben Tag ohnehin nicht auf fam≥1 steigen (sonst drehte sich dasselbe Wort endlos, `reviewCount`/`currentUnexercised` filtern fam=-1 ODER fam=0-mit-Frist-abgelaufen). Sind alle heutigen Wörter durch, aber noch nicht alles fam≥1 → Meldung „Für heute geschafft" (`freqDoneToday`), morgen geht es weiter
  - **Review-Phase ist persistent** (`bible-review-step` in localStorage, gesetzt/gelöscht via `setReviewStep`): sie überlebt „Beenden" und App-Neustart. Solange die Review läuft, setzt der Trainings-Button die Review fort (statt eine normale C2.3-Einheit zu starten, die per Levelanpassung wieder unter das Top-Level absenken könnte). Der Marker wird erst gelöscht, wenn alles fam≥1 ist (freqAllDone)
  - **Review folgt der gewählten Übungsart** (`startReview`): im Quiz-Modus normale Vokabel-Einheit, im Kontext-Modus dieselbe Review-Wortauswahl als Lückentext dargestellt (Wörter ohne Kontextübung bleiben Quiz — gemischte Einheit). Die Auswahl bleibt identisch zur Quiz-Auswahl, damit `reviewCount` und tatsächliche Einheit übereinstimmen (sonst Endlosschleife). So bleibt „Im Kontext" auch über Einheiten-Grenzen hinweg erhalten

### Einstufungstest

- 30 Multiple-Choice-Fragen (6×5, A1–C2) zur Bestimmung des CEFR-Niveaus
- Ergebnis: A1 bis C2; setzt auch die Trainingsstufen (`bible-train-step`, `bible-freq-step`)
- Passt die Vokabelanzeige automatisch an
- Jederzeit wiederholbar in den Einstellungen

### Statistiken

- Bücher, Kapitel, Verse, Wörter pro Buch
- Schwierigkeitsbewertung pro Buch (gewichteter CEFR-Durchschnitt)
- CEFR-Verteilung der Vokabeln mit Sublevel-Aufschlüsselung (Oxford 5000 und Bibel-Vokabular getrennt)
- Min–max Vorkommen pro Level in der Bibel (z.B. „1–56.635×")
- Lernfortschritt: bekannte/unbekannte/nicht gesehene Wörter, gelernte und vergessene Wörter
- **Wortstatistik pro Buch:** 📊-Icon neben jedem Buchnamen in der Navigation. Zeigt beim Klick: Kapitelanzahl, Wörter gesamt, noch nicht angeschaut, bekannte Wörter (davon neu gelernt), unbekannte Wörter (davon vergessen). Annotationen werden lazy geladen.

---

## Technische Architektur

### Dateistruktur

```
bible-reader/
├── index.html                         Haupt-App (React + Babel, ~3000 Zeilen)
├── sw.js                              Service Worker (Offline-Caching)
├── manifest.json                      PWA-Manifest
├── icon-192.png / icon-512.png        App-Icons
├── lib/                               React, ReactDOM, Babel (lokal gebündelt)
├── sync_www.sh                        Spiegelt root → www/ → ios/ (Capacitor), vor jedem iOS-Build
├── www/ · ios/                        Capacitor-Ableitungen (gitignored, nie manuell bearbeiten)
├── bibles/
│   ├── index.json                     Buch-Metadaten und Statistiken
│   ├── eng/web/
│   │   ├── {nr}_web.json              Bibeltext (66 Dateien)
│   │   ├── anno/
│   │   │   └── {nr}_web_deu.json      Annotationen (66 Dateien)
│   │   └── web_deu/
│   │       └── {nr}_web_deu.json      Wörtliche DE-Übersetzung (66 Dateien)
│   ├── deu/
│   │   ├── sch1951/                   Schlachter 1951 (66 Dateien)
│   │   ├── sch1951mod/                Schlachter modernisiert (vorbereitet für v2)
│   │   └── l1912mod/                  Luther 1912 modernisiert (66 Dateien)
│   └── fra/ · ita/ · spa/             lsg1910, riv1927, rv1909 (+ mod-Varianten) —
│                                      vorbereitet für Version 2, von der App noch nicht genutzt
├── data/
│   ├── words.json                     Single Source of Truth: Vokabel-Pool + Lückentext-
│   │                                  Übungen (5.684 Wörter; VOCAB_POOL + CLOZE_EXERCISES
│   │                                  werden daraus abgeleitet)
│   ├── examples.json                  Beispielsätze-Index (Lemma → Vers-Referenzen, 207 KB, lazy)
│   └── vocab_pool.json / context_exercises.json   Lokale Build-Intermediates (gitignored)
├── generate_training_data.js          Generiert words.json aus Annotationen
│                                      (Oxford 5000 + Kaggle + Opus CEFR-Abgleich, Filterung)
├── generate_pos.py / generate_deform.py / generate_examples.py
│                                      Ergänzen pos / deForm+form / examples.json (Opus Batch)
├── oxford_5000.csv                    Oxford 5000 Referenzliste (extern)
├── kaggle_cefr.csv                    Kaggle CEFR Referenzliste (8.653 Wörter, extern)
├── opus_cefr_levels.json              Opus 4.7 CEFR-Zuordnung (1.488 Wörter)
├── review_annotations.py              Annotations-Review (Claude API, synchron)
├── review_batch_submit.py             Batch-Review einreichen (Anthropic Batch API)
├── review_batch_collect.py            Batch-Ergebnisse abholen und validieren
├── review_common.py                   Shared Logic (Prompt, Validierung)
├── dokumentation.md                   Diese Dokumentation
├── projekt-ziele.md                   Projektziele
├── projekt-regeln.md                  Git-Workflow- und Deployment-Regeln
├── projekt-arbeitspakete.md           Arbeitspakete / App-Store-Checkliste
├── projekt-log.md                     Entwicklungsprotokoll
└── projekt-json-konsolidierung.md     Datei-Architektur / Konsolidierungsplan
```

### Annotationsformat

Jedes Wort im Bibeltext erhält eine Annotation mit Position, Form, Lemma, CEFR-Stufe und deutscher Übersetzung:

```json
{
  "chapters": {
    "1": {
      "21": [
        {"pos": 0, "form": "She", "lemma": "she", "level": "A1", "de": "Sie"},
        {"pos": 2, "pos_end": 4, "form": "give birth to", "lemma": "give birth to", "level": "B1", "de": "gebären"},
        {"pos": 2, "form": "give", "lemma": "give", "level": "A1", "de": "geben", "phrase": 2},
        {"pos": 3, "form": "birth", "lemma": "birth", "level": "B1", "de": "Geburt", "phrase": 2},
        {"pos": 4, "form": "to", "lemma": "to", "level": "A1", "de": "zu", "phrase": 2}
      ]
    }
  }
}
```

**Felder:**

| Feld | Beschreibung |
|------|-------------|
| `pos` | 0-basierter Wortindex im Vers |
| `pos_end` | Endposition bei Mehrwortausdrücken |
| `form` | Wortform wie im Text |
| `lemma` | Grundform |
| `level` | CEFR-Stufe (A1–C2) |
| `de` | Deutsche Übersetzung (kontextbezogen) |
| `phrase` | Position der zugehörigen Phrase-Annotation (nur bei Einzelwort-Annotationen innerhalb einer Phrase) |

**Eigennamen:** Im **Bibeltext** sind alle Eigennamen (Personen, Orte) annotiert — immer Level A1. Deutsche Entsprechungen werden verwendet: Christ→Christus, Moses→Mose, Egypt→Ägypten, Isaiah→Jesaja. Namen ohne Änderung (Jesus, Abraham) erhalten die gleiche Form als `de`. Im **Lernwortpool** (`words.json`) steht dagegen nur eine kuratierte Auswahl der wichtigsten Namen mit Lernwert (en ≠ de) — obskure Namen aus Genealogien sind nicht enthalten.

### PWA und Offline-Fähigkeit

- **Service Worker** (`sw.js`): Network-first für HTML, Cache-first für Daten
- **Cache-Name:** `bible-full-vXXXX` (aktuell `bible-full-v2031`, wird bei jedem Deploy hochgezählt)
- Vollständige Offline-Nutzung nach erstem Laden
- Automatisches Update bei neuer Version

### Lokale Datenspeicherung (LocalStorage)

| Schlüssel | Inhalt |
|-----------|--------|
| `bible-reader-state` | Phase, Lese-Level (`userStep` 0–17, sublevel-genau), Position, Wortlisten |
| `bible-ui-lang` | UI-Sprache (de/en) |
| `bible-view-mode` | Ansichtsmodus (phone/desktop) |
| `bible-layout` | Theme/Layout (classic/icf/icf-light) |
| `bible-de-trans` | Gewählte deutsche Übersetzung (sch1951/l1912mod/web_deu) |
| `bible-word-data` | Wortdaten pro Wort ({familiarity, lasttrained, numberoftrainings, learned, forgotten}) |
| `bible-word-data-backups` | Liste zeitgestempelter Lernstand-Backups (Entwickler-Werkzeug „Test-Daten laden"; max. 12, ältestes wird bei Speicherüberlauf verworfen). Jedes Backup ist ein vollständiger Snapshot: Wortdaten, Lese-Level (`userStep`) samt Wortlisten, Trainingsstufen, Lernfokus, Übungsart, Trainingshistorie und Kapitel-Markierungen (`unk-*`/`rev-*`). Migriert den früheren Einzel-Slot `bible-word-data-backup` (nur Wortdaten). |
| `bible-test-accel` | Beschleunigter Test-Modus (Entwickler-Einstellungen): alle Lern-Fristen ÷96 (unbekannt 15 min · gelernt 30 min · gefestigt 105 min · sicher 15 h) und nur ¼ des Wortpools (pro Level/Sublevel jedes 4. Wort — Level-Verhältnisse bleiben erhalten). Wirkt beim App-Laden; ⚡-Hinweis im Training. |
| `bible-train-focus` | Lernfokus im Training ('level'/'freq') |
| `bible-ex-mode` | Übungsart im Training ('quiz'/'cloze') |
| `bible-train-step` | Aktuelle Trainingsstufe CEFR-Modus (0–17) |
| `bible-freq-step` | Aktuelle Trainingsstufe Häufigkeits-Modus (0–17) |
| `bible-training-history` | Trainingshistorie (letzte 200) |
| `bible-level-tested` | Einstufungstest absolviert |
| `bible-bookmarks` | Lesezeichen pro Buch |
| `bible-font-size` / `-tr` / `-ex` | Schriftgrößen (Bibeltext / Übersetzungen / Übungen) |
| `bible-cloze-ctx` | Lückentext-Kontext (Satz / ganzer Vers) |
| `bible-show-lemma` / `bible-show-cefr` | Anzeige-Optionen beim Lesen |
| `bible-show-ex-level` | Zeigt in den Übungen neben dem Wort CEFR-Sublevel + Häufigkeitsstufe (1–18) |
| `bible-stats-visible` | Sichtbare Statistik-Abschnitte |
| `unk-{lang}-{buch}-{kapitel}` | Unbekannte Wörter pro Kapitel |
| `tts-speed` | TTS-Geschwindigkeit |

### Deutsche Übersetzungen

Drei deutsche Parallelübersetzungen stehen zur Auswahl (einstellbar unter Einstellungen):

| Übersetzung | Pfad | Format |
|-------------|------|--------|
| **Schlachter 1951** (Standard) | `bibles/deu/sch1951/` | Dict (`{"chapters":{"1":{"1":"Text",...},...}}`) |
| **Luther 1912 (modernisiert)** | `bibles/deu/l1912mod/` | Dict (wie Schlachter) |
| **Wörtlich WEB→DE** | `bibles/eng/web/web_deu/` | Array (`{"chapters":[{"number":1,"verses":[{"n":1,"text":"..."}]}]}`) — wird zur Laufzeit normalisiert |

Die wörtliche Übersetzung (`web_deu`) wird automatisch aus den Annotationen generiert: Phrase-Übersetzungen werden bevorzugt, Einzelwort-Übersetzungen als Fallback, Satzzeichen aus dem englischen Quelltext übernommen.

### Themes

- **Warm** (Standard, `classic`): Beige/Braun-Palette
- **ICF Dark** (`icf`): Dunkler Hochkontrast-Modus
- **ICF Light** (`icf-light`): Heller, cleaner Modus

Gespeichert im localStorage-Schlüssel `bible-layout`.

---

## Annotierungs-Workflow

Die Annotationen werden mit Claude (Opus 4.7) erstellt und verbessert. Der Prompt in `review_common.py` ist die zentrale Quelle für alle Annotierungsregeln.

### Einzelnes Kapitel reviewen (synchron)

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
export REVIEW_MODEL=claude-opus-4-7
python3 review_annotations.py 40 1    # Matthäus Kapitel 1
```

### Batch-Review (50% günstiger, empfohlen für ganze Bücher)

```bash
REVIEW_MODEL=claude-opus-4-7 python3 review_batch_submit.py 40 41 42  # Bücher einreichen
python3 review_batch_collect.py --wait                                 # Ergebnisse abholen
```

### Vollständiger Workflow für neue Annotationen

1. **Batch-Review** mit Opus 4.7 (Anthropic Batch API, 50% Rabatt)
2. **Eigennamen annotieren** — alle Personen- und Ortsnamen mit deutschen Entsprechungen
3. **Transparente Phrasal Verbs entfernen** — z.B. „came out", „went up" (funktionieren wörtlich)
4. **Wörtliche DE-Übersetzung generieren** (`web_deu`) — aus Annotationen zusammengesetzt
5. **sw.js Cache-Version bumpen** und deployen

**Buchnummern:** 1–39 = AT, 40 = Matthäus, 41 = Markus, 42 = Lukas, 43 = Johannes, ... 66 = Offenbarung

### Kosten

Das Review aller 66 Bücher kostete ca. $1.500 (Batch API mit 50% Rabatt, Opus 4.7).

---

## Deployment

Entwicklung auf Branch `dev`, Deploy mit `./deploy.sh "Changelog-Zeile"`: bumpt `APP_VERSION`/`APP_DATE` (index.html) und `CACHE_NAME` (sw.js), schreibt den Changelog-Eintrag nach `projekt-log.md`, aktualisiert den Versionskopf dieser Dokumentation, merged `dev` → `main` und pusht (GitHub Pages).

Die Version trägt bis auf Weiteres den Suffix `b` (Beta).

---

## Installation

### Smartphone (empfohlen)

- **iOS:** Safari → Teilen → „Zum Home-Bildschirm"
- **Android:** Chrome → Menü → „App installieren"

### Desktop

- Direkt im Browser unter der GitHub-Pages-URL nutzbar
- Chrome/Edge: Adressleiste → Installations-Symbol

---

## Statistiken

- **66 Bücher** mit vollständigen Annotationen (reviewt mit Opus 4.7)
- **755.526 Wörter** im Bibeltext
- **~30.000 Eigennamen-Annotationen** mit deutschen Entsprechungen
- **5.087 einzigartige Lemmata** (nach Filterung und Zusammenführung)
- **Einheitlicher Vokabelpool:** 5.684 Wörter (A1: 1.063, A2: 548, B1: 798, B2: 1.503, C1: 1.208, C2: 564) — Eigennamen auf die wichtigsten mit Lernwert kuratiert (obskure entfernt, fehlende wichtige wie Moses/Jeremiah/Elia ergänzt)
- **CEFR-Quellen:** Oxford 5000 (2.654), Kaggle CEFR (945), Opus 4.7 (1.488); Rest: Eigennamen und Pool-Erweiterungen (v1.9.53b–58b)
- **3 deutsche Übersetzungen:** Schlachter 1951, Luther 1912 mod, Wörtlich WEB→DE
