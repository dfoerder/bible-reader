"""STEPBible TAHOT (Translators Amalgamated Hebrew OT, CC BY 4.0) -> bible-reader format.
Englische Verszählung (wie die anderen Bibeln der App); die hebräische steht im TAHOT in Klammern.
Übernommen werden Wörter des Leningrad-Kodex (Typ L…), Qere-Lesungen (Q…) und die
wiederhergestellten Verse Jos 21,36–37 (R); X/V (Zusätze anderer Handschriften) entfallen.
Psalm-Überschriften (TAHOT Vers 0) werden vorne an Vers 1 gehängt (wie in der Zählung der App).
Die App ordnet Wort-Daten über Leerzeichen zu: darum steht auch nach dem Maqaf (־) ein
Leerzeichen, und Absatz-/Sonderzeichen (פ ס ׆) ohne eigenes Wort entfallen im Lesetext."""
import glob, json, os, re, sys, unicodedata
src, out = sys.argv[1], sys.argv[2]
BOOKS = ['Gen','Exo','Lev','Num','Deu','Jos','Jdg','Rut','1Sa','2Sa','1Ki','2Ki','1Ch','2Ch','Ezr','Neh','Est','Job','Psa','Pro',
         'Ecc','Sng','Isa','Jer','Lam','Ezk','Dan','Hos','Jol','Amo','Oba','Jon','Mic','Nam','Hab','Zep','Hag','Zec','Mal']
NR = {b: i+1 for i, b in enumerate(BOOKS)}
REF = re.compile(r'^([1-3][A-Z][a-z]|[A-Z][a-z][a-z])\.(\d+)\.(\d+)(?:\([^)]*\))?#(\d+)=(\S+)')
nfc = lambda s: unicodedata.normalize('NFC', s)
PUNCT = '־׃׀'          # Maqaf, Sof Pasuq, Paseq
NONWORD = {'פ', 'ס', '׆'}         # Petucha, Setuma, umgekehrtes Nun
text, anno, skipped = {}, {}, {}
for f in sorted(glob.glob(os.path.join(src, 'TAHOT*.txt'))):
    for line in open(f, encoding='utf-8'):
        m = REF.match(line)
        if not m or m.group(1) not in NR: continue
        b, c, v, _, typ = m.groups()
        if typ[0] not in 'LQR':
            skipped[typ] = skipped.get(typ, 0) + 1; continue
        col = line.rstrip('\n').split('\t')
        nr, c, v = NR[b], str(int(c)), str(max(1, int(v)))
        core = re.search(r'\{(H\d+)[A-Z]?\}', col[4]) or re.search(r'(H\d+)', col[4])
        strong = 'H' + str(int(core.group(1)[1:])) if core else ''
        lem = re.search(r'\{H\d+[A-Z]?=([^=]+)=', col[11] if len(col) > 11 else '')
        lemma = nfc(lem.group(1)) if lem else ''
        words, glosses = col[1].split('/ /'), col[3].split('/ /')   # Qere mit zwei Wörtern
        vt = text.setdefault(nr, {}).setdefault(c, {})
        va = anno.setdefault(nr, {}).setdefault(c, {}).setdefault(v, [])
        for k, w in enumerate(words):
            heb = nfc(w.replace('/', '').replace('\\', ' '))
            toks = [x for x in heb.split() if x not in NONWORD]
            heb = ''.join(toks)                     # Satzzeichen (׃ ־ ׀) bleiben am Wort
            form = heb.strip(PUNCT)
            if not form: continue
            vt[v] = (vt[v] + ' ' if v in vt else '') + heb
            g = glosses[k] if k < len(glosses) else glosses[-1]
            e = {'pos': len(va), 'form': form, 'lemma': lemma, 'en': re.sub(r'\s+', ' ', g.replace('/', ' ')).strip(),
                 'strong': strong, 'morph': col[5]}
            va.append({kk: x for kk, x in e.items() if x != '' or kk == 'pos'})
os.makedirs(f'{out}/anno', exist_ok=True)
names = {b['nr']: b['name'] for b in json.load(open(sys.argv[3]))['books']} if len(sys.argv) > 3 else {}
for nr in sorted(text):
    name = names.get(nr, BOOKS[nr-1])
    json.dump({'name': name, 'chapters': text[nr]}, open(f'{out}/{nr}_wlc.json', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    json.dump({'name': name, 'chapters': anno[nr]}, open(f'{out}/anno/{nr}_wlc_multi.json', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print(len(text), 'Bücher; ausgelassen:', skipped)
