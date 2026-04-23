#!/usr/bin/env python3
"""
  Add A1/A2 annotations to existing annotation files.
  Merges new A1/A2 annotations with existing B1+ annotations.

  SETUP:
    export ANTHROPIC_API_KEY="sk-ant-..."
    python3 annotate_a1a2.py

  Requires bible_nt_en.json and nt_annotations_en.json.
"""
import json
import urllib.request
import os
import sys
import time
import re

API_URL  = "https://api.anthropic.com/v1/messages"
MODEL    = "claude-sonnet-4-20250514"

# Configure what to annotate
BIBLE_FILE  = "bible_ot_en.json"
ANNO_FILE   = "ot_annotations_en.json"
ONLY_BOOKS  = [1,2,3,4,5]  # Pentateuch

API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
if not API_KEY:
    print("\n  No API key! Set: export ANTHROPIC_API_KEY='sk-ant-...'\n")
    sys.exit(1)

SYSTEM_PROMPT = """You are an expert linguist in English as a foreign language (EFL) and German.

Your task: For a given Bible chapter, annotate EVERY word that is not already annotated at B1+ level.
This means: annotate all A1 and A2 words, including function words.

For each annotated word, provide:
- "pos": word position in the verse (0-indexed, counting each space-separated word)
- "form": the word as it appears in the text (inflected form)
- "lemma": the base form / infinitive / canonical form of the word
- "level": the CEFR level of the LEMMA (A1 or A2)
- "de": the correct German translation IN THIS SPECIFIC CONTEXT

Important rules:
1. ONLY annotate A1 and A2 words. Do NOT annotate B1, B2, C1, C2 words.
2. Do NOT annotate proper nouns (God, Jesus, Moses, Abraham, Israel, Jerusalem, Galilee, Egypt, etc.)
3. DO annotate EVERYTHING else, including:
   - Articles: the → der/die/das (context-dependent!), a/an → ein/eine
   - Pronouns: he → er, she → sie, it → es, they → sie, him → ihm/ihn, we → wir, etc.
   - Prepositions: in → in, on → auf, to → zu/nach, from → von, with → mit, by → von/bei, for → für, of → von, etc.
   - Conjunctions: and → und, or → oder, but → aber, if → wenn/falls, because → weil, when → als/wenn, etc.
   - Auxiliary verbs: is → ist, was → war, were → waren, has → hat, had → hatte, will → wird, etc.
   - Demonstratives: this → dieser/diese/dieses, that → jener/das, these → diese, those → jene
   - Adverbs: not → nicht, also → auch, very → sehr, here → hier, there → dort, now → jetzt, then → dann, etc.
   - Negation: no → kein/nein, not → nicht, never → nie
   - Quantifiers: all → alle, some → einige, many → viele, much → viel, every → jeder, each → jeder
4. The German translation MUST match the meaning IN THIS SPECIFIC VERSE context
   - "the man" → "der Mann", "the woman" → "die Frau", "the house" → "das Haus"
   - "to" before a place → "nach", "to" before a person → "zu", "to" as infinitive marker → "zu"
   - "that" as conjunction → "dass", "that" as demonstrative → "jener/das"
   - "was" as past of "be" → "war", "were" → "waren"

Response FORMAT — ONLY a JSON object, no markdown or comments:
{
  "1": [{"pos":0,"form":"The","lemma":"the","level":"A1","de":"Das"}, {"pos":2,"form":"came","lemma":"come","level":"A1","de":"kam"}, ...],
  "2": [...]
}

Keys are verse numbers (as strings). Values are arrays of annotations for that verse."""


def _normalize(word):
    return re.sub(r"[.,;:!?()\[\]\"\u2019\u2018\u00AB\u00BB\u2014\u2013\u2026*]", "", word).lower()


def correct_positions(chapter_annotations, chapter):
    corrections = 0
    verse_map = {str(v["n"]): v["text"] for v in chapter["verses"]}

    for verse_key, annotations in chapter_annotations.items():
        text = verse_map.get(verse_key, "")
        if not text:
            continue
        words = text.split()

        for ann in annotations:
            pos  = ann.get("pos", -1)
            form = ann.get("form", "")
            form_norm = _normalize(form)
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

    return corrections


CHUNK_SIZE = 15  # max verses per API call


def _call_api(book_name, chapter_num, verses_text, label=""):
    payload = json.dumps({
        "model": MODEL,
        "max_tokens": 16000,
        "system": SYSTEM_PROMPT,
        "messages": [{
            "role": "user",
            "content": (
                f"Here are verses from chapter {chapter_num} of {book_name} "
                f"(World English Bible){label}.\n"
                "Annotate every A1/A2 word with its form, lemma, "
                "CEFR level and contextual German translation.\n\n"
                f"{verses_text}\n\n"
                "Return ONLY the JSON object."
            )
        }]
    }).encode("utf-8")

    req = urllib.request.Request(API_URL, data=payload, headers={
        "Content-Type": "application/json",
        "x-api-key": API_KEY,
        "anthropic-version": "2023-06-01"
    })

    with urllib.request.urlopen(req, timeout=180) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        text = data["content"][0]["text"].strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1]
        if text.endswith("```"):
            text = text[:-3]
        return json.loads(text.strip())


def annotate_chapter(book_name, chapter_num, chapter):
    verses = chapter["verses"]
    if len(verses) <= CHUNK_SIZE:
        verses_text = "\n".join(f"{v['n']}. {v['text']}" for v in verses)
        return _call_api(book_name, chapter_num, verses_text)

    # Split into chunks
    merged = {}
    chunks = [verses[i:i+CHUNK_SIZE] for i in range(0, len(verses), CHUNK_SIZE)]
    for ci, chunk in enumerate(chunks):
        verses_text = "\n".join(f"{v['n']}. {v['text']}" for v in chunk)
        label = f" (part {ci+1}/{len(chunks)})"
        result = _call_api(book_name, chapter_num, verses_text, label)
        if isinstance(result, dict):
            merged.update(result)
        time.sleep(1)
    return merged


def merge_annotations(existing_chapter, new_a1a2_chapter):
    """Merge new A1/A2 annotations into existing chapter annotations."""
    merged = {}
    all_verses = set(list(existing_chapter.keys()) + list(new_a1a2_chapter.keys()))

    for verse_key in all_verses:
        existing = existing_chapter.get(verse_key, [])
        new_anns = new_a1a2_chapter.get(verse_key, [])

        existing_positions = {(a["pos"], _normalize(a["form"])) for a in existing}

        combined = list(existing)
        for ann in new_anns:
            key = (ann["pos"], _normalize(ann["form"]))
            if key not in existing_positions:
                combined.append(ann)

        combined.sort(key=lambda a: a.get("pos", 0))
        merged[verse_key] = combined

    return merged


def main():
    print()
    print("=" * 58)
    print("  Add A1/A2 annotations")
    print(f"  Books: {ONLY_BOOKS}")
    print("=" * 58)
    print()

    with open(BIBLE_FILE, "r", encoding="utf-8") as f:
        bible = json.load(f)

    with open(ANNO_FILE, "r", encoding="utf-8") as f:
        anno_data = json.load(f)

    books = anno_data.get("books", {})

    target_books = [b for b in bible.get("books", [])
                    if b.get("nr") in ONLY_BOOKS]

    # Track progress in a separate file
    progress_file = "a1a2_progress.json"
    done_chapters = {}
    if os.path.exists(progress_file):
        with open(progress_file, "r") as f:
            done_chapters = json.load(f)

    for book in target_books:
        book_nr   = str(book.get("nr"))
        book_name = book["name"]
        chapters  = book.get("chapters", [])
        total_ch  = len(chapters)

        book_done = done_chapters.get(book_nr, [])

        remaining = [c for c in chapters if str(c["number"]) not in book_done]
        if not remaining:
            print(f"  {book_name}: already complete")
            continue

        print(f"  {book_name} ({total_ch} chapters, {len(book_done)} already done)")
        print(f"  {'-' * 50}")

        if book_nr not in books:
            books[book_nr] = {"name": book_name, "chapters": {}}

        failed = []

        for chapter in remaining:
            ch_num = str(chapter["number"])

            print(f"    Ch {ch_num.rjust(3)}/{total_ch} ...", end=" ", flush=True)

            try:
                new_annotations = annotate_chapter(book_name, chapter["number"], chapter)

                if not isinstance(new_annotations, dict):
                    failed.append(ch_num)
                    print("FAIL: invalid format")
                    continue

                fixed = correct_positions(new_annotations, chapter)
                new_count = sum(len(v) for v in new_annotations.values())

                existing_chapter = books[book_nr]["chapters"].get(ch_num, {})
                merged = merge_annotations(existing_chapter, new_annotations)
                total_after = sum(len(v) for v in merged.values())

                books[book_nr]["chapters"][ch_num] = merged
                fix_note = f" [{fixed} corr.]" if fixed else ""
                print(f"OK +{new_count} A1/A2, total {total_after}{fix_note}")

                # Save annotation file
                anno_data["books"] = books
                anno_data["total_annotations"] = sum(
                    sum(len(anns) for anns in ch.values())
                    for bk in books.values()
                    for ch in bk["chapters"].values()
                )
                anno_data["levels"] = "A1, A2, B1, B2, C1, C2"
                with open(ANNO_FILE, "w", encoding="utf-8") as f:
                    json.dump(anno_data, f, ensure_ascii=False, indent=2)

                # Save progress
                if book_nr not in done_chapters:
                    done_chapters[book_nr] = []
                done_chapters[book_nr].append(ch_num)
                with open(progress_file, "w") as f:
                    json.dump(done_chapters, f)

            except Exception as e:
                failed.append(ch_num)
                print(f"FAIL: {str(e)[:80]}")

            time.sleep(1)

        if failed:
            print(f"\n    Retrying {len(failed)} failed chapters ...")
            for ch_num in failed[:]:
                chapter = next(
                    (c for c in chapters if str(c["number"]) == ch_num), None
                )
                if not chapter:
                    continue
                print(f"    Retry ch {ch_num} ...", end=" ", flush=True)
                time.sleep(3)
                try:
                    new_annotations = annotate_chapter(book_name, int(ch_num), chapter)
                    if isinstance(new_annotations, dict):
                        fixed = correct_positions(new_annotations, chapter)
                        new_count = sum(len(v) for v in new_annotations.values())
                        existing_chapter = books[book_nr]["chapters"].get(ch_num, {})
                        merged = merge_annotations(existing_chapter, new_annotations)
                        total_after = sum(len(v) for v in merged.values())
                        books[book_nr]["chapters"][ch_num] = merged
                        fix_note = f" [{fixed} corr.]" if fixed else ""
                        failed.remove(ch_num)
                        print(f"OK +{new_count} A1/A2, total {total_after}{fix_note}")

                        anno_data["books"] = books
                        anno_data["total_annotations"] = sum(
                            sum(len(anns) for anns in ch.values())
                            for bk in books.values()
                            for ch in bk["chapters"].values()
                        )
                        anno_data["levels"] = "A1, A2, B1, B2, C1, C2"
                        with open(ANNO_FILE, "w", encoding="utf-8") as f:
                            json.dump(anno_data, f, ensure_ascii=False, indent=2)

                        if book_nr not in done_chapters:
                            done_chapters[book_nr] = []
                        done_chapters[book_nr].append(ch_num)
                        with open(progress_file, "w") as f:
                            json.dump(done_chapters, f)
                    else:
                        print("FAIL")
                except Exception as e:
                    print(f"FAIL: {str(e)[:80]}")

        if failed:
            print(f"\n  Failed chapters: {failed}")
            print("  Run script again to retry.")

    total = anno_data.get("total_annotations", 0)
    print()
    print("=" * 58)
    print(f"  Done. Total annotations in {ANNO_FILE}: {total}")
    print("=" * 58)
    print()


if __name__ == "__main__":
    main()
