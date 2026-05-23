#!/usr/bin/env python3
"""
Review and improve word-by-word annotations for one chapter (synchronous).

Usage:
  export ANTHROPIC_API_KEY="sk-ant-..."
  python3 review_annotations.py              # default: Matthew ch 1
  python3 review_annotations.py 40 1         # book_nr chapter_nr
"""
import json, os, sys, urllib.request, time

from review_common import (
    ANNO_DIR, SYSTEM_PROMPT,
    load_bible_chapter, load_annotations, build_user_message,
    validate_and_fix, parse_response_json,
)

API_URL = "https://api.anthropic.com/v1/messages"
MODEL = os.environ.get("REVIEW_MODEL", "claude-sonnet-4-20250514")

API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
if not API_KEY:
    print("\n  ⚠  No API key! → export ANTHROPIC_API_KEY='sk-ant-...'\n")
    sys.exit(1)

BOOK_NR = int(sys.argv[1]) if len(sys.argv) > 1 else 40
CHAP_NR = int(sys.argv[2]) if len(sys.argv) > 2 else 1


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
                return parse_response_json(text)

        except Exception as e:
            if attempt < max_retries - 1:
                wait = (attempt + 1) * 15
                print(f"\n  ⚠ {str(e)[:60]} — retry in {wait}s...", end=" ", flush=True)
                time.sleep(wait)
            else:
                raise


def print_diff(old_annotations, new_annotations, chapter):
    verse_map = {str(v["n"]): v["text"] for v in chapter["verses"]}

    for vnum in sorted(new_annotations.keys(), key=lambda k: int(k) if k.isdigit() else 0):
        text = verse_map.get(vnum, "")
        old = {(a["pos"], a.get("pos_end", a["pos"]), a["form"]): a
               for a in old_annotations.get(vnum, [])}
        new = {(a["pos"], a.get("pos_end", a["pos"]), a["form"]): a
               for a in new_annotations.get(vnum, [])}

        changes = []

        for key, a in new.items():
            if key not in old:
                old_at_pos = [o for o in old_annotations.get(vnum, [])
                              if o["pos"] == a["pos"]]
                if old_at_pos:
                    for o in old_at_pos:
                        changes.append(
                            f"  CHANGED: [{a['pos']}] "
                            f"{o['form']}→{o.get('de','?')}  ➜  {a['form']}→{a.get('de','?')}"
                        )
                else:
                    changes.append(
                        f"  NEW:     [{a['pos']}] {a['form']} → {a.get('de','?')}"
                    )

        for key, a in old.items():
            if key not in new:
                new_at_pos = [n for n in new_annotations.get(vnum, [])
                              if n["pos"] == a["pos"]]
                if not new_at_pos:
                    changes.append(
                        f"  REMOVED: [{a['pos']}] {a['form']} → {a.get('de','?')}"
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

        sub_chapter = {"number": chapter["number"], "verses": chunk_verses}
        sub_old = {str(v["n"]): old_annotations.get(str(v["n"]), [])
                   for v in chunk_verses}

        print(f"  Verses {chunk_range} — calling API ({MODEL})...", end=" ", flush=True)

        user_msg = build_user_message(book_name, CHAP_NR, sub_chapter, sub_old)
        chunk_result = call_api(user_msg)
        time.sleep(2)

        issues, fixes = validate_and_fix(chunk_result, sub_chapter)
        ann_count = sum(len(v) for v in chunk_result.values())
        fix_note = f" [{fixes} pos fixed]" if fixes else ""

        if issues:
            print(f"✓ {ann_count} ann{fix_note}")
            for issue in issues[:5]:
                print(f"    ⚠ {issue}")
        else:
            print(f"✓ {ann_count} annotations{fix_note}")

        for k, v in chunk_result.items():
            if k.isdigit():
                new_annotations[k] = v

    new_count = sum(len(v) for v in new_annotations.values())
    print(f"\n  Total: {old_count} → {new_count} annotations")

    print("\n  ─── Changes ───")
    print_diff(old_annotations, new_annotations, chapter)

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
