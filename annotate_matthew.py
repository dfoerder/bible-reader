#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════
  Matthäus — Wort-für-Wort Annotation
  
  Annotiert jedes B1+ Wort im Matthäus-Evangelium mit:
  - Wortform (wie im Text)
  - Lemma (Grundform)
  - CEFR-Niveau (B1, B2, C1, C2)
  - Kontextabhängige deutsche Übersetzung
  
  SETUP:
    export ANTHROPIC_API_KEY="sk-ant-..."
    python3 annotate_matthew.py
    
  Benötigt bible_nt.json im selben Ordner.
  Speichert nach jedem Kapitel — bei Abbruch einfach nochmal starten.
    
  KOSTEN: ca. 3-5 USD
═══════════════════════════════════════════════════════════════
"""
import json
import urllib.request
import os
import sys
import time
import re

API_URL = "https://api.anthropic.com/v1/messages"
MODEL = "claude-sonnet-4-20250514"
OUTPUT_FILE = "matthieu_annotations.json"
BIBLE_FILE = "bible_nt.json"

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


def load_matthew():
    """Load Matthew from bible_nt.json."""
    with open(BIBLE_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    for book in data.get("books", []):
        if book.get("name", "").lower().startswith("mat"):
            return book
        # Also try by book number (Matthew = 40)
        if book.get("nr") == 40:
            return book
    
    print("  ⚠  Matthäus nicht in bible_nt.json gefunden!")
    sys.exit(1)


def annotate_chapter(chapter_num, verses_text):
    """Call the API to annotate one chapter."""
    payload = json.dumps({
        "model": MODEL,
        "max_tokens": 16000,
        "system": SYSTEM_PROMPT,
        "messages": [{"role": "user", "content": f"""Voici le chapitre {chapter_num} de l'Évangile selon Matthieu (Louis Segond 1910).
Annote chaque mot de niveau B1+ avec sa forme, son lemme, son niveau CECR et sa traduction allemande contextuelle.

{verses_text}

Retourne UNIQUEMENT le JSON object."""}]
    }).encode("utf-8")

    req = urllib.request.Request(API_URL, data=payload, headers={
        "Content-Type": "application/json",
        "x-api-key": API_KEY,
        "anthropic-version": "2023-06-01"
    })

    with urllib.request.urlopen(req, timeout=180) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        text = data["content"][0]["text"].strip()
        # Clean markdown fencing
        if text.startswith("```"):
            text = text.split("\n", 1)[1]
        if text.endswith("```"):
            text = text[:-3]
        return json.loads(text.strip())


def main():
    print()
    print("═" * 55)
    print("  Matthäus — Wort-für-Wort Annotation")
    print("  Lemma · CEFR-Niveau · Deutsche Übersetzung")
    print("═" * 55)
    print()

    matthew = load_matthew()
    chapters = matthew.get("chapters", [])
    total = len(chapters)
    print(f"  {matthew['name']}: {total} Kapitel gefunden\n")

    # Load existing progress
    result = {}
    if os.path.exists(OUTPUT_FILE):
        try:
            with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
                existing = json.load(f)
                result = existing.get("chapters", {})
                if result:
                    print(f"  ℹ Fortschritt: {len(result)}/{total} Kapitel bereits annotiert\n")
        except:
            pass

    failed = []

    for chapter in chapters:
        ch_num = str(chapter["number"])
        if ch_num in result:
            continue

        # Build verse text
        verses_text = "\n".join(
            f"{v['n']}. {v['text']}" for v in chapter["verses"]
        )

        print(f"  [{ch_num.rjust(2)}/{total}] Kapitel {ch_num}...", end=" ", flush=True)

        try:
            annotations = annotate_chapter(chapter["number"], verses_text)
            if annotations and isinstance(annotations, dict):
                # Count total annotations
                total_ann = sum(len(v) for v in annotations.values())
                result[ch_num] = annotations
                print(f"✓ ({total_ann} Annotationen)")
                save_output(result, matthew["name"])
            else:
                failed.append(ch_num)
                print("✗ ungültiges Format")
        except Exception as e:
            failed.append(ch_num)
            err_msg = str(e)[:80]
            print(f"✗ {err_msg}")

        time.sleep(1)

    # Retry
    if failed:
        print(f"\n  Wiederhole {len(failed)} fehlgeschlagene Kapitel...\n")
        for ch_num in failed[:]:
            chapter = next((c for c in chapters if str(c["number"]) == ch_num), None)
            if not chapter:
                continue
            verses_text = "\n".join(f"{v['n']}. {v['text']}" for v in chapter["verses"])
            print(f"  Retry Kapitel {ch_num}...", end=" ", flush=True)
            time.sleep(3)
            try:
                annotations = annotate_chapter(int(ch_num), verses_text)
                if annotations and isinstance(annotations, dict):
                    total_ann = sum(len(v) for v in annotations.values())
                    result[ch_num] = annotations
                    failed.remove(ch_num)
                    print(f"✓ ({total_ann} Annotationen)")
                    save_output(result, matthew["name"])
                else:
                    print("✗")
            except Exception as e:
                print(f"✗ {str(e)[:80]}")

    save_output(result, matthew["name"])

    total_annotations = sum(
        sum(len(v) for v in ch.values())
        for ch in result.values()
    )
    print()
    print(f"  ✓ Fertig! {len(result)}/{total} Kapitel")
    print(f"  ✓ {total_annotations} Wörter annotiert")
    if failed:
        print(f"  ⚠ Fehlgeschlagen: Kapitel {', '.join(failed)}")
        print(f"  → Script nochmal starten zum Fortfahren")
    print(f"  ✓ Gespeichert: {OUTPUT_FILE}")
    print()


def save_output(chapters, book_name):
    output = {
        "book": book_name,
        "description": "Wort-für-Wort Annotationen: Lemma, CEFR-Niveau, kontextabhängige DE-Übersetzung",
        "levels": "B1, B2, C1, C2 (A1/A2 sind ausgelassen)",
        "chapters": chapters
    }
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
