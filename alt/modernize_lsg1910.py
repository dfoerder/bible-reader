#!/usr/bin/env python3
"""Modernize the French Louis Segond 1910 Bible — clear 1:1 replacements only.

Only replaces words where gender and article elision are safe:
- Same gender AND same initial type (both consonant or both vowel), OR
- Article context handled explicitly.

Dropped: opprobre, ignominie, courroux, ire, rémission, propitiatoire
(gender change or vowel/consonant mismatch too complex for regex).
"""

import json, glob, os, re

SRC = os.path.join(os.path.dirname(__file__), '..', 'bibles', 'fra', 'lsg1910')
OUT = os.path.join(os.path.dirname(__file__), '..', 'bibles', 'fra', 'lsg1910mod')
os.makedirs(OUT, exist_ok=True)

A = '’'  # typographic apostrophe


def modernize(text):
    # === Compound expressions (longest first) ===
    text = re.sub(r'\bsouverains sacrificateurs\b', 'grands prêtres', text)
    text = re.sub(r'\bSouverains sacrificateurs\b', 'Grands prêtres', text)
    text = re.sub(r'\bsouverain sacrificateur\b', 'grand prêtre', text)
    text = re.sub(r'\bSouverain sacrificateur\b', 'Grand prêtre', text)
    text = re.sub(r'\bSouverain Sacrificateur\b', 'Grand Prêtre', text)

    # ============================================================
    # SAFE 1:1 — same gender, same initial type (consonant/vowel)
    # ============================================================

    # sacrificateur(s) → prêtre(s)  [m→m, consonant→consonant]
    text = re.sub(r'\bsacrificateurs\b', 'prêtres', text)
    text = re.sub(r'\bSacrificateurs\b', 'Prêtres', text)
    text = re.sub(r'\bsacrificateur\b', 'prêtre', text)
    text = re.sub(r'\bSacrificateur\b', 'Prêtre', text)

    # sépulcre(s) → tombeau(x)  [m→m, consonant→consonant]
    text = re.sub(r'\bsépulcres\b', 'tombeaux', text)
    text = re.sub(r'\bSépulcres\b', 'Tombeaux', text)
    text = re.sub(r'\bsépulcre\b', 'tombeau', text)
    text = re.sub(r'\bSépulcre\b', 'Tombeau', text)

    # centenier(s) → centurion(s)  [m→m, consonant→consonant]
    text = re.sub(r'\bcenteniers\b', 'centurions', text)
    text = re.sub(r'\bCenteniers\b', 'Centurions', text)
    text = re.sub(r'\bcentenier\b', 'centurion', text)
    text = re.sub(r'\bCentenier\b', 'Centurion', text)

    # publicain(s) → collecteur(s) d'impôts  [m→m, consonant→consonant]
    text = re.sub(r'\bpublicains\b', f'collecteurs d{A}impôts', text)
    text = re.sub(r'\bPublicains\b', f'Collecteurs d{A}impôts', text)
    text = re.sub(r'\bpublicain\b', f'collecteur d{A}impôts', text)
    text = re.sub(r'\bPublicain\b', f'Collecteur d{A}impôts', text)

    # postérité → descendance  [f→f, consonant→consonant]
    text = re.sub(r'\bpostérité\b', 'descendance', text)
    text = re.sub(r'\bPostérité\b', 'Descendance', text)

    # concupiscence(s) → convoitise(s)  [f→f, consonant→consonant]
    text = re.sub(r'\bconcupiscences\b', 'convoitises', text)
    text = re.sub(r'\bConcupiscences\b', 'Convoitises', text)
    text = re.sub(r'\bconcupiscence\b', 'convoitise', text)
    text = re.sub(r'\bConcupiscence\b', 'Convoitise', text)

    # prévarication(s) → transgression(s)  [f→f, consonant→consonant]
    text = re.sub(r'\bprévarications\b', 'transgressions', text)
    text = re.sub(r'\bPrévarications\b', 'Transgressions', text)
    text = re.sub(r'\bprévarication\b', 'transgression', text)
    text = re.sub(r'\bPrévarication\b', 'Transgression', text)

    # prévaricateur(s) → transgresseur(s)  [m→m, consonant→consonant]
    text = re.sub(r'\bprévaricateurs\b', 'transgresseurs', text)
    text = re.sub(r'\bPrévaricateurs\b', 'Transgresseurs', text)
    text = re.sub(r'\bprévaricateur\b', 'transgresseur', text)
    text = re.sub(r'\bPrévaricateur\b', 'Transgresseur', text)

    # dissolution(s) → débauche(s)  [f→f, consonant→consonant]
    text = re.sub(r'\bdissolutions\b', 'débauches', text)
    text = re.sub(r'\bDissolutions\b', 'Débauches', text)
    text = re.sub(r'\bdissolution\b', 'débauche', text)
    text = re.sub(r'\bDissolution\b', 'Débauche', text)

    # fornicateur(s) → débauché(s)  [m→m, consonant→consonant]
    text = re.sub(r'\bfornicateurs\b', 'débauchés', text)
    text = re.sub(r'\bFornicateurs\b', 'Débauchés', text)
    text = re.sub(r'\bfornicateur\b', 'débauché', text)
    text = re.sub(r'\bFornicateur\b', 'Débauché', text)

    # iniquité(s) → injustice(s)  [f→f, vowel→vowel]
    text = re.sub(r'\biniquités\b', 'injustices', text)
    text = re.sub(r'\bIniquités\b', 'Injustices', text)
    text = re.sub(r'\biniquité\b', 'injustice', text)
    text = re.sub(r'\bIniquité\b', 'Injustice', text)

    # impudicité(s) → immoralité(s)  [f→f, vowel→vowel]
    text = re.sub(r'\bimpudicités\b', 'immoralités', text)
    text = re.sub(r'\bImpudicités\b', 'Immoralités', text)
    text = re.sub(r'\bimpudicité\b', 'immoralité', text)
    text = re.sub(r'\bImpudicité\b', 'Immoralité', text)

    # oblation(s) → offrande(s)  [f→f, vowel→vowel]
    text = re.sub(r'\boblations\b', 'offrandes', text)
    text = re.sub(r'\bOblations\b', 'Offrandes', text)
    text = re.sub(r'\boblation\b', 'offrande', text)
    text = re.sub(r'\bOblation\b', 'Offrande', text)

    # derechef → de nouveau  [adverb, no article]
    text = re.sub(r'\bderechef\b', 'de nouveau', text)
    text = re.sub(r'\bDerechef\b', 'De nouveau', text)

    # septante → soixante-dix  [numeral, no article]
    text = re.sub(r'\bseptante\b', 'soixante-dix', text)
    text = re.sub(r'\bSeptante\b', 'Soixante-dix', text)

    # débonnaire(s) → doux  [adjective, no article issue]
    text = re.sub(r'\bdébonnaires\b', 'doux', text)
    text = re.sub(r'\bDébonnaires\b', 'Doux', text)
    text = re.sub(r'\bdébonnaire\b', 'doux', text)
    text = re.sub(r'\bDébonnaire\b', 'Doux', text)

    # prémices — DROPPED: creates "premiers fruits des premiers fruits" in Ex 23:19 etc.
    # The word is still understood in modern French.

    # ============================================================
    # WITH ARTICLE HANDLING — consonant→vowel or vowel→consonant
    # ============================================================

    # holocauste(s) → sacrifice(s) brûlé(s)  [m→m, vowel→consonant]
    # Contractions first: de l' → du, à l' → au (longest patterns first)
    text = re.sub(rf"de l{A}holocauste\b", 'du sacrifice brûlé', text)
    text = re.sub(rf"De l{A}holocauste\b", 'Du sacrifice brûlé', text)
    text = re.sub(rf"à l{A}holocauste\b", 'au sacrifice brûlé', text)
    text = re.sub(rf"À l{A}holocauste\b", 'Au sacrifice brûlé', text)
    # Then l'/d' → le/de
    text = re.sub(rf"[lL]{A}holocaustes\b", 'les sacrifices brûlés', text)
    text = re.sub(rf"[dD]{A}holocaustes\b", 'de sacrifices brûlés', text)
    text = re.sub(rf"l{A}holocauste\b", 'le sacrifice brûlé', text)
    text = re.sub(rf"L{A}holocauste\b", 'Le sacrifice brûlé', text)
    text = re.sub(rf"L{A}Holocauste\b", 'Le Sacrifice brûlé', text)
    text = re.sub(rf"d{A}holocauste\b", 'de sacrifice brûlé', text)
    text = re.sub(rf"D{A}holocauste\b", 'De sacrifice brûlé', text)
    text = re.sub(rf"cet holocauste\b", 'ce sacrifice brûlé', text)
    text = re.sub(rf"Cet holocauste\b", 'Ce sacrifice brûlé', text)
    # Standalone (after un, son, mon, ton, etc. — no change needed, both m)
    text = re.sub(r'\bholocaustes\b', 'sacrifices brûlés', text)
    text = re.sub(r'\bHolocaustes\b', 'Sacrifices brûlés', text)
    text = re.sub(r'\bholocauste\b', 'sacrifice brûlé', text)
    text = re.sub(r'\bHolocauste\b', 'Sacrifice brûlé', text)

    # fornication(s) → immoralité(s) sexuelle(s)  [f→f, consonant→vowel]
    # Fix articles: la fornication → l'immoralité sexuelle
    text = re.sub(r'\bla fornications\b', f'les immoralités sexuelles', text)
    text = re.sub(r'\bLa fornications\b', f'Les immoralités sexuelles', text)
    text = re.sub(r'\bla fornication\b', f'l{A}immoralité sexuelle', text)
    text = re.sub(r'\bLa fornication\b', f'L{A}immoralité sexuelle', text)
    text = re.sub(r'\bde fornication\b', f'd{A}immoralité sexuelle', text)
    text = re.sub(r'\bsa fornication\b', f'son immoralité sexuelle', text)
    text = re.sub(r'\bSa fornication\b', f'Son immoralité sexuelle', text)
    text = re.sub(r'\bfornications\b', 'immoralités sexuelles', text)
    text = re.sub(r'\bFornications\b', 'Immoralités sexuelles', text)
    text = re.sub(r'\bfornication\b', 'immoralité sexuelle', text)
    text = re.sub(r'\bFornication\b', 'Immoralité sexuelle', text)

    # tribulation(s) → épreuve(s)  [f→f, consonant→vowel]
    text = re.sub(r'\bla tribulation\b', f'l{A}épreuve', text)
    text = re.sub(r'\bLa tribulation\b', f'L{A}épreuve', text)
    text = re.sub(r'\bde tribulation\b', f'd{A}épreuve', text)
    text = re.sub(r'\bsa tribulation\b', f'son épreuve', text)
    text = re.sub(r'\bSa tribulation\b', f'Son épreuve', text)
    text = re.sub(r'\btribulations\b', 'épreuves', text)
    text = re.sub(r'\bTribulations\b', 'Épreuves', text)
    text = re.sub(r'\btribulation\b', 'épreuve', text)
    text = re.sub(r'\bTribulation\b', 'Épreuve', text)

    # turpitude(s) → infamie(s)  [f→f, consonant→vowel]
    text = re.sub(r'\bla turpitude\b', f'l{A}infamie', text)
    text = re.sub(r'\bLa turpitude\b', f'L{A}infamie', text)
    text = re.sub(r'\bde turpitude\b', f'd{A}infamie', text)
    text = re.sub(r'\bsa turpitude\b', f'son infamie', text)
    text = re.sub(r'\bSa turpitude\b', f'Son infamie', text)
    text = re.sub(r'\bturpitudes\b', 'infamies', text)
    text = re.sub(r'\bTurpitudes\b', 'Infamies', text)
    text = re.sub(r'\bturpitude\b', 'infamie', text)
    text = re.sub(r'\bTurpitude\b', 'Infamie', text)

    # souillure(s) → impureté(s)  [f→f, consonant→vowel]
    text = re.sub(r'\bla souillures\b', f'les impuretés', text)
    text = re.sub(r'\bla souillure\b', f'l{A}impureté', text)
    text = re.sub(r'\bLa souillure\b', f'L{A}impureté', text)
    text = re.sub(r'\bde souillure\b', f'd{A}impureté', text)
    text = re.sub(r'\bsa souillure\b', f'son impureté', text)
    text = re.sub(r'\bSa souillure\b', f'Son impureté', text)
    text = re.sub(r'\bsouillures\b', 'impuretés', text)
    text = re.sub(r'\bSouillures\b', 'Impuretés', text)
    text = re.sub(r'\bsouillure\b', 'impureté', text)
    text = re.sub(r'\bSouillure\b', 'Impureté', text)

    # libation(s) → offrande(s) liquide(s)  [f→f, consonant→vowel]
    text = re.sub(r'\bla libation\b', f'l{A}offrande liquide', text)
    text = re.sub(r'\bLa libation\b', f'L{A}offrande liquide', text)
    text = re.sub(r'\bde libation\b', f'd{A}offrande liquide', text)
    text = re.sub(r'\bsa libation\b', f'son offrande liquide', text)
    text = re.sub(r'\blibations\b', 'offrandes liquides', text)
    text = re.sub(r'\bLibations\b', 'Offrandes liquides', text)
    text = re.sub(r'\blibation\b', 'offrande liquide', text)
    text = re.sub(r'\bLibation\b', 'Offrande liquide', text)

    return text


total_changes = 0
for f in sorted(glob.glob(os.path.join(SRC, '*_lsg1910.json'))):
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

    bn = os.path.basename(f).replace('_lsg1910.json', '')
    out_name = f'{bn}_lsg1910mod.json'
    out_path = os.path.join(OUT, out_name)
    with open(out_path, 'w', encoding='utf-8') as fh:
        json.dump(d, fh, ensure_ascii=False)

    if changes:
        print(f'  {d["name"]}: {changes} Änderungen')
    total_changes += changes

print(f'\nTotal: {total_changes} Verse geändert')
