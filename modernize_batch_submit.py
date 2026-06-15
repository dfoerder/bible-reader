#!/usr/bin/env python3
"""
Submit Luther 1912 modernization requests to the Anthropic Batch API (50% cheaper).

Usage:
  python3 modernize_batch_submit.py 1-66          # whole Bible
  python3 modernize_batch_submit.py 40-43          # gospels only
  python3 modernize_batch_submit.py 1              # single book
  MODERNIZE_MODEL=claude-sonnet-4-20250514 python3 modernize_batch_submit.py 1-66
"""
import json, os, sys, urllib.request, time

BIBLE_DIR = "bibles/deu/l1912"
OUT_DIR = "bibles/deu/l1912mod"
BATCH_API_URL = "https://api.anthropic.com/v1/messages/batches"
STATE_FILE = "modernize_batch_state.json"

MODEL = os.environ.get("MODERNIZE_MODEL", "claude-sonnet-4-20250514")
API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

SYSTEM_PROMPT = """\
Du modernisierst den Text der Luther-Bibel von 1912 für Deutschlerner (nicht-muttersprachliche Leser).

## Regeln

1. **Rechtschreibung modernisieren**: daß→dass, ward→wurde, Laß→Lass usw.
2. **Veraltete Wörter ersetzen**:
   - zeugte → war der Vater von
   - Weib → Frau
   - Gemahl → Frau / Mann (je nach Kontext)
   - allda → dort
   - gen → nach
   - Otterngezüchte → Schlangenbrut
   - genugsam → wert
   - Buße tun → umkehren
   - Glieder (Generationen) → Generationen
   - Weisen vom Morgenland → Sterndeuter aus dem Osten
   - erkannte sie (nicht) → schlief (nicht) mit ihr
   - und andere veraltete Ausdrücke sinngemäß modernisieren
3. **Satzbau vereinfachen**: Lange Schachtelsätze in kürzere, klare Sätze aufteilen.
4. **Ton bewahren**: Der Text soll würdevoll und biblisch klingen, aber klar verständlich sein.
5. **Inhaltlich treu bleiben**: Keine theologischen Änderungen, keine Ergänzungen, nichts weglassen.
6. **Eigennamen beibehalten** wie im Original.

## Ausgabeformat

Gib NUR ein JSON-Objekt zurück. Schlüssel = Versnummern (Strings). Werte = modernisierter Verstext (String).

Beispiel:
{"1": "Am Anfang schuf Gott Himmel und Erde.", "2": "Und die Erde war leer und öde..."}

Kein Markdown, keine Erklärungen — nur das JSON-Objekt."""


def parse_book_ranges(args):
    books = []
    for arg in args:
        if "-" in arg:
            start, end = arg.split("-", 1)
            books.extend(range(int(start), int(end) + 1))
        else:
            books.append(int(arg))
    return sorted(set(books))


def load_book(book_nr):
    path = os.path.join(BIBLE_DIR, f"{book_nr}_l1912.json")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["name"], data["chapters"]


def already_modernized(book_nr, chap_nr):
    path = os.path.join(OUT_DIR, f"{book_nr}_l1912mod.json")
    if not os.path.exists(path):
        return False
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return str(chap_nr) in data.get("chapters", {})


def build_user_message(book_name, chap_nr, verses):
    lines = [f"{book_name}, Kapitel {chap_nr} (Luther 1912):\n"]
    for vnum in sorted(verses.keys(), key=int):
        lines.append(f"{vnum}: {verses[vnum]}")
    lines.append("\nModernisiere alle Verse dieses Kapitels. Gib das Ergebnis als JSON zurück.")
    return "\n".join(lines)


def main():
    if not API_KEY:
        print("\n  ⚠  No API key! → export ANTHROPIC_API_KEY='sk-ant-...'\n")
        sys.exit(1)

    if len(sys.argv) < 2:
        print("Usage: python3 modernize_batch_submit.py <books>")
        print("  e.g.: 1-66  40-43  1")
        sys.exit(1)

    skip_existing = "--skip-existing" in sys.argv
    books = parse_book_ranges([a for a in sys.argv[1:] if not a.startswith("--")])

    os.makedirs(OUT_DIR, exist_ok=True)

    requests = []
    for book_nr in books:
        path = os.path.join(BIBLE_DIR, f"{book_nr}_l1912.json")
        if not os.path.exists(path):
            print(f"  ⚠ Book {book_nr}: file not found ({path})")
            sys.exit(1)

        book_name, chapters = load_book(book_nr)
        book_requests = 0

        for chap_nr in sorted(chapters.keys(), key=int):
            if skip_existing and already_modernized(book_nr, int(chap_nr)):
                continue

            verses = chapters[chap_nr]
            user_msg = build_user_message(book_name, chap_nr, verses)

            requests.append({
                "custom_id": f"b{book_nr}_c{chap_nr}",
                "params": {
                    "model": MODEL,
                    "max_tokens": 16000,
                    "system": SYSTEM_PROMPT,
                    "messages": [{"role": "user", "content": user_msg}],
                },
            })
            book_requests += 1

        print(f"  {book_nr:2d}  {book_name:20s}  {len(chapters):3d} ch  {book_requests:4d} requests")

    if not requests:
        print("\n  No requests to submit (all chapters already modernized?).")
        sys.exit(0)

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
    print(f"  Next: python3 modernize_batch_collect.py")


if __name__ == "__main__":
    main()
