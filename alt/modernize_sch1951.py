#!/usr/bin/env python3
"""Modernize the German Schlachter 1951 Bible.

Only safe 1:1 replacements: adverbs/conjunctions (no articles),
pronouns with same declension, nouns with same gender,
archaic verb forms (sehet→seht, höret→hört, etc.).

Dropped: Weib (n→f), Jüngling (→compound), Dirne (f→n),
Kebsweib (n→f).
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

    # ================================================================
    # 5. ARCHAIC VERB FORMS (drop the -e- before -t)
    # ================================================================
    # "sehet, höret, gehet" → "seht, hört, geht"
    # Applies to imperatives, 2nd pl., 3rd sg., and past participles.

    _VERBS = {
        # Simple verbs
        'lasset': 'lasst', 'sehet': 'seht', 'höret': 'hört',
        'wisset': 'wisst', 'gehet': 'geht', 'saget': 'sagt',
        'nehmet': 'nehmt', 'bringet': 'bringt', 'esset': 'esst',
        'lobet': 'lobt', 'ziehet': 'zieht', 'machet': 'macht',
        'glaubet': 'glaubt', 'suchet': 'sucht', 'sprechet': 'sprecht',
        'dienet': 'dient', 'bleibet': 'bleibt', 'merket': 'merkt',
        'kehret': 'kehrt', 'grüßet': 'grüßt', 'waret': 'wart',
        'stehet': 'steht', 'liebet': 'liebt', 'singet': 'singt',
        'gedenket': 'gedenkt', 'erkennet': 'erkennt', 'kommet': 'kommt',
        'freuet': 'freut', 'trinket': 'trinkt', 'führet': 'führt',
        'erhebet': 'erhebt', 'danket': 'dankt', 'leget': 'legt',
        'lebet': 'lebt', 'weichet': 'weicht', 'habet': 'habt',
        'traget': 'tragt', 'heiliget': 'heiligt',
        'fliehet': 'flieht', 'folget': 'folgt', 'bauet': 'baut',
        'weinet': 'weint', 'schauet': 'schaut', 'preiset': 'preist',
        'fallet': 'fallt', 'sorget': 'sorgt', 'stärket': 'stärkt',
        'rufet': 'ruft', 'stellet': 'stellt', 'rühret': 'rührt',
        'säet': 'sät', 'schlaget': 'schlagt', 'spielet': 'spielt',
        'reiniget': 'reinigt', 'leset': 'lest', 'prüfet': 'prüft',
        'lehret': 'lehrt', 'laufet': 'lauft', 'teilet': 'teilt',
        'tuet': 'tut', 'treibet': 'treibt', 'herrschet': 'herrscht',
        'heilet': 'heilt', 'schlafet': 'schlaft', 'kämpfet': 'kämpft',
        'rühmet': 'rühmt', 'schwöret': 'schwört', 'empfanget': 'empfangt',
        'schicket': 'schickt', 'löset': 'löst', 'schreibet': 'schreibt',
        'rücket': 'rückt', 'eilet': 'eilt', 'schmecket': 'schmeckt',
        'klaget': 'klagt', 'lieget': 'liegt', 'schmücket': 'schmückt',
        'wirket': 'wirkt', 'wünschet': 'wünscht',
        'gehorchet': 'gehorcht', 'gelobet': 'gelobt',
        'wachet': 'wacht', 'heulet': 'heult', 'denket': 'denkt',
        'setzet': 'setzt', 'hebet': 'hebt', 'meinet': 'meint',
        'werfet': 'werft', 'sündiget': 'sündigt', 'übet': 'übt',
        'fanget': 'fangt', 'lobsinget': 'lobsingt',
        'frohlocket': 'frohlockt', 'jauchzet': 'jauchzt',
        'fraget': 'fragt', 'blaset': 'blast', 'sterbet': 'sterbt',
        'lernet': 'lernt', 'pflanzet': 'pflanzt', 'füllet': 'füllt',
        'möget': 'mögt', 'schaffet': 'schafft', 'kaufet': 'kauft',
        'brechet': 'brecht', 'zoget': 'zogt', 'wehret': 'wehrt',
        'stoßet': 'stoßt', 'jaget': 'jagt', 'hasset': 'hasst',
        'mehret': 'mehrt', 'zeiget': 'zeigt', 'sahet': 'saht',
        'irret': 'irrt', 'sprachet': 'spracht', 'forschet': 'forscht',
        'zählet': 'zählt', 'fahret': 'fahrt', 'prediget': 'predigt',
        'fasset': 'fasst', 'schreiet': 'schreit', 'murret': 'murrt',
        'heißet': 'heißt', 'kamet': 'kamt', 'sitzet': 'sitzt',
        'klopfet': 'klopft',
        # Compound verbs with prefixes
        'verkündiget': 'verkündigt', 'verlasset': 'verlasst',
        'erschrecket': 'erschreckt', 'erfahret': 'erfahrt',
        'vertrauet': 'vertraut', 'befolget': 'befolgt',
        'vergesset': 'vergesst', 'befleißiget': 'befleißigt',
        'vermöget': 'vermögt', 'befraget': 'befragt',
        'umkommet': 'umkommt', 'verehret': 'verehrt',
        'hineinkommet': 'hineinkommt', 'ertraget': 'ertragt',
        'erzählet': 'erzählt', 'verstocket': 'verstockt',
        'begehret': 'begehrt', 'erforschet': 'erforscht',
        'ergreifet': 'ergreift', 'besitzet': 'besitzt',
        'einnehmet': 'einnehmt', 'hingehet': 'hingeht',
        'erfüllet': 'erfüllt', 'erstarket': 'erstarkt',
        'ansehet': 'anseht', 'zerstreuet': 'zerstreut',
        'verstehet': 'versteht', 'bedenket': 'bedenkt',
        'erkundiget': 'erkundigt', 'bezeuget': 'bezeugt',
        'verunreiniget': 'verunreinigt', 'angehöret': 'angehört',
        'bedürfet': 'bedürft', 'erlanget': 'erlangt',
        'besehet': 'beseht', 'ermahnet': 'ermahnt',
        'vergebet': 'vergebt', 'verberget': 'verbergt',
        'bewahret': 'bewahrt', 'zerstöret': 'zerstört',
        'verzehret': 'verzehrt', 'darbringet': 'darbringt',
        'umkehret': 'umkehrt', 'bestellet': 'bestellt',
        'erlöset': 'erlöst', 'beschauet': 'beschaut',
        'bekehret': 'bekehrt', 'erbauet': 'erbaut',
        'zuhöret': 'zuhört', 'versuchet': 'versucht',
        'anrufet': 'anruft', 'abkehret': 'abkehrt',
        'abweichet': 'abweicht',
        # Remaining forms found in second pass
        'weiset': 'weist', 'ehret': 'ehrt', 'neiget': 'neigt',
        'brauchet': 'braucht', 'müsset': 'müsst', 'nahet': 'naht',
        'leihet': 'leiht', 'reizet': 'reizt', 'wälzet': 'wälzt',
        'reißet': 'reißt', 'ruhet': 'ruht', 'strebet': 'strebt',
        'zerreißet': 'zerreißt', 'erwählet': 'erwählt',
        'gießet': 'gießt', 'speiset': 'speist', 'begrabet': 'begrabt',
        'währet': 'währt', 'reichet': 'reicht', 'holet': 'holt',
        'reget': 'regt', 'waschet': 'wascht', 'vergießet': 'vergießt',
        'abweiset': 'abweist', 'verwerfet': 'verwerft',
    }

    def _fix_verb(m):
        word = m.group(0)
        modern = _VERBS[word.lower()]
        if word[0].isupper():
            return modern[0].upper() + modern[1:]
        return modern

    _verb_pat = r'\b(' + '|'.join(
        sorted(_VERBS, key=len, reverse=True)
    ) + r')\b'
    text = re.sub(_verb_pat, _fix_verb, text, flags=re.IGNORECASE)

    # "gebet" (lowercase only) → "gebt" — skip "Gebet" (noun = prayer)
    text = re.sub(r'\bgebet\b', 'gebt', text)

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
