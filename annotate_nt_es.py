#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════
  Nuevo Testamento — Anotación palabra por palabra (Español → Inglés)

  Anota CADA palabra del texto español (Reina-Valera 1909, versión
  modernizada "rv1909mod") con:
  - Forma (como aparece en el texto)
  - Lema (forma base / infinitivo)
  - Nivel CEFR (A1–C2) para un estudiante de español como lengua extranjera
  - Traducción al inglés dependiente del contexto

  Pilot run: un solo libro (ONLY_BOOKS), pensado para evaluar calidad
  antes de escalar a todo el NT.

  Llama a la API en lotes pequeños de VERSE_BATCH versículos (no un
  capítulo entero de una vez) — respuestas más chicas, más rápidas y
  reiniciables verso por verso si algo falla a mitad de camino.

  SETUP:
    export ANTHROPIC_API_KEY="sk-ant-..."
    python3 annotate_nt_es.py

  Lee bibles/spa/rv1909mod/{nr}_rv1909mod.json (uno por libro).
  Escribe bibles/spa/rv1909mod/anno/{nr}_rv1909mod_eng.json
  (mismo esquema que bibles/eng/web/anno/{nr}_web_deu.json, pero con "en"
  en vez de "de"). Guarda progreso después de cada lote — reiniciable.
═══════════════════════════════════════════════════════════════
"""
import json
import os
import sys
import time
import re
import subprocess
import tempfile


API_URL = "https://api.anthropic.com/v1/messages"
MODEL = "claude-sonnet-5"
BIBLE_DIR = "bibles/spa/rv1909mod"
ANNO_DIR = "bibles/spa/rv1909mod/anno"

# Libros a anotar en esta corrida (nr de libro). None = todos los que falten.
# Piloto: 40 = Mateo
ONLY_BOOKS = [40]

# Versículos por llamada a la API — chico a propósito, para respuestas
# rápidas y confiables (capítulos densos como genealogías necesitan
# muchas anotaciones por versículo).
VERSE_BATCH = 6
REQUEST_TIMEOUT = 150
MAX_ATTEMPTS = 6

API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
if not API_KEY:
    print("\n  ⚠  Sin API key! → export ANTHROPIC_API_KEY='sk-ant-...'\n")
    sys.exit(1)

os.makedirs(ANNO_DIR, exist_ok=True)

SYSTEM_PROMPT = """You are an expert linguist reviewing/producing Spanish→English word-by-word Bible annotations, for English-speaking learners of Spanish (as a foreign language, "ELE" perspective) who are reading the Reina-Valera 1909 (modernized spelling) Spanish Bible.

## Translation philosophy

1. **Word-by-word is the default.** Annotate EVERY word in the verse, from A1 through C2 — do not skip common words. Each word gets the contextually correct English translation, so the result is understandable when reading word-by-word under the Spanish text.

2. **Multi-word phrases** are ONLY used when word-by-word translation would be incomprehensible or seriously misleading. Examples:
   - Fixed idioms: "dar a luz" → "to give birth" (word-by-word "give to light" is nonsensical)
   - Verbal periphrases with shifted meaning: "acabar de" (+ inf.) → "to have just (done)"
   - BUT: transparent constructions work fine word-by-word — keep as single words, NOT as phrases

3. **Proper nouns** (Jesús, Abraham, David, Jerusalén, etc.) MUST be annotated with their English equivalent (Jesús → Jesus, Moisés → Moses, Isaías → Isaiah, Egipto → Egypt). Level is always A1.

4. **Spanish-specific word forms — treat as ONE token (position = word split by whitespace), never split:**
   - Contractions "del" (de + el) → "of the", "al" (a + el) → "to the/at the". Lemma = "del"/"al", level A1.
   - Enclitic pronouns attached to infinitives/gerunds/affirmative imperatives (e.g. "decirle" = decir+le, "viéndolo" = viendo+lo, "escúchame" = escucha+me): annotate the WHOLE word as one entry. Lemma = the base verb infinitive (e.g. "decir", "ver", "escuchar"). The English translation ("en") should convey the full meaning including the pronoun, e.g. "escúchame" → "listen to me", "decirle" → "to tell him/her".
   - Reflexive verbs (e.g. "se levantó", "arrepentíos"): the reflexive pronoun ("se") is its own token when written separately (annotate separately, level A1, en "himself/herself/itself/themselves" or omit if purely grammatical — use judgment), but when attached ("arrepentíos" = arrepentid+os) treat as one token like the enclitic-pronoun case above.

5. **Positions** must be exact: pos = 0-based index of the word in the verse (split by spaces, exactly matching the given text). Each occurrence of a word gets its OWN annotation at its OWN position — if "el" appears at positions 0, 3, and 8, there must be three separate annotations.

6. **Multi-word phrases** use "pos" for the first word and "pos_end" for the last word. Words covered by a phrase MUST ALSO get their own individual single-word annotations, so the app can show the phrase translation first, then individual word translations on tap.

7. **CEFR level** is for a learner of Spanish as a foreign language, of the LEMMA (not the inflected form). Calibrate roughly like: A1 = the ~500 most basic everyday words (agua, casa, decir, bueno, día...); A2 = common everyday vocabulary; B1 = general vocabulary needed for most topics (generación, camino, servir...); B2 = more abstract/less frequent vocabulary (linaje, testimonio, injusticia...); C1 = literary/formal/specialized vocabulary (engendrar, primogénito, concupiscencia...); C2 = rare, archaic, or highly specialized/theological vocabulary. Biblical/religious vocabulary (profeta, sacerdote, pecado, salvación) is typically B1–B2 since it's thematically central to this text, not because it's rare.

8. **English translations** must be contextually correct and natural English, matching the grammatical role (tense, number) of the Spanish word in this specific verse — not just a dictionary default.

## Output format

Return ONLY a JSON object, no markdown or comments. Keys = verse numbers (as strings). Values = arrays of annotations for that verse. If somehow a verse had zero content, use an empty array.

Single word:
  {"pos": 3, "form": "padre", "lemma": "padre", "level": "A1", "en": "father"}

Multi-word phrase — include the phrase AND individual annotations for each covered word:
  {"pos": 2, "pos_end": 3, "form": "dar a luz", "lemma": "dar a luz", "level": "B1", "en": "to give birth"},
  {"pos": 2, "form": "dar", "lemma": "dar", "level": "A1", "en": "to give"},
  {"pos": 3, "form": "a", "lemma": "a", "level": "A1", "en": "to"}

CEFR levels: A1, A2, B1, B2, C1, C2"""


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


# ─── API call ─────────────────────────────────────────────────────────────────
# Uses curl (subprocess) instead of urllib: in this environment, requests go
# through a local proxy that can hold a socket ESTABLISHED indefinitely without
# delivering data, which defeats Python's socket-level `timeout=`. curl's
# --max-time enforces a hard wall-clock deadline at the process level instead.

def _call_via_curl(payload_bytes):
    last_err = None
    for attempt in range(MAX_ATTEMPTS):
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tf:
            tf.write(payload_bytes)
            payload_path = tf.name
        try:
            proc = subprocess.run(
                ["curl", "-sS", "--max-time", str(REQUEST_TIMEOUT), API_URL,
                 "-H", "content-type: application/json",
                 "-H", f"x-api-key: {API_KEY}",
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


def annotate_batch(book_name, chapter_num, verse_items):
    """verse_items: list of (vnum_str, text_str), already sorted."""
    verses_text = "\n".join(f"{n}. {t}" for n, t in verse_items)
    payload = json.dumps({
        "model": MODEL,
        "max_tokens": 16000,
        "thinking": {"type": "disabled"},
        "system": SYSTEM_PROMPT,
        "messages": [{
            "role": "user",
            "content": (
                f"Here are verses from chapter {chapter_num} of {book_name} "
                f"(Reina-Valera 1909, modernized spelling).\n"
                "Annotate EVERY word (A1 through C2) with its form, lemma, "
                "CEFR level and contextual English translation.\n\n"
                f"{verses_text}\n\n"
                "Return ONLY the JSON object."
            )
        }]
    }).encode("utf-8")

    data = _call_via_curl(payload)

    if data.get("type") == "error":
        raise RuntimeError(f"API error: {data.get('error')}")
    text_block = next(b for b in data["content"] if b.get("type") == "text")
    text = text_block["text"].strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1]
    if text.endswith("```"):
        text = text[:-3]
    return json.loads(text.strip())


# ─── Persistence ──────────────────────────────────────────────────────────────

def anno_path(book_nr):
    return os.path.join(ANNO_DIR, f"{book_nr}_rv1909mod_eng.json")


def load_progress(book_nr):
    path = anno_path(book_nr)
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("chapters", {})
    except Exception:
        return {}


def save_progress(book_nr, book_name, chapters):
    output = {"name": book_name, "chapters": chapters}
    tmp_path = anno_path(book_nr) + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    os.replace(tmp_path, anno_path(book_nr))


def chunk(items, size):
    for i in range(0, len(items), size):
        yield items[i:i + size]


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    print()
    print("═" * 58)
    print("  Nuevo Testamento — Anotación palabra por palabra (ES→EN)")
    print(f"  Lotes de {VERSE_BATCH} versículos · modelo {MODEL}")
    print("═" * 58)
    print()

    with open(os.path.join(BIBLE_DIR, "..", "..", "index.json"), "r", encoding="utf-8") as f:
        index = json.load(f)
    nt_books = [b for b in index["books"]
                if b["testament"] == "nt" and (ONLY_BOOKS is None or b["nr"] in ONLY_BOOKS)]

    grand_failed = []

    for book in nt_books:
        book_nr = book["nr"]
        src_path = os.path.join(BIBLE_DIR, f"{book_nr}_rv1909mod.json")
        with open(src_path, "r", encoding="utf-8") as f:
            src = json.load(f)
        book_name = src["name"]
        chapters_src = src["chapters"]  # {chNum: {verseNum: text}}
        total_ch = len(chapters_src)

        chapters_out = load_progress(book_nr)

        done_ch = sum(
            1 for c, vm in chapters_src.items()
            if len(chapters_out.get(c, {})) >= len(vm)
        )
        print(f"\n  {book_name} ({total_ch} capítulos, {done_ch} ya completos)")
        print(f"  {'─' * 50}")

        failed_batches = []

        for ch_num in sorted(chapters_src.keys(), key=int):
            verse_map = chapters_src[ch_num]
            ch_out = chapters_out.setdefault(ch_num, {})
            missing = [(v, t) for v, t in sorted(verse_map.items(), key=lambda x: int(x[0]))
                       if v not in ch_out]

            if not missing:
                continue

            batches = list(chunk(missing, VERSE_BATCH))
            for bi, batch in enumerate(batches, 1):
                v_lo, v_hi = batch[0][0], batch[-1][0]
                label = f"Cap {ch_num.rjust(3)}/{total_ch} v{v_lo}-{v_hi}"
                print(f"    {label} ...", end=" ", flush=True)
                try:
                    result = annotate_batch(book_name, ch_num, batch)
                    if not isinstance(result, dict):
                        failed_batches.append((ch_num, batch))
                        print("✗ formato inválido")
                        continue
                    fixed = correct_positions(result, verse_map)
                    total_ann = sum(len(v) for v in result.values())
                    fix_note = f" [{fixed} corr.]" if fixed else ""
                    ch_out.update(result)
                    print(f"✓ {total_ann} anotaciones{fix_note}")
                    save_progress(book_nr, book_name, chapters_out)
                except Exception as e:
                    failed_batches.append((ch_num, batch))
                    print(f"✗ {str(e)[:120]}")
                time.sleep(1)

        if failed_batches:
            print(f"\n    Reintentando {len(failed_batches)} lotes fallidos ...")
            for ch_num, batch in failed_batches[:]:
                verse_map = chapters_src[ch_num]
                ch_out = chapters_out.setdefault(ch_num, {})
                v_lo, v_hi = batch[0][0], batch[-1][0]
                print(f"    Retry cap {ch_num} v{v_lo}-{v_hi} ...", end=" ", flush=True)
                time.sleep(3)
                try:
                    result = annotate_batch(book_name, ch_num, batch)
                    if isinstance(result, dict):
                        fixed = correct_positions(result, verse_map)
                        total_ann = sum(len(v) for v in result.values())
                        fix_note = f" [{fixed} corr.]" if fixed else ""
                        ch_out.update(result)
                        failed_batches.remove((ch_num, batch))
                        print(f"✓ {total_ann} anotaciones{fix_note}")
                        save_progress(book_nr, book_name, chapters_out)
                    else:
                        print("✗")
                except Exception as e:
                    print(f"✗ {str(e)[:120]}")

        grand_failed.extend([(book_name, ch, batch[0][0]) for ch, batch in failed_batches])

    print()
    print("═" * 58)
    if grand_failed:
        print("  ⚠  Fallidos:")
        for bk, ch, v in grand_failed:
            print(f"     {bk} cap. {ch} (desde v{v})")
        print("  → Ejecutar de nuevo para continuar")
    print("  ✓ Listo")
    print()


if __name__ == "__main__":
    main()
