#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════
  Matthäus vereinfachen — A2 Wortschatz + Passé Composé
  
  Verwendet die Anthropic API (Claude) um den Text zu vereinfachen.
  
  SETUP:
    1. Hol dir einen API-Key: https://console.anthropic.com/
    2. Setze den Key:
       export ANTHROPIC_API_KEY="sk-ant-..."
    3. Starte das Script:
       python3 simplify_matthew.py
       
  KOSTEN: ca. 2-3 USD für das ganze Matthäus-Evangelium
═══════════════════════════════════════════════════════════════
"""
import json
import urllib.request
import os
import time
import sys

API_URL = "https://api.anthropic.com/v1/messages"
MODEL = "claude-sonnet-4-20250514"
TOTAL_CHAPTERS = 28
OUTPUT_FILE = "matthieu_simple.json"

# Check for API key
API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
if not API_KEY:
    print()
    print("  ⚠  Kein API-Key gefunden!")
    print()
    print("  So bekommst du einen (kostenlos zum Testen):")
    print("  1. Gehe zu: https://console.anthropic.com/")
    print("  2. Erstelle ein Konto")
    print("  3. Unter 'API Keys' erstelle einen neuen Key")
    print("  4. Dann starte das Script so:")
    print()
    print('     export ANTHROPIC_API_KEY="sk-ant-dein-key-hier"')
    print("     python3 simplify_matthew.py")
    print()
    sys.exit(1)


SYSTEM_PROMPT = """Tu es un expert en français langue étrangère (FLE) et en textes bibliques.

Ta tâche: Réécrire un chapitre de l'Évangile selon Matthieu (Louis Segond 1910) en respectant ces règles:

1. VOCABULAIRE: Utilise uniquement du vocabulaire de niveau A2 (CECR) quand c'est possible.
   - Remplace les mots difficiles par des synonymes simples
   - EXCEPTIONS: Garde les termes bibliques/religieux qui n'ont pas de synonyme simple (ex: baptiser, prophète, temple, figuier, parabole, crucifier, pharisiens, disciples, ange, circoncire, sabbat, synagogue, etc.)
   - Garde tous les noms propres tels quels (Jésus, Pierre, Hérode, Jérusalem, etc.)
   - Préfère les mots courts et courants

2. TEMPS VERBAUX: Convertis TOUS les passé simple en passé composé.
   - "il dit" → "il a dit"
   - "ils allèrent" → "ils sont allés"
   - "il vint" → "il est venu"
   - "elle répondit" → "elle a répondu"
   - "il prit" → "il a pris"
   - "ils virent" → "ils ont vu"
   - Attention aux verbes qui prennent être: aller, venir, partir, arriver, entrer, sortir, monter, descendre, naître, mourir, rester, tomber, retourner, devenir, passer

3. STRUCTURE: Garde exactement la même numérotation de versets. Ne fusionne pas et ne supprime pas de versets.

4. SENS: Le sens du texte doit rester fidèle à l'original. Ne simplifie pas au point de perdre le sens théologique.

5. FORMAT: Retourne UNIQUEMENT un JSON array de versets, sans aucun texte supplémentaire, sans markdown:
[{"n": 1, "text": "..."}, {"n": 2, "text": "..."}, ...]"""


def call_api(chapter_num):
    """Call the Anthropic API to simplify one chapter."""
    user_msg = f"""Réécris le chapitre {chapter_num} de l'Évangile selon Matthieu (Louis Segond 1910) en français simplifié (niveau A2) avec passé composé au lieu de passé simple.

Donne le texte COMPLET du chapitre, tous les versets, sans en oublier aucun.

Retourne UNIQUEMENT le JSON array des versets."""

    payload = json.dumps({
        "model": MODEL,
        "max_tokens": 8000,
        "system": SYSTEM_PROMPT,
        "messages": [{"role": "user", "content": user_msg}]
    }).encode("utf-8")

    req = urllib.request.Request(API_URL, data=payload, headers={
        "Content-Type": "application/json",
        "x-api-key": API_KEY,
        "anthropic-version": "2023-06-01"
    })

    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        text = data["content"][0]["text"].strip()
        # Clean up potential markdown fencing
        if text.startswith("```"):
            text = text.split("\n", 1)[1]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()
        return json.loads(text)


def main():
    print()
    print("═" * 55)
    print("  Matthäus vereinfachen (A2 + passé composé)")
    print("  Louis Segond 1910 → Version simplifiée")
    print("═" * 55)
    print()

    # Load existing progress if any
    chapters = []
    done_chapters = set()
    if os.path.exists(OUTPUT_FILE):
        try:
            with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
                existing = json.load(f)
                chapters = existing.get("chapters", [])
                done_chapters = {c["number"] for c in chapters}
                if done_chapters:
                    print(f"  ℹ Fortfahren: {len(done_chapters)}/{TOTAL_CHAPTERS} Kapitel bereits fertig")
                    print()
        except:
            pass

    failed = []

    for ch in range(1, TOTAL_CHAPTERS + 1):
        if ch in done_chapters:
            continue

        print(f"  [{ch:2d}/{TOTAL_CHAPTERS}] Kapitel {ch}...", end=" ", flush=True)
        try:
            verses = call_api(ch)
            if verses and isinstance(verses, list):
                chapters.append({"number": ch, "verses": verses})
                done_chapters.add(ch)
                print(f"✓ ({len(verses)} Verse)")
                # Save after each chapter (resume support)
                save_output(chapters)
            else:
                failed.append(ch)
                print("✗ ungültiges Format")
        except Exception as e:
            failed.append(ch)
            print(f"✗ {e}")

        time.sleep(1)

    # Retry failed chapters
    if failed:
        print(f"\n  Wiederhole {len(failed)} fehlgeschlagene Kapitel...\n")
        for ch in failed[:]:
            print(f"  Retry Kapitel {ch}...", end=" ", flush=True)
            time.sleep(3)
            try:
                verses = call_api(ch)
                if verses and isinstance(verses, list):
                    chapters.append({"number": ch, "verses": verses})
                    failed.remove(ch)
                    print(f"✓ ({len(verses)} Verse)")
                    save_output(chapters)
                else:
                    print("✗")
            except Exception as e:
                print(f"✗ {e}")

    save_output(chapters)

    total_verses = sum(len(c["verses"]) for c in chapters)
    print()
    print(f"  ✓ Fertig! {len(chapters)}/{TOTAL_CHAPTERS} Kapitel, {total_verses} Verse")
    if failed:
        print(f"  ⚠ Fehlgeschlagen: Kapitel {', '.join(str(c) for c in failed)}")
        print(f"  → Starte das Script nochmal, es fährt dort fort wo es aufgehört hat")
    print(f"  ✓ Gespeichert: {OUTPUT_FILE}")
    print()


def save_output(chapters):
    """Save current progress."""
    chapters_sorted = sorted(chapters, key=lambda c: c["number"])
    output = {
        "book": "Matthieu",
        "translation": "Louis Segond 1910 — Version simplifiée A2",
        "description": "Vocabulaire simplifié au niveau A2, passé simple converti en passé composé",
        "language": "fr",
        "chapters": chapters_sorted
    }
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
