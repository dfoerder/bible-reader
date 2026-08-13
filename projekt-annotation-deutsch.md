# Deutsche Annotation (l1912mod → en/es/fr/it)

Wort-für-Wort-Annotation der deutschen Bibel mit Übersetzungen nach Englisch,
Spanisch, Französisch und Italienisch. Begonnen 25.07.2026, **das Neue
Testament (Bücher 40–66) ist seit 28.07.2026 vollständig**.

Das ist die **Gegenrichtung** zu den bestehenden Annotationen: Bisher war
Deutsch immer Gloss-Sprache (WEB-Bibel mit `de`-Feld), hier ist Deutsch der
annotierte Text und die vier anderen Sprachen sind die Glossen.

## Stand

**Das Neue Testament ist vollständig annotiert** — alle 27 Bücher, 7957 Verse,
172 517 Einträge (3985 Phrasen, 3038 Klammern). Abgeschlossen am 28.07.2026.

**Der Pentateuch ist vollständig.** 1. Mose am 29.07.2026 (50 Kapitel,
1533 Verse, 33 781 Einträge), 2. Mose am selben Tag (40 Kapitel, 1213 Verse,
26 318 Einträge), **3. Mose und 4. Mose am 11.08.2026** (27 Kapitel,
859 Verse, 19 644 Einträge bzw. 36 Kapitel, 1288 Verse, 26 189 Einträge),
**5. Mose am 12.08.2026** (34 Kapitel, 959 Verse, 25 278 Einträge).

**Die Geschichtsbücher bis 2. Könige sind vollständig.** Josua, Richter und
Ruth am 12.08.2026, **1. Samuel und 2. Samuel am 13.08.2026** (31 Kapitel,
811 Verse, 22 011 Einträge bzw. 24 Kapitel, 695 Verse, 17 931 Einträge),
**1. Könige am 13.08.2026** (22 Kapitel, 817 Verse, 21 132 Einträge),
**2. Könige am 14.08.2026** (25 Kapitel, 720 Verse, 20 422 Einträge).

Damit sind **39 von 66 Büchern fertig**: 598 Kapitel, 18 213 Verse,
418 971 Einträge. `validate.py alle` gibt für alle 39 Bücher `[ok]` aus,
`qa.py alle` meldet 0 Verdachtsfälle. Es fehlen die Bücher 13–39
(rund 600 Kapitel).

| Buch | Kapitel | Verse | Einträge |
|---|---|---|---|
| **1. Mose (1)** | **50** | **1533** | **33 781** |
| **2. Mose (2)** | **40** | **1213** | **26 318** |
| **3. Mose (3)** | **27** | **859** | **19 644** |
| **4. Mose (4)** | **36** | **1288** | **26 189** |
| **5. Mose (5)** | **34** | **959** | **25 278** |
| **Josua (6)** | **24** | **658** | **15 319** |
| **Richter (7)** | **21** | **618** | **16 117** |
| **Ruth (8)** | **4** | **85** | **2 311** |
| **1. Samuel (9)** | **31** | **811** | **22 011** |
| **2. Samuel (10)** | **24** | **695** | **17 931** |
| **1. Könige (11)** | **22** | **817** | **21 132** |
| **2. Könige (12)** | **25** | **720** | **20 422** |
| Matthäus (40) | 28 | 1071 | 22 780 |
| Markus (41) | 16 | 678 | 14 235 |
| Lukas (42) | 24 | 1151 | 24 552 |
| Johannes (43) | 21 | 879 | 18 751 |
| Apostelgeschichte (44) | 28 | 1006 | 22 361 |
| Römer bis Kolosser (45–51) | 71 | 1517 | 32 512 |
| 1. Thessalonicher (52) | 5 | 89 | 1 806 |
| 2. Thessalonicher (53) | 3 | 47 | 1 011 |
| 1. Timotheus (54) | 6 | 113 | 2 212 |
| 2. Timotheus (55) | 4 | 83 | 1 662 |
| Titus (56) | 3 | 46 | 935 |
| Philemon (57) | 1 | 25 | 454 |
| Hebräer (58) | 13 | 303 | 6 543 |
| Jakobus (59) | 5 | 108 | 2 270 |
| 1. Petrus (60) | 5 | 105 | 2 354 |
| 2. Petrus (61) | 3 | 61 | 1 562 |
| 1. Johannes (62) | 5 | 105 | 2 386 |
| 2. Johannes (63) | 1 | 13 | 304 |
| 3. Johannes (64) | 1 | 15 | 310 |
| Judas (65) | 1 | 25 | 578 |
| Offenbarung (66) | 22 | 405 | 10 627 |
| **Summe NT** | **260** | **7957** | **172 518** |
| **Summe gesamt** | **598** | **18 213** | **418 971** |

Jedes Buch ist gegen den Quelltext auf Vollständigkeit geprüft, und für jedes
stimmt die Gegenrechnung (Tokens − Einzelworteinträge = alleinstehende
Satzzeichen). `qa.py` meldet über den gesamten Bestand keine Auffälligkeiten.

## Werkzeuge und Regeln, die aus dem Alten Testament entstanden sind

Die verbindliche Bindungsliste für das AT ist `BINDUNGEN_AT.md` im Werkzeugordner
— inzwischen **über hundert Abschnitte**, einer je Kapitel. Daneben steht seit
2. Mose 32 ein `AUFTRAG_AT.md`, das AT-Gegenstück zu `AUFTRAG_BRIEFE.md`: der
gesamte verbindliche Ablauf an einer Stelle, damit ihn nicht jeder Prompt
wiederholen muss. Der Prompt enthält dann nur noch, was am Kapitel besonders ist.

Die Datei ist beim Annotieren der Genesis gewachsen und enthält jetzt:

- **Die Kollisionsregel.** Zwei deutsche Wörter, die dieselbe Glosse tragen, sind
  im Lesefluss nicht zu unterscheiden. Aufgelöst wird aber **nur, wo sie
  tatsächlich in einem Vers zusammenstehen** — und die Zahl wird über alle 39
  AT-Bücher ausgezählt, nie geschätzt. Eine Auflösung ohne Kollisionsstelle macht
  den Bestand nur inkonsistent.
- **Die Lexikonfalle.** Der Formextrakt zeigt dem nächsten Agenten die
  Korpusmehrheit. Wo eine Handvoll NT-Belege gegen eine Bindung steht, zieht die
  Mehrheit den Agenten auf die falsche Seite. Rund vierzig Wörter sind so
  gefunden und korpusweit korrigiert worden — `HERR`, `Land`, `Knecht`, `Magd`,
  `Dienerin`, `Mädchen`, `Hütte`, `Vieh`, `Not`, `Kummer`, `Grimm` und andere.
- **Die Gegenprobe dazu.** Manche Spaltung *sieht aus* wie eine Falle und ist
  richtig: `Herde` = *herd* sind die Schweine von Gadara, `weiden` = *rule* ist
  die Hirtenmetapher der Offenbarung, `Ziegenbock` = *young goat* ist das Zicklein
  aus Lukas 15. **Vor jedem korpusweiten Zug die Belegverse lesen.**
- **Der Dublettenabgleich.** Wo der Text sich wiederholt (1Mo 20/26, 42/43/44,
  35/48), deckt der Vergleich Fehler auf, die keine Prüfung findet. Er hat
  1Mo 20,11 korrigiert und zwei vertauschte Farbwörter zwischen Nachbarkapiteln
  gefunden.
- **Homographen.** Achtzehn Fälle, in denen dieselbe deutsche Form zwei
  Bedeutungen trägt — `Assur`, `Ham`, `Lot`, `Seba`, `Leiter`, `Warte`, `Junges`,
  `Groschen`, `Mal`, `darum`, `Judas`, `Wagen`, `Serah`, `Becher`, `Lager`,
  `Füllen`, `weiß`, `Würde`. Jede ist positionsgebunden gelöst.
- **Keine Namensdeutung ohne hörbare Ableitung.** Siebenundzwanzig Namensstellen
  von Babel bis Abel-Mizrajim, **keine einzige Ausnahme** — der l1912mod deutet
  nirgends, und wo Luther transliterierte, übersetzt er (`Machpela` →
  `Doppelhöhle`, `Mizpa` → `Warte`, `Silo` → `Held`, `Schekel` → `Lot`).

Neue Prüfskripte im Werkzeugordner:

- **`ausreisser.py`** — sucht Fälle, in denen drei Sprachen sich einig sind und
  die vierte abweicht. Findet Positionsverschiebungen und mechanisch angewandte
  Grammatikregeln, die `konsistenz.py` prinzipiell nicht sehen kann. Erster Lauf:
  862 Verdachtsfälle, 44 echte Fehler.
- **`lexicon.py` mit `"verwandt"`-Abschnitt** — schlägt auch über das Lemma nach,
  nicht nur über die Wortform. Ohne ihn wären mehrfach Wörter neu erfunden worden,
  die längst im Bestand standen. **In Namenskapiteln liefert er allerdings mehr
  Rauschen als Signal** (`Gosen`→`gießen`, `jüngerer`→`Jünger`).
- **`hilfsverb.py`** — findet Hilfsverben, deren Glosse das Vollverb des
  Nachbartokens verschluckt. „ich **würde** **sterben**" trug an `würde` die
  volle Verbform *moriría/mourrais/morirei*, und im Lesefluss stand an beiden
  Tokens dasselbe Verb. `qa.py` sieht das nicht: strukturell ist der Eintrag
  perfekt, und die Glossen sind nicht identisch, sondern nur **stammgleich**.
  Erster Lauf über den gesamten Bestand: vier Verdachtsfälle, **zwei echte
  Fehler** (1Mo 19,19 · 1Kor 14,25), beide nach dem SPEC-Muster periphrastisch
  korrigiert (*iba a / allais / stavo per*).

### 3. Mose: der Prompt-Hinweis ist der unzuverlässigste Teil des Verfahrens

Das dritte Buch hat den Befund aus der Offenbarung in einer Deutlichkeit
bestätigt, die überrascht hat: **in fast jedem Kapitel lagen mehrere meiner
Vokabelhinweise daneben** — und zwar nicht bei Randwörtern, sondern bei den
Leitbegriffen des jeweiligen Kapitels.

| Kapitel | ich schrieb | der Text sagt |
|---|---|---|
| 16 | `Sühneort`, `das Allerheiligste`, `sich kasteien`, `Kopfbund` | `Gnadenstuhl`, `das innere Heiligtum`, `fasten`, `Kopfschmuck` — **sieben von acht Hinweisen falsch** |
| 18 | `Blöße aufdecken`, `Gräuel`, `Unzucht`, `ausspeien` | `mit … schlafen` (19 Satzklammern), `abscheulich`, `Frevel`, `ausstoßen` |
| 25 | `Erbbesitz`, `einlösen`, `Loskauf`, `Nachlese`, `Kaufpreis` … | `Besitz`, `auslösen`, `Rückkauf`, `Preis` — **sieben Leitbegriffe kommen im ganzen Kapitel nicht vor** |
| 27 | `Schekel`, `Bann`, `einlösen`, `Zehntel` | `Silberlinge`, `unwiderruflich geweiht`, `auslösen`, `Zehnter` |
| 11 | `Huf`, `Aas` | `Klaue`, `Kadaver` |
| 13 | `heller Fleck`, `Grind`, `wildes Fleisch`, `Einschlag`, `Leder` | `weißer Fleck`, `Ausschlag`, `offenes Fleisch`, `Schuss`, `Fell`/`Fellwerk` |
| 20 | „soll getötet werden", „ihr Blut sei auf ihnen" | schlicht `sterben`, `ausrotten` |
| 22 | die Mängelliste sei das Gegenstück zu 21,18–20 | die beiden Listen sind **fast disjunkt** |

**Jeder dieser Fälle wurde vom Agenten gemeldet, keiner von mir gefunden.**
Der Satz „Der Quelltext hat immer recht" ist deshalb kein Zierrat im Prompt,
sondern die Bedingung dafür, dass Prompt-Hinweise überhaupt nützen dürfen.

### Listen-Prüfskripte: acht Läufe, null Abweichungen

Jedes listenhaltige Kapitel bekam die Auflage, ein **eigenes Prüfskript mit neu
getippter Erwartungsliste** zu schreiben, das die Position jedes Glieds aus dem
Quelltext ableitet. Bilanz für 3. Mose: 52 Glieder (Speisegesetze, 11) · 47
(Verwandtschaftsgrade, 18) · 93 (Kalenderzahlen, 23) · 50 (Tariftafel, 27) ·
18 (Gebrechen, 21) · 12 (Fettteile, 9) · 10 (Mängel, 22) · 4 (Talion, 24) —
**keine einzige Abweichung**. Die Tariftafel von Kapitel 27 hatte zusätzlich
eine Gegenprobe gegen Auslassung, damit die Tabelle nicht durch Weglassen
sauber wird.

### Was `crosscheck.py` an einer geteilten Kapitelgrenze findet

Drei Kapitel gingen an zwei Agenten (13, 14, 25). Der Abschnittsvergleich
meldete 28, 18 und 25 Divergenzen — **fast alle legitime Genus- und
Numerusvarianten, und ein echter Fehler**: `verblasst` trug in 13,6/21/26/28
maskuline Glossen, obwohl `marca`, `marque`, `quemadura` und `brûlure` feminin
sind. Die zweite Kapitelhälfte hatte dieselbe Formel richtig. Ohne den
Vergleich wäre das nicht aufgefallen — der Validator sieht Kongruenz nicht.

### Sieben deutsche Wörter für „ein ewiges Gesetz"

Der l1912mod wechselt in 3. Mose zwischen `Ordnung`, `Recht`, `Gesetz`,
`Regel`, `Rechtsvorschrift` und — nur in Kapitel 18 — `Satzung` und
`Rechtsbestimmung`. Alle sieben behalten ihre eigene Glosse. Dasselbe gilt für
die vier Sühne-Wörter (`sühnen`, `Sühne leisten`, `entsündigen`, `entsühnen`),
die in 14,52 f. sogar in **benachbarten Versen** verschieden gewählt sind.
**Der Text unterscheidet, also unterscheidet die Annotation.**

### Was zwei gleichzeitig laufende Agenten kostet

Dreimal haben parallel laufende Kapitel dasselbe neue Wort verschieden
geprägt: `Webebrust`/`Hebeschulter` (7 gegen 10), `Wahrsager` (19 gegen 20),
`Feueropfer` und drei weitere Bindungen, die ich selbst falsch vorgegeben
hatte. Alle drei Fälle waren mechanisch zu heilen, weil die Kapitelquellen
vorliegen — aber sie sind der Preis der Parallelität und **müssen beim
Einsammeln aktiv gesucht werden**; kein Werkzeug meldet sie von allein.
Die Gegenprobe: `Webeopfer` haben zwei Agenten unabhängig **identisch**
gewählt.

### 4. Mose: die Rechenprobe ist die schärfste Prüfung

Das vierte Buch besteht über weite Strecken aus Zahlen — zwei Musterungen,
ein Opferkalender, eine Tariftafel, eine Beuteteilung. Jedes zahlenhaltige
Kapitel bekam die Auflage, **die Rechnung selbst nachzuvollziehen**, nicht nur
die Ziffern gegen den Quelltext zu halten. Das hat dreimal etwas gefunden, was
keine Strukturprüfung sehen kann:

- **4Mo 3:** 7500 + 8600 + 6200 = 22 300, aber V39 nennt 22 000. Der Agent hat
  beide Seiten am Quelltext nachgelesen und **gemeldet statt korrigiert**.
- **4Mo 7,88:** der Summenvers nennt sechzig Böcke, die zwölf Einzelverse
  listen keinen. Gegen den Luther 1912 geprüft (die Lücke steht schon dort)
  **und** gegen den Schlachter 1951 (der hat „fünf Böcke" je Vers, dort geht
  die Summe auf). Also eine Eigenheit der Vorlage.
- **4Mo 26 und 31:** beide Proben gehen vollständig auf — 601 730 wie in 26,51,
  und alle sechzehn Teilrechnungen der Beuteteilung. Die zweite Kapitelhälfte
  von 26 hat die Summe **unabhängig neu addiert**, statt die Zahlen des ersten
  Agenten zu übernehmen.

**Wo eine Probe nicht aufgeht, ist zuerst der Quelltext zu prüfen, nicht die
Annotation.** Beide Male lag es am Text.

### Wörtlich identische Verse sind die Ausnahme — bis 4. Mose 7

Nach hunderten von Dublettenvergleichen in 3. und 4. Mose war das Ergebnis fast
immer dasselbe: **kein Paar ist wörtlich gleich.** Die Ausnahmen ließen sich an
einer Hand abzählen (3Mo 3,4 = 3,10 = 3,15 · 4Mo 4,35 = 4,39 = 4,43 ·
4Mo 23,1 = 23,29).

**4. Mose 7 kippt das Bild:** dort sind **48 Verse wörtlich identisch** — die
vier Gabenverse jedes der zwölf Fürstenblöcke. Beide Agenten haben sie
**maschinell kopiert** und jede Kopie einzeln gegen den Quelltext geprüft,
statt sie zwölfmal zu tippen. Das ist bei dieser Textsorte der einzige Weg,
weder Tipp- noch Ermüdungsfehler zu produzieren.

Und die Ausnahme der Ausnahme: der Dankopfervers weicht in allen zwölf Blöcken
an **genau zwei Positionen** ab, die Kopfverse haben **vier Bauarten**, und
7,60 bricht sogar diese (eingeschobener Artikel, Vatername im Nominativ).
Wer den Block abgeschrieben hätte, hätte genau dort gefehlt.

### Namen: der Text entscheidet, ob übersetzt oder stehen gelassen wird

Die Regel „keine Namensdeutung ohne hörbare Ableitung" hat sich in vier Fällen
bewähren müssen, und das Kriterium hat jedes Mal getragen:

| Stelle | Text | Behandlung |
|---|---|---|
| 4Mo 11,34 `Lustgräber` | Luther **verdeutscht selbst** | übersetzt (*graves of craving*) |
| 4Mo 13,24 `Eskol` | nennt nur den **Grund** („wegen der Traube") | Eigenname |
| 4Mo 20,13 `Haderwasser` | Luther **verdeutscht selbst** | übersetzt (*water of strife*) |
| 4Mo 21,3 · 32,42 `Horma`, `Nobah` | berichten nur die **Benennung** | Eigenname |

Dasselbe gilt für Gattungswörter in Ortsnamen: 4Mo 34 sagt `Steige Akrabbim`,
`Dorf Adar`, `Meer Kinneret`, 4Mo 22 sagt `die Gassenstadt` und `die Höhe
Baals` — **das Gattungswort wird übersetzt, der Name bleibt stehen.**

### Textvarianten bleiben stehen

Dreimal sah eine Stelle nach einem Fehler aus und war keiner. Jedes Mal hat der
Vergleich mit dem **unmodernisierten Luther 1912** entschieden:

- `Deguel` (1,14 · 7,42 · 10,20) gegen `Reguel` (2,14) — der Luther hat es
  genauso, und er folgt dem hebräischen Text.
- 4Mo 12,3 sagt nicht „demütig", sondern **`geplagt`** — Luther: „ein sehr
  geplagter Mensch".
- 4Mo 34,14 nennt den Stamm **Gad nicht**, obwohl der Folgevers mit zwei
  Stämmen rechnet — die Lücke steht schon im Luther.

Dazu die Schreibungsvarianten innerhalb des Buches, alle stehen gelassen:
`Basan`/`Baschan`, `Eskol`/`Eschkol`, `Kades`/`Kadesch-Barnea`,
`Ahieser`/`Ahi-Eser`, `Pinehas`/`Pinhas`, `Pihachiroth`/`Hachiroth`,
`Ije-Abarim`/`Ijim` — und die fünf Töchter Zelophehads, die in 4Mo 36 in
**anderer Reihenfolge** stehen als in 26,33 und 27,1.

### Die Dubletten von 2. Mose sind Neuformulierungen

Der wichtigste Einzelbefund des zweiten Buches, **von sieben Agenten unabhängig
vermessen**: die große Dublette 25–31 ↔ 35–40 wiederholt nicht, sie formuliert
neu. Kapitel 34 weicht an über zwanzig Stellen von seiner Vorlage ab, 35 an 24,
36 an 22, 37 an 28, 38 an über zwanzig, 39 an über zwanzig — und **Kapitel 40
weicht innerhalb seiner selbst ab**, Befehl (V1–15) gegen Vollzug (V16–33) an
elf Stellen.

`Bronze`/`Erz` · `Purpurstoff`/`Purpur` · `Gerät`/`Zubehör` · `Vorhof`/`Hof` ·
`Pflöcke`/`Pfähle` · `Becken`/`Waschbecken` · `Ständer`/`Fuß` ·
`Deckplatte`/`Oberseite` · `rundherum` (ein Token) / `rund herum` (zwei) — und
in 35,31 stehen Adjektive, wo 31,3 Substantive hat. **Wer abschreibt,
glossiert falsch.**

In 3. Mose 3 hat dasselbe Verfahren in einem Kapitel mit drei Fassungen
**45 Abweichungsblöcke** gefunden und genau **einen** Vers, der wörtlich
dreimal identisch dasteht.

### `Fuß` und `Kopf` tragen im Stiftshüttenblock die Bauteillesart

`Fuß` = *sockets/basas/bases/basamenti* (der Sockel), `Kopf` =
*capitals/capiteles/chapiteaux/capitelli* (das Säulenkapitell). **Zwei
A1-Körperteilwörter, die im ganzen Bauabschnitt etwas anderes bedeuten** — und
drei Verse weiter steht „pro Kopf" und meint wieder den Kopf, und 2Mo 40,31
wäscht Hände und Füße. Beide behalten ihr A1-Level, weil das Level am Lemma
hängt: eine Anhebung zöge 57 bzw. 66 Körperteil-Einträge mit.

Der Lexikonextrakt bietet für 2. Mose fast nur die Sockel-Lesart an. Wer sie
übernimmt, macht aus Tischfüßen Sockel, und strukturell fällt nichts auf.

### 5. Mose: das Buch erzählt nach, ohne zu zitieren

Das fünfte Buch ist über weite Strecken Wiederholung — und **fast nirgends
Wiederholung des Wortlauts**. Die Agenten haben jede Parallele Token für Token
vermessen, und das Ergebnis ist über 34 Kapitel gleich:

| Parallele | Ergebnis |
|---|---|
| 5Mo 2 ↔ 4Mo 20/21 | **kein Vers wörtlich gleich** (0,06–0,57) |
| 5Mo 9 ↔ 2Mo 32/34 | **keiner** (max. 0,62) |
| 5Mo 14 ↔ 3Mo 11 | **keiner** (0,11–0,64) |
| 5Mo 19 ↔ 4Mo 35 | **keiner** (0,03–0,29) |
| 5Mo 25 ↔ 2Mo 17 | **keiner**, zwei Paare mit **null** gemeinsamen Inhaltswörtern |
| 5Mo 5 ↔ 2Mo 20 (Dekalog) | **4 von 16** wörtlich gleich |
| 5Mo 11 ↔ 5Mo 6 | **1 von 9** (11,20 ↔ 6,9, Ähnlichkeit 0,87) |
| 5Mo 31 ↔ 5Mo 1 | **1 Satz** (31,8 Schluss = 1,21 Schluss) |
| 5Mo 15,23 ↔ 5Mo 12,16 | **0,93** — Unterschied ist ein Wort |

Die Konsequenz für den Prompt: **die Parallelstelle liefert das Vokabular,
nicht den Satz.** Wer sie als Vorlage nimmt, annotiert einen Text, der nicht
dasteht. Bei 5Mo 9,12 sagt 2. Mose `ein gegossenes Kalb`, 5. Mose `ein
gegossenes Bild`; bei 9,27 sagt 2. Mose `Abraham, Isaak und Israel`, 5. Mose
`… und Jakob`.

### Fünf Doppelschreibungen im selben Buch

Der Quelltext ist bei Eigennamen und einem Gattungswort **in sich
uneinheitlich**. Das ist kein Modernisierungsfehler, den man glätten dürfte —
jede Stelle behält ihre Schreibung als Lemma, alle teilen die Glosse:

| erste Form | zweite Form |
|---|---|
| `Hetiter`, `Perisiter`, `Hiwiter` (7,1) | `Hethiter`, `Pheresiter`, `Heviter` (20,17) |
| `Gräuel` (Kap. 7 · 12 · 13 · 17 · 18) | `Greuel` (Kap. 22 · 23 · 24 · 25) |
| `Hesbon`, `Basan` (2,24 · 3,1) | `Heschbon`, `Baschan` (29,6 · 33,22) |
| `Naphthali` (27,13) | `Naphtali` (33,23 · 34,2) |
| `Isaschar` (27,12) | `Issaschar` (33,18) |

Bei den Völkerlisten ist **7,1 die Abweichung, nicht 20,17**: `Hethiter` steht
17× im Bestand, `Hetiter` nirgends. Beim `Gräuel`/`Greuel`-Paar liegt ein
sauberer Bruch in der Mitte des Buches.

### Die Schema-Formel schrumpft von Kapitel zu Kapitel

Nur **6,5** hat alle drei Glieder. Danach ist sie jedes Mal verkürzt, und die
Präposition wechselt — das sind verschiedene Mehrwort-Einträge mit
verschiedenen Levels (`von ganzem Herzen` B1 gegen `mit ganzem Herzen` B2):

| Stelle | Wortlaut |
|---|---|
| 6,5 | `mit ganzem Herzen`, `mit ganzer Seele`, `mit aller Kraft` |
| 10,12 · 11,13 | `von ganzem Herzen und ganzer Seele` — kein `Kraft`, `von` statt `mit` |
| 13,4 | `von ganzem Herzen` — nur eines |
| 26,16 · 30,2.6.10 | `mit ganzem Herzen und ganzer Seele` — vierte Variante |

`Kraft` = *strength* gilt deshalb **nur** in der Formel; sonst ist es *power*.
Ausnahme mit eigener Begründung: 21,17 („der Erste seiner Kraft" =
Zeugungskraft) und 34,7 (Körperkraft des Greises), wo `Macht` = *power* im
selben Kapitel steht.

### Vorgegebene Wörter, die im Text nicht stehen

Über die 34 Kapitel haben die Agenten **weit über zweihundert** Prompt-Hinweise
widerlegt. Die Quote steigt mit der Textsorte: Gesetzesprosa etwa zehn bis
fünfzehn je Kapitel, das Moselied (32) **19 von 34 geprüften Behauptungen**.

Wiederkehrendes Muster: der Text **umschreibt**, wo Bibelkenntnis ein Kompositum
erwartet. Statt `Mischsaat` „mit verschiedenen Samen bepflanzen", statt
`Geldstrafe` „zu hundert Silberstücken verurteilen", statt `Gefangenschaft`
„dein Schicksal wenden", statt der Bann-Formel `dem Untergang weihen`. Und er
wählt andere Wörter: `Beamte` statt `Amtleute` (16,18, aber `Amtleute` in 20
und 29), `Zelt der Begegnung` statt `Stiftshütte`, `Wasserträger` statt
`Wasserschöpfer`, `junge Kuh` statt `Kalb`, `zurechtweisen` statt `züchtigen`,
`Jesurun` statt `Jeschurun`, `Haderwasser` statt `Meriba`, `Südland` statt
`Negeb`.

**Auch Strukturannahmen sind Hypothesen.** Der Prompt zu 27 verlangte zu
prüfen, ob die Rahmenformel der zwölf Fluchsprüche identisch ist — sie ist es
nicht: 27,15 sagt `antworten`, die elf übrigen `sagen`. Der Prompt zu 28
behauptete, die Segensreihe spiegle die Fluchreihe Glied für Glied — `Korb` und
`Frucht` sind vertauscht, und 28,18 ist gegenüber 28,4 gekürzt. Der Prompt zu
28 behauptete, 28,59–61 nehme die Krankheitsliste aus 28,21–28 auf — die
Schnittmenge ist **leer**: fünfzehn spezifische Übel dort, drei Sammelbegriffe
hier. Und einmal lag sogar die **Versgrenze** falsch (23,4–6 statt 23,5–6).

### Ein Grammatikfehler im Bibeltext

5Mo 23,10: „Wenn **du** gegen deine Feinde **auszieht**…" — Subjekt 2. Sg.,
Verb 3. Sg. Das ist ein Modernisierungsfehler in `l1912mod`, kein
Annotationsproblem. Die Annotation folgt dem Subjekt; **die Stelle gehört im
Bibeltext korrigiert**, richtig wäre `ausziehst`.

### Was buchweite Angleichungen kosten können

Als `Völker` von *nations* auf *peoples* gezogen wurde, blieben die Artikel und
Adjektive davor stehen — *naciones/nations/nazioni* sind feminin,
*pueblos/peuples/popoli* maskulin. **27 Glossen in Kapitel 7 und eine in 6,14
standen danach im falschen Genus** (`todas`, `toutes`, `tutte`, `muchas`,
`estas`, `de las`). Gefunden hat es der Agent von Kapitel 14, nicht die
Prüfskripte. Dasselbe Muster bei neun italienischen Artikeln vor `Weg` (*il*
statt *la*, weil `Weg` mit *via* glossiert ist).

**Konsequenz:** nach jeder buchweiten Glossenänderung die **Nachbarpositionen**
mitprüfen, nicht nur das geänderte Wort.

### Die Königsbücher: der Versatz ist gefährlicher als die Abweichung

In den bisherigen Büchern war die Regel „die Dublette formuliert neu" — man
durfte nichts abschreiben, weil der Text fast nie wörtlich wiederholt. Die
Königsbücher zeigen den **zweiten, schwereren Fall**: Blöcke, die *wirklich*
wörtlich identisch sind, aber an **verschobener Position** stehen. Wer sie als
Block überträgt, produziert einen strukturell tadellosen und inhaltlich um *n*
Positionen verrutschten Eintrag, den kein Validator sieht.

| Stelle | Befund |
|---|---|
| 2Kön 7,1 ↔ 7,18 | gleicher Wortlaut, **vertauschte Reihenfolge** der beiden Preisglieder — beide Verse 34 Tokens, `kosten` springt trotzdem von 26 auf 25 |
| 2Kön 8,18 ↔ 8,27 | `tat, was dem HERRN missfiel` einmal am Versende, einmal vorn — **Versatz 15** |
| 2Kön 9,18 ↔ 9,20 | identischer 7-Token-Block, **Versatz −30** |
| 2Kön 11,4 ↔ 11,12 | `den Sohn des`, **Versatz −39** |
| 2Kön 10,1–7 | im ganzen Briefwechsel liegt **kein einziger** identischer Block an gleicher Position (−18 bis +29) |
| 2Kön 2,3 ↔ 2,5 | 30 von 32 Tokens gleich — ein zusätzliches `heraus` verschiebt **alles danach um eins** |

Die Konsequenz für den Prompt: **messen, nicht annehmen.** Jedes Kapitel mit
Wiederholungen bekommt ein eigenes Prüfskript, das den **Versatz** jedes
identischen Blocks ausgibt und in jedem Block alle sechs Felder gegeneinander
hält. Wo der Vergleich Gleichheit ausweist, ist Kopieren richtig (1Kön 19,10 =
19,14 mit 45 von 45 Tokens, 1Kön 22,6 = 22,12 = 22,15); wo nicht, ist es der
sicherste Weg in einen unsichtbaren Fehler.

**Und der umgekehrte Fall.** In 2Kön 9,21 und 9,27 steht zweimal wörtlich
`Sie trafen ihn` — einmal „begegnen", einmal „mit der Waffe treffen", nach dem
Befehl „Erschlagt auch ihn!". **Ein identischer Block darf nicht automatisch
dieselbe Glosse bekommen.** Gleichheit des Wortlauts ist ein Grund
nachzusehen, kein Grund zu kopieren.

### Was zwei gleichzeitig laufende Agenten in den Königsbüchern gekostet haben

Zweimal ist eingetreten, wovor die Erfahrung aus 3. Mose warnt — und beide Male
hat es **kein Prüfskript** gemeldet, weil beide Fassungen strukturell tadellos
sind:

- **Die Quellenformel.** „Was es sonst noch über X zu berichten gibt" steht
  achtmal wortgleich im Text und war von vier parallel laufenden Agenten
  **dreifach verschieden** geprägt: `berichten` als *tell* oder *report*, `über`
  als *de/de/di* oder *sobre/sur/su*, `zu` als *a/à/a* oder *de/de/di*, und
  `es gibt` einmal als Mehrwort-Eintrag, dreimal nicht. Vereinheitlicht auf die
  Fassung von 1Kön 11,41, der drei der vier Kapitel bereits folgten.
- **`Gehasi` im Italienischen** — elfmal *Giezi* in 2Kön 4, sechsmal *Ghiezi* in
  2Kön 5, beide Kapitel gleichzeitig gelaufen. Mit `remap.py` auf die Mehrheit
  gezogen.

Die Gegenprobe gibt es auch: `Ahasja` haben der Agent von 1Kön 22 und der von
2Kön 1 **unabhängig identisch** geprägt (*Ahaziah / Ocozías / Achazia /
Acazia*).

**Die Lehre bleibt dieselbe wie in 3. Mose:** Parallelität ist bezahlbar, weil
die Kapitelquellen vorliegen und `remap.py` in beides schreibt — aber die
Divergenzen **müssen beim Einsammeln aktiv gesucht werden**. Der einzige
verlässliche Ort dafür ist ein Wort, das in mehreren Kapiteln neu entsteht.

### Bei `steht` entscheidet der Text, nicht die Mehrheit

Die Chronikformel endet in 1Kön 11,41 auf „das steht in der Chronik Salomos
**geschrieben**", überall sonst nur auf „das steht in der Chronik". Nach dem
Mehrheitsprinzip wäre alles auf eine Lesart zu ziehen — richtig ist das
Gegenteil: Wo `geschrieben` als zweites Token dasteht, deckt ein
`parts`-Eintrag `geschrieben stehen` die Bedeutung ab und das Einzelwort `steht`
bleibt wörtlich (*stands*). Wo es fehlt, muss `steht` die Bedeutung **allein**
tragen (*is written / está escrito / est écrit / è scritto*). Neun Einträge sind
so korrigiert worden, und 11,41 bleibt bewusst anders.

### Zwei Rechenfehler an der Lexikonfalle

Vier Agenten haben unabhängig gemeldet, `BINDUNGEN_AT.md` widerspreche dem
Lexikon-Extrakt bei `nämlich`. Nachgezählt stimmt die Tabelle: von 49 Belegen
für *in fact* sind **41 aus dem NT**, im AT steht die Lesart nur achtmal.
**`lexicon.py` und `fixgloss.py` trennen nicht nach Testamenten** — wer die
Gesamtzahl gegen die Tabelle hält, hält die Falle gegen die Warnung davor.

In der Sache hatten die Agenten trotzdem recht: im AT steht `nämlich` **14:14**
zwischen der erklärenden Lesart (*namely*) und der kausalen (*in fact* / *for*).
Die Tabelle nennt je Lemma die häufigste AT-Lesart, auch wo das Wort schlicht
zwei Bedeutungen hat und es gar keine Bindung geben kann. Beides steht jetzt in
`AUFTRAG_AT.md`.

**Dazu eine Lücke im Hinweis-Skript:** `hints.py` blendet Funktionswörter aus
der Kollisionsprüfung aus, sonst ersäuft der Bericht im Rauschen. Auf dieser
Liste stehen aber `aus`, `an`, `auf`, `zu`, `nach`, `vor`, `über`, `um` — also
die **Partikeln trennbarer Verben**, die eine eigene Bedeutung tragen. In
2Kön 6,7 standen `aus` (von *ausstrecken*) und `heraus` im selben Vers mit
identischer Glosse in allen vier Sprachen, ohne gemeldet zu werden; dasselbe in
10,26 und 11,7. Kein Fehler im Skript, aber ein blinder Fleck, der in den
Auftrag gehört.

### Prompt-Hinweise: die Quote bleibt hoch

Über die 32 Kapitel der Königsbücher haben die Agenten wieder **weit über
hundert** Vorgaben widerlegt. Die auffälligsten:

| ich schrieb | der Text sagt |
|---|---|
| Saba, Tarsis, Kue | `Reicharabien`, `Hochseeflotte`, schlicht `Waren` |
| Talente, Minen, Schekel | `Zentner`, `Lot`, `Pfund`, `Silberling` |
| „ein Maß Feinmehl für einen Schekel" | `ein Scheffel feines Mehl einen Silberling` |
| Gottesmann | `Mann Gottes` (14× in einem Kapitel, nie anders) |
| „schlief sich zu seinen Vätern" | `Dann starb X und wurde begraben` — die Wendung existiert nicht |
| Säuseln, Wirbelwind | `ein leises, sanftes Flüstern`, `Sturm` |
| Höhen, Tempelhurer | `Kulthöhen`/`Opferhöhen`, `Tempelprostituierte`, `Kultprostituierte` |
| Adjutant, Beth-Eked, Baalstempel | `Offizier`, `Hirtenhaus`, `Tempel Baals` (zweiwortig) |
| Astarte, Molech, Bascha, Nabot, Aphek, Ramoth | `Astoreth`, `Moloch`, `Baesa`, `Naboth`, `Afek`, `Ramot` |
| zwölf Löwen auf sechs Stufen | **vierzehn** — zwei an den Armlehnen, „zwölf weitere" |
| „viermal vier Krüge" | vier Krüge in **drei** Durchgängen |

Zwei Fälle sind besonders lehrreich, weil sie keine Vokabelfrage sind:
**2Kön 3,1** sagt „Im **achtzehnten** Jahr Joschafats", nicht im zwölften — die
Zwölf gilt allein der Regierungsdauer. Und **1Kön 18,29** hat `rasten`, was
keine Form von „rasten" ist, sondern von **`rasen`** (dieselbe Szene wie
1Sam 18,10) — ein Agent, der die naheliegende Lesart nimmt, produziert einen
strukturell tadellosen Eintrag mit der falschen Bedeutung.

### Das Einzelwort schluckt seine Mehrwort-Einheit — der häufigste stille Fehler

`hilfsverb.py` sucht Hilfsverben, deren Glosse das Vollverb des Nachbartokens
verschluckt. Beim Abschluss von 2. Könige hat sich gezeigt, dass **derselbe
Fehler auch bei Vollverben auftritt**, und dort meldet ihn kein Skript. Vier
Fälle in zehn Kapiteln, jeder von einem anderen Agenten produziert:

| Stelle | Mehrwort-Eintrag | Einzelwort trug | richtig ist |
|---|---|---|---|
| 17,17 | `gehen lassen` = *made pass* | `gehen` = *pasar · passer · passare* | *ir · aller · andare* |
| 17,6 · 18,11 | `fortführen` = *emmena* | `führte` = fr *emmena* | fr *conduisit* |
| 25,26 | `sich aufmachen` = *set out* | `machte` = *puso · mit · mise* | *hizo · fit · fece* |

Die Spezifikation sagt es klar: **die Einzelwörter behalten ihre wörtliche
Bedeutung, der Mehrwort-Eintrag trägt die Bedeutung der Einheit.** Strukturell
ist jeder dieser Einträge tadellos, und `qa.py` sieht nichts — im Lesefluss
steht aber an zwei Tokens dasselbe Wort. Gefunden wurden alle drei erst beim
**paarweisen Abgleich der gleichzeitig gelaufenen Kapitel**; der Präzedenzfall
steht jedes Mal schon im Bestand (5Mo 18,10 für `gehen`, 16,9 für `führte`).

### Der Abgleich paralleler Kapitel, systematisch

Die Warnung aus 3. Mose („die Divergenzen müssen beim Einsammeln aktiv gesucht
werden") ist für 2. Könige 16–25 in ein festes Verfahren übersetzt worden:
nach jedem Kapitel werden die **gemeinsamen Inhaltswortformen** gegen jedes
gleichzeitig gelaufene und jedes schon fertige Nachbarkapitel gehalten,
Funktionswörter ausgeblendet. Typisch sind 40 bis 98 gemeinsame Formen je Paar
und 4 bis 21 abweichende Lesarten — davon fast alle legitim (Genus, Numerus,
Kasus, Kontext), aber in jeder Welle ein bis zwei echte.

Über ein Dutzend Korrekturen sind so entstanden, die meisten **korpusweit**:

| Befund | Umfang |
|---|---|
| `an` in der Nachfolgeformel stand auf *in·en·à·al* statt *at·a·à·al* | 11 Einträge in 4 Büchern |
| `le ÉTERNEL` statt `l'ÉTERNEL` — im Französischen schlicht falsch | 62 Einträge in 6 Büchern |
| `Völker` auf *nations* statt *peoples*, samt Nachbarpositionen | 4 Stellen |
| `spricht` in der Botenformel fr *dit* statt *parle* | 22 Einträge in 5 Büchern |
| `ganz wie` mit drei verschiedenen Lesarten | 4 Stellen |
| `Nebats` es *de Nabat* / fr *de Nebath* gegen 19 einheitliche Belege | 1 Eintrag |
| `verstoßen`, `führte`, `heute`, `Kraft`, `Genauso` | je 1–3 Einträge |

**Die Botenformel** ist der lehrreichste Fall, weil die Mehrheit allein die
falsche Antwort gegeben hätte: `spricht der HERR` stand 26:19 zwischen *parle*
und *dit*, in 2. Könige intern 4:4. Die Belege trennen sich aber sauber nach
der **Stellung** — einleitend *parle*, nachgestellt nach Komma *dit*, genau wie
in der LSG. Alle vier eindeutig nachgestellten Belege hatten es schon richtig.
Die Regel steht jetzt in `BINDUNGEN_KOENIGE.md`.

### Ein gemeinsamer Satz, vorab gebunden

23,31 und 24,18 enthalten denselben Satz („Seine Mutter hieß Hamutal und war
eine Tochter Jeremias aus Libna"), und beide Kapitel liefen **gleichzeitig**.
Statt es hinterher zu reparieren, haben beide Prompts dasselbe Muster aus dem
bereits fertigen 22,1 mitbekommen, mit der Auflage, die Positionen im eigenen
Quelltext zu messen. Ergebnis: **Versatz 0, alle elf Tokens in allen sechs
Feldern identisch** — zwei Agenten, kein Abgleich nötig.

Dasselbe hat bei den Blöcken funktioniert, die *nicht* an gleicher Position
stehen: 18,8 ↔ 17,9 mit Versatz −12, 18,11 ↔ 17,6 mit Versatz −7, 21,2 ↔ 16,3
mit Versatz −10, 19,34 ↔ 20,6 mit Versatz −16. Jedes Mal hat der Agent ein
eigenes Prüfskript geschrieben, das die Positionen aus **beiden** Quelltexten
ableitet; jedes Mal habe ich es unabhängig nachgerechnet. Null Abweichungen.

**Die Konsequenz für die Reihenfolge:** Kapitel mit einem wortgleichen Block
gehören nicht in dieselbe Welle, wenn eines das andere als Vorlage braucht
(17 vor 18 vor 19). Wo sich das nicht vermeiden lässt, ist die Vorab-Bindung
im Prompt der Ersatz dafür — sie kostet nichts und hat hier vollständig
getragen.

### `ausreisser.py` beim Buchabschluss: 336 Verdachtsfälle, kein Fehler

Der Lauf über das fertige Buch meldet 336 Stellen, an denen drei Sprachen sich
einig sind und die vierte abweicht. Am Vers nachgesehen ist **keine davon ein
Fehler**, und die Fehltreffer fallen in wiederkehrende Klassen, die das Skript
prinzipiell nicht erkennen kann:

- **Französische Elision** — `parce qu'`, `afin qu'`, `jusqu'` vor Vokal
- **Genuskongruenz der Zielsprache** — `l'année suivante`, `ma colère`
- **Großschreibung in Namen** — `King Hezekiah`, `Mount`, `Valley`
- **Buchlokale Bindungen** — `in die Hand` ist in den Königsbüchern fr *mains*
- **Bewusste Kollisionsauflösungen** — `denn` = *since* neben `für` = *for*

Der einzige Treffer, den ich übernommen habe, war `Genauso` = *The same way*
gegen zwölf von dreizehn Belegen *In the same way*. `hilfsverb.py` meldet über
das ganze Buch 0 Verdachtsfälle.

### Was 2. Könige an eigenen Formeln gebracht hat

- **Drei Nachfolgeformeln in einem Kapitel.** 23,30 sagt `an der Stelle seines
  Vaters` (eigenes Bestandslemma `an der Stelle`), 23,34 `anstelle` als **ein**
  Token — und die Standardfassung `an seiner Stelle` kommt in Kapitel 23 gar
  nicht vor.
- **Die Schema-Formel außerhalb von 5. Mose.** 23,3 hat zwei Glieder mit
  Präpositionswechsel (`von ganzem Herzen` B1 gegen `mit ganzer Seele` B2),
  23,25 alle drei. `Kraft` = *strength* gilt nur dort — 17,36 („mit großer
  Kraft und ausgestrecktem Arm") folgt seiner wörtlichen Parallele 5Mo 9,29
  mit *power*.
- **`geschrieben stehen`** greift dreimal in 23 und zweimal in 22. Wo das
  zweite Token `geschrieben` dasteht, deckt die Spanne die Bedeutung ab und
  `steht` bleibt wörtlich; nur in der Chronikformel trägt `steht` sie allein.
- **Vier Wendungen fürs Wegführen in einem Kapitel** (24,12.14.15): `nahm
  gefangen`, `in die Verbannung führen`, `führte weg` und `führte gefangen` —
  die letzten beiden im selben Vers.
- **`verstoßen` ist zweigleisig, aber nach der Bedeutung.** Mit „aus seinem
  Angesicht" (17,18.20.23 · 24,3.20) ist es *cast out*, ohne den Zusatz
  (13,23 · 21,14) *reject*. Die Agenten von 21 und 24 haben das **unabhängig
  gleich** entschieden.

### Ein Agentenbefund, der der Prüfung nicht standhielt

Der Agent von Kapitel 25 meldete, in **Richter 15,5** trügen zwei Tokens keinen
Einzelwort-Eintrag. Nachgesehen sind alle 28 Positionen belegt und
`validate.py 7` läuft sauber durch. **Auch ein Agentenbefund ist eine
Hypothese** — das gilt in beide Richtungen und ist der Grund, warum jeder
gemeldete Bestandsfehler nachgezählt wird, bevor er korrigiert wird. Von den
Befunden dieser zehn Kapitel haben sich zwölf bestätigt und einer nicht.

Angefangene, noch unvollständige Kapitel liegen unter `anno/_wip/` — siehe den
README dort. Die App lädt diesen Ordner nie. Zurzeit ist der Ordner leer.

## Datenformat

`bibles/deu/l1912mod/anno/<buchNr>_l1912mod_multi.json`, kompakt geschrieben
(ohne Einrückung, wie `bibles/eng/web/anno/*` — Einrückung kostete 39 % Größe
bei einer Datei, die zur Laufzeit pro Buch nachgeladen wird).

```json
{"name": "Matthäus", "chapters": {"1": {"1": [ …Einträge… ]}}}
```

### Einzelwort-Eintrag

```json
{"pos": 3, "form": "Vater", "lemma": "Vater", "level": "A1",
 "en": "father", "es": "padre", "fr": "père", "it": "padre"}
```

- `pos` — 0-basierter Index im Vers, `text.split()`
- `form` — Token **ohne** umschließende Satzzeichen (`"Davids,"` → `"Davids"`)
- `lemma` — Grundform; Artikel/Pronomen normalisiert (`das`/`dem`/`den` → `der`)
- `level` — CEFR **aus Sicht von Deutschlernenden**, bezogen auf das Lemma
- vier Glossen, **kontextuell** korrekt (Tempus, Numerus, Person)

Jede Tokenposition bekommt genau einen Einzelwort-Eintrag. **Ausnahme:**
alleinstehende Satzzeichen (eingeschobene Gedankenstriche wie in Mt 17,20 oder
Mk 7,11) bleiben unannotiert — eine Glosse „dash/tiret" wäre im Lesefluss ein
Übersetzungsetikett an einem Satzzeichen. Die App stellt unannotierte Wörter
als normalen Text dar.

### Mehrwort-Einträge

Zusätzlich zu den Einzelwörtern, nicht statt ihrer. Die Einzelwörter behalten
ihre wörtliche Bedeutung, der Mehrwort-Eintrag trägt die Bedeutung der Einheit.

**Zusammenhängend** — `pos` + `pos_end`:

```json
{"pos": 4, "pos_end": 6, "form": "zur Welt bringen", "lemma": "zur Welt bringen",
 "level": "B1", "en": "give birth to", "es": "dar a luz", …}
```

**Getrennte Satzklammer** — `pos` + `parts` (Liste der Positionen):

```json
{"pos": 1, "parts": [1, 3], "form": "stand auf", "lemma": "aufstehen",
 "level": "A2", "en": "got up", "es": "se levantó", …}
```

`parts` ist für dieses Projekt neu entstanden und beschreibt die deutsche
**Satzklammer**: „Da **stand** Joseph **auf**". `parts[0] == pos`, aufsteigend,
mindestens zwei Positionen, nie zusammenhängend (dann `pos_end`). `form` sind
die Tokens an genau diesen Positionen — also „stand auf", nicht „stand Joseph
auf". Wörter dazwischen gehören nicht dazu und behalten ihre eigenen Glossen.

**Zwei Klammern an derselben Position.** Ein Kausativ kann zwei Infinitive
regieren: „Er **ließ** die Wächter **verhören** und **hinrichten**" (Apg 12,19)
ergibt `ließ verhören` [10,13] und `ließ hinrichten` [10,15]. Beide Einträge
sind richtig, aber `getAnnotation` nimmt mit `verse.find` die **erste**
zutreffende Mehrwort-Annotation — an Position 10 ist also nur eine erreichbar,
die andere über ihre eigene zweite Position. Der Fall ist selten (viermal im
ganzen Bestand, zuerst Mt 23,7 „lassen sich grüßen / nennen") und verliert
keine Daten; er ist nur an der geteilten Position nicht vollständig auflösbar.

Mehrwort-Einträge nur, wenn sich die Bedeutung nicht aus den Teilen ergibt:
trennbare Verben mit Bedeutungsverschiebung (`fing … an`), Funktionsverbgefüge
(`hatte … Angst`, `steht geschrieben`), feste Wendungen (`auf die Probe
stellen`), Reflexiva (`freuten … sich`), Kausativ (`ließ … töten`).
**Nicht** für reine Tempus-/Passivklammern (`hat … gesagt`, `wird … genannt`) —
die funktionieren Wort für Wort.

## Laufzeit (index.html)

- `BIBLES['deu-l1912mod']`: `annoDir`, `annoSuffix: '_l1912mod_multi.json'`,
  `annoGlossLangs: ['en','es','fr','it']`, `hasAnno: true`
- Drei Helfer bündeln die Mehrwort-Logik: `annoIsMulti`, `annoCovers`, `annoLast`
- `getAnnotation`, `getChapterAnnotations` und das Lese-Quiz nutzen sie
- `buildChapClozeMap` überspringt `parts`-Einträge — eine Lücke mit Loch ist
  keine sinnvolle Cloze-Vorlage
- Rein additiv: `pos_end` verhält sich unverändert, die anderen vier Bibeln
  sind nicht betroffen

## Werkzeugkette

Liegt seit dem 11.08.2026 in **`../bibles-translations/anno-tools/`** und ist
damit dauerhaft. Vorher lag sie im Scratchpad und war „beim Fortsetzen in einer
neuen Sitzung neu anzulegen" — genau das ist eingetreten: die gesamte Kette und
die handgepflegte `BINDUNGEN_AT.md` mit über hundert Kapitelabschnitten sind mit
dem Scratchpad verschwunden. Sie ist neu gebaut und gegen den vorhandenen
Bestand geprüft (0 Befunde, alle 29 Bücher bauen byte-identisch neu).

Was der Neubau nicht zurückbringen konnte, ist die handgeschriebene
Bindungsliste. `bindungen.py` erzeugt sie jetzt **aus den Daten** — die
Bindungen stecken ohnehin im fertigen Bestand. Der wertvollste Teil, die
Lexikonfallen, fällt dabei automatisch an.

Die Kernstücke:

| Datei | Zweck |
|---|---|
| `common.py` | Pfade, Tokenisierung, Laden von Quelltext, Quellen und Anno-Dateien |
| `SPEC.md` | verbindliche Spezifikation für die Agenten |
| `AUFTRAG_AT.md` | der verbindliche Ablauf für ein AT-Kapitel, einmal statt in jedem Prompt |
| `buildbook.py <nr>` | baut die Anno-Datei eines Buches aus den Kapitel-JSONs, samt Level-Abgleich |
| `validate.py <nr>\|alle` | Struktur-Validator und Gegenrechnung über ganze Bücher |
| `selfcheck.py <nr> <kap> <datei> [von bis]` | derselbe Validator als Agentenaufruf für ein Kapitel |
| `qa.py <nr>\|alle`, `qa.py --kapitel …` | inhaltliche Heuristiken gegen verrutschte Zuordnungen |
| `lexicon.py <nr> <kap> [von bis] -o <ziel>` | gefilterter Lexikon-Extrakt für einen Versbereich |
| `hints.py <nr> [kap]` | Prompt-Hinweise aus dem **Quelltext** statt aus Bibelkenntnis |
| `konsistenz.py <nr>` | ein Lemma, zwei Lesarten — innerhalb eines Buches und gegen den Bestand |
| `fixgloss.py show\|showform <lemma>`, `verse <nr> <kap> <v>` | alle Lesarten eines Lemmas mit Belegstellen |
| `remap.py <lemma> <feld> alt=neu …` | korpusweite Korrektur, numerus-erhaltend |
| `bindungen.py` | erzeugt `BINDUNGEN_AT.md` aus dem Bestand, samt Lexikonfallen |
| `quellen_sync.py <nr>\|alle` | gewinnt Kapitelquellen aus den gebauten Anno-Dateien zurück |
| `BINDUNGEN_AT.md` | Glossen-Bindungen der Bücher 1–39, erzeugt |
| `BINDUNGEN_3MOSE.md` | die Opfer- und Kultbegriffe von 3. Mose, von Hand gepflegt |
| `BINDUNGEN_KOENIGE.md` | die Formeln der Bücher 11 und 12, von Hand gepflegt |

`crosscheck.py`, `ausreisser.py` und `hilfsverb.py` sind wieder da und beim
Abschluss von 2. Könige gelaufen. Was ihnen fehlt, ist der **paarweise
Abgleich gleichzeitig bearbeiteter Kapitel** — den erledigt bislang ein
Wegwerfskript beim Einsammeln (gemeinsame Inhaltswortformen, Funktionswörter
ausgeblendet). Er hat in 2. Könige mehr echte Fehler gefunden als alle
Prüfskripte zusammen und gehört als `parallelcheck.py` in die Kette.
`levels.py` ist in `buildbook.py` aufgegangen. Die
`BINDUNGEN_OFFB.md` und `BINDUNGEN_BRIEFE.md` sind mit dem Scratchpad
verloren — ihre Festlegungen stehen im fertigen Bestand und werden über
`lexicon.py` und `fixgloss.py` erreicht.

### Der Level-Abgleich hatte einen Aufschaukel-Fehler

Die alte Kette glich Level in vier Durchgängen ab: gleiche Bedeutung, gleiches
Lemma, gleiche Wortform, dann buchübergreifend. Der Wortform-Durchgang und der
Lemma-Durchgang **widersprechen einander**, sobald eine Wortform zu zwei
Lemmata gehört — zwei Läufe hintereinander gaben verschiedene Stände (in
1. Mose 41 Einträge, in Lukas 37). Der Neubau hat nur noch zwei Durchgänge,
und der letzte (gleiches Lemma, Korpusmehrheit) partitioniert alles; damit ist
jedes gebaute Buch ein Fixpunkt. Wortformen mit uneinheitlichem Level werden
nur noch **gemeldet** — das sind Homographen, und die soll niemand automatisch
glätten.

`hints.py`, `konsistenz.py`, `fixgloss.py` und `remap.py` sind für die Bücher
52–65 entstanden. Sie schließen vier Lücken:

**`hints.py` liest den Text, nicht die Bibelkenntnis.** Es vergleicht die
Wortformen eines Kapitels gegen den gesamten annotierten Bestand und meldet,
was dort noch nirgends vorkommt, plus die Verse, in denen zwei Wörter derselben
Bedeutungsgruppe zusammenstehen. Genau das war in der Offenbarung über
dreißigmal schiefgegangen. Es hat sofort geliefert: der Text sagt `Wiederkunft`,
nicht „Ankunft"; Titus benutzt durchgehend `Heiland`, nie `Retter`; `Gnadenthron`
steht in Hebräer an zwei Stellen in zwei verschiedenen Bedeutungen.

**Achtung, zwei Fallen des Werkzeugs selbst.** Erstens ist die Kollisionsprüfung
anfangs über Präfixe gelaufen — `Heil` schlug in `Heiligung` an und erfand eine
Kollision in 2Thess 2,13, die es nicht gibt. Ein Agent hat es gemeldet; die
Liste ist mit exakter Wortformprüfung neu ausgezählt worden, und dabei kamen
drei echte Fälle dazu, darunter **1Petr 4,11 als vierter Vers der
`Macht`-Ausnahme**. Zweitens ist die „noch nicht belegt"-Liste **formbasiert**:
das Lemma kann über eine andere Form längst im Bestand stehen. Sieben Agenten
sind darauf hereingefallen, bis der Hinweis im Prompt stand. Beides gehört in
jeden Prompt, der `hints.py` benutzt.

**`konsistenz.py` schließt die Lücke von `crosscheck.py`.** Das prüft nur zwei
Hälften **eines** Kapitels; `konsistenz.py` prüft ein ganzes Buch — Abschnitt A
findet Lemmata mit zwei Lesarten innerhalb des Buches, Abschnitt B Abweichungen
von der Korpusmehrheit. Numerus, Genus und vorangestellte Kasuspräpositionen
werden zusammengefasst, sonst besteht der Bericht nur aus Singular/Plural-Paaren.
Abschnitt B ist auf Substantive und auf Bestandslesarten mit mindestens drei
Belegen beschränkt: bei Verben und Adjektiven überwiegen Person-, Numerus- und
Tempusvarianten so stark, dass die echten Fälle im Rauschen verschwinden.

Es hat in jedem Buch etwas gefunden, das kein Agent hätte sehen können, weil
es zwischen Kapiteln liegt: `Mensch` in 1Tim 4,2 mit der Ausweichglosse aus
1,10, obwohl das kollidierende `Mann` in dem Vers gar nicht steht · `erkennen`
in 1Joh 3 mit der `kennen`-Glosse, während der Rest des Buchs sie meidet ·
`Plan` und `Fundament`, die zwischen Epheser, 2. Timotheus und Hebräer
auseinandergelaufen waren.

**`fixgloss.py` und `remap.py` machen korpusweite Korrekturen durchführbar.**
Beide schreiben immer in **beides** — die gebaute Anno-Datei und die
`out/`-Kapitelquelle. Ohne das ist jede Korrektur beim nächsten Build wieder
weg; das war vorher Handarbeit und die häufigste Fehlerquelle beim Nachziehen.
`remap.py` ersetzt feldweise nur exakte Werte und lässt Singular und Plural
dadurch getrennt.

`lexicon.py` und `selfcheck.py` sind entstanden, weil sonst jeder Agent beides
selbst erfindet — der Extrakt wurde mal vollständig gebaut (siehe Fehlerfälle),
mal falsch gefiltert. Zentral gelöst ist es ein Aufruf im Prompt. `lexicon.py`
zieht aus **allen** vorhandenen Anno-Dateien, aufsteigend nach Buchnummer, und
nimmt neue Bücher von selbst auf.

`crosscheck.py` prüft, was bei einem in Hälften geteilten Kapitel
auseinanderlaufen kann. Funktionswörter blendet es aus: Artikel, Pronomen und
Präpositionen weichen legitim ständig ab (Genus der Zielsprache, syntaktische
Rolle) und würden die echten Fälle zudecken.

`buildbook.py` nimmt ein Kapitel **nur** auf, wenn es vollständig ist und der
Validator es durchwinkt; unvollständige Stände (laufender Agent) werden mit
Hinweis übersprungen. Danach: Satzzeichen-Einträge verwerfen, Level
vereinheitlichen, buchübergreifend angleichen, kompakt schreiben.

## Qualitätssicherung

Drei Ebenen, weil jede etwas anderes findet:

**1. Struktur-Validator** (`gen_mt1.validate`) — jede Tokenposition genau einmal
annotiert, `form` deckt sich mit dem satzzeichenbefreiten Token, Spannen und
Klammern decken sich mit dem Text, `parts` aufsteigend und nicht zusammenhängend,
keine leeren Werte, keine Klammer-Grammatik-Tags.

**2. Inhaltliche QA** (`qa.py`) — findet, was strukturell unauffällig ist. Eine
um eine Position verrutschte Zuordnung ist strukturell perfekt und inhaltlich
Unsinn. Heuristiken:

- **Eigennamen-Kanarienvogel**: steht bei „Jesus" etwas anderes als
  *Jesus/Jesús/Jésus/Gesù*, ist die Zuordnung verschoben. Vorangestellte
  Kasus-Präpositionen werden abgestreift („des Hauses Israel" → *of Israel*).
  **Zwei bekannte Fehltreffer**, beide richtig annotiert: Apg 28,6 („er sei ein
  Gott" — ein heidnischer Gott) und 2Kor 4,4 („der Gott dieser Welt") tragen im
  Spanischen und Italienischen bewusst *dios*/*dio* klein. Der Kanarienvogel
  erwartet dort die Großschreibung. Über den gesamten NT-Bestand sind das die
  einzigen beiden Treffer.
- **Wiederholungsläufe**: drei oder mehr aufeinanderfolgende Positionen mit
  identischem Wert.
- **Funktionswörter mit langer Glosse**: „der"/„und"/„von" dürfen kein
  mehrwortiges Inhaltswort bekommen. Positivliste für echte periphrastische
  Entsprechungen (frz. Spaltsatz-Verneinung, agentivisches „von").
- **Platzhalter und Klammer-Tags**: `-`, leer, `(futuro)`.
- **Fremdsprachige Zeichen**: ein französisches `à` im spanischen Feld, ein `ñ`
  im französischen. Zweimal ist einem Agenten eine Glosse in der falschen
  Sprachspalte gelandet (Joh 8,26 und 13,37) — strukturell unauffällig,
  inhaltlich falsch. Die Prüfung vergleicht gegen den Zeichenvorrat der
  jeweiligen Sprache; der ganze Bestand ist darunter sauber, einziger legitimer
  Treffer war das englische Lehnwort *fiancée* (Positivliste).
- **Mehrwort-Lemma in finiter Form**: `ließen gehen` statt `gehen lassen`.
  Die Spezifikation verlangt den Infinitiv; ein Agent hat es in
  Apostelgeschichte 4 dreimal übersehen, ein nachfolgender es gemeldet. Sonst
  war der Bestand sauber. `form` bleibt davon unberührt — die ist der Text.

**3. Gegenrechnung pro Buch** — Tokens im Quelltext gegen Einzelwort-Einträge;
die Differenz muss exakt der Zahl der alleinstehenden Satzzeichen entsprechen.
Matthäus: 21 699 − 21 687 = 12. Markus: 13 461 − 13 455 = 6. Lukas:
23 423 − 23 422 = 1 (der Gedankenstrich in 6,9). Johannes: 18 109 − 18 099 = 10.
Apostelgeschichte: 21 396 − 21 396 = 0 — sie enthält als einziges Buch kein
alleinstehendes Satzzeichen. Offenbarung: 10 360 − 10 349 = 11. Alle sechs
stimmen.

**4. Abschnittsgrenzen** (`crosscheck.py`) — nur bei Kapiteln, die zwei Agenten
in Hälften bearbeitet haben. Es findet keine Fehler, sondern Divergenzen, die
man ansehen muss: In Lukas waren es zwischen 2 und 32 Inhaltswörter je Kapitel,
durchweg berechtigte Kontextvarianten (`hören` als *hear* vs. *listen*, `redete`
punktuell vs. durativ). Kein einziger Fall war eine verrutschte Zuordnung.

### Kollisionen: der Hauptfehlertyp der Offenbarung

In den Evangelien war der typische Fehler die **verrutschte Zuordnung**. In der
Offenbarung war es etwas anderes: **zwei verschiedene deutsche Wörter, die
dieselbe Glosse bekommen** und im Lesefluss ununterscheidbar werden. Das Buch
häuft Synonyme in Doxologien, Viererformeln und Ständelisten, während der
Bestand aus den Evangelien sie oft gleich übersetzt.

Vierzehn Fälle sind aufgetreten. Sie zerfallen in zwei Klassen:

**Die Kollision entsteht durch das neue Buch** — dann wird sie dort aufgelöst:

| Paar | Grund | Auflösung |
|---|---|---|
| `Schale` ↔ `Kelch` | Schale war *platter* (Mt 23), wird als Zornschale *copa/coupe* | Kelch → *cáliz/calice* |
| `Herrschaft` ↔ `Reich` | beide it *regno* | Herrschaft → *dominio* |
| `Unterwelt` ↔ `Totenreich` | die Offenbarung hat **drei** Wörter für den Hades (dazu `Hölle` 1,18) | Unterwelt → *underworld/inframundo* |
| `siegen` ↔ `überwinden` | beide *vencer/vaincre/vincere* | siegen → *triumph/triunfar* |
| `Völker` ↔ `Nationen` | Bestandsmehrheit gab beiden *nations* | Völker → *peoples/pueblos* |
| `Plage` ↔ `Geschwür` | beide it *piaghe* | Geschwür → *ulcere* |
| `Mühle` ↔ `Mühlstein` | beide fr *meule*, in 18,21 f. nacheinander | Mühle → *moulin* |

**Die Kollision steckt schon im Bestand** — dann wird sie korpusweit korrigiert,
inklusive der Kapitelquellen im Scratchpad:

| Paar | Befund | Auflösung |
|---|---|---|
| `Ehre` ↔ `Herrlichkeit` | beide *glory*; fünf NT-Verse stellen sie nebeneinander (Röm 2,7 · 2,10 · 1Petr 1,7 · 2Petr 1,17 · Offb 21,26) | Ehre → *honor/honra/honneur/onore*, 50 Einträge in vier Büchern |
| `Becher` ↔ `Kelch` ↔ `Schale` | Becher war 5:3 gespalten | Becher → *goblet/vaso/gobelet/bicchiere* |

Der `Ehre`-Fall ist der lehrreichste. In der Offenbarung hatte ich ihn mit der
Bestandsmehrheit 14:1 **falsch** entschieden — die Mehrheit stammt aus den
Evangelien, wo `Herrlichkeit` selten danebensteht. Erst die Vorbereitung der
Briefe hat es aufgedeckt. **Eine Bestandsmehrheit ist nur dann ein Argument,
wenn die Belege aus vergleichbaren Kontexten stammen.**

Nicht aufgelöst wurden Paare, die **nirgends im NT im selben Vers stehen**:
`Gericht` ↔ `Urteil` (null Verse), `Knecht` ↔ `Diener` (im Französischen beide
*serviteur*, aber korpusweit so und nie zusammen). Eine buchlokale Sonderlösung
hätte das Buch gegen die anderen inkonsistent gemacht.

**Für die Briefe ist der Test vorgezogen worden**: statt die Kollisionen
einzusammeln, habe ich für 30 Synonymgruppen ausgezählt, welche Wörter in den
21 Briefen tatsächlich im selben Vers vorkommen. Ergebnis: 34 Paare mit
Belegstelle, alle vorab aufgelöst in `BINDUNGEN_BRIEFE.md`. Die aufwendigsten
sind `Kraft`/`Macht`/`Stärke` (Kol 1,11 · Eph 1,19 · 2Petr 2,11) und
`Weisheit`/`Erkenntnis`/`Einsicht`/`Verstand`/`Klugheit` (Röm 11,33 · Kol 1,9 ·
1Kor 1,19).

### Prompt-Hinweise sind Hypothesen, keine Vorgaben

In der Offenbarung lagen meine Hinweise **über dreißigmal** daneben, weil sie
aus der Bibelkenntnis stammen und nicht aus dem modernisierten Text: der
l1912mod kennt kein `Malzeichen` (überall `Zeichen`), keine `Sichel` in 14,17 ff.
(`Winzermesser`), kein `Büchlein` (`Schriftrolle`), keinen `Ankläger` (`Verkläger`),
keinen `Adler` in 8,13 (`Engel`), kein `Sardis` unter den Edelsteinen (`Karneol`);
die Warenliste in 18,12 f. wich zur Hälfte ab, und 11,9 und 13,7 haben nur drei
statt vier Gliedern. Jeder dieser Fälle wurde von einem Agenten gemeldet, nicht
von mir gefunden. Der Satz **„Der Quelltext hat immer recht"** gehört deshalb in
jeden Prompt, zusammen mit der Aufforderung, Abweichungen zu melden statt ihnen
zu folgen.

Bei den Büchern 52–65 ist das trotz `hints.py` weitergegangen — das Werkzeug
findet unbelegte Wortformen, aber nicht, ob eine Perikope so heißt, wie ich sie
im Prompt beschreibe. Ein Dutzend Fälle, alle von Agenten gemeldet:
2Petr 1,5 ff. hat `Geduld` und `Gottesfurcht`, nicht „Ausdauer" und
„Frömmigkeit" · 1Joh 2,16 sagt `Lust`, nicht „Begierde" (womit die von mir
befürchtete Kollision gar nicht entsteht) · Jak 3,17 hat **fünf** Tugenden,
nicht vier · 1Thess 4 kennt weder `Unzucht` noch `Gefäß` noch `entrückt`,
sondern `sexuelle Unmoral`, `Körper`, `emporgehoben` · 2Tim 4,2 hat den
Imperativ `Predige`, kein Substantiv `Predigt` · Hebr 12,24 sagt `Mittler`,
nicht `Vermittler`, und hat keine „Festversammlung" · 3Joh 9 enthält nur zwei
der fünf Diotrephes-Vorwürfe, die übrigen stehen in V10 · 2Petr 2,16 hat ein
`Lasttier`, keine „Eselin" · Phlm 11 spielt `unnütz` gegen `Nutzen` aus, nicht
gegen „nützlich".

Zwei davon waren keine Bibelkenntnis-Fehler, sondern **Fehler meines eigenen
Werkzeugs**: die Präfix-Kollisionsprüfung erfand `Heil ↔ Rettung` in 2Thess 2,13
und `Erlösung ↔ Heil` in Hebr 9,12, weil `Heil` in `Heiligung` und `Heiligtum`
anschlägt. Beide Male hat ein Agent am Vers nachgesehen und widersprochen. Die
Lehre bleibt dieselbe und gilt auch für automatisch erzeugte Hinweise: **ein
Prompt-Hinweis ist eine Hypothese, auch wenn ein Skript ihn erzeugt hat.**

### Listen sind die riskanteste Stelle

Aufzählungen gleicher Bauart — zwölf Stämme (7,5–8), dreißig Waren (18,12 f.),
zwölf Edelsteine (21,19 f.) — sind der wahrscheinlichste Ort für eine um eine
Position verrutschte Zuordnung, und strukturell fällt das nicht auf. Bewährt
hat sich, was drei Agenten unabhängig entwickelt haben: ein **eigenes
Prüfskript mit neu getippter Erwartungsliste**, das die Position jedes
Listenglieds aus dem Quelltext ableitet und den Eintrag dort dagegenhält. In
allen drei Fällen null Abweichungen.

Dasselbe Verfahren trägt auch **zwischen zwei parallel bearbeiteten Kapiteln**,
wenn sie ein gemeinsames Sachfeld haben. Apostelgeschichte 27 und 28 teilen das
Seefahrtsvokabular; der Vergleich der geteilten Inhaltswörter ergab 42
Divergenzen, davon 39 legitime Kontextvarianten (Person, Numerus, Tempus,
`heftig` als Sturm vs. als Streitgespräch) und drei echte Angleichungen. Die
Funktionswörter müssen dabei ausgeblendet bleiben, sonst verschwinden die drei
Fälle im Rauschen.

Wirksamer als die Nachkontrolle ist die Vorsorge: Seit Johannes 4 liefert jeder
Agent einer geteilten Bearbeitung eine **Wortfeld-Liste der Schnittstelle** mit
— die Begriffe, die über die Grenze laufen, samt gewählter Glosse und Level.
Das steht so im Prompt. Ein Agent hat von sich aus dazugeschrieben, dass Joh
12,23 „Zeit" und 12,27 „Stunde" sagt und beides **nicht** angeglichen werden
darf; genau die Art Fehler, die eine geteilte Bearbeitung sonst erzeugt.

Wo eine Festlegung über Kapitelgrenzen hinweg gilt, gehört sie in den nächsten
Prompt: Kapitel 14 hat `Tröster` bestimmt, die Kapitel 15 und 16 haben es
wörtlich übernommen — die Abschiedsreden sind dadurch durchgehend einheitlich.

**5. Vollständigkeit gegen den Quelltext** — beim Abschluss eines Buches
zusätzlich prüfen, dass jedes Kapitel und jeder Vers des Quelltextes in der
Anno-Datei steht. Der Validator prüft nur, was da ist; ein komplett fehlendes
Kapitel fällt ihm nicht auf.

### Level-Abgleich

Das CEFR-Level gehört laut Spezifikation zum **Lemma**. Verschiedene Agenten
stufen dasselbe Wort aber unabhängig ein. Der Build vereinheitlicht deshalb in
mehreren Durchgängen (gleiche Bedeutung → gleiches Level; gleiches Lemma →
gleiches Level; gleiche Wortform → gleiches Level) und gleicht anschließend
**buchübergreifend** über alle Anno-Dateien ab: häufigstes Level gewinnt, bei
Gleichstand das niedrigere. Matthäus liefert die meisten Belege und ist damit
faktisch der Maßstab, ohne dass er dazu erklärt werden muss.

Das gehört in den Build und nicht dahinter — die Datei entsteht bei jedem Build
neu aus den Kapitel-JSONs, eine nachträgliche Korrektur wäre sofort wieder weg.

## Arbeitsweise mit Subagenten

Ein Agent pro Kapitel, **3–4 gleichzeitig**. Jeder Agent:

1. liest `SPEC.md`
2. baut sich ein **gefiltertes** Lexikon: erst die Wortformen des eigenen
   Kapitels bestimmen, dann nur zu diesen die Einträge aus den fertigen
   Anno-Dateien sammeln
3. arbeitet in Abschnitten von 8–10 Versen und schreibt nach jedem Abschnitt
   eine Teildatei weg
4. prüft sich mit eigenem Skript, oft zusätzlich mit `qa.py`
5. liefert nach `out/<buchNr>/ch<N>.json`

Verbindliche Auflagen in jedem Prompt:

- **Nie ins Repository schreiben**, nur lesen
- **Keine eigenen Subagenten** — sonst vervielfacht sich die Parallelität unsichtbar
- **Übersetzungen direkt am Eintrags-Dict zuweisen**, nie eine separate Liste
  bauen und hinterher per Index zusammenführen (dabei verrutschen Zuordnungen
  unbemerkt um eine Position)
- Eigener Arbeitsordner je Agent (sonst überschreiben sie sich gegenseitig)

Danach validiere ich jedes Kapitel **unabhängig** gegen den Quelltext, baue,
lasse QA laufen und committe. Die Selbstauskunft eines Agenten reicht nie —
zweimal war ein als „fertig" gemeldeter Stand in Wahrheit ein Zwischenstand,
den nur die Vollständigkeitsprüfung gegen den Quelltext aufgedeckt hat.

### Nachrücken statt in Blöcken arbeiten

Bei den Büchern 52–65 hat sich bewährt, die Parallelität **konstant** zu halten:
sobald ein Agent fertig ist, startet sofort der nächste, statt auf einen ganzen
Viererblock zu warten. Das kostet nichts und spart bei 51 Kapiteln viel
Leerlauf, weil ein 40-Verse-Kapitel dreimal so lange braucht wie ein
14-Verse-Kapitel.

Wichtiger ist der Nebeneffekt: der nächste Agent bekommt die Festlegungen
seines Vorgängers als **fertige Kapiteldatei** in den Prompt, nicht nur die
Wortfeld-Liste. Die Reihenfolge ist deshalb kein Detail — ein Buch beginnt mit
seinem Kapitel 1 („dein Kapitel ist der Maßstab für dieses Buch"), und dessen
Ergebnis wandert wörtlich in die folgenden Prompts.

Der Bestand wächst dabei sichtbar mit: die Lexikon-Abdeckung lag bei den ersten
Kapiteln der Thessalonicherbriefe schon bei 92–99 % statt der 53 %, die für die
Briefe vorhergesagt waren — weil Römer bis Kolosser inzwischen im Lexikon
stehen.

### Wenn ein Agent mitten im Kapitel stirbt

Vier gleichzeitig laufende Agenten sind an einem Wochen-Nutzungslimit
abgebrochen. Das abschnittsweise Wegschreiben hat genau das getan, wofür es da
ist: ein Kapitel war bereits vollständig, von einem zweiten waren elf von
22 Versen gerettet. Beides ging nach `anno/_wip/`; ein frischer Agent hat das
Fragment als **Vorlage** gelesen (Terminologie, Level und Namensformen des
Kapitels standen darin schon fest) und nur die fehlenden Verse ergänzt.

Die Lehre ist nicht neu, aber sie ist erstmals unter Last geprüft: **das
Wegschreiben nach jedem Abschnitt ist der einzige Schutz**, und `_wip/` ist der
Ort, an dem ein Fragment auf seinen Nachfolger wartet. Wer den Nachfolger
ansetzt, muss ihm die Fragmentdatei ausdrücklich zu lesen geben und die
Selbstprüfung über das **ganze** Kapitel verlangen, nicht nur über die
Ergänzung.

### Anschluss an den Bestand

Matthäus ist der Maßstab fürs ganze NT. Ein Markus-Agent zieht sein Lexikon aus
Matthäus, nicht aus dem eigenen Buch — sonst bekäme dieselbe Perikope in zwei
Evangelien verschiedene Glossen. Die Abdeckung lag über alle Markus-Kapitel
zwischen 91 % und 98 %, in Lukas zwischen 75 % (Kapitel 3 mit dem Stammbaum)
und 92 %, im ersten Johannes-Kapitel bei 90 %.

Jedem Agenten gehört im Prompt gesagt, **welche Parallelstellen** sein Kapitel
hat („Lukas 20 ist parallel zu Markus 12 und Matthäus 22"). Das Lexikon liefert
nur Wortformen; welche Perikope schon einmal übersetzt wurde, sieht ein Agent
daran nicht. Mit dem Hinweis übernehmen die Agenten ganze Verse wörtlich, ohne
ihn erfinden sie neben dem Bestand her.

Entscheidend ist die Grenze: **Die Vorgabe gilt für dieselbe Bedeutung, nicht
für dieselbe Buchstabenfolge.** Beispiele, die Agenten korrekt abweichend
gelöst haben:

| Wort | Bestand | abweichender Kontext |
|---|---|---|
| `Ofen` | Backofen (Mt 6,30) | Feuerofen (Mt 13,42) |
| `Himmel` | *heaven* | Wetterhimmel *sky* (Mt 16,2) |
| `Herde` | Schweineherde (Mt 8) | Schafherde (Mk 14,27) |
| `vergeben` | *forgive* | *zuteilen* (Mt 20,23) |
| `Arme` | Adjektiv *poor* | Körperteil *arm* (Mk 10,16) |
| `Gadarener` | Mt hat „Gergesener" | anderer Name im Markus-Text |
| `Leib` | *body* | Mutterleib *womb* (Lk 1,41) |
| `erließ` | Schulderlass *canceled* | eine Anordnung erlassen *issued* (Lk 2,1) |
| `Geist` | *spirit* | Gespenst *ghost* (Lk 24,37) |
| `Kraft` | *power* | Körperkraft *strength* (Lk 10,27) |
| `sieben` | Zahlwort *seven* | Verb *sift* (Lk 22,31) |
| `Flut` | Überschwemmung | Sintflut *deluge* (Lk 17,27) |
| `Acht` | *in Acht nehmen* | Zahlwort *eight* (Joh 20,26) |
| `weiß` | Form von *wissen* | Farbe *white* (Joh 20,12) |
| `Weide` | Substantiv *pasture* (Joh 10,9) | Imperativ von *weiden* (Joh 21,15) |

### Dasselbe Wort an zwei Stellen desselben Kapitels

Der Bestandsabgleich hilft nicht, wenn dieselbe Buchstabenfolge **innerhalb**
eines Kapitels verschieden zu lesen ist. Johannes 18 hat das zweimal: `Ich bin
es` (18,5, Selbstbezeichnung Jesu) bekommt `es` → *he/él/lui/lui* wie in
Johannes 8, Petrus' Verleugnung `Ich bin es nicht` (18,17) dagegen *it/lo/le/lo*.
Solche Fälle findet nur die Handstichprobe.

### Anderes deutsches Wort, gleiche Perikope

**Die App glossiert das deutsche Wort, nicht die Perikope.** Wo Johannes einen
anderen Ausdruck wählt als die Synoptiker, bekommt er die Glossen der
bedeutungsgleichen Bestandsstelle, aber ein **eigenes Lemma**:

| Johannes | Synoptiker |
|---|---|
| `Palast` (18,28) | `Amtsgebäude` (Mt 27,27), `Amtssitz` (Mk 15,16) |
| `Brauch` (18,39) | `Gewohnheit` (Mt 27,15) |
| `stritt ab` (18,25) | `verleugnen` |
| `Mörder` (18,40) | `Räuber` |
| `Tröster` (14,16) | — (kein synoptisches Gegenstück) |
| `Herrscher dieser Welt` (14,30) | `Fürst` wäre die geläufige Wendung |

Die letzten beiden sind lehrreich: Ich hatte einem Agenten „Beistand" und
„Fürst dieser Welt" in den Prompt geschrieben — beides steht nicht im Text. Er
hat es geprüft, korrigiert und gemeldet. **Perikopen-Hinweise im Prompt sind
Hilfen, keine Vorgaben; der Quelltext hat immer recht.**

### Uneinheitlichkeiten im Bestand

Mehrfach hat ein Agent nicht bei sich, sondern **im Bestand** etwas gefunden,
das zweigleisig lief. Alles ist korpusweit korrigiert worden:

| Wort | Befund | Auflösung |
|---|---|---|
| `Bund` | Lk 1,72 es *alianza*, Mt 26,28 und Mk 14,24 *pacto* | auf Matthäus vereinheitlicht |
| `Schuhe` | Mt 3,11 und Mk 1,7 fr *souliers* / it *calzari*, vier andere Stellen *sandales* / *sandali* | auf die Mehrheitsform (4:2) vereinheitlicht |
| `Schiff` | Apg 20,13 und 20,38 fr *bateau*, vier andere Stellen *navire* | auf die Mehrheitsform vereinheitlicht |
| `Gefangener` | Lk 21,24 es *prisioneros*, elf andere Stellen *preso/presos* | auf die Mehrheitsform (11:1) vereinheitlicht |

Beim `Schuhe`-Fall waren auch die **Kapitelquellen im Scratchpad** zu ändern,
nicht nur die gebauten Dateien — sonst wäre die Korrektur beim nächsten Neubau
von Matthäus und Markus wieder verschwunden. Das gilt für jede solche Korrektur.

Der `Gefangener`-Fall ist zusätzlich lehrreich, weil ich ihn selbst ausgelöst
habe: Ich hatte die Bindung für den Prompt aus der Form `Gefangene` gezogen —
einem einzigen Beleg, der die Ausnahme war — statt aus dem Lemma über alle
Formen. Eine Bindung für einen Prompt gehört über das **Lemma** ausgezählt,
sonst schreibt man einen Ausreißer fort.

## Gelernte Fehlerfälle

**Gedankenstrich als eigenes Token.** Die Spezifikation verlangte einen Eintrag
für jede Position und verbot `-` als Wert. Zwei Agenten lösten das unabhängig
mit „dash/guion/tiret/trattino". Zentral gelöst (Build verwirft solche
Einträge), nicht per Prompt — dann ist es egal, wie ein einzelner Agent
entscheidet.

**Lexikon-Extrakt wächst mit dem Bestand.** Bei 37 000 Einträgen wird ein
vollständiger Extrakt ~1 MB und bringt den Agentenlauf zum Stillstand. Deshalb
zwingend gefiltert bauen. Das Problem wäre mit jedem fertigen Buch schlimmer
geworden.

**Verbindungsabbrüche.** Kommen vor, teils in Serie. Gegenmittel:
Abschnittsweise arbeiten mit sofortigem Wegschreiben — bei einem Ausfall in
Lukas 1 waren dadurch 30 von 80 Versen gerettet. Ein Agent wird höchstens
**einmal** fortgesetzt; jede Fortsetzung verlängert sein Transkript und erhöht
die Ausfallwahrscheinlichkeit. Danach übernimmt ein frischer Agent die
Restverse und liest die fertigen Teildateien als Vorlage.

**Kapitel über ~55 Verse** gehen von vornherein an zwei Agenten mit halber
Verszahl, nicht erst nach einem Abbruch.

**Ziffern als Token.** Johannes 2,20 („46 Jahre") enthält das einzige
Ziffern-Token im bisher bearbeiteten Text. Es bekommt einen regulären Eintrag
mit „46" in allen vier Sprachen — anders als der Gedankenstrich, der
übersprungen wird: eine Zahl ist Inhalt, kein Satzzeichen, und ausgeschriebene
Zahlwörter (`vierzehn` → *fourteen*) werden ebenfalls glossiert.

**Commit-Nachrichten gegen die Build-Ausgabe prüfen.** Dreimal habe ich den
Inhalt zu niedrig angegeben, weil beim Bauen bereits ein weiteres fertiges
Kapitel vorlag, dessen Agent sich noch nicht gemeldet hatte. Inhaltlich war nie
etwas falsch, aber die Beschreibung hinkte hinterher. In Lukas ist es zweimal
anders passiert: Zahl in die Commit-Nachricht geschrieben, **bevor** das
Zählskript gelaufen war. Erst rechnen, dann schreiben — sonst steht eine
erfundene Zahl im Log.

**Das Prüfskript kann selbst falsch liegen.** `qa.py` hat bei Lukas 16,15
angeschlagen („das ist Gott ein Gräuel", fr *pour Dieu*). Die Glosse war als
Dativ richtig; die Präfix-Liste des Eigennamen-Kanarienvogels kannte nur `à/au/
de`, nicht `pour`, während en `to`, es `para` und it `per` längst drin waren.
Bei einem Treffer also erst die Stelle ansehen, dann entscheiden, wer den
Fehler hat.

## Commit-Schema

Ein Commit je validiertem Kapitel oder Kapitelpaar, ausschließlich auf `dev`,
**nicht gepusht** — Push und Merge nach `main` macht `deploy.sh` und wäre ein
Deployment. Committet wird nur, was der Validator durchgewunken hat.

## Neues Buch anfangen

Es ist **kein Eingriff in `index.html` nötig**. Die App lädt Anno-Dateien per
Buchnummer (`index.html:2555`) und behandelt eine fehlende Datei als „keine
Glossen"; ein neues Buch erscheint, sobald seine Datei da ist. `lexicon.py`
zieht ebenfalls über alle vorhandenen Anno-Dateien und nimmt neue von selbst
auf.

## Kapitelquellen

Die gebauten `<buchNr>_l1912mod_multi.json` entstehen bei jedem Build aus
Kapiteldateien, die **nicht in diesem Repository** liegen, sondern in
`../bibles-translations/anno-quellen/deu/l1912mod/<buchNr>/ch<N>.json`
(Bücher 42–66, rund 20 MB, siehe den README dort).

Sie liegen dort und nicht hier, weil `sync_www.sh` das ganze
`bibles/`-Verzeichnis ins iOS-Bundle spiegelt — hier wären sie toter
Ballast, den die App nie lädt. `buildbook.py` liest sie direkt von dort;
kopiert werden muss nichts mehr.

**Alle Bücher sind wieder baubar, auch Matthäus und Markus.** Sie galten als
eingefroren, weil ihre Quellen mit dem Scratchpad verschwunden waren — dasselbe
war unbemerkt mit **2. Mose 30–40** passiert. Die gebaute Anno-Datei enthält
aber alles, was die Quelle enthält: `quellen_sync.py` rechnet sie zurück.
Verloren geht dabei nur, was der Build ohnehin verwirft (Satzzeichen-Einträge)
oder überschreibt (Level). Seither entstehen alle 29 Bücher byte-identisch neu.

**Nach jedem fertigen Kapitel die Quelle mitcommitten.** Der Verlust ist genau
dadurch entstanden, dass zwischen Agentenlauf und Commit ein Schritt fehlte.

## Offen

- Kein Vokabeltraining für Deutsch: dafür bräuchte es `words.json` +
  `examples.json` analog zur ES-Pipeline (`build_training.py` → Opus-Enrichment
  → `finalize_training.py`) und `build_keepnames.py` für die Eigennamen-Liste
- `hasTraining`/`hasLevelTest` bleiben bis dahin `false`
