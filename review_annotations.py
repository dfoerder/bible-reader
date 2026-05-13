#!/usr/bin/env python3
"""
Review and improve word-by-word annotations for one chapter.

Philosophy:
  - Word-by-word translation when the German is understandable
  - Multi-word phrases when word-by-word would be incomprehensible
    (idioms, phrasal verbs, fixed expressions)
  - Every word in the verse gets an annotation (A1–C2)
  - Correct positions for every word occurrence

Usage:
  export ANTHROPIC_API_KEY="sk-ant-..."
  python3 review_annotations.py              # default: Matthew ch 1
  python3 review_annotations.py 40 1         # book_nr chapter_nr
"""
import json, os, sys, urllib.request, re, copy, time

API_URL = "https://api.anthropic.com/v1/messages"
MODEL = os.environ.get("REVIEW_MODEL", "claude-sonnet-4-20250514")

BIBLE_DIR = "bibles/eng/web"
ANNO_DIR = "bibles/eng/web/anno"

API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
if not API_KEY:
    print("\n  ⚠  No API key! → export ANTHROPIC_API_KEY='sk-ant-...'\n")
    sys.exit(1)

BOOK_NR = int(sys.argv[1]) if len(sys.argv) > 1 else 40
CHAP_NR = int(sys.argv[2]) if len(sys.argv) > 2 else 1

SYSTEM_PROMPT = """\
You are an expert linguist reviewing English→German word-by-word Bible annotations.

## Translation philosophy

The goal is to help German-speaking learners (A2+) understand the English Bible text.

1. **Word-by-word is the default.** Translate each English word individually into German, \
   using the contextually correct German word. The result should be understandable when \
   reading word-by-word under the English text.

2. **Multi-word phrases** are ONLY used when word-by-word translation would be \
   incomprehensible or seriously misleading. Examples:
   - Idioms: "be with child" → "schwanger sein" (word-by-word "sein mit Kind" is nonsensical)
   - Phrasal verbs: "put away" → "entlassen/verlassen" ("put" + "away" separately misleads)
   - Fixed expressions: "give birth to" → "gebären"
   - BUT: "became the father of" works fine word-by-word ("wurde der Vater von") → keep as single words

3. **Every word** in the verse must be annotated — A1 through C2.

4. **Proper nouns** (Jesus, Abraham, David, Babylon, etc.) are NOT annotated.

5. **Positions** must be exact: pos = 0-based index of the word in the verse (split by spaces). \
   Each occurrence of a word gets its OWN annotation at its OWN position. \
   If "the" appears at positions 0, 3, and 8, there must be three separate annotations.

6. **Multi-word phrases** use "pos" for the first word and "pos_end" for the last word. \
   The individual words covered by a phrase do NOT get separate annotations.

7. **German translations** must be contextually correct and natural:
   - Match grammatical form (case, number, tense) to the English word's role in the sentence
   - "found" in "was found pregnant" → "befunden" (not "befand" which means "sich befinden")
   - "afraid" in "be afraid" → as part of phrase "sich fürchten" (not "fürchte" alone)
   - "sexually" → "geschlechtlich" (not "erkannte" which duplicates the verb)

## Output format

Return ONLY a JSON object. Keys = verse numbers (strings). Values = arrays of annotations.

Single word:
  {"pos": 3, "form": "father", "lemma": "father", "level": "A1", "de": "Vater"}

Multi-word phrase:
  {"pos": 2, "pos_end": 4, "form": "give birth to", "lemma": "give birth to", "level": "B1", "de": "gebären"}

CEFR levels: A1, A2, B1, B2, C1, C2"""


def load_bible_chapter(book_nr, chap_nr):
    path = os.path.join(BIBLE_DIR, f"{book_nr}_web.json")
    with open(path, "r", encoding="utf-8") as f:
        book = json.load(f)
    for ch in book["chapters"]:
        if ch["number"] == chap_nr:
            return book["name"], ch
    raise ValueError(f"Chapter {chap_nr} not found in book {book_nr}")


def load_annotations(book_nr, chap_nr):
    path = os.path.join(ANNO_DIR, f"{book_nr}_web_deu.json")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data, data["chapters"].get(str(chap_nr), {})


def format_verse_with_positions(verse_text):
    words = verse_text.split()
    return "  ".join(f"[{i}]{w}" for i, w in enumerate(words))


def call_api(user_message, max_retries=3):
    payload = json.dumps({
        "model": MODEL,
        "max_tokens": 32000,
        "system": SYSTEM_PROMPT,
        "messages": [{"role": "user", "content": user_message}]
    }).encode("utf-8")

    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(API_URL, data=payload, headers={
                "Content-Type": "application/json",
                "x-api-key": API_KEY,
                "anthropic-version": "2023-06-01"
            })

            with urllib.request.urlopen(req, timeout=600) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                text = data["content"][0]["text"].strip()
                if text.startswith("```"):
                    text = text.split("\n", 1)[1]
                if text.endswith("```"):
                    text = text[:-3]
                text = text.strip()
                if not text.startswith("{"):
                    idx = text.find("{")
                    if idx >= 0:
                        text = text[idx:]
                try:
                    return json.loads(text)
                except json.JSONDecodeError:
                    print(f"\n  ⚠ JSON parse error. Length: {len(text)}")
                    print(f"  First 200: {text[:200]}")
                    print(f"  Last 200: {text[-200:]}")
                    raise

        except Exception as e:
            if attempt < max_retries - 1:
                wait = (attempt + 1) * 15
                print(f"\n  ⚠ {str(e)[:60]} — retry in {wait}s...", end=" ", flush=True)
                time.sleep(wait)
            else:
                raise


def analyze_verse_problems(vnum, text, annotations):
    """Identify specific problems in a verse's annotations to guide the API."""
    problems = []
    words = text.split()
    annotated_positions = set()

    for a in annotations:
        pos = a["pos"]
        pos_end = a.get("pos_end", pos)
        for p in range(pos, pos_end + 1):
            annotated_positions.add(p)

    # Check for duplicate positions (multiple annotations at same pos, not phrase)
    pos_counts = {}
    for a in annotations:
        if "pos_end" not in a:
            pos_counts[a["pos"]] = pos_counts.get(a["pos"], 0) + 1
    for pos, count in pos_counts.items():
        if count > 1 and pos < len(words):
            problems.append(
                f"  ⚠ pos {pos} ({words[pos]}): {count} duplicate annotations — "
                f"likely different occurrences mapped to same position"
            )

    # Check for missing word positions (not annotated, not proper noun)
    proper_nouns = {
        "jesus", "christ", "abraham", "isaac", "jacob", "judah", "perez",
        "zerah", "tamar", "hezron", "ram", "amminadab", "nahshon", "salmon",
        "boaz", "rahab", "obed", "ruth", "jesse", "david", "solomon",
        "uriah", "rehoboam", "abijah", "asa", "jehoshaphat", "joram",
        "uzziah", "jotham", "ahaz", "hezekiah", "manasseh", "amon",
        "josiah", "jechoniah", "babylon", "shealtiel", "zerubbabel",
        "abiud", "eliakim", "azor", "zadok", "achim", "eliud", "eleazar",
        "matthan", "joseph", "mary", "immanuel", "god",
    }
    for i, w in enumerate(words):
        clean = re.sub(r'[.,;:!?"“”‘’()\[\]]', '', w).lower()
        if i not in annotated_positions and clean and clean not in proper_nouns:
            problems.append(f"  ⚠ pos {i} ({w}): not annotated")

    return problems


def analyze_translation_quality(vnum, text, annotations):
    """Flag translations that are likely wrong or need multi-word treatment."""
    problems = []
    words = text.lower().split()

    ann_by_pos = {}
    for a in annotations:
        ann_by_pos.setdefault(a["pos"], []).append(a)

    # Known problematic patterns to check
    for a in annotations:
        form_lower = a["form"].lower()
        de = a["de"]

        # "being" → "seiend" is unnatural German
        if form_lower == "being" and de == "seiend":
            problems.append(
                f'  ⚠ pos {a["pos"]}: "being" → "seiend" is unnatural German. '
                f'Consider context: maybe "da er/sie ... war" or a phrase.'
            )

        # "the" translated as a content word (e.g. "Herrn")
        if form_lower == "the" and de not in (
            "der", "die", "das", "dem", "den", "des"
        ):
            problems.append(
                f'  ⚠ pos {a["pos"]}: "the" → "{de}" — articles should only '
                f'translate to der/die/das/dem/den/des. The content meaning '
                f'belongs to the next word.'
            )

    # Check for phrasal verbs / idioms that should be multi-word
    text_lower = text.lower()
    phrase_checks = [
        ("make her a public example", "bloßstellen / zum Beispiel machen"),
        ("make him a public example", "bloßstellen / zum Beispiel machen"),
        ("at the time of", "zur Zeit"),
        ("came together", "zusammenkamen"),
        ("put away", "entlassen / verlassen"),
        ("be with child", "schwanger sein"),
        ("be afraid", "sich fürchten"),
        ("passed away", "verstarb / verging"),
        ("fell asleep", "schlief ein"),
        ("cast out", "austreiben / hinauswerfen"),
        ("set apart", "aussondern"),
        ("laid hands on", "die Hände auflegen"),
    ]
    for phrase, suggestion in phrase_checks:
        if phrase in text_lower:
            # Check if already handled as multi-word
            already_phrase = any(
                " " in a["form"] and phrase in a["form"].lower()
                for a in annotations
            )
            if not already_phrase:
                problems.append(
                    f'  ⚠ "{phrase}" should be a multi-word phrase → {suggestion}'
                )

    return problems


def build_user_message(book_name, chap_nr, chapter, old_annotations):
    lines = []
    lines.append(
        f"Review and correct the annotations for {book_name} chapter {chap_nr} "
        f"(World English Bible).\n"
    )

    for verse in chapter["verses"]:
        vnum = str(verse["n"])
        text = verse["text"]
        positioned = format_verse_with_positions(text)

        lines.append(f"--- Verse {vnum} ---")
        lines.append(f"Text: {text}")
        lines.append(f"Positions: {positioned}")

        old = old_annotations.get(vnum, [])
        if old:
            lines.append("Current annotations:")
            for a in sorted(old, key=lambda x: x["pos"]):
                pe = f"-{a['pos_end']}" if "pos_end" in a else ""
                lines.append(
                    f"  [{a['pos']}{pe}] {a['form']} → {a['de']}  "
                    f"({a['level']}, lemma: {a['lemma']})"
                )

        # Add specific problems found by analysis
        struct_problems = analyze_verse_problems(vnum, text, old)
        trans_problems = analyze_translation_quality(vnum, text, old)
        all_problems = struct_problems + trans_problems
        if all_problems:
            lines.append("PROBLEMS FOUND — you MUST fix these:")
            lines.extend(all_problems)

        lines.append("")

    lines.append(
        "Fix ALL flagged problems. Also fix any other issues you notice: "
        "wrong translations, missing multi-word phrases, wrong positions, "
        "duplicate entries. Return the complete corrected annotations as JSON."
    )
    return "\n".join(lines)


def _normalize(word):
    return re.sub(r"[.,;:!?()\[\]\"“”’‘«»—–…*]", "", word).lower()


def validate_and_fix(result, chapter):
    """Validate annotations: form must match word at pos. Fix or flag mismatches."""
    verse_map = {str(v["n"]): v["text"] for v in chapter["verses"]}
    issues = []
    fixes = 0

    for vnum, annotations in result.items():
        text = verse_map.get(vnum, "")
        if not text:
            issues.append(f"V{vnum}: verse not found in text")
            continue
        words = text.split()

        for a in annotations:
            pos = a.get("pos", -1)
            pos_end = a.get("pos_end", pos)
            form = a.get("form", "")

            if pos < 0 or pos >= len(words):
                issues.append(f"V{vnum}: pos {pos} out of range for '{form}'")
                continue
            if pos_end >= len(words):
                issues.append(f"V{vnum}: pos_end {pos_end} out of range for '{form}'")
                continue

            # For single words, check form matches
            if "pos_end" not in a:
                actual = _normalize(words[pos])
                expected = _normalize(form)
                if actual != expected:
                    # Try to find the right position
                    found = False
                    for i, w in enumerate(words):
                        if _normalize(w) == expected:
                            a["pos"] = i
                            fixes += 1
                            found = True
                            break
                    if not found:
                        issues.append(
                            f"V{vnum}: pos {pos} has '{words[pos]}' but "
                            f"annotation says '{form}' — MISMATCH"
                        )
            else:
                # For multi-word, check first word matches
                actual = _normalize(words[pos])
                first_form = _normalize(form.split()[0])
                if actual != first_form:
                    issues.append(
                        f"V{vnum}: phrase '{form}' at pos {pos} — "
                        f"text has '{words[pos]}'"
                    )

    return issues, fixes


def print_diff(old_annotations, new_annotations, chapter):
    """Show what changed."""
    verse_map = {str(v["n"]): v["text"] for v in chapter["verses"]}

    for vnum in sorted(new_annotations.keys(), key=int):
        text = verse_map.get(vnum, "")
        old = {(a["pos"], a.get("pos_end", a["pos"]), a["form"]): a
               for a in old_annotations.get(vnum, [])}
        new = {(a["pos"], a.get("pos_end", a["pos"]), a["form"]): a
               for a in new_annotations.get(vnum, [])}

        changes = []

        # Find changed/new annotations
        for key, a in new.items():
            if key not in old:
                old_at_pos = [o for o in old_annotations.get(vnum, [])
                              if o["pos"] == a["pos"]]
                if old_at_pos:
                    for o in old_at_pos:
                        changes.append(
                            f"  CHANGED: [{a['pos']}] "
                            f"{o['form']}→{o['de']}  ➜  {a['form']}→{a['de']}"
                        )
                else:
                    changes.append(
                        f"  NEW:     [{a['pos']}] {a['form']} → {a['de']}"
                    )

        # Find removed annotations
        for key, a in old.items():
            if key not in new:
                new_at_pos = [n for n in new_annotations.get(vnum, [])
                              if n["pos"] == a["pos"]]
                if not new_at_pos:
                    changes.append(
                        f"  REMOVED: [{a['pos']}] {a['form']} → {a['de']}"
                    )

        if changes:
            print(f"\n  Vers {vnum}: {text[:80]}...")
            for c in changes:
                print(c)


def main():
    book_name, chapter = load_bible_chapter(BOOK_NR, CHAP_NR)
    anno_data, old_annotations = load_annotations(BOOK_NR, CHAP_NR)

    old_count = sum(len(v) for v in old_annotations.values())
    verses = chapter["verses"]
    print(f"\n  Reviewing: {book_name} chapter {CHAP_NR}")
    print(f"  Existing annotations: {old_count}")
    print(f"  Verses: {len(verses)}")

    CHUNK_SIZE = 5
    new_annotations = {}

    for i in range(0, len(verses), CHUNK_SIZE):
        chunk_verses = verses[i:i + CHUNK_SIZE]
        chunk_range = f"{chunk_verses[0]['n']}-{chunk_verses[-1]['n']}"

        # Build a sub-chapter with only these verses
        sub_chapter = {"number": chapter["number"], "verses": chunk_verses}
        sub_old = {str(v["n"]): old_annotations.get(str(v["n"]), [])
                   for v in chunk_verses}

        print(f"  Verses {chunk_range} — calling API ({MODEL})...", end=" ", flush=True)

        user_msg = build_user_message(book_name, CHAP_NR, sub_chapter, sub_old)
        chunk_result = call_api(user_msg)
        time.sleep(2)

        # Validate
        issues, fixes = validate_and_fix(chunk_result, sub_chapter)
        ann_count = sum(len(v) for v in chunk_result.values())
        fix_note = f" [{fixes} pos fixed]" if fixes else ""

        if issues:
            print(f"✓ {ann_count} ann{fix_note}")
            for issue in issues[:5]:
                print(f"    ⚠ {issue}")
        else:
            print(f"✓ {ann_count} annotations{fix_note}")

        new_annotations.update(chunk_result)

    new_count = sum(len(v) for v in new_annotations.values())
    print(f"\n  Total: {old_count} → {new_count} annotations")

    print("\n  ─── Changes ───")
    print_diff(old_annotations, new_annotations, chapter)

    # Backup and save
    anno_path = os.path.join(ANNO_DIR, f"{BOOK_NR}_web_deu.json")
    backup_path = anno_path + ".bak"

    print(f"\n  Saving backup → {backup_path}")
    with open(backup_path, "w", encoding="utf-8") as f:
        json.dump(anno_data, f, ensure_ascii=False, indent=2)

    anno_data["chapters"][str(CHAP_NR)] = new_annotations

    print(f"  Saving updated → {anno_path}")
    with open(anno_path, "w", encoding="utf-8") as f:
        json.dump(anno_data, f, ensure_ascii=False, indent=2)

    print(f"\n  ✓ Done. Review the app to check the result.\n")


if __name__ == "__main__":
    main()
