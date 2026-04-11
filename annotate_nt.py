#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════
  Neues Testament — Wort-für-Wort Annotation (alle 27 Bücher)

  Annotiert jedes B1+ Wort im NT mit:
  - Wortform (wie im Text)
  - Lemma (Grundform)
  - CEFR-Niveau (B1, B2, C1, C2)
  - Kontextabhängige deutsche Übersetzung

  Nach jedem Kapitel werden die Wortpositionen automatisch
  gegen den Originaltext geprüft und korrigiert.

  SETUP:
    export ANTHROPIC_API_KEY="sk-ant-..."
    python3 annotate_nt.py

  Benötigt bible_nt.json im selben Ordner.
  Speichert nach jedem Kapitel — bei Abbruch einfach nochmal starten.

  KOSTEN: ca. 60-90 USD für das gesamte NT
═══════════════════════════════════════════════════════════════
"""
import json
import urllib.request
import os
import sys
import time
import re

API_URL  = "https://api.anthropic.com/v1/messages"
MODEL    = "claude-sonnet-4-20250514"
OUTPUT_FILE = "nt_annotations.json"
BIBLE_FILE  = "bible_nt.json"

# Welche Bücher annotiert werden (Buchnummern, None = alle NT-Bücher)
# Evangelien: 40=Matthieu, 41=Marc, 42=Luc, 43=Jean
ONLY_BOOKS = [40, 41, 42, 43]

API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
if not API_KEY:
    print("\n  ⚠  Kein API-Key! → export ANTHROPIC_API_KEY='sk-ant-...'\n")
    sys.exit(1)

if not os.path.exists(BIBLE_FILE):
    print(f"\n  ⚠  {BIBLE_FILE} nicht gefunden!")
    print("  Starte zuerst start.command um den Bibeltext herunterzuladen.\n")
    sys.exit(1)

SYSTEM_PROMPT = """Tu es un linguiste expert en français langue étrangère (FLE) et en allemand.

Ta tâche: Pour un chapitre biblique donné, annote chaque mot de niveau B1 ou supérieur (B1, B2, C1, C2) selon le CECR.

Pour chaque mot annoté, fournis:
- "pos": position du mot dans le verset (0-indexé, en comptant chaque mot séparé par un espace)
- "form": le mot tel qu'il apparaît dans le texte (forme fléchie)
- "lemma": la forme de base / infinitif / forme canonique du mot
- "level": le niveau CECR du LEMME (B1, B2, C1 ou C2)
- "de": la traduction allemande correcte DANS CE CONTEXTE PRÉCIS

Règles importantes:
1. N'annote PAS les mots de niveau A1 ou A2 (mots très courants comme: être, avoir, faire, dire, aller, voir, pouvoir, vouloir, savoir, devoir, prendre, mettre, donner, homme, femme, fils, fille, père, mère, frère, roi, pays, ville, jour, nuit, eau, pain, maison, terre, nom, main, yeux, coeur, vie, mort, tout, rien, grand, petit, bon, nouveau, premier, autre, même, peu, très, bien, aussi, encore, toujours, jamais, ici, où, quand, comment, pourquoi, car, donc, mais, avec, dans, sur, sous, vers, pour, par, sans, entre, depuis, avant, après, contre, chez, selon, etc.)
2. N'annote PAS les noms propres (Jésus, Abraham, Matthieu, Jérusalem, etc.)
3. N'annote PAS les articles, pronoms personnels, prépositions simples, conjonctions de base
4. ANNOTE les verbes en passé simple (forme rare pour un apprenant)
5. ANNOTE le vocabulaire religieux/biblique spécifique (baptiser, prophète, crucifier, etc.)
6. La traduction allemande doit correspondre au sens DANS CE VERSET précis
   - Exemple: "esprit" peut être "Geist" ou "Verstand" selon le contexte
   - Exemple: "engendra" dans un contexte généalogique = "zeugte"
   - Exemple: "grâce" au sens religieux = "Gnade", au sens de "merci" = "Dank"

FORMAT de réponse — UNIQUEMENT un JSON object, sans markdown ni commentaire:
{
  "1": [{"pos":2,"form":"engendra","lemma":"engendrer","level":"C1","de":"zeugte"}, ...],
  "2": [...]
}

Les clés sont les numéros de versets (en string). La valeur est un array d'annotations pour ce verset.
Si un verset n'a aucun mot B1+, utilise un array vide: "5": []"""


# ─── Position correction ─────────────────────────────────────────────────────

def _normalize(word):
    """Strip punctuation and lowercase for comparison."""
    return re.sub(r"[.,;:!?()\[\]\"\u2019\u2018\u00AB\u00BB\u2014\u2013\u2026*]", "", word).lower()


def correct_positions(chapter_annotations, chapter):
    """
    After each API call, verify that annotation["pos"] actually points to
    annotation["form"] in the verse text. Correct silently when possible.
    Returns the number of corrected entries.
    """
    corrections = 0
    verse_map = {str(v["n"]): v["text"] for v in chapter["verses"]}

    for verse_key, annotations in chapter_annotations.items():
        text = verse_map.get(verse_key, "")
        if not text:
            continue
        words = text.split()

        for ann in annotations:
            pos  = ann.get("pos", -1)
            form = ann.get("form", "")
            form_norm = _normalize(form)
            if not form_norm:
                continue

            # Check if current pos is already correct
            if 0 <= pos < len(words) and _normalize(words[pos]) == form_norm:
                continue

            # Search the verse for the correct position
            found = -1
            for i, w in enumerate(words):
                if _normalize(w) == form_norm:
                    found = i
                    break

            if found >= 0:
                ann["pos"] = found
                corrections += 1
            # If not found at all: leave pos as-is (LLM hallucinated form)

    return corrections


# ─── API call ─────────────────────────────────────────────────────────────────

def annotate_chapter(book_name, chapter_num, verses_text):
    """Call the Claude API to annotate one chapter."""
    payload = json.dumps({
        "model": MODEL,
        "max_tokens": 16000,
        "system": SYSTEM_PROMPT,
        "messages": [{
            "role": "user",
            "content": (
                f"Voici le chapitre {chapter_num} de {book_name} "
                f"(Louis Segond 1910).\n"
                "Annote chaque mot de niveau B1+ avec sa forme, son lemme, "
                "son niveau CECR et sa traduction allemande contextuelle.\n\n"
                f"{verses_text}\n\n"
                "Retourne UNIQUEMENT le JSON object."
            )
        }]
    }).encode("utf-8")

    req = urllib.request.Request(API_URL, data=payload, headers={
        "Content-Type": "application/json",
        "x-api-key": API_KEY,
        "anthropic-version": "2023-06-01"
    })

    with urllib.request.urlopen(req, timeout=180) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        text = data["content"][0]["text"].strip()
        # Strip optional markdown code fences
        if text.startswith("```"):
            text = text.split("\n", 1)[1]
        if text.endswith("```"):
            text = text[:-3]
        return json.loads(text.strip())


# ─── Persistence ──────────────────────────────────────────────────────────────

def load_progress():
    """Load existing output file; return books dict keyed by book nr (str)."""
    if not os.path.exists(OUTPUT_FILE):
        return {}
    try:
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("books", {})
    except Exception:
        return {}


def save_progress(books):
    total_words = sum(
        sum(len(anns) for anns in ch.values())
        for bk in books.values()
        for ch in bk["chapters"].values()
    )
    output = {
        "description": (
            "Wort-für-Wort Annotationen NT: "
            "Lemma, CEFR-Niveau, kontextabhängige DE-Übersetzung"
        ),
        "levels": "B1, B2, C1, C2 (A1/A2 ausgelassen)",
        "total_annotations": total_words,
        "books": books
    }
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    print()
    print("═" * 58)
    print("  Neues Testament — Wort-für-Wort Annotation")
    print("  Alle 27 Bücher · Lemma · CEFR · Deutsche Übersetzung")
    print("═" * 58)
    print()

    with open(BIBLE_FILE, "r", encoding="utf-8") as f:
        bible = json.load(f)

    nt_books = [b for b in bible.get("books", [])
                if ONLY_BOOKS is None or b.get("nr") in ONLY_BOOKS]
    total_books = len(nt_books)
    total_chapters_all = sum(len(b.get("chapters", [])) for b in nt_books)
    print(f"  {total_books} Bücher · {total_chapters_all} Kapitel insgesamt\n")

    books = load_progress()
    if books:
        done_ch = sum(len(bk["chapters"]) for bk in books.values())
        print(f"  ℹ Fortschritt: {done_ch}/{total_chapters_all} Kapitel bereits annotiert\n")

    grand_failed = []

    for book_idx, book in enumerate(nt_books, 1):
        book_nr   = str(book.get("nr", book_idx + 39))
        book_name = book["name"]
        chapters  = book.get("chapters", [])
        total_ch  = len(chapters)

        # Ensure book entry exists
        if book_nr not in books:
            books[book_nr] = {"name": book_name, "chapters": {}}

        book_chapters = books[book_nr]["chapters"]
        remaining = [c for c in chapters if str(c["number"]) not in book_chapters]

        if not remaining:
            print(f"  [{book_idx:2}/{total_books}] {book_name}: bereits vollständig ✓")
            continue

        done = len(book_chapters)
        print(f"\n  [{book_idx:2}/{total_books}] {book_name} ({total_ch} Kapitel, {done} bereits fertig)")
        print(f"  {'─' * 50}")

        failed = []

        for chapter in remaining:
            ch_num = str(chapter["number"])
            verses_text = "\n".join(
                f"{v['n']}. {v['text']}" for v in chapter["verses"]
            )

            print(f"    Kap {ch_num.rjust(3)}/{total_ch} ...", end=" ", flush=True)

            try:
                annotations = annotate_chapter(book_name, chapter["number"], verses_text)

                if not isinstance(annotations, dict):
                    failed.append(ch_num)
                    print("✗ ungültiges Format")
                    continue

                # Correct positions against source text
                fixed = correct_positions(annotations, chapter)
                total_ann = sum(len(v) for v in annotations.values())
                fix_note  = f" [{fixed} korr.]" if fixed else ""

                book_chapters[ch_num] = annotations
                print(f"✓ {total_ann} Annotationen{fix_note}")
                save_progress(books)

            except Exception as e:
                failed.append(ch_num)
                print(f"✗ {str(e)[:80]}")

            time.sleep(1)

        # ── Retry failed chapters ──────────────────────────────────────────
        if failed:
            print(f"\n    Wiederhole {len(failed)} fehlgeschlagene Kapitel ...")
            for ch_num in failed[:]:
                chapter = next(
                    (c for c in chapters if str(c["number"]) == ch_num), None
                )
                if not chapter:
                    continue
                verses_text = "\n".join(
                    f"{v['n']}. {v['text']}" for v in chapter["verses"]
                )
                print(f"    Retry Kap {ch_num} ...", end=" ", flush=True)
                time.sleep(3)
                try:
                    annotations = annotate_chapter(
                        book_name, int(ch_num), verses_text
                    )
                    if isinstance(annotations, dict):
                        fixed = correct_positions(annotations, chapter)
                        total_ann = sum(len(v) for v in annotations.values())
                        fix_note  = f" [{fixed} korr.]" if fixed else ""
                        book_chapters[ch_num] = annotations
                        failed.remove(ch_num)
                        print(f"✓ {total_ann} Annotationen{fix_note}")
                        save_progress(books)
                    else:
                        print("✗")
                except Exception as e:
                    print(f"✗ {str(e)[:80]}")

        grand_failed.extend([(book_name, ch) for ch in failed])

    save_progress(books)

    # ── Summary ───────────────────────────────────────────────────────────────
    total_words = sum(
        sum(len(anns) for anns in ch.values())
        for bk in books.values()
        for ch in bk["chapters"].values()
    )
    done_ch = sum(len(bk["chapters"]) for bk in books.values())

    print()
    print("═" * 58)
    print(f"  ✓ {done_ch}/{total_chapters_all} Kapitel annotiert")
    print(f"  ✓ {total_words} Wörter annotiert")
    if grand_failed:
        print(f"  ⚠  Fehlgeschlagen:")
        for bk, ch in grand_failed:
            print(f"     {bk} Kap. {ch}")
        print("  → Script nochmal starten zum Fortfahren")
    print(f"  ✓ Gespeichert: {OUTPUT_FILE}")
    print()


if __name__ == "__main__":
    main()
