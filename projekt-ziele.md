# Englisch mit der Bibel — Projektziele

## Vision

### Fernziel: 
Eine ios app, die Christen hilft, durch das Lesen der Bibel in Fremdsprachen, ihre Sprachkenntnisse zu verbessern und ihren Glauben zu vertiefen. Die App richtet sich an die Christen der ganzen Welt. 

### Erstes Teilziel 1. Version:
Eine ios App, die deutschsprachigen Christen hilft, durch das Lesen der Bibel in Englisch, ihre Englischkenntnisse zu verbessern und ihren Glauben zu vertiefen.

## Zielgruppe
### Zielgruppe Fernziel
- Christen mit Grundkenntnissen in einer Fremdsprache (ab ca. A2)
- Alter und technisches Niveau breit gestreut — die App muss einfach und intuitiv sein

#### Zielgruppe erstes Teilziel
- Deutschsprachige Christen mit Englisch-Grundkenntnissen (ab ca. A2)
- Alter und technisches Niveau breit gestreut — die App muss einfach und intuitiv sein

## Kernfunktionen der 1. Version

### Bibel lesen
- Komplette englische Bibel (WEB — World English Bible, 66 Bücher)
- Wort-für-Wort-Annotationen mit deutschen Übersetzungen
- Schwierige Wörter nach CEFR-Level (A1–C1) farblich markiert
- Antippen eines Wortes zeigt die deutsche Übersetzung
- Deutsche Parallelübersetzung (Schlachter 1951) versweise einblendbar
- Lesezeichen pro Buch — merkt sich automatisch Kapitel und Vers

### Vorlesen (Text-to-Speech)
- Kapitel vorlesen mit Wort-für-Wort-Hervorhebung
- Geschwindigkeit anpassbar (0.2x bis 1.0x), auch während des Vorlesens
- Einzelne Verse oder ganze Kapitel vorlesbar
- Unbekannte Wörter separat üben (Aussprache)

### Schwierige Wörter (kapitelweise)
- **Schwierige Wörter anschauen**: alle Wörter über dem CEFR-Level des Nutzers werden einzeln angezeigt (englisch + deutsche Übersetzung). Der Nutzer markiert jedes Wort als bekannt (✓) oder unbekannt (?). Dieser Schritt bestimmt, welche Wörter trainiert werden.
- **Schwierige Wörter trainieren**: Multiple-Choice-Quiz (englisch → deutsch) mit den unbekannten Wörtern des Kapitels. Wird die Review-Übung übersprungen, werden alle Wörter über dem Level trainiert, da noch nicht bekannt ist, welche der Nutzer kann. Die Übung wird in Lerneinheiten zu je 15 Fragen aufgeteilt. Ablauf pro Einheit:
  1. 15 Fragen beantworten
  2. Zwischenergebnis: „X von 15 richtig"
  3. Falls Fehler: Ankündigung und Wiederholung der falsch beantworteten Fragen
  4. Einheitsergebnis mit Buttons „Wiederholen" (Einheit nochmals) und „Weiter" (nächste Einheit). Bei der letzten Einheit: „Beenden" statt „Weiter".

### Lernfortschritt (Familiarity-System)
Jedes Wort hat einen numerischen `familiarity`-Wert, der den Lernstand abbildet:
- **-1** = undefiniert (noch nie gesehen)
- **0** = unbekannt
- **1** = bekannt
- **2** = gut bekannt
- **3** = sehr gut bekannt

**Regeln bei „Schwierige Wörter anschauen":**
- Nur Wörter mit familiarity ≤ 0 werden angezeigt
- ✓ (bekannt) → familiarity = 1
- ? (unbekannt) → familiarity = 0
- `lasttrained`-Timestamp wird gesetzt

**Regeln bei „Schwierige Wörter trainieren":**
- Nur Wörter mit familiarity ≤ 0 werden trainiert
- Richtige Antwort (erster Durchgang):
  - familiarity ≤ 0 → familiarity = 1
  - familiarity > 0 und `lasttrained` > 2 Tage zurück und familiarity ≤ 2 → familiarity + 1
- Falsche Antwort → familiarity = 0
- Wiederholungsdurchgang (Retry): richtig → keine Änderung, falsch → familiarity = 0

### Vokabeltraining
- Alle Vokabeln aus den Bibel-Annotationen (~7.500 Wortpaare)
- Multiple-Choice: englisches Wort → deutsche Übersetzung wählen
- 15 Schwierigkeitsstufen (A1.1 bis C1.3), basierend auf Worthäufigkeit
- Adaptives System: bei <85% Erfolg wird es leichter, bei ≥85% schwieriger, bei 100% Doppelsprung (+2 Sublevels)
- Priorisierung der Wortauswahl (15 Wörter pro Übung):
  1. familiarity=0 + lasttrained >24h auf dem aktuellen Step-Level (bekannte Schwächen)
  2. familiarity=-1 auf dem aktuellen Step-Level (neue Wörter)
  3. familiarity=0 + lasttrained >24h auf höheren Levels (Schwächen darüber)
  4. familiarity=-1 auf höheren Levels (neue Wörter darüber)
- Wörter mit familiarity ≥ 1 werden nicht mehr trainiert
- Selbsteinschätzung: „zu einfach" → familiarity=3, „ich rate" → Wiederholung am Ende
- Richtig beantwortet → familiarity=1, falsch → familiarity=0
- Ablauf: 15 Fragen → Zwischenergebnis mit Score → Wiederholung der Fehler → Endergebnis (First-Pass-Score + „Alle Fehler korrigiert")
- Level-Anpassung basiert auf dem First-Pass-Score

### Sprachtest
- Einstufungstest beim ersten Start (Multiple-Choice, Englisch → Deutsch)
- Bestimmt das CEFR-Niveau und passt Vokabelprüfung und Training an
- Jederzeit in den Einstellungen wiederholbar

### Suche
- Volltextsuche über alle 66 Bücher der Bibel
- Treffer mit Kontext und Hervorhebung
- Direktnavigation zum gefundenen Vers


## Technische Grundsätze

- **Eine einzige HTML-Datei** — kein Build-Schritt, kein Framework-Overhead
- **Progressive Web App (PWA)** — installierbar auf iPhone/Android, offline nutzbar
- **Daten in JSON-Dateien** — Bibeltexte, Annotationen, Vokabelpool
- **localStorage** für Benutzereinstellungen, Lesezeichen, Lernfortschritt
- **Zweisprachige Oberfläche** — Deutsch (Standard) und Englisch wählbar
- **Responsive Design** — funktioniert auf Handy, Tablet und Desktop
- **GitHub Pages** als Hosting

## Offene Ideen / Nächste Schritte

- Lückentext-Übungen (Cloze) für mehr Bücher ausbauen
- Lesefortschritt-Statistiken erweitern
- Teilen von Versen / Lesezeichen
- iOS App Store (Capacitor-Bündelung)

## 2. Version (Multilingual)
### Weitere Sprachen (Bibeltexte)
- Spanisch: Reina-Valera 1909 (Original + modernisierte Version)
- Deutsch: Schlachter 1951 (Original + modernisierte Version)
- Modernisierung: archaische Wörter durch verständlichere ersetzt, per Skript reproduzierbar
