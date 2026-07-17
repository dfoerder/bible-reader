#!/usr/bin/env python3
"""Erzeugt bibles/eng/web/train/examples.json: pro Lemma ein schlanker Index von Vers-Referenzen
(ohne Verstext), damit der Nutzer bei einer falsch beantworteten Kontext-Übung
über "Weitere Beispiele" das Wort in weiteren Sätzen sehen kann. Der Verstext
wird in der App on-the-fly aus den Bibeltext-Dateien geholt (fetchBook/_bookCache).

Format (kompakt):  { "<lemma>": [ [<bookNr>, <chapter>, <verse>, <wortindex>], ... ] }

Lazy in der App geladen (nicht beim Start).

Run:  python3 generate_examples.py
"""
import json, os

ANNO_DIR = "bibles/eng/web/anno"
TEXT_DIR = "bibles/eng/web"
OUT = "bibles/eng/web/train/examples.json"
WORDS = "bibles/eng/web/train/words.json"

MAX_PER_LEMMA = 5
MIN_WORDS, MAX_WORDS = 5, 30


def main():
    # Curated-Refs je Lemma, um Dubletten zum Übungssatz zu vermeiden
    curated = {}
    w = json.load(open(WORDS))
    for arr in w.values():
        for e in arr:
            curated[e["en"]] = e.get("ref")

    by_lemma = {}  # lemma -> list of (ref, text, pos)
    for nr in range(1, 67):
        ap = os.path.join(ANNO_DIR, f"{nr}_web_deu.json")
        tp = os.path.join(TEXT_DIR, f"{nr}_web.json")
        if not (os.path.exists(ap) and os.path.exists(tp)):
            continue
        anno = json.load(open(ap))
        text = json.load(open(tp))
        name = text.get("name") or anno.get("name") or f"Book {nr}"
        # Vers-Text-Lookup: chapter(str) -> verse(str) -> text
        # Quellformat einheitlich dict: {chapters:{cn:{vn:text}}}
        vtext = {}
        for cn, verses in text["chapters"].items():
            vtext[str(cn)] = {str(vn): t for vn, t in verses.items()}
        for cn, verses in anno["chapters"].items():
            for vn, anns in verses.items():
                vt = vtext.get(cn, {}).get(vn)
                if not vt:
                    continue
                wc = len(vt.split())
                if wc < MIN_WORDS or wc > MAX_WORDS:
                    continue
                ref = f"{name} {cn}:{vn}"
                seen_lemmas = set()
                for a in anns:
                    lem = a.get("lemma")
                    pos = a.get("pos")
                    if not lem or pos is None or lem in seen_lemmas:
                        continue
                    if lem not in curated:  # nur Lemmas, die der Lückentext auch nutzt
                        continue
                    seen_lemmas.add(lem)
                    if ref == curated.get(lem):  # Übungssatz nicht doppeln
                        continue
                    by_lemma.setdefault(lem, []).append([nr, int(cn), int(vn), pos])

    # Pro Lemma höchstens MAX_PER_LEMMA, gleichmäßig über die Vorkommen gestreut
    out = {}
    for lem, occ in by_lemma.items():
        # nach Textlänge nahe 14 Wörtern bevorzugen, dann gleichmäßig auswählen
        if len(occ) <= MAX_PER_LEMMA:
            picks = occ
        else:
            step = len(occ) / MAX_PER_LEMMA
            picks = [occ[int(i * step)] for i in range(MAX_PER_LEMMA)]
        out[lem] = picks

    json.dump(out, open(OUT, "w"), ensure_ascii=False, separators=(",", ":"))
    total = sum(len(v) for v in out.values())
    print(f"{len(out)} Lemmas, {total} Beispiele -> {OUT}")
    print(f"Dateigröße: {os.path.getsize(OUT)/1024:.0f} KB")


if __name__ == "__main__":
    main()
