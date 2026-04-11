#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════
  Neues Testament vereinfachen — A2 Wortschatz + Passé Composé
  
  1. Lädt den Originaltext von der getBible API
  2. Vereinfacht jedes Kapitel mit der Anthropic API
  
  SETUP:
    export ANTHROPIC_API_KEY="sk-ant-..."
    python3 simplify_nt.py
    
  Das Script speichert nach jedem Kapitel. Bei Abbruch einfach
  nochmal starten — es fährt dort fort wo es aufgehört hat.
    
  KOSTEN: ca. 15-20 USD für das gesamte NT (260 Kapitel)
═══════════════════════════════════════════════════════════════
"""
import json
import urllib.request
import os
import time
import sys
import re

API_URL = "https://api.anthropic.com/v1/messages"
BIBLE_API = "https://api.getbible.net/v2/ls1910"
MODEL = "claude-sonnet-4-20250514"
OUTPUT_FILE = "bible_nt_simple.json"
ORIGINAL_FILE = "bible_nt_original.json"

API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
if not API_KEY:
    print("\n  ⚠  Kein API-Key! → export ANTHROPIC_API_KEY='sk-ant-...'\n")
    sys.exit(1)

NT_BOOKS = list(range(40, 67))  # Matthew to Revelation

SYSTEM_PROMPT = """Tu es un expert en français langue étrangère (FLE) et en textes bibliques.

Réécris le texte biblique fourni en respectant ces règles:

1. VOCABULAIRE: Niveau A2 (CECR) quand possible. Garde les termes bibliques sans synonyme simple.
2. PASSÉ SIMPLE → PASSÉ COMPOSÉ: Convertis tous les passé simple.
3. STRUCTURE: Garde la numérotation identique des versets.
4. SENS: Reste fidèle au sens théologique.
5. FORMAT: Retourne UNIQUEMENT un JSON array: [{"n": 1, "text": "..."}, ...]
   Pas de markdown, pas de commentaires."""


def clean_text(text):
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def download_bible():
    """Download the NT from getBible API."""
    if os.path.exists(ORIGINAL_FILE):
        print(f"  ℹ Originaltext bereits vorhanden: {ORIGINAL_FILE}")
        with open(ORIGINAL_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    print("  Lade Neues Testament herunter...")
    url = f"{BIBLE_API}.json"
    req = urllib.request.Request(url, headers={"User-Agent": "BibleSimplifier/1.0"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    # Extract NT books
    nt_books = [b for b in data["books"] if b["nr"] in NT_BOOKS]

    result = {"books": []}
    for book in nt_books:
        chapters = []
        for ch in book.get("chapters", []):
            verses = [{"n": v["verse"], "text": clean_text(v["text"])} for v in ch.get("verses", [])]
            chapters.append({"number": ch["chapter"], "verses": verses})
        result["books"].append({"nr": book["nr"], "name": book["name"], "chapters": chapters})

    with open(ORIGINAL_FILE, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False)

    total_v = sum(len(c["verses"]) for b in result["books"] for c in b["chapters"])
    print(f"  ✓ {len(result['books'])} Bücher, {total_v} Verse heruntergeladen\n")
    return result


def simplify_chapter(book_name, chapter_num, verses):
    """Simplify one chapter using the Anthropic API."""
    verses_text = "\n".join(f"{v['n']}. {v['text']}" for v in verses)

    payload = json.dumps({
        "model": MODEL,
        "max_tokens": 8000,
        "system": SYSTEM_PROMPT,
        "messages": [{"role": "user", "content": f"""Voici {book_name} chapitre {chapter_num} (Louis Segond 1910).
Réécris-le en français A2 avec passé composé. Retourne UNIQUEMENT le JSON array.

{verses_text}"""}]
    }).encode("utf-8")

    req = urllib.request.Request(API_URL, data=payload, headers={
        "Content-Type": "application/json",
        "x-api-key": API_KEY,
        "anthropic-version": "2023-06-01"
    })

    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        text = data["content"][0]["text"].strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1]
        if text.endswith("```"):
            text = text[:-3]
        return json.loads(text.strip())


def main():
    print()
    print("═" * 55)
    print("  NT vereinfachen (A2 + passé composé)")
    print("═" * 55)
    print()

    # Download original
    bible = download_bible()

    # Load existing progress
    done = set()
    simplified_books = []
    if os.path.exists(OUTPUT_FILE):
        try:
            with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
                existing = json.load(f)
                simplified_books = existing.get("books", [])
                for b in simplified_books:
                    for c in b.get("chapters", []):
                        done.add((b["name"], c["number"]))
            print(f"  ℹ Fortschritt: {len(done)} Kapitel bereits fertig\n")
        except:
            pass

    total_chapters = sum(len(b["chapters"]) for b in bible["books"])
    current = len(done)

    for book in bible["books"]:
        book_name = book["name"]
        # Find or create simplified book entry
        simp_book = next((b for b in simplified_books if b["name"] == book_name), None)
        if not simp_book:
            simp_book = {"nr": book["nr"], "name": book_name, "chapters": []}
            simplified_books.append(simp_book)

        for chapter in book["chapters"]:
            ch_num = chapter["number"]
            if (book_name, ch_num) in done:
                continue

            current += 1
            print(f"  [{current:3d}/{total_chapters}] {book_name} {ch_num}...", end=" ", flush=True)

            try:
                simplified = simplify_chapter(book_name, ch_num, chapter["verses"])
                if simplified and isinstance(simplified, list):
                    simp_book["chapters"].append({"number": ch_num, "verses": simplified})
                    simp_book["chapters"].sort(key=lambda c: c["number"])
                    done.add((book_name, ch_num))
                    print(f"✓ ({len(simplified)} Verse)")
                    save_progress(simplified_books)
                else:
                    print("✗ ungültiges Format")
            except Exception as e:
                print(f"✗ {e}")

            time.sleep(1)

    save_progress(simplified_books)
    total_v = sum(len(c["verses"]) for b in simplified_books for c in b.get("chapters", []))
    print(f"\n  ✓ Fertig! {len(done)}/{total_chapters} Kapitel, {total_v} Verse")
    print(f"  ✓ Gespeichert: {OUTPUT_FILE}\n")


def save_progress(books):
    output = {
        "translation": "Louis Segond 1910 — Version simplifiée A2",
        "description": "Vocabulaire A2, passé composé",
        "language": "fr",
        "testament": "NT",
        "books": sorted(books, key=lambda b: b.get("nr", 0))
    }
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
