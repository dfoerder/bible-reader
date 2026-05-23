#!/usr/bin/env python3
"""
Collect results from an Anthropic Batch API job and apply to annotation files.

Usage:
  python3 review_batch_collect.py                    # latest batch from state file
  python3 review_batch_collect.py msgbatch_xxxxx     # specific batch
  python3 review_batch_collect.py --status            # just check status
  python3 review_batch_collect.py --wait              # poll until done, then apply
"""
import json, os, sys, urllib.request, time, re

from review_common import (
    ANNO_DIR, load_book, load_annotations,
    validate_and_fix, parse_response_json,
)

BATCH_API_URL = "https://api.anthropic.com/v1/messages/batches"
STATE_FILE = "batch_state.json"

API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")


def get_batch_id():
    for arg in sys.argv[1:]:
        if arg.startswith("msgbatch_"):
            return arg

    if not os.path.exists(STATE_FILE):
        print(f"  ⚠ No batch ID given and no {STATE_FILE} found.")
        sys.exit(1)

    with open(STATE_FILE, "r", encoding="utf-8") as f:
        state = json.load(f)

    if not state.get("batches"):
        print(f"  ⚠ No batches in {STATE_FILE}")
        sys.exit(1)

    return state["batches"][-1]["id"]


def api_get(url):
    req = urllib.request.Request(
        url,
        headers={
            "x-api-key": API_KEY,
            "anthropic-version": "2023-06-01",
        },
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        return resp.read().decode("utf-8")


def check_status(batch_id):
    data = json.loads(api_get(f"{BATCH_API_URL}/{batch_id}"))
    status = data.get("processing_status", "unknown")
    counts = data.get("request_counts", {})

    print(f"\n  Batch:  {batch_id}")
    print(f"  Status: {status}")
    if counts:
        total = sum(counts.values())
        print(f"  Progress: {counts.get('succeeded', 0)}/{total} succeeded, "
              f"{counts.get('errored', 0)} errored, "
              f"{counts.get('processing', 0)} processing")

    return data


def download_results(batch_id):
    results_url = f"{BATCH_API_URL}/{batch_id}/results"
    raw = api_get(results_url)
    lines = raw.strip().split("\n")

    results = {}
    errors = []

    for line in lines:
        if not line.strip():
            continue
        entry = json.loads(line)
        cid = entry["custom_id"]
        result = entry["result"]

        if result["type"] == "succeeded":
            text = result["message"]["content"][0]["text"]
            try:
                parsed = parse_response_json(text)
                results[cid] = parsed
            except (json.JSONDecodeError, IndexError) as e:
                errors.append((cid, f"JSON parse error: {e}"))
        elif result["type"] == "errored":
            err = result.get("error", {})
            errors.append((cid, f"{err.get('type', '?')}: {err.get('message', '?')}"))
        else:
            errors.append((cid, f"status: {result['type']}"))

    return results, errors


def parse_custom_id(cid):
    m = re.match(r"b(\d+)_c(\d+)_v(\d+)-(\d+)", cid)
    if not m:
        return None
    return {
        "book": int(m.group(1)),
        "chapter": int(m.group(2)),
        "v_start": int(m.group(3)),
        "v_end": int(m.group(4)),
    }


def apply_results(results, errors):
    # Group by book → chapter → chunk results
    by_book = {}
    for cid, chunk_data in results.items():
        info = parse_custom_id(cid)
        if not info:
            print(f"  ⚠ Can't parse custom_id: {cid}")
            continue
        book = info["book"]
        chap = info["chapter"]
        by_book.setdefault(book, {}).setdefault(chap, {})

        # Merge verse annotations (filter invalid keys)
        for vnum, annotations in chunk_data.items():
            if vnum.isdigit():
                by_book[book][chap][vnum] = annotations

    # Track errored chapters
    errored_chapters = set()
    for cid, msg in errors:
        info = parse_custom_id(cid)
        if info:
            errored_chapters.add((info["book"], info["chapter"]))

    saved_books = 0
    saved_chapters = 0
    skipped_chapters = 0

    for book_nr in sorted(by_book.keys()):
        book_name, chapters = load_book(book_nr)
        anno_data = load_annotations(book_nr)
        chapter_map = {ch["number"]: ch for ch in chapters}
        modified = False

        for chap_nr in sorted(by_book[book_nr].keys()):
            new_annotations = by_book[book_nr][chap_nr]
            chapter = chapter_map.get(chap_nr)
            if not chapter:
                print(f"  ⚠ {book_name} ch {chap_nr}: chapter not found in Bible data")
                continue

            had_error = (book_nr, chap_nr) in errored_chapters

            # Validate
            all_issues = []
            for vnum in list(new_annotations.keys()):
                sub_ch = {"number": chap_nr, "verses": [
                    v for v in chapter["verses"] if str(v["n"]) == vnum
                ]}
                if sub_ch["verses"]:
                    issues, fixes = validate_and_fix(
                        {vnum: new_annotations[vnum]}, sub_ch
                    )
                    all_issues.extend(issues)

            if had_error:
                # Partial result: merge into existing annotations
                existing = anno_data["chapters"].get(str(chap_nr), {})
                existing.update(new_annotations)
                anno_data["chapters"][str(chap_nr)] = existing
                print(f"  {book_name} ch {chap_nr}: PARTIAL — "
                      f"{len(new_annotations)} verses merged (some chunks errored)")
            else:
                anno_data["chapters"][str(chap_nr)] = new_annotations
                saved_chapters += 1

            if all_issues:
                for issue in all_issues[:3]:
                    print(f"    ⚠ {issue}")

            modified = True

        if modified:
            anno_path = os.path.join(ANNO_DIR, f"{book_nr}_web_deu.json")
            backup_path = anno_path + ".bak"

            with open(backup_path, "w", encoding="utf-8") as f:
                json.dump(anno_data, f, ensure_ascii=False, indent=2)
            with open(anno_path, "w", encoding="utf-8") as f:
                json.dump(anno_data, f, ensure_ascii=False, indent=2)

            saved_books += 1
            print(f"  ✓ {book_name}: saved ({len(by_book[book_nr])} chapters)")

    return saved_books, saved_chapters


def main():
    if not API_KEY:
        print("\n  ⚠  No API key! → export ANTHROPIC_API_KEY='sk-ant-...'\n")
        sys.exit(1)

    batch_id = get_batch_id()
    status_only = "--status" in sys.argv
    wait_mode = "--wait" in sys.argv

    batch = check_status(batch_id)
    status = batch.get("processing_status", "unknown")

    if status != "ended":
        if not wait_mode:
            if status == "in_progress":
                print("\n  Batch still processing. Run with --wait to poll, or check later.")
            sys.exit(0)

        print("\n  Waiting for batch to complete...")
        while status != "ended":
            time.sleep(60)
            batch = check_status(batch_id)
            status = batch.get("processing_status", "unknown")
            if status == "ended":
                break
            print(f"  ... still {status}, checking again in 60s")

    if status_only:
        sys.exit(0)

    print("\n  Downloading results...")
    results, errors = download_results(batch_id)

    print(f"\n  Results: {len(results)} succeeded, {len(errors)} errors")

    if errors:
        print("\n  ─── Errors ───")
        for cid, msg in errors[:20]:
            print(f"  {cid}: {msg}")
        if len(errors) > 20:
            print(f"  ... and {len(errors) - 20} more")

    if not results:
        print("\n  No results to apply.")
        sys.exit(1)

    print("\n  ─── Applying results ───")
    saved_books, saved_chapters = apply_results(results, errors)

    print(f"\n  ✓ Done: {saved_books} books, {saved_chapters} chapters updated.")

    if errors:
        print(f"  ⚠ {len(errors)} chunks failed — re-submit those books if needed.")


if __name__ == "__main__":
    main()
