# Bible Reader PWA — Dokumentation

## Überblick

**Bible Reader** ist eine Progressive Web App (PWA), die beim Bibellesen zugleich die Sprache lernen lässt: wortgenaue Annotationen, Vokabeltraining und Text-to-Speech. Als Hauptbibel — also als Lese- und Lernsprache — stehen drei Editionen mit vollem Ausbau zur Verfügung: **Englisch** (WEB, Glossen in de/es/fr/it), **Spanisch** (RV1909, Glossen in en) und **Deutsch** (Luther 1912 modernisiert, Glossen in en/es/fr/it). Französisch und Italienisch sind bisher nur zum Lesen und als Hilfsbibel da.

- **Aktuelle Version:** 1.11.13b (22.09.2026)
- **Architektur:** Single-File React-App (`index.html`, ~5.400 Zeilen), kein Build-Step
- **Bibeltexte:** WEB (en), Reina-Valera 1909 (es), Luther 1912 (de), Segond 1910 (fr), Riveduta 1927 (it) — alle gemeinfrei, die nicht-englischen KI-modernisiert
- **Deutsche Übersetzungen:** Luther 1912 (modernisiert), Wörtliche WEB→DE-Übersetzung
- **Zielgruppe:** Sprachlernende ab A2 in der jeweils gewählten Lesesprache
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
- Wahl zwischen 2 deutschen Übersetzungen: Luther 1912 (modernisiert), Wörtlich (WEB→DE)
- Eigennamen mit deutschen Entsprechungen annotiert (Christ→Christus, Moses→Mose, Egypt→Ägypten)
- Automatische Lesezeichen (merkt sich Position pro Buch)
- Volltextsuche mit wählbarem **Suchbereich** unter dem Suchfeld: Kapitel · Buch · AT · NT · AT+NT (Voreinstellung); die Wahl bleibt gespeichert (`bible-search-scope`). Ein enger Bereich lädt nur die betroffenen Bücher nach
- **Kopfleiste im Kapitel:** links Start und Vorlesen, in der Mitte Kapitel zurück/vor mit dem antippbaren Kapiteltitel, rechts die Suche. Ein Tipp auf den Titel klappt das Inhaltsverzeichnis des Buches auf; solange es offen ist, sind die Reiter „Training"/„Einstellungen" darunter ausgeblendet

### Multi-Wort-Ausdrücke

Idiome, Phrasal Verbs und feste Wendungen werden als Mehrwortausdrücke annotiert:

- **Erster Klick** auf ein Wort des Ausdrucks: zeigt die Phrase-Übersetzung (z.B. „give birth to" → „gebären")
- **Zweiter Klick**: zeigt die wörtliche Einzelwort-Übersetzung (z.B. „give" → „geben", „birth" → „Geburt")
- **Satzklammer:** Bei nicht zusammenhängenden Ausdrücken (`parts`, im Deutschen die Regel: „rief … her", „ließ … bringen") sind die Teile gepunktet unterstrichen und die Wörter dazwischen mit einer **gestrichelten** Linie verbunden (`S.phraseBridge`), damit das Auge die Klammer verfolgen kann

### Text-to-Speech (TTS)

- Kapitelweise Vorlesefunktion mit Wort-für-Wort-Hervorhebung
- Weiterlesen bei gesperrtem Bildschirm (iOS): beim Start läuft zusätzlich eine stumme 1-s-WAV-Schleife (`keepAliveStart`, zur Laufzeit erzeugt), die die Audio-Session der Seite offen hält — sonst friert iOS das JS ein und nach der laufenden Äußerung kommt kein nächster Vers mehr. Endet mit Stopp bzw. am Bibelende. Media Session liefert Sperrbildschirm-/Kopfhörer-Steuerung (Play/Pause/Stopp, Vers vor/zurück) und zeigt Buch + Kapitel
- Einstellbare Geschwindigkeit (0.2×–1.0×); die Voreinstellungen stehen als `SPEED_PRESETS` in `index.html` (🐌 0.2 · Langsam 0.3 · Normal 0.6 · Schnell 0.85 · Sehr schnell 1.0) und werden an allen drei Stellen daraus gespeist
- Einzelvers-Vorleseoption
- Übungsmodus für unbekannte Wörter
- **Audioleiste unten:** Während des Vorlesens klebt am unteren Bildschirmrand eine eigene Leiste (`#audio-bar`, `position:sticky`) mit Vers zurück/vor (samt Versnummer), Pause sowie der Tempo-Einstellung — **Stopp steht nur oben** in der Kapitelleiste, damit es nicht doppelt erscheint — dort liegen die Knöpfe in Daumennähe, ohne dass die Hand über dem Text steht. Die Kopfleiste bleibt dadurch im Audiobetrieb genauso flach wie sonst.
- **Pause:** hält die laufende Äußerung an und setzt genau dort fort (`speechSynthesis.pause()`/`resume()`); die Warteschlange bleibt stehen, die Leiste sichtbar. Jede neue Ausgabe (Kapitelstart, Verssprung, Tempowechsel) hebt eine Pause selbsttätig auf.
- **Mitlaufender Text:** Der Vers wird unterhalb der Kopfleiste eingeblendet, die Wortmarke wird zusätzlich nachgeführt, sobald sie den unteren Rand erreicht — Unterkante ist die Audioleiste bzw., wenn keine läuft, die Safe-Area (Home-Indikator). Code: `readingViewBottom()`, `scrollVerseIntoView()` und der Nachführ-Effekt in `App`.
- **Kapitelwechsel im Audiobetrieb:** Die Pfeile in der Kopfleiste brechen das Vorlesen nicht ab — kurze Pause, dann liest das neue Kapitel weiter (`autoPlayRef`). Genauso geht es am **Kapitelende** von selbst weiter (`tts.onChapterEnd`, in `App` gesetzt); erst am Ende der Bibel hört es auf.

### Schwierige Wörter (kapitelweise)

- **Wörter anschauen:** Alle Wörter über dem Lese-Level werden einzeln angezeigt. Der Nutzer markiert jedes als bekannt (✓) oder unbekannt (?). Nur Wörter mit familiarity ≤ 0 werden angezeigt. ✓ setzt familiarity=1, ? setzt familiarity=0. Das Lese-Level ist ein 18-Stufen-Wert (`userStep` 0–17); ein Wort gilt als „über Level", wenn seine Sublevel-Stufe (aus `words.json` level+sub; für Wörter ohne Pool-Eintrag Fallback auf das obere Band-Ende) größer als `userStep` ist. Dadurch verschwinden die schwierigen Wörter nicht mehr schlagartig beim Eintritt in ein grobes CEFR-Band, sondern feinstufig. Markiert man dabei durchgehend „bekannt" (≥ 85 % von mindestens 20 Wörtern), schlägt die App **einmal je Durchgang** vor, das Lese-Level anzuheben; nach Ja oder Nein kommt die Frage im selben Durchgang nicht wieder (`levelSuggestDone`, zurückgesetzt beim erneuten Aufklappen).
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

Jede Hauptbibel bringt ihren eigenen Wortpool mit (`train/words.json`): **Englisch 5.615**, **Spanisch 6.846**, **Deutsch 9.973** Wörter über A1–C2. Der deutsche Pool ist der grösste, weil das Deutsche Komposita produktiv bildet — ein Grossteil des Überhangs in B2/C1 sind Einmal-Bildungen, die durch die Sublevel-Sortierung nach Häufigkeit hinten stehen.

Eigennamen sind aus den Übungen ausgenommen, bis auf die **wichtigsten mit Lernwert** (`train/keepnames.json`): Bibelbuch-Autoren/Propheten, Erzväter, Könige, Apostel, Kernorte — obskure Namen aus Genealogien nicht (englischer Pool v1.9.53b: +710 Eigennamen ergänzt, später auf ~90 relevante reduziert):

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
- Adaptive Schwierigkeit (5-stufig): 100% = Doppelsprung (+2 Sublevels) · > 80% = +1 · 70–80% = Level halten (±0) · 40–69% = −1 · < 40% = −2. Zählt nur Wörter der Slots B/E des aktuellen Levels (A/C/D herausgerechnet); eine Anpassung erfolgt erst ab **5 gewerteten Wörtern** — kurz vor Stufen-Erschöpfung bestehen Einheiten fast nur aus Wiederholungen, und auf 1–3 Wörtern wäre die Quote reines Rauschen (Level wird dann gehalten, bis der Erschöpfungs-Aufstieg greift). **Die Anpassung wird nie ungefragt übernommen:** der Ergebnis-Screen zeigt „Level auf X anheben/senken? Ja · Nein"; Fertig/Weiter erscheinen erst nach der Antwort. Ja → Level gespeichert („Dein Level ist jetzt X"), Nein → „Level bleibt X". Einstellungen → Übungen → „Level nach Ergebnis automatisch anpassen" (`bible-auto-level`, Standard aus) übernimmt die Anpassung ohne Rückfrage
- Level-Aufstieg bei Erschöpfung: hat der aktuelle Step keine neuen und keine fälligen unbekannten Wörter mehr → automatischer Step+1 mit 🎉-Gratulations-Screen; fällige Wiederholungen blockieren den Aufstieg nicht
- Review als „Level 18": Auf der obersten Stufe (C2.3) gibt es keinen höheren Step. Wird dort eine Einheit **aufstiegswürdig** absolviert (>80% = normalerweise +1/+2), springt der Ergebnis-Screen direkt in die Review über („🎉 Oberste Stufe gemeistert!", Weiter-Button startet die erste Review-Einheit ab B2.2) — man muss also nicht erst ganz C2.3 durchüben. Bei Halten (70–80%) oder Abstieg (<70%) bleibt/sinkt das Level normal
- Nutzer-Feedback: „zu einfach" → familiarity=3, „nur geraten" → Wiederholung am Ende
- Intervall-Guard zentral in `trainWord`: Erhöhen nur nach Ablauf des Stufen-Intervalls (24h / 2 Tage / 7 Tage), Erniedrigen immer erlaubt — gilt für alle Übungspfade inkl. Kapitel-Training
- Anzeige: „X Wörter zum Üben" + „Y Wiederholungen fällig" unter dem Trainings-Button (passend zur gewählten Übungsart); dieselbe Zahl (gemeinsame Funktion `computeCounts`) erscheint auch auf dem Ergebnis-Screen nach jeder Einheit („Noch X Wörter auf dieser Stufe zu üben", bezogen auf die — nach evtl. Levelanpassung — aktuelle Stufe; bei 0 → „Alle Wörter dieser Stufe geübt!"). Darunter steht, wie viele **Einheiten** das noch sind (`unitsLeftText`, Restwörter ÷ `UNIT_WORDS`=15, gerundet, „etwa"). Fortschritts-Panel schlüsselt Bekannt nach Stufen auf (gelernt/gefestigt/sicher)
- **Stufenanzeige in jeder Übung:** unter den Antwortknöpfen steht durchgehend, auf welcher Stufe man gerade übt (`stepFooter` — in der Review die Review-Stufe, im Fokus „Häufigkeit" die Stufennummer, sonst das CEFR-Sublevel)
- Abschluss (oberste Stufe C2.3 erreicht): **Review-Phase** über die restlichen ungeübten Wörter, geordnet nach **CEFR-Nützlichkeit** (nicht nach Häufigkeit) — Reihenfolge als Zickzack-Spirale um B2.2 (die nützlichsten Wörter zuerst): `B2.2, B2.3, B2.1, C1.1, B1.3, C1.2, B1.2, C1.3, B1.1, C2.1, A2.3, C2.2, A2.2, C2.3, A2.1, A1.3, A1.2, A1.1` (`REVIEW_ORDER`/`reviewNextStep`). Jedes CEFR-Sublevel wird in 15er-Einheiten vollständig durchgearbeitet, bevor zum nächsten gewechselt wird; gilt für beide Fokus-Modi, Anzeige als CEFR-Label. Fällige Wiederholungen (Slot A) laufen auch in der Review mit (wie im normalen Training), damit während der langen Review-Phase Gelerntes nicht verblasst. Sobald alle Wörter familiarity ≥ 1 haben → freqAllDone
  - **Nur heute offene Wörter je Sublevel:** ein Sublevel gilt als „für heute erledigt", wenn nur noch fam=0-Wörter übrig sind, die heute schon geübt wurden — der Intervall-Guard lässt sie am selben Tag ohnehin nicht auf fam≥1 steigen (sonst drehte sich dasselbe Wort endlos, `reviewCount`/`currentUnexercised` filtern fam=-1 ODER fam=0-mit-Frist-abgelaufen). Sind alle heutigen Wörter durch, aber noch nicht alles fam≥1 → Meldung „Für heute geschafft" (`freqDoneToday`), morgen geht es weiter
  - **Review-Phase ist persistent** (`bible-review-step` in localStorage, gesetzt/gelöscht via `setReviewStep`): sie überlebt „Beenden" und App-Neustart. Solange die Review läuft, setzt der Trainings-Button die Review fort (statt eine normale C2.3-Einheit zu starten, die per Levelanpassung wieder unter das Top-Level absenken könnte). Der Marker wird erst gelöscht, wenn alles fam≥1 ist (freqAllDone)
  - **Rückfrage nur beim Stufenwechsel:** Nach einer Review-Einheit erscheint der normale Ergebnis-Screen (Stufe, Restwörter, Resteinheiten, Weiter/Beenden) — der Weiter-Knopf startet direkt die nächste Einheit derselben Stufe (`reviewNext`). Die Frage „Es gibt noch N ungeübte Wörter auf Level X. Möchtest du weitermachen?" (`freqComplete`) kommt erst, wenn die Stufe erschöpft ist und die Review auf ein **anderes** Sublevel wechselt — nicht mehr hinter jeder Einheit
  - **Review folgt der gewählten Übungsart** (`startReview`): im Quiz-Modus normale Vokabel-Einheit, im Kontext-Modus dieselbe Review-Wortauswahl als Lückentext dargestellt (Wörter ohne Kontextübung bleiben Quiz — gemischte Einheit). Die Auswahl bleibt identisch zur Quiz-Auswahl, damit `reviewCount` und tatsächliche Einheit übereinstimmen (sonst Endlosschleife). So bleibt „Im Kontext" auch über Einheiten-Grenzen hinweg erhalten

### Einstufungstest

- 30 Multiple-Choice-Fragen (6×5, A1–C2) zur Bestimmung des CEFR-Niveaus
- Ergebnis: A1 bis C2; setzt auch die Trainingsstufen (`bible-train-step`, `bible-freq-step`)
- Passt die Vokabelanzeige automatisch an
- Jederzeit wiederholbar in den Einstellungen; überspringbar über „Einstufungstest überspringen" (setzt B1)
- **Festlegung:** Der Test gehört zur **Sprache** (`LEVEL_TEST_DATA` ist nach Studiensprache geschlüsselt), die Trainingsdaten dagegen zur **Übersetzung** (`wordsPath` je `BIBLES`-Eintrag). Solange es je Sprache nur eine Übersetzung gibt, fällt der Unterschied nicht auf.
- Wer die Hauptbibel wechselt und den Test für die neue Sprache noch nicht gemacht hat, bekommt ihn direkt beim Wechsel (`levelTestPending()` in `index.html`). Der Merker liegt unter dem Instanz-Präfix — bei einer zweiten Übersetzung derselben Sprache käme der Test dort erneut; das wäre die Stelle zum Nachziehen

### Statistiken

- Bücher, Kapitel, Verse, Wörter pro Buch
- Schwierigkeitsbewertung pro Buch (gewichteter CEFR-Durchschnitt)
- CEFR-Verteilung der Vokabeln mit Sublevel-Aufschlüsselung (Oxford 5000 und Bibel-Vokabular getrennt)
- Min–max Vorkommen pro Level in der Bibel (z.B. „1–56.635×")
- Lernfortschritt: bekannte/unbekannte/nicht gesehene Wörter, gelernte und vergessene Wörter
- **Zugang:** Die Statistik-Seite wird nur noch über das Training geöffnet (📊 „Fortschritt" im Trainings-Kopf → „Statistik"). In der Startseite und in der Leseansicht erscheint kein Statistik-Icon mehr.
- **Wortstatistik pro Buch:** In der Statistik-Seite unter „Wörter pro Buch" aufklappbar. Zeigt: Wörter gesamt, bekannte Wörter (davon neu gelernt), unbekannte Wörter (davon vergessen), noch nicht geübte. Annotationen werden lazy geladen.

---

## Technische Architektur

### Dateistruktur

```
bible-reader/
├── index.html                         Haupt-App (React + Babel, ~5.400 Zeilen)
├── sw.js                              Service Worker (Offline-Caching)
├── manifest.json                      PWA-Manifest
├── icon-192.png / icon-512.png        App-Icons
├── lib/                               React, ReactDOM, Babel (lokal gebündelt)
├── sync_www.sh                        Spiegelt root → www/ → ios/ (Capacitor), vor jedem iOS-Build
├── bugserver.py                       Empfänger für die im Handy gemeldeten Bugs; serviert
│                                      zugleich die App aus dem Repo-Root (--list / --done / --import)
├── bugtunnel.sh                       bugserver.py + cloudflared-HTTPS-Tunnel für Tests unterwegs
├── bugs/bugs.json                     Eingegangene Bug-Meldungen (gitignored)
├── www/ · ios/                        Capacitor-Ableitungen (gitignored, nie manuell bearbeiten)
├── bibles/                            Alles zu einer Bibel-Edition liegt beisammen: Text,
│   │                                  Annotationen und Trainingsdaten. Die Pfade stehen in der
│   │                                  BIBLES-Registry in index.html (annoDir/wordsPath/examplesPath).
│   ├── index.json                     Buch-Metadaten und Statistiken
│   ├── eng/web/                       English (WEB) — Lesen, Glossen, Training, Einstufungstest
│   │   ├── {nr}_web.json              Bibeltext (66 Dateien)
│   │   ├── anno/{nr}_web_deu.json     Annotationen, Glossen in de/es/fr/it (66 Dateien)
│   │   ├── web_deu/{nr}_web_deu.json  Wörtliche DE-Übersetzung (66 Dateien)
│   │   └── train/
│   │       ├── words.json             Single Source of Truth: Vokabel-Pool + Lückentext-Übungen
│   │       │                          (5.615 Wörter über A1–C2; VOCAB_POOL + CLOZE_EXERCISES
│   │       │                          werden daraus abgeleitet)
│   │       ├── examples.json          Beispielsätze-Index (Lemma → Vers-Referenzen, 207 KB, lazy)
│   │       ├── lemma_freq.json        Lemma → Vorkommen in der ganzen Bibel (148 KB, lazy;
│   │       │                          Wortkarte „in der Bibel N × · in diesem Buch N ×")
│   │       └── vocab_pool.json · context_exercises.json   Build-Intermediates (gitignored)
│   ├── spa/rv1909mod/                 Español — wie eng/web mit anno/ (Glossen en) und train/
│   ├── spa/rv1909 · fra/lsg1910mod · ita/riv1927mod   Nur Lesen (keine Annotationen/Training)
│   └── deu/l1912mod/                  Luther 1912 modernisiert — Lesen, Glossen (en/es/fr/it),
│       │                              Training, Einstufungstest; auch Hilfsbibel für Deutsch
│       ├── anno/{nr}_l1912mod_multi.json   Annotationen mit vier Glossen (66 Dateien)
│       └── train/                     words.json (mehrsprachig, siehe unten, 9973 Wörter),
│                                      examples.json, propnames.json (3223 Eigennamen),
│                                      keepnames.json; lemmas_raw.json ist ein
│                                      Build-Intermediate (gitignored)
├── generate_lemma_freq.py             Zählt je Edition alle Annotationen pro Lemma → train/lemma_freq.json
│                                      (eng/web, spa/rv1909mod, deu/l1912mod, fra/lsg1910mod = nur NT)
├── generate_training_data.js          Generiert words.json aus Annotationen
│                                      (Oxford 5000 + Kaggle + Opus CEFR-Abgleich, Filterung)
├── build_training.py                  Trainingsdaten Schritt 1: Lemmata, Häufigkeit, bester
│                                      Lückentext und Mehrheitsglossen je Sprache → lemmas_raw.json
├── prepare_enrich.py                  Schritt 2a: Anreicherungs-Pakete schnüren (wellenfähig,
│                                      überspringt bereits Angereichertes)
├── enrich_prompt.md                   Schritt 2b: Arbeitsanweisung der Anreicherungs-Agenten
├── check_enrich.py                    Prüft die Agenten-Ausgaben gegen ihre Eingaben
├── finalize_training.py               Schritt 3: → words.json + propnames.json
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

**Eigennamen im Übungsfilter:** Die Kapitelübungen lassen Eigennamen aus, außer den kuratierten aus `train/keepnames.json`. Erkannt werden sie normalerweise an der Großschreibung des Lemmas — im Deutschen ist das wertlos, weil jedes Substantiv groß geschrieben wird. Editionen können deshalb über `propNamesPath` eine echte Liste mitbringen (aus der Anreicherung, `pos == propn`); liegt eine vor, entscheidet sie statt der Schreibung.

**Eigennamen:** Im **Bibeltext** sind alle Eigennamen (Personen, Orte) annotiert — immer Level A1. Deutsche Entsprechungen werden verwendet: Christ→Christus, Moses→Mose, Egypt→Ägypten, Isaiah→Jesaja. Namen ohne Änderung (Jesus, Abraham) erhalten die gleiche Form als `de`. Im **Lernwortpool** (`words.json`) steht dagegen nur eine kuratierte Auswahl der wichtigsten Namen mit Lernwert (en ≠ de) — obskure Namen aus Genealogien sind nicht enthalten.

### Trainingsdatenformat (`words.json`)

Nach CEFR-Stufe gebucketet, je Wort ein Eintrag; `VOCAB_POOL`, `FREQ_POOL` und
`CLOZE_EXERCISES` werden daraus abgeleitet.

| Feld | Beschreibung |
|------|-------------|
| `en` | Lemma in der Studiensprache (historischer Feldname) |
| `de` | Übersetzung in der aktiven Glossensprache (historischer Feldname) |
| `tr` | **Mehrsprachig:** Grundform-Übersetzung je Glossensprache, z.B. `{"en":"to create","es":"crear",…}` |
| `deForm` / `trForm` | dasselbe für die **flektierte Form** im Lückentext |
| `sub` | Sublevel 1–3 innerhalb der CEFR-Stufe (nach Häufigkeit gedrittelt) |
| `occ` | Vorkommen im Bibeltext |
| `pos` | Wortart (nur noun/verb/adj/adv kommen in den Pool) |
| `form` | Formkategorie sg/pl/inf/pres/past/part/base — bündelt die Lückentext-Ablenker |
| `text` · `answer` · `ref` · `book` | Lückentext-Satz, Zielwort, Stellenangabe |

`tr`/`trForm` stehen nur bei Editionen mit mehreren Glossensprachen (deutsche
Bibel). `applyGlossToWords()` füllt daraus `de`/`deForm` — beim Laden und erneut,
wenn die Glossensprache im laufenden Betrieb gewechselt wird; alle Übungen lesen
weiterhin nur `de`/`deForm`. Fehlt `tr`, bleibt es beim einsprachigen Bestand.

Aus Platzgründen stehen `de`/`deForm` bei mehrsprachigen Editionen **nicht** in der
Datei (die App leitet sie ab), und `trForm` entfällt, wenn es mit `tr`
übereinstimmt — bei vier Sprachen spart das rund ein Sechstel der Dateigröße.

### PWA und Offline-Fähigkeit

- **Service Worker** (`sw.js`): Network-first für HTML, Cache-first für Daten
- **Cache-Name:** `bible-full-vXXXX` (aktuell `bible-full-v2108`, wird bei jedem Deploy hochgezählt)
- Vollständige Offline-Nutzung nach erstem Laden
- Automatisches Update bei neuer Version

### Lokale Datenspeicherung (LocalStorage)

| Schlüssel | Inhalt |
|-----------|--------|
| `bible-reader-state` | Phase, Lese-Level (`userStep` 0–17, sublevel-genau), Position, Wortlisten |
| `bible-ui-lang` | UI-Sprache (de/en) |
| `bible-view-mode` | Ansichtsmodus (phone/desktop) |
| `bible-layout` | Theme/Layout (classic/icf/icf-light) |
| `bible-de-trans` | Gewählte Hilfsbibel (BIBLES-Registry-ID). Wird auf der Startseite unter „Hilfsbibel" gewählt — in den Einstellungen steht dort nur noch der Schalter, ob ihre Verse immer eingeblendet werden |
| `bible-word-data` | Wortdaten pro Wort ({familiarity, lasttrained, numberoftrainings, learned, forgotten}) |
| `bible-word-data-backups` | Liste zeitgestempelter Lernstand-Backups (Entwickler-Werkzeug „Test-Daten laden"; max. 12, ältestes wird bei Speicherüberlauf verworfen). Jedes Backup ist ein vollständiger Snapshot: Wortdaten, Lese-Level (`userStep`) samt Wortlisten, Trainingsstufen, Lernfokus, Übungsart, Trainingshistorie und Kapitel-Markierungen (`unk-*`/`rev-*`). Migriert den früheren Einzel-Slot `bible-word-data-backup` (nur Wortdaten). |
| `bible-test-accel` | Beschleunigter Test-Modus (Entwickler-Einstellungen): alle Lern-Fristen ÷96 (unbekannt 15 min · gelernt 30 min · gefestigt 105 min · sicher 15 h) und nur ¼ des Wortpools (pro Level/Sublevel jedes 4. Wort — Level-Verhältnisse bleiben erhalten). Wirkt beim App-Laden; ⚡-Hinweis im Training. |
| `bible-train-focus` | Lernfokus im Training ('level'/'freq') |
| `bible-ex-mode` | Übungsart im Training ('quiz'/'cloze') |
| `bible-train-step` | Aktuelle Trainingsstufe CEFR-Modus (0–17) |
| `bible-freq-step` | Aktuelle Trainingsstufe Häufigkeits-Modus (0–17) |
| `bible-training-history` | Trainingshistorie (letzte 200) |
| `bible-level-tested` | Einstufungstest absolviert — pro Hauptbibel (Instanz-Präfix). Nach einem Hauptbibelwechsel erscheint der Test der neuen Bibel deshalb sofort, auch wenn das Onboarding global schon abgeschlossen ist |
| `bible-bookmarks` | Lesezeichen pro Buch |
| `bible-font-size` / `-tr` / `-pill` / `-ex` | Schriftgrößen (Bibeltext / Hilfsbibel / Wortübersetzung / Übungen). Das Minus/Plus in den Einstellungen verstellt alle vier gemeinsam um 1 px (gesperrt, sobald ein Wert seine Grenze erreicht); einzeln — ebenfalls in 1-px-Schritten — unter „Details". **Ohne Instanz-Präfix gespeichert** — die Schriftgrößen gelten für alle Hauptbibeln gemeinsam (`FONT_LS` in `index.html`; alte, pro Instanz abgelegte Werte werden als Fallback gelesen). |
| `bible-line-height` / `-tr` | Zeilenabstände (Bibeltext / Hilfsbibel) — bewusst NICHT Teil der Sammelskalierung, da sie als Verhältniswerte mit der Schrift ohnehin mitwachsen; ebenfalls ohne Instanz-Präfix (gilt für alle Hauptbibeln) |
| `bible-cloze-ctx` | Lückentext-Kontext (Satz / ganzer Vers) |
| `bible-show-lemma` / `bible-show-cefr` | Anzeige-Optionen beim Lesen |
| `bible-show-ex-level` | Zeigt in den Übungen neben dem Wort CEFR-Sublevel · Häufigkeitsstufe (1–18) · absolute Häufigkeit („N × in der Bibel", aus lemma_freq.json, sonst occ) |
| `bible-auto-level` | Levelanpassung nach einer Einheit ohne Rückfrage übernehmen (Standard aus = fragen) |
| `bible-stats-visible` | Sichtbare Statistik-Abschnitte |
| `bible-search-scope` | Suchbereich der Volltextsuche ('chapter'/'book'/'ot'/'nt'/'all') |
| `unk-{lang}-{buch}-{kapitel}` | Unbekannte Wörter pro Kapitel |
| `tts-speed` | TTS-Geschwindigkeit |
| `bible-bugs` / `bible-bugmode` / `bible-bug-endpoint` | Bug-Melder: gemeldete Bugs, Ein/Aus-Schalter, Empfänger-Adresse. Ohne LS-Präfix, damit die Liste bibelübergreifend ist; der komplette Reset lässt diese drei Schlüssel als einzige stehen. Siehe `CLAUDE.md` → „Bug-Melder". |

### Bug-Melder (Testwerkzeug)

Zum Testen auf dem Gerät lässt sich auf jeder Ansicht ein 🐞-Knopf einblenden. Ein Tipp öffnet ein
Formular für Schwere und Beschreibung; automatisch mitgeschrieben werden Ansicht, Buch/Kapitel,
Bibel-Edition, Gloss-Sprache, Lese-Level, App-Version, Viewport, PWA-Modus und die letzten acht
JavaScript-Fehler (Ringpuffer `window.__bugLog`, gesetzt vor dem Babel-Block, damit auch Ladefehler
erfasst werden). Die Meldungen bleiben im Gerät (`localStorage['bible-bugs']`), bis sie übertragen
sind — für normale Nutzer ist der Knopf unsichtbar.

- **Einschalten:** App-URL einmal mit `?bugs=1` öffnen, oder fünfmal auf die Versionszeile in den
  Einstellungen tippen (nötig in der vom Homescreen gestarteten PWA, die einen eigenen
  localStorage hat). `?bugs=0` oder erneut fünf Tipps schalten wieder aus.
- **Übertragen:** „Speichern & senden" schickt die offenen Bugs per POST an `{Empfänger}/bugs`.
  Kommt die App vom Empfänger selbst (`bugserver.py` im WLAN oder über den `bugtunnel.sh`-Tunnel),
  genügt die eigene Herkunft und es braucht keine Adresse; bei Auslieferung über GitHub Pages
  blockiert der Browser den http-Empfänger (Mixed Content), dann Tunnel-Adresse eintragen oder
  „Exportieren / Teilen" nutzen (Teilen-Sheet, sonst Zwischenablage/Datei).
- **Auf dem Mac:** `python3 bugserver.py` nimmt entgegen und schreibt nach `bugs/bugs.json`;
  `--list` zeigt die offenen, `--done <id>` hakt ab, `--import <datei>` liest eine geteilte Liste ein.
- **Nachträglich bearbeiten:** In der Liste „Gemeldete Bugs" lassen sich Text und Schwere eines
  Eintrags ändern (Knopf „Bearbeiten"). Der erfasste Kontext bleibt unangetastet, der Eintrag gilt
  wieder als offen und geht beim nächsten Senden erneut mit. `merge()` in `bugserver.py` erkennt die
  bekannte id und übernimmt die neue Fassung, statt sie zu verwerfen; ein bereits erledigter Eintrag
  wird dabei nicht wieder geöffnet.

Der Melder überlebt den kompletten Reset in den Entwickler-Einstellungen. Details zum Code und zum
Arbeitsablauf stehen in `CLAUDE.md` → „Bug-Melder".

### Deutsche Übersetzungen

Zwei deutsche Parallelübersetzungen stehen zur Auswahl (einstellbar unter Einstellungen):

| Übersetzung | Pfad | Format |
|-------------|------|--------|
| **Luther 1912 (modernisiert)** (Standard) | `bibles/deu/l1912mod/` | Dict (`{"chapters":{"1":{"1":"Text",...},...}}`) |
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
- **Einheitlicher Vokabelpool:** 5.615 Wörter (A1: 1.063, A2: 544, B1: 792, B2: 1.499, C1: 1.185, C2: 532) — Eigennamen auf die wichtigsten mit Lernwert kuratiert (obskure entfernt, fehlende wichtige wie Moses/Jeremiah/Elia ergänzt)
- **CEFR-Quellen:** Oxford 5000 (2.654), Kaggle CEFR (945), Opus 4.7 (1.488); Rest: Eigennamen und Pool-Erweiterungen (v1.9.53b–58b)
- **2 deutsche Übersetzungen:** Luther 1912 mod, Wörtlich WEB→DE
