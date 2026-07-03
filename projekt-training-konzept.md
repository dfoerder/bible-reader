# Trainingskonzept 2.0 — Spaced Repetition

**Status: ENTWURF (03.07.2026), noch nicht implementiert.**
Zielkonzept für das allgemeine Vokabeltraining. Nach Umsetzung wird `dokumentation.md`
(§ Vokabeltraining, § Lernfortschritt) aktualisiert und dieses Dokument als umgesetzt markiert.

## Motivation

Analyse vom 03.07.2026: Das heutige Training deckt die Vision gut ab, hat aber eine
zentrale Lücke — **Wörter mit fam ≥ 1 werden nie wieder geübt**. Dadurch:
- werden frisch gelernte Wörter (die wichtigste Kategorie) nicht gefestigt,
- kann „Vergessen" im Training gar nicht erkannt werden (nur zufällig in Kapitel-Übungen),
- sind fam=2 und fam=3 im allgemeinen Training unerreichbar — die Skala ist eine Treppe,
  die niemand hochsteigt.

Kern der Verbesserung: **Leitner-artige Spaced Repetition** auf der vorhandenen
Familiarity-Skala, ohne neue Datenfelder (familiarity, lasttrained, learned, forgotten reichen).

## Beschlossene Parameter (03.07.2026)

| Parameter | Entscheidung |
|---|---|
| Wiederholungs-Intervalle | fam=1 fällig nach **2 Tagen**, fam=2 nach **7 Tagen** |
| fam=3 | Seltene Stichprobe nach **~60 Tagen** (max. 1 pro Einheit) |
| Level-Aufstieg bei erschöpftem Level | **Automatisch** mit Gratulations-Hinweis |
| Beimischung Step+1 | **1 Wort** pro Einheit |

## Familiarity-Treppe (Soll)

| fam | Bedeutung | Fällig zur Wiederholung |
|---|---|---|
| −1 | ungeübt | — (neu) |
| 0 | unbekannt / vergessen | > 24 h |
| 1 | gelernt | > 2 Tage |
| 2 | gefestigt | > 7 Tage |
| 3 | sicher | > 60 Tage (Stichprobe) |

**Übergänge im Training:**
- Richtige Antwort (erster Durchgang, Wort fällig): fam+1 (max. 3); fam −1/0 → 1 wie bisher
- Falsche Antwort: fam=0 (immer erlaubt); von fam ≥ 1 kommend zählt `forgotten` +1 (wie bisher)
- Retry: richtig → keine Änderung, falsch → fam=0 (wie bisher)
- „zu einfach" → fam=3, „ich rate" → Wiederholung am Ende ohne fam-Erhöhung (wie bisher)
- `learned` +1 bei fam 0 → >0 (wie bisher)

Die Intervalle steuert die **Wortauswahl** (nur fällige Wörter werden gezogen); die zentrale
24h-Erhöhungsregel in `trainWord` bleibt als Sicherheitsnetz für alle anderen Pfade bestehen.

## Einheiten-Mix (15 Wörter pro Einheit)

Slots in Prioritätsreihenfolge, danach gemischt (shuffle):

| Slot | Inhalt | Quote |
|---|---|---|
| A | Fällige Wiederholungen fam=1/2 (alle Levels), am längsten überfällige zuerst; darunter max. 1 fam=3-Stichprobe | bis 4 |
| B | Fällige fam=0 (aktuelles + tiefere Levels), **vergessene** (`forgotten`>0) zuerst | bis 3 |
| C | 1 ungeübtes Wort (fam=−1) tieferer Levels | 1 |
| D | 1 ungeübtes Wort (fam=−1) aus Step+1 (entfällt auf Step 17) | 1 |
| E | Neue Wörter (fam=−1) des aktuellen Levels | Rest (~6) |

Auffüllregel bei Knappheit: leerer Slot E wird zuerst aus Überhang von A, dann B, dann C/D gefüllt.
Die Quoten begrenzen die Review-Last, damit sich kein „Review-Stau" bildet, der neue Wörter
verdrängt (wichtig auch bei Bestandsnutzern: deren alte fam=1-Wörter sind beim Update alle
sofort fällig — die Quote von 4 pro Einheit taktet das ab).

Gilt für beide Fokus-Modi: Level-Modus über `VOCAB_POOL` (tiefere/höhere CEFR-Levels),
Frequenz-Modus über `FREQ_POOL` (freqStep−/+1). Der Kapitel-Lückentext und das Kapitel-Quiz
bleiben unverändert (nutzen weiterhin `trainWord` und profitieren automatisch von der Treppe).

## Levelanpassung und Aufstieg

- **Score-Basis:** Nur Wörter des aktuellen Levels mit fam ∈ {−1, 0} bei Einheitsstart
  (Slots B/E). Wiederholungen (A) und Beimischungen (C/D) werden — wie heute schon die
  tieferen Wörter — über den `adjTotal`-Mechanismus herausgerechnet.
- **Delta-System unverändert:** 100% → +2 · >80% → +1 · 70–80% → ±0 · 40–69% → −1 · <40% → −2
- **Neu — Aufstieg bei Erschöpfung:** Hat das aktuelle Level keine fam=−1-Wörter und keine
  fälligen fam=0-Wörter mehr → automatischer Step+1 mit Gratulations-Screen
  (ersetzt den heutigen `nowords`-Screen mit „tieferes Level"-Angebot).
  Fällige Wiederholungen laufen level-unabhängig weiter.
- **Step 17 erschöpft:** bestehender freqComplete-/Review-Flow (ungeübte Wörter aller
  Levels, schrittweise), plus weiterhin fällige Wiederholungen. freqAllDone wenn alle fam ≥ 1.

## UI-Konsequenzen

- Zähler unter den Trainings-Buttons: neue Kategorie „X Wiederholungen fällig"
  (zusätzlich zu neuen/unbekannten Wörtern), Zähler muss exakt dem Einheiten-Pool entsprechen
- Fortschritts-Panel (📊): Aufschlüsselung bekannt → gelernt/gefestigt/sicher (fam 1/2/3),
  da diese Stufen jetzt real erreicht werden
- Gratulations-Screen für den automatischen Level-Aufstieg (Custom-Dialog, kein alert)

## Implementierungspakete

- **AP-T1** Fälligkeits-Helper (`reviewDue`) + neuer Einheiten-Mix in `startVocab`
  (Slots A–E, Auffüllregel), analog für den allgemeinen Cloze-Start
  · **ERLEDIGT (03.07.2026)** — im Browser verifiziert (Slot-Quoten, Intervalle 2/7/60 Tage,
  fam=3-Stichprobe, Vergessene zuerst)
- **AP-T2** fam-Treppe in `pick()`: richtige Antwort → fam+1 statt hart fam=1;
  Intervall-Guard zentral in `trainWord` (24h/2d/7d je Stufe)
  · **ERLEDIGT (03.07.2026)**
- **AP-T3** Level-Aufstieg bei Erschöpfung (nowords-Ersatz), Step-17-Verzahnung mit
  freqComplete prüfen
- **AP-T4** `adjTotal`-Ausweitung auf Slots A/C/D (Levelanpassung nur über B/E);
  bei adjTotal=0 (reine Wiederholungs-Einheit) keine Levelanpassung
  · **ERLEDIGT (03.07.2026)** — mit AP-T1 umgesetzt (untrennbar); Bonus-Fix: startBookCloze
  setzt die Ausnahme-Refs jetzt zurück (vorher stale aus Vorsession)
- **AP-T5** Zähler, Fortschritts-Panel, Gratulations-Screen, I18N-Texte
- **AP-T6** Nach Umsetzung: `dokumentation.md` aktualisieren, dieses Dokument als
  umgesetzt markieren, Deploy mit Changelog
