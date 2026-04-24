#!/usr/bin/env python3
"""Download Spanish Reina-Valera 1909 from getBible API and convert to JSON."""

import json, os, ssl, time, urllib.request

BASE = 'https://api.getbible.net/v2/valera/'
OUT = os.path.join(os.path.dirname(__file__), '..', 'bibles', 'spa', 'rv1909')
os.makedirs(OUT, exist_ok=True)

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

SPANISH_NAMES = {
    1: 'Génesis', 2: 'Éxodo', 3: 'Levítico', 4: 'Números', 5: 'Deuteronomio',
    6: 'Josué', 7: 'Jueces', 8: 'Rut', 9: '1 Samuel', 10: '2 Samuel',
    11: '1 Reyes', 12: '2 Reyes', 13: '1 Crónicas', 14: '2 Crónicas',
    15: 'Esdras', 16: 'Nehemías', 17: 'Ester', 18: 'Job', 19: 'Salmos',
    20: 'Proverbios', 21: 'Eclesiastés', 22: 'Cantares', 23: 'Isaías',
    24: 'Jeremías', 25: 'Lamentaciones', 26: 'Ezequiel', 27: 'Daniel',
    28: 'Oseas', 29: 'Joel', 30: 'Amós', 31: 'Abdías', 32: 'Jonás',
    33: 'Miqueas', 34: 'Nahúm', 35: 'Habacuc', 36: 'Sofonías',
    37: 'Hageo', 38: 'Zacarías', 39: 'Malaquías',
    40: 'Mateo', 41: 'Marcos', 42: 'Lucas', 43: 'Juan', 44: 'Hechos',
    45: 'Romanos', 46: '1 Corintios', 47: '2 Corintios', 48: 'Gálatas',
    49: 'Efesios', 50: 'Filipenses', 51: 'Colosenses',
    52: '1 Tesalonicenses', 53: '2 Tesalonicenses',
    54: '1 Timoteo', 55: '2 Timoteo', 56: 'Tito', 57: 'Filemón',
    58: 'Hebreos', 59: 'Santiago', 60: '1 Pedro', 61: '2 Pedro',
    62: '1 Juan', 63: '2 Juan', 64: '3 Juan', 65: 'Judas', 66: 'Apocalipsis',
}

for book_num in range(1, 67):
    name = SPANISH_NAMES[book_num]
    url = f'{BASE}{book_num}.json'
    print(f'  {book_num:2d}/66 {name}...', end=' ', flush=True)

    try:
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0')
        with urllib.request.urlopen(req, context=ctx, timeout=30) as resp:
            data = json.loads(resp.read())
    except Exception as e:
        print(f'FEHLER: {e}')
        continue

    chapters = {}
    for ch_data in data.get('chapters', []):
        ch_num = str(ch_data['chapter'])
        verses = {}
        for v_data in ch_data.get('verses', []):
            verses[str(v_data['verse'])] = v_data['text'].strip()
        chapters[ch_num] = verses

    out_data = {'name': name, 'chapters': chapters}
    out_path = os.path.join(OUT, f'{book_num}_rv1909.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(out_data, f, ensure_ascii=False)

    total_v = sum(len(v) for v in chapters.values())
    print(f'{len(chapters)} Kapitel, {total_v} Verse')

    time.sleep(0.3)

print('\nFertig!')
