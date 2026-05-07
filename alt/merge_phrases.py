#!/usr/bin/env python3
"""
Find and merge multi-word expressions in Bible annotations.

Phase 1: Scan Bible text for known phrases, report findings.
Phase 2: Merge matching consecutive annotations into single entries with pos_end.
"""

import json, os, re
from collections import defaultdict

BASE = os.path.dirname(os.path.abspath(__file__))
BIBLE_DIR = os.path.join(BASE, '..', 'bibles', 'eng', 'web')

# ── Phrase list ──────────────────────────────────────────
# Format: (english_phrase, german_translation, cefr_level)
# Sorted by word count descending so longer phrases match first.

PHRASES = [
    # 4-word
    ("on account of", "wegen", "B2"),
    ("in front of", "vor", "A2"),
    ("in the midst of", "inmitten", "C1"),
    ("on top of", "auf", "A2"),
    ("at the end of", "am Ende von", "A2"),
    ("in spite of", "trotz", "B1"),
    ("on behalf of", "im Namen von", "B2"),
    ("by means of", "mittels", "B2"),
    ("in place of", "anstelle von", "B1"),
    ("in charge of", "verantwortlich für", "B1"),
    ("take care of", "sich kümmern um", "A2"),
    ("take hold of", "ergreifen", "B1"),
    ("take part in", "teilnehmen an", "B1"),
    ("give birth to", "gebären", "B1"),
    ("gave birth to", "gebar", "B1"),
    ("given birth to", "geboren", "B1"),
    ("gives birth to", "gebiert", "B1"),
    ("giving birth to", "gebärend", "B1"),
    ("give thanks to", "danken", "A2"),
    ("gave thanks to", "dankte", "A2"),
    ("giving thanks to", "dankend", "A2"),
    ("make use of", "nutzen", "B1"),
    ("get rid of", "loswerden", "B1"),

    # 3-word phrasal verbs
    ("set apart for", "absondern für", "B2"),
    ("carried away to", "weggeführt nach", "B2"),
    ("casting out", "austreibend", "B2"),
    ("look forward to", "sich freuen auf", "B1"),
    ("come up with", "sich einfallen lassen", "B2"),
    ("put up with", "ertragen", "B2"),
    ("run out of", "ausgehen", "B1"),
    ("look down on", "herabsehen auf", "B2"),
    ("look up to", "aufblicken zu", "B2"),
    ("cut off from", "abschneiden von", "B2"),

    # 3-word nouns / fixed expressions
    ("burnt offering", "Brandopfer", "C2"),
    ("burnt offerings", "Brandopfer", "C2"),
    ("sin offering", "Sündopfer", "C2"),
    ("sin offerings", "Sündopfer", "C2"),
    ("peace offering", "Friedensopfer", "C2"),
    ("peace offerings", "Friedensopfer", "C2"),
    ("grain offering", "Speiseopfer", "C2"),
    ("grain offerings", "Speiseopfer", "C2"),
    ("guilt offering", "Schuldopfer", "C2"),
    ("guilt offerings", "Schuldopfer", "C2"),
    ("drink offering", "Trankopfer", "C2"),
    ("drink offerings", "Trankopfer", "C2"),
    ("wave offering", "Schwingopfer", "C2"),
    ("high priest", "Hohepriester", "B2"),
    ("high priests", "Hohepriester", "B2"),
    ("chief priests", "Hohepriester", "B2"),
    ("chief priest", "Hohepriester", "B2"),
    ("olive tree", "Olivenbaum", "A2"),
    ("olive trees", "Olivenbäume", "A2"),
    ("fig tree", "Feigenbaum", "A2"),
    ("fig trees", "Feigenbäume", "A2"),
    ("palm tree", "Palme", "A2"),
    ("palm trees", "Palmen", "A2"),
    ("upper room", "Obergemach", "B2"),
    ("holy place", "heilige Stätte", "B1"),
    ("holy places", "heilige Stätten", "B1"),
    ("most holy", "Allerheiligstes", "B2"),
    ("Most High", "Höchster", "C1"),
    ("eternal life", "ewiges Leben", "B2"),
    ("living God", "lebendiger Gott", "B2"),
    ("right hand", "rechte Hand", "A2"),
    ("left hand", "linke Hand", "A2"),
    ("right hands", "rechte Hände", "A2"),
    ("young man", "junger Mann", "A2"),
    ("young men", "junge Männer", "A2"),
    ("young woman", "junge Frau", "A2"),
    ("young women", "junge Frauen", "A2"),
    ("old man", "alter Mann", "A2"),
    ("old men", "alte Männer", "A2"),
    ("outer darkness", "äußere Finsternis", "C1"),
    ("loving kindness", "Güte", "B2"),
    ("lovingkindness", "Güte", "C1"),
    ("no one", "niemand", "A2"),
    ("one another", "einander", "B1"),
    ("each other", "einander", "A2"),
    ("as well", "auch", "B1"),
    ("at once", "sofort", "B1"),
    ("at last", "endlich", "B1"),
    ("in vain", "vergeblich", "B2"),
    ("so that", "damit", "A2"),
    ("as if", "als ob", "B1"),
    ("even though", "obwohl", "B1"),
    ("even if", "selbst wenn", "B1"),
    ("instead of", "anstatt", "B1"),
    ("because of", "wegen", "A2"),
    ("in order to", "um zu", "A2"),
    ("according to", "gemäß", "B1"),
    ("tent of meeting", "Zelt der Begegnung", "C2"),
    ("ark of the covenant", "Bundeslade", "C2"),
    ("day of atonement", "Versöhnungstag", "C2"),

    # 2-word phrasal verbs
    ("give birth", "gebären", "B1"),
    ("gave birth", "gebar", "B1"),
    ("given birth", "geboren", "B1"),
    ("gives birth", "gebiert", "B1"),
    ("giving birth", "gebärend", "B1"),
    ("set apart", "absondern", "B2"),
    ("sets apart", "sondert ab", "B2"),
    ("setting apart", "absondernd", "B2"),
    ("set up", "aufstellen", "B1"),
    ("set out", "aufbrechen", "B1"),
    ("set free", "freilassen", "B1"),
    ("sent out", "aussenden", "B1"),
    ("send out", "aussenden", "B1"),
    ("send away", "wegschicken", "B1"),
    ("sent away", "wegschicken", "B1"),
    ("cast out", "austreiben", "B2"),
    ("casts out", "treibt aus", "B2"),
    ("casting out", "austreibend", "B2"),
    ("cast down", "niederwerfen", "B2"),
    ("cast into", "hineinwerfen", "B2"),
    ("cast off", "verwerfen", "B2"),
    ("put on", "anziehen", "A2"),
    ("put off", "ablegen", "B1"),
    ("put away", "wegtun", "B1"),
    ("put forth", "ausstrecken", "B2"),
    ("take away", "wegnehmen", "B1"),
    ("took away", "nahm weg", "B1"),
    ("takes away", "nimmt weg", "B1"),
    ("taking away", "wegnehmend", "B1"),
    ("take off", "ausziehen", "A2"),
    ("take out", "herausnehmen", "B1"),
    ("take up", "aufheben", "B1"),
    ("took up", "nahm auf", "B1"),
    ("takes up", "nimmt auf", "B1"),
    ("taking up", "aufnehmend", "B1"),
    ("taken away", "weggenommen", "B1"),
    ("taken up", "aufgenommen", "B1"),
    ("turn away", "abwenden", "B1"),
    ("turns away", "wendet ab", "B1"),
    ("turning away", "abwendend", "B1"),
    ("turn back", "umkehren", "B1"),
    ("turns back", "kehrt um", "B1"),
    ("turning back", "umkehrend", "B1"),
    ("turn around", "sich umdrehen", "A2"),
    ("turned away", "abgewandt", "B1"),
    ("turned back", "umgekehrt", "B1"),
    ("bring forth", "hervorbringen", "B2"),
    ("brings forth", "bringt hervor", "B2"),
    ("bringing forth", "hervorbringend", "B2"),
    ("bring back", "zurückbringen", "B1"),
    ("brings back", "bringt zurück", "B1"),
    ("bringing back", "zurückbringend", "B1"),
    ("bring up", "aufziehen", "B1"),
    ("brings up", "zieht auf", "B1"),
    ("bringing up", "aufziehend", "B1"),
    ("brought forth", "hervorgebracht", "B2"),
    ("brought back", "zurückgebracht", "B1"),
    ("brought up", "aufgezogen", "B1"),
    ("come about", "geschehen", "B2"),
    ("come back", "zurückkommen", "A2"),
    ("come forth", "hervorkommen", "B2"),
    ("come out", "herauskommen", "A2"),
    ("came about", "geschah", "B2"),
    ("came back", "kam zurück", "A2"),
    ("came forth", "kam hervor", "B2"),
    ("came out", "kam heraus", "A2"),
    ("go out", "hinausgehen", "A2"),
    ("go up", "hinaufgehen", "A2"),
    ("go down", "hinuntergehen", "A2"),
    ("go back", "zurückgehen", "A2"),
    ("went out", "ging hinaus", "A2"),
    ("went up", "ging hinauf", "A2"),
    ("went down", "ging hinunter", "A2"),
    ("went back", "ging zurück", "A2"),
    ("gone out", "hinausgegangen", "A2"),
    ("go forth", "hinausgehen", "B2"),
    ("goes forth", "geht hinaus", "B2"),
    ("going forth", "hinausgehend", "B2"),
    ("went forth", "ging hinaus", "B2"),
    ("gone forth", "hinausgegangen", "B2"),
    ("look at", "ansehen", "A2"),
    ("look for", "suchen", "A2"),
    ("look after", "sich kümmern um", "B1"),
    ("looked at", "sah an", "A2"),
    ("looked for", "suchte", "A2"),
    ("cut off", "abschneiden", "B1"),
    ("cut down", "fällen", "B1"),
    ("break down", "niederreißen", "B2"),
    ("break off", "abbrechen", "B2"),
    ("break out", "ausbrechen", "B2"),
    ("broke down", "riss nieder", "B2"),
    ("broke off", "brach ab", "B2"),
    ("broke out", "brach aus", "B2"),
    ("lay down", "hinlegen", "B1"),
    ("laid down", "hingelegt", "B1"),
    ("throw away", "wegwerfen", "B1"),
    ("throw out", "hinauswerfen", "B1"),
    ("threw away", "warf weg", "B1"),
    ("threw out", "warf hinaus", "B1"),
    ("thrown away", "weggeworfen", "B1"),
    ("thrown out", "hinausgeworfen", "B1"),
    ("pick up", "aufheben", "A2"),
    ("picked up", "hob auf", "A2"),
    ("cry out", "ausrufen", "B1"),
    ("cries out", "ruft aus", "B1"),
    ("crying out", "ausrufend", "B1"),
    ("cried out", "rief aus", "B1"),
    ("call out", "ausrufen", "B1"),
    ("called out", "rief aus", "B1"),
    ("call upon", "anrufen", "B2"),
    ("called upon", "rief an", "B2"),
    ("pass by", "vorübergehen", "B1"),
    ("pass over", "hinübergehen", "B2"),
    ("pass through", "hindurchgehen", "B1"),
    ("pass away", "vergehen", "B2"),
    ("passed by", "ging vorüber", "B1"),
    ("passed over", "ging hinüber", "B2"),
    ("passed through", "ging hindurch", "B1"),
    ("passed away", "verging", "B2"),
    ("find out", "herausfinden", "B1"),
    ("found out", "herausgefunden", "B1"),
    ("reach out", "ausstrecken", "B1"),
    ("reached out", "streckte aus", "B1"),
    ("stretch out", "ausstrecken", "B1"),
    ("stretches out", "streckt aus", "B1"),
    ("stretching out", "ausstreckend", "B1"),
    ("stretched out", "streckte aus", "B1"),
    ("wipe out", "auslöschen", "B2"),
    ("wiped out", "ausgelöscht", "B2"),
    ("blot out", "auslöschen", "C1"),
    ("blotted out", "ausgelöscht", "C1"),
    ("pour out", "ausgießen", "B1"),
    ("pours out", "gießt aus", "B1"),
    ("pouring out", "ausgießend", "B1"),
    ("poured out", "ausgegossen", "B1"),
    ("drive out", "vertreiben", "B2"),
    ("drives out", "treibt aus", "B2"),
    ("driving out", "austreibend", "B2"),
    ("drove out", "vertrieb", "B2"),
    ("driven out", "vertrieben", "B2"),
    ("shut up", "einschließen", "B2"),
    ("shut out", "ausschließen", "B2"),
    ("shuts out", "schließt aus", "B2"),
    ("rise up", "sich erheben", "B1"),
    ("rises up", "erhebt sich", "B1"),
    ("rising up", "sich erhebend", "B1"),
    ("rose up", "erhob sich", "B1"),
    ("risen up", "sich erhoben", "B1"),
    ("get up", "aufstehen", "A2"),
    ("got up", "stand auf", "A2"),
    ("stand up", "aufstehen", "A2"),
    ("stood up", "stand auf", "A2"),
    ("wake up", "aufwachen", "A2"),
    ("woke up", "wachte auf", "A2"),
    ("stir up", "aufwiegeln", "B2"),
    ("stirred up", "aufgewiegelt", "B2"),
    ("build up", "aufbauen", "B1"),
    ("built up", "aufgebaut", "B1"),
    ("tear down", "niederreißen", "B2"),
    ("tore down", "riss nieder", "B2"),
    ("torn down", "niedergerissen", "B2"),
    ("burn up", "verbrennen", "B1"),
    ("burned up", "verbrannte", "B1"),
    ("burnt up", "verbrannte", "B1"),
    ("burn down", "niederbrennen", "B1"),
    ("burned down", "brannte nieder", "B1"),
    ("dry up", "austrocknen", "B1"),
    ("dried up", "trocknete aus", "B1"),
    ("grow up", "aufwachsen", "A2"),
    ("grew up", "wuchs auf", "A2"),
    ("grown up", "aufgewachsen", "A2"),
    ("hold on", "festhalten", "B1"),
    ("held on", "hielt fest", "B1"),
    ("hold back", "zurückhalten", "B2"),
    ("held back", "hielt zurück", "B2"),
    ("hand over", "übergeben", "B1"),
    ("handed over", "übergeben", "B1"),
    ("give in", "nachgeben", "B2"),
    ("gave in", "gab nach", "B2"),
    ("run away", "weglaufen", "A2"),
    ("ran away", "lief weg", "A2"),
    ("bow down", "sich niederwerfen", "B2"),
    ("bows down", "wirft sich nieder", "B2"),
    ("bowing down", "sich niederwerfend", "B2"),
    ("bowed down", "warf sich nieder", "B2"),
    ("fall down", "niederfallen", "B1"),
    ("falls down", "fällt nieder", "B1"),
    ("falling down", "niederfallend", "B1"),
    ("fell down", "fiel nieder", "B1"),
    ("fallen down", "niedergefallen", "B1"),
    ("kneel down", "niederknien", "B1"),
    ("knelt down", "kniete nieder", "B1"),
    ("sit down", "sich setzen", "A2"),
    ("sat down", "setzte sich", "A2"),
    ("lie down", "sich hinlegen", "A2"),
    ("swear by", "schwören bei", "B2"),
    ("swore by", "schwor bei", "B2"),
    ("carry out", "ausführen", "B1"),
    ("carried out", "ausgeführt", "B1"),
    ("carry away", "wegtragen", "B2"),
    ("carried away", "weggetragen", "B2"),
    ("wipe away", "abwischen", "B1"),
    ("wiped away", "abgewischt", "B1"),
    ("wash away", "wegwaschen", "B1"),
    ("washed away", "weggewaschen", "B1"),
    ("give up", "aufgeben", "B1"),
    ("gave up", "gab auf", "B1"),
    ("given up", "aufgegeben", "B1"),
    ("fill up", "füllen", "B1"),
    ("filled up", "gefüllt", "B1"),
    ("speak up", "laut sprechen", "B1"),
    ("spoke up", "sprach laut", "B1"),
    ("tear apart", "zerreißen", "B2"),
    ("tore apart", "zerriss", "B2"),
    ("torn apart", "zerrissen", "B2"),
    ("lift up", "erheben", "B1"),
    ("lifts up", "erhebt", "B1"),
    ("lifting up", "erhebend", "B1"),
    ("lifted up", "erhob", "B1"),
    ("raised up", "aufgerichtet", "B1"),
    ("raise up", "aufrichten", "B1"),
    ("pulled out", "herausgezogen", "B1"),
    ("pull out", "herausziehen", "B1"),
    ("pull down", "niederreißen", "B2"),
    ("pulled down", "niedergerissen", "B2"),
    ("move away", "weggehen", "B1"),
    ("moved away", "ging weg", "B1"),
    ("carry off", "fortschleppen", "B2"),
    ("carried off", "fortgeschleppt", "B2"),
    ("draw near", "sich nähern", "B2"),
    ("drew near", "näherte sich", "B2"),
    ("drawn near", "genähert", "B2"),
    ("draw back", "zurückweichen", "B2"),
    ("drew back", "wich zurück", "B2"),
    ("shut in", "einschließen", "B2"),
    ("kept on", "weitermachen", "B1"),
    ("keep on", "weitermachen", "B1"),
    ("called on", "rief an", "B1"),
    ("watch over", "bewachen", "B1"),
    ("watched over", "bewachte", "B1"),
    ("rule over", "herrschen über", "B1"),
    ("ruled over", "herrschte über", "B1"),
    ("reign over", "regieren über", "B2"),
    ("reigned over", "regierte über", "B2"),
    ("triumph over", "triumphieren über", "B2"),
    ("triumphed over", "triumphierte über", "B2"),
    ("prevail over", "obsiegen über", "C1"),
    ("prevailed over", "obsiegte über", "C1"),
    ("preside over", "vorstehen", "C1"),

    # 2-word nouns / adjectives / adverbs
    ("burnt offering", "Brandopfer", "C2"),
    ("new moon", "Neumond", "B1"),
    ("full moon", "Vollmond", "B1"),
    ("wild beast", "wildes Tier", "B1"),
    ("wild beasts", "wilde Tiere", "B1"),
    ("wild animal", "wildes Tier", "B1"),
    ("wild animals", "wilde Tiere", "B1"),
    ("firstborn son", "erstgeborener Sohn", "B2"),
    ("promised land", "gelobtes Land", "B2"),
    ("chosen people", "auserwähltes Volk", "B2"),
    ("every day", "jeden Tag", "A2"),
    ("every night", "jede Nacht", "A2"),
    ("next day", "nächster Tag", "A2"),
    ("next morning", "nächster Morgen", "A2"),
    ("third day", "dritter Tag", "A2"),
    ("last day", "letzter Tag", "A2"),
    ("far away", "weit weg", "A2"),
    ("right away", "sofort", "B1"),
    ("at least", "mindestens", "A2"),
    ("at first", "zuerst", "A2"),
]

# Sort by phrase length (words) descending so longer matches take priority
PHRASES.sort(key=lambda x: -len(x[0].split()))


def load_bible_texts():
    """Load all verse texts keyed by (book_nr, chapter, verse)."""
    verses = {}
    for fname in os.listdir(BIBLE_DIR):
        if not fname.endswith('_web.json'):
            continue
        with open(os.path.join(BIBLE_DIR, fname)) as f:
            book = json.load(f)
        for ch in book['chapters']:
            for v in ch['verses']:
                verses[(book['nr'], ch['number'], v['n'])] = v['text']
    return verses


def scan_phrases(verses):
    """Scan Bible text for phrase occurrences, return counts and examples."""
    results = defaultdict(lambda: {'count': 0, 'examples': []})

    for (book_nr, chap, verse_n), text in verses.items():
        text_lower = text.lower()
        for phrase, de, level in PHRASES:
            pattern = re.compile(r'\b' + re.escape(phrase.lower()) + r'\b')
            for match in pattern.finditer(text_lower):
                key = (phrase, de, level)
                results[key]['count'] += 1
                if len(results[key]['examples']) < 2:
                    results[key]['examples'].append({
                        'ref': f'{book_nr}:{chap}:{verse_n}',
                        'text': text,
                        'match_start': match.start(),
                        'match_end': match.end()
                    })
    return results


def merge_annotations(ann_path, verses, dry_run=True):
    """Merge consecutive single-word annotations into multi-word phrases."""
    with open(ann_path) as f:
        data = json.load(f)

    merged_count = 0
    already_multi = 0
    details = []

    for book_nr_str, book_data in data.get('books', {}).items():
        if not isinstance(book_data, dict) or 'chapters' not in book_data:
            continue
        book_nr = int(book_nr_str)
        for chap_str, chap_data in book_data['chapters'].items():
            if not isinstance(chap_data, dict):
                continue
            chap = int(chap_str)
            for verse_str, words in chap_data.items():
                if not isinstance(words, list):
                    continue
                verse_n = int(verse_str)

                vkey = (book_nr, chap, verse_n)
                verse_text = verses.get(vkey, '')
                if not verse_text:
                    continue

                tokens = verse_text.split()

                for phrase, de, level in PHRASES:
                    phrase_words = phrase.lower().split()
                    phrase_len = len(phrase_words)

                    # Find phrase in tokens
                    for start_pos in range(len(tokens) - phrase_len + 1):
                        # Strip punctuation for matching
                        candidate = [re.sub(r'[^\w]', '', t).lower() for t in tokens[start_pos:start_pos+phrase_len]]
                        if candidate != phrase_words:
                            continue

                        end_pos = start_pos + phrase_len - 1

                        # Check if this span already has a multi-word annotation
                        existing_multi = [w for w in words if w.get('pos_end') is not None
                                         and w['pos'] == start_pos and w['pos_end'] == end_pos]
                        if existing_multi:
                            already_multi += 1
                            continue

                        # Find single-word annotations in this span
                        span_annos = [w for w in words if w.get('pos') is not None
                                     and 'pos_end' not in w
                                     and start_pos <= w['pos'] <= end_pos]

                        if not span_annos:
                            continue

                        # Create merged annotation
                        form = ' '.join(tokens[start_pos:start_pos+phrase_len])
                        # Clean trailing punctuation from last word
                        form_clean = re.sub(r'[.,;:!?"\')\]]+$', '', form)

                        merged = {
                            'pos': start_pos,
                            'pos_end': end_pos,
                            'form': form_clean,
                            'lemma': phrase,
                            'level': level,
                            'de': de
                        }

                        details.append({
                            'ref': f'{book_nr}:{chap}:{verse_n}',
                            'phrase': phrase,
                            'de': de,
                            'replaced': len(span_annos),
                            'text': verse_text[:80]
                        })

                        if not dry_run:
                            # Remove individual annotations in the span
                            for a in span_annos:
                                words.remove(a)
                            # Add merged annotation
                            words.append(merged)

                        merged_count += 1

    if not dry_run:
        with open(ann_path, 'w') as f:
            json.dump(data, f, ensure_ascii=False)

    return merged_count, already_multi, details


if __name__ == '__main__':
    import sys

    dry_run = '--apply' not in sys.argv

    print("Loading Bible texts...")
    verses = load_bible_texts()

    print(f"\nScanning {len(verses)} verses for {len(PHRASES)} phrases...")
    results = scan_phrases(verses)

    found = {k: v for k, v in results.items() if v['count'] > 0}
    found_sorted = sorted(found.items(), key=lambda x: -x[1]['count'])

    print(f"\n{'='*70}")
    print(f"Found {len(found_sorted)} phrases with {sum(v['count'] for v in found.values())} total occurrences")
    print(f"{'='*70}\n")

    for (phrase, de, level), info in found_sorted:
        print(f"  {info['count']:4d}x  [{level}] {phrase:30s} → {de}")

    # Now merge annotations
    print(f"\n{'='*70}")
    print(f"{'DRY RUN — ' if dry_run else ''}Merging annotations...")
    print(f"{'='*70}\n")

    for ann_file in ['nt_annotations_en.json', 'ot_annotations_en.json']:
        ann_path = os.path.join(BASE, ann_file)
        if not os.path.exists(ann_path):
            print(f"  Skipping {ann_file} (not found)")
            continue

        count, already, details = merge_annotations(ann_path, verses, dry_run=dry_run)
        print(f"  {ann_file}:")
        print(f"    {count} phrases to merge")
        print(f"    {already} already merged (skipped)")

        if details:
            print(f"    Examples:")
            for d in details[:10]:
                print(f"      {d['ref']} — \"{d['phrase']}\" → {d['de']} (replaced {d['replaced']} entries)")

    if dry_run:
        print(f"\n  This was a dry run. Use --apply to actually merge.")
    else:
        print(f"\n  Done! Annotations have been updated.")
