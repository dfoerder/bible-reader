#!/usr/bin/env python3
"""
Collect results from modernization batch and write l1912mod JSON files.

Usage:
  python3 modernize_batch_collect.py                  # latest batch
  python3 modernize_batch_collect.py msgbatch_xxxxx   # specific batch
  python3 modernize_batch_collect.py --status          # just check status
  python3 modernize_batch_collect.py --wait            # poll until done, then apply
"""
import json, os, sys, urllib.request, time, re

BIBLE_DIR = "bibles/deu/l1912"
OUT_DIR = "bibles/deu/l1912mod"
BATCH_API_URL = "https://api.anthropic.com/v1/messages/batches"
STATE_FILE = "modernize_batch_state.json"

API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

BOOK_NAMES = {
    1:'1. Mose',2:'2. Mose',3:'3. Mose',4:'4. Mose',5:'5. Mose',
    6:'Josua',7:'Richter',8:'Ruth',9:'1. Samuel',10:'2. Samuel',
    11:'1. Könige',12:'2. Könige',13:'1. Chronika',14:'2. Chronika',
    15:'Esra',16:'Nehemia',17:'Esther',18:'Hiob',19:'Psalmen',20:'Sprüche',
    21:'Prediger',22:'Hohelied',23:'Jesaja',24:'Jeremia',25:'Klagelieder',
    26:'Hesekiel',27:'Daniel',28:'Hosea',29:'Joel',30:'Amos',31:'Obadja',
    32:'Jona',33:'Micha',34:'Nahum',35:'Habakuk',36:'Zephanja',37:'Haggai',
    38:'Sacharja',39:'Maleachi',40:'Matthäus',41:'Markus',42:'Lukas',
    43:'Johannes',44:'Apostelgeschichte',45:'Römer',46:'1. Korinther',
    47:'2. Korinther',48:'Galater',49:'Epheser',50:'Philipper',51:'Kolosser',
    52:'1. Thessalonicher',53:'2. Thessalonicher',54:'1. Timotheus',
    55:'2. Timotheus',56:'Titus',57:'Philemon',58:'Hebräer',59:'Jakobus',
    60:'1. Petrus',61:'2. Petrus',62:'1. Johannes',63:'2. Johannes',
    64:'3. Johannes',65:'Judas',66:'Offenbarung'
}


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
    m = re.match(r"b(\d+)_c(\d+)", cid)
    if not m:
        return None
    return {"book": int(m.group(1)), "chapter": int(m.group(2))}


def apply_results(results, errors):
    by_book = {}
    for cid, chapter_data in results.items():
        info = parse_custom_id(cid)
        if not info:
            print(f"  ⚠ Can't parse custom_id: {cid}")
            continue
        by_book.setdefault(info["book"], {})[str(info["chapter"])] = chapter_data

    errored_chapters = set()
    for cid, msg in errors:
        info = parse_custom_id(cid)
        if info:
            errored_chapters.add((info["book"], info["chapter"]))

    saved_books = 0
    saved_chapters = 0

    for book_nr in sorted(by_book.keys()):
        book_name = BOOK_NAMES.get(book_nr, f"Buch {book_nr}")
        out_path = os.path.join(OUT_DIR, f"{book_nr}_l1912mod.json")

        existing = {"name": book_name, "chapters": {}}
        if os.path.exists(out_path):
            with open(out_path, "r", encoding="utf-8") as f:
                existing = json.load(f)

        for chap_nr, verses in by_book[book_nr].items():
            existing["chapters"][chap_nr] = verses
            saved_chapters += 1

        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(existing, f, ensure_ascii=False)

        errored_in_book = [c for b, c in errored_chapters if b == book_nr]
        suffix = ""
        if errored_in_book:
            suffix = f" ({len(errored_in_book)} chapters errored)"

        print(f"  ✓ {book_name}: {len(by_book[book_nr])} chapters saved{suffix}")
        saved_books += 1

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

    os.makedirs(OUT_DIR, exist_ok=True)

    print("\n  ─── Applying results ───")
    saved_books, saved_chapters = apply_results(results, errors)

    print(f"\n  ✓ Done: {saved_books} books, {saved_chapters} chapters written to {OUT_DIR}")

    if errors:
        print(f"  ⚠ {len(errors)} chapters failed — re-submit those books if needed.")


if __name__ == "__main__":
    main()
