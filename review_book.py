#!/usr/bin/env python3
"""Run review + cleanup for all chapters of a book."""
import subprocess, sys, os, json

BOOK_NR = int(sys.argv[1]) if len(sys.argv) > 1 else 40
START_CH = int(sys.argv[2]) if len(sys.argv) > 2 else 1

with open(f"bibles/eng/web/{BOOK_NR}_web.json") as f:
    book = json.load(f)

book_name = book["name"]
total_ch = len(book["chapters"])

model = os.environ.get("REVIEW_MODEL", "claude-sonnet-4-20250514")
env = {**os.environ, "REVIEW_MODEL": model}

print(f"\n{'=' * 58}")
print(f"  Reviewing: {book_name} ({total_ch} chapters)")
print(f"  Model: {model}")
print(f"  Starting from chapter {START_CH}")
print(f"{'=' * 58}\n")

failed = []

for ch in book["chapters"]:
    ch_num = ch["number"]
    if ch_num < START_CH:
        continue

    print(f"\n--- {book_name} chapter {ch_num}/{total_ch} ---")

    result = subprocess.run(
        ["python3", "review_annotations.py", str(BOOK_NR), str(ch_num)],
        env=env, capture_output=False
    )

    if result.returncode != 0:
        print(f"  ✗ Review failed for chapter {ch_num}")
        failed.append(ch_num)
        continue

    subprocess.run(
        ["python3", "cleanup_punct.py", str(BOOK_NR), str(ch_num)],
        capture_output=False
    )

print(f"\n{'=' * 58}")
print(f"  Done: {book_name}")
if failed:
    print(f"  ⚠ Failed chapters: {failed}")
else:
    print(f"  ✓ All {total_ch - START_CH + 1} chapters processed")
print(f"{'=' * 58}\n")
