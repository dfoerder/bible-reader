#!/usr/bin/env python3
"""Erzeugt für jedes Wort in bibles/eng/web/train/words.json drei deutsche Felder über die Opus Batch API:
  de     = saubere Grundform/Lemma-Übersetzung   (Vokabel-Quiz)
  deForm = an die Wortform im Satz angepasste Übersetzung (Numerus/Tempus) (Lückentext)
  form   = Merkmal-Tag für Distraktor-Matching: sg|pl (Substantive),
           inf|pres|past|part (Verben), base (sonst)

Run:  python3 generate_deform.py            (submit + poll + write)
      python3 generate_deform.py --resume <batch_id>   (laufenden Batch abholen)
      python3 generate_deform.py --write    (vorhandene opus_deform.json erneut anwenden)
"""
import json, os, sys, time, re

WORDS_PATH = "bibles/eng/web/train/words.json"
MAP_PATH = "opus_deform.json"
MODEL = "claude-opus-4-8"
CHUNK = 120
FORMS = ["sg", "pl", "inf", "pres", "past", "part", "base"]

SYSTEM = (
    "Du bist ein Englisch→Deutsch-Lexikograf für einen Bibel-Vokabeltrainer. "
    "Für jedes Item bekommst du: das englische LEMMA (\"en\"), die konkrete WORTFORM im Satz "
    "(\"word\"), den Satz (\"sentence\") und die Wortart (\"pos\"). Liefere drei Felder:\n"
    "  \"de\"     = die deutsche GRUNDFORM (Wörterbuch-Lemma) des englischen Lemmas: Substantive "
    "im Nominativ Singular, Verben im Infinitiv, Adjektive/Adverbien in der Grundform.\n"
    "  \"deForm\" = dieselbe Bedeutung, aber an die WORTFORM im Satz angepasst — Substantive im "
    "Numerus (Singular/Plural) der englischen Form, Verben im Tempus/der Form der englischen "
    "Form (z.B. came→\"kam\", men→\"Männer\", showed→\"zeigte\"). Wenn die Wortform der Grundform "
    "entspricht, ist deForm gleich de.\n"
    "  \"form\"   = genau einer dieser Tags, passend zur WORTFORM: für Substantive \"sg\" oder "
    "\"pl\"; für Verben \"inf\", \"pres\" (Präsens), \"past\" (Vergangenheit) oder \"part\" "
    "(Partizip); für alles andere \"base\".\n"
    "Beide Übersetzungen sind einzelne deutsche Wörter/Wendungen ohne Satzzeichen, ohne "
    "nachgestellten Bindestrich. Antworte mit NUR einem JSON-Array von Objekten "
    "{\"id\": <int>, \"de\": <str>, \"deForm\": <str>, \"form\": <tag>}, ohne Prosa, ohne Markdown."
)


def load_env():
    if not os.environ.get("ANTHROPIC_API_KEY") and os.path.exists(".env"):
        for line in open(".env"):
            if line.strip().startswith("ANTHROPIC_API_KEY"):
                os.environ["ANTHROPIC_API_KEY"] = line.split("=", 1)[1].strip().strip('"').strip("'")


def build_items():
    """Ein Item pro Wort-Eintrag (en ist eindeutig)."""
    words = json.load(open(WORDS_PATH))
    items = []
    for arr in words.values():
        for e in arr:
            sent = e.get("text", "").replace("___", e.get("answer", e["en"]))
            items.append({"en": e["en"], "word": e.get("answer", e["en"]),
                          "sentence": sent, "pos": e.get("pos", "")})
    return items


def parse_json_array(text):
    text = re.sub(r"^```(?:json)?\s*", "", text.strip())
    text = re.sub(r"\s*```$", "", text)
    return json.loads(text[text.find("["):text.rfind("]") + 1])


def chunks_of(items):
    return [items[i:i + CHUNK] for i in range(0, len(items), CHUNK)]


def collect(client, batch_id, chunks):
    out = {}
    for result in client.messages.batches.results(batch_id):
        if result.result.type != "succeeded":
            print(f"  !! {result.custom_id}: {result.result.type}", flush=True)
            continue
        ci = int(result.custom_id.split("-")[1])
        chunk = chunks[ci]
        txt = next((b.text for b in result.result.message.content if b.type == "text"), "")
        try:
            arr = parse_json_array(txt)
        except Exception as ex:
            print(f"  !! parse fail {result.custom_id}: {ex}", flush=True)
            continue
        for o in arr:
            idx = o.get("id")
            if idx is None or idx >= len(chunk):
                continue
            form = o.get("form") if o.get("form") in FORMS else "base"
            out[chunk[idx]["en"]] = {"de": o.get("de"), "deForm": o.get("deForm"), "form": form}
    return out


def poll(client, batch_id):
    while True:
        b = client.messages.batches.retrieve(batch_id)
        if b.processing_status == "ended":
            break
        c = b.request_counts
        print(f"  {b.processing_status}: processing={c.processing} succeeded={c.succeeded} errored={c.errored}", flush=True)
        time.sleep(20)
    print(f"ended: succeeded={b.request_counts.succeeded} errored={b.request_counts.errored}", flush=True)


def apply_map(m):
    words = json.load(open(WORDS_PATH))
    miss = 0
    for arr in words.values():
        for e in arr:
            r = m.get(e["en"])
            if r and r.get("de") and r.get("deForm"):
                e["de"] = r["de"].strip()
                e["deForm"] = r["deForm"].strip()
                e["form"] = r.get("form", "base")
            else:
                e["deForm"] = e["de"]
                e["form"] = "base"
                miss += 1
    json.dump(words, open(WORDS_PATH, "w"), ensure_ascii=False, separators=(",", ":"))
    print(f"wrote de/deForm/form to words.json; missing (fell back to lemma): {miss}")


def main():
    load_env()
    import anthropic
    from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
    from anthropic.types.messages.batch_create_params import Request
    client = anthropic.Anthropic()

    if "--write" in sys.argv:
        apply_map(json.load(open(MAP_PATH)))
        return

    items = build_items()
    chunks = chunks_of(items)

    if "--resume" in sys.argv:
        batch_id = sys.argv[sys.argv.index("--resume") + 1]
        poll(client, batch_id)
        m = collect(client, batch_id, chunks)
        json.dump(m, open(MAP_PATH, "w"), ensure_ascii=False, indent=1)
        print(f"got {len(m)}/{len(items)} -> {MAP_PATH}")
        apply_map(m)
        return

    print(f"{len(items)} Wörter in {len(chunks)} Requests")
    requests = []
    for ci, chunk in enumerate(chunks):
        payload = [{"id": i, "en": it["en"], "word": it["word"],
                    "sentence": it["sentence"], "pos": it["pos"]} for i, it in enumerate(chunk)]
        requests.append(Request(
            custom_id=f"chunk-{ci}",
            params=MessageCreateParamsNonStreaming(
                model=MODEL, max_tokens=16000, system=SYSTEM,
                messages=[{"role": "user", "content": "Items:\n" + json.dumps(payload, ensure_ascii=False)}],
            ),
        ))
    batch = client.messages.batches.create(requests=requests)
    print(f"batch {batch.id} submitted, status {batch.processing_status}")
    print(f"→ Fortsetzen mit: python3 generate_deform.py --resume {batch.id}")
    poll(client, batch.id)
    m = collect(client, batch.id, chunks)
    json.dump(m, open(MAP_PATH, "w"), ensure_ascii=False, indent=1)
    print(f"got {len(m)}/{len(items)} -> {MAP_PATH}")
    apply_map(m)


if __name__ == "__main__":
    main()
