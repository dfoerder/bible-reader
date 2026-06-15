#!/usr/bin/env python3
"""Assign CEFR levels to Bible words using Claude Opus 4.7."""

import json
import sys
import anthropic

BATCH_SIZE = 200
MODEL = "claude-opus-4-7"

with open("/tmp/bible_words_for_cefr.json") as f:
    words = json.load(f)

print(f"Total words: {len(words)}")

client = anthropic.Anthropic()
results = {}
batches = [words[i:i+BATCH_SIZE] for i in range(0, len(words), BATCH_SIZE)]

for i, batch in enumerate(batches):
    print(f"Batch {i+1}/{len(batches)} ({len(batch)} words)...", end=" ", flush=True)

    prompt = f"""Assign a CEFR level (A1, A2, B1, B2, C1, or C2) to each English word below.
Base your assessment on general English proficiency — how common the word is in everyday English, not in any specific domain.

Words:
{json.dumps(batch)}

Return ONLY a JSON object mapping each word to its CEFR level, like:
{{"word1": "B1", "word2": "C1", ...}}

No explanation, no markdown, just the JSON object."""

    response = client.messages.create(
        model=MODEL,
        max_tokens=8192,
        messages=[{"role": "user", "content": prompt}]
    )

    text = response.content[0].text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()

    batch_results = json.loads(text)
    results.update(batch_results)
    print(f"OK ({len(batch_results)} assigned)")

    missing = [w for w in batch if w not in batch_results]
    if missing:
        print(f"  WARNING: {len(missing)} words missing: {missing[:5]}")

print(f"\nTotal assigned: {len(results)}")

with open("opus_cefr_levels.json", "w") as f:
    json.dump(results, f, indent=2)

print("Written: opus_cefr_levels.json")

# Show distribution
from collections import Counter
dist = Counter(results.values())
for lvl in ["A1", "A2", "B1", "B2", "C1", "C2"]:
    print(f"  {lvl}: {dist.get(lvl, 0)}")
