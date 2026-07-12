#!/usr/bin/env python3
"""
Merge one or more per-chapter Spanish->English annotation JSON files
(produced by subagents into /tmp) into the canonical
bibles/spa/rv1909mod/anno/{book_nr}_rv1909mod_eng.json, after validating
word positions against the source text (same logic as annotate_nt_es.py).

Usage:
  python3 merge_es_anno.py <book_nr> <chapter_num> <path_to_chapter_json> [<chapter_num> <path> ...]

Each <path_to_chapter_json> must be a JSON object {verseNum: [annotations]}
for exactly that chapter (or a subset of verses of that chapter — existing
verses are left untouched, new ones are added).
"""
import json
import os
import re
import sys

BIBLE_DIR = "bibles/spa/rv1909mod"
ANNO_DIR = "bibles/spa/rv1909mod/anno"


def _normalize(word):
    return re.sub(r"[.,;:!?()\[\]\"'’‘«»—–…¡¿*]", "", word).lower()


def correct_positions(batch_annotations, verse_map):
    corrections = 0
    issues = []
    for verse_key, annotations in batch_annotations.items():
        text = verse_map.get(verse_key, "")
        if not text:
            issues.append(f"v{verse_key}: not in source text")
            continue
        words = text.split()
        for ann in annotations:
            pos = ann.get("pos", -1)
            form = ann.get("form", "")
            form_norm = _normalize(form.split()[0] if "pos_end" in ann else form)
            if not form_norm:
                continue
            if 0 <= pos < len(words) and _normalize(words[pos]) == form_norm:
                continue
            found = -1
            for i, w in enumerate(words):
                if _normalize(w) == form_norm:
                    found = i
                    break
            if found >= 0:
                ann["pos"] = found
                corrections += 1
            else:
                issues.append(f"v{verse_key}: '{form}' not found in text: {text!r}")
    return corrections, issues


def anno_path(book_nr):
    return os.path.join(ANNO_DIR, f"{book_nr}_rv1909mod_eng.json")


def main():
    if len(sys.argv) < 4 or len(sys.argv) % 2 != 0:
        print(__doc__)
        sys.exit(1)

    book_nr = sys.argv[1]
    pairs = [(sys.argv[i], sys.argv[i + 1]) for i in range(2, len(sys.argv), 2)]

    src_path = os.path.join(BIBLE_DIR, f"{book_nr}_rv1909mod.json")
    with open(src_path, "r", encoding="utf-8") as f:
        src = json.load(f)
    book_name = src["name"]
    chapters_src = src["chapters"]

    path = anno_path(book_nr)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            out = json.load(f)
    else:
        out = {"name": book_name, "chapters": {}}

    total_new = 0
    for ch_num, json_path in pairs:
        with open(json_path, "r", encoding="utf-8") as f:
            batch = json.load(f)
        if not isinstance(batch, dict):
            print(f"  ✗ cap {ch_num}: {json_path} no es un objeto JSON")
            continue
        verse_map = chapters_src.get(ch_num)
        if verse_map is None:
            print(f"  ✗ cap {ch_num}: capítulo no existe en el texto fuente")
            continue

        fixed, issues = correct_positions(batch, verse_map)
        ch_out = out["chapters"].setdefault(ch_num, {})
        new_verses = [v for v in batch if v not in ch_out]
        ch_out.update(batch)
        n_ann = sum(len(v) for v in batch.values())
        total_new += n_ann

        missing = [v for v in verse_map if v not in ch_out]
        status = "✓" if not missing and not issues else "⚠"
        print(f"  {status} cap {ch_num}: +{n_ann} anotaciones ({len(new_verses)} versos nuevos, "
              f"{fixed} posiciones corregidas), {len(ch_out)}/{len(verse_map)} versos cubiertos")
        if missing:
            print(f"      faltan versos: {missing}")
        for issue in issues[:10]:
            print(f"      ⚠ {issue}")
        if len(issues) > 10:
            print(f"      ... y {len(issues) - 10} problemas más")

    tmp_path = path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    os.replace(tmp_path, path)
    print(f"\n  Guardado: {path} (+{total_new} anotaciones en esta corrida)")


if __name__ == "__main__":
    main()
