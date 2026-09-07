#!/usr/bin/env python3
"""Trainingsdaten-Builder — Schritt 2a: Anreicherungs-Pakete schnüren.

Zerlegt das Extraktions-Intermediate (train/lemmas_raw.json) in handliche
JSON-Pakete, die je ein Claude-Code-Subagent anreichert. Der Agent bekommt pro
Lemma die vorläufige Einstufung, die Mehrheitsglossen aller Glossensprachen und
einen Beispielsatz und liefert zurück:

    {"lemma": "schaffen", "level": "B1", "pos": "verb",
     "base": {"en": "to create", "es": "crear", "fr": "créer", "it": "creare"}}

Nur `level`, `pos` und die **Grundform-Übersetzungen** kommen aus dem Modell.
Die flektierten Formübersetzungen (Antwortanzeige im Lückentext) stehen bereits
kontextuell korrekt in den Annotationen und werden in Schritt 3 direkt von der
Cloze-Fundstelle übernommen.

Lemmata, die schon angereichert sind (out_*.json) ODER bereits in einem offenen
Paket stecken (in_*.json), werden übersprungen; bestehende Pakete bleiben liegen
und die Nummerierung zählt dahinter weiter. Das Skript ist damit wiederholbar und
wellenfähig, auch während Agenten noch arbeiten.

Aufruf:  python3 prepare_enrich.py deu-l1912mod --min-freq 3
         python3 prepare_enrich.py deu-l1912mod --min-freq 1 --size 250
"""
import json, os, sys, glob, argparse, re

BATCH_SIZE = 250

# Sprachnamen für die Agenten-Anweisung
LANG_NAMES = {"en": "Englisch", "de": "Deutsch", "es": "Spanisch",
              "it": "Italienisch", "fr": "Französisch"}

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_training import LANGS  # noqa: E402  (eine Registry für beide Schritte)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("edition", choices=sorted(LANGS))
    ap.add_argument("--min-freq", type=int, default=1,
                    help="nur Lemmata ab dieser Häufigkeit (Welle 1: 3)")
    ap.add_argument("--size", type=int, default=BATCH_SIZE, help="Lemmata je Paket")
    args = ap.parse_args()

    cfg = LANGS[args.edition]
    train = os.path.join(cfg["bible_dir"], "train")
    raw = json.load(open(os.path.join(train, "lemmas_raw.json"), encoding="utf-8"))
    out_dir = os.path.join(train, "enrich")
    os.makedirs(out_dir, exist_ok=True)

    done = set()   # schon angereichert oder bereits in einem Paket
    for f in glob.glob(os.path.join(out_dir, "out_*.json")):
        for o in json.load(open(f, encoding="utf-8")):
            if o.get("lemma"):
                done.add(o["lemma"])

    # Auch Lemmata überspringen, die schon in einem OFFENEN Paket stecken — sonst
    # schnürt ein zweiter Lauf dieselben Wörter noch einmal, während die Agenten
    # der ersten Welle noch daran sitzen.
    for f in glob.glob(os.path.join(out_dir, "in_*.json")):
        for o in json.load(open(f, encoding="utf-8")):
            if o.get("lemma"):
                done.add(o["lemma"])

    # Häufigste zuerst: die ersten Pakete tragen den grössten Teil des Textes
    todo = sorted((r for l, r in raw.items()
                   if not r["is_cap"] and r["freq"] >= args.min_freq and l not in done),
                  key=lambda r: (-r["freq"], r["lemma"]))

    # Bestehende Pakete stehen lassen und dahinter weiterzählen: ein noch laufender
    # Agent darf seine Eingabedatei nicht unter den Händen verlieren.
    used = [int(re.search(r'in_(\d+)', f).group(1))
            for f in glob.glob(os.path.join(out_dir, "in_*.json"))]
    n = max(used) if used else 0

    batches = 0
    for i in range(0, len(todo), args.size):
        chunk = todo[i:i + args.size]
        items = []
        for r in chunk:
            cz = r.get("cloze") or {}
            form = cz.get("answer") or ""
            # Beispielsatz mit eingesetzter Form: der Agent sieht das Wort im Satz,
            # `form` sagt ihm, welches der Tokens gemeint ist.
            sentence = (cz.get("text") or "").replace("___", form or "___")
            items.append({
                "lemma": r["lemma"],
                "prelim_level": r["level"],
                "freq": r["freq"],
                "gloss": r.get("gloss_by") or {},
                "form": form,
                "sentence": sentence,
            })
        batches += 1
        n += 1
        path = os.path.join(out_dir, "in_%03d.json" % n)
        json.dump(items, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    langs = ", ".join(LANG_NAMES.get(l, l) for l in cfg["gloss_fields"])
    print(f"✓ {batches} Paket(e) à max. {args.size} in {out_dir}")
    print(f"  offen: {len(todo)} Lemmata (ab Häufigkeit {args.min_freq}), "
          f"schon angereichert: {len(done)}")
    print(f"  Glossensprachen: {langs}")


if __name__ == "__main__":
    main()
