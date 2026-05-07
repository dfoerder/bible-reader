#!/usr/bin/env python3
"""Generate 'Vokabeln im Kontext' exercises from Bible annotations."""

import json, os, random
from collections import defaultdict

BASE = os.path.dirname(os.path.abspath(__file__))
BIBLE_DIR = os.path.join(BASE, '..', 'bibles', 'eng', 'web')
OUT = os.path.join(BASE, '..', 'data', 'context_exercises.json')

LEVELS = ['A2', 'B1', 'B2', 'C1', 'C2']

def load_bible_texts():
    """Load all verse texts keyed by (book_nr, chapter, verse)."""
    verses = {}
    for fname in os.listdir(BIBLE_DIR):
        if not fname.endswith('_web.json'):
            continue
        with open(os.path.join(BIBLE_DIR, fname)) as f:
            book = json.load(f)
        book_nr = book['nr']
        book_name = book['name']
        for ch in book['chapters']:
            ch_num = ch['number']
            for v in ch['verses']:
                verses[(book_nr, ch_num, v['n'])] = {
                    'text': v['text'],
                    'book_name': book_name
                }
    return verses

def load_annotations(path):
    """Load annotation file, yield (book_nr, chapter, verse, word_info)."""
    with open(path) as f:
        data = json.load(f)
    for book_nr, book_data in data.get('books', {}).items():
        if not isinstance(book_data, dict) or 'chapters' not in book_data:
            continue
        for chap_nr, chap_data in book_data['chapters'].items():
            if not isinstance(chap_data, dict):
                continue
            for verse_nr, words in chap_data.items():
                if not isinstance(words, list):
                    continue
                for w in words:
                    yield int(book_nr), int(chap_nr), int(verse_nr), w

def build_exercises():
    print("Loading Bible texts...")
    verses = load_bible_texts()

    print("Loading annotations...")
    nt_ann = os.path.join(BASE, 'nt_annotations_en.json')
    ot_ann = os.path.join(BASE, 'ot_annotations_en.json')

    # Collect candidates: group by (lemma, de, level)
    # Keep the best verse (longest text) per unique word
    candidates = defaultdict(list)
    for ann_path in [ot_ann, nt_ann]:
        if not os.path.exists(ann_path):
            print(f"  Skipping {ann_path} (not found)")
            continue
        print(f"  Processing {os.path.basename(ann_path)}...")
        for book_nr, chap, verse_n, w in load_annotations(ann_path):
            lvl = w.get('level', '')
            if lvl not in LEVELS:
                continue
            lemma = w.get('lemma', '')
            form = w.get('form', '')
            de = w.get('de', '')
            if not lemma or not de or not form:
                continue

            vkey = (book_nr, chap, verse_n)
            vinfo = verses.get(vkey)
            if not vinfo:
                continue
            text = vinfo['text']
            # Ensure the word actually appears in the verse
            if form.lower() not in text.lower():
                continue
            # Skip very short verses
            if len(text.split()) < 5:
                continue

            key = (lemma, de, lvl)
            candidates[key].append({
                'text': text,
                'form': form,
                'book': book_nr,
                'ref': f"{vinfo['book_name']} {chap}:{verse_n}"
            })

    print(f"  Found {len(candidates)} unique (lemma, de, level) combinations")

    # Build exercises: pick one good verse per word
    exercises = defaultdict(list)
    random.seed(42)

    for (lemma, de, lvl), verse_list in candidates.items():
        # Prefer medium-length verses (not too short, not too long)
        scored = sorted(verse_list, key=lambda v: abs(len(v['text'].split()) - 15))
        best = scored[0]
        text = best['text']
        form = best['form']

        # Mark the word position with ___ for the existing data format
        # Find the word in text (case-insensitive, whole word)
        import re
        pattern = re.compile(r'\b' + re.escape(form) + r'\b', re.IGNORECASE)
        match = pattern.search(text)
        if not match:
            continue

        marked_text = text[:match.start()] + '___' + text[match.end():]

        exercises[lvl].append({
            'text': marked_text,
            'answer': match.group(),
            'de': de,
            'ref': best['ref'],
            'book': best['book']
        })

    # Shuffle each level
    for lvl in exercises:
        random.shuffle(exercises[lvl])

    total = sum(len(v) for v in exercises.values())
    print(f"\nGenerated exercises per level:")
    for lvl in LEVELS:
        print(f"  {lvl}: {len(exercises.get(lvl, []))}")
    print(f"  Total: {total}")

    with open(OUT, 'w') as f:
        json.dump(exercises, f, ensure_ascii=False)
    print(f"\nSaved to {OUT} ({os.path.getsize(OUT) / 1024 / 1024:.1f} MB)")

if __name__ == '__main__':
    build_exercises()
