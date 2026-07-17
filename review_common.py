#!/usr/bin/env python3
"""Shared functions for annotation review scripts."""
import json, os, re

BIBLE_DIR = "bibles/eng/web"
ANNO_DIR = "bibles/eng/web/anno"

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
   - Phrasal verbs where meaning shifts: "put away" → "entlassen" ("put" + "away" separately misleads)
   - Fixed expressions: "give birth to" → "gebären"
   - BUT: "became the father of" works fine word-by-word ("wurde der Vater von") → keep as single words
   - BUT: transparent phrasal verbs like "came out" (kam heraus), "went up" (ging hinauf), \
     "put down" (legte nieder) work fine word-by-word → keep as single words, NOT as phrases

3. **Every word** in the verse must be annotated — A1 through C2.

4. **Proper nouns** (Jesus, Abraham, David, Babylon, etc.) MUST be annotated with their \
   German equivalent. Examples: Christ → Christus, Moses → Mose, Egypt → Ägypten, \
   Isaiah → Jesaja, Pharaoh → Pharao. Names that stay the same (Jesus, Abraham, Jerusalem) \
   still get an annotation with the same word as "de". Level is always A1.

5. **Positions** must be exact: pos = 0-based index of the word in the verse (split by spaces). \
   Each occurrence of a word gets its OWN annotation at its OWN position. \
   If "the" appears at positions 0, 3, and 8, there must be three separate annotations.

6. **Multi-word phrases** use "pos" for the first word and "pos_end" for the last word. \
   Words covered by a phrase MUST ALSO get their own individual single-word annotations. \
   This allows the app to show the phrase translation first, then individual word translations on tap.

7. **German translations** must be contextually correct and natural:
   - Match grammatical form (case, number, tense) to the English word's role in the sentence
   - "found" in "was found pregnant" → "befunden" (not "befand" which means "sich befinden")
   - "afraid" in "be afraid" → as part of phrase "sich fürchten" (not "fürchte" alone)
   - "sexually" → "geschlechtlich" (not "erkannte" which duplicates the verb)

## Output format

Return ONLY a JSON object. Keys = verse numbers (strings). Values = arrays of annotations.

Single word:
  {"pos": 3, "form": "father", "lemma": "father", "level": "A1", "de": "Vater"}

Multi-word phrase — include the phrase AND individual annotations for each word:
  {"pos": 2, "pos_end": 4, "form": "give birth to", "lemma": "give birth to", "level": "B1", "de": "gebären"},
  {"pos": 2, "form": "give", "lemma": "give", "level": "A1", "de": "geben"},
  {"pos": 3, "form": "birth", "lemma": "birth", "level": "A2", "de": "Geburt"},
  {"pos": 4, "form": "to", "lemma": "to", "level": "A1", "de": "zu"}

CEFR levels: A1, A2, B1, B2, C1, C2"""


def _chapters_as_array(book):
    """Quellformat ist einheitlich dict ({chapters:{cn:{vn:text}}}). Für die
    Review-Logik in die array-Form ({number, verses:[{n,text}]}) bringen —
    numerisch sortiert. (Alt-array wird rückwärtskompatibel durchgereicht.)"""
    raw = book["chapters"]
    if isinstance(raw, list):
        return raw
    out = []
    for cn in sorted(raw.keys(), key=int):
        verses = [{"n": int(vn), "text": t}
                  for vn, t in sorted(raw[cn].items(), key=lambda x: int(x[0]))]
        out.append({"number": int(cn), "verses": verses})
    return out


def load_bible_chapter(book_nr, chap_nr):
    path = os.path.join(BIBLE_DIR, f"{book_nr}_web.json")
    with open(path, "r", encoding="utf-8") as f:
        book = json.load(f)
    for ch in _chapters_as_array(book):
        if ch["number"] == chap_nr:
            return book["name"], ch
    raise ValueError(f"Chapter {chap_nr} not found in book {book_nr}")


def load_book(book_nr):
    path = os.path.join(BIBLE_DIR, f"{book_nr}_web.json")
    with open(path, "r", encoding="utf-8") as f:
        book = json.load(f)
    return book["name"], _chapters_as_array(book)


def load_annotations(book_nr, chap_nr=None):
    path = os.path.join(ANNO_DIR, f"{book_nr}_web_deu.json")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if chap_nr is not None:
        return data, data["chapters"].get(str(chap_nr), {})
    return data


def format_verse_with_positions(verse_text):
    words = verse_text.split()
    return "  ".join(f"[{i}]{w}" for i, w in enumerate(words))


def analyze_verse_problems(vnum, text, annotations):
    problems = []
    words = text.split()
    annotated_positions = set()

    for a in annotations:
        pos = a["pos"]
        pos_end = a.get("pos_end", pos)
        for p in range(pos, pos_end + 1):
            annotated_positions.add(p)

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

    for i, w in enumerate(words):
        clean = re.sub(r'[.,;:!?"""''()\[\]]', '', w).lower()
        if i not in annotated_positions and clean:
            problems.append(f"  ⚠ pos {i} ({w}): not annotated")

    return problems


def analyze_translation_quality(vnum, text, annotations):
    problems = []
    words = text.lower().split()

    ann_by_pos = {}
    for a in annotations:
        ann_by_pos.setdefault(a["pos"], []).append(a)

    for a in annotations:
        form_lower = a.get("form", "").lower()
        de = a.get("de", "")

        if form_lower == "being" and de == "seiend":
            problems.append(
                f'  ⚠ pos {a["pos"]}: "being" → "seiend" is unnatural German. '
                f'Consider context: maybe "da er/sie ... war" or a phrase.'
            )

        if form_lower == "the" and de not in (
            "der", "die", "das", "dem", "den", "des"
        ):
            problems.append(
                f'  ⚠ pos {a["pos"]}: "the" → "{de}" — articles should only '
                f'translate to der/die/das/dem/den/des. The content meaning '
                f'belongs to the next word.'
            )

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
            already_phrase = any(
                " " in a.get("form", "") and phrase in a.get("form", "").lower()
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
            for a in sorted(old, key=lambda x: x.get("pos", 0)):
                pe = f"-{a['pos_end']}" if "pos_end" in a else ""
                form = a.get("form", a.get("find", "?"))
                lines.append(
                    f"  [{a.get('pos','?')}{pe}] {form} → {a.get('de', '???')}  "
                    f"({a.get('level', '?')}, lemma: {a.get('lemma', '?')})"
                )

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
    return re.sub(r"[.,;:!?()\[\]\"""''«»—–…*]", "", word).lower()


def validate_and_fix(result, chapter):
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

            if "pos_end" not in a:
                actual = _normalize(words[pos])
                expected = _normalize(form)
                if actual != expected:
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
                actual = _normalize(words[pos])
                first_form = _normalize(form.split()[0])
                if actual != first_form:
                    issues.append(
                        f"V{vnum}: phrase '{form}' at pos {pos} — "
                        f"text has '{words[pos]}'"
                    )

    return issues, fixes


def parse_response_json(text):
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1]
    if text.endswith("```"):
        text = text[:-3]
    text = text.strip()
    if not text.startswith("{"):
        idx = text.find("{")
        if idx >= 0:
            text = text[idx:]
    return json.loads(text)
