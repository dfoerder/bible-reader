# Bible Reader PWA — Dokumentation

## Überblick

**Bible Reader** ist eine Progressive Web App (PWA), die deutschsprachigen Christen hilft, die englische Bibel zu lesen und dabei ihren Wortschatz zu erweitern. Die App bietet wortgenaue deutsch-englische Annotationen, Vokabeltraining und Text-to-Speech.

- **Aktuelle Version:** 1.5.4b (26.05.2026)
- **Architektur:** Single-File React-App (`index.html`, ~2100 Zeilen), kein Build-Step
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
- Wörter oberhalb des Benutzerniveaus werden automatisch mit Übersetzung angezeigt
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

- **Wörter anschauen:** Alle Wörter über dem CEFR-Level werden einzeln angezeigt. Der Nutzer markiert jedes als bekannt (✓) oder unbekannt (?). Nur Wörter mit familiarity ≤ 0 werden angezeigt. ✓ setzt familiarity=1, ? setzt familiarity=0.
- **Wörter im Kontext üben:** Cloze-Übungen mit Sätzen aus dem Kapitel. Das schwierige Wort wird im Satz hervorgehoben, der Nutzer wählt die richtige deutsche Übersetzung aus drei Optionen. Aufgeteilt in Lerneinheiten zu je 15 Fragen. Phrasen werden als Ganzes ersetzt, Einzelwörter innerhalb von Phrasen übersprungen.
- **Wörter Quiz:** Multiple-Choice-Quiz mit den unbekannten Wörtern. Wird die Review-Übung übersprungen, werden alle Wörter über dem Level trainiert. Aufgeteilt in Lerneinheiten zu je 15 Fragen mit Zwischenergebnis, Fehler-Wiederholung und Einheitsergebnis.

### Lernfortschritt (Familiarity-System)

Jedes Wort hat einen numerischen `familiarity`-Wert:
- **-1** = undefiniert (noch nie gesehen)
- **0** = unbekannt
- **1** = bekannt
- **2** = gut bekannt
- **3** = sehr gut bekannt

**Regeln Wörter Quiz / Wörter im Kontext:** Richtige Antwort: fam ≤ 0 → 1; fam > 0 + lasttrained > 2 Tage + fam ≤ 2 → fam+1. Falsche Antwort → fam=0. Retry: richtig → keine Änderung, falsch → fam=0.

### Vokabeltraining

- Multiple-Choice-Quiz: englisches Wort → deutsche Übersetzung
- 15 Schwierigkeitsstufen (A1.1 bis C1.3)
- Adaptive Schwierigkeit: < 85% Erfolg = leichter, ≥ 85% = schwerer, 100% = Doppelsprung (+2 Sublevels)
- Priorisierte Wortauswahl (15 Wörter pro Übung):
  1. familiarity=0 + lasttrained >24h auf dem aktuellen Step-Level
  2. familiarity=-1 auf dem aktuellen Step-Level
  3. familiarity=0 + lasttrained >24h auf höheren Levels
  4. familiarity=-1 auf höheren Levels
- Wörter mit familiarity ≥ 1 erscheinen nicht mehr im Training
- Ablauf: 15 Fragen → Zwischenergebnis mit Score → Wiederholung der Fehler → Endergebnis (First-Pass-Score + „Alle Fehler korrigiert")
- Level-Anpassung basiert auf dem First-Pass-Score (nicht aufgeblähtem Retry-Score)
- Nutzer-Feedback: „zu einfach" → familiarity=3, „nur geraten" → Wiederholung am Ende

### Einstufungstest

- 30 Multiple-Choice-Fragen zur Bestimmung des CEFR-Niveaus
- Ergebnis: A1, A2, B1, B2 oder C1
- Passt die Vokabelanzeige automatisch an
- Jederzeit wiederholbar in den Einstellungen

### Statistiken

- Bücher, Kapitel, Verse, Wörter pro Buch
- Schwierigkeitsbewertung pro Buch (gewichteter CEFR-Durchschnitt)
- CEFR-Verteilung der Vokabeln
- Lernfortschritt (% gelernter Lemmata)

---

## Technische Architektur

### Dateistruktur

```
bible-reader/
├── index.html                         Haupt-App (React + Babel, ~2100 Zeilen)
├── sw.js                              Service Worker (Offline-Caching)
├── manifest.json                      PWA-Manifest
├── icon-192.png / icon-512.png        App-Icons
├── bibles/
│   ├── index.json                     Buch-Metadaten und Statistiken
│   ├── eng/web/
│   │   ├── {nr}_web.json              Bibeltext (66 Dateien)
│   │   ├── {nr}_web_deu_parallel.json Schlachter-Paralleltext (66 Dateien)
│   │   ├── anno/
│   │   │   └── {nr}_web_deu.json      Annotationen (66 Dateien)
│   │   └── web_deu/
│   │       └── {nr}_web_deu.json      Wörtliche DE-Übersetzung (66 Dateien)
│   └── deu/
│       ├── sch1951/                    Schlachter 1951 (66 Dateien)
│       └── l1912mod/                   Luther 1912 modernisiert (66 Dateien)
├── data/
│   ├── vocab_pool.json                7.500+ Wortpaare für Training
│   └── context_exercises.json         Lückentext-Übungen
├── review_annotations.py              Annotations-Review (Claude API, synchron)
├── review_batch_submit.py             Batch-Review einreichen (Anthropic Batch API)
├── review_batch_collect.py            Batch-Ergebnisse abholen und validieren
├── review_common.py                   Shared Logic (Prompt, Validierung)
├── dokumentation.md                   Diese Dokumentation
├── projekt-ziele.md                   Projektziele
├── projekt-regeln.md                  Git-Workflow-Regeln
├── projekt-arbeitspakete.md           Arbeitspakete
└── projekt-log.md                     Entwicklungsprotokoll
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

**Eigennamen:** Alle Eigennamen (Personen, Orte) sind annotiert — immer Level A1. Deutsche Entsprechungen werden verwendet: Christ→Christus, Moses→Mose, Egypt→Ägypten, Isaiah→Jesaja. Namen ohne Änderung (Jesus, Abraham) erhalten die gleiche Form als `de`.

### PWA und Offline-Fähigkeit

- **Service Worker** (`sw.js`): Network-first für HTML, Cache-first für Daten
- **Cache-Name:** `bible-full-v154`
- Vollständige Offline-Nutzung nach erstem Laden
- Automatisches Update bei neuer Version

### Lokale Datenspeicherung (LocalStorage)

| Schlüssel | Inhalt |
|-----------|--------|
| `bible-reader-state` | Phase, Level, Position, Wortlisten |
| `bible-ui-lang` | UI-Sprache (de/en) |
| `bible-view-mode` | Ansichtsmodus (phone/desktop) |
| `bible-de-trans` | Gewählte deutsche Übersetzung (sch1951/l1912mod/web_deu) |
| `bible-word-data` | Familiarity-Daten pro Wort ({familiarity, lasttrained, numberoftrainings}) |
| `bible-train-step` | Aktuelle Trainingsstufe |
| `bible-training-history` | Trainingshistorie (letzte 200) |
| `unk-en-{book}-{chapter}` | Unbekannte Wörter pro Kapitel |
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

- **Warm** (Standard): Beige/Braun-Palette
- **ICF Dark**: Dunkler Hochkontrast-Modus
- **ICF Light**: Heller, cleaner Modus

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

1. Entwicklung auf Branch `dev`
2. `APP_VERSION` in `index.html` und `CACHE_NAME` in `sw.js` hochzählen
3. Merge `dev` → `main`
4. Push nach GitHub (GitHub Pages)

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
- **6.376 einzigartige Lemmata**
- **CEFR-Verteilung:** A1 (624), A2 (907), B1 (2.312), B2 (2.988), C1 (2.254), C2 (1.557)
- **7.500+ Wortpaare** im Vokabeltraining
- **3 deutsche Übersetzungen:** Schlachter 1951, Luther 1912 mod, Wörtlich WEB→DE
