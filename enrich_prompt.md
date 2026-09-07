# Anreicherungs-Auftrag (Schritt 2 der Trainingsdaten-Pipeline)

Diese Datei ist die vollständige Arbeitsanweisung für einen Anreicherungs-Agenten.
Ein Aufruf lautet: „Arbeite `enrich_prompt.md` ab für `<in_NNN.json>`."

## Aufgabe

Lies die zugewiesene Eingabedatei `bibles/<edition>/train/enrich/in_NNN.json` und
schreibe `out_NNN.json` in denselben Ordner. Beides sind JSON-Arrays.

Eingabe je Lemma:

```json
{"lemma": "schaffen", "prelim_level": "B2", "freq": 122,
 "gloss": {"en": "created", "es": "creado", "fr": "créé", "it": "creato"},
 "form": "schaffte", "sentence": "Danach schaffte sich Absalom einen Wagen …"}
```

`gloss` ist die **häufigste kontextuelle** Glosse aus den Annotationen — also oft
eine flektierte Form und manchmal nur eine von mehreren Bedeutungen. `form` ist
das Token im Beispielsatz.

Ausgabe je Lemma **genau ein** Objekt:

```json
{"lemma": "schaffen", "level": "B1", "pos": "verb",
 "base": {"en": "to create", "es": "crear", "fr": "créer", "it": "creare"}}
```

## Regeln

**Vollständigkeit.** Die Ausgabe enthält genau so viele Objekte wie die Eingabe,
in derselben Reihenfolge, mit dem `lemma` **zeichengleich** übernommen. Nichts
auslassen, nichts zusammenfassen, nichts erfinden.

**`level`** — CEFR aus Sicht von **Deutschlernenden**, bezogen auf das Lemma (nicht
auf die Form im Satz): A1 A2 B1 B2 C1 C2. `prelim_level` ist die Mehrheit der
Annotationen und oft zu hoch gegriffen, weil sie am Kontext klebt — korrigiere sie,
wenn das Wort als Vokabel klar leichter oder schwerer ist. Massstab ist der
allgemeine Wortschatz, nicht die Bibelhäufigkeit: `Wasser` A1, `Bund` B1,
`Gräuel` C1, `Stiftshütte` C2.

**`pos`** — genau einer von:
`noun` `verb` `adj` `adv` `propn` `det` `pron` `prep` `conj` `num` `intj` `part`

- `propn` nur für **echte Eigennamen**: Personen, Orte, Völker, Flüsse, Monate,
  Gestirnsnamen. Gattungswörter bleiben `noun`, auch wenn sie im Englischen gross
  geschrieben werden: `Gott` → noun, `HERR` → noun, `Geist` → noun,
  `Priester` → noun. Im Zweifel: steht ein Artikel davor („der Priester"), ist es
  ein Gattungswort.
- Nur `noun` `verb` `adj` `adv` kommen später in den Übungspool; alles andere wird
  verworfen. Trotzdem für **jedes** Lemma eine Wortart angeben.

**`base`** — Grundform-Übersetzung in **allen vier** Sprachen, so wie sie im
Wörterbuch stünde, **nicht** die flektierte Kontextglosse:

- Verben: englisch mit `to` (`to create`), spanisch/französisch/italienisch im
  Infinitiv (`crear`, `créer`, `creare`)
- Substantive: Nominativ Singular, ohne Artikel (`beginning`, `principio`,
  `commencement`, `principio`)
- Adjektive/Adverbien: Grundform, unflektiert, ohne Steigerung

Passt die Mehrheitsglosse zur Grundform, übernimm sie; steht dort eine gebeugte
Form (`created`, `creado`), setze die Grundform ein.

**Mehrdeutige Lemmata.** Manche Lemmata bündeln mehrere Bedeutungen (`sein` =
Kopula und Possessivum, `schaffen` = erschaffen und schaffen/besorgen). Wähle die
**im Bibeltext vorherrschende** Bedeutung — Mehrheitsglosse und Beispielsatz
zeigen sie. Keine Doppelangaben, keine Schrägstrich-Listen.

**Keine Grammatik-Etiketten.** Niemals Klammerausdrücke wie `(futuro)`,
`(reflexive)`, `(Hilfsverb)` oder `(Partikel)` als Übersetzung. Ein unübersetzbares
Funktionswort bekommt das nächstliegende echte Wort der Zielsprache; gibt es keines,
die gebräuchlichste Entsprechung in einfachen Worten.

**Register.** Normale, heutige Umgangssprache ist richtig — nicht gestelzt, nicht
altertümlich. Nur ausgesprochene Gossensprache vermeiden.

**Format.** Reines JSON, UTF-8, keine Kommentare, kein Markdown-Rahmen, keine
Erklärungen ausserhalb der Datei. Schreibe die Datei mit dem Write-Werkzeug.

## Zum Schluss

Prüfe selbst, bevor du fertig meldest:

1. `len(out) == len(in)` und die Lemma-Folge stimmt zeichengleich überein.
2. Kein `base`-Wert enthält eine Klammer oder ein Grammatik-Etikett.
3. Jedes `pos` steht auf der Liste, jedes `level` ist A1–C2.

Melde am Ende nur: Anzahl Einträge, Anzahl `propn`, und was dir aufgefallen ist
(unklare Lemmata, Verdacht auf Annotationsfehler).
