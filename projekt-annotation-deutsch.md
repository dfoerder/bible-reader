# Deutsche Annotation (l1912mod → en/es/fr/it)

Wort-für-Wort-Annotation der deutschen Bibel mit Übersetzungen nach Englisch,
Spanisch, Französisch und Italienisch. Begonnen 25.07.2026, **das Neue
Testament (Bücher 40–66) ist seit 28.07.2026 vollständig**, **Jesaja seit
03.09.2026**. Stand: **50 von 66 Büchern**, 1005 Kapitel, 26 973 Verse,
588 313 Einträge — es fehlen die Bücher 24–39.

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

**1. Chronik am 19.08.2026** (29 Kapitel, 942 Verse, 17 062 Einträge) — das
erste Buch der Chronik-Gruppe und das bisher schwierigste, weil fast jedes
Kapitel eine schon annotierte Parallele in Genesis, Samuel, den Königsbüchern
oder Josua hat, und zwar mit **verschobenen Blockpositionen** (gemessene
Versätze von −49 bis +34).

**Esra ist am 24.08.2026 fertig geworden** — 10 Kapitel, 280 Verse,
5997 Einträge, in vier Wellen zu je drei gleichzeitig laufenden Kapiteln
(zuletzt eines allein). Die Vollständigkeitsprobe über alle **5833 Tokens**
gegen den Quelltext läuft ohne Befund durch; die 16 Satzzeichen-Tokens stimmen
auf den Token genau.

**2. Chronik ist am 24.08.2026 fertig geworden** — 36 Kapitel, 822 Verse,
22 607 Einträge, in zwölf Wellen zu je drei gleichzeitig laufenden Kapiteln.
Die Vollständigkeitsprobe über alle **21 786 Tokens** gegen den Quelltext
läuft ohne Befund durch; die 44 Satzzeichen-Tokens stimmen auf den Token
genau.

**Ester ist am 27.08.2026 fertig geworden** — 10 Kapitel, 167 Verse,
5041 Einträge, in drei Wellen. Die Vollständigkeitsprobe über alle **4864
Tokens** gegen den Quelltext läuft ohne Befund durch; die 10 Satzzeichen-Tokens
stimmen auf den Token genau. Das Buch steht praktisch allein: `parallelen.py`
findet über 69 gescannte Verse sieben Treffer ab fünf Tokens, alle bei
Ähnlichkeit 0,21 bis 0,47 — wiederkehrende Wendungen, keine Parallelstellen.

**Nehemia ist am 25.08.2026 fertig geworden** — 13 Kapitel, 406 Verse,
8758 Einträge, in fünf Wellen zu je drei gleichzeitig laufenden Kapiteln
(Kapitel 7 auf zwei Agenten geteilt). Die Vollständigkeitsprobe über alle
**8503 Tokens** gegen den Quelltext läuft ohne Befund durch; die 20
Satzzeichen-Tokens stimmen auf den Token genau.

**Hiob ist am 29.08.2026 fertig geworden** — 42 Kapitel, 1070 Verse,
16 617 Einträge, 782 Mehrwort-Einträge. Das erste Buch der Poesie und mit
Abstand das schwierigste bisher: `parallelen.py` findet für die meisten
Kapitel **null** Verse mit einem gemeinsamen Block ab fünf Tokens im gesamten
übrigen Bestand. Es gab keine Vorlagen; alles kam aus dem Lexikon-Extrakt und
aus der buchinternen Konsistenz. Was es gelehrt hat, steht unten im eigenen
Abschnitt.

**Der Psalter ist am 29.08.2026 fertig geworden** — 150 Kapitel, 2528 Verse,
39 098 Einträge, 1756 Mehrwort-Einträge. Das grösste Einzelbuch des Bestands
und mit Abstand das aufwendigste: 68 Pakete, jedes von einem eigenen Agenten.
Psalm 119 (176 Verse) musste auf zwei Agenten geteilt werden.

Damit waren **46 von 66 Büchern fertig**: 888 Kapitel, 24 428 Verse,
534 181 Einträge.

`mehrwort.py alle` meldet 17 Fälle, davon 2 aus Hiob (40,23 `Ufer`) — beide
sind der vom Werkzeug selbst beschriebene richtige Fall: das deutsche Wort
steht im Plural, die Wendung enthält es im selben Numerus.

**`hilfsverb.py` ist mit Hiob umgebaut worden** und meldet die
`werden`-Treffer jetzt getrennt als erwartete Bauform. Der Grund steht unten
unter „Der Konjunktiv II"; die 35 Altfälle aus `BEFUNDE_NEHEMIA.md` sind davon
teilweise erfasst.

**Die Sprüche sind am 30.08.2026 fertig geworden** — 31 Kapitel, 915 Verse,
14 019 Einträge, in elf Paketen (Kapitel 1 allein als Maßstab, danach
Dreierwellen). Die unabhängige Vollständigkeitsprobe über alle **13 380 Tokens**
läuft ohne Befund durch: jede Tokenposition trägt genau einen Eintrag, jede
`form` stimmt mit dem Quelltext überein, und die 20 alleinstehenden Satzzeichen
gehen auf den Token genau auf.

**Der Prediger ist am 30.08.2026 fertig geworden** — 12 Kapitel, 222 Verse,
5217 Einträge, in fünf Paketen. Die unabhängige Vollständigkeitsprobe über alle
**4991 Tokens** läuft ohne Befund durch.

**Das Hohelied ist am 30.08.2026 fertig geworden** — 8 Kapitel, 117 Verse,
2407 Einträge, in vier Paketen. Die unabhängige Vollständigkeitsprobe über alle
**2351 Tokens** läuft ohne Befund durch. Das Buch hat die höchste
Dublettendichte des Bestands (sieben Verspaare auf 117 Verse, drei davon
wörtlich gleich), deshalb folgte die Paketreihenfolge den Dubletten statt der
Kapitelzahl: 1 / 2+4+5 / 3+6+7 / 8.

**Jesaja (23) ist am 03.09.2026 fertig geworden** — 66 Kapitel, 1291 Verse,
32 487 Einträge, in 24 Paketen. Das größte Buch nach dem Psalter und das mit
der dichtesten Vorlagendecke: 21 Kapitel haben einen gemessenen Block von
mindestens fünf Tokens in einem anderen Kapitel desselben Buches. Die
unabhängige Vollständigkeitsprobe über alle **31 193 Tokens** läuft ohne
Befund durch; die 147 Satzzeichen-Tokens stimmen auf den Token genau.
`validate.py 23`, `qa.py 23` und `hilfsverb.py 23` melden nichts.

Damit sind **52 von 66 Büchern** annotiert. Es fehlen die Bücher 26–39.

**Jeremia (24) ist seit 03.09.2026 in Arbeit** — 52 Kapitel, 1364 Verse,
18 Pakete nach `PAKETE_JEREMIA.txt`. Das Buch unterscheidet sich von Jesaja
durch seine **261 buchinternen Dublettenpaare** (Jesaja hatte rund fünf): der
größte Teil sind Botenformeln, und deshalb steht am Anfang keine
Maßstabsentscheidung an einem Kapitel, sondern eine **Formelentscheidung**.
Dafür ist `vorbereitung.py` entstanden — es baut die Vorbereitungsdatei jedes
Pakets maschinell und teilt die Dubletten in die drei Richtungen auf, die
etwas völlig Verschiedenes bedeuten (Vorlage in einem fertigen Kapitel · beide
Verse im selben Paket · der eigene Vers ist die Vorlage für später).

Die Verszählung weicht in genau zwei Kapiteln ab, dieselbe Bauform wie
Jesaja 8/9: de 8,23 = deren 9,1, ab 9 dann Versatz +1. Deshalb liegen 8 und 9
im selben Paket.

**Jeremia ist vollständig (04.09.2026): 52 von 52 Kapiteln, 1364 Verse,
36 972 Einträge, 3123 verschiedene Lemmata, 1452 Mehrwörter.** `validate.py`
rechnet die 35 638 Tokens der Paketplanung Zeichen für Zeichen nach — 35 520
Einzeleinträge plus 118 alleinstehende Satzzeichen, 0 Befunde. Alle Pflicht-
läufe über das fertige Buch sind sauber; von den 16 verbliebenen Kollisions-
paaren sind fünfzehn echte Verschmelzungen der Zielsprachen (romanisch deckt
`tun` und `machen` mit einem Verb ab, *pecado*/*péché*/*peccato* sind zugleich
Substantiv und Partizip), das sechzehnte ist aufgelöst.

**Ein Befund für jedes weitere Buch:** der l1912mod modernisiert Eigennamen in
Jeremia systematisch anders als in den älteren Büchern. Neun Fälle sind
belegt — `Paschhur`/`Pashur`, `Betlehem`/`Bethlehem`, `Hananel`/`Hananeel`,
`Kaftor`/`Kaphthor`, `Anakiter`/`Enakiter`, `Teman`/`Theman`,
`Ben-Hadad`/`Benhadad`, `Aschkenas`/`Askenas`, `Ewil-Merodach`/`Evil-Merodach`.
Sechs davon haben Agenten gegen den Prompt gefunden. Das gehört künftig in
jede Vorbereitung. Mit 43,8 ist die Botenformel des Buches
vollständig entschieden — in allen drei Fassungen (mit `Da`, ohne `Da`
verb-zweit, und mit Subjekt voran). Kapitel 48 hat sich als **Umarbeitung von
Jesaja 15–16** bestätigt: die seltensten Ortsnamen des Moab-Spruchs haben je
einen einzigen Bestandsbeleg, und der steht jedes Mal in Jesaja 15,5/15,6 oder
16,11. Paket 11 war mit 110 Versen das größte des Buches
und hatte **49 Dubletten mit fertiger Vorlage**; Paket 12 hat die Botenformel
des Buches abgeschlossen — sieben Formelketten, jede Feld für Feld gegen ihre
Vorlage nachgerechnet, null Abweichungen, und `34,12` und `35,12` kamen bei
zwei Agenten **ohne Absprache identisch** zurück. In Paket 12 blieb
`paketcheck.py` Abschnitt A erstmals im Buch **vollständig leer**: jedes neu
geprägte Lemma trug in allen drei Kapiteln dieselbe Reihe.

Beim Einsammeln von Paket 12 ist eine **buchweite Angleichung** fällig
geworden. `mehrwort.py` meldete 13 Verdachtsfälle, zwölf davon `Hand`
französisch *mains* innerhalb der Wendung `in die Hand geben`. Der Bestand
außerhalb Jeremias steht dort **68 : 11 auf *main*** — das deutsche Wort ist
Singular, nur die französische Wendung (*livrer entre les mains*) trägt den
Plural; das Buch war abgedriftet, weil die Prompt-Vorgabe seit Paket 7 den
Plural verlangte. 16 Einträge in acht Kapiteln angeglichen, `mehrwort.py` fällt
von 13 auf 1.

In Paket 13 hat ein Agent **die Vorbereitung an ihrer wichtigsten Stelle
widerlegt**. Ich hatte in den Prompt geschrieben, 2. Könige 25 sei keine
brauchbare Vorlage für Jeremia 39 — gestützt auf eine einzige
Ähnlichkeitszahl für einen einzigen Vers. Der Agent hat das Kapitel trotzdem
aufgeschlagen und **fünf Verse wörtlich** vorgefunden; alle fünf sind
nachgeprüft. Für Paket 18 (Kap. 52) heißt das: 2. Könige 25 zuerst
aufschlagen. Die Lehre für die Vorbereitung ist allgemein — **eine einzelne
Ähnlichkeitszahl aus `parallelen.py` trägt keine Negativaussage**; wo
`PAKETE_JEREMIA.txt` eine fremde Parallele nennt, gehört sie in den Prompt,
auch wenn das Werkzeug schweigt.

In Paket 14 ist diese Lehre umgesetzt worden und hat getragen: 2. Könige 25
stand von Anfang an im Prompt und deckt die ganze Gedalja-Erzählung ab. Das
Paket hat dafür den bisher höchsten Stand an **widerlegten Prompt-Angaben** —
darunter zwei echte Sachfehler von mir (`geritzt` ist über `ritzen` in
Jer 16,6 belegt; bei `Königstöchter` zeigte ich auf die falsche
Bestandsreihe). Umgekehrt hat ein Agent **sieben Vorlagen benutzt, die
`vorbereitung.py` gar nicht meldet**, während vier der gemeldeten reines
Rauschen waren. Beides zusammen ist das belastbarste Argument dafür, die
Berichte der Agenten als Prüfinstanz für die Vorbereitung zu lesen und nicht
umgekehrt.

Paket 15 hat dabei einen **systematischen Fehler in meiner eigenen
Vorbereitung** aufgedeckt: `belegt.py <Wort>` zählt die übergebene
**Wortform**, nicht das Lemma, und ich hatte die Formzahl als Belegzahl in die
Prompts geschrieben (`Steinsäule` 1 statt 6, `Flüchtling` 1 statt 5,
`Truppenführer` 1 statt 8). Eine zu niedrige Belegzahl lädt den Agenten dazu
ein, eine feste Bindung für verhandelbar zu halten. Seither stehen in den
Vorgabetabellen nur noch Zahlen, die über alle Flexionsformen geprüft sind.

In Paket 16 kam ein schwererer Werkzeugbefund dazu: **`levelcheck.py 24` ohne
Kapitelnummer prüft nichts.** Im Quelltext ist `kaps = argv[1:]` dann leer, die
Schleife läuft null Mal, und das Skript meldet unweigerlich „0 Abweichungen" —
genau so stand der Aufruf in der Sammelkette. Der nachgeholte Lauf über alle
48 Kapitel meldet ebenfalls null, es ist also kein Schaden entstanden; der
erste *richtige* Aufruf fand aber sofort einen echten Fall. **Ein Pflichtlauf,
der bei falschem Aufruf still „sauber" meldet, ist schlimmer als keiner.**

Was das wert war, zeigte das nächste Paket: mit korrigiertem Aufruf fand
`levelcheck` in Paket 17 **23 echte Levelfehler** (6 in Kap. 50, 17 in
Kap. 51) — von einem Lauf, der vorher immer „0 Abweichungen" gemeldet hatte.
Ein zweiter Aufruf derselben Bauart kam dazu: `glosskollision.py --datei`
verlangt die Datei als drittes Argument. Der stürzt allerdings laut ab und
kann deshalb nichts verstecken. Paket 7 ist das erste des Buches, in dem
`glosskollision.py` über **alle drei Kapitel null inhaltliche Paare** meldet.

In Paket 8 sind **alle drei Agenten gleichzeitig an einem Serverfehler
(HTTP 529) gestorben**, kurz nach dem Einlesen der Unterlagen. Von Kapitel 23
lagen die Verse 1–8 als Teildatei da und liefen sauber durch; der Nachfolger hat
sie als Vorlage gelesen, den Rest ergänzt und über das **ganze** Kapitel geprüft
— dabei genau einen echten Fehler im übernommenen Teil gefunden. Zweite
Bestätigung dafür, dass das abschnittsweise Wegschreiben der einzige Schutz ist. `validate.py 24`, `qa.py 24`, `hilfsverb.py 24`,
`levelcheck.py` und `mehrwort.py 24` laufen über das gebaute Buch ohne Befund.

Paket 3 hat die **einzige Verszählungsfalle des Buches** enthalten, und
`ausgaben.py` hat sie selbst erzeugt: für Kapitel 8 meldet es Versatz −1 und
schreibt daneben, dass +0 besser liegt. Die Warnung hat recht — die Rohausgabe
ist um einen Vers verschoben und liest sich plausibel. Die Ausgabendatei für
Kapitel 8 ist deshalb von Hand gebaut worden (8,1–22 aus Kapitel 8 der Ausgabe,
8,23 aus deren 9,1), die Rohfassung im Prompt ausdrücklich verboten.

Dazu der zweite `wackeln`-Fall, gefunden von `paketcheck.py` Abschnitt A:
`Starrsinn` ist im Bestand unbelegt und stand in 7,24 und 9,13 verschieden,
obwohl beide Verse dieselbe Buchformel tragen. Sieben Pflichtläufe melden dazu
nichts — es gibt keine Zeile im Bestand, gegen die zu prüfen wäre.

Paket 4 hat den größten Vorlagenblock des Buches eingesammelt: 10,12–16 sind
mit 51,15–19 wörtlich gleich (bis auf ein `aber` in 10,12). Und es hat gezeigt,
dass der Werkzeugbefund eine **untere Schranke** ist — die zweite Hälfte von
10,13 steht fertig in Psalmen 135,7, was `parallelen.py` nicht gemeldet hat und
der Agent selbst gefunden hat.

Paket 5 hat die **Schwert-Hunger-Pest-Formel** entschieden, die das halbe Buch
trägt, und einen Fehlertyp aufgedeckt, den kein Pflichtlauf sehen kann:
`Gürtel` stand in 13,1 spanisch anders als in den sieben übrigen Vorkommen
derselben Szene. `glosskollision.py` sieht nur innerhalb eines Verses,
`paketcheck.py` nur zwischen Kapiteln — eine Uneinheitlichkeit **innerhalb**
eines Kapitels fällt durch beide Netze und ist beim Einsammeln von Hand
gefunden worden.

Die Konsequenz daraus läuft seit Paket 6 mit: `konsistenz.py 24` nach jedem
Build. Es hat sofort einen Fall gefunden, den kein anderes Netz sehen kann —
`Angst` stand in 6,24 anders als in 4,31, 13,21 und 15,8, bei gleicher
Bedeutung und gegen alle vier Ausgaben. `paketcheck.py` konnte es nicht sehen
(verschiedene Pakete), `glosskollision.py` nicht (verschiedene Verse), und der
Bestand steht 97-mal auf der falschen Lesart.

Die drei Werkzeuge, die in diesen 24 Paketen entstanden sind:

- **`paketcheck.py`** vergleicht die gleichzeitig gebauten Kapitel
  gegeneinander. Sein Abschnitt A meldet die Klasse, die keine Pflichtprüfung
  sehen kann: **im Bestand unbelegte Lemmata, die zwei Agenten verschieden
  geprägt haben.** Anlass war `wackeln` (40,20 gegen 41,7), gefunden erst beim
  Einsammeln von Hand; im letzten Paket des Buches hat das Werkzeug denselben
  Fall selbst gefunden (`Schweinefleisch`, 65,4 gegen 66,17).
- **`promptcheck.py`** hält die in Backticks gesetzten Wörter eines Prompts
  über einen Stammvergleich gegen den Quelltext. Anlass war der älteste Befund
  des Verfahrens: die Agenten widerlegen in jedem Paket ein Dutzend meiner
  Hinweise, fast immer, weil ich Wörter behaupte, die nicht dastehen. Seit
  Paket 18 läuft es **vor** dem Abschicken; die Zahl der widerlegten Hinweise
  ist von 28–29 auf 8–17 gefallen, und was übrig bleibt, sind Aussagen über
  Wörter, die es gibt (Level, Numerus, Bedeutung).
- **`levelcheck.py --fix`** behält jetzt die Schreibweise der Datei. Dabei sind
  396 Levelrutscher in den Kapitelquellen über 28 Bücher bereinigt worden — am
  gebauten Bestand ändert das nichts, aber die Quelle behauptete etwas anderes
  als das Ergebnis.

Vier Regeln haben sich über die 24 Pakete herausgeschält:

1. **Eine gemessene Ähnlichkeit sagt nichts, ein Block trägt bis zu der Stelle,
   an der der deutsche Text ein anderes Wort schreibt.** Paket 14: von sieben
   als „wörtlich" eingestuften Versen war genau einer identisch. Paket 18:
   51,11 gegen 35,10, 22 Formen identisch, null abweichend. Paket 21: 60,16
   gegen 49,26, 13 von 13.
2. **Der Blockmesser misst eher zu wenig als zu viel.** Viermal getroffen:
   61,1 gegen Lukas 4,18 (gemessen 21, wörtlich gleich 32), 65,25 gegen 11,9
   (gemessen 11, gleich 24), 66,1 gegen Apg 7,49 (zwei Blöcke, getragen 19 von
   20), 63,13 gegen Ps 106,9 (gemessen 4, getragen 8). Er findet nur
   zusammenhängende Folgen, und Zitate sind zerstreut.
3. **Eine Kollisionsauflösung gilt im Kollisionsvers, nicht im Wortfeld.**
   `Gewand`/`Kleid` (63 gegen 64,5), `beschämt` (41,11 gegen 42,17),
   `gemeinsam` (14 Stellen in Jesaja, ausgewichen in genau den vier mit
   `zusammen`). Eine Entscheidung, die aus einer Kollision entstand, gilt
   dagegen im **ganzen übernommenen Block**: 62,11 trägt `bei` = *beside*, weil
   40,10 ein `mit` im Vers hatte, das 62,11 gar nicht hat.
4. **Was über Kapitelgrenzen läuft, wird vor dem Start festgelegt.** Seit
   Paket 16 gehen die paketweiten Reihen wortgleich in alle Prompts; seither
   meldet `paketcheck.py` Abschnitt A neun Pakete lang null Fälle.

Was Jesaja bisher gelehrt hat, steht in `WORTFELD_JESAJA.md` (ein Abschnitt je
Paket). Die drei Funde mit Reichweite über das Buch hinaus:

- **Paket 7 fand 52 falsche italienische Artikel vor `HERR`** — der Bestand
  stand 1420 : 25 für `il`, und alle 25 Ausreißer waren Jesaja. Ursache ist die
  **Nachbarfalle**: RIV schreibt *l'Eterno*, die Elision wanderte beim Übertragen
  mit, und das Nachbarwort wurde nicht angepasst. Französisch (`l' ÉTERNEL`) und
  spanisch (`el SEÑOR`) sind richtig — **nur italienisch war es falsch**, weil
  `SIGNORE` konsonantisch anlautet. **Paket 8 hat den Fehler nicht geerbt**
  (21 von 21 Stellen richtig); die Korrektur hinter dem Einsammeln hat gehalten.
- **Namen: `belegt.py` und `lexicon.py` schweigen zu Recht und trotzdem gibt es
  eine Vorlage.** Der l1912mod schreibt Eigennamen nicht durchgehend gleich
  (`Schinar`/`Sinear`, `Anatot`/`Anathoth`). Verfahren: Lemma folgt der
  Jesaja-Schreibung, Glossenreihe kommt aus dem Bestand — aber **erst die vier
  Ausgaben aufschlagen**, denn Lautähnlichkeit ist kein Beweis für denselben
  Träger (`Lascha` gegen `Lasa` sind zwei verschiedene Orte).
- **Wo zwei Kapitel einer Welle zwei Bestandsreihen desselben Lemmas wählen,
  entscheidet nicht die Belegzahl, sondern was die Ausgaben an den beiden Versen
  selbst schreiben** (Paket 8, `Hüfte` in 20,2 gegen 21,3). `konsistenz.py` sieht
  zwei belegte Reihen und schweigt — dieser Fall ist nur beim Einsammeln zu finden.
- **Dasselbe Kriterium sagt auch, wann eine Divergenz stehen bleiben muss.**
  Paket 9 brauchte deshalb **keine einzige Angleichung**: `in der Höhe` trägt in
  22,16 und 24,21 zwei verschiedene Reihen, und beide sind richtig — die Stellen
  meinen die Felsgruft gegen den Himmelsbereich, der Bestand spaltet selbst so,
  und die drei romanischen Ausgaben schreiben in 24,21 wörtlich, was dort steht.
- **Ein gemeldeter „Bestandsbefund" ist erst dann ein Auftrag, wenn die
  Auszählung zeigt, dass eine Seite *falsch* ist — nicht nur seltener.** Paket 9
  brachte beides an einer einzigen Wendung: italienisch `dei eserciti` war
  ungrammatisch (5 Stellen, alle Jesaja, korpusweit auf `degli` korrigiert —
  die zweite Auflage der Nachbarfalle), englisch `of` gegen `of the` dagegen ist
  eine offene Entscheidung über 62 Einträge in sieben Büchern und wurde
  ausdrücklich **nicht** angefasst.

**Klagelieder (25) ist am 04.09.2026 fertig geworden** — 5 Kapitel, 154 Verse,
3219 Einträge, 780 verschiedene Lemmata, 135 Mehrwörter, in 2 Paketen. Das Buch
ist zugleich das erste, bei dem die **Modernisierung des l1912mod vor der
Annotation** stand: Kapitel 2 war durchgehend altertümlich und ist ganz neu
geschrieben worden, dazu fünf Verse in Kapitel 1 und einer in Kapitel 4.

Daraus die wichtigste Lehre des Buches — **mein Archaismus-Maß war in beide
Richtungen falsch geeicht.** Ich hatte `Schütte`, `Stehe`, `Hebe` (gewöhnliche
Imperative) als Archaismen gezählt und dafür `richte…zurecht`, `zugerichtet`,
`darniederliegt`, `großsprecherisch` übersehen. Folge: Kapitel 1 lief als
„sauber" in die Annotation und war in Wahrheit das schlechteste Kapitel des
Buches (7 harte Archaismen). Brauchbar ist nur die maschinelle Zählung —
**Wörter mit 0–2 Belegen im fertigen Bestand, pro 1000 Tokens**. Und: eine
Modernisierung kann eine **neue Kollision erzeugen**. In 2,5 standen nach
meiner Überarbeitung `vernichtet` und `zerstört` im selben Vers auf derselben
Bestandsreihe; ersetzt durch `verschlungen`, was WEB/LSG/RIV dort ohnehin lesen.

`paketcheck.py` Abschnitt A ist über alle fünf Kapitel **leer** — kein neu
geprägtes Lemma ist von zwei Agenten verschieden entschieden worden, und das
bei fünf unabhängig gelaufenen Kapiteln. Die zentrale Buchentscheidung
`schauen` (*look*) gegen `sehen` (*see*) steht an allen vier Kollisionsstellen
(1,11 · 1,12 · 2,20 · 5,1) wortgleich, geschrieben von drei verschiedenen
Agenten. Beim Einsammeln waren sechs Angleichungen fällig, alle in Abschnitt B
oder in `ausreisser.py`: `Gegner` Plural auf die Bestandsreihe *opponents*
(19 Belege), `achten` auf *esteemed*, `liegen` 5,18 auf die Buchreihe
*yace · gît*, `aufdecken` 4,22 auf die Schuld-Reihe *expose* (wie 2,14),
`lauern` 3,10 auf *lurks* und `daran` 5,1 auf it *ci*.

Ein siebter Zug ist **zurückgenommen** worden und ist der lehrreichste: ich
hatte `Ohr` in 3,56 von *oreja* auf die Bestandsmehrheit *oído* gelegt — und
`glosskollision.py` meldete sofort ein neues Paar, weil `gehört` im selben Vers
spanisch ebenfalls *oído* ist. Der Agent hatte *oreja* nicht aus Nachlässigkeit
gewählt, sondern als Kollisionsauflösung. **Ein `ausreisser.py`-Treffer ist erst
dann ein Auftrag, wenn im Kollisionsvers nichts dagegen steht.**

Drei weitere Abweichungen sind nach Prüfung **stehen geblieben**: `Himmel`
4,19 en *sky* (die Adler am Himmel — der Bestand führt *sky* 82-mal, darunter
Jeremia 8,7 für dieselben Vögel), `Hilfe` 4,17 en *aid* (Kollision mit
`helfen` im Vers) und `kein mehr` in 5,14 gegen 2,9 (nur in 5,14 steht
`nicht mehr` im selben Vers). `Volk` trägt im Buch **vier** Reihen —
*people* · *nations* · *peoples* · *nation* (4,17) —, jede am Vers entschieden.

**Hesekiel (26) ist seit 04.09.2026 in Arbeit** — 48 Kapitel, 1273 Verse,
18 Pakete nach `PAKETE_HESEKIEL.txt`, geschnitten nach Tokengewicht. Das Buch
ist auf Formeln gebaut wie kein anderes: `dubletten.py` findet **979
Verspaare**, fast das Vierfache von Jeremia, und der Grund ist eine einzige
Wendung — die Wortereignisformel steht 34× zeichengleich da. Sie war schon
entschieden, bevor das Buch anfing: Jeremia 1,4 = 2,1 = 16,1 ist derselbe
Vers, und `ergehen an` ist nie ein Mehrwort.

Paket 1 (Kap. 1 · 2 · 3) hat die drei Signaturformeln des Buches festgelegt.
Die größte ist **`Menschensohn`** mit 93 Vorkommen: der Bestand führt 88
Belege, **alle neutestamentlich**, mit dem messianischen Titel — in Hesekiel
ist es die Anrede an den Propheten. Die Ausgaben trennen die beiden selbst, in
drei von vier Sprachen (englisch über die Kleinschreibung von *man*, spanisch
und italienisch über den fehlenden Artikel); **Französisch kann nicht
trennen**, das bleibt eine echte Verschmelzung der Zielsprache.
`paketcheck.py` Abschnitt A und C sind über alle drei Kapitel leer, und das
Paket trifft mit 1447 Tokens die Planung auf den Token genau.

**Ein Agent hat die Kollisionsanweisung der Vorbereitung widerlegt.** Ich
hatte für 1,3 geschrieben, `kommen` solle vor `ergehen` auf eine Lesart
ausweichen, „die der Bestand schon führt". Der Agent hat alle 40 `kam`-Lesarten
ausgezählt: **jede einzelne** steht englisch in der *come*-Familie, und die
idiomatisch nächste Stelle (1. Könige 18,46 und 2. Könige 3,15, „die Hand des
HERRN kam über Elia/Elisa") trägt genau die kollidierende Reihe. Es gibt die
Auflösung im Bestand nicht. Er ist deshalb den Ausgaben gefolgt — WEB, LSG und
RIV lesen dort selbst die Kopula — und hat das ausdrücklich als Neuprägung in
en/fr gemeldet, statt eine passende Bestandszeile zu behaupten.

Zwei Befunde mit Reichweite über das Buch: der l1912mod liest an den
`widerspenstig`-Stellen **`Volk`, wo alle vier Ausgaben „Haus" schreiben**
(2,5 · 2,6 · 2,8) — annotiert wird das Deutsche, und die Wendung kehrt
dutzendfach wieder. Und `Wesen` trägt im Buch **zwei** Bedeutungen: das
Thronwagen-`Wesen` (*living creatures*) und in 3,19 den Lebenswandel
(*nature*, nach Richter 2,19, wo wörtlich „ihr böses Wesen" steht).

**Stand nach Paket 16: 44 von 48 Kapiteln, 1166 Verse, 30 037 Einträge.**
`paketcheck.py` Abschnitt C ist **vierzehnmal in Folge leer** geblieben;
Abschnitt A hatte in Paket 14 seinen ersten Treffer — und der ist ein Erfolg:
**zwei Agenten haben dasselbe Wort unabhängig neu geprägt und dieselbe Reihe
gewählt** (`besiedeln`, 36,33 und 38,12), der Unterschied ist reine Flexion.

Drei Erkenntnisse aus den Paketen 5 bis 8, die über Hesekiel hinausreichen:

**Die Anerkennungsformel hat 71 Vorkommen, nicht 54.** Die Zahl ist zweimal
nach oben korrigiert worden, beide Male von einem Agenten, beide Male aus
demselben Grund: mein Suchmuster war am *Ende* festgemacht (`der HERR bin`)
statt am Kern. Verdeckt wurde die Formel nacheinander durch die Wortstellung,
durch eine eingeschobene Apposition (13,9) und durch ein anderes Prädikat
(17,21 · 17,24). **Die Konstante ist `erkennen` + `dass ich`.** An allen 71
Stellen steht die *recognize*-Familie — maschinell geprüft, null Abweichungen.
Dieselbe Fehlerform ein viertes Mal in Paket 8: eine Botenformel in der
`Gott`-losen Ausnahmefassung (21,14), die meine Paketvorbereitung nicht
mitgezählt hatte, obwohl `PAKETE_HESEKIEL.txt` sie führte.

**Die Lexikonfalle hat zwei Richtungen.** Bekannt war, dass eine erdrückende
Bestandsmehrheit vollständig neutestamentlich sein kann und für ein
Prophetenbuch nicht passt (`Menschensohn` 88 von 89, `Anstoß` 16 von 21,
`aufnehmen` 24 von 40). Paket 8 zeigt die Gegenrichtung: bei `schärfen`
**verdeckt die häufigste Lesart die passende**. Die vier NT-Belege stehen für
*einschärfen*; darunter, ungelesen, acht AT-Belege für das Schleifen einer
Klinge. Daraus die Regel: **bei mehrdeutigen Lemmata nie die erste Zeile von
`fixgloss.py show` allein nehmen** — die Liste ist nach Häufigkeit sortiert,
nicht nach Passung.

**Ein Fehlertyp, den kein Werkzeug sah, hat jetzt ein eigenes:**
`anno-tools/kongruenz.py` prüft italienische Possessiva gegen das folgende
Nomen. `il suo Bund` statt `la sua alleanza` verletzt weder Struktur noch
Bindung noch Level — `selfcheck`, `qa`, `glosskollision`, `levelcheck` und
`konvention` schweigen alle. Ein Agent hatte zehn solche Stellen im eigenen
Kapitel gefunden; der buchweite Lauf fand acht weitere, **vier davon in längst
committeten Kapiteln**. Die Ursache ist durchweg dieselbe: das deutsche Genus
schlägt durch, wo das italienische abweicht (`Hand`/`mano`, `Kopf`/`testa`,
`Bund`/`alleanza`). Der Fehlertyp ist nicht hesekielspezifisch — ein Lauf
gegen die 51 fertigen Bücher steht noch aus.

In Paket 9 kam **Französisch** dazu, nachdem ein Agent `sa règles` in 18,6
fand — der italienische Lauf konnte das nicht sehen, weil `mestruazione` dort
Singular ist. Geprüft wird französisch nur der Numerus; das Genus hängt am
Nomen und steht vor Vokal auch bei Femininum auf `son`. Drei weitere echte
Fehler (3,18 · 16,39 · 16,47), alle behoben.

**Der vierte und schwerste Vorbereitungsfehler des Buches war meiner:** die
Vorgabetabelle für Paket 9 gab **beide Signaturformeln falsch wieder** — die
Wortereignisformel in vier Feldern, die Botenformel in dreien. Die fertigen
Kapitel waren durchweg richtig; ich hatte die Reihen von Hand abgeschrieben
statt sie aus einer Kapiteldatei zu ziehen. Beide Agenten haben es unabhängig
gefunden und sind dem Bestand gefolgt. Daraus die Regel, die jetzt in
`PAKETE_HESEKIEL.txt` steht: **eine Reihe, die im Bestand schon zwanzigmal
steht, wird nie abgeschrieben.** Jede Vorgabetabelle nennt ab sofort die
Kapiteldatei und den Vers, aus dem eine Formel stammt.

Und die Lehre vom zu engen Suchmuster hat ihre Umkehrung gefunden. Beim Prüfen
derselben Tabelle gegen den Quelltext habe ich mit ungebundenen Mustern
gesucht — „Bestechung" matcht in „Bestechungs**geld**", „Wucher" in
„Wucher**zinsen**", „Jungfrau" in „jung**fräulichen**". Fünf Tabellenzeilen
liefen deshalb ins Leere. **Ein Prüfmuster muss an beiden Enden gebunden
sein:** zu eng übersieht es Vorkommen, zu weit behauptet es welche.

In Paket 10 hat sich die erste Hälfte dieser Regel gleich noch einmal bestätigt,
diesmal rechtzeitig: die **Wortereignisformel steht 50-mal im Buch, nicht 36**.
Vierzehn Vorkommen sind umgestellt („Im elften Jahr … *erging das Wort des
HERRN* an mich"), fast alle nach einer Datumsangabe. Sechs davon liegen in
fertigen Kapiteln und sind **alle sechs zeichengleich** mit der Referenz — die
Agenten hatten sie erkannt, obwohl mein Muster sie nie zeigte. Das ist der
fünfte Formelfund dieser Art und der dritte ohne Schaden.

Der praktische Schluss daraus ist nicht, bessere Muster zu schreiben, sondern
**den Agenten die Quelle zu nennen statt der Zahl**. Seit Paket 10 werden die
Glossenreihen der Signaturformeln maschinell aus den Kapiteldateien gezogen und
als eigene Datei mitgegeben.

Zwei Werkzeugbefunde kamen dazu. `belegt.py` meldete eine Form unter fremdem
Lemma (`Morden` unter `Mord`) und **verschwieg dabei, dass das gesuchte Wort
zugleich ein eigenes Lemma ist** (`morden`, belegt über `mordet` in Jeremia
7,9) — der Hinweis stand bisher nur im Zweig „gar nicht belegt". Behoben, über
acht Kontrollwörter null Fehlalarme. Und ein neuer buchweiter Lauf sucht
Stellen, an denen ein im Buch verwendetes Mehrwort fehlt: **`durchs Schwert
fallen` fehlte an drei Stellen** (11,10 · 23,25 · 24,21), alle nachgetragen.

Schließlich ein Fallentyp, den kein Werkzeug finden kann: **`Kereter` hat im
Bestand einen Zwilling unter anderer deutscher Schreibung** — `Kreter`, acht
Belege, mit genau den Glossen, die alle vier Ausgaben schreiben. Zwei
Schreibungen desselben Namens teilen weder Form noch Stamm. Bei Eigennamen
lohnt deshalb der Blick auf die Ausgaben: schreiben alle vier dasselbe, steht
der Name womöglich schon im Bestand.

**Diese Prüfung hat im nächsten Paket dreimal getroffen**: `Minnit` = `Minnith`
(Richter 11,33), `Elischa` = `Elisa` (1. Chronika 1,7), `Bet-Togarma` =
`Thogarma`. Der `Elischa`-Fall zeigt zugleich die Grenze: `Elisa` trägt im
Bestand auch 79× den **Propheten**, ein bloßes Übernehmen hätte Insel und
Prophet verschmolzen. Es braucht also ein eigenes Lemma mit der übernommenen
Reihe, nicht das fremde Lemma selbst.

Der `belegt.py`-Fix aus Paket 10 hat dabei **nicht funktioniert** — ein Agent
fand, dass `flicken` nur als Substantiv `Flicken` gemeldet wird, obwohl es
zugleich ein Verb-Lemma ist. Meine Bedingung verglich kleingeschrieben, und
`Flicken`/`flicken` sind kleingeschrieben identisch. **Gerade das ist die
häufigste Bauform dieses Falltyps** (`morden`/`Morden`, `schichten`/`Schichten`).
Jetzt case-sensitiv.

In Paket 13 ist ein Befund aufgetaucht, der **größer ist als dieses Buch** und
deshalb offen bleibt: die **Elision romanischer Artikel vor Vokal**. Ein Agent
meldete, dass 18,21 · 18,23 · 18,24 französisch *le* und italienisch *il* vor
*impie*/*empio* schreiben, während Kapitel 33 *l'* schreibt. Die Messung ergab
194 nicht elidierte Stellen allein in Hesekiel und **2828 elidierte gegen 2091
nicht elidierte im Gesamtbestand**. Das ist keine Mehrheit, die eine
Entscheidung trägt, und die Frage ist grundsätzlich: Wort-für-Wort-Glossen
sind kein Fließtext, *le* ist als Glosse für `der` korrekt, und die Elision
ist eine Sandhi-Erscheinung des zusammenhängenden Textes. Eine Korrektur
mitten im Buch hätte 194 Stellen hier gegen 4919 dort gestellt — sie ist
zurückgenommen und der Befund als Bestandsfrage vorgemerkt.

Ebenfalls aus Paket 13, zur Zuverlässigkeit von `hints.py`: das Werkzeug
vergleicht **Bestands-Defaultformen**, nicht die Formen im Vers. Dadurch hat
es in 32,25 eine Kollision *unter*gemeldet (nur Englisch statt vier Sprachen)
und in 33,13 eine gemeldet, **die es nicht gibt** — dort stehen `Gerechter`
und `gerecht` in verschiedenem Numerus und tragen deshalb von sich aus
verschiedene Glossen. Beide Male hat erst die Prüfung am Vers das geklärt.

Zwei Regeln haben sich in Paket 11 geschärft. Die erste: **eine Ausgabe kann
nicht nur ein Wort, sondern eine ganze Liste anders zuordnen.** In der
Edelsteinliste von 28,13 verschieben alle vier Ausgaben die Steinreihe so, dass
ihnen zu folgen zwei Kollisionen im selben Vers erzeugt hätte. Der Test für
„Bestand oder Ausgabe?" läuft deshalb über den Vers, nicht über das Wort:
erzeugt die Ausgabenlesart eine Kollision, ist sie falsch.

Die zweite betrifft `kongruenz.py`. Die in Paket 9 eingebaute Doppelprüfung
gegen Adjektive war ein Rückschritt — sie hätte echte Treffer verschluckt.
Ersetzt durch etwas, das im Deutschen umsonst zu haben ist: **die
Großschreibung.** Der Lauf sucht das erste großgeschriebene Folgewort, weil
Nomen groß und Adjektive klein sind. Zwölf Fehlalarme verschwanden, zwei
verdeckte Treffer kamen ans Licht.
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
| **1. Chronik (13)** | **29** | **942** | **17 062** |
| **2. Chronik (14)** | **36** | **822** | **22 607** |
| **Esra (15)** | **10** | **280** | **5 997** |
| **Nehemia (16)** | **13** | **406** | **8 758** |
| **Ester (17)** | **10** | **167** | **5 041** |
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
| **Hiob (18)** | **42** | **1070** | **16 617** |
| **Psalmen (19)** | **150** | **2528** | **39 098** |
| **Sprüche (20)** | **31** | **915** | **14 019** |
| **Prediger (21)** | **12** | **222** | **5 217** |
| **Hohelied (22)** | **8** | **117** | **2 407** |
| **Jesaja (23)** | **66** | **1291** | **32 487** |
| **Summe gesamt** | **1005** | **26 973** | **588 313** |

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

### 1. Chronik: der Kreuzabgleich schlägt jedes Prüfskript

Über die letzten fünf Kapitel des Buches sind **zwölf Angleichungen** nötig
geworden, und **keine einzige** davon hat ein Prüfskript gemeldet.
`selfcheck.py`, `qa.py`, `validate.py` und `hilfsverb.py` liefen über alle
fünf Kapitel ohne Befund; gefunden hat sie ausnahmslos der paarweise
Formvergleich zwischen gleichzeitig gelaufenen Kapiteln. Alle zwölf sitzen in
**wörtlich identischen Satzteilen**:

| Satzteil | Stellen | was auseinanderlief |
|---|---|---|
| `die Obersten über tausend und über hundert` | 26,26 · 27,1 · 28,1 · 29,6 | *chiefs* gegen *leaders*, *a thousand* gegen *thousand* |
| `den Jüngeren wie den Älteren` | 25,8 · 26,13 | *cadet/minore* gegen *plus jeune/più giovane* — **und A2 gegen B1** |
| `Verwalter über das Vermögen des Königs` | 27,31 · 28,1 | *property* gegen *wealth* |
| `die geweihten Schätze` | 26,20 · 26,26 · 28,12 | *dedicated* gegen *consecrated* |

Die Wendung mit den Obersten ist der Lehrfall: sie steht **fünfmal im Buch**
und danach weiter in 2. Chronik. Die Trennung ist ausgezählt worden, nicht
geraten — *leaders* hat 11 Belege, alle vom Typ „die Obersten Israels / des
Volkes", *chiefs* steht beim Truppenkommando, und **1Chr 15,25 („die Obersten
über Tausend") ist die nächste Parallele**. In **28,1 stehen beide Lesarten im
selben Vers**, elf Positionen auseinander.

Das Muster ist inzwischen dreimal in Folge dasselbe (2. Könige, 1. Chronik
Welle 3, 1. Chronik Welle 9): **wo zwei Agenten gleichzeitig an derselben
Formel arbeiten, prägen sie sie verschieden**, und strukturell ist beides
tadellos. Das vorherige Gegenmittel — den gemeinsamen Satz vorab in beide
Prompts binden — hat dort gegriffen, wo ich die Überschneidung vorhergesehen
habe. Vorhergesehen habe ich sie in vier von zwölf Fällen.

### Zwei Wege, dieselbe Kollision aufzulösen — und nur einer ist der des Bestands

`Gold`/`golden`, `Silber`/`silbern`, `Bronze`/`bronzen` und `Eisen`/`eisern`
stehen in 28,14 · 28,16 · 29,2 paarweise im selben Vers und tragen im Bestand
dieselbe Glosse. Zwei Agenten haben das unabhängig aufgelöst, und zwar
entgegengesetzt:

- **über das Substantiv** (Kapitel 28): `des Goldes` → *the gold*, `des
  Silbers` → *the silver*, das Adjektiv bleibt *golden* / *silver*
- **über das Adjektiv** (Kapitel 29): `silbernen` → *of silver*, `bronzenen` →
  *of bronze*, `eisernen` → *of iron*, das Substantiv bleibt bloß

Beide Fassungen trennen sauber in allen vier Sprachen. Entschieden hat der
Bestand: **1Chr 18,8** hat genau diese Kollision (`Bronze` und `bronzenen` in
einem Vers) und löst sie über das Adjektiv, und **4Mo 7,85 f.** — dieselbe
Konstruktion „das Gewicht des Goldes / des Silbers" — lässt das Substantiv im
Genitiv bloß. Kapitel 28 ist nachgezogen worden; damit verschwinden die
Lesarten *the gold* und *the silver*, die es sonst **nirgends im Korpus** gibt.

Die Auflösung bleibt dabei **lokal**: `bronzen` steht 36-mal auf *bronze* und
nur in 18,8 auf *of bronze*. Eine Kollisionsauflösung zieht nie die anderen
Belege mit.

### Ein Agent hat meiner Vorgabe widersprochen und behalten recht

Ich hatte dem Agenten von Kapitel 29 vorgegeben, `Gepriesen` (29,10) auf die
Mehrheit *Praised · Bendito · Béni · Benedetto* zu setzen (7 Belege) und den
einen Ausreißer *Blessed* in **1Chr 16,36** zu melden, damit ich ihn nachziehe.

Er hat es nicht getan und begründet, warum: 16,36 ist der **einzige** Vers
außer 29,10, in dem `Gepriesen` und `lobte` zusammenstehen — und `lobte` trägt
die Bindung *praised*. Die Fassung *Blessed* löst dort die Kollision, die
*Praised* gerade erzeugen würde. Die sieben Mehrheitsbelege haben kein `loben`
im Vers. **Wer die Mehrheit nachzieht, baut die Kollision ein, die die
Minderheit vermeidet.** 16,36 bleibt, wie es ist, und 29,10 folgt ihm.

Das ist der zweite Fall dieser Art im Buch — in Welle 8 hatte mein
Bindungsdokument selbst den `Oberhaupt`-Ausreißer aus 11,6 zur Regel erklärt.
**Eine Minderheitslesart ist erst dann ein Ausreißer, wenn man nachgesehen
hat, was sie im Vers leistet.**

### `hints.py` ist umlautblind

`Vorhöfe` (28,6) wurde als unbelegte Form gemeldet, mit den verwandten Formen
`Vorhaben`, `Vorhalle`, `Vorhang`. Das Lemma `Vorhof` hat **30 Belege**, und
einer davon steht fünf Kapitel vorher in **1Chr 23,28**. Der Stammfilter
vergleicht Buchstabenfolgen ohne Umlaut-Normalisierung und findet `Vorhof`
neben `Vorhöfe` nicht.

Vier der neun in Kapitel 28 als „nur über den Stamm belegt" gemeldeten Formen
waren so fälschlich in der Liste; in Kapitel 29 waren es acht von zehn, in
Kapitel 27 siebenundzwanzig von siebenunddreißig. Die Agenten haben es jedes
Mal selbst gemerkt, weil sie den Extrakt nach dem **Lemma** fragen statt der
Form — aber die Liste treibt sie zum Neuprägen, und Neuprägen ist genau das,
was den Bestand auseinandertreibt. Ein Normalisierungsschritt im Stammfilter
würde das beheben.

### Die Zählproben gehen dreimal nicht auf, und dreimal hat der Text recht

- **25,9–31**: 24 Lose, jedes mit `zwölf` — aber das Wort steht nur
  **23-mal**. Dem ersten Los fehlt die Zahl. Erst mit ihr ergibt sich die 288
  aus 25,7. Die Lücke steht schon im Luther 1912 und im hebräischen Text.
- **27,16–22**: die Stammesliste lässt **Gad und Asser** aus, schiebt mit den
  Aaroniten eine Priestersippe ein und teilt Josef in Ephraim und zweimal
  halb-Manasse — 13 Einträge statt 12.
- **26,19**: der Vers, gegen den ich die Torwachen prüfen ließ, enthält gar
  keine Zahl.

Dazu **24,15 `Hefir`** — die Form steht genau einmal im ganzen `l1912mod`,
während derselbe Name in Neh 10,21 `Hesir` lautet. Mit größter
Wahrscheinlichkeit eine Lang-s-Verlesung der Modernisierung. Geglost ist
*Hezir*, damit beide Stellen zusammenfinden; der Text bleibt unangetastet.

**Gemeldet, nicht korrigiert** — wie in 3,22, 6,45 und 7,3.

### Was der Prompt an Zahlen erfunden hat

Für Kapitel 27 habe ich „1 alleinstehender Gedankenstrich" behauptet. Das
Kapitel hat **keinen**, weder als Token noch im Fließtext — und die
Verteilungstabelle in `BINDUNGEN_CHRONIK.md` führt Kapitel 27 gar nicht auf.
Die Zahl stammt aus dem Prompt, nicht aus den Daten.

Genauso: `vierundzwanzigtausend` steht in Kapitel 27 **dreizehnmal**, nicht
zwölfmal — die dreizehnte ist die Rahmenangabe in 27,1. 28,1 hat weder
`Aufseher` noch `Mächtige`, sondern `Verwalter`, `Kriegsleute` und `angesehene
Männer`. In 25 gibt es keinen `Sänger`, keine `Anweisung des Königs`, keine
`Trompete` und keine `Posaune`. In 27 keinen `Kanzler`, keinen `Schreiber`,
keinen `Rat` und keinen `Aufseher`.

Über das ganze Buch sind **mehr als vierzig** meiner Prompt-Vorgaben vom
Quelltext widerlegt worden. Die Quote liegt damit dort, wo sie in der
Offenbarung und in 3. Mose lag, und die Konsequenz bleibt dieselbe: **der
Prompt-Hinweis ist der unzuverlässigste Teil des Verfahrens**, und der Satz
„der Quelltext hat immer recht" gehört in jeden Auftrag.

### Offen geblieben, jeweils ein eigener gezählter Zug

- **`König` vor Eigennamen** — im Buch 5:5 zwischen *King* und *king*
  („König David" mitten im Satz), korpusweit 1135:66 für klein. Kapitel 29 ist
  in sich angeglichen, das Buch nicht.
- **Die italienische Großschreibung der Gentilizia** gilt für die
  **levitischen Sippennamen nicht**: `ghersoniti`, `ishariti`, `kehatiti`,
  `merariti`, `ebroniti`, `amramiti`, `uzzieliti` stehen durchgehend klein,
  `Korahiter` dagegen 3:1 auf `Coreiti`. In 26,19 steht deshalb `Coreiti`
  neben `merariti`. Etwa zwanzig Einträge.
- **`Herrschaft`** steht im Regierungs-Sinn it 10:4 zwischen *dominio* und
  *regno*. Das Buch folgt der Mehrheit.
- **71 italienische Glossen mit dem Digraph „Sh"**, den die italienische
  Orthografie nicht kennt (Bestand 196:71 für die S-Form).
- **`bauen`** 117 *construir* : 85 *edificar*.

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
| `vorlage.py <nrA> <kapA> <nrB> <kapB>` | Parallelkapitel als gemessene Vorlage, Vers für Vers, mit Versatz und Abweichungen |
| `parallelen.py <nr> <kap> [minblock]` | Parallelstellen im **ganzen** Bestand, sortiert nach längstem gemeinsamen Block |
| `dubletten.py <nr> [--anteil] [--min]` | Verspaare **innerhalb** eines Buches — was `parallelen.py` im noch leeren Buch prinzipiell nicht findet |
| `mehrwort.py <nr…>\|alle [--nur=…] [--fix]` | Einzelwörter, die die Glosse ihres Mehrwort-Eintrags übernommen haben |
| `zweigleisig.py <nr…>\|alle [--min 5] [--wieoft 2]` | Lesarten, die ein Kapitel erfunden und das nächste weitergereicht hat |
| `BEFUNDE_NEHEMIA.md` | Bestandsbefunde aus Nehemia, gemeldet und noch nicht entschieden |

**`konvention.py`, `levelcheck.py` und `kreuz.py` hatten den Scratchpad-Pfad
der Esra-Sitzung fest eingebaut** und wären in jeder neuen Sitzung ins Leere
gelaufen. Sie nehmen ihn seit Nehemia aus **`ANNO_OUT`** und brechen mit klarer
Meldung ab, wenn er fehlt. Ein toter Pfad als Vorgabewert wäre beim nächsten
Buch wieder stillschweigend falsch gewesen.

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

## Nachrücken statt Wellen — was Nehemia dazu sagt

Nehemia ist in fünf Wellen zu je drei Kapiteln gelaufen, nicht im
Nachrück-Verfahren der Briefe. Das hat einen Preis (Leerlauf, wenn ein Kapitel
dreimal so lang ist wie die anderen) und einen Ertrag, der ihn aufwiegt: **die
Übergabetabelle zwischen den Wellen entsteht maschinell.**

Nach jeder Welle wird gebaut und committet; für die nächste erzeugt ein
Zehnzeiler aus der gebauten Anno-Datei eine Tabelle „Was die fertigen Kapitel
schon festgelegt haben", **gefiltert auf die Wortformen der neuen Kapitel** und
mit `tabellenpruefung.py` gegen den Bestand geprüft. Sie wuchs von 389 Zeilen
(Welle 2) über 491 und 724 auf 828 (Welle 5), lief jedes Mal mit 0 Abweichungen
durch, und kein Agent musste eine Festlegung erraten, die ein Vorgänger schon
getroffen hatte.

Das ist der Grund, warum in Nehemia **keine einzige** buchinterne
Terminologie-Divergenz nachzuziehen war — anders als in 2. Chronik und Esra,
wo der Kreuzabgleich jedes Mal mehrere fand. Die Wellen-Struktur ist also kein
Rückschritt gegenüber dem Nachrücken, sondern die Voraussetzung dafür, dass die
Übergabe überhaupt maschinell prüfbar wird.

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

## 2. Chronik: was das Buch gelehrt hat

Das Buch ist in **zwölf Wellen zu je drei gleichzeitig laufenden Kapiteln**
entstanden. Die wichtigste Erfahrung ist nicht fachlich, sondern methodisch.

### Der Kreuzabgleich schlägt jedes Prüfskript

Zwischen den drei Kapiteln einer Welle wurden die **gemeinsamen Wortformen**
gegeneinander gehalten (Funktionswörter und Mehrwort-Einträge ausgeschlossen).
Über das ganze Buch hat das **mehr als vierzig echte Abweichungen** gefunden,
und **keine einzige davon hat ein Prüfskript gemeldet** — es sind durchweg
wortgleiche Wendungen mit auseinanderlaufenden Glossen. Beispiele aus den
letzten beiden Wellen: `setzte Hauptleute` stand in 32,6 und 33,14 auf zwei
verschiedenen Glossen; `ganzen` vor Femininum stand in 32,7/32,9 auf
*entera · entière · intera*, während der Bestand **99 zu 8** auf
*toda · toute · tutta* steht; `dazu` stand zweimal auf *en outre* — einer
Lesart, die der Bestand **überhaupt nicht kennt** (Mehrheit *en plus*, 166
Belege).

### Die Agenten widerlegen mehr als sie fragen

Über neunzig Vorgaben aus meinen Prompts sind vom Quelltext widerlegt worden,
und **jede Widerlegung war richtig**. Die lehrreichsten:

- Ich hatte für 2Chr 32 vier Zahlenfragen gestellt. **Das Kapitel nennt keine
  einzige Zahl** — der Chronist streicht sogar die 185 000 aus 2Kön 19,35.
- Ich hatte für 32,33 ein Begräbnis „auf der Anhöhe bei den Gräbern der Söhne
  Davids" angekündigt. Der Text sagt „auf dem **Weg** zu den Gräbern der
  **Nachkommen** Davids" — keine der neun bekannten Todesformeln.
- Ich hatte 33,18–19 als „Geschichte der Könige" und „Geschichte Hosais"
  beschrieben. Beides steht nicht da; es sind zwei verschiedene
  Formelfassungen in einem Kapitel, und in 33,18 fehlt `geschrieben`, sodass
  `steht` die Bedeutung allein trägt.
- Meine Kollisionsauflösung für `all` ↔ `ganz` **trennt in 31,1 nur im
  Englischen**, weil dort ein Neutrum steht. Der Agent hat das gemerkt und
  eine andere belegte Lesart genommen.
- Ich hatte 31,16 und 31,17 als konkurrierende Altersgrenzen beschrieben.
  31,17 verzeichnet die Priester **ohne** Altersangabe.

### Zwei meiner eigenen Messungen waren falsch

**Das Satzzeichen-Skript.** `text.split().count('–')` sieht das Token `–,`
nicht. Das Buch hat **44** Satzzeichen-Tokens, nicht 41; drei Kapitel waren
betroffen. Gefunden hat es der Agent von Kapitel 10, nicht ich.

**Die spanische Altersangabe.** Ich hatte **26 zu 12** für *tenía* gegen *era*
gezählt und daraus geschlossen, `era` sei eine Buchkonvention von 2. Könige,
und den Fix abgelehnt. Mein Skript zählte **jedes** `war` im Vers mit, auch
„seine Mutter *war*…". Zählt man nur das `war` vor der Altersangabe, steht es
**31 zu 1**. Es war kein Muster, sondern ein einzelner Ausreißer. Korrigiert
sind jetzt 2Kön 14,2 und 2Sam 5,4; die Formel steht korpusweit lückenlos.

### Die Parallelenkarte musste zweimal neu gebaut werden

Die erste Fassung maß **Kapitel gegen Kapitel** und war damit blind für jede
Parallele, die über eine Kapitelgrenze der Quelle läuft — 2Chr 5,1 galt als
Sondergut und ist in Wahrheit die engste Parallele seines Kapitels. Die zweite
Fassung hatte eine zu strenge Schwelle. Und die Tabelle in
`BINDUNGEN_CHRONIK.md` führte bis zuletzt fünf Kapitel als „kein Vers mit
Parallele" — eine Zeile aus der **ersten** Karte, die beim Neubau nicht
nachgeführt worden war. Nachgezählt hat **kein einziges Kapitel des Buches**
null Parallelverse.

Die Karte bleibt außerdem prinzipiell blind für **innerbuchliche** Parallelen,
weil sie 2. Chronik nur gegen *andere* Bücher misst. Gerade die Rahmenformeln
wiederholen sich aber im Buch selbst, und dort oft enger: 36,8 ↔ 2Chr 27,7 hat
**20 formgleiche Positionen und null Glossenabweichung** — enger als jede
Königsbuch-Stelle. Diese Parallelen wurden pro Welle von Hand nachgemessen und
den Prompts beigelegt.

### Nachgezogene Bestandsbefunde

- **`von ganzem Herzen` ↔ `mit ganzer Seele`**: sechs Verse führen beide
  Spannen, **vier** trugen identische Einzelwort-Glossen. Jos 22,5, 2Kön 23,3
  und 23,25 folgen jetzt dem Muster aus 2Chr 34,31.
- **Die Thronbesteigungsformel**: 2Kön 14,2 und 2Sam 5,4 nachgezogen.
- **`Obersten der Leviten`** ist *chiefs*, nicht *leaders* — bei Kultpersonal
  entscheidet die Fügung, nicht der Kontext.
- **`brachte` + Sachobjekt** ist französisch *emporta*, nicht *amena*.

### Zwei Agenten sind gestorben, beide Kapitel waren gerettet

Ein Serverfehler und ein Ruhezustand des Rechners. Beide Kapitel ließen sich
vollständig aus den Teildateien rekonstruieren, weil die Prompts
**Schreiben nach jedem Abschnitt von 6–10 Versen** verlangen. Diese Regel
gehört in jeden Prompt.

## Esra: was das Buch gelehrt hat

Vier Wellen zu je drei gleichzeitig laufenden Kapiteln, das letzte allein.
Die Erfahrung ist wieder methodisch, und diesmal betrifft der wichtigste
Befund **den Prompt-Ersteller, nicht die Agenten**.

### Acht von 54 handgetippten Levels waren falsch

Die Vorab-Bindungstabelle für Welle 1 hatte ich zur Hälfte von Hand gefüllt,
weil mein Extraktionsskript beim ersten Lauf nur die Glossen ausgab. **Alle
drei Agenten haben es unabhängig gemeldet** und sind richtigerweise dem
Bestand gefolgt, der je Lemma zu 100 % einheitlich ist:

| Lemma | Tabelle | Bestand |
|---|---|---|
| `Brandopfer` | B2 | **C1** (218 Belege) |
| `Nachkomme` | B1 | **B2** (331) |
| `Gemeinde` | B1 | **B2** (282) |
| `Torhüter` | B1 | **C1** (18) |
| `Gefangenschaft` | B2 | **C1** (17) |
| `Statthalter` | B2 | **C1** (34) |
| `Grundstein` | C1 | **B2** (5) |
| `Tempeldiener` | C1 | **B2** (1) |

Dasselbe bei der Blocktabelle: der Agent von Kapitel 1 fand einen zehnten
Parallelblock zu 2Chr 36,22–23, den ich beim Abtippen verloren hatte
(`sodass er`, Versatz +6).

**Konsequenz — drei neue Skripte, und keine Tabelle mehr von Hand:**

- **`vorab.py`** erzeugt die Bindungstabelle aus dem Bestand: für jede Form,
  die in mehreren Kapiteln der Welle steht, Lemma, Level und Belegzahl.
- **`bloecke.py`** erzeugt die Blocktabelle mit gemessenem Versatz.
- **`tabellenpruefung.py`** hält jede Zeile einer fertigen Tabelle gegen den
  Bestand — Level **und** Glossen.

Und eine Formatentscheidung, die mehr getragen hat als erwartet: die
Belegspalte unterscheidet **eine Zahl** (`27` — der Bestand kennt nur diese
Lesart, übernehmen) von **einem Bruch** (`53/97` — Mehrheitsvorschlag, der
Vers entscheidet). Die Agenten haben in genau diesen Zeilen begründet
widersprochen.

### Fünf bedeutungsblinde Bindungen in einem Buch

`BINDUNGEN_AT.md` nennt je Lemma die häufigste AT-Lesart, auch wo das Wort zwei
Bedeutungen trägt. Esra hat fünf solche Fälle aufgedeckt, jeder mit sauber
getrennten Sachfeldern:

| Lemma | Lesart A | Lesart B |
|---|---|---|
| `Gefäß` | Alltagsgefäß, *recipiente* (21) | **Tempel- und Prunkgerät**, *vasijas* (12) |
| `Becken` | das eherne Meer, *pila · cuve* (12) | **Sprengschalen der Geräteliste**, *tazones · catini* (7) |
| `Rat` | der Ratschlag, *advice* (30, AT) | **das Gremium**, *council* (29, NT) |
| `Aufruhr` | der Menschenauflauf, *uproar* (14, NT) | **der politische Aufstand** |
| `Gewalt` | *violence* | ***force*** (1Mo 31,31) |

Bei `Gefäß` und `Becken` ist es **die Gegenprobe zur Lexikonfalle**: es sieht
aus wie eine Inkonsistenz und ist eine echte Bedeutungsspaltung. Die
Belegverse zu lesen war jedes Mal die Entscheidung.

### Ein fehlender Mehrwort-Eintrag ist für jedes Prüfskript unsichtbar

Kapitel 4 hat gemeldet, dass Esra 1–3 `um zu` und `so wie` **nicht** als
Mehrwort-Einträge führt, obwohl der Bestand sie 267- bzw. 91-mal kennt.
`selfcheck.py` und `qa.py` sehen das prinzipiell nicht: die Einzelwörter sind
vollständig und richtig, strukturell fehlt nichts. Zehn Stellen nachgetragen.

Daraus ist **`konvention.py`** entstanden — es sucht die Wortfolge im Quelltext
und fragt, ob ein Eintrag darauf liegt. Und es produziert **richtigerweise
Fehlalarme**: bei 8,22 (`den König **um** eine Eskorte **zu** bitten` =
`bitten um` plus Infinitiv) und bei 8,27 (`**so** wertvoll **wie** Gold` = die
Vergleichsklammer). Der Bestand führt `so wie` ausnahmslos zusammenhängend
(95 Belege, alle `pos_end`). Beide Male hätte ein Eintrag den Satz falsch
geklammert.

### `levelcheck.py`: was der Build stillschweigend repariert

`buildbook.py` zieht abweichende Level beim Bauen auf die Korpusmehrheit —
die Quelle behauptet danach dauerhaft etwas anderes als das Ergebnis, und die
Abweichung wandert durch jeden Neubau mit. In Esra waren es 3 Einträge in
Welle 2, 10 in Kapitel 9, 3 in Kapitel 8, 9 in Kapitel 10. Das neue Skript
prüft **vor** dem Build und meldet nur, wo der Bestand einheitlich ist.

### Der Kreuzabgleich, dritte Bestätigung

Über drei Wellen: 44 · 101 · 90 gemeinsame Inhaltswortformen, davon
**19 echte Divergenzen** — und **keine einzige** hat ein Prüfskript gemeldet.
Die lehrreichsten:

- **Ein Einzelwort hatte den Plural seines Mehrwort-Eintrags übernommen.**
  In 5,12 trägt `in die Hand geben` zu Recht das idiomatische französische
  *entre les mains*; das Einzelwort `Hand` stand daneben ebenfalls auf *mains*,
  obwohl der Text Singular hat und der Bestand 535 zu 589 auf *main* steht.
- **`Fest der ungesäuerten Brote`** steht 15-mal im Bestand, ausnahmslos auf
  *loaves · panes · pains · pani*. Esra 6,22 war das sechzehnte und stand auf
  *bread*. Gefunden hat es `ausreisser.py`, nicht der Kreuzabgleich.
- **`verlassen`** stand im selben theologischen Sinn dreifach (*forsake* ·
  *abandoned* · *forsaken*), obwohl es/fr/it überall dieselbe Wortfamilie
  tragen und nur Englisch spaltete.
- **`Dies`** als Listeneinleiter stand auf *Ceci* und *Voici*. Entschieden hat
  die LSG selbst: sie schreibt an beiden Stellen *voici*.

### Ein wortgleicher Block, der nicht übertragbar ist

`Esra 5,14` und `6,5` teilen einen **18-Token-Block bei Versatz 0**, der vorab
gebunden war und deckungsgleich herauskam. Das Prüfskript von Kapitel 5 fand
aber einen **dritten** gemeinsamen Block, den weder mein Prompt noch die
Tabelle nannte: `aus dem Tempel`, Versatz **−17**. Er ist wortgleich und
inhaltlich unübertragbar — in 6,5 nimmt Nebukadnezar die Gefäße *aus dem
Tempel in Jerusalem*, in 5,14 holt Kores sie *aus dem Tempel von Babel*.
**Zwei verschiedene Tempel.** Derselbe Fall wie 2Kön 9,21/9,27.

### Sechs Fassungen einer Formel über zwei gleichzeitige Kapitel

Die Hand-Formel steht sechsmal im Buch (7,6 · 7,9 · 7,28 · 8,18 · 8,22 ·
8,31), **keine zwei gleich**: `gütige` steht nur zweimal, `des HERRN` in der
Hälfte, die Stellung von `war` wechselt. Und der Unterschied ist nicht nur
Stellung — in 7,6 und 7,28 ist das Possessiv Apposition zu `des HERRN`
(*his*), in 7,9 Genitivattribut zu `Hand` (*of his*). Beide Agenten haben ihre
drei Stellen einzeln vermessen; `Hand` trägt überall dieselbe Glosse, das
Drumherum nicht.

### Zwei Rechenproben gehen nicht auf — beide sind Erbe der Vorlage

1,11 nennt 5400 gegen 2499 aufgezählte, 2,64 nennt 42 360 gegen rund 29 400.
Der Agent von Kapitel 2 hat den **unmodernisierten Luther 1912** Zeile für
Zeile gegengelesen: **alle 45 Zahlangaben identisch**. Dazu liest l1912mod in
2,24 `240`, wo WEB, RV, LSG und RIV alle 42 haben. Gemeldet, nicht korrigiert.

### Homographen: Lemma und Level werden geteilt, nur die Glosse trennt

Vier neue Fälle — `Hagab` (Personenname gegen die Heuschrecke aus 3Mo 11,22),
`Cherub` (Ortsname gegen den Engel, 44 Belege), `Ariel` (in 4Mo 26,17 ist
Areli, der Sohn Gads, gemeint), `Sarai` (in 10,40 ein Mann der Sippenliste,
im Bestand 16-mal Abrahams Frau). Alle vier nach der Konvention des Bestands
gelöst, die `Becher` (B1 als Kelch **und** als Name), `Lot` (A1 als Gewicht
**und** als Person) und `Mal` (A2 als Zeit **und** als Zeichen) schon
vorgeben. `buildbook.py` erzwingt es ohnehin: es gleicht Level je Lemma
korpusweit an.

### Prompt-Hinweise: die Quote bleibt hoch

Über zehn Kapitel wieder **weit über hundert** widerlegte Vorgaben. Die
lehrreichsten sind die, bei denen ein Agent, der dem Hinweis folgt, einen
strukturell tadellosen Eintrag mit der falschen Bedeutung produziert hätte:

| ich schrieb | der Text sagt |
|---|---|
| `wachte` sei von `aufwachen` (5,5) | von **`wachen`** — der Extrakt bietet nur `aufwachen` an |
| `riss … aus` sei ein trennbares Verb (9,3) | `aus` regiert `Kopf und Bart`, ist also **Präposition**; die Modernisierung hat das Objekt in eine PP umgebaut |
| `wie es bis heute der Fall ist` stehe zweimal | 9,15 sagt es **ohne `bis`** — ab dort alles um eine Position versetzt |
| 9,11–12 habe eine Parallele in 5Mo 7,3 / 23,7 | andere Konstruktion, andere Wortstellung; nur die **Lemma-Glossen** übernehmbar |
| `sodass` stehe in 4,24 | 4,24 hat `So`; damit entfällt die angekündigte Kollision ganz |
| `nannten` sei `benennen` (5,4) | heißt **mitteilen**, gegen die Bestandsmehrheit *named/llamaron* |
| die Absenderformel stehe dreimal voll da | 4,8 ist gekürzt, 4,23 die Kurzform — **vier verschieden gebaute Fassungen** |

### `des` vor `Euphrat` stand in drei Fassungen

Kapitel 7 hat gemeldet, dass die schon **gebauten** Kapitel 4 und 6
auseinanderlaufen — drei Lesarten in zwölf Einträgen. Sein grammatisches
Argument war schlüssig, der Bestand entscheidet aber anders und mit einem
direkten Präzedenzfall: 32 Belege nach `jenseits`, 5 nach `diesseits`,
darunter **1Kön 5,4 mit exakt derselben Wendung `diesseits des Euphrat`**.

**Offen und korpusweit zu entscheiden:** `diesseits` trägt die Präposition im
Glossentext (*a este lado de · de ce côté-ci de · di qua da*), `jenseits`
nicht (*al otro lado · au-delà · di là*). Im Lesefluss doppelt sich dadurch
bei `diesseits` die Präposition — 17 Einträge im ganzen Bestand.

### Nachzuziehende Bestandsbefunde

- **1Mo 30,35:** das Einzelwort `sonderte` trägt `lemma='aussondern'` **und**
  dieselbe Glosse wie sein Mehrwort-Eintrag. Fünfter Fall dieser Bauart.
- **2Kön 12,14 · 25,15:** `Becken` in einer Geräteliste, aber mit der
  Meer-Lesart. Nach dem Zug die **Nachbarpositionen** mitprüfen — das Genus
  wechselt.
- **`sodass`** steht 364 zu 3 auf en *so that*; die drei Ausreißer sind
  2Chr 36,22, 5Mo 26,19 und Jos 20,9. Esra 1,1 folgt der Parallele 2Chr 36,22.
- **`fragen nach`** existiert als zwei Lemmata (`fragen nach` 8, `nach fragen`
  2) für dieselbe Konstruktion.
- **`beistehen`** hat drei Lesarten nebeneinander (*stood by* · *support* ·
  *assist*) bei identischem Lemma und Level.
- **`aufschreiben`** verschluckt sein Einzelwort an fast allen Stellen; nur
  Richter 8,14 unterscheidet.

## Nehemia: was das Buch gelehrt hat

Fünf Wellen zu je drei gleichzeitig laufenden Kapiteln; Kapitel 7 ging nach
der 55-Verse-Regel von vornherein an zwei Agenten. Der Ertrag ist diesmal fast
ausschließlich **methodisch**, und der rote Faden ist derselbe wie in Esra: die
teuersten Fehler stehen im Prompt, nicht in der Arbeit.

### Die Ähnlichkeit ist bei Listen das falsche Maß — zweimal gelernt

`vorlage.py` suchte je Vers unabhängig den ähnlichsten Vers der Vorlage. Bei
einer Liste gleichgebauter Zeilen (`die Nachkommen von X: Zahl;`) trägt das
nicht: wenn Name **und** Zahl abweichen, ist der Rest der Zeile in **jeder**
anderen Zeile genauso ähnlich. Nehemia 7,15 (Binnui/648) bekam so Esra 2,4
(Sephatja/372) statt 2,10; ebenso 7,28. Gefunden hat es der Agent von 7,1–40.

Die Antwort ist eine **ordnungserhaltende Gesamtzuordnung** (Needleman-Wunsch
über die Ähnlichkeitsmatrix), die keine Zeile überspringen kann, um eine
zufällig ähnlichere weiter hinten zu greifen. Wo beide Verfahren übereinstimmen,
ist die Zuordnung belastbar; wo nicht, steht eine **WARNUNG** samt Wortlaut und
Einträgen der Gegenkandidatin. In Nehemia 7 sind das genau sieben Stellen — die
drei Fehlzuordnungen und die vier Verse der echten Umstellung
(7,22 · 23 · 24 · 25 ↔ Esra 2,19 · 2,17 · 2,18 · 2,20). Entscheiden kann das
kein Verfahren; das Skript benennt jetzt, **wo** entschieden werden muss.

**Und dann bin ich selbst darauf hereingefallen** — nachdem der Fehler behoben
war. Für den Prompt von Kapitel 11 hatte ich jeden Vers gegen den ganzen
Bestand abgeglichen und nach Ähnlichkeit sortiert; der Agent hat zwei von acht
Zuordnungen gemessen widerlegt. Nehemia 11,7 hat gegen 1Chr 5,14 die
Ähnlichkeit **0,57**, teilt mit ihr aber nur `Dies sind die`. Gegen 1Chr 9,7
liegt sie bei **0,44**, der gemeinsame Block ist aber
`Benjamins: Sallu, der Sohn Mesullams, des Sohnes` — sieben Tokens, die es so
nur dort gibt.

**Bei Genealogien misst die Ähnlichkeit die Gattung, der lange Block die
Stelle.** Daraus ist `parallelen.py` entstanden: es durchsucht den ganzen
Bestand und sortiert nach der Länge des längsten gemeinsamen Blocks. Der erste
Lauf über Kapitel 11 reproduziert unabhängig genau die zwei Korrekturen.

### Ein Prüfskript, das an den bekannten Fällen nicht anschlägt, ist nicht geprüft

Das Muster „**Einzelwort übernimmt den Numerus seines Mehrwort-Eintrags**" war
seit Esra 5,12 bekannt und trat in Nehemia 9 dreimal wieder auf: `Hand` stand
französisch im Plural (*mains*), weil daneben `in die Hand geben` =
*livrer entre les mains* steht, während der deutsche Text Singular hat.
Gefunden wurde es jedes Mal nur zufällig — `selfcheck.py` und `qa.py` sehen es
prinzipiell nicht, `ausreisser.py` nur, wenn drei Sprachen sich einig sind.

`mehrwort.py` sucht es gezielt. Der Weg dahin ist die Lehre:

1. Die erste Fassung meldete **18 335** Stellen, fast alles Artikel und
   Präpositionen, deren Zielsprachenform legitim nach Genus und Kasus wechselt.
2. Auf Inhaltswörter und Flexionsvarianten der Korpusmehrheit eingeschränkt:
   34 Stellen.
3. **Gegenprobe:** die drei bekannten Nehemia-Fehler künstlich wiederhergestellt
   — das Skript meldete **null**. Die Enthaltensein-Prüfung lief auf
   Teilzeichenketten, und `main` ist eine Teilzeichenkette von `mains`; die
   Mehrheitsform galt damit als in der Wendung enthalten und der Treffer fiel
   weg. Seither prüft es auf Wortgrenzen.

Der Lauf über den Gesamtbestand fand **34 Stellen in acht Büchern** — 31-mal
`Hand`, dazu `Arm`, `Seite`, `Zeit`. Alle korrigiert, in Anno-Datei **und**
Quelle; Neubau byte-identisch.

**`--fix` gehört immer mit `--nur`.** Ein pauschaler Lauf korrigiert auch, was
richtig ist: `Ufer` in Josua 3,15 ist im Deutschen wirklich Plural („trat über
seine Ufer"), und `das Rechte` in 1. Johannes 2,29 ist ein anderes Wort als die
`Rechte` im Sinne von Rechtsansprüchen.

Was `mehrwort.py` **nicht** findet: den Fall, in dem die Wendung ein ganz
anderes Wort einsetzt — `Rücken` stand italienisch auf *spalle* aus *voltare le
spalle*, während die Mehrheit *schiena* ist. Das ist keine Flexionsvariante;
dafür ist `ausreisser.py` zuständig. **Die beiden Skripte decken zusammen alle
vier bekannten Fälle ab, einzeln keines.**

### Der eigene Kollisionslauf schlägt `hints.py` um Größenordnungen

`hints.py` blendet Funktionswörter aus, sonst ersäuft der Bericht im Rauschen.
Die Kehrseite ist in Nehemia viermal vermessen worden:

| Kapitel | `hints.py` | eigener Lauf des Agenten | davon echt |
|---|---|---|---|
| 8 | 0 | 3 | 3 |
| 10 | 0 | 10 | 10 |
| 11 | 0 | 18 | 3 |
| 12 | 1 | 18 | 4 |
| 13 | 4 | 49 | 4 |

Seit Kapitel 9 steht in jedem Prompt: **selbst einen Lauf über jeden Vers und
jede der vier Sprachen fahren.**

**Aber der Hinweis allein macht es schlimmer.** Der Agent von Kapitel 11 bekam
18 Meldungen und hätte fast alle aufgelöst — bis er sie gegen den Bestand
nachzählte: `nach` und `zu` teilen sich englisch *to* in **200** fertigen
Versen, `auf` und `in` teilen sich spanisch *en* in 181, `aus` und `von` teilen
sich spanisch *de* in 208, `ihr` und `sein` teilen sich *su* in 129. Die
Zielsprachen verschmelzen diese Präpositionen und Possessiva; eine Sonderlösung
in einem Kapitel macht den Bestand nur inkonsistent.

Seither steht die Zählregel im Prompt, und sie wirkt: Kapitel 12 ließ **alle
18** Meldungen stehen (niedrigste Bestandszahl 13, höchste 571), Kapitel 13
löste **4 von 49** auf — und zwar genau die, für die der Bestand **null oder
eine** gemeinsame Stelle kennt.

### Kollisionen werden verse-lokal aufgelöst, nicht lemma-weit

`Winkel` und `Ecke` kollidieren in 3,24 echt. Der Agent löste es lemma-weit —
das hätte `Ecke` gegen 23 Bestandseinträge gespalten. Umgedreht: `Winkel`
bekommt als **eigenes Sachfeld** die Bauwinkel-Lesart (*angle · ángulo ·
angle · angolo*), die zwei Bestandsbelege in 2Kön 10,21 und 19,23 meinen den
*Nischen*-Winkel und bleiben; die Ausweichglosse für `Ecke` gilt nur im
Kollisionsvers. Das ist die Regel aus 1Tim 4,2: eine Auflösung gehört an die
Kollisionsstelle, nicht ans Lemma. Ebenso gehandhabt in 6,1, 6,9, 6,13, 7,3,
10,32, 10,35, 12,37, 13,11, 13,17, 13,25.

### Ein Negativbefund ist auch ein Befund

Nehemia 9 erzählt die ganze Heilsgeschichte nach — Schöpfung, Abraham, Ägypten,
Schilfmeer, Sinai, Manna, Wüste, Landnahme. Es liegt nahe anzunehmen, dass es
den Pentateuch wörtlich aufgreift. Ein Abgleich **jedes** der 37 Verse gegen
1.–5. Mose, Josua und Esra findet genau **einen** Treffer über 0,40: 9,18 gegen
2Mo 32,4, das goldene Kalb. Das stand so im Prompt — und hat genau den Reflex
verhindert, hier aus Bibelkenntnis abzuschreiben. Der Agent hat den Scan
zusätzlich über den **gesamten** Bestand laufen lassen und einen zweiten
Treffer gefunden, den meine Einschränkung nicht sehen konnte: 9,36 gegen
2Chr 6,31.

Dasselbe bei den Kapiteln 12 und 13: 18 Verse teilen einen Fünf-Token-Block mit
irgendeiner Bestandsstelle, aber alle Ähnlichkeitswerte liegen zwischen 0,16
und 0,38. Das sind wiederkehrende Wendungen, keine Parallelstellen — es gibt
nichts abzuschreiben.

### Die Dublette formuliert neu, und die Falle liegt daneben

Der Agent von Kapitel 12 hat die zwei Dankchöre (12,31–37 und 12,38–39)
vermessen: von fünf geprüften Verspaaren teilt genau eines einen Block (fünf
Tokens der Mauerformel), alle übrigen keinen ab Länge drei. **Die Falle liegt
eine Position vor dem Block:** in 12,31 steht `oben` zweimal mit zwei Lesarten
— „oben auf die Mauer steigen" (*up*) und „oben auf der Mauer" (*on top*). Wer
den gemeinsamen Block abschreibt, ohne die Verse zu lesen, setzt an der ersten
Stelle die falsche.

Ebenso die Schlussformel des Buches. `Denk mir zugute, mein Gott!` steht
viermal (5,19 · 13,14 · 13,22 · 13,31) und ist viermal anders gebaut: 13,31
gegen 5,19 teilt vier Tokens, 13,14 gegen 5,19 nur drei Zweierblöcke, und
13,14 gegen 13,22 hat bei Ähnlichkeit **0,07** keinen Block. Vier verschiedene
Mehrwort-Lemmata über vier Stellen — wer abgeschrieben hätte, hätte drei davon
falsch.

### Die Agenten bauen bessere Prüfskripte, als der Prompt verlangt

Beide Hälften von Kapitel 7 haben unabhängig voneinander einen **Zahlwort-
Parser** gebaut: er liest jedes deutsche Zahlwort in eine Zahl, **erzeugt**
daraus die Zahlwörter der vier Zielsprachen und hält sie gegen die gelieferte
Glosse — samt spanischer Genusprobe (*doscientas* Maultiere gegen *doscientos*
Sänger), italienischer Elision (*centottantotto*) und Endbetonung
(*settecentoquarantatré*). 55 Zahlwörter geprüft, davon 22 mit von Esra 2
abweichender Summe. **Beide Skripte haben dabei je einen Fehler im eigenen
Generator aufgedeckt, keinen in den Daten.**

Das ist die Antwort auf ein Problem, das keine Strukturprüfung lösen kann: die
abweichenden Summen stehen als **ausgeschriebene Zahlwörter** da
(`zweitausendachthundertzwölf` gegen `zweitausendachthundertachtzehn`), und
keine Ziffernprüfung fängt sie.

### `um zu` fällt durch, wenn man es nicht ausdrücklich prüft

In Welle 2 haben zwei von drei Agenten den Mehrwort-Eintrag `um zu` vergessen
— viermal insgesamt. Ein fehlender Mehrwort-Eintrag ist für `selfcheck.py` und
`qa.py` **prinzipiell unsichtbar**: die Einzelwörter sind vollständig und
richtig, strukturell fehlt nichts. Der `konvention.py`-Lauf steht seither als
Pflichtschritt in `AUFTRAG_AT.md`.

Und `konvention.py` selbst hatte einen Fehler: bei zwei Vorkommen desselben
Einleitworts paarte es das erste mit dem `zu` des **nächsten** Teilsatzes. In
Neh 6,10 (`um dich umzubringen – nachts … um dich zu töten`) meldete es
dadurch eine Lücke, die es nicht gab. Die Vorwärtssuche bricht jetzt an einem
zweiten Einleitwort und an alleinstehenden Satzzeichen ab; Gegenprobe an
entkernten Kontrolldateien: alle sieben echten Lücken werden weiterhin
gefunden.

### `hints.py` meldet Präfixverben falsch als unbelegt

Viermal nachgewiesen: `herunterkommen` und `hinabziehen` (6,3), `dafür sorgen`
(7,1), `sich absondern` (10,29). Der VERWANDT-Abschnitt führt bei trennbaren
und Präfixverben auf `herum`, `hinab`, `Sorge` statt aufs Lemma. Aufgedeckt hat
es jedes Mal **nur `levelcheck.py`**. Steht seit Welle 3 in jedem Prompt.

### Prompt-Hinweise: die Quote bleibt hoch

Wieder weit über hundert widerlegte Vorgaben. Die lehrreichsten:

| ich schrieb | der Text sagt |
|---|---|
| `Rosstor` sei neu | steht im Bestand, C1 (Neh 3,28 hatte es aus einer anderen Form) |
| `Ephraimtor` sei neu | steht in 2Kön 14,13 und 2Chr 25,23, B2 |
| in 3,5 kollidierten `Vornehme`/`Vorgesetzte` | tragen längst drei verschiedene Glossen |
| 1,8–9 habe keine Blöcke aus 5Mo 30 | **1,9 hat zwei** (`Ende des Himmels`, `von dort sammeln und`) |
| 12,35 teile `des Sohnes Michas` mit 11,22 | 12,35 liest **`Michajas`** — anderer Name, andere Glosse |
| 12,37 habe `Ophel` aus 3,26 | steht dort nicht; geteilt sind fünf Tokens |
| `anstimmen` und `Dankgebet` gehörten zu Kapitel 12 | stehen in 11,17 |
| 11,7 gehöre zu 1Chr 5,14 | gehört zu **1Chr 9,7** (Block 7 gegen Block 3) |
| `Hebopfer` stehe in Kapitel 10 | der Text hat dort `Abgaben` |
| die `und dass wir`-Formel stehe dreimal | zweimal; 10,33 beginnt anders |
| 13,15 habe fünf Warenwörter | **acht** Sachwörter |
| `Kaufleute` stehe in 13,20 | dort stehen `Händler und Verkäufer` |
| `zugute` habe drei Belege | **vier** — Neh 5,19 gehört dazu |

### Nachzuziehende Bestandsbefunde

Alle gesammelt in **`BEFUNDE_NEHEMIA.md`** im Werkzeugordner. Die wichtigsten:

- **`Tür` und `Tor` tragen im ganzen Bestand dieselbe romanische Glosse.** Eine
  korpusweite Kollision, in Nehemia dreimal verse-lokal aufgelöst (3,6 · 6,1 ·
  7,3). Eine saubere Lösung wäre die Trennung `Tor` = *portón/portail/portone*
  gegen `Tür` = *puerta/porte/porta*.
- **`Josabad` trägt in allen 12 Belegen englisch *Jehozabad*, romanisch aber
  *Jozabad*.** Das Hebräische hat beide Namen, das Deutsche schreibt überall
  `Josabad`. Entweder die englische Spalte auf die Mehrheit ziehen oder
  positionsgebunden trennen wie bei `Assur` und `Lot`.
- **`Hosea` trägt für Josuas Vorname und den Propheten dieselbe englische
  Glosse.**
- **`Rind` und `Vieh`** tragen beide *cattle/livestock · ganado · bétail ·
  bestiame`; in 10,37 stehen sie im selben Vers.
- **`Vorsteher` und `Oberhaupt`** sind in es/fr/it identisch (*jefe · chef ·
  capo*) — latente Bindungsschwäche.
- **Die spanischen Tornamen sind uneinheitlich großgeschrieben:** acht heißen
  `puerta del …` klein, nur `Schaftor` heißt `Puerta de las Ovejas` groß (aus
  der Bindung an Joh 5,2).
- **`hilfsverb.py alle` meldet 35 Fälle**, alle in älteren Büchern; mindestens
  2Mo 8,3 ist eindeutig echt (`ließen` und `machten` mit derselben Glosse in
  drei Sprachen).

## Ester: was das Buch gelehrt hat

Drei Wellen, zehn Kapitel, 167 Verse. Ester ist das erste Buch, das **fast
keine Parallelen** hat — und dadurch ist der Ertrag fast ganz methodisch. Zwei
Regeln sind entstanden, zwei Werkzeugfehler behoben, und einer der beiden
Fehler war meiner.

### Die Glossen folgen den vier Referenzausgaben

Diese Regel stand nirgends, obwohl sie 43 Bücher lang befolgt worden ist. Ein
Agent hatte in Nehemia gemeldet, `Susa` trage englisch das archaische
*Shushan* neben modernen romanischen Formen, und ich hatte das als
Korrekturkandidaten notiert. Weil Ester `Susa` 17-mal führt und die
Entscheidung vor dem Buch fallen musste, habe ich die Ausgaben aufgeschlagen:
**WEB schreibt „Shushan the palace" (Est 1,2)**, LSG *Suse*, RIV *Susa*,
RV1909mod *Susa*. Die Vierergruppe gibt jede Ausgabe korrekt wieder. Der
Befund war ein Fehlalarm, und meine Notiz war falsch.

Seither steht in `AUFTRAG_AT.md`: **die Glossen folgen WEB · RV1909mod ·
LSG1910 · RIV1927, nicht einem einheitlichen Modernitätsgrad.** Eine Sprache,
die altertümlich wirkt, ist kein Befund, solange ihre Ausgabe es so schreibt.
Ein echter Befund ist nur, wo eine Sprache von **sich selbst** abweicht.

Die Regel hat sofort getragen: **`Sethar` steht in Ester 1,10 und 1,14 und
meint zwei verschiedene Personen.** WEB schreibt *Zethar* und *Shethar*, LSG
*Zéthar* und *Schéresch*. Die Ausgaben lösen einen Homographen auf, den das
Deutsche verschmilzt — ohne den Blick in die Quelle wäre der Name pauschal
einmal geglost worden. Dasselbe bei `Seres` (Hamans Frau, *Zeresh*) gegen den
`Seres` aus 1Chr 7,16 (der Bruder des Peres, *Sheresh*).

**Zwei Ausnahmen gehören dazu.** Erstens: wo die Schreibung der Ausgabe mit
einem Gemeinwort zusammenfällt und einen falschen Sinn setzt — WEB schreibt den
Kämmerer in 1,10 „Carcass", im Lesefluss stünde an einem Personennamen das
englische Wort für *Kadaver*. Dort gilt die Form der drei anderen Ausgaben.
Zweitens: wo eine Ausgabe selbst schwankt, entscheidet ihre Mehrheit — WEB
schreibt `Susa` im selben Buch teils *Shushan*, teils *Susa*; LSG schreibt
`Hegai` zweierlei; RIV hat in Kapitel 2 zwei Setzfehler (*cimei* für Simei,
*ettimo* für settimo) und schreibt `Bigthan` einmal *Bightan*.

### Die Ausgabe liefert den Namen, der Bestand die Bedeutung

Die neue Regel hatte eine offene Flanke, und drei Fälle haben sie erzwungen:
`Tharsis` (die Ausgaben uneinheitlich, der Bestand gebunden), `Pracht` (WEB
*glory* gegen die Ester-1,4-Festlegung *splendor*), `Zahl` (RV *cantidad* an
dieser einen Zeile gegen 92:1 *número* im Bestand).

Die Grenze steht jetzt in `AUFTRAG_AT.md`: **die Ausgabe entscheidet, wo der
Bestand schweigt oder nicht antworten kann** — neuer Name, Homograph, Wendung
ohne Beleg. **Der Bestand entscheidet, wo er für ein gewöhnliches Wort eine
feste Bindung hat.** Eine Glosse ist ein Leseassistent, keine Zeilenwiedergabe:
wer `Zahl` zweiundneunzigmal als *número* gelesen hat, soll es nicht einmal als
*cantidad* sehen.

### Der Block hört auf, wo er aufhört

Der lehrreichste Fall des Buches steht in **7,2**: der Vers teilt mit 5,6 einen
Zwölf-Token-Block, der **genau bei `Selbst` endet**. Danach sagt 7,2 `das halbe
Königreich`, 5,6 `die Hälfte des Königreichs` — zwei deutsche Formulierungen
für dieselbe Sache, romanisch sogar mit verschiedenem Genus. Das Prüfskript des
Agenten hat deshalb nicht nur die Blockgleichheit geprüft, sondern ausdrücklich
das **erste Token nach dem Blockende auf Verschiedenheit**. Das gehört in jedes
Blockprüfskript.

Die Gegenprobe steht in **7,4 gegen 3,13**: Ähnlichkeit **0,07**, kein Block ab
drei Tokens, obwohl beide Verse dieselben drei Vernichtungswörter tragen.
`vernichten, töten und umbringen` gegen `vernichtet, getötet und umgebracht` —
nur die Lemma-Glossen sind übertragbar.

Ebenso in Kapitel 6: die **Ehren-Formel steht in zwei Fassungen** (`den der
König gerne ehren möchte` gegen `den der König ehren will`), innerhalb jedes
Paars deckungsgleich, zwischen den Paaren nicht. Der Agent hat beim Nachzählen
im Quelltext außerdem gefunden, dass die zweite Fassung **dreimal** steht —
`bloecke.py` meldet nur Paare.

### Mein eigener Prozessfehler

Für die Wellenbriefings habe ich die Blöcke mit `bloecke.py` vermessen, aber
die **Verspaare von Hand ausgewählt**. Für Ester 8 nannte meine Tabelle fünf
Blöcke. Der Agent hat `parallelen_ch8.md` gelesen — die Datei, die ich selbst
erzeugt hatte — und **siebzehn** gefunden, darunter den längsten des Kapitels:
**8,13 ← 3,14, Länge 19, Ähnlichkeit 0,74**, der ganze Versanfang wörtlich.

**Regel für kommende Bücher:** das Wellenbriefing wird aus `parallelen.py`
**abgeschrieben**, nicht aus geratenen Verspaaren zusammengestellt.
`bloecke.py` ist für die Nachmessung eines bereits bekannten Paares da, nicht
für die Suche.

### `vorab.py` führte bei Eigennamen aktiv in die Irre

Die Tabelle schlägt die Bestandslesart einer **Wortform** nach und weiß nicht,
ob derselbe Träger gemeint ist. Für `Seres` bot sie *Sheresh* mit einem Beleg
an — der Beleg ist 1Chr 7,16, der Bruder des Peres. Jede großgeschriebene Zeile
trägt jetzt einen Warnhinweis **mit Belegstelle**: `Seres | … | 1 ⚠ 1. Chronika
7,16`. Die bloße Zahl ist bei einem Eigennamen wertlos.

### Der Level-Abgleich las die Mehrheit aus dem falschen Stand

Der schwerwiegendste Werkzeugfehler des Buches, aufgedeckt an einem Befund des
Ester-9-Agenten: `vierzehnt` stand in allen 22 Belegen auf **B1**, während die
ganze Zehnerklasse (`elft` bis `zwanzigst`) **A2** trägt. Uniform in sich und
deshalb von `levelcheck.py` nicht zu finden — das meldet nur, wo ein *Kapitel*
von einem einheitlichen Bestand abweicht.

Der Versuch, es mit `remap.py` zu ziehen, blieb wirkungslos. **Durchgang 2 des
Level-Abgleichs in `buildbook.py` bestimmte die Korpusmehrheit aus den
gebauten Dateien der anderen Bücher.** Wer ein Level in allen 22 Quellen
ändert, bekommt beim Bauen des ersten Buches die 42 noch nicht gebauten als
alte Mehrheit entgegen — und die Änderung zurück. Bei jedem Buch, in jeder
Reihenfolge, beliebig oft wiederholt. **Eine korpusweite Levelkorrektur über
die Quellen war damit prinzipiell unmöglich.**

Die Mehrheit kommt jetzt aus den **Kapitelquellen**. Die Quelle ist der
bearbeitete Stand und damit die Autorität; die gebaute Datei ist ihr Ergebnis.

Der Neubau aller 44 Bücher änderte 32 Einträge in 19 Dateien — und legte
dabei eine **Regression** frei, die zu genau diesem Fehler gehört: `Kidron` in
Johannes 18,1 stand italienisch in der Quelle auf *Kidron*, in der gebauten
Datei auf *Cedron*. Eine Korrektur hatte also nur in der gebauten Datei gelebt.
Beide Stände waren falsch: RIV schreibt an allen acht alttestamentlichen
Stellen *Kidron* und in Johannes 18,1 ***Chedron***, weil es dort dem
griechischen Κεδρών folgt — die Ausgabe unterscheidet selbst zwischen AT und
NT.

### Der eigene Kollisionslauf, vierte Bestätigung

| Kapitel | `hints.py` | eigener Lauf | davon echt |
|---|---|---|---|
| 1 | 1 | 17 | 1 |
| 2 | 2 | 58 | 4 |
| 3 | 0 | 34 | 3 |
| 4 | 1 | 25 | 2 |
| 5 | 2 | 11 | 4 |
| 6 | 1 | 10 | 0 |
| 7 | 1 | 15 | 1 |
| 8 | 1 | 33 | 5 |
| 9 + 10 | 3 | 57 | 15 |

**Echt sind durchweg die mit null bis sechs gemeinsamen Bestandsversen.** Die
Zählregel trägt: kein Agent hat mehr eine korpusweite Konvention aufgelöst.

### Nachzuziehende Bestandsbefunde

Gesammelt in **`BEFUNDE_ESTER.md`**. Die wichtigsten:

- **`herrschen` hat keine saubere „regieren"-Lesart.** Die romanische
  Kombination *reinaba · régnait · regnava* hängt durchgehend an englisch
  ***prevailed*** (10 Belege, alle „Hungersnot herrschte").
- **`begehen`, `ausfallen`, `zutragen`, `bedrohen`, `lagern`, `wandeln` sind
  bedeutungsverschoben** — der Bestand kennt jeweils nur die andere Lesart.
- **Die niedrigen Ordinalia sind weiter uneinheitlich** (`sechst` A2 gegen
  `siebt` und `acht` A1); dort mischen sich Kardinal- und Ordinalhomographen.
- **`kleiden` steht auf B2, `sich kleiden` auf B1.**


## Hiob: was das Buch gelehrt hat

42 Kapitel, 1070 Verse, das erste Buch der Poesie — und das erste, das **fast
ohne Vorlagen** auskommen musste. `parallelen.py` findet für Kapitel 3, 4, 5,
10, 14, 16, 17, 23, 24, 26, 27, 29, 30, 31, 35, 39 und 41 **null** Verse mit
einem gemeinsamen Block ab fünf Tokens im gesamten übrigen Bestand. Der
gesamte Ertrag kam aus dem Lexikon-Extrakt, den vier Referenzausgaben und der
buchinternen Konsistenz.

### Der teuerste Fehler: eine Ausweichlesart wandert weiter

Das ist **sechsmal** passiert und musste jedes Mal zurückgezogen werden:

| Wort | erfunden in | weitergereicht nach |
|---|---|---|
| `würde` (*starei per*) | 3,13, als Ausweichlesart gegen `hätte` | 5,8 · 6,10 · 6,27 · 6,28 |
| `nur` (*Solamente · Soltanto*) | 1,15, gegen `allein` | zwölf Einträge in sieben Kapiteln |
| `Grab` (*grave · sepultura*) | 5,26, ein Beleg im Gesamtbestand | 10,19 |
| `sodass` (it *sicché*) | Kapitel 5 | 5,12 · 5,16 · 5,21 |
| `doch` (*aun así · pure*) | zwei Belege | 9,31 · 10,16, von zwei verschiedenen Agenten |
| `Seufzen` (*sighing*) | 23,2, ohne Kollisionsgrund | — rechtzeitig gemeldet |
| `Unrecht` (en *injustice*) | 5,16, nur im Englischen | — |

**Der Grund ist strukturell, nicht menschlich.** `lexicon.py` zieht aus *allen*
vorhandenen Anno-Dateien, also auch aus den frisch gebauten Kapiteln des
laufenden Buches. Was ein Kapitel entscheidet, sieht das nächste als Bestand —
ohne zu sehen, dass es eine Auflösung für genau einen Vers war.

Dagegen sind vier Maßnahmen entstanden, in dieser Reihenfolge:

1. **Die Kollisionskarte** (`BUCHKOLLISIONEN.md`), vor dem ersten Kapitel über
   den ganzen Quelltext ausgezählt: 17 Bedeutungsgruppen, 87 Kollisionsverse.
   Sie sagt **vorher**, wo aufgelöst werden muss — und vor allem, wo nicht.
2. **Die Prompt-Warnung** mit den gemessenen Zahlen.
3. **`zweigleisig.py`**, das den Fehler hinterher findet.
4. **Die Tabelle der versgebundenen Lesarten** am Ende der Wortfeld-Datei —
   nachdem sich herausstellte, dass das Dokument selbst den Fehler enthielt.

### Die Kollisionskarte hat sich bezahlt gemacht — und acht Fehlalarme produziert

Der Ertrag ist, dass sie **begrenzt**: `Frevler` und `Gottloser` stehen zusammen
in 31 Versen, berühren sich aber im ganzen Buch **genau einmal**, in 20,5. Die
Löwenwörter kollidieren nur in 4,10 und 4,11, die Zorn-Gruppe **nie**. Vier
Kapitel haben 20,5 bewusst offengelassen und die Auflösung dorthin verwiesen;
als der Vers drankam, lagen beide Bindungen fertig da. Dasselbe bei 12,4
(`rechtschaffen` ↔ `untadelig`) und bei 16,11 und 27,7, die ein Agent gefunden
hat, **bevor** sie annotiert wurden.

Der Preis: **acht formbasierte Fehlalarme** (11,8 · 12,13 · 13,22 · 21,28 ·
23,5 · 24,1 · 29,3 · 29,14). Die Karte findet Wortformen, keine Wortarten —
`Tiefer` ist in 11,8 der Komparativ des Adjektivs, `Gerichtszeiten` in 24,1 ein
Kompositum. Jeder Treffer gehört am Vers angesehen.

### Der Konjunktiv II — und ein Konflikt in der Werkzeugkette

Der Bestand löst `würde` überwiegend periphrastisch (*iba a · allait · stava
per*). Das ist Futur-im-Vergangenen und sagt beim Irrealis der Gegenwart das
Falsche: *starei per mentire* heißt „ich bin im Begriff zu lügen".

**Die geltende Regel** (aus 1. Mose 42,38, wo `würdet` = *llevaríais ·
conduiriez · condurreste* neben `bringen` = *llevar · conduire · condurre*
steht): bei echtem Irrealis trägt das Hilfsverb den **Konditional des
Vollverbs**, das Vollverb bleibt Infinitiv, Englisch bleibt *would*. Bei echtem
Futur bleibt die Periphrase richtig. Kapitel 11 hat die Regel präzisiert:
innerhalb des Irrealis entscheidet **Vorder- gegen Nachsatz** — Protasis
Imperfekt-Konjunktiv, Apodosis Konditional. Kapitel 13 lieferte den Prüffall:
dasselbe Verb `schweigen` in beiden Rollen, in 13,5 und 13,19.

**`hilfsverb.py` führte genau dieses Muster als Fehler** und hatte zwei Stellen
in die Gegenrichtung korrigiert. Nachgeprüft war der Bestand von Anfang an
gespalten: 1. Mose 42,38 und 44,34 tragen den Konditional und sind nie
umgestellt worden — 42,38 nur deshalb nicht, weil der Abstand elf Tokens
beträgt und das Suchfenster acht war. Aufgelöst zugunsten des Konditionals;
1. Mose 19,19 und 1. Korinther 14,25 sind zurückgezogen, das Werkzeug trennt
die `werden`-Treffer jetzt als erwartete Bauform ab.

**Die Gegenprobe steht in 5,26**: dort stand `wirst` periphrastisch als *vas a*
vor dem Passivpartizip `getragen` — „vas a llevado" ist kein Spanisch. Der
Kapitel-22-Agent hat seinen eigenen Fall richtig gelöst und die ältere Stelle
gemeldet, statt sie nachzuahmen.

### Die Verszählung der Gottesreden läuft auseinander

**Der gefährlichste Befund des Buches, weil er lautlos ist.** In den Kapiteln
38 bis 41 zählen die vier Referenzausgaben **alle vier verschieden**:

| Kapitel | l1912mod | WEB | RV1909mod | LSG1910 | RIV1927 |
|---|---|---|---|---|---|
| 38 | 41 | 41 | 38 | 38 | 41 |
| 39 | 30 | 30 | 30 | 38 | 30 |
| 40 | 32 | 24 | 19 | 28 | 24 |
| 41 | 26 | 34 | 34 | 25 | 34 |

Deutsch 39,N = RV/LSG 39,N+3 · deutsch 40,N = RV/LSG 40,N−5 · deutsch 41,N =
WEB/RV/RIV 41,N−8 und LSG 41,N+1. **Deutsch 41,1 ist in keiner Ausgabe 41,1.**
RV zieht am Ende von Kapitel 39 vier deutsche Verse in einen einzigen zusammen.

Wer die Ausgabe über die Versnummer aufschlägt, bekommt einen versetzten Satz
aus derselben Tierreihe — thematisch ähnlich genug, dass die falsche Glosse
plausibel aussieht und durch jede Prüfung läuft. `VERSZAEHLUNG_38_41.md` hält
die Messung fest und verlangt, in diesen vier Kapiteln **über den Inhalt**
aufzuschlagen. RIV1927 druckt die alte Zählung übrigens selbst mit
(`41,1 | (40:25)`) und ist damit der beste Anker.

### Der Quelltext schlägt die Ausgabe — durchgehend

Der l1912mod formuliert an über sechzig Stellen bewusst anders als alle vier
Ausgaben, und die Linie ist ohne Ausnahme durchgehalten worden:

- **Metaphern werden nicht wiedereingeschleppt.** `tiefes Dunkel` (3,5) gegen
  „Schatten des Todes", `Verderben` und `Grab` (33,18 ff.) gegen „Grube",
  `Nilpferd` und `Krokodil` (40,15 · 40,25) gegen Behemot und Leviatan — wobei
  LSG und RIV dort **selbst** die Gemeinwörter schreiben.
- **Das Idiom bleibt beim Deutschen.** 19,20 „dem Tod von der Schippe
  gesprungen" ist unbelegt, und die vier Ausgaben lesen es *auch nicht*
  wörtlich, sondern mit ihrem eigenen Idiom. Der Agent hat die Einzelwörter
  wörtlich glossiert und die Wendung als Mehrwort geführt.
- **Bei Eigennamen entscheidet die Ausgabe, bei gewöhnlichen Wörtern der
  Bestand.** Die drei Töchternamen in 42,14 sind der `Carcass`-Fall in
  Reinform: RIV *übersetzt* sie (*Colomba*, *Cassia*, *Cornustibia*), also gilt
  die Form der drei anderen.

### Homographen: dreimal gefährlich, dreimal abgefangen

`Rahab` (9,13 · 26,12) ist das Meeresungeheuer, im Bestand aber neunmal die
Frau aus Jericho, italienisch *Raab*. Die Ausgaben unterscheiden die beiden —
nur nicht in 9,13, wo drei von vieren umschreiben; der Beleg steht in
Jesaja 51,9. `Bus` (32,2) trug in der Bestandszeile die **Kasuspräposition
schon in sich** (*of Buz*), während der l1912mod `von Bus` mit eigenem Token
schreibt. Bei `Ram` wäre die Matthäus-Zeile (*Aram*) die Falle gewesen. Dazu
`Tor` (Narr/Stadttor), `Falle` (Substantiv/Imperativ), `Würde`
(Substantiv/Konjunktiv), `Freie`, `Keule`.

### `lexicon.py` und `hints.py` melden zu viel — gemessen

Die „unbelegt"-Liste war in **jedem** Kapitel überwiegend falsch: Hiob 24 elf
von zwölf, Hiob 23 fünf von fünf, Hiob 38 zu 87 %, Hiob 39 zu 60 %, Hiob 40 zu
55 %. Die Ursache im Sortieralgorithmus ist behoben (siehe `hints.py`), die
Ablautlücke bleibt prinzipiell.

**Zwei weitere Lücken sind erst in Hiob sichtbar geworden:**

1. **Der Extrakt zeigt nur die Lesarten der im Kapitel vorkommenden Wortform.**
   In Kapitel 15 bot er für `Schild` nur *breastpiece* an, obwohl der Bestand
   38 Belege für *shield* hat; in Kapitel 20 für `Spitze` nur *forefront*.
2. **Bei getrennt stehenden trennbaren Verben findet er das Mehrwort-Lemma
   nicht.** `vordringen`, `heranreichen`, `gleichkommen`, `anhäufen`,
   `losfahren` standen alle im Bestand und waren unsichtbar. **`levelcheck.py`
   hat sie gefunden**, in den Kapiteln 32, 34 und 38 je eines.

Die Kapitel 39 und 41 haben daraus die richtige Konsequenz gezogen und sich
**Sweep-Skripte** geschrieben, die *jede* Mehrwort-Wendung des Bestands im
Quelltext suchen — nicht nur die feste Liste von `konvention.py`. Sie fanden
zusammen dreizehn echte Lücken. **Das gehört als `sweep.py` in die Kette**;
diese Fehlerklasse ist für `selfcheck.py` und `qa.py` prinzipiell unsichtbar.

### Wo die Kollisionsregel gegen sich selbst arbeitet

Genau einmal: `Bedrängnis` und `Not` tragen im AT-Bestand **in allen vier
Sprachen dieselbe Glosse**, und sie stehen in 36,15 · 36,16 · 36,19 in drei
benachbarten, nie aber im selben Vers. Die strikte Regel hätte dort zweimal
dieselbe Glosse für zwei verschiedene deutsche Wörter erzeugt. Die
15,24-Ausweichlesart ist deshalb zur **Buchlesart** erhoben worden.

Die Regel bleibt richtig — aber sie ist eine Regel über *Verse*, und wo ein
Leser drei Verse am Stück liest, greift sie zu kurz.

### Zahlen zum Verfahren

Ein Agent pro Kapitel, zwei bis drei gleichzeitig, jedes Kapitel unabhängig
validiert und einzeln committet. **Ein Ausfall** (Kapitel 31, Verbindungsabbruch
vor dem ersten Vers, sauber neu angesetzt). Der **eigene Kollisionslauf** der
Agenten fand in jedem Kapitel mehr als `hints.py` — zwischen zwei und acht
Paare, in Kapitel 5 acht bei null gemeldeten. Er ist nicht optional.

Und die Prompts selbst waren die häufigste Fehlerquelle: in mindestens zwölf
Kapiteln hat ein Agent eine meiner Angaben am Quelltext widerlegt — falsche
Verse, Verb statt Substantiv, Person statt Abstraktum, Wörter, die gar nicht
vorkommen. **Der Hinweis „lies den Quelltext, nicht meine Aufzählung" gehört in
jeden Prompt.**

## Sprüche: was das Buch gelehrt hat

Das Buch ist in **elf Paketen** entstanden — Kapitel 1 allein als Maßstab,
danach zehn Dreierwellen. 915 Verse, 14 019 Einträge, 659 Mehrwort-Einträge.

### Die Kollisionsliste von `hints.py` ist zu einem Fünftel falsch

Erstmals ist die Meldung eines Werkzeugs über ein ganzes Buch hinweg
ausgezählt worden. `hints.py` hatte **30 Kollisionspaare** gemeldet; **sechs
davon sind Fehlalarme**, jeder von einem Agenten am Quelltext widerlegt:

| Stelle | was `hints.py` sah | was dasteht |
|---|---|---|
| 4,16 | `Schlaf` / `schlafen` | Verb und Stammsubstantiv, Zusammenfall nur im Englischen |
| 4,27 | `ab` / `fern` | `ab` ist die Partikel von `abweichen` |
| 9,8 | `Weiser` / `weise` | zwei **Imperative von `weisen`** — die Klammerhälften von `zurechtweisen` |
| 10,14 | `heran` / `nahe` | `heran` ist die Partikel von `heranbringen` |
| 19,25 | `klug` / `weise` | wieder `weisen`, kein Adjektiv |
| 22,29 | `Leute` / `Mensch` | `Mensch` steht im Singular |

**Vier der sechs sind Partikeln trennbarer Verben oder Verbformen, die wie ein
Adjektiv aussehen** — genau die Klasse, vor der `AUFTRAG_AT.md` unter
„Partikeln selbst nachzählen" warnt. Das Werkzeug ist formbasiert und kann sie
prinzipiell nicht sehen.

Dem stehen **mindestens 25 echte Kollisionen** gegenüber, die `hints.py`
prinzipiell **nicht** sehen konnte. In mehreren Kapiteln (11 · 23 · 24 · 26 ·
28) meldete es **null** Paare, während `glosskollision.py` und die Handprüfung
vier bis sechs echte fanden. Der eindrücklichste Fall steht in **23,29**, dem
dichtesten Vers des Buches (sechs Substantive in sechs Fragen): der Bestand
führt für `Leid` **auch** die Lesart *misery · miseria · misère · miseria* —
wortgleich mit `Elend` in allen vier Sprachen. `hints.py` vergleicht nur die
häufigste Lesart und konnte das nicht melden.

**Regel daraus:** `hints.py` ist eine Hypothesenliste, kein Prüflauf. Der
Prüflauf ist `glosskollision.py`, und er gehört an das **fertige** Kapitel.

### `levelcheck.py` gehört in die Pflichtliste — aus einem anderen Grund als vermutet

Es prüft Level, findet aber dreimal etwas, das kein anderer Lauf melden konnte:
den Bestandsbeleg `Steinmauer` (Kap. 25), den der Lexikon-Extrakt formbasiert
nicht zeigte; das zusammengeschriebene `guttun` (Kap. 22), belegt als
`gut tun`; und in Kapitel 29 **drei Mehrwort-Lemmata**, die ein Agent als neu
angesetzt hatte und die längst im Bestand stehen. An allen drei Stellen waren
die fünf vorgeschriebenen Läufe mit 0 Treffern durchgelaufen.

Der Agent von Kapitel 29 hat das selbst vorgeschlagen; `AUFTRAG_SPRUECHE.md`
führt seither sechs Pflichtläufe.

### `dubletten.py` — was `parallelen.py` prinzipiell nicht findet

`parallelen.py` durchsucht den **fertigen Bestand**. Was sich innerhalb des
gerade entstehenden Buches wiederholt, sieht es nicht, weil dort noch nichts
annotiert ist. Die Sprüche haben **26 solcher Verspaare**, sechs davon wörtlich
gleich, bis zu zwölf Kapitel auseinander und von verschiedenen Agenten zu
schreiben. Das neue Werkzeug erzeugt die Karte vor dem ersten Kapitel; jede
Übernahme ist danach programmatisch tiefkopiert und von mir feldweise
nachgerechnet worden.

**Ein Sonderfall war 14,12 ↔ 16,25**: beide Verse liefen **gleichzeitig** und
konnten sich nicht abstimmen. Beide Agenten haben den Vers vollständig
berichtet, die Fassungen unterschieden sich an drei Stellen, und die
Entscheidung fiel danach am gebauten 12,15, das dieselbe Konstruktion trägt.
**Das ist die Arbeitsteilung, die funktioniert:** der Agent berichtet
vollständig, die Zusammenführung macht der Koordinator.

### Die Prompt-Hinweise waren in jedem Paket falsch

Über elf Pakete haben die Agenten **mehr als fünfzig** meiner Prompt-Hinweise
am Quelltext widerlegt. Die schwersten:

- Für die Schöpfungsrede in Kapitel 8 nannte ich `Urflut`, `Himmelsgewölbe` und
  `Grundfeste`. Der Text sagt `Ozeane`, `Horizont` und `Fundamente`.
- 12,11 sagt „Wer sein **Land bestellt**, wird satt **von** Brot" — nicht
  `Acker bebaut`/`satt an`.
- 18,10/18,11 stellen einen **starken** Turm gegen eine feste Stadt, nicht
  „fester Turm" gegen „feste Stadt".
- `Bedürftiger` kommt im ganzen Kapitel 28 nicht vor, obwohl ich ihn für sechs
  Verse nannte.
- **`Freude machen` war zweimal falsch** (17,21 · 23,24): dort steht „hat keine
  Freude" bzw. „hat Freude an ihm", also `Freude haben`. Die Regel lautet:
  `Freude machen` nur, wo der Text „macht … Freude" sagt.

Das bestätigt, was seit 3. Mose in diesem Dokument steht — **der Prompt-Hinweis
ist der unzuverlässigste Teil des Verfahrens**. Sein Wert liegt darin, die
Aufmerksamkeit an die richtige Stelle zu lenken, nicht darin, recht zu haben.

### Der Homograph des Buches, und wie er gelöst wurde

`Toren` steht fünfmal und ist viermal das **Stadttor**, einmal der **Narr**
(17,21) — und dort steht `Narren` in derselben Zeile. **Drei der vier Ausgaben
trennen von selbst** (RV *necio/insensato*, LSG *insensé/fou*, RIV *stolto/uomo
da nulla*); nur WEB schreibt zweimal *fool*. es, fr und it folgen den Ausgaben
und decken sich mit der eigenen Narren-Lesart des Bestands aus Ps 14,1, deren
Italienisch bereits trennt. **Nur die englische Glosse hatte keine Quelle** —
*fool* ist `Narr`, *senseless one* ist `Unvernünftiger`; genommen ist *foolish
man*.

Dasselbe Muster in **18,15**: von den vier Ausgaben trennt **nur RV**, und zwar
umgekehrt zur Bindung. Da `Erkenntnis` mit 18 Vorkommen die stärkere Bindung
hat, weicht `Wissen` aus — und übernimmt dabei genau das Wort, das RV im Vers
selbst anbietet.

### Die Lexikonfalle in vier Varianten

| Wort | Bestand | warum er nicht trägt |
|---|---|---|
| `Erziehung` | im AT **unbelegt**, 5 NT-Belege | trägt trotzdem — die NT-Lesart ist bedeutungsgleich |
| `Besonnenheit` | 2 NT-Belege („Selbstbeherrschung") | in den Sprüchen ein Weisheitsbegriff; alle vier Ausgaben schreiben in allen drei Versen dasselbe |
| `Geheimnis` | 22 Belege, **sämtlich NT** (*mystery*) | 25,9 meint das gehütete Geheimnis eines Dritten |
| `Wohlgefallen` | 5 Belege, sämtlich NT (Gottes Ratschluss) | 8,35/18,22 meint „Gunst finden" |
| `tüchtig` | 11 Belege *capable*, alle „diensttaugliche Männer" | 12,4/31,10 ist eine sittliche Qualität |
| `Fremder` | 80 AT-Belege *extranjero* (Fremdling im Land) | 5,17/6,1 meint den Außenstehenden — hier trägt die **NT**-Lesart |

Der letzte Fall ist der lehrreichste: **die Bindung gilt für dieselbe
Bedeutung, nicht für dieselbe Buchstabenfolge**, und das kann auch heißen, dass
im AT die NT-Lesart die richtige ist.

### Was die Agenten an eigener Arbeit dazugelegt haben

- Kapitel 7 hat `kreuz.py` von sich aus gegen das gleichzeitig laufende
  Kapitel 5 gefahren und die wörtlich gleiche Zeile in 5,7 und 7,24 gefunden.
- Kapitel 28 hat dasselbe getan, zwei Divergenzen bei sich selbst angeglichen
  und zwei offen gemeldet statt eigenmächtig zu entscheiden.
- Kapitel 30 hat für die fünf Zahlensprüche ein Listenskript geschrieben, 62
  Glieder positionsgenau geprüft **und einen Mutationstest gefahren**: nach
  programmatischem Vertauschen zweier Glossen meldet es acht Befunde.
- Kapitel 9 hat den `hints.py`-Fehlalarm 9,8 nicht nur erkannt, sondern die
  Alternative mitprotokolliert, die er nicht gegangen ist.

### Acht Kollisionen bleiben bewusst stehen

`glosskollision.py` meldet über das fertige Buch acht inhaltliche Paare, jedes
am Vers geprüft: 4,16 und 14,5 (Verb und Stammsubstantiv, nur englisch), 18,20
(synonymer Parallelismus — alle vier Ausgaben wiederholen ihr eigenes Wort),
22,22 (figura etymologica; jede romanische Ausweichform wäre besetzt), 18,24
und 29,20 (das Einzelwort des Mehrworts `es gibt`), 25,21 und 30,8 (der
korpusweite `da'`-Befund).

**Zwei Bestandsbefunde sind korpusweit zu entscheiden und nicht angefasst
worden:** `gib` trägt italienisch `da'` (96 Belege) gegen `da` (4), und
`widerspiegeln`/`spiegeln` kollidieren im gebauten 2Kor 3,18 in en/es/fr.

## Prediger: was das Buch gelehrt hat

Zwölf Kapitel, 222 Verse, 5217 Einträge, fünf Pakete. Das erste Buch, das nach
dem verallgemeinerten `AUFTRAG_BUCH.md` gelaufen ist.

### Die Ausrichtung muss vor dem ersten Kapitel gemessen werden — und das Werkzeug dafür hat eine Grenze

`verszaehlung.py` ist neu und hat für alle Bücher 21–39 die Karte erzeugt. Das
Ergebnis: **die Sprüche waren der Sonderfall.** Dort stimmte die Verszahl in
allen 31 Kapiteln mit allen vier Ausgaben überein; im Prediger wackeln vier von
zwölf, und **Joel und Maleachi haben sogar eine abweichende Kapitelzahl**.

Im Prediger sind es zwei verschobene **Kapitelgrenzen**, keine fehlenden Verse:

| | wer verschiebt |
|---|---|
| **4 / 5** | de 4,17 = en/es/it 5,1, danach de 5,n = en/es/it 5,n+1. **LSG folgt dem Deutschen.** |
| **11 / 12** | umgekehrt: de 11,9 = **fr** 12,1, danach de 12,n = fr 12,n+2. en, es, it folgen dem Deutschen. |

Die vier Ausgaben laufen also **untereinander** auseinander, und für jeden Vers
braucht man zwei Nummern.

**`ausgaben.py` schätzt den Versatz global aus den Verslängen, und bei einer
verschobenen Kapitelgrenze ist das falsch** — der Versatz ist am Kapitelanfang
0 und kippt erst später. In Kapitel 4 meldete es `-1 UNSICHER`, zeigte aber die
richtige Zeile; **in Kapitel 11 zeigte es die falsche** (für de 11,5 die
französische Zeile 3). Das Skript warnt seither ausdrücklich: wenn ein Versatz
`UNSICHER` ist, kann auch die Anzeige falsch sein.

### Die Ausgaben helfen bei den Leitwörtern eines modernisierten Textes nicht

Die drei Wörter, die das Buch tragen, sind im Bestand fast unbelegt —
`vergänglich` steht 25× und hat einen einzigen AT-Beleg, `Haschen` 9× und
keinen, `Prediger` 7× und keinen. Bei allen dreien versagen die Ausgaben:

- Bei **`vergänglich`** schreiben alle vier ein **Substantiv** (*vanity ·
  vanidad · vanité · vanità*), wo der Text ein prädikatives Adjektiv hat, und
  bauen 1,2 völlig anders. Der Modernisierer hat Luthers „Es ist alles ganz
  eitel" durch „Alles ist vergänglich" ersetzt und die Bedeutung damit bewusst
  von *nichtig* auf *flüchtig* verschoben — die Glosse folgt dem einzigen
  AT-Beleg (Ps 39,5), nicht der NT-Mehrheit 6:1.
- Bei **`Haschen nach Wind`** schreibt RV an allen neun Stellen *aflicción de
  espíritu*, die alte Vulgata-Lesart, und folgt dem deutschen Text nicht. Das
  Spanische ist dort als einziges gebildet statt abgelesen.
- Bei **`Prediger`** teilen sich die Ausgaben: *Preacher/Predicador* gegen
  *Ecclésiaste/Ecclesiaste*. Jede bekommt ihre eigene.

**Das ist die Lehre des Buches:** wo der modernisierte Text weiter von Luther
weggeht als die Ausgaben von ihrer Vorlage, kann die Ausgabe die Glosse nicht
liefern. Dann entscheidet der Bestand — und wo auch der schweigt, das deutsche
Wort.

### `glosskollision.py` gegen `hints.py`, zweites Buch in Folge

`hints.py` meldete 22 Paare. Davon waren mehrere Fehlalarme (1,9 `neu`/`wieder`
— es rechnete mit der adverbialen Lesart, im Text steht das Adjektiv; 5,11 und
7,11), und mindestens ebenso viele echte hat es **nicht** gesehen. In den
Kapiteln 6, 8 und 10 meldete es **null** Paare, während `glosskollision.py` und
die Handprüfung je vier bis acht fanden.

Die schwerste Stelle des Buches, **8,14**, hätte es gemeldet — aber die Lösung
kam aus dem Bestand: `geschieht` und zweimal `ergeht` im selben Vers, beide
Lemmata auf *happens · sucede · arrive · accade*, und **drei der vier Ausgaben
schreiben genau die Kollisionswörter**. Gelöst mit der formgleichen Lesart aus
Ps 49,14 und dem Mehrwort-Eintrag `es ergehen`, den Prediger 2,15 bereits führt.

### Die Bindungstabelle muss nach jedem Buch neu erzeugt werden

Der Agent von Kapitel 9 meldete, `BINDUNGEN_AT.md` führe für `Netz` das
**Fettnetz des Opfertiers** als Bindung — wer ihr folgt, glossiert das
Fischernetz als Bauchfell. Kein Fehler im Generator: der Eintrag lautete
„(11/14)" und stammte aus einem Bestand von 14 AT-Belegen. Inzwischen sind es
31, und die Mehrheit hat sich gedreht. `bindungen.py` war seit dem Abschluss
von **Hiob** nicht mehr gelaufen, während Psalmen und Sprüche dazugekommen sind.

Neu erzeugt: 1899 statt 1217 Lemmata, und von den 1127 gemeinsamen haben elf
eine andere Lesart. Inhaltlich schwer sind `Netz` (*caul* → *net*) und `Mal`
(*mark* → *time*). **Das gehört ab jetzt zum Buchabschluss.**

### Elf Wörter, die als unbelegt gemeldet wurden und es nicht sind

`verwöhnen`, `begehren`, `weitersagen`, `säen`, `süß`, `verbannen`,
`wiederfinden` und vier weitere. `hints.py` und der `UNBELEGT`-Abschnitt von
`lexicon.py` sind **formbasiert**; bei zusammengesetzten und präfigierten
Verben zeigt der VERWANDT-Abschnitt oft nur Nominalableitungen. Es war in Buch
20 dasselbe Muster und ist inzwischen im `AUFTRAG_BUCH.md` vermerkt.

### Eine eigene Korrektur, die das Verfahren bestätigt

Ich hatte 11,9 an die Bestandsbindung von „in den Tagen" angeglichen, nachdem
Kapitel 12 sie belegt hatte — und damit die Kollision wiederhergestellt, die
Kapitel 11 bewusst aufgelöst hatte (in 11,9 stehen `an deiner Jugend` und
`in den Tagen` im selben Vers). Zurückgenommen. **Eine verse-lokale Auflösung
darf eine Bindung an der Kollisionsstelle überschreiben — genau dafür ist sie
da**, und 12,1 hat kein `an` daneben und behält die Bindung.


## Hohelied: was das Buch gelehrt hat

Acht Kapitel, 117 Verse — das kleinste bisher annotierte Buch, und dennoch das
mit den meisten Werkzeugbefunden. Drei davon haben zu Änderungen an den
Werkzeugen selbst geführt.

### `ausgaben.py` hat lautlos falsch ausgerichtet

Für Hohelied 6 meldete das Werkzeug **Versatz +1** für Englisch, Spanisch und
Italienisch — ohne `UNSICHER`-Marke — und paarte damit **jede** deutsche Zeile
mit der falschen fremdsprachigen. Nachgemessen: Versatz **0** bewertet
0,09–0,14, der angezeigte +1 bewertet 0,24–0,29. Der Agent hat das gefunden,
indem er die Kapiteldateien direkt aufschlug, statt der Anzeige zu glauben.

Die Ursache ist strukturell und betraf jedes bisherige Buch. Der Versatz kommt
aus dem letzten Vers. Hat eine Ausgabe **einen Vers mehr**, weil ihre
Kapitelgrenze weiter hinten liegt, schiebt diese Rechnung den Überhang nach
**vorn**. Die vorhandene Kontrolle (`len(de) + versatz == len(ausgabe)`) stimmt
in **beiden** Fällen und greift deshalb nie.

`ausgaben.py` bewertet jetzt die Nachbarversätze mit und meldet, wenn einer
deutlich besser liegt. Der angewandte Versatz wird **nicht** stillschweigend
ausgetauscht — genau das lag früher in Ps 9, 15 und 19 daneben. Die Schwelle
ist an fünf Kapiteln geeicht; über alle 939 fertigen Kapitel melden **4,9 %**
etwas, **17 Ausgabenzeilen davon wären vorher völlig stumm geblieben** —
darunter **Prediger 4**, das denselben Fehler trägt.

### Gleichzeitig laufende Kapitel kollidieren an Teilversen, die kein Werkzeug meldet

Zweimal in vier Paketen: der Halbvers „Bis der Tag sich abkühlt und die
Schatten fliehen" steht wörtlich gleich in **2,17 und 4,6**, der Block „ob der
Weinstock ausschlägt, ob die Granatbäume blühen" in **6,11 und 7,13**. Beide
Male liefen die Kapitel in derselben Welle und setzten verschieden.

`dubletten.py` findet sie nicht — es misst **ganze Verse**, und die Verse gehen
im Rest auseinander. `parallelen.py` findet sie, aber erst, wenn die Vorlage
gebaut ist. Dazu kam ein dritter Fall, den erst der Kreuzvergleich zeigte:
„zwischen den Lilien weiden" steht in **2,16 · 4,5 · 6,3**, und Kapitel 4 nahm
die Bestandsmehrheit (*between*), wo Kapitel 2 die kontextrichtige zweite
Lesart gesetzt hatte (*among*, weil es mehr als zwei Lilien sind).

**Konsequenz: der Kreuzvergleich aller Kapitel eines Buches gegeneinander ist
Pflicht, bevor gebaut wird** — Form plus Lemma als Schlüssel, Glossen als Wert.
Über die sieben Kapitel der ersten drei Pakete zeigte er 21 Divergenzen, von
denen drei echt waren; die übrigen 18 waren Numerus, Kasus oder bewusste
Zweitlesarten.

### `BINDUNGEN_AT.md` ist an zwei Stellen blind

- **bedeutungsblind**: bei `Schale` (7,3) markiert die Tabelle *bowl* als
  NT-Falle und bindet an *basin*. Hier ist es ein Trinkgefäß, und die
  *bowl*-Lesart hat mit Richter 5,25 einen AT-Beleg.
- **positionsblind**: bei `kaum` (3,4) nennt sie it *a malapena* (8/14) — die
  **großgeschriebene** Form hat aber 10 Belege mit *Appena*.

Dazu ein Randfall, der beim Neuerzeugen nach dem Buch sichtbar wurde: der
Kopftext sagte „häufigste Lesart **über** die Hälfte", die Bedingung im Code
lässt aber **genau** die Hälfte durch. Betroffen sind 91 Lemmata. Vor einer
Änderung nachgemessen: von den 21 echten 50:50-Gleichständen unterscheidet sich
**keiner** in der Bedeutung — alle sind Numerusvarianten. Eine Verschärfung
hätte 91 brauchbare Zeilen für nichts gekostet. **Die Schwelle blieb, der
Kopftext wurde berichtigt.**

### Die Vorbereitung selbst war die Fehlerquelle

Ich hatte ins Wortfeld geschrieben, `beschwören` sei im AT unbelegt — das war
der Anlass, Kapitel 2 als Maßstab vorzuziehen. Das Lemma hat **13 Belege, neun
davon im AT**, und die Bedeutung „feierlich bitten" ist dreimal alttestamentlich
belegt. Gezählt worden war die *Form* `beschwöre`, nicht das *Lemma* — genau
der Fehler, vor dem dasselbe Dokument die Kapitelagenten warnt.

Zweite eigene Fehlerquelle: in den Aufträgen standen mehrfach Wörter, die im
Quelltext gar nicht vorkommen (`Salböl`, `Nardenöl`, `Ketten`, `Wasserfluten`,
`bewahren`, `in Blüte stehen` für 7,13) oder in anderer Form (`Küssen` statt
`Küsse`, `ruhen lassen` statt `lagern`). **Prompt-Hinweise sind der
unzuverlässigste Teil des Auftrags** — das gilt inzwischen für jedes Buch, und
die Agenten prüfen sie richtigerweise am Quelltext nach.

### Wieder bestätigt: formbasiert unbelegt heißt nicht unbelegt

| Kapitel | von `hints.py` gemeldet | wirklich neu |
|---|---|---|
| 1 | 20 | 3 |
| 3 | 6 | 2 |
| 5 | 26 | 7 |
| 7 | 18 | 12 |
| 8 | 10 | 3 |

Und zweimal zeigte der Lexikon-Auszug das Lemma **auch unter VERWANDT nicht** —
nur `fixgloss.py show` fand es: `purpurn` und `Königsgewand` (7,2),
`verstärken` und `bieten` (8,7 · 8,9; `Böte` stand sogar unter UNBELEGT).
**Beide Werkzeuge fragen, nicht eines.**

### Die Kollisionsbilanz

`glosskollision.py` fand über das ganze Buch die üblichen Verschmelzungen. Die
Agenten fanden durch **eigenes Nachzählen zehn weitere, sechs davon in allen
vier Sprachen** — darunter `doch`/`aber` (5,6), `springend`/`hüpfend` (2,8),
`vorüber`/`vorbei` (2,11), `führen`/`bringen` (8,2, spanisch beide *llevar*)
und in 2,9 **drei** Wörter des Sehens im selben Vers (`Sieh`, `schaut`,
`blickt`), die im Bestand alle drei auf *look · mira · regarde · guarda* liegen.

Dazu eine feste Wendung, die **drei** Skripte übersahen: „priesen sie glücklich"
(6,9) ist `glücklich preisen`, im Bestand mit drei Belegen geführt, und
Sprüche 31,28 hat exakt dieselbe Konstellation.

### Was das Buch inhaltlich verlangt hat

Das Leitwort `Geliebter`/`Geliebte` (39 Vorkommen) ist **dasselbe Lemma in
entgegengesetztem Genus**, weil die beiden Liebenden einander mit demselben
deutschen Wort nennen. Alle vier Ausgaben trennen — jede anders. Nur das
Englische kann nicht über das Genus trennen, und in 2,10 stehen beide Formen im
selben Vers: dort ist WEBs eigenes Wort genommen (*my love* für die Frau,
*beloved* für den Mann).

Die folgenreichste Entscheidung war, **RIV nicht zu folgen**: die italienische
Ausgabe liest maskulin *amico*, was an seiner eigenen Stelle richtig aussieht —
aber in 5,16 steht `Geliebter` neben `Freund` (89 Belege, gebunden an
*amico*) und in 5,2 neben `Freundin` (*amica*). Kapitel 1 hat diese Kollision
drei Kapitel im Voraus gesehen. In 5,16 weicht RIV dann selbst aus („Tal è
l'**amor** mio, tal è l'**amico** mio") — die Ausgabe bestätigt die Festlegung
an genau der Stelle, für die sie getroffen wurde.

Ein zweiter Fall derselben Art: in **8,11** bindet `BINDUNGEN_AT.md` `Wächter`
an *watchman*, aber es sind Weinbergspächter, keine Stadtwächter. Die
naheliegende Alternative *keeper · guardián · gardien · custode* ist die feste
Bindung von `Hüter` — das im **Folgevers 8,12** steht.

### Ausgabenbefunde

- **WEB trägt die Sprecherangaben als Fließtext im Vers** („Beloved", „Lover",
  „Friends"), in 1,4 und 5,1 sogar mitten im Satz. Betrifft alle Kapitel außer
  **3**, das als einziges keine hat. Ein Importartefakt, das jeden verrutschen
  lässt, der WEB Wort für Wort abzählt.
- **RIV hat sechs Setzfehler** mit fehlenden Buchstaben: „alomone" (1,5),
  „il iorno" (3,11), „’ho cercato" (5,6), „l'amico uo" (5,9), zweimal „e" statt
  „è" (7,2 · 7,4).
- **LSG 8,14 endet mit einer freistehenden Tilde.**
- **RV1909mod benutzt im ganzen Buch *ustedes***, wo der Bestand die
  *vosotros*-Konvention führt — Bestand gehalten, sonst liefe das Buch gegen
  die übrigen 65.
