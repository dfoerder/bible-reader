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
| Lukas (42) | in Arbeit | — | — | — | — |

Angefangene, noch unvollständige Kapitel liegen unter `anno/_wip/` — siehe den
README dort. Die App lädt diesen Ordner nie.

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

Liegt im Scratchpad (`scratchpad/mt1/`), **nicht** im Repo — beim Fortsetzen in
einer neuen Sitzung neu anzulegen. Die Kernstücke:

| Datei | Zweck |
|---|---|
| `SPEC.md` | verbindliche Spezifikation für die Agenten |
| `buildbook.py <nr>` | baut die Anno-Datei eines Buches aus den Kapitel-JSONs |
| `gen_mt1.validate()` | Struktur-Validator (Vollständigkeit, Formen, Spannen) |
| `qa.py [pfad]` | inhaltliche Heuristiken gegen verrutschte Zuordnungen |
| `levels.py` | Level-Vereinheitlichung, wird vom Build aufgerufen |

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

**3. Gegenrechnung pro Buch** — Tokens im Quelltext gegen Einzelwort-Einträge;
die Differenz muss exakt der Zahl der alleinstehenden Satzzeichen entsprechen.
Matthäus: 21 699 − 21 687 = 12. Markus: 13 461 − 13 455 = 6. Beide stimmen.

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
zwischen 91 % und 98 %.

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

**Commit-Nachrichten gegen die Build-Ausgabe prüfen.** Dreimal habe ich den
Inhalt zu niedrig angegeben, weil beim Bauen bereits ein weiteres fertiges
Kapitel vorlag, dessen Agent sich noch nicht gemeldet hatte. Inhaltlich war nie
etwas falsch, aber die Beschreibung hinkte hinterher.

## Commit-Schema

Ein Commit je validiertem Kapitel oder Kapitelpaar, ausschließlich auf `dev`,
**nicht gepusht** — Push und Merge nach `main` macht `deploy.sh` und wäre ein
Deployment. Committet wird nur, was der Validator durchgewunken hat.

## Offen

- Lukas fertigstellen, dann Johannes, Apostelgeschichte, Offenbarung, Briefe
- Sehr kurze Bücher (Philemon, 2./3. Johannes, Judas — je unter 600 Wörter)
  kann je ein Agent komplett übernehmen statt kapitelweise
- Kein Vokabeltraining für Deutsch: dafür bräuchte es `words.json` +
  `examples.json` analog zur ES-Pipeline (`build_training.py` → Opus-Enrichment
  → `finalize_training.py`) und `build_keepnames.py` für die Eigennamen-Liste
- `hasTraining`/`hasLevelTest` bleiben bis dahin `false`
