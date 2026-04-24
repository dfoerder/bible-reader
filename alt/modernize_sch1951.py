#!/usr/bin/env python3
"""Modernize the German Schlachter 1951 Bible.

Only safe 1:1 replacements: adverbs/conjunctions (no articles),
pronouns with same declension, nouns with same gender.

Dropped: Weib (n→f), Jüngling (→compound), Dirne (f→n),
Kebsweib (n→f), Trübsal (ambiguous gender).
"""

import json, glob, os, re

SRC = os.path.join(os.path.dirname(__file__), '..', 'bibles', 'deu', 'sch1951')
OUT = os.path.join(os.path.dirname(__file__), '..', 'bibles', 'deu', 'sch1951mod')
os.makedirs(OUT, exist_ok=True)


def modernize(text):
    # ================================================================
    # 1. VERBS (no article issues)
    # ================================================================

    # ward → wurde (Präteritum von "werden")
    text = re.sub(r'\bward\b', 'wurde', text)
    text = re.sub(r'\bWard\b', 'Wurde', text)

    # ================================================================
    # 2. ADVERBS / CONJUNCTIONS (no article issues)
    # ================================================================

    text = re.sub(r'\bdaselbst\b', 'dort', text)
    text = re.sub(r'\bDaselbst\b', 'Dort', text)

    text = re.sub(r'\balsbald\b', 'sofort', text)
    text = re.sub(r'\bAlsbald\b', 'Sofort', text)

    text = re.sub(r'\bgleichwie\b', 'so wie', text)
    text = re.sub(r'\bGleichwie\b', 'So wie', text)

    text = re.sub(r'\ballezeit\b', 'jederzeit', text)
    text = re.sub(r'\bAllezeit\b', 'Jederzeit', text)

    text = re.sub(r'\bdesgleichen\b', 'ebenso', text)
    text = re.sub(r'\bDesgleichen\b', 'Ebenso', text)

    text = re.sub(r'\bhinfort\b', 'von nun an', text)
    text = re.sub(r'\bHinfort\b', 'Von nun an', text)

    text = re.sub(r'\bhernach\b', 'danach', text)
    text = re.sub(r'\bHernach\b', 'Danach', text)

    text = re.sub(r'\bimmerdar\b', 'immer', text)
    text = re.sub(r'\bImmerdar\b', 'Immer', text)

    text = re.sub(r'\bwiewohl\b', 'obwohl', text)
    text = re.sub(r'\bWiewohl\b', 'Obwohl', text)

    text = re.sub(r'\ballenthalben\b', 'überall', text)
    text = re.sub(r'\bAllenthalben\b', 'Überall', text)

    text = re.sub(r'\babermals\b', 'erneut', text)
    text = re.sub(r'\bAbermals\b', 'Erneut', text)

    text = re.sub(r'\bobschon\b', 'obwohl', text)
    text = re.sub(r'\bObschon\b', 'Obwohl', text)

    text = re.sub(r'\bfürwahr\b', 'wahrlich', text)
    text = re.sub(r'\bFürwahr\b', 'Wahrlich', text)

    text = re.sub(r'\bdieweil\b', 'weil', text)
    text = re.sub(r'\bDieweil\b', 'Weil', text)

    text = re.sub(r'\bewiglich\b', 'ewig', text)
    text = re.sub(r'\bEwiglich\b', 'Ewig', text)

    text = re.sub(r'\bnunmehr\b', 'jetzt', text)
    text = re.sub(r'\bNunmehr\b', 'Jetzt', text)

    # ================================================================
    # 3. PRONOUNS / ADJECTIVES (same declension pattern)
    # ================================================================

    # etliche/r/s/n → einige/r/s/n
    text = re.sub(r'\betlichen\b', 'einigen', text)
    text = re.sub(r'\bEtlichen\b', 'Einigen', text)
    text = re.sub(r'\betlicher\b', 'einiger', text)
    text = re.sub(r'\bEtlicher\b', 'Einiger', text)
    text = re.sub(r'\betliches\b', 'einiges', text)
    text = re.sub(r'\bEtliches\b', 'Einiges', text)
    text = re.sub(r'\betliche\b', 'einige', text)
    text = re.sub(r'\bEtliche\b', 'Einige', text)

    # ================================================================
    # 4. NOUNS — same gender, safe replacements
    # ================================================================

    # Trübsal (f) → Bedrängnis (f)  [f→f, consonant→consonant]
    text = re.sub(r'\bTrübsale\b', 'Bedrängnisse', text)
    text = re.sub(r'\bTrübsalen\b', 'Bedrängnissen', text)
    text = re.sub(r'\bTrübsal\b', 'Bedrängnis', text)

    # Greuel (m) → Gräuel (m)  [neue Rechtschreibung]
    text = re.sub(r'\bGreueln\b', 'Gräueln', text)
    text = re.sub(r'\bGreuels\b', 'Gräuels', text)
    text = re.sub(r'\bGreuel\b', 'Gräuel', text)

    # Speisopfer (n) → Speiseopfer (n)  [Fugen-e]
    text = re.sub(r'\bSpeisopfers\b', 'Speiseopfers', text)
    text = re.sub(r'\bSpeisopfer\b', 'Speiseopfer', text)

    # Hurerei (f) → Unzucht (f)  [f→f]
    text = re.sub(r'\bHurereien\b', 'Unzuchtsünden', text)
    text = re.sub(r'\bHurerei\b', 'Unzucht', text)

    # Buhlerei (f) → Unzucht (f)  [f→f]
    text = re.sub(r'\bBuhlerei\b', 'Unzucht', text)

    # Missetat (f) → Sünde (f)
    # DROPPED: ~30 Verse haben "Missetat" und "Sünde" zusammen,
    # Ersetzung würde "Sünde ... Sünde" erzeugen (Ps 32:1, 2Mo 34:7 etc.)
    # Missetäter → Übeltäter is safe though (different word)
    text = re.sub(r'\bMissetäter\b', 'Übeltäter', text)

    # Schmach (f) → Schande (f)  [f→f, consonant→consonant]
    text = re.sub(r'\bSchmach\b', 'Schande', text)

    # Zöllner (m) → Steuereintreiber (m)  [m→m, consonant→consonant]
    text = re.sub(r'\bZöllnern\b', 'Steuereintreibern', text)
    text = re.sub(r'\bZöllners\b', 'Steuereintreibers', text)
    text = re.sub(r'\bZöllner\b', 'Steuereintreiber', text)

    # Antlitz (n) → Gesicht (n)  [n→n, vowel→consonant]
    # German: no article elision, so "das Antlitz" → "das Gesicht" ✓
    text = re.sub(r'\bAntlitzes\b', 'Gesichtes', text)
    text = re.sub(r'\bAntlitz\b', 'Gesicht', text)

    # Schnur (f) → Schwiegertochter (f)
    # DROPPED: "Schnur" also means measuring cord/string (1 Kön 7:9 etc.)
    # Can't distinguish meanings with regex.

    # Oheim (m) → Onkel (m)  [m→m, vowel→vowel]
    text = re.sub(r'\bOheims\b', 'Onkels', text)
    text = re.sub(r'\bOheim\b', 'Onkel', text)

    return text


total_changes = 0
for f in sorted(glob.glob(os.path.join(SRC, '*_sch1951.json'))):
    with open(f) as fh:
        d = json.load(fh)

    changes = 0
    for ch in d['chapters']:
        for v in d['chapters'][ch]:
            orig = d['chapters'][ch][v]
            mod = modernize(orig)
            if mod != orig:
                d['chapters'][ch][v] = mod
                changes += 1

    bn = os.path.basename(f).replace('_sch1951.json', '')
    out_name = f'{bn}_sch1951mod.json'
    out_path = os.path.join(OUT, out_name)
    with open(out_path, 'w', encoding='utf-8') as fh:
        json.dump(d, fh, ensure_ascii=False)

    if changes:
        print(f'  {d["name"]}: {changes} Änderungen')
    total_changes += changes

print(f'\nTotal: {total_changes} Verse geändert')
