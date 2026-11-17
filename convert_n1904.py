"""MACULA Greek Nestle1904 TSV -> bible-reader format (bibles/grc/n1904/)."""
import csv, json, os, sys, unicodedata
src, out = sys.argv[1], sys.argv[2]
NAMES = {40:'ΚΑΤΑ ΜΑΘΘΑΙΟΝ',41:'ΚΑΤΑ ΜΑΡΚΟΝ',42:'ΚΑΤΑ ΛΟΥΚΑΝ',43:'ΚΑΤΑ ΙΩΑΝΗΝ',44:'ΠΡΑΞΕΙΣ ΑΠΟΣΤΟΛΩΝ',
 45:'ΠΡΟΣ ΡΩΜΑΙΟΥΣ',46:'ΠΡΟΣ ΚΟΡΙΝΘΙΟΥΣ Α',47:'ΠΡΟΣ ΚΟΡΙΝΘΙΟΥΣ Β',48:'ΠΡΟΣ ΓΑΛΑΤΑΣ',49:'ΠΡΟΣ ΕΦΕΣΙΟΥΣ',
 50:'ΠΡΟΣ ΦΙΛΙΠΠΗΣΙΟΥΣ',51:'ΠΡΟΣ ΚΟΛΟΣΣΑΕΙΣ',52:'ΠΡΟΣ ΘΕΣΣΑΛΟΝΙΚΕΙΣ Α',53:'ΠΡΟΣ ΘΕΣΣΑΛΟΝΙΚΕΙΣ Β',
 54:'ΠΡΟΣ ΤΙΜΟΘΕΟΝ Α',55:'ΠΡΟΣ ΤΙΜΟΘΕΟΝ Β',56:'ΠΡΟΣ ΤΙΤΟΝ',57:'ΠΡΟΣ ΦΙΛΗΜΟΝΑ',58:'ΠΡΟΣ ΕΒΡΑΙΟΥΣ',
 59:'ΙΑΚΩΒΟΥ',60:'ΠΕΤΡΟΥ Α',61:'ΠΕΤΡΟΥ Β',62:'ΙΩΑΝΝΟΥ Α',63:'ΙΩΑΝΝΟΥ Β',64:'ΙΩΑΝΝΟΥ Γ',65:'ΙΟΥΔΑ',66:'ΑΠΟΚΑΛΥΨΙΣ ΙΩΑΝΝΟΥ'}
nfc = lambda s: unicodedata.normalize('NFC', s or '')
text, anno = {}, {}
with open(src, encoding='utf-8') as f:
    for r in csv.DictReader(f, delimiter='\t', quoting=csv.QUOTE_NONE):
        i = r['xml:id']  # nBBCCCVVVWWW
        b, c, v = int(i[1:3]), str(int(i[3:6])), str(int(i[6:9]))
        vt = text.setdefault(b, {}).setdefault(c, {})
        a = r['after'] or ''
        vt[v] = vt.get(v, '') + nfc(r['text']) + (a if a[-1:].isspace() else a + ' ')
        va = anno.setdefault(b, {}).setdefault(c, {}).setdefault(v, [])
        e = {'pos': len(va), 'form': nfc(r['text']), 'lemma': nfc(r['lemma']), 'en': (r['gloss'] or '').strip(),
             'strong': 'G' + r['strong'] if r['strong'] else '', 'morph': r['morph']}
        va.append({k: x for k, x in e.items() if x != ''} | {'pos': e['pos']})
os.makedirs(f'{out}/anno', exist_ok=True)
for b in sorted(text):
    for ch in text[b].values():
        for k in ch: ch[k] = ' '.join(ch[k].split())
    json.dump({'name': NAMES[b], 'chapters': text[b]}, open(f'{out}/{b}_n1904.json', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    json.dump({'name': NAMES[b], 'chapters': anno[b]}, open(f'{out}/anno/{b}_n1904_multi.json', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print(len(text), 'Bücher')
