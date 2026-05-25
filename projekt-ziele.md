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

### Vokabeltraining
- Alle Vokabeln aus den Bibel-Annotationen (~7.500 Wortpaare)
- Multiple-Choice: englisches Wort → deutsche Übersetzung wählen
- 15 Schwierigkeitsstufen (A1.1 bis C1.3), basierend auf Worthäufigkeit
- Adaptives System: bei <85% Erfolg wird es leichter, bei ≥85% schwieriger
- Spaced Repetition: richtig beantwortete Wörter verschwinden für 7 Tage
- Selbsteinschätzung: "zu einfach" (100 Tage Pause) und "ich rate" (Wiederholung am Ende)
- Falsch beantwortete Fragen werden am Ende der Übung wiederholt

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
