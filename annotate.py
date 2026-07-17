#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════
  Wort-für-Wort-Annotation — sprachparametrisiert (eine Pipeline für alle)

  Ersetzt annotate_nt_en.py / annotate_ot_en.py / annotate_a1a2.py und
  verallgemeinert annotate_nt_es.py. EIN Durchlauf annotiert A1–C2 (kein
  separater A1/A2-Nachtrag mehr).

  Konzept (aus dem ES-Skript übernommen, für alle Sprachen):
  - Word-by-word als Default: JEDES Wort A1–C2 bekommt eine kontextrichtige
    Übersetzung in die Hilfssprache (gloss_field).
  - Eigennamen werden annotiert (immer A1, mit Hilfssprachen-Äquivalent).
  - Mehrwort-Phrasen: pos_end + zusätzlich Einzelwort-Annotationen der
    abgedeckten Wörter.
  - Sprachspezifische Tokenisierung (Kontraktionen, Elisionen, Enklitika …)
    steckt pro Sprache im 'tokenization'-Block der LANGS-Config.
  - Kleine Vers-Batches, curl-Transport mit hartem Timeout, Per-Buch-Ausgabe,
    atomares Speichern, verse-genaues Resume.

  AUFRUF:
    export ANTHROPIC_API_KEY="sk-ant-..."
    python3 annotate.py <edition-id> [--books 40,41] [--testament nt|ot]
                        [--batch 6] [--model claude-sonnet-5]

    <edition-id> ist ein Schlüssel aus LANGS (z.B. spa-rv1909mod, fra-lsg1910mod).

  Liest bibles/<dir>/{nr}<suffix>.json (array- ODER dict-Format).
  Schreibt bibles/<dir>/anno/{nr}<anno_suffix>.json (gleiches Schema wie der
  bestehende Bestand). Nach jedem Batch gespeichert — jederzeit neu startbar.
═══════════════════════════════════════════════════════════════
"""
import json
import os
import sys
import time
import re
import argparse
import subprocess
import tempfile

API_URL = "https://api.anthropic.com/v1/messages"
DEFAULT_MODEL = "claude-sonnet-5"
INDEX_FILE = "bibles/index.json"

REQUEST_TIMEOUT = 150
MAX_ATTEMPTS = 6

# ─── Sprach-Konfiguration ───────────────────────────────────────────────────
# Pro Edition: Quell-/Hilfssprache, Gloss-Feld (= Sprachkürzel der Hilfsbibel),
# Dateipfade/-suffixe und die zwei sprachspezifischen Prompt-Blöcke
# (proper_nouns, tokenization, cefr). Alles andere ist gemeinsam.

LANGS = {
    "eng-web": {
        "source_lang": "English", "gloss_lang": "German", "gloss_field": "de",
        "edition_desc": "World English Bible (WEB)",
        "bible_dir": "bibles/eng/web", "suffix": "_web", "anno_suffix": "_web_deu",
        "proper_nouns": "(Jesus → Jesus, Moses → Mose, Egypt → Ägypten, Jerusalem → Jerusalem)",
        "tokenization": (
            "- English needs little special tokenization. Keep possessives with "
            "apostrophe-s as the single token as written (e.g. \"Yahweh's\", \"man's\"); "
            "lemma = the base noun.\n"
            "- Contractions are rare in this text; if one occurs (e.g. \"don't\"), treat it "
            "as one token, lemma = the base verb."
        ),
        "cefr": (
            "A1 = the ~500 most basic everyday words (water, house, say, good, day…); "
            "A2 = common everyday vocabulary; B1 = general vocabulary needed for most topics "
            "(gather, praise, wilderness…); B2 = more abstract/less frequent vocabulary "
            "(covenant, mourn, likewise…); C1 = literary/formal/archaic Bible English "
            "(behold, beget, tabernacle…); C2 = rare, archaic, or highly specialized/theological."
        ),
    },
    "spa-rv1909mod": {
        "source_lang": "Spanish", "gloss_lang": "English", "gloss_field": "en",
        "edition_desc": "Reina-Valera 1909 (modernized spelling)",
        "bible_dir": "bibles/spa/rv1909mod", "suffix": "_rv1909mod", "anno_suffix": "_rv1909mod_eng",
        "proper_nouns": "(Jesús → Jesus, Moisés → Moses, Isaías → Isaiah, Egipto → Egypt)",
        "tokenization": (
            "- Contractions \"del\" (de+el) → \"of the\", \"al\" (a+el) → \"to the/at the\". "
            "Lemma = \"del\"/\"al\", level A1.\n"
            "- Enclitic pronouns attached to infinitives/gerunds/affirmative imperatives "
            "(decirle, viéndolo, escúchame): annotate the WHOLE word as ONE entry. Lemma = the "
            "base verb infinitive (decir, ver, escuchar). The translation conveys the full "
            "meaning including the pronoun (escúchame → \"listen to me\").\n"
            "- Reflexive \"se\" written separately is its own token (A1); when attached "
            "(arrepentíos = arrepentid+os) treat as one token like the enclitic case."
        ),
        "cefr": (
            "A1 = the ~500 most basic everyday words (agua, casa, decir, bueno, día…); "
            "A2 = common everyday vocabulary; B1 = general vocabulary needed for most topics "
            "(generación, camino, servir…); B2 = more abstract/less frequent vocabulary "
            "(linaje, testimonio, injusticia…); C1 = literary/formal/specialized vocabulary "
            "(engendrar, primogénito, concupiscencia…); C2 = rare, archaic, or highly "
            "specialized/theological vocabulary."
        ),
    },
    "fra-lsg1910mod": {
        "source_lang": "French", "gloss_lang": "English", "gloss_field": "en",
        "edition_desc": "Louis Segond 1910 (modernized spelling)",
        "bible_dir": "bibles/fra/lsg1910mod", "suffix": "_lsg1910mod", "anno_suffix": "_lsg1910mod_eng",
        "proper_nouns": "(Jésus → Jesus, Moïse → Moses, Ésaïe → Isaiah, Égypte → Egypt)",
        "tokenization": (
            "- Elisions with an apostrophe are ONE token: l'homme, d'eau, j'ai, qu'il, n'est, "
            "s'il, c'est, jusqu'à. Lemma = the full base word behind the elision "
            "(l' → le/la, d' → de, qu' → que, n' → ne, s' → se, j' → je).\n"
            "- Fused preposition+article are ONE token: du (de+le) → \"of the\", des → "
            "\"of the/some\", au (à+le) → \"to the\", aux → \"to the\". Lemma = the fused form, level A1.\n"
            "- Hyphenated inverted or clitic forms are ONE token: va-t-il, dit-il, celui-ci, "
            "est-ce. Lemma = the base verb/word."
        ),
        "cefr": (
            "A1 = the ~500 most basic everyday words (eau, maison, dire, bon, jour…); "
            "A2 = common everyday vocabulary; B1 = general vocabulary needed for most topics "
            "(chemin, servir, génération…); B2 = more abstract/less frequent vocabulary "
            "(lignée, témoignage, injustice…); C1 = literary/formal/specialized vocabulary "
            "(engendrer, premier-né…); C2 = rare, archaic, or highly specialized/theological."
        ),
    },
    "ita-riv1927mod": {
        "source_lang": "Italian", "gloss_lang": "English", "gloss_field": "en",
        "edition_desc": "Riveduta 1927 (modernized spelling)",
        "bible_dir": "bibles/ita/riv1927mod", "suffix": "_riv1927mod", "anno_suffix": "_riv1927mod_eng",
        "proper_nouns": "(Gesù → Jesus, Mosè → Moses, Isaia → Isaiah, Egitto → Egypt)",
        "tokenization": (
            "- Elisions with an apostrophe are ONE token: l'acqua, dell'uomo, un'anima, "
            "dall'alto. Lemma = the full base word behind the elision (l' → il/la/lo, "
            "dell' → di/del, un' → una).\n"
            "- Fused preposition+article are ONE token: nel (in+il) → \"in the\", della → "
            "\"of the\", sul → \"on the\", dei/degli/alle/coi etc. Lemma = the fused form, level A1.\n"
            "- Enclitic pronouns attached to verbs are ONE token: dirgli (dire+gli), "
            "andarsene (andare+se+ne), ascoltami. Lemma = the base infinitive; the translation "
            "conveys the pronoun (dirgli → \"to tell him\")."
        ),
        "cefr": (
            "A1 = the ~500 most basic everyday words (acqua, casa, dire, buono, giorno…); "
            "A2 = common everyday vocabulary; B1 = general vocabulary needed for most topics "
            "(cammino, servire, generazione…); B2 = more abstract/less frequent vocabulary "
            "(stirpe, testimonianza, ingiustizia…); C1 = literary/formal/specialized vocabulary "
            "(generare, primogenito…); C2 = rare, archaic, or highly specialized/theological."
        ),
    },
}

# ─── System-Prompt (gemeinsam, mit «…»-Platzhaltern) ─────────────────────────
# .replace() statt .format(), damit die geschweiften Klammern der JSON-Beispiele
# unangetastet bleiben.

SYSTEM_TEMPLATE = """You are an expert linguist producing «SOURCE»→«GLOSS» word-by-word Bible annotations, for «GLOSS»-speaking learners of «SOURCE» as a foreign language who are reading the «EDITION».

## Translation philosophy

1. **Word-by-word is the default.** Annotate EVERY word in the verse, from A1 through C2 — do not skip common words. Each word gets the contextually correct «GLOSS» translation, so the result is understandable when reading word-by-word under the «SOURCE» text.

2. **Multi-word phrases** are ONLY used when word-by-word translation would be incomprehensible or seriously misleading (fixed idioms, verbal periphrases with shifted meaning). Transparent constructions stay as single words, NOT as phrases.

3. **Proper nouns** (names of people and places) MUST be annotated with their «GLOSS» equivalent «PROPER_NOUNS». Level is always A1.

4. **«SOURCE»-specific word forms — treat as ONE token (position = word split by whitespace), never split:**
«TOKENIZATION»

5. **Positions** must be exact: pos = 0-based index of the word in the verse (split by spaces, exactly matching the given text). Each occurrence of a word gets its OWN annotation at its OWN position — if a word appears at positions 0, 3 and 8, there must be three separate annotations.

6. **Multi-word phrases** use "pos" for the first word and "pos_end" for the last word. Words covered by a phrase MUST ALSO get their own individual single-word annotations, so the app can show the phrase translation first, then individual word translations on tap.

7. **CEFR level** is for a learner of «SOURCE» as a foreign language, of the LEMMA (not the inflected form). Calibrate roughly like:
«CEFR»
Biblical/religious vocabulary (prophet, priest, sin, salvation) is typically B1–B2 since it is thematically central to this text, not because it is rare.

8. **«GLOSS» translations** must be contextually correct and natural «GLOSS», matching the grammatical role (tense, number) of the «SOURCE» word in this specific verse — not just a dictionary default.

## Output format

Return ONLY a JSON object, no markdown or comments. Keys = verse numbers (as strings). Values = arrays of annotations for that verse. If a verse somehow had zero content, use an empty array.

Single word:
  {"pos": 3, "form": "<form>", "lemma": "<lemma>", "level": "A1", "«FIELD»": "<translation>"}

Multi-word phrase — include the phrase AND individual annotations for each covered word:
  {"pos": 2, "pos_end": 3, "form": "<phrase>", "lemma": "<phrase lemma>", "level": "B1", "«FIELD»": "<translation>"},
  {"pos": 2, "form": "<word1>", "lemma": "<lemma1>", "level": "A1", "«FIELD»": "<t1>"},
  {"pos": 3, "form": "<word2>", "lemma": "<lemma2>", "level": "A1", "«FIELD»": "<t2>"}

CEFR levels: A1, A2, B1, B2, C1, C2"""


def build_system_prompt(cfg):
    return (SYSTEM_TEMPLATE
            .replace("«SOURCE»", cfg["source_lang"])
            .replace("«GLOSS»", cfg["gloss_lang"])
            .replace("«FIELD»", cfg["gloss_field"])
            .replace("«EDITION»", cfg["edition_desc"])
            .replace("«PROPER_NOUNS»", cfg["proper_nouns"])
            .replace("«TOKENIZATION»", cfg["tokenization"])
            .replace("«CEFR»", cfg["cefr"]))


# ─── Position correction ─────────────────────────────────────────────────────

def _normalize(word):
    return re.sub(r"[.,;:!?()\[\]\"’‘«»—–…¡¿*]", "", word).lower()


def correct_positions(batch_annotations, verse_map):
    corrections = 0
    for verse_key, annotations in batch_annotations.items():
        text = verse_map.get(verse_key, "")
        if not text:
            continue
        words = text.split()
        for ann in annotations:
            pos = ann.get("pos", -1)
            form = ann.get("form", "")
            form_norm = _normalize(form.split()[0] if "pos_end" in ann else form)
            if not form_norm:
                continue
            if 0 <= pos < len(words) and _normalize(words[pos]) == form_norm:
                continue
            found = -1
            for i, w in enumerate(words):
                if _normalize(w) == form_norm:
                    found = i
                    break
            if found >= 0:
                ann["pos"] = found
                corrections += 1
    return corrections


# ─── API call (curl-Subprozess mit hartem Wall-Clock-Timeout) ────────────────
# urllib scheitert hier, weil Requests durch einen lokalen Proxy laufen, der einen
# Socket ESTABLISHED halten kann, ohne Daten zu liefern — das umgeht Pythons
# socket-timeout. curls --max-time erzwingt eine harte Deadline auf Prozessebene.

def _call_via_curl(payload_bytes, api_key):
    last_err = None
    for attempt in range(MAX_ATTEMPTS):
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tf:
            tf.write(payload_bytes)
            payload_path = tf.name
        try:
            proc = subprocess.run(
                ["curl", "-sS", "--max-time", str(REQUEST_TIMEOUT), API_URL,
                 "-H", "content-type: application/json",
                 "-H", f"x-api-key: {api_key}",
                 "-H", "anthropic-version: 2023-06-01",
                 "--data-binary", f"@{payload_path}"],
                capture_output=True, timeout=REQUEST_TIMEOUT + 15
            )
            if proc.returncode != 0:
                last_err = RuntimeError(
                    f"curl exit {proc.returncode}: {proc.stderr.decode('utf-8', 'replace')[:200]}"
                )
                time.sleep(3 * (attempt + 1))
                continue
            try:
                return json.loads(proc.stdout.decode("utf-8"))
            except json.JSONDecodeError as e:
                last_err = e
                time.sleep(3 * (attempt + 1))
                continue
        except subprocess.TimeoutExpired as e:
            last_err = e
            time.sleep(3 * (attempt + 1))
        finally:
            try:
                os.unlink(payload_path)
            except OSError:
                pass
    raise last_err


def annotate_batch(cfg, system_prompt, api_key, model, book_name, chapter_num, verse_items):
    """verse_items: list of (vnum_str, text_str), already sorted."""
    verses_text = "\n".join(f"{n}. {t}" for n, t in verse_items)
    payload = json.dumps({
        "model": model,
        "max_tokens": 16000,
        "thinking": {"type": "disabled"},
        "system": system_prompt,
        "messages": [{
            "role": "user",
            "content": (
                f"Here are verses from chapter {chapter_num} of {book_name} "
                f"({cfg['edition_desc']}).\n"
                f"Annotate EVERY word (A1 through C2) with its form, lemma, "
                f"CEFR level and contextual {cfg['gloss_lang']} translation.\n\n"
                f"{verses_text}\n\n"
                "Return ONLY the JSON object."
            )
        }]
    }).encode("utf-8")

    data = _call_via_curl(payload, api_key)

    if data.get("type") == "error":
        raise RuntimeError(f"API error: {data.get('error')}")
    text_block = next(b for b in data["content"] if b.get("type") == "text")
    text = text_block["text"].strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1]
    if text.endswith("```"):
        text = text[:-3]
    return json.loads(text.strip())


# ─── Quell- und Ausgabe-IO ──────────────────────────────────────────────────

def load_book_source(cfg, book_nr):
    """Liest ein Quell-Buch und normalisiert auf {chNum_str: {vNum_str: text}} —
    egal ob array-Format (eng) oder dict-Format (spa/fra/ita)."""
    path = os.path.join(cfg["bible_dir"], f"{book_nr}{cfg['suffix']}.json")
    if not os.path.exists(path):
        return None, None
    with open(path, "r", encoding="utf-8") as f:
        d = json.load(f)
    name = d.get("name", f"Book {book_nr}")
    chapters = {}
    raw = d["chapters"]
    if isinstance(raw, list):  # array-Format
        for ch in raw:
            cn = str(ch["number"])
            chapters[cn] = {str(v["n"]): v["text"] for v in ch.get("verses", [])}
    else:  # dict-Format
        for cn, verses in raw.items():
            if isinstance(verses, list):
                chapters[str(cn)] = {str(v["n"]): v["text"] for v in verses}
            else:
                chapters[str(cn)] = {str(vn): t for vn, t in verses.items()}
    return name, chapters


def anno_path(cfg, book_nr):
    return os.path.join(cfg["bible_dir"], "anno", f"{book_nr}{cfg['anno_suffix']}.json")


def load_progress(cfg, book_nr):
    path = anno_path(cfg, book_nr)
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f).get("chapters", {})
    except Exception:
        return {}


def save_progress(cfg, book_nr, book_name, chapters):
    os.makedirs(os.path.join(cfg["bible_dir"], "anno"), exist_ok=True)
    output = {"name": book_name, "chapters": chapters}
    tmp = anno_path(cfg, book_nr) + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    os.replace(tmp, anno_path(cfg, book_nr))


def chunk(items, size):
    for i in range(0, len(items), size):
        yield items[i:i + size]


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(description="Sprachparametrisierte Bibel-Wortannotation")
    ap.add_argument("edition", choices=list(LANGS.keys()), help="Edition-ID aus LANGS")
    ap.add_argument("--books", help="Buch-Nummern, kommagetrennt (z.B. 40,41). Default: alle")
    ap.add_argument("--testament", choices=["ot", "nt"], help="Nur AT oder NT")
    ap.add_argument("--batch", type=int, default=6, help="Verse pro API-Call (Default 6)")
    ap.add_argument("--model", default=DEFAULT_MODEL, help=f"Modell (Default {DEFAULT_MODEL})")
    args = ap.parse_args()

    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        print("\n  ⚠  Kein API key! → export ANTHROPIC_API_KEY='sk-ant-...'\n")
        sys.exit(1)

    cfg = LANGS[args.edition]
    system_prompt = build_system_prompt(cfg)

    only_books = None
    if args.books:
        only_books = {int(x) for x in args.books.split(",") if x.strip()}

    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        index = json.load(f)
    books = [b for b in index["books"]
             if (only_books is None or b["nr"] in only_books)
             and (args.testament is None or b["testament"] == args.testament)]

    print()
    print("═" * 62)
    print(f"  Annotation {cfg['source_lang']}→{cfg['gloss_lang']} · {args.edition}")
    print(f"  {len(books)} Bücher · Batches à {args.batch} Verse · Modell {args.model}")
    print("═" * 62)

    grand_failed = []

    for book in books:
        book_nr = book["nr"]
        book_name, chapters_src = load_book_source(cfg, book_nr)
        if chapters_src is None:
            print(f"\n  ⚠  Quelle fehlt für Buch {book_nr} ({book['name']}) — übersprungen")
            continue
        total_ch = len(chapters_src)
        chapters_out = load_progress(cfg, book_nr)

        done_ch = sum(1 for c, vm in chapters_src.items()
                      if len(chapters_out.get(c, {})) >= len(vm))
        print(f"\n  {book_name} ({total_ch} Kapitel, {done_ch} komplett)")
        print(f"  {'─' * 52}")

        failed_batches = []

        for ch_num in sorted(chapters_src.keys(), key=int):
            verse_map = chapters_src[ch_num]
            ch_out = chapters_out.setdefault(ch_num, {})
            missing = [(v, t) for v, t in sorted(verse_map.items(), key=lambda x: int(x[0]))
                       if v not in ch_out]
            if not missing:
                continue

            for batch in chunk(missing, args.batch):
                v_lo, v_hi = batch[0][0], batch[-1][0]
                print(f"    Kap {ch_num.rjust(3)}/{total_ch} v{v_lo}-{v_hi} ...", end=" ", flush=True)
                try:
                    result = annotate_batch(cfg, system_prompt, api_key, args.model,
                                            book_name, ch_num, batch)
                    if not isinstance(result, dict):
                        failed_batches.append((ch_num, batch))
                        print("✗ ungültiges Format")
                        continue
                    fixed = correct_positions(result, verse_map)
                    total_ann = sum(len(v) for v in result.values())
                    fix_note = f" [{fixed} korr.]" if fixed else ""
                    ch_out.update(result)
                    print(f"✓ {total_ann} Annotationen{fix_note}")
                    save_progress(cfg, book_nr, book_name, chapters_out)
                except Exception as e:
                    failed_batches.append((ch_num, batch))
                    print(f"✗ {str(e)[:120]}")
                time.sleep(1)

        if failed_batches:
            print(f"\n    Wiederhole {len(failed_batches)} fehlgeschlagene Batches ...")
            for ch_num, batch in failed_batches[:]:
                verse_map = chapters_src[ch_num]
                ch_out = chapters_out.setdefault(ch_num, {})
                v_lo, v_hi = batch[0][0], batch[-1][0]
                print(f"    Retry Kap {ch_num} v{v_lo}-{v_hi} ...", end=" ", flush=True)
                time.sleep(3)
                try:
                    result = annotate_batch(cfg, system_prompt, api_key, args.model,
                                            book_name, ch_num, batch)
                    if isinstance(result, dict):
                        fixed = correct_positions(result, verse_map)
                        total_ann = sum(len(v) for v in result.values())
                        fix_note = f" [{fixed} korr.]" if fixed else ""
                        ch_out.update(result)
                        failed_batches.remove((ch_num, batch))
                        print(f"✓ {total_ann} Annotationen{fix_note}")
                        save_progress(cfg, book_nr, book_name, chapters_out)
                    else:
                        print("✗")
                except Exception as e:
                    print(f"✗ {str(e)[:120]}")

        grand_failed.extend([(book_name, ch, batch[0][0]) for ch, batch in failed_batches])

    print()
    print("═" * 62)
    if grand_failed:
        print("  ⚠  Fehlgeschlagen:")
        for bk, ch, v in grand_failed:
            print(f"     {bk} Kap. {ch} (ab v{v})")
        print("  → Skript erneut ausführen, um fortzusetzen")
    print("  ✓ Fertig")
    print()


if __name__ == "__main__":
    main()
