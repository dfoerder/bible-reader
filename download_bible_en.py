#!/usr/bin/env python3
"""
Downloads the New Testament (World English Bible) from the getBible API
and saves it as bible_nt_en.json
"""
import json
import urllib.request
import re
import time
import sys

API_BASE = "https://api.getbible.net/v2/web"

# New Testament: books 40–66
NT_BOOKS = list(range(40, 67))

def clean_text(text):
    """Remove Strong's numbers and clean up whitespace."""
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def download_book(book_nr):
    """Download a single book from the API."""
    url = f"{API_BASE}/{book_nr}.json"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'BibleReader/1.0'})
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        print(f"  ⚠ Error downloading book {book_nr}: {e}")
        return None

def main():
    print("=" * 50)
    print("  New Testament download")
    print("  World English Bible (public domain)")
    print("=" * 50)
    print()

    books = []
    total = len(NT_BOOKS)

    for i, book_nr in enumerate(NT_BOOKS, 1):
        data = download_book(book_nr)
        if not data:
            print(f"  [{i}/{total}] Book {book_nr} skipped")
            continue

        book_name = data.get("name", f"Book {book_nr}")
        chapters = []

        for chap_data in data.get("chapters", []):
            chap_nr = chap_data.get("chapter", 0)
            verses = []
            for v in chap_data.get("verses", []):
                verses.append({
                    "n": v.get("verse", 0),
                    "text": clean_text(v.get("text", ""))
                })
            chapters.append({
                "number": chap_nr,
                "verses": verses
            })

        books.append({
            "nr": book_nr,
            "name": book_name,
            "chapters": chapters
        })

        chap_count = len(chapters)
        verse_count = sum(len(c["verses"]) for c in chapters)
        print(f"  [{i}/{total}] ✓ {book_name} — {chap_count} chapters, {verse_count} verses")
        time.sleep(0.3)

    output = {
        "translation": "World English Bible",
        "language": "en",
        "testament": "NT",
        "books": books
    }

    with open("bible_nt_en.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=None)

    total_verses = sum(
        sum(len(c["verses"]) for c in b["chapters"])
        for b in books
    )
    file_size = len(json.dumps(output, ensure_ascii=False)) / 1024 / 1024

    print()
    print(f"  ✓ Done! {len(books)} books, {total_verses} verses")
    print(f"  ✓ Saved: bible_nt_en.json ({file_size:.1f} MB)")
    print()

if __name__ == "__main__":
    main()
