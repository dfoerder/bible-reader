#!/usr/bin/env python3
"""Prüft die Anreicherungs-Ausgaben einer Edition gegen ihre Eingabepakete.

Findet, was ein Agent still falsch machen kann: fehlende oder zusätzliche
Einträge, verschobene Reihenfolge, verfremdete Lemmata, unbekannte Wortarten
oder Level, fehlende Zielsprachen, Grammatik-Etiketten in Klammern statt echter
Wörter (der häufigste stille Fehler) und leere Übersetzungen.

Aufruf:  python3 check_enrich.py deu-l1912mod
"""
import json, os, sys, glob, re, collections

POS = {"noun", "verb", "adj", "adv", "propn", "det", "pron", "prep", "conj",
       "num", "intj", "part"}
LEVELS = {"A1", "A2", "B1", "B2", "C1", "C2"}
TAG = re.compile(r'[()\[\]]|/')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_training import LANGS  # noqa: E402


def main():
    ed = sys.argv[1] if len(sys.argv) > 1 else "deu-l1912mod"
    cfg = LANGS[ed]
    langs = set(cfg["gloss_fields"])
    d = os.path.join(cfg["bible_dir"], "train", "enrich")

    problems = 0
    total = 0
    pos_count = collections.Counter()
    lvl_count = collections.Counter()
    for inp in sorted(glob.glob(os.path.join(d, "in_*.json"))):
        outp = inp.replace("in_", "out_")
        if not os.path.exists(outp):
            continue
        i = json.load(open(inp, encoding="utf-8"))
        try:
            o = json.load(open(outp, encoding="utf-8"))
        except ValueError as e:
            print(f"✗ {os.path.basename(outp)}: kein gültiges JSON ({e})")
            problems += 1
            continue
        name = os.path.basename(outp)
        if len(i) != len(o):
            print(f"✗ {name}: {len(o)} Einträge statt {len(i)}")
            problems += 1
        li, lo = [x["lemma"] for x in i], [x.get("lemma") for x in o]
        if li != lo:
            miss = [x for x in li if x not in set(lo)]
            extra = [x for x in lo if x not in set(li)]
            print(f"✗ {name}: Lemma-Folge weicht ab "
                  f"(fehlend {len(miss)}: {miss[:5]} · zusätzlich {len(extra)}: {extra[:5]})")
            problems += 1
        for x in o:
            total += 1
            lem = x.get("lemma", "?")
            if x.get("pos") not in POS:
                print(f"✗ {name}/{lem}: Wortart {x.get('pos')!r}")
                problems += 1
            else:
                pos_count[x["pos"]] += 1
            if x.get("level") not in LEVELS:
                print(f"✗ {name}/{lem}: Level {x.get('level')!r}")
                problems += 1
            else:
                lvl_count[x["level"]] += 1
            base = x.get("base")
            if not isinstance(base, dict) or set(base) != langs:
                print(f"✗ {name}/{lem}: base {sorted(base) if isinstance(base, dict) else base!r} "
                      f"statt {sorted(langs)}")
                problems += 1
                continue
            for l, v in base.items():
                if not (v or "").strip():
                    print(f"✗ {name}/{lem}: leere Übersetzung [{l}]")
                    problems += 1
                elif TAG.search(v):
                    print(f"✗ {name}/{lem}: Grammatik-Etikett/Liste [{l}] {v!r}")
                    problems += 1

    done = len(glob.glob(os.path.join(d, "out_*.json")))
    todo = len(glob.glob(os.path.join(d, "in_*.json")))
    print(f"\n{done}/{todo} Pakete · {total} Lemmata · {problems} Beanstandung(en)")
    print("  Wortarten: " + ", ".join(f"{k}={v}" for k, v in pos_count.most_common()))
    print("  Level: " + ", ".join(f"{k}={lvl_count[k]}" for k in sorted(LEVELS)))
    content = sum(pos_count[p] for p in ("noun", "verb", "adj", "adv"))
    print(f"  davon Inhaltswörter (Pool-Kandidaten): {content}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
