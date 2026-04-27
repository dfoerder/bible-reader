#!/usr/bin/env python3
"""Extract all unique vocab pairs from Bible annotations, grouped by CEFR level."""

import json, os, re

ANNO_DIR = os.path.join(os.path.dirname(__file__), '..', 'bibles', 'eng', 'web', 'anno')
OUT_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'vocab_pool.json')

SKIP_EN = {
    'the','a','an','of','to','in','and','but','or','for','is','are','was','were','be','been','am',
    'has','have','had','do','does','did','not','no','so','as','at','by','on','if','it','he','she',
    'we','they','me','my','his','her','its','our','your','their','this','that','these','those',
    'who','which','what','with','from','into','will','shall','would','should','can','could','may',
    'might','than','then','when','where','how','all','also','very','much','more','most','some',
    'any','each','every','both','own','other','such','only','just','even','still','up','out',
    'about','over','after','before','between','through','under','again','further','there','here',
    'him','them','us','you','whom','whose','let','said','says','say','came','come','comes',
    'went','go','goes','got','get','put','take','took','taken','make','made','give','gave','given',
    'now','yet','too','well','back','down','off','upon','being','having','doing','going',
    'because','while','until','since','though','already','away','near','thing','things',
    'one','two','many','few','new','old','great','good','long','little','first','last',
    'same','another','next','called','became','left','set','told','asked','brought',
    'saw','see','seen','knew','know','known','thought','think','found','find','began','kept',
    'keep','stood','stand','sent','send','heard','hear','fell','fall','held','hold','ran','run',
    'read','wrote','write','sat','sit','lay','lie','spoke','speak','met','meet','paid','pay',
    'cut','led','lead','lost','lose','won','win','felt','feel','grew','grow','drew','draw',
    'wore','wear','broke','break','drove','drive','ate','eat','threw','throw','built','build',
    'must','need','dare','like','just','right','way','time','part','end',
    'according','saying','among',
}

SKIP_DE = {
    'und','der','die','das','den','dem','des','ein','eine','einen','einem','einer','zu','auf',
    'in','an','mit','von','für','ist','sind','war','hat','er','sie','es','ich','wir','ihr',
    'du','nicht','auch','aber','oder','als','so','wie','aus','nach','über','vor','bis',
    'wenn','da','noch','schon','denn','um','am','im','zum','zur','vom','beim','dass',
    'wird','wurde','haben','sein','werden','kann','soll','muss','darf','will',
    'sich','ihm','ihn','uns','euch','mich','dich','dir','mir',
    'doch','nun','hier','dort','dann','hin','her',
}

# Collect all (en_lower, de) pairs with counts, keyed by (lemma_lower, level)
raw = {}

for book_num in range(1, 67):
    path = os.path.join(ANNO_DIR, f'{book_num}_web_deu.json')
    if not os.path.exists(path):
        continue
    data = json.load(open(path, encoding='utf-8'))
    for ch_num, ch in data['chapters'].items():
        for v_num, annotations in ch.items():
            for anno in annotations:
                form = anno.get('form', '')
                lemma = anno.get('lemma', '')
                de = anno.get('de', '')
                level = anno.get('level', '')
                if not form or not de or not level:
                    continue
                if len(form) < 3 or len(de) < 2:
                    continue
                if "'" in form or "'" in form:
                    continue
                if ' ' in de:
                    continue
                if form.lower() in SKIP_EN or de.lower() in SKIP_DE:
                    continue
                if form[0].isupper() and anno.get('pos', 0) > 0:
                    continue

                key = (lemma.lower(), level)
                if key not in raw:
                    raw[key] = {}
                pair = (form, de)
                raw[key][pair] = raw[key].get(pair, 0) + 1

# For each lemma+level, pick the most frequent (en, de) pair
vocab = {}
for (lemma, level), pairs in raw.items():
    best_pair = max(pairs, key=pairs.get)
    en, de = best_pair
    count = pairs[best_pair]
    # Deduplicate by en_lower within each level
    dedup_key = (en.lower(), level)
    if dedup_key not in vocab or vocab[dedup_key]['count'] < count:
        vocab[dedup_key] = {'en': en, 'de': de, 'level': level, 'count': count}

# Check for ambiguity: same en word mapping to different de words within same level
en_to_de = {}
for key, v in vocab.items():
    lvl_key = (v['en'].lower(), v['level'])
    if lvl_key not in en_to_de:
        en_to_de[lvl_key] = []
    en_to_de[lvl_key].append(v)

# Group by level, sort by frequency
by_level = {}
for key, v in vocab.items():
    lvl = v['level']
    if lvl not in by_level:
        by_level[lvl] = []
    by_level[lvl].append(v)

for lvl in by_level:
    by_level[lvl].sort(key=lambda w: -w['count'])

# Also deduplicate: same de word within same level (keep highest count)
for lvl in by_level:
    seen_de = {}
    deduped = []
    for w in by_level[lvl]:
        if w['de'] not in seen_de:
            seen_de[w['de']] = True
            deduped.append(w)
    by_level[lvl] = deduped

out = {}
for lvl in ['A1', 'A2', 'B1', 'B2', 'C1']:
    words = by_level.get(lvl, [])
    n = len(words)
    t1 = n // 3
    t2 = 2 * n // 3
    for i, w in enumerate(words):
        w['sub'] = 1 if i < t1 else (2 if i < t2 else 3)
    out[lvl] = [{'en': w['en'], 'de': w['de'], 'sub': w['sub']} for w in words]
    print(f"{lvl}: {n} words  ({t1} / {t2-t1} / {n-t2})")

os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
with open(OUT_PATH, 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False)

total = sum(len(v) for v in out.values())
print(f"\nTotal: {total} word pairs")
print(f"Saved to {OUT_PATH}")
sz = os.path.getsize(OUT_PATH)
print(f"File size: {sz/1024:.1f} KB")
