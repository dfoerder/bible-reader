## Laufend
- detailverbesserungen, debugging

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