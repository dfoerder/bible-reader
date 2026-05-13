#!/usr/bin/env python3
"""Clean up punctuation and proper nouns from a chapter's annotations."""
import json, re, sys

BOOK_NR = int(sys.argv[1]) if len(sys.argv) > 1 else 40
CHAP_NR = str(int(sys.argv[2])) if len(sys.argv) > 2 else "3"

ANNO_PATH = f"bibles/eng/web/anno/{BOOK_NR}_web_deu.json"

_PUNCT = ".,;:!?“”„‘’«»\"'"
PUNCT_TRAIL = re.compile("[" + _PUNCT + "]+$")
PUNCT_LEAD = re.compile("^[" + _PUNCT + "]+")

PROPER_NOUNS = {
    "bethlehem", "judea", "juda", "judah", "jerusalem", "jordan",
    "john", "jesus", "christ", "galilee", "god", "gottes", "gott",
    "israel", "abraham", "isaac", "jacob", "isaiah", "jesaja",
    "david", "mary", "joseph", "moses", "egypt", "nazareth",
    "herod", "herodes", "solomon", "babylon", "samaria", "nazarene",
    "pharisees", "sadducees", "immanuel",
}


def strip_punct(s):
    s = PUNCT_TRAIL.sub("", s)
    s = PUNCT_LEAD.sub("", s)
    return s


with open(ANNO_PATH, "r", encoding="utf-8") as f:
    anno = json.load(f)

chap = anno["chapters"][CHAP_NR]

fixed = 0
for vnum, annotations in chap.items():
    for a in annotations:
        old_form = a["form"]
        old_de = a["de"]
        a["form"] = strip_punct(a["form"])
        a["de"] = strip_punct(a["de"])
        if a["form"] != old_form or a["de"] != old_de:
            fixed += 1

removed = 0
for vnum in list(chap.keys()):
    before = len(chap[vnum])
    chap[vnum] = [
        a for a in chap[vnum]
        if strip_punct(a["form"]).lower() not in PROPER_NOUNS
    ]
    diff = before - len(chap[vnum])
    if diff:
        removed += diff

print(f"  Chapter {CHAP_NR}: fixed {fixed} punctuation, removed {removed} proper nouns")

with open(ANNO_PATH, "w", encoding="utf-8") as f:
    json.dump(anno, f, ensure_ascii=False, indent=2)
print("  Saved.")
