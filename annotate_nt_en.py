#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════
  New Testament — Word-by-word Annotation (English → German)

  Annotates every B1+ word in the English NT (WEB) with:
  - Word form (as in text)
  - Lemma (base form)
  - CEFR level (B1, B2, C1, C2)
  - Context-dependent German translation

  After each chapter, word positions are automatically
  verified and corrected against the source text.

  SETUP:
    export ANTHROPIC_API_KEY="sk-ant-..."
    python3 annotate_nt_en.py

  Requires bible_nt_en.json in the same folder.
  Saves after each chapter — can be restarted at any time.

  COST: approx. 60–90 USD for the full NT
═══════════════════════════════════════════════════════════════
"""
import json
import urllib.request
import os
import sys
import time
import re

API_URL  = "https://api.anthropic.com/v1/messages"
MODEL    = "claude-sonnet-4-20250514"
OUTPUT_FILE = "nt_annotations_en.json"
BIBLE_FILE  = "bible_nt_en.json"

# Which books to annotate (book numbers, None = all NT books)
# Gospels: 40=Matthew, 41=Mark, 42=Luke, 43=John
# Gospels + Acts: 40=Matthew, 41=Mark, 42=Luke, 43=John, 44=Acts
ONLY_BOOKS = [40, 41, 42, 43, 44]

API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
if not API_KEY:
    print("\n  ⚠  No API key! → export ANTHROPIC_API_KEY='sk-ant-...'\n")
    sys.exit(1)

if not os.path.exists(BIBLE_FILE):
    print(f"\n  ⚠  {BIBLE_FILE} not found!")
    print("  Run start.command first to download the Bible text.\n")
    sys.exit(1)

SYSTEM_PROMPT = """You are an expert linguist in English as a foreign language (EFL) and German.

Your task: For a given Bible chapter, annotate every word at CEFR level B1 or higher (B1, B2, C1, C2).

For each annotated word, provide:
- "pos": word position in the verse (0-indexed, counting each space-separated word)
- "form": the word as it appears in the text (inflected form)
- "lemma": the base form / infinitive / canonical form of the word
- "level": the CEFR level of the LEMMA (B1, B2, C1 or C2)
- "de": the correct German translation IN THIS SPECIFIC CONTEXT

Important rules:
1. Do NOT annotate A1 or A2 words (very common words like: be, have, do, make, say, go, see, can, want, know, must, take, put, give, man, woman, son, daughter, father, mother, brother, king, country, city, day, night, water, bread, house, earth, name, hand, eye, heart, life, death, all, nothing, big, small, good, new, first, other, same, little, very, well, also, still, always, never, here, where, when, how, why, because, so, but, with, in, on, under, to, for, by, without, between, since, before, after, against, the, a, an, this, that, etc.)
2. Do NOT annotate proper nouns (Jesus, Abraham, Matthew, Jerusalem, etc.)
3. Do NOT annotate articles, personal pronouns, simple prepositions, basic conjunctions
4. DO annotate archaic/literary forms common in Bible English (e.g. "behold", "rebuke", "exhort")
5. DO annotate religious/biblical vocabulary (baptize, prophet, crucify, etc.)
6. The German translation must match the meaning IN THIS SPECIFIC VERSE
   - Example: "spirit" can be "Geist" or "Verstand" depending on context
   - Example: "begat" in a genealogical context = "zeugte"
   - Example: "grace" in religious sense = "Gnade", as "thanks" = "Dank"

Response FORMAT — ONLY a JSON object, no markdown or comments:
{
  "1": [{"pos":2,"form":"begat","lemma":"beget","level":"C1","de":"zeugte"}, ...],
  "2": [...]
}

Keys are verse numbers (as strings). Values are arrays of annotations for that verse.
If a verse has no B1+ words, use an empty array: "5": []"""


# ─── Position correction ─────────────────────────────────────────────────────

def _normalize(word):
    """Strip punctuation and lowercase for comparison."""
    return re.sub(r"[.,;:!?()\[\]\"\u2019\u2018\u00AB\u00BB\u2014\u2013\u2026*]", "", word).lower()


def correct_positions(chapter_annotations, chapter):
    """
    After each API call, verify that annotation["pos"] actually points to
    annotation["form"] in the verse text. Correct silently when possible.
    Returns the number of corrected entries.
    """
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

            # Check if current pos is already correct
            if 0 <= pos < len(words) and _normalize(words[pos]) == form_norm:
                continue

            # Search the verse for the correct position
            found = -1
            for i, w in enumerate(words):
                if _normalize(w) == form_norm:
                    found = i
                    break

            if found >= 0:
                ann["pos"] = found
                corrections += 1

    return corrections


# ─── API call ─────────────────────────────────────────────────────────────────

def annotate_chapter(book_name, chapter_num, verses_text):
    """Call the Claude API to annotate one chapter."""
    payload = json.dumps({
        "model": MODEL,
        "max_tokens": 16000,
        "system": SYSTEM_PROMPT,
        "messages": [{
            "role": "user",
            "content": (
                f"Here is chapter {chapter_num} of {book_name} "
                f"(World English Bible).\n"
                "Annotate every word at level B1+ with its form, lemma, "
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
        # Strip optional markdown code fences
        if text.startswith("```"):
            text = text.split("\n", 1)[1]
        if text.endswith("```"):
            text = text[:-3]
        return json.loads(text.strip())


# ─── Persistence ──────────────────────────────────────────────────────────────

def load_progress():
    """Load existing output file; return books dict keyed by book nr (str)."""
    if not os.path.exists(OUTPUT_FILE):
        return {}
    try:
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("books", {})
    except Exception:
        return {}


def save_progress(books):
    total_words = sum(
        sum(len(anns) for anns in ch.values())
        for bk in books.values()
        for ch in bk["chapters"].values()
    )
    output = {
        "description": (
            "Word-by-word annotations NT (English): "
            "Lemma, CEFR level, context-dependent DE translation"
        ),
        "levels": "B1, B2, C1, C2 (A1/A2 omitted)",
        "total_annotations": total_words,
        "books": books
    }
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    print()
    print("═" * 58)
    print("  New Testament — Word-by-word Annotation (EN→DE)")
    print("  All 27 books · Lemma · CEFR · German Translation")
    print("═" * 58)
    print()

    with open(BIBLE_FILE, "r", encoding="utf-8") as f:
        bible = json.load(f)

    nt_books = [b for b in bible.get("books", [])
                if ONLY_BOOKS is None or b.get("nr") in ONLY_BOOKS]
    total_books = len(nt_books)
    total_chapters_all = sum(len(b.get("chapters", [])) for b in nt_books)
    print(f"  {total_books} books · {total_chapters_all} chapters total\n")

    books = load_progress()
    if books:
        done_ch = sum(len(bk["chapters"]) for bk in books.values())
        print(f"  ℹ Progress: {done_ch}/{total_chapters_all} chapters already annotated\n")

    grand_failed = []

    for book_idx, book in enumerate(nt_books, 1):
        book_nr   = str(book.get("nr", book_idx + 39))
        book_name = book["name"]
        chapters  = book.get("chapters", [])
        total_ch  = len(chapters)

        if book_nr not in books:
            books[book_nr] = {"name": book_name, "chapters": {}}

        book_chapters = books[book_nr]["chapters"]
        remaining = [c for c in chapters if str(c["number"]) not in book_chapters]

        if not remaining:
            print(f"  [{book_idx:2}/{total_books}] {book_name}: already complete ✓")
            continue

        done = len(book_chapters)
        print(f"\n  [{book_idx:2}/{total_books}] {book_name} ({total_ch} chapters, {done} already done)")
        print(f"  {'─' * 50}")

        failed = []

        for chapter in remaining:
            ch_num = str(chapter["number"])
            verses_text = "\n".join(
                f"{v['n']}. {v['text']}" for v in chapter["verses"]
            )

            print(f"    Ch {ch_num.rjust(3)}/{total_ch} ...", end=" ", flush=True)

            try:
                annotations = annotate_chapter(book_name, chapter["number"], verses_text)

                if not isinstance(annotations, dict):
                    failed.append(ch_num)
                    print("✗ invalid format")
                    continue

                fixed = correct_positions(annotations, chapter)
                total_ann = sum(len(v) for v in annotations.values())
                fix_note  = f" [{fixed} corr.]" if fixed else ""

                book_chapters[ch_num] = annotations
                print(f"✓ {total_ann} annotations{fix_note}")
                save_progress(books)

            except Exception as e:
                failed.append(ch_num)
                print(f"✗ {str(e)[:80]}")

            time.sleep(1)

        # ── Retry failed chapters ──────────────────────────────────────────
        if failed:
            print(f"\n    Retrying {len(failed)} failed chapters ...")
            for ch_num in failed[:]:
                chapter = next(
                    (c for c in chapters if str(c["number"]) == ch_num), None
                )
                if not chapter:
                    continue
                verses_text = "\n".join(
                    f"{v['n']}. {v['text']}" for v in chapter["verses"]
                )
                print(f"    Retry ch {ch_num} ...", end=" ", flush=True)
                time.sleep(3)
                try:
                    annotations = annotate_chapter(
                        book_name, int(ch_num), verses_text
                    )
                    if isinstance(annotations, dict):
                        fixed = correct_positions(annotations, chapter)
                        total_ann = sum(len(v) for v in annotations.values())
                        fix_note  = f" [{fixed} corr.]" if fixed else ""
                        book_chapters[ch_num] = annotations
                        failed.remove(ch_num)
                        print(f"✓ {total_ann} annotations{fix_note}")
                        save_progress(books)
                    else:
                        print("✗")
                except Exception as e:
                    print(f"✗ {str(e)[:80]}")

        grand_failed.extend([(book_name, ch) for ch in failed])

    save_progress(books)

    # ── Summary ───────────────────────────────────────────────────────────────
    total_words = sum(
        sum(len(anns) for anns in ch.values())
        for bk in books.values()
        for ch in bk["chapters"].values()
    )
    done_ch = sum(len(bk["chapters"]) for bk in books.values())

    print()
    print("═" * 58)
    print(f"  ✓ {done_ch}/{total_chapters_all} chapters annotated")
    print(f"  ✓ {total_words} words annotated")
    if grand_failed:
        print(f"  ⚠  Failed:")
        for bk, ch in grand_failed:
            print(f"     {bk} ch. {ch}")
        print("  → Run script again to continue")
    print(f"  ✓ Saved: {OUTPUT_FILE}")
    print()


if __name__ == "__main__":
    main()
