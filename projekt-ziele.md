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
- Deutsche Parallelübersetzung (Luther 1912, modernisiert) versweise einblendbar
- Lesezeichen pro Buch — merkt sich automatisch Kapitel und Vers

### Vorlesen (Text-to-Speech)
- Kapitel vorlesen mit Wort-für-Wort-Hervorhebung
- Geschwindigkeit anpassbar (0.2x bis 1.0x), auch während des Vorlesens
- Einzelne Verse oder ganze Kapitel vorlesbar
- Unbekannte Wörter separat üben (Aussprache)

### Schwierige Wörter (kapitelweise)
- **Wörter anschauen**: alle Wörter über dem CEFR-Level des Nutzers werden einzeln angezeigt (englisch + deutsche Übersetzung). Der Nutzer markiert jedes Wort als bekannt (✓) oder unbekannt (?). Dieser Schritt bestimmt, welche Wörter trainiert werden.
- **Wörter im Kontext üben**: Lückentext-Übungen mit Sätzen aus dem Kapitel. Das schwierige Wort wird im Satz hervorgehoben, der Nutzer wählt die richtige deutsche Übersetzung aus drei Optionen. Aufgeteilt in Lerneinheiten zu je 15 Fragen.
- **Wörter Quiz**: Multiple-Choice-Quiz (englisch → deutsch) mit den unbekannten Wörtern des Kapitels, in Lerneinheiten zu je 15 Fragen mit Zwischenergebnis und Fehler-Wiederholung. Wird die Review-Übung übersprungen, werden alle Wörter über dem Level trainiert.

### Lernfortschritt (Familiarity-System)
Jedes Wort trägt einen numerischen `familiarity`-Wert (−1 = noch nie gesehen bis 3 = sehr gut bekannt), der den Lernstand abbildet, plus Zähler für aktiv gelernte und vergessene Wörter. Die verbindlichen Regeln (Werte, Übergänge, 24h-Regel) stehen in `dokumentation.md` → „Lernfortschritt (Familiarity-System)".

### Vokabeltraining
- Einheitlicher Vokabelpool aus den Bibel-Annotationen (A1–C2, inkl. Eigennamen)
- Multiple-Choice: englisches Wort → deutsche Übersetzung wählen
- 18 Schwierigkeitsstufen (A1.1 bis C2.3), zwei Lernfokus-Modi: CEFR-Level oder Häufigkeit in der Bibel
- Adaptives System: Levelanpassung nach jeder 15er-Einheit anhand des First-Pass-Scores
- Fehler-Wiederholung am Einheitsende; Selbsteinschätzung („zu einfach", „ich rate")
- Exakte Mechanik (Wortauswahl, Levelanpassungs-Schwellen, Familiarity-Regeln, Abschluss-Flows): `dokumentation.md` → „Vokabeltraining"

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

- Lückentext-Übungen für mehr Bücher ausbauen
- Lesefortschritt-Statistiken erweitern
- Teilen von Versen / Lesezeichen
- iOS App Store (Capacitor-Bündelung)

## 2. Version (Multilingual)
### Weitere Sprachen (Bibeltexte)
- Spanisch: Reina-Valera 1909 (Original + modernisierte Version)
- Modernisierung: archaische Wörter durch verständlichere ersetzt, per Skript reproduzierbar
