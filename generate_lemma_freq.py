#!/usr/bin/env python3
"""Lemma-Häufigkeit je Edition: bibles/<ed>/train/lemma_freq.json

Zählt für jede annotierte Edition, wie oft jedes Lemma in der ganzen Bibel
vorkommt (jede Annotation zählt, auch Mehrwortausdrücke und ihre Teilwörter).
Die App zeigt daraus „in der Bibel: N ×"; die Zahl fürs aktuelle Buch rechnet
sie zur Laufzeit aus den geladenen Buch-Annotationen (dieselbe Zählregel,
siehe countBookLemmas in index.html).

Aufruf: python3 generate_lemma_freq.py            # alle Editionen
        python3 generate_lemma_freq.py spa/rv1909mod
"""
import json, os, sys
from collections import Counter

ROOT = os.path.dirname(os.path.abspath(__file__))
EDITIONS = ['eng/web', 'spa/rv1909mod', 'deu/l1912mod', 'fra/lsg1910mod']

def build(ed):
    anno_dir = os.path.join(ROOT, 'bibles', ed, 'anno')
    if not os.path.isdir(anno_dir):
        print(f'{ed}: kein anno/ – übersprungen'); return
    cnt = Counter()
    files = sorted(f for f in os.listdir(anno_dir) if f.endswith('.json'))
    for f in files:
        with open(os.path.join(anno_dir, f), encoding='utf-8') as fh:
            data = json.load(fh)
        for verses in (data.get('chapters') or {}).values():
            for anns in (verses or {}).values():
                for a in anns or []:
                    if a.get('lemma'):
                        cnt[a['lemma']] += 1
    out_dir = os.path.join(ROOT, 'bibles', ed, 'train')
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, 'lemma_freq.json')
    with open(out, 'w', encoding='utf-8') as fh:
        json.dump(dict(sorted(cnt.items(), key=lambda kv: -kv[1])), fh, ensure_ascii=False, separators=(',', ':'))
    print(f'{ed}: {len(files)} Bücher, {len(cnt)} Lemmata → {out} ({os.path.getsize(out)//1024} KB)')

if __name__ == '__main__':
    for ed in (sys.argv[1:] or EDITIONS):
        build(ed)
