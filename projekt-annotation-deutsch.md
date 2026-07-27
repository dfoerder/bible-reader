# Deutsche Annotation (l1912mod → en/es/fr/it)

Wort-für-Wort-Annotation der deutschen Bibel mit Übersetzungen nach Englisch,
Spanisch, Französisch und Italienisch. Begonnen 25.07.2026. Ziel ist das
vollständige Neue Testament (Bücher 40–66).

Das ist die **Gegenrichtung** zu den bestehenden Annotationen: Bisher war
Deutsch immer Gloss-Sprache (WEB-Bibel mit `de`-Feld), hier ist Deutsch der
annotierte Text und die vier anderen Sprachen sind die Glossen.

## Stand

| Buch | Kapitel | Verse | Einträge | Phrasen | Klammern |
|---|---|---|---|---|---|
| Matthäus (40) | 28/28 | 1071 | 22 780 | 629 | 464 |
| Markus (41) | 16/16 | 678 | 14 235 | 434 | 346 |
| Lukas (42) | 24/24 | 1151 | 24 552 | 609 | 521 |
| Johannes (43) | 21/21 | 879 | 18 751 | 379 | 273 |
| Apostelgeschichte (44) | 28/28 | 1006 | 22 361 | 442 | 523 |
| Offenbarung (66) | 22/22 | 405 | 10 627 | 169 | 98 |
| **Summe** | **139** | **5190** | **113 306** | **2662** | **2225** |

Damit sind die vier Evangelien, die Apostelgeschichte und die Offenbarung
vollständig. Es fehlen die 21 Briefe (45–65): 121 Kapitel, 2764 Verse.

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

Liegt im Scratchpad (`scratchpad/anno/`, früher `scratchpad/mt1/`), **nicht** im
Repo — beim Fortsetzen in einer neuen Sitzung neu anzulegen. Die Kernstücke:

| Datei | Zweck |
|---|---|
| `SPEC.md` | verbindliche Spezifikation für die Agenten |
| `buildbook.py <nr>` | baut die Anno-Datei eines Buches aus den Kapitel-JSONs |
| `gen_mt1.validate()` | Struktur-Validator (Vollständigkeit, Formen, Spannen) |
| `qa.py [pfad]` | inhaltliche Heuristiken gegen verrutschte Zuordnungen |
| `levels.py` | Level-Vereinheitlichung, wird vom Build aufgerufen |
| `lexicon.py <nr> <kap> <von> <bis> <ziel>` | gefilterter Lexikon-Extrakt für einen Versbereich |
| `BINDUNGEN_OFFB.md` | Glossen-Bindungen der Offenbarung, gegen den Bestand geprüft |
| `BINDUNGEN_BRIEFE.md` | dasselbe für die Briefe, mit vorab gemessenen Kollisionen |
| `selfcheck.py <nr> <kap> <datei> [von bis]` | Validator als Kommandozeilenaufruf für die Agenten |
| `crosscheck.py <datei> <grenze…>` | Abschnittsgrenzen: welche Inhaltswörter weichen links und rechts ab |

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

## Offen

- Die 21 Briefe (45–65): 121 Kapitel, 2764 Verse. Römer ist für sie der
  Maßstab, so wie Matthäus für die Evangelien — sein Vokabular tragen alle
  weiteren Briefe. Die Abdeckung durch den vorhandenen Bestand liegt bei nur
  53 % (Offenbarung: 70 %), weil argumentative Prosa einen anderen Wortschatz
  hat als Erzählung.
- Sehr kurze Bücher (Philemon, 2./3. Johannes, Judas — je unter 600 Wörter)
  kann je ein Agent komplett übernehmen statt kapitelweise
- Kein Vokabeltraining für Deutsch: dafür bräuchte es `words.json` +
  `examples.json` analog zur ES-Pipeline (`build_training.py` → Opus-Enrichment
  → `finalize_training.py`) und `build_keepnames.py` für die Eigennamen-Liste
- `hasTraining`/`hasLevelTest` bleiben bis dahin `false`
