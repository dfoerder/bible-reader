## Laufend
- detailverbesserungen, debugging

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