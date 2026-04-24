#!/usr/bin/env python3
"""Download French Louis Segond 1910 Bible from BibleCorps USFM and convert to JSON."""

import json, os, re, ssl, urllib.request

BASE = 'https://raw.githubusercontent.com/BibleCorps/FRA-B-LSG1910-PD-UBS/main/p.sfm/'
PREFIX = 'FRA[B]LSG1910[PD]UBS-'
OUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'bibles', 'fra', 'lsg1910')

# BibleCorps file numbering → standard book number (1-66) and French name
BOOKS = [
    (1,  '01', 'GEN', 'Genèse'),
    (2,  '02', 'EXO', 'Exode'),
    (3,  '03', 'LEV', 'Lévitique'),
    (4,  '04', 'NUM', 'Nombres'),
    (5,  '05', 'DEU', 'Deutéronome'),
    (6,  '06', 'JOS', 'Josué'),
    (7,  '07', 'JDG', 'Juges'),
    (8,  '08', 'RUT', 'Ruth'),
    (9,  '09', '1SA', '1 Samuel'),
    (10, '10', '2SA', '2 Samuel'),
    (11, '11', '1KI', '1 Rois'),
    (12, '12', '2KI', '2 Rois'),
    (13, '13', '1CH', '1 Chroniques'),
    (14, '14', '2CH', '2 Chroniques'),
    (15, '15', 'EZR', 'Esdras'),
    (16, '16', 'NEH', 'Néhémie'),
    (17, '17', 'EST', 'Esther'),
    (18, '18', 'JOB', 'Job'),
    (19, '19', 'PSA', 'Psaumes'),
    (20, '20', 'PRO', 'Proverbes'),
    (21, '21', 'ECC', 'Ecclésiaste'),
    (22, '22', 'SNG', 'Cantique des Cantiques'),
    (23, '23', 'ISA', 'Ésaïe'),
    (24, '24', 'JER', 'Jérémie'),
    (25, '25', 'LAM', 'Lamentations'),
    (26, '26', 'EZK', 'Ézéchiel'),
    (27, '27', 'DAN', 'Daniel'),
    (28, '28', 'HOS', 'Osée'),
    (29, '29', 'JOL', 'Joël'),
    (30, '30', 'AMO', 'Amos'),
    (31, '31', 'OBA', 'Abdias'),
    (32, '32', 'JON', 'Jonas'),
    (33, '33', 'MIC', 'Michée'),
    (34, '34', 'NAM', 'Nahum'),
    (35, '35', 'HAB', 'Habacuc'),
    (36, '36', 'ZEP', 'Sophonie'),
    (37, '37', 'HAG', 'Aggée'),
    (38, '38', 'ZEC', 'Zacharie'),
    (39, '39', 'MAL', 'Malachie'),
    # 40 = INT (introduction), skip
    (40, '41', 'MAT', 'Matthieu'),
    (41, '42', 'MRK', 'Marc'),
    (42, '43', 'LUK', 'Luc'),
    (43, '44', 'JHN', 'Jean'),
    (44, '45', 'ACT', 'Actes'),
    (45, '46', 'ROM', 'Romains'),
    (46, '47', '1CO', '1 Corinthiens'),
    (47, '48', '2CO', '2 Corinthiens'),
    (48, '49', 'GAL', 'Galates'),
    (49, '50', 'EPH', 'Éphésiens'),
    (50, '51', 'PHP', 'Philippiens'),
    (51, '52', 'COL', 'Colossiens'),
    (52, '53', '1TH', '1 Thessaloniciens'),
    (53, '54', '2TH', '2 Thessaloniciens'),
    (54, '55', '1TI', '1 Timothée'),
    (55, '56', '2TI', '2 Timothée'),
    (56, '57', 'TIT', 'Tite'),
    (57, '58', 'PHM', 'Philémon'),
    (58, '59', 'HEB', 'Hébreux'),
    (59, '60', 'JAS', 'Jacques'),
    (60, '61', '1PE', '1 Pierre'),
    (61, '62', '2PE', '2 Pierre'),
    (62, '63', '1JN', '1 Jean'),
    (63, '64', '2JN', '2 Jean'),
    (64, '65', '3JN', '3 Jean'),
    (65, '66', 'JUD', 'Jude'),
    (66, '67', 'REV', 'Apocalypse'),
]

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

os.makedirs(OUT_DIR, exist_ok=True)

def parse_usfm(text):
    text = re.sub(r'\\x .*?\\x\*', '', text)
    text = re.sub(r'\\f .*?\\f\*', '', text)

    chapters = {}
    current_ch = None

    for line in text.split('\n'):
        line = line.strip()
        if not line:
            continue

        m = re.match(r'\\c\s+(\d+)', line)
        if m:
            current_ch = m.group(1)
            chapters[current_ch] = {}
            continue

        if current_ch is None:
            continue

        if line.startswith(('\\s', '\\r', '\\p', '\\ms', '\\mr', '\\ip', '\\imt', '\\ie', '\\d', '\\q', '\\b', '\\nb', '\\mi', '\\pi', '\\li')):
            vcheck = re.match(r'\\[a-z]+\d?\s+\\v\s+(\d+)\s+(.*)', line)
            if vcheck:
                vnum = vcheck.group(1)
                vtxt = vcheck.group(2)
                vtxt = re.sub(r'\\[a-z]+\d?\s*', '', vtxt).strip()
                if vtxt:
                    chapters[current_ch][vnum] = vtxt
            continue

        m = re.match(r'\\v\s+(\d+)\s+(.*)', line)
        if m:
            vnum = m.group(1)
            vtxt = m.group(2)
            vtxt = re.sub(r'\\[a-z]+\d?\s*', '', vtxt).strip()
            if vtxt:
                chapters[current_ch][vnum] = vtxt
            continue

    return chapters


for book_num, file_num, code, name in BOOKS:
    fname = f'{PREFIX}{file_num}-{code}.p.sfm'
    url = BASE + urllib.request.quote(fname, safe='')
    print(f'  {book_num:2d}/{66} {name}...', end=' ', flush=True)

    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, context=ctx) as resp:
            raw = resp.read().decode('utf-8')
    except Exception as e:
        print(f'FEHLER: {e}')
        continue

    chapters = parse_usfm(raw)
    if not chapters:
        print('keine Kapitel gefunden!')
        continue

    data = {'name': name, 'chapters': chapters}
    out_path = os.path.join(OUT_DIR, f'{book_num}_lsg1910.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)

    total_v = sum(len(v) for v in chapters.values())
    print(f'{len(chapters)} Kapitel, {total_v} Verse')

print('\nFertig!')
