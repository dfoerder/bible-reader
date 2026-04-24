#!/usr/bin/env python3
"""
Converts an OSIS XML Bible file to per-book JSON files
matching the bible-reader app format.
"""
import xml.etree.ElementTree as ET
import json
import os
import sys

OSIS_NS = "http://www.bibletechnologies.net/2003/OSIS/namespace"

OSIS_TO_NR = {
    "Gen": 1, "Exod": 2, "Lev": 3, "Num": 4, "Deut": 5,
    "Josh": 6, "Judg": 7, "Ruth": 8, "1Sam": 9, "2Sam": 10,
    "1Kgs": 11, "2Kgs": 12, "1Chr": 13, "2Chr": 14, "Ezra": 15,
    "Neh": 16, "Esth": 17, "Job": 18, "Ps": 19, "Prov": 20,
    "Eccl": 21, "Song": 22, "Isa": 23, "Jer": 24, "Lam": 25,
    "Ezek": 26, "Dan": 27, "Hos": 28, "Joel": 29, "Amos": 30,
    "Obad": 31, "Jonah": 32, "Mic": 33, "Nah": 34, "Hab": 35,
    "Zeph": 36, "Hag": 37, "Zech": 38, "Mal": 39,
    "Matt": 40, "Mark": 41, "Luke": 42, "John": 43, "Acts": 44,
    "Rom": 45, "1Cor": 46, "2Cor": 47, "Gal": 48, "Eph": 49,
    "Phil": 50, "Col": 51, "1Thess": 52, "2Thess": 53,
    "1Tim": 54, "2Tim": 55, "Titus": 56, "Phlm": 57, "Heb": 58,
    "Jas": 59, "1Pet": 60, "2Pet": 61, "1John": 62, "2John": 63,
    "3John": 64, "Jude": 65, "Rev": 66,
}

ITALIAN_NAMES = {
    1: "Genesi", 2: "Esodo", 3: "Levitico", 4: "Numeri",
    5: "Deuteronomio", 6: "Giosuè", 7: "Giudici", 8: "Rut",
    9: "1 Samuele", 10: "2 Samuele", 11: "1 Re", 12: "2 Re",
    13: "1 Cronache", 14: "2 Cronache", 15: "Esdra", 16: "Neemia",
    17: "Ester", 18: "Giobbe", 19: "Salmi", 20: "Proverbi",
    21: "Ecclesiaste", 22: "Cantico dei Cantici", 23: "Isaia",
    24: "Geremia", 25: "Lamentazioni", 26: "Ezechiele", 27: "Daniele",
    28: "Osea", 29: "Gioele", 30: "Amos", 31: "Abdia", 32: "Giona",
    33: "Michea", 34: "Naum", 35: "Abacuc", 36: "Sofonia",
    37: "Aggeo", 38: "Zaccaria", 39: "Malachia",
    40: "Matteo", 41: "Marco", 42: "Luca", 43: "Giovanni",
    44: "Atti", 45: "Romani", 46: "1 Corinzi", 47: "2 Corinzi",
    48: "Galati", 49: "Efesini", 50: "Filippesi", 51: "Colossesi",
    52: "1 Tessalonicesi", 53: "2 Tessalonicesi",
    54: "1 Timoteo", 55: "2 Timoteo", 56: "Tito", 57: "Filemone",
    58: "Ebrei", 59: "Giacomo", 60: "1 Pietro", 61: "2 Pietro",
    62: "1 Giovanni", 63: "2 Giovanni", 64: "3 Giovanni",
    65: "Giuda", 66: "Apocalisse",
}

def convert(xml_path, out_dir, translation_abbr):
    os.makedirs(out_dir, exist_ok=True)
    tree = ET.parse(xml_path)
    root = tree.getroot()

    total_verses = 0
    for book_div in root.iter(f"{{{OSIS_NS}}}div"):
        if book_div.get("type") != "book":
            continue
        osis_id = book_div.get("osisID")
        nr = OSIS_TO_NR.get(osis_id)
        if nr is None:
            continue

        name = ITALIAN_NAMES[nr]
        chapters = {}

        for chapter_el in book_div.iter(f"{{{OSIS_NS}}}chapter"):
            ch_osis = chapter_el.get("osisID")
            ch_num = ch_osis.split(".")[-1]
            verses = {}
            for verse_el in chapter_el.iter(f"{{{OSIS_NS}}}verse"):
                v_osis = verse_el.get("osisID")
                v_num = v_osis.split(".")[-1]
                text = (verse_el.text or "").strip()
                if text:
                    verses[v_num] = text
                    total_verses += 1
            if verses:
                chapters[ch_num] = verses

        out_file = os.path.join(out_dir, f"{nr}_{translation_abbr}.json")
        data = {"name": name, "chapters": chapters}
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, separators=(",", ":"))

        ch_count = len(chapters)
        v_count = sum(len(v) for v in chapters.values())
        print(f"  {name}: {ch_count} Kapitel, {v_count} Verse")

    print(f"\n  Fertig! {total_verses} Verse insgesamt nach {out_dir}")


if __name__ == "__main__":
    xml_file = sys.argv[1] if len(sys.argv) > 1 else "ita-riveduta.osis.xml"
    out_dir = sys.argv[2] if len(sys.argv) > 2 else "bibles/ita/riv1927"
    abbr = sys.argv[3] if len(sys.argv) > 3 else "riv1927"
    convert(xml_file, out_dir, abbr)
