#!/usr/bin/env python3
"""Modernize the Spanish Reina-Valera 1909 Bible.

Two categories:
1. Orthographic fixes (pre-1911 spelling rules) — very safe, mechanical
2. Archaic vocabulary → modern equivalents — only clear 1:1 swaps
"""

import json, glob, os, re

SRC = os.path.join(os.path.dirname(__file__), '..', 'bibles', 'spa', 'rv1909')
OUT = os.path.join(os.path.dirname(__file__), '..', 'bibles', 'spa', 'rv1909mod')
os.makedirs(OUT, exist_ok=True)


def modernize(text):
    # ================================================================
    # 1. ORTHOGRAPHIC FIXES (pre-1911 rules)
    # ================================================================

    # Accented monosyllables: á→a, ó→o, é→e (as standalone words)
    text = re.sub(r'\bá\b', 'a', text)
    text = re.sub(r'\bó\b', 'o', text)
    text = re.sub(r'\bé\b', 'e', text)
    # Also at start of verse (capitalized — but these are prepositions,
    # so uppercase Á only at sentence start)
    text = re.sub(r'\bÁ\b', 'A', text)
    text = re.sub(r'\bÓ\b', 'O', text)
    text = re.sub(r'\bÉ\b', 'E', text)

    # Accented monosyllabic past tenses: fué→fue, dió→dio, vió→vio, fuí→fui
    text = re.sub(r'\bfué\b', 'fue', text)
    text = re.sub(r'\bFué\b', 'Fue', text)
    text = re.sub(r'\bFUÉ\b', 'FUE', text)
    text = re.sub(r'\bdió\b', 'dio', text)
    text = re.sub(r'\bDió\b', 'Dio', text)
    text = re.sub(r'\bvió\b', 'vio', text)
    text = re.sub(r'\bVió\b', 'Vio', text)
    text = re.sub(r'\bfuí\b', 'fui', text)
    text = re.sub(r'\bFuí\b', 'Fui', text)

    # crió → creó (old form of "crear" preterite)
    text = re.sub(r'\bcrió\b', 'creó', text)
    text = re.sub(r'\bCrió\b', 'Creó', text)

    # ================================================================
    # 2. VOCABULARY — safe 1:1 replacements
    # ================================================================

    # empero → pero  [conjunction, no article]
    text = re.sub(r'\bempero\b', 'pero', text)
    text = re.sub(r'\bEmpero\b', 'Pero', text)
    text = re.sub(r'\bEMPERO\b', 'PERO', text)

    # simiente(s) → descendencia / semilla(s)
    # "simiente" in biblical context usually means "descendencia" (lineage)
    # but also "semilla" (seed). Use "descendencia" as it's the dominant meaning.
    # Actually both meanings exist — keep it simple: simiente → descendencia
    # since that's the primary biblical usage. Drop simientes (only 4, mixed context).
    text = re.sub(r'\bsimiente\b', 'descendencia', text)
    text = re.sub(r'\bSimiente\b', 'Descendencia', text)

    # mancebo(s) → joven / jóvenes  [m→m, consonant→consonant]
    text = re.sub(r'\bmancebos\b', 'jóvenes', text)
    text = re.sub(r'\bMancebos\b', 'Jóvenes', text)
    text = re.sub(r'\bmancebo\b', 'joven', text)
    text = re.sub(r'\bMancebo\b', 'Joven', text)

    # sepulcro(s) → tumba(s)  [m→f gender change!]
    # "sepulcro" is m, "tumba" is f → article issues.
    # Use "sepultura" (f) which is also common? No — "tumba" is most natural.
    # Actually use "sepultura" — same gender change. Let's keep it simple:
    # el sepulcro → la tumba, del sepulcro → de la tumba...
    # Too complex. Use "sepultura" (f) — same issue.
    # Actually just drop this — sepulcro is still understood in modern Spanish.
    # DROPPED: gender change m→f too complex.

    # publicano(s) → cobrador(es) de impuestos  [m→m, consonant→consonant]
    text = re.sub(r'\bpublicanos\b', 'cobradores de impuestos', text)
    text = re.sub(r'\bPublicanos\b', 'Cobradores de impuestos', text)
    text = re.sub(r'\bpublicano\b', 'cobrador de impuestos', text)
    text = re.sub(r'\bPublicano\b', 'Cobrador de impuestos', text)

    # concupiscencia(s) → codicia(s)  [f→f, consonant→consonant]
    text = re.sub(r'\bconcupiscencias\b', 'codicias', text)
    text = re.sub(r'\bConcupiscencias\b', 'Codicias', text)
    text = re.sub(r'\bconcupiscencia\b', 'codicia', text)
    text = re.sub(r'\bConcupiscencia\b', 'Codicia', text)

    # prevaricación(es) → transgresión(es)  [f→f, consonant→consonant]
    text = re.sub(r'\bprevaricaciones\b', 'transgresiones', text)
    text = re.sub(r'\bPrevaricaciones\b', 'Transgresiones', text)
    text = re.sub(r'\bprevaricación\b', 'transgresión', text)
    text = re.sub(r'\bPrevaricación\b', 'Transgresión', text)

    # prevaricador(es) → transgresor(es)  [m→m, consonant→consonant]
    text = re.sub(r'\bprevaricadores\b', 'transgresores', text)
    text = re.sub(r'\bPrevaricadores\b', 'Transgresores', text)
    text = re.sub(r'\bprevaricador\b', 'transgresor', text)
    text = re.sub(r'\bPrevaricador\b', 'Transgresor', text)

    # fornicario(s) → inmoral(es)  [m→m, consonant→vowel]
    # "el fornicario" → "el inmoral" ✓ (both m, article doesn't change)
    text = re.sub(r'\bfornicarios\b', 'inmorales', text)
    text = re.sub(r'\bFornicarios\b', 'Inmorales', text)
    text = re.sub(r'\bfornicario\b', 'inmoral', text)
    text = re.sub(r'\bFornicario\b', 'Inmoral', text)

    # fornicación(es) → inmoralidad(es) sexual(es)  [f→f, consonant→vowel]
    # "la fornicación" → "la inmoralidad sexual" ✓ (both f, consonant start)
    # Wait: inmoralidad starts with vowel 'i'. "la fornicación" → "la inmoralidad" ✓
    # (in Spanish "la" doesn't elide before vowels except "a": "la inmoralidad" is correct)
    text = re.sub(r'\bfornicaciones\b', 'inmoralidades sexuales', text)
    text = re.sub(r'\bFornicaciones\b', 'Inmoralidades sexuales', text)
    text = re.sub(r'\bfornicación\b', 'inmoralidad sexual', text)
    text = re.sub(r'\bFornicación\b', 'Inmoralidad sexual', text)

    # disolución(es) → libertinaje(s)  [f→m gender change]
    # DROPPED: gender change f→m

    # iniquidad(es) → injusticia(s)  [f→f, vowel→vowel]
    text = re.sub(r'\biniquidades\b', 'injusticias', text)
    text = re.sub(r'\bIniquidades\b', 'Injusticias', text)
    text = re.sub(r'\biniquidad\b', 'injusticia', text)
    text = re.sub(r'\bIniquidad\b', 'Injusticia', text)

    # inmundicia(s) → impureza(s)  [f→f, vowel→vowel]
    text = re.sub(r'\binmundicias\b', 'impurezas', text)
    text = re.sub(r'\bInmundicias\b', 'Impurezas', text)
    text = re.sub(r'\binmundicia\b', 'impureza', text)
    text = re.sub(r'\bInmundicia\b', 'Impureza', text)

    # tribulación(es) → sufrimiento(s)  [f→m gender change]
    # DROPPED: gender change f→m
    # Actually: use "prueba(s)" (f→f) instead
    text = re.sub(r'\btribulaciones\b', 'pruebas', text)
    text = re.sub(r'\bTribulaciones\b', 'Pruebas', text)
    text = re.sub(r'\btribulación\b', 'prueba', text)
    text = re.sub(r'\bTribulación\b', 'Prueba', text)

    # longanimidad → paciencia  [f→f, consonant→consonant]
    # DROPPED: creates "paciencia, y paciencia" in Rom 2:4 etc.

    # holocausto(s) → sacrificio(s) quemado(s)  [m→m, vowel→consonant]
    # "el holocausto" → "el sacrificio quemado" ✓ (Spanish: no elision)
    # "del holocausto" → "del sacrificio quemado" ✓
    text = re.sub(r'\bholocaustos\b', 'sacrificios quemados', text)
    text = re.sub(r'\bHolocaustos\b', 'Sacrificios quemados', text)
    text = re.sub(r'\bholocausto\b', 'sacrificio quemado', text)
    text = re.sub(r'\bHolocausto\b', 'Sacrificio quemado', text)

    # postrimería(s) → final(es)  [f→m gender change]
    # DROPPED: gender change

    # remisión → perdón  [f→m gender change]
    # DROPPED: gender change

    # ignominia → vergüenza  [f→f, vowel→consonant]
    # "la ignominia" → "la vergüenza" ✓ (Spanish: no article elision)
    text = re.sub(r'\bignominias\b', 'vergüenzas', text)
    text = re.sub(r'\bIgnominias\b', 'Vergüenzas', text)
    text = re.sub(r'\bignominia\b', 'vergüenza', text)
    text = re.sub(r'\bIgnominia\b', 'Vergüenza', text)

    # menester → necesidad  [m→f gender change]
    # DROPPED: gender change

    # escarnio → burla  [m→f gender change]
    # DROPPED: gender change

    # allegó → acercó, allegaron → acercaron, etc.  [verb, no article]
    text = re.sub(r'\ballegaron\b', 'acercaron', text)
    text = re.sub(r'\bAllegaron\b', 'Acercaron', text)
    text = re.sub(r'\ballegaos\b', 'acercaos', text)
    text = re.sub(r'\bAllegaos\b', 'Acercaos', text)
    text = re.sub(r'\ballegarse\b', 'acercarse', text)
    text = re.sub(r'\bAllegarse\b', 'Acercarse', text)
    text = re.sub(r'\ballegó\b', 'acercó', text)
    text = re.sub(r'\bAllegó\b', 'Acercó', text)
    # Don't replace "allegar" generically — could conflict with other forms

    # congoja(s) → angustia(s)  [f→f, consonant→vowel]
    # DROPPED: creates "pan de angustia y agua de angustia" in Isa 30:20

    return text


total_changes = 0
for f in sorted(glob.glob(os.path.join(SRC, '*_rv1909.json'))):
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

    bn = os.path.basename(f).replace('_rv1909.json', '')
    out_name = f'{bn}_rv1909mod.json'
    out_path = os.path.join(OUT, out_name)
    with open(out_path, 'w', encoding='utf-8') as fh:
        json.dump(d, fh, ensure_ascii=False)

    if changes:
        print(f'  {d["name"]}: {changes} Änderungen')
    total_changes += changes

print(f'\nTotal: {total_changes} Verse geändert')
