#!/usr/bin/env python3
"""
Fill in empty OT annotation verses.
Finds all verses with [] in ot_annotations_en.json, groups them by
book+chapter, sends them to Claude for annotation, and merges results back.

SETUP:
  export ANTHROPIC_API_KEY="sk-ant-..."
  python3 fill_empty_ot.py
"""
import json
import urllib.request
import os
import sys
import time
import re
import ssl
import subprocess

def _make_ssl_context():
    ctx = ssl.create_default_context()
    # macOS: export system root certs if Python's default bundle is missing
    try:
        ctx.load_default_certs()
    except Exception:
        pass
    if not ctx.get_ca_certs():
        pem = subprocess.run(
            ["security", "find-certificate", "-a", "-p",
             "/System/Library/Keychains/SystemRootCertificates.keychain"],
            capture_output=True, text=True
        ).stdout
        if pem:
            import tempfile
            tmp = tempfile.NamedTemporaryFile(suffix=".pem", delete=False, mode="w")
            tmp.write(pem)
            tmp.close()
            ctx.load_verify_locations(tmp.name)
    return ctx

SSL_CTX = _make_ssl_context()

API_URL = "https://api.anthropic.com/v1/messages"
MODEL = "claude-sonnet-4-20250514"

ANNO_FILE = "ot_annotations_en.json"
BIBLE_FILE = "bible_ot_en.json"

API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
if not API_KEY:
    print("\n  No API key! Set: export ANTHROPIC_API_KEY='sk-ant-...'\n")
    sys.exit(1)

SYSTEM_PROMPT = """You are an expert linguist in English as a foreign language (EFL) and German.

Your task: For given Bible verses, annotate EVERY word at A1, A2, B1, B2, C1, or C2 level.
This means: annotate all common words including function words. Skip proper nouns.

For each annotated word, provide:
- "pos": word position in the verse (0-indexed, counting each space-separated word)
- "form": the word as it appears in the text (inflected form)
- "lemma": the base form / infinitive / canonical form of the word
- "level": the CEFR level of the LEMMA (A1, A2, B1, B2, C1, or C2)
- "de": the correct German translation IN THIS SPECIFIC CONTEXT

Important rules:
1. Annotate words at ALL CEFR levels (A1 through C2).
2. Do NOT annotate proper nouns (God, Jesus, Moses, Abraham, Israel, Jerusalem, etc.)
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
   - Verbs: spoke → sprach, said → sagte, came → kam, went → ging, made → machte, etc.
   - Nouns: son → Sohn, father → Vater, land → Land, people → Volk/Leute, etc.
4. The German translation MUST match the meaning IN THIS SPECIFIC VERSE context
5. If a verse contains ONLY proper nouns (e.g., "Hadoram, Uzal, Diklah,"), return an empty array [] for that verse.
6. For verses that are mostly names but have some common words (like "the sons of X"), annotate only the common words.

Response FORMAT — ONLY a JSON object, no markdown or comments:
{
  "1": [{"pos":0,"form":"The","lemma":"the","level":"A1","de":"Die"}, ...],
  "2": []
}

Keys are verse numbers (as strings). Values are arrays of annotations for that verse."""


def _normalize(word):
    return re.sub(r"[.,;:!?()\[\]\"’‘«»—–…*]", "", word).lower()


def correct_positions(annotations, verse_texts):
    corrections = 0
    for verse_key, anns in annotations.items():
        text = verse_texts.get(verse_key, "")
        if not text or not anns:
            continue
        words = text.split()
        for ann in anns:
            pos = ann.get("pos", -1)
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


CHUNK_SIZE = 20


def call_api(book_name, chapter_num, verse_items, label=""):
    verses_text = "\n".join(f"{vn}. {vt}" for vn, vt in verse_items)
    payload = json.dumps({
        "model": MODEL,
        "max_tokens": 16000,
        "system": SYSTEM_PROMPT,
        "messages": [{
            "role": "user",
            "content": (
                f"Here are verses from chapter {chapter_num} of {book_name} "
                f"(World English Bible){label}.\n"
                "Annotate every word (except proper nouns) with its form, lemma, "
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

    with urllib.request.urlopen(req, timeout=180, context=SSL_CTX) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        text = data["content"][0]["text"].strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1]
        if text.endswith("```"):
            text = text[:-3]
        return json.loads(text.strip())


def main():
    print()
    print("=" * 58)
    print("  Fill empty OT annotation verses")
    print("=" * 58)
    print()

    with open(BIBLE_FILE, "r", encoding="utf-8") as f:
        bible = json.load(f)

    with open(ANNO_FILE, "r", encoding="utf-8") as f:
        anno_data = json.load(f)

    bible_lookup = {}
    for book in bible["books"]:
        bnr = str(book["nr"])
        bible_lookup[bnr] = {"name": book["name"], "chapters": {}}
        for ch in book["chapters"]:
            cnum = str(ch["number"])
            bible_lookup[bnr]["chapters"][cnum] = {
                str(v["n"]): v["text"] for v in ch["verses"]
            }

    books = anno_data["books"]

    # Collect all empty verses grouped by (book_id, chapter)
    groups = {}
    for book_id in sorted(books.keys(), key=int):
        book_data = books[book_id]
        for ch_num in sorted(book_data["chapters"].keys(), key=int):
            ch_data = book_data["chapters"][ch_num]
            for v_num, v_data in ch_data.items():
                if isinstance(v_data, list) and not v_data:
                    text = (bible_lookup.get(book_id, {})
                            .get("chapters", {})
                            .get(ch_num, {})
                            .get(v_num, ""))
                    if not text:
                        continue
                    key = (book_id, ch_num)
                    if key not in groups:
                        groups[key] = []
                    groups[key].append((v_num, text))

    total_empty = sum(len(v) for v in groups.values())
    print(f"  Found {total_empty} empty verses in {len(groups)} chapter groups")
    print()

    # Load progress
    progress_file = "fill_empty_progress.json"
    done_keys = set()
    if os.path.exists(progress_file):
        with open(progress_file, "r") as f:
            done_keys = set(json.load(f))

    filled = 0
    failed_groups = []

    for (book_id, ch_num), verse_items in sorted(groups.items(), key=lambda x: (int(x[0][0]), int(x[0][1]))):
        group_key = f"{book_id}:{ch_num}"
        if group_key in done_keys:
            filled += len(verse_items)
            continue

        book_name = bible_lookup[book_id]["name"]
        vcount = len(verse_items)
        vnums = ",".join(vn for vn, _ in verse_items)
        print(f"  {book_name} ch{ch_num} ({vcount} verses: {vnums}) ...", end=" ", flush=True)

        try:
            if len(verse_items) <= CHUNK_SIZE:
                result = call_api(book_name, ch_num, verse_items)
            else:
                result = {}
                chunks = [verse_items[i:i+CHUNK_SIZE]
                          for i in range(0, len(verse_items), CHUNK_SIZE)]
                for ci, chunk in enumerate(chunks):
                    label = f" (part {ci+1}/{len(chunks)})"
                    part = call_api(book_name, ch_num, chunk, label)
                    if isinstance(part, dict):
                        result.update(part)
                    time.sleep(1)

            if not isinstance(result, dict):
                failed_groups.append((book_id, ch_num, verse_items))
                print("FAIL: invalid format")
                continue

            verse_texts = {vn: vt for vn, vt in verse_items}
            fixed = correct_positions(result, verse_texts)

            ann_count = 0
            for vn, anns in result.items():
                if isinstance(anns, list) and anns:
                    books[book_id]["chapters"][ch_num][vn] = anns
                    ann_count += len(anns)
                elif isinstance(anns, list) and not anns:
                    pass  # names-only verse, keep empty

            fix_note = f" [{fixed} pos-fixes]" if fixed else ""
            print(f"OK +{ann_count} annotations{fix_note}")
            filled += vcount

            # Save
            anno_data["books"] = books
            anno_data["total_annotations"] = sum(
                sum(len(anns) for anns in ch.values() if isinstance(anns, list))
                for bk in books.values()
                for ch in bk["chapters"].values()
            )
            with open(ANNO_FILE, "w", encoding="utf-8") as f:
                json.dump(anno_data, f, ensure_ascii=False, indent=2)

            done_keys.add(group_key)
            with open(progress_file, "w") as f:
                json.dump(list(done_keys), f)

        except Exception as e:
            failed_groups.append((book_id, ch_num, verse_items))
            print(f"FAIL: {str(e)[:100]}")

        time.sleep(1)

    # Retry failed
    if failed_groups:
        print(f"\n  Retrying {len(failed_groups)} failed groups ...")
        for book_id, ch_num, verse_items in failed_groups[:]:
            book_name = bible_lookup[book_id]["name"]
            print(f"  Retry {book_name} ch{ch_num} ...", end=" ", flush=True)
            time.sleep(3)
            try:
                if len(verse_items) <= CHUNK_SIZE:
                    result = call_api(book_name, ch_num, verse_items)
                else:
                    result = {}
                    chunks = [verse_items[i:i+CHUNK_SIZE]
                              for i in range(0, len(verse_items), CHUNK_SIZE)]
                    for ci, chunk in enumerate(chunks):
                        label = f" (part {ci+1}/{len(chunks)})"
                        part = call_api(book_name, ch_num, chunk, label)
                        if isinstance(part, dict):
                            result.update(part)
                        time.sleep(1)

                if isinstance(result, dict):
                    verse_texts = {vn: vt for vn, vt in verse_items}
                    fixed = correct_positions(result, verse_texts)
                    ann_count = 0
                    for vn, anns in result.items():
                        if isinstance(anns, list) and anns:
                            books[book_id]["chapters"][ch_num][vn] = anns
                            ann_count += len(anns)

                    fix_note = f" [{fixed} pos-fixes]" if fixed else ""
                    print(f"OK +{ann_count}{fix_note}")
                    filled += len(verse_items)
                    failed_groups.remove((book_id, ch_num, verse_items))

                    anno_data["books"] = books
                    anno_data["total_annotations"] = sum(
                        sum(len(anns) for anns in ch.values() if isinstance(anns, list))
                        for bk in books.values()
                        for ch in bk["chapters"].values()
                    )
                    with open(ANNO_FILE, "w", encoding="utf-8") as f:
                        json.dump(anno_data, f, ensure_ascii=False, indent=2)

                    done_keys.add(f"{book_id}:{ch_num}")
                    with open(progress_file, "w") as f:
                        json.dump(list(done_keys), f)
                else:
                    print("FAIL")
            except Exception as e:
                print(f"FAIL: {str(e)[:100]}")

    # Final count
    still_empty = 0
    for book_id, book_data in books.items():
        for ch_num, ch_data in book_data["chapters"].items():
            for v_num, v_data in ch_data.items():
                if isinstance(v_data, list) and not v_data:
                    still_empty += 1

    total = anno_data.get("total_annotations", 0)
    print()
    print("=" * 58)
    print(f"  Done. Total annotations: {total}")
    print(f"  Remaining empty verses: {still_empty}")
    print("=" * 58)
    print()


if __name__ == "__main__":
    main()
