#!/usr/bin/env python3
"""Resume an already-submitted POS batch: poll (with retry), collect, write pos."""
import json, time, sys
import generate_pos as g

BATCH_ID = sys.argv[1] if len(sys.argv) > 1 else "msgbatch_01Rck8fJxatZ1JHpn2uWv9Jw"


def retry(fn, tries=10, delay=15):
    import anthropic
    for attempt in range(tries):
        try:
            return fn()
        except (anthropic.APIConnectionError, anthropic.InternalServerError) as ex:
            print(f"  (transient {type(ex).__name__}; retry {attempt+1}/{tries} in {delay}s)", flush=True)
            time.sleep(delay)
    return fn()


def main():
    g.load_env()
    import anthropic
    client = anthropic.Anthropic()
    items = g.build_items()
    chunks = [items[i:i + g.CHUNK] for i in range(0, len(items), g.CHUNK)]

    while True:
        b = retry(lambda: client.messages.batches.retrieve(BATCH_ID))
        if b.processing_status == "ended":
            break
        c = b.request_counts
        print(f"  {b.processing_status}: processing={c.processing} succeeded={c.succeeded} errored={c.errored}", flush=True)
        time.sleep(20)
    print(f"ended: succeeded={b.request_counts.succeeded} errored={b.request_counts.errored}", flush=True)

    pos_map = {}
    for result in retry(lambda: list(client.messages.batches.results(BATCH_ID))):
        if result.result.type != "succeeded":
            print(f"  !! {result.custom_id}: {result.result.type}", flush=True)
            continue
        ci = int(result.custom_id.split("-")[1])
        chunk = chunks[ci]
        txt = next((bl.text for bl in result.result.message.content if bl.type == "text"), "")
        try:
            arr = g.parse_json_array(txt)
        except Exception as ex:
            print(f"  !! parse fail {result.custom_id}: {ex}", flush=True)
            continue
        for obj in arr:
            idx, pos = obj.get("id"), obj.get("pos")
            if idx is None or idx >= len(chunk) or pos not in g.POS_TAGS:
                continue
            pos_map[chunk[idx]["lemma"]] = pos

    json.dump(pos_map, open(g.MAP_PATH, "w"), ensure_ascii=False, indent=1)
    print(f"got {len(pos_map)}/{len(items)} pos tags -> {g.MAP_PATH}", flush=True)
    g.apply_map(pos_map)


if __name__ == "__main__":
    main()
