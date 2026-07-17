#!/usr/bin/env python3
"""Generate part-of-speech (POS) tags for every cloze lemma via the Opus Batch API.

Approach A (bundled): ~150 words per request, one batch job, 50% Batch-API discount.
Writes a `pos` field into bibles/eng/web/train/words.json and saves the raw map to
opus_pos_levels.json.

Run:  python3 generate_pos.py          (submit + poll + write, ~minutes)
      python3 generate_pos.py --write  (only re-apply an existing opus_pos_levels.json)
"""
import json, os, sys, time, re

WORDS_PATH = "bibles/eng/web/train/words.json"
MAP_PATH = "opus_pos_levels.json"
MODEL = "claude-opus-4-8"
CHUNK = 150
POS_TAGS = ["noun", "verb", "adj", "adv", "pron", "prep", "conj", "det", "num", "intj", "other"]

SYSTEM = (
    "You are a linguistic annotator. For each item, identify the part of speech of the "
    "TARGET English word (field \"word\") as it is used in the given sentence. "
    "Choose exactly one tag from this set: " + ", ".join(POS_TAGS) + ". "
    "Use 'det' for articles and determiners, 'intj' for interjections, 'other' only if "
    "nothing else fits. Respond with ONLY a JSON array of objects {\"id\": <int>, \"pos\": <tag>}, "
    "no prose, no markdown fences."
)


def load_env():
    if not os.environ.get("ANTHROPIC_API_KEY") and os.path.exists(".env"):
        for line in open(".env"):
            line = line.strip()
            if line.startswith("ANTHROPIC_API_KEY"):
                os.environ["ANTHROPIC_API_KEY"] = line.split("=", 1)[1].strip().strip('"').strip("'")


def build_items():
    """One item per unique word, with a filled-in context sentence."""
    words = json.load(open(WORDS_PATH))
    items, seen = [], {}
    for lvl, arr in words.items():
        for e in arr:
            lem = e["en"]
            if lem in seen:
                continue
            seen[lem] = True
            sent = e.get("text", "").replace("___", e.get("answer", lem))
            items.append({"lemma": lem, "word": lem, "sentence": sent})
    return items


def parse_json_array(text):
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    start = text.find("[")
    end = text.rfind("]")
    if start == -1 or end == -1:
        raise ValueError("no JSON array found")
    return json.loads(text[start:end + 1])


def submit_and_poll(items):
    import anthropic
    from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
    from anthropic.types.messages.batch_create_params import Request
    client = anthropic.Anthropic()

    chunks = [items[i:i + CHUNK] for i in range(0, len(items), CHUNK)]
    print(f"{len(items)} lemmas in {len(chunks)} requests of up to {CHUNK}")

    requests = []
    for ci, chunk in enumerate(chunks):
        payload = [{"id": i, "word": it["word"], "sentence": it["sentence"]} for i, it in enumerate(chunk)]
        requests.append(Request(
            custom_id=f"chunk-{ci}",
            params=MessageCreateParamsNonStreaming(
                model=MODEL,
                max_tokens=8000,
                system=SYSTEM,
                messages=[{"role": "user", "content": "Items:\n" + json.dumps(payload, ensure_ascii=False)}],
            ),
        ))

    batch = client.messages.batches.create(requests=requests)
    print(f"batch {batch.id} submitted, status {batch.processing_status}")
    while True:
        b = client.messages.batches.retrieve(batch.id)
        if b.processing_status == "ended":
            break
        c = b.request_counts
        print(f"  {b.processing_status}: processing={c.processing} succeeded={c.succeeded} errored={c.errored}")
        time.sleep(20)
    print(f"ended: succeeded={b.request_counts.succeeded} errored={b.request_counts.errored}")

    pos_map = {}
    for result in client.messages.batches.results(batch.id):
        if result.result.type != "succeeded":
            print(f"  !! {result.custom_id}: {result.result.type}")
            continue
        ci = int(result.custom_id.split("-")[1])
        chunk = chunks[ci]
        txt = next((b.text for b in result.result.message.content if b.type == "text"), "")
        try:
            arr = parse_json_array(txt)
        except Exception as ex:
            print(f"  !! parse fail {result.custom_id}: {ex}")
            continue
        for obj in arr:
            idx = obj.get("id")
            pos = obj.get("pos")
            if idx is None or idx >= len(chunk) or pos not in POS_TAGS:
                continue
            pos_map[chunk[idx]["lemma"]] = pos
    return pos_map


def apply_map(pos_map):
    words = json.load(open(WORDS_PATH))
    miss = 0
    for arr in words.values():
        for e in arr:
            p = pos_map.get(e["en"])
            if p:
                e["pos"] = p
            else:
                miss += 1
    json.dump(words, open(WORDS_PATH, "w"), ensure_ascii=False, separators=(",", ":"))
    print(f"wrote pos to words.json; missing: {miss}")


def main():
    load_env()
    if "--write" in sys.argv:
        pos_map = json.load(open(MAP_PATH))
        apply_map(pos_map)
        return
    items = build_items()
    pos_map = submit_and_poll(items)
    json.dump(pos_map, open(MAP_PATH, "w"), ensure_ascii=False, indent=1)
    print(f"got {len(pos_map)}/{len(items)} pos tags -> {MAP_PATH}")
    apply_map(pos_map)


if __name__ == "__main__":
    main()
