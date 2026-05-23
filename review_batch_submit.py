#!/usr/bin/env python3
"""
Submit annotation review requests to the Anthropic Batch API (50% cheaper).

Usage:
  REVIEW_MODEL=claude-opus-4-7 python3 review_batch_submit.py 1-39        # OT
  REVIEW_MODEL=claude-opus-4-7 python3 review_batch_submit.py 44-66       # NT minus gospels
  REVIEW_MODEL=claude-opus-4-7 python3 review_batch_submit.py 1-39 44-66  # all except gospels
"""
import json, os, sys, urllib.request, time

from review_common import (
    BIBLE_DIR, ANNO_DIR, SYSTEM_PROMPT,
    load_book, load_annotations, build_user_message,
)

BATCH_API_URL = "https://api.anthropic.com/v1/messages/batches"
STATE_FILE = "batch_state.json"
CHUNK_SIZE = 5

MODEL = os.environ.get("REVIEW_MODEL", "claude-sonnet-4-20250514")
API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")


def parse_book_ranges(args):
    books = []
    for arg in args:
        if "-" in arg:
            start, end = arg.split("-", 1)
            books.extend(range(int(start), int(end) + 1))
        else:
            books.append(int(arg))
    return sorted(set(books))


def main():
    if not API_KEY:
        print("\n  ⚠  No API key! → export ANTHROPIC_API_KEY='sk-ant-...'\n")
        sys.exit(1)

    if len(sys.argv) < 2:
        print("Usage: REVIEW_MODEL=claude-opus-4-7 python3 review_batch_submit.py <books>")
        print("  e.g.: 1-39  44-66  1-39 44-66  44")
        sys.exit(1)

    books = parse_book_ranges(sys.argv[1:])

    # Verify all book files exist
    for b in books:
        path = os.path.join(BIBLE_DIR, f"{b}_web.json")
        if not os.path.exists(path):
            print(f"  ⚠ Book {b}: file not found ({path})")
            sys.exit(1)

    requests = []
    for book_nr in books:
        book_name, chapters = load_book(book_nr)
        anno_data = load_annotations(book_nr)
        all_ann = anno_data.get("chapters", {})
        book_chunks = 0

        for chapter in chapters:
            chap_nr = chapter["number"]
            old_ann = all_ann.get(str(chap_nr), {})
            verses = chapter["verses"]

            for i in range(0, len(verses), CHUNK_SIZE):
                chunk = verses[i : i + CHUNK_SIZE]
                v_start, v_end = chunk[0]["n"], chunk[-1]["n"]

                sub_ch = {"number": chap_nr, "verses": chunk}
                sub_old = {
                    str(v["n"]): old_ann.get(str(v["n"]), []) for v in chunk
                }

                user_msg = build_user_message(book_name, chap_nr, sub_ch, sub_old)

                requests.append({
                    "custom_id": f"b{book_nr}_c{chap_nr}_v{v_start}-{v_end}",
                    "params": {
                        "model": MODEL,
                        "max_tokens": 32000,
                        "system": SYSTEM_PROMPT,
                        "messages": [{"role": "user", "content": user_msg}],
                    },
                })
                book_chunks += 1

        print(f"  {book_nr:2d}  {book_name:20s}  {len(chapters):3d} ch  {book_chunks:4d} requests")

    print(f"\n  Total: {len(requests)} requests for {len(books)} books")
    print(f"  Model: {MODEL}")
    print(f"  Batch API = 50% cost reduction\n")

    payload = json.dumps({"requests": requests}).encode("utf-8")
    size_mb = len(payload) / 1024 / 1024
    print(f"  Submitting batch ({size_mb:.1f} MB)...")

    req = urllib.request.Request(
        BATCH_API_URL,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "x-api-key": API_KEY,
            "anthropic-version": "2023-06-01",
        },
    )

    with urllib.request.urlopen(req, timeout=600) as resp:
        result = json.loads(resp.read().decode("utf-8"))

    batch_id = result["id"]
    print(f"  ✓ Batch created: {batch_id}")
    print(f"  Status: {result.get('processing_status', '?')}")

    # Save state
    state = {"batches": []}
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            state = json.load(f)

    state["batches"].append({
        "id": batch_id,
        "submitted_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "model": MODEL,
        "request_count": len(requests),
        "books": books,
    })

    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)

    print(f"\n  State saved → {STATE_FILE}")
    print(f"  Next: python3 review_batch_collect.py")


if __name__ == "__main__":
    main()
