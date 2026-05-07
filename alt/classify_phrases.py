#!/usr/bin/env python3
"""Classify phrase CEFR levels using Claude API."""

import json, os, sys, urllib.request

API_URL = "https://api.anthropic.com/v1/messages"
MODEL = "claude-sonnet-4-20250514"
API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

if not API_KEY:
    print("\n  No API key! → export ANTHROPIC_API_KEY='sk-ant-...'\n")
    sys.exit(1)

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "phrase_levels.json")

sys.path.insert(0, BASE)
from merge_phrases import PHRASES

# Collect unique phrases
seen = set()
unique = []
for phrase, de, level in PHRASES:
    key = phrase.lower()
    if key not in seen:
        seen.add(key)
        unique.append({"phrase": phrase, "de": de, "current_level": level})

print(f"Classifying {len(unique)} phrases via API...")

phrase_list = "\n".join(f"{i+1}. {p['phrase']} (= {p['de']})" for i, p in enumerate(unique))

prompt = f"""Classify each English phrase/expression by CEFR level (A1, A2, B1, B2, C1, C2).

The CEFR level should reflect how difficult the PHRASE AS A WHOLE is for a learner of English.
Consider:
- A phrase like "give birth to" uses simple words but the expression itself is B1
- Phrasal verbs (set apart, cast out) are typically B1-B2
- Biblical/formal expressions (burnt offering, ark of the covenant) are C1-C2
- Simple combinations (sit down, get up) are A2
- Common conjunctions/prepositions (because of, so that) are A2-B1

Return ONLY a JSON array of objects with "phrase" and "level" fields.
No explanation, no markdown, just the JSON array.

Phrases to classify:
{phrase_list}"""

body = json.dumps({
    "model": MODEL,
    "max_tokens": 8000,
    "messages": [{"role": "user", "content": prompt}]
}).encode()

req = urllib.request.Request(API_URL, data=body, headers={
    "Content-Type": "application/json",
    "x-api-key": API_KEY,
    "anthropic-version": "2023-06-01"
})

print("Sending request...")
with urllib.request.urlopen(req) as resp:
    result = json.loads(resp.read())

text = result["content"][0]["text"].strip()
# Extract JSON from response
if text.startswith("```"):
    text = text.split("```")[1]
    if text.startswith("json"):
        text = text[4:]
classifications = json.loads(text)

# Build lookup
level_map = {}
for c in classifications:
    level_map[c["phrase"].lower()] = c["level"]

print(f"Got {len(level_map)} classifications")

# Show changes
changes = 0
for p in unique:
    new_level = level_map.get(p["phrase"].lower())
    if new_level and new_level != p["current_level"]:
        print(f"  {p['phrase']:30s} {p['current_level']} → {new_level}")
        changes += 1

print(f"\n{changes} level changes out of {len(unique)} phrases")

# Save
with open(OUT, "w") as f:
    json.dump(level_map, f, ensure_ascii=False, indent=2)
print(f"Saved to {OUT}")
