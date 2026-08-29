## Laufend
- detailverbesserungen, debugging
- Schwierige Wörter: nach Ablehnung eines Level-Vorschlags im selben Kapitel nicht erneut fragen (übernommen aus issues.md)

### Datenfehler: der italienische Psalter hat in 63 Psalmen keinen Vers 1
`bibles/ita/riv1927/19_riv1927.json` und `…/riv1927mod/19_riv1927mod.json`
beginnen in 63 Psalmen bei Vers 2. Der Vers ist nicht zusammengezogen, er
**fehlt**. In Psalm 23 fehlt damit `Il Signore è il mio pastore` — italienische
Leser bekommen die bekannteste Zeile des Psalters gar nicht zu sehen.

Der Fehler steht schon im importierten Grundtext `riv1927`, nicht erst in der
modernisierten Fassung, und betrifft **nur** diese beiden Dateien: kein anderes
Buch und keine andere Sprache hat ein Kapitel ohne Vers 1. Gemessen mit einem
Durchlauf über alle Editionen.

Zum Beheben braucht es den RIV1927-Text dieser 63 Verse aus einer anderen
Quelle. Betroffene Psalmen und die genaue Messung stehen in
`../bibles-translations/anno-tools/VERSZAEHLUNG_PSALMEN.md`.

Kleiner verwandter Importartefakt: im italienischen Psalter stehen vereinzelt
`}`-Zeichen mitten im Text (z. B. Ps 81,1 `Salmo di Asaf.} Cantate…`), dort wo
die Überschrift in den ersten Vers gefaltet wurde.

### `di io` statt `di Dio` — 26 Verse im italienischen Grundtext
`bibles/ita/riv1927` schreibt in 26 Versen `di io`, wo `di Dio` stehen muss —
darunter `Figliuol di io` in Matthäus 14,33 und 26,63, Markus 3,11, Johannes
5,25 und 1. Johannes 3,8, sowie `il Regno di io` in Lukas 6,20 und 18,25. Es
ist dieselbe verlorene Majuskel wie bei den übrigen Importartefakten.

**Die App ist nicht betroffen:** sie liefert `ita/riv1927mod` aus, und dort ist
der Fehler in allen 26 Versen behoben (0 Treffer).

Betroffen ist die **Werkzeugkette**: `anno-tools/ausgaben.py` liest als
italienische Referenzausgabe `riv1927`, nicht `riv1927mod`. Damit vergleicht
die Annotation gegen einen anderen italienischen Text als den, den Leser
sehen — und zwar asymmetrisch, denn für das Spanische nimmt dieselbe Liste die
modernisierte Fassung (`rv1909mod`), fürs Italienische die rohe.

Zu entscheiden ist beides zusammen: ob `riv1927` repariert wird und ob die
Werkzeugkette auf `riv1927mod` umgestellt wird. Eine Umstellung mitten im Buch
wäre allerdings ein Bruch — 46 Bücher sind gegen `riv1927` annotiert.

### Modernisierungsfehler: Psalm 37,36 wechselt das Subjekt
`l1912` liest `Da **man** vorüberging, siehe, da war er dahin`; `l1912mod`
schreibt `Doch als **ich** vorüberging, war er verschwunden`. Aus dem
unpersönlichen „man" ist ein „ich" geworden — eine Bedeutungsverschiebung, die
der Grundtext nicht hergibt und die auch keine der vier Referenzausgaben stützt
(WEB `he passed away`, RV `Pero pasó`, LSG `Il a passé`, RIV `ma è passato
via` — dort vergeht jeweils der Gottlose).

Gefunden beim Annotieren von Psalm 37. Die Annotation folgt dem Quelltext, wie
die Regel es verlangt; der Quelltext selbst wäre zu prüfen.

**Es ist kein Muster.** Der Abgleich `l1912` gegen `l1912mod` über alle 66
Bücher zeigt **424 Verse**, die das unpersönliche `man` verlieren — fast
durchweg zu Recht, weil modernes Deutsch dort das Passiv setzt (`daß man mir
viel Holz zubereite` → `damit reichlich Holz für mich vorbereitet wird`). In
50 davon steht in der neuen Fassung ein `ich` oder `wir`, aber in aller Regel
stand es schon im alten Vers. Psalm 37,36 ist der einzige gefundene Fall, in
dem das `man` **derselben Teilaussage** durch ein `ich` ersetzt ist und keine
der vier Referenzausgaben das stützt.

Eine vollständige Prüfung bräuchte einen Abgleich je Teilsatz, nicht je Vers;
das ist hier nicht geleistet.

### Rückstand: fehlende Mehrwort-Wendungen in den fertigen Büchern
`anno-tools/sweep.py alle` meldet rund 500 Verdachtsfälle — Wortfolgen, die der
Bestand fast immer als Wendung führt und die an dieser Stelle keinen
Mehrwort-Eintrag tragen. Eine Stichprobe von 14 ergab rund 43 % echte Lücken.

Die harte Teilmenge (zusammenhängend, Deckung ≥ 93 %, ≥ 8 Belege) ist
abgearbeitet: 28 Stellen geprüft, 16 ergänzt, 12 zu Recht wörtlich. Der Rest
sind überwiegend Treffer mit Abstand zwischen den Wörtern, wo die Fehlalarmquote
höher liegt — sie brauchen einen eigenen Durchgang.

## Lese-Level sublevel-genau (18 Stufen) · UMGESETZT (03.07.2026)
Das Lese-Level ist jetzt ein 18-Stufen-Wert (`userStep` 0–17) statt der 6 groben CEFR-Stufen.
Kapitel-„schwierige Wörter" und Text-Hervorhebung nutzen `annoStep` (Sublevel aus `words.json`,
Fallback oberes Band-Ende). Behebt den Cliff, bei dem alle schwierigen Wörter schlagartig bei
C2.1 verschwanden. Offen/optional: Der Trainingsfortschritt hebt weiterhin das Lese-Level (jetzt
sublevel-genau gekoppelt); falls unerwünscht → entkoppeln oder manuellen Level-Regler wieder
einführen (siehe Diskussion 03.07.2026).

## Trainingskonzept 2.0 — Spaced Repetition · UMGESETZT (03.07.2026)
Alle Pakete AP-T1 bis AP-T6 abgeschlossen, siehe `projekt-training-konzept.md`.
Offen: Praxiserfahrung sammeln (sind 4 Wiederholungen pro Einheit im Alltag richtig
dosiert?) und Quoten/Intervalle ggf. nachjustieren.

### Abgeschlossen (Session 18.06.2026, v1.9.30b–v1.9.42b)
- POS-Distraktoren einheitlich in allen Übungen (Wortart + Numerus/Tempus)
- Flexions-Übersetzungen (`deForm`/`form`) via Opus-Batch für alle 5086 Wörter
- „Weitere Beispiele für \<wort\>" bei falscher Antwort (on-the-fly, 207 KB Refs-Index)
- Separate Schriftgröße für Übungstexte; Bibeltext-Default 16 px
- Fortschritt-Statistik (Geübt/Bekannt/Unbekannt/Ungeübt) als 📊-Panel im Training-Screen
- Lernfortschritt-Logik: gelernt vs. geübt im Ergebnis, fam=0 vor fam=-1 priorisiert
- 24h-Regel in `trainWord` zentralisiert (Familiarity nur nach 24h erhöhbar)
- Bugfixes: leerer Bildschirm nach Reload (NaN-Check), belowLevel-Statistik im Freq-Modus

## Vor der App-Store-Einreichung

### Design & Assets
- besseres Icon für iOS entwickeln (alle Größen: 20–1024 pt)
- Launch Screen / Splash Screen erstellen
- App Store Screenshots erstellen (iPhone 6.7", 6.5", 5.5" — mind. 3 pro Sprache)
- App Store Preview-Video (optional, aber empfohlen)

### Apple Developer Setup
- Apple Developer Account eröffnen (99 $/Jahr)
- App in App Store Connect anlegen (Bundle ID: `de.biblereader.app`)
- Signing & Capabilities in Xcode konfigurieren

### App Store Metadaten
- App-Name, Untertitel, Beschreibung (DE + EN)
- Keywords für App Store Search (DE + EN)
- Support-URL und Datenschutz-URL einrichten
- Datenschutzerklärung erstellen und hosten
- Altersfreigabe festlegen (wahrscheinlich 4+)
- Kategorie: Bildung / Bücher

### Technisch
- **Entwickler-Einstellungen ausblenden** (Abschnitt ENTWICKLER in den Einstellungen: Test-Daten laden, Frischer Start, Backups, beschleunigter Test-Modus, Lerner-Simulation) — ein normaler Nutzer darf seinen Lernstand nicht versehentlich mit Test-Daten überschreiben können; dabei auch prüfen, dass `bible-test-accel` bei Nutzern nicht gesetzt ist
- Tip-Jar via StoreKit / In-App Purchase implementieren (2–3 Stufen, 1.99 / 4.99 / 9.99 $)
- Spendenhinweis-Dialog bei Sprachpaket-Downloads
- Offline-Verhalten und Fehlerbehandlung testen
- App auf echtem Gerät testen (nicht nur Simulator)
- Barrierefreiheit prüfen (Dynamic Type, VoiceOver)

### TestFlight & Review
- Interne Tests via TestFlight
- App-Review-Informationen für Apple vorbereiten (Demo-Account falls nötig)
- Einreichung und Review-Prozess

## Danach
- app publizieren
- Android-Version (Capacitor, Play Store)