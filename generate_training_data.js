const fs = require('fs');
const path = require('path');

const ANNO_DIR = 'bibles/eng/web/anno';
const TEXT_DIR = 'bibles/eng/web';
const INDEX_FILE = 'bibles/index.json';
const LEVELS = ['A1','A2','B1','B2','C1','C2'];

// ── Load book metadata ──
const index = JSON.parse(fs.readFileSync(INDEX_FILE, 'utf8'));
const bookMap = {};
index.books.forEach(b => { bookMap[b.nr] = b.name; });

// ── Load Oxford 5000 ──
console.log('Loading Oxford 5000...');
const oxLines = fs.readFileSync('oxford_5000.csv', 'utf8').split('\n').slice(1);
const oxMap = {};
for (const line of oxLines) {
  if (!line.trim()) continue;
  const match = line.match(/^\d+,([^,]+),[^,]+,([^,]+)/);
  if (!match) continue;
  const word = match[1].toLowerCase().trim();
  const level = match[2].toUpperCase().trim();
  if (!['A1','A2','B1','B2','C1'].includes(level)) continue;
  if (!oxMap[word]) oxMap[word] = [];
  if (!oxMap[word].includes(level)) oxMap[word].push(level);
}
console.log(`  ${Object.keys(oxMap).length} unique Oxford words loaded`);

// ── Load Kaggle CEFR (secondary reference) ──
console.log('Loading Kaggle CEFR...');
const kagLines = fs.readFileSync('kaggle_cefr.csv', 'utf8').split('\n').slice(1);
const kagMap = {};
for (const line of kagLines) {
  if (!line.trim()) continue;
  const lastComma = line.lastIndexOf(',');
  const word = line.slice(0, lastComma).toLowerCase().trim();
  const level = line.slice(lastComma + 1).trim().toUpperCase();
  if (!['A1','A2','B1','B2','C1','C2'].includes(level)) continue;
  if (oxMap[word]) continue;
  if (!kagMap[word]) kagMap[word] = level;
}
console.log(`  ${Object.keys(kagMap).length} unique Kaggle words loaded (excluding Oxford)`);

// ── Phase 1: Build unified lemma map from annotations ──
console.log('\nPhase 1: Scanning annotations...');

const lemmaData = {};

fs.readdirSync(ANNO_DIR).filter(f => f.endsWith('.json')).sort().forEach(f => {
  const bookNr = parseInt(f.split('_')[0]);
  const anno = JSON.parse(fs.readFileSync(path.join(ANNO_DIR, f), 'utf8'));

  for (const [ch, verses] of Object.entries(anno.chapters || {})) {
    for (const [vn, anns] of Object.entries(verses)) {
      (anns || []).forEach(a => {
        if (a.pos_end != null) return;
        if (a.phrase != null) return;
        if (!a.lemma || !a.level || !a.de) return;
        if (!LEVELS.includes(a.level)) return;

        const lem = a.lemma;
        if (!lemmaData[lem]) {
          lemmaData[lem] = { levelCounts: {}, deCounts: {}, freq: 0, occurrences: [] };
        }
        const d = lemmaData[lem];
        d.levelCounts[a.level] = (d.levelCounts[a.level] || 0) + 1;
        d.deCounts[a.de] = (d.deCounts[a.de] || 0) + 1;
        d.freq++;
        d.occurrences.push({ bookNr, ch: parseInt(ch), vn: parseInt(vn), pos: a.pos, form: a.form, de: a.de });
      });
    }
  }
});

// Merge case variants: "After" + "after" → "after" (keep lowercase as canonical)
const merged = {};
for (const [lem, data] of Object.entries(lemmaData)) {
  const key = lem.toLowerCase();
  if (!merged[key]) {
    merged[key] = { levelCounts: {}, deCounts: {}, freq: 0, occurrences: [], originalCasings: [] };
  }
  const m = merged[key];
  for (const [lvl, cnt] of Object.entries(data.levelCounts)) m.levelCounts[lvl] = (m.levelCounts[lvl] || 0) + cnt;
  for (const [de, cnt] of Object.entries(data.deCounts)) m.deCounts[de] = (m.deCounts[de] || 0) + cnt;
  m.freq += data.freq;
  m.occurrences.push(...data.occurrences);
  m.originalCasings.push(lem);
}
// Use original casing with most occurrences for proper noun detection
const lemmaDataMerged = {};
for (const [key, data] of Object.entries(merged)) {
  const bestCasing = data.originalCasings.sort((a, b) => {
    const freqA = lemmaData[a].freq, freqB = lemmaData[b].freq;
    return freqB - freqA;
  })[0];
  lemmaDataMerged[key] = { ...data, displayLemma: bestCasing };
}

// Determine canonical level, de, and filter
// Build general set (Oxford + Kaggle) for inflection checks
const oxLemmaSet = new Set([...Object.keys(oxMap), ...Object.keys(kagMap)]);

const IRREGULAR_MAP = {
  those:'that',these:'this',women:'woman',men:'man',children:'child',
  feet:'foot',teeth:'tooth',mice:'mouse',geese:'goose',oxen:'ox',
  was:'be',were:'be',been:'be',am:'be',is:'be',are:'be',
  had:'have',has:'have',did:'do',does:'do',doesnt:'do',dont:'do',
  went:'go',gone:'go',came:'come',took:'take',gave:'give',
  said:'say',told:'tell',made:'make',got:'get',saw:'see',
  knew:'know',known:'know',ran:'run',sat:'sit',stood:'stand',
  fell:'fall',fallen:'fall',kept:'keep',led:'lead',left:'leave',
  built:'build',sent:'send',spent:'spend',lost:'lose',found:'find',
  brought:'bring',thought:'think',bought:'buy',caught:'catch',
  taught:'teach',wrote:'write',written:'write',spoke:'speak',
  broke:'break',broken:'break',chose:'choose',chosen:'choose',
  drove:'drive',drove:'drive',ate:'eat',eaten:'eat',
  threw:'throw',thrown:'throw',drew:'draw',grew:'grow',grew:'grow',
  wore:'wear',worn:'wear',bore:'bear',born:'bear',
  began:'begin',begun:'begin',sang:'sing',sung:'sing',
  drank:'drink',drunk:'drink',swam:'swim',swore:'swear',
  woke:'wake',woken:'wake',shook:'shake',hid:'hide',hidden:'hide',
  laid:'lay',paid:'pay',held:'hold',hung:'hang',dug:'dig',
  bound:'bind',wound:'wind',lit:'light',set:'set',
  worse:'bad',worst:'bad',better:'good',best:'good',
  more:'much',most:'much',less:'little',least:'little',
  further:'far',furthest:'far',
};

function isInflectedOxford(word) {
  const lw = word.toLowerCase();
  if (oxLemmaSet.has(lw)) return false;
  if (IRREGULAR_MAP[lw] && oxLemmaSet.has(IRREGULAR_MAP[lw])) return true;
  // US→UK spelling variants
  if (lw.endsWith('or') && oxLemmaSet.has(lw.slice(0,-2)+'our')) return true;
  if (lw.endsWith('ior') && oxLemmaSet.has(lw.slice(0,-3)+'iour')) return true;
  if (lw.includes('bor') && oxLemmaSet.has(lw.replace('bor','bour'))) return true;
  if (lw.includes('vor') && oxLemmaSet.has(lw.replace('vor','vour'))) return true;
  if (lw.endsWith('ize') && oxLemmaSet.has(lw.slice(0,-3)+'ise')) return true;
  if (lw.endsWith('ized') && oxLemmaSet.has(lw.slice(0,-4)+'ised')) return true;
  if (!lw.endsWith('eed') && lw.endsWith('ed') && oxLemmaSet.has(lw.replace(/(?<=\w)ed$/, 'sed'))) return true;
  if (oxLemmaSet.has(lw.replace(/(?<=\w)e$/, 'ae'))) return true;
  // Base form where Oxford has the -d/-ed/-ing form
  if (oxLemmaSet.has(lw+'d') || oxLemmaSet.has(lw+'ed') || oxLemmaSet.has(lw+'ing')) return true;
  const bases = [];
  if (lw.endsWith('s') && lw.length > 2) bases.push(lw.slice(0, -1));
  if (lw.endsWith('es') && lw.length > 3) bases.push(lw.slice(0, -2));
  if (lw.endsWith('ies') && lw.length > 4) bases.push(lw.slice(0, -3) + 'y');
  if (lw.endsWith('ed') && lw.length > 3) bases.push(lw.slice(0, -2), lw.slice(0, -1));
  if (lw.endsWith('ied') && lw.length > 4) bases.push(lw.slice(0, -3) + 'y');
  if (lw.endsWith('ing') && lw.length > 4) bases.push(lw.slice(0, -3), lw.slice(0, -3) + 'e');
  if (lw.endsWith('er') && lw.length > 3) bases.push(lw.slice(0, -2), lw.slice(0, -1));
  if (lw.endsWith('ier') && lw.length > 4) bases.push(lw.slice(0, -3) + 'y');
  if (lw.endsWith('est') && lw.length > 4) bases.push(lw.slice(0, -3), lw.slice(0, -2));
  if (lw.endsWith('ly') && lw.length > 3) bases.push(lw.slice(0, -2));
  if (lw.endsWith('n') && lw.length > 3) bases.push(lw.slice(0, -1), lw.slice(0, -2));
  if (lw.endsWith('en') && lw.length > 3) bases.push(lw.slice(0, -2));
  if (lw.endsWith('th') && lw.length > 4) bases.push(lw.slice(0, -2));
  if (lw.endsWith('ieth') && lw.length > 5) bases.push(lw.slice(0, -4) + 'y');
  // Derivation suffixes
  if (lw.endsWith('ness') && lw.length > 5) { bases.push(lw.slice(0, -4)); if (lw.endsWith('iness')) bases.push(lw.slice(0, -5) + 'y'); }
  if (lw.endsWith('ful') && lw.length > 4) bases.push(lw.slice(0, -3));
  if (lw.endsWith('less') && lw.length > 5) bases.push(lw.slice(0, -4));
  if (lw.endsWith('ment') && lw.length > 5) bases.push(lw.slice(0, -4), lw.slice(0, -4) + 'e');
  if (lw.endsWith('ity') && lw.length > 5) bases.push(lw.slice(0, -3), lw.slice(0, -3) + 'e');
  if (lw.endsWith('ous') && lw.length > 5) bases.push(lw.slice(0, -3), lw.slice(0, -3) + 'e');
  if (lw.endsWith('ings') && lw.length > 5) bases.push(lw.slice(0, -4));
  if (lw.endsWith('y') && !lw.endsWith('ly') && lw.length > 3) bases.push(lw.slice(0, -1), lw.slice(0, -1) + 'e');
  // Compound: sun+rise, grand+child etc. (both parts ≥ 3 letters)
  const NOT_COMPOUND = new Set(['forsake','bondage','bandage','perverse','perversion','winnow',
    'hissing','appease','endanger','barbed','flatten','fatten','reddish','forego','herbage',
    'tillage','perchance','dragnet','wayward','offset','penknife','godhead','capstone',
    'boxwood','frontlet','armlet','inkhorn','forbear']);
  if (!NOT_COMPOUND.has(lw)) {
    for (let i = 3; i <= lw.length - 3; i++) {
      if (oxLemmaSet.has(lw.slice(0,i)) && oxLemmaSet.has(lw.slice(i))) return true;
    }
  }
  return bases.some(b => b.length >= 2 && oxLemmaSet.has(b));
}

function isNameLike(en, de) {
  const le = en.toLowerCase().replace(/[^a-z]/g, '').replace(/^y/,'j');
  const ld = de.toLowerCase().replace(/[^a-zäöüß]/g, '');
  if (le.length < 3 || ld.length < 3) return false;
  const prefix = Math.min(3, le.length, ld.length);
  return le.slice(0, prefix) === ld.slice(0, prefix) && Math.abs(le.length - ld.length) <= 3;
}

const unified = [];
let filterStats = { properNoun: 0, space: 0, special: 0, short: 0, compoundNum: 0, noTrans: 0, contraction: 0, caseVariant: 0, partial: 0, inflected: 0, nameAdj: 0, name: 0 };

for (const [lemma, data] of Object.entries(lemmaDataMerged)) {
  const annoLevel = Object.entries(data.levelCounts).sort((a, b) => b[1] - a[1])[0][0];
  const de = Object.entries(data.deCounts).sort((a, b) => b[1] - a[1])[0][0];
  const origLemma = data.displayLemma;

  // Filter proper nouns: uppercase lemma where de is also capitalized
  if (origLemma[0] === origLemma[0].toUpperCase() && origLemma[0] !== origLemma[0].toLowerCase()
      && de[0] === de[0].toUpperCase() && de[0] !== de[0].toLowerCase()) { filterStats.properNoun++; continue; }

  // Determine level: Oxford > Kaggle > annotation level
  const oxLevels = oxMap[lemma];
  const kagLevel = kagMap[lemma];
  let level = annoLevel;
  let isGeneral = false;
  if (oxLevels) {
    const LEVEL_ORDER = { A1: 0, A2: 1, B1: 2, B2: 3, C1: 4, C2: 5 };
    let bestOx = oxLevels[0];
    let bestDiff = Math.abs(LEVEL_ORDER[bestOx] - LEVEL_ORDER[annoLevel]);
    for (const ol of oxLevels) {
      const d = Math.abs(LEVEL_ORDER[ol] - LEVEL_ORDER[annoLevel]);
      if (d < bestDiff) { bestDiff = d; bestOx = ol; }
    }
    level = bestOx;
    isGeneral = true;
  } else if (kagLevel) {
    level = kagLevel;
    isGeneral = true;
  }

  // Additional filters for Bible-only words (not in Oxford or Kaggle)
  if (!isGeneral) {
    if (lemma.includes(' ')) { filterStats.space++; continue; }
    if (/[+—\/\*]/.test(lemma) || /^\d+$/.test(lemma)) { filterStats.special++; continue; }
    if (lemma.length <= 2) { filterStats.short++; continue; }
    if (/\b(twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred)\b/i.test(lemma) && lemma.includes('-')) { filterStats.compoundNum++; continue; }
    if (de.toLowerCase() === lemma.toLowerCase()) { filterStats.noTrans++; continue; }
    if (/[''']/.test(lemma)) { filterStats.contraction++; continue; }
    if (lemma !== lemma.toLowerCase()) { filterStats.caseVariant++; continue; }
    if (de.endsWith('-')) { filterStats.partial++; continue; }
    if (isInflectedOxford(lemma)) { filterStats.inflected++; continue; }
    if (/^(yourselves|ourselves|ourself|himself|herself|itself|themselves|myself|oneself)$/.test(lemma)) { filterStats.inflected++; continue; }
    if (/^(jewish|christian|egyptian|roman|greek|hebrew|persian|assyrian|babylonian|philistine|levitical|italian|caesar)$/i.test(lemma)) { filterStats.nameAdj++; continue; }
    if (isNameLike(lemma, de)) { filterStats.name++; continue; }
    if (oxLemmaSet.has(lemma.replace(/-/g, ''))) { filterStats.inflected++; continue; }
  }

  unified.push({ lemma, level, annoLevel, de, freq: data.freq, occurrences: data.occurrences, isGeneral });
}

console.log('Filters applied (non-Oxford):');
Object.entries(filterStats).forEach(([k, v]) => { if (v > 0) console.log(`  ${k}: ${v}`); });

// Split into general words (Oxford + Kaggle) and Bible-specific words
const oxfordWords = unified.filter(w => w.isGeneral);
const bibleWords = unified.filter(w => !w.isGeneral);

console.log(`  Total: ${unified.length} (General: ${oxfordWords.length}, Bible: ${bibleWords.length})`);

// ── Assign sublevels within each level by frequency ──
function assignSublevels(words) {
  const byLevel = {};
  LEVELS.forEach(l => { byLevel[l] = []; });
  words.forEach(w => byLevel[w.level].push(w));

  for (const lvl of LEVELS) {
    byLevel[lvl].sort((a, b) => b.freq - a.freq || a.lemma.localeCompare(b.lemma));
    const total = byLevel[lvl].length;
    const third = Math.ceil(total / 3);
    byLevel[lvl].forEach((w, i) => {
      w.sub = i < third ? 1 : i < third * 2 ? 2 : 3;
    });
  }
  return byLevel;
}

const oxByLevel = assignSublevels(oxfordWords);
const biByLevel = assignSublevels(bibleWords);

const oxOnlyCount = oxfordWords.filter(w => oxMap[w.lemma]).length;
const kagOnlyCount = oxfordWords.filter(w => !oxMap[w.lemma]).length;
console.log(`\nGeneral word list (Oxford ${oxOnlyCount} + Kaggle ${kagOnlyCount}):`);
let oxTotal = 0;
for (const lvl of LEVELS) {
  if (oxByLevel[lvl].length > 0) {
    console.log(`  ${lvl}: ${oxByLevel[lvl].length}`);
    oxTotal += oxByLevel[lvl].length;
  }
}
console.log(`  Total: ${oxTotal}`);

console.log('\nBible word list:');
let biTotal = 0;
for (const lvl of LEVELS) {
  if (biByLevel[lvl].length > 0) {
    console.log(`  ${lvl}: ${biByLevel[lvl].length}`);
    biTotal += biByLevel[lvl].length;
  }
}
console.log(`  Total: ${biTotal}`);

// Show level changes
let oxChanged = 0, oxUnchanged = 0;
for (const w of oxfordWords) {
  if (w.level !== w.annoLevel) oxChanged++;
  else oxUnchanged++;
}
console.log(`\nGeneral pool level adjustments: ${oxChanged} changed, ${oxUnchanged} unchanged`);

// ── Shared: Load Bible texts and extract cloze ──

const textCache = {};
function loadText(bookNr) {
  if (textCache[bookNr]) return textCache[bookNr];
  const f = path.join(TEXT_DIR, `${bookNr}_web.json`);
  if (!fs.existsSync(f)) return null;
  const data = JSON.parse(fs.readFileSync(f, 'utf8'));
  const chapters = {};
  if (Array.isArray(data.chapters)) {
    data.chapters.forEach(ch => {
      chapters[ch.number] = {};
      (ch.verses || []).forEach(v => { chapters[ch.number][v.n] = v.text; });
    });
  } else if (data.chapters) {
    for (const [ch, verses] of Object.entries(data.chapters)) {
      chapters[ch] = {};
      if (Array.isArray(verses)) {
        verses.forEach(v => { chapters[ch][v.n] = v.text; });
      } else {
        Object.assign(chapters[ch], verses);
      }
    }
  }
  textCache[bookNr] = chapters;
  return chapters;
}

function extractCloze(verseText, pos, form) {
  const words = verseText.split(/\s+/);
  if (pos >= words.length) return null;

  const sentences = verseText.split(/(?<=[.!?…;:])\s+/);
  let targetSentence = null;
  let sentOffset = 0;
  let targetInSent = -1;

  for (const sent of sentences) {
    const sw = sent.split(/\s+/);
    if (pos >= sentOffset && pos < sentOffset + sw.length) {
      targetSentence = sent;
      targetInSent = pos - sentOffset;
      break;
    }
    sentOffset += sw.length;
  }
  if (!targetSentence || targetInSent < 0) return null;

  const quoteIdx = targetSentence.search(/["„«"]/);
  if (quoteIdx > 0 && quoteIdx < targetSentence.length / 2) {
    const before = targetSentence.slice(0, quoteIdx);
    const beforeWords = before.split(/\s+/).filter(w => w.length > 0).length;
    targetSentence = targetSentence.slice(quoteIdx);
    targetInSent -= beforeWords;
    if (targetInSent < 0) return null;
  }

  let sentWords = targetSentence.split(/\s+/);
  if (sentWords.length < 3) return null;

  const MAX = 15;
  if (sentWords.length > MAX) {
    const end = Math.max(MAX, targetInSent + 2);
    sentWords = sentWords.slice(0, end);
    sentWords[sentWords.length - 1] = sentWords[sentWords.length - 1].replace(/[.!?;,]*$/, '') + ' …';
  }

  if (targetInSent >= sentWords.length) return null;
  sentWords[targetInSent] = '___';
  const text = sentWords.join(' ');
  if (!text.includes('___')) return null;
  return text;
}

function generateExercises(wordList) {
  const exercises = {};
  LEVELS.forEach(l => { exercises[l] = []; });
  let noExercise = 0;

  for (const w of wordList) {
    let bestScore = Infinity;
    let bestExercise = null;

    for (const occ of w.occurrences) {
      const chapters = loadText(occ.bookNr);
      if (!chapters) continue;
      const chData = chapters[occ.ch];
      if (!chData) continue;
      const verseText = chData[occ.vn];
      if (!verseText) continue;

      const wordCount = verseText.split(/\s+/).length;
      if (wordCount < 5) continue;

      const text = extractCloze(verseText, occ.pos, occ.form);
      if (!text) continue;

      const score = Math.abs(wordCount - 15);
      if (score < bestScore) {
        bestScore = score;
        const bookName = bookMap[occ.bookNr] || `Book ${occ.bookNr}`;
        bestExercise = {
          text,
          answer: occ.form,
          de: w.de,
          lemma: w.lemma,
          ref: `${bookName} ${occ.ch}:${occ.vn}`,
          book: occ.bookNr,
          sub: w.sub
        };
      }

      if (score === 0) break;
    }

    if (bestExercise) {
      exercises[w.level].push(bestExercise);
    } else {
      noExercise++;
    }
  }
  return { exercises, noExercise };
}

// ── Phase 2: Generate Oxford exercises ──
console.log('\nPhase 2: Generating Oxford context exercises...');
const { exercises: oxExercises, noExercise: oxNoEx } = generateExercises(oxfordWords);
fs.writeFileSync('data/context_exercises.json', JSON.stringify(oxExercises));
console.log('  Written: data/context_exercises.json');

// ── Phase 3: Generate Oxford vocab pool ──
console.log('\nPhase 3: Generating Oxford vocab pool...');
const vocabPool = {};
for (const lvl of LEVELS) {
  const ceSet = new Set(oxExercises[lvl].map(e => e.lemma));
  vocabPool[lvl] = oxByLevel[lvl]
    .filter(w => ceSet.has(w.lemma))
    .map(w => ({ en: w.lemma, de: w.de, sub: w.sub, occ: w.freq }));
}
fs.writeFileSync('data/vocab_pool.json', JSON.stringify(vocabPool));
console.log('  Written: data/vocab_pool.json');

// ── Phase 4: Generate Bible vocab exercises ──
console.log('\nPhase 4: Generating Bible vocabulary...');
const { exercises: biExercises, noExercise: biNoEx } = generateExercises(bibleWords);
fs.writeFileSync('data/bible_exercises.json', JSON.stringify(biExercises));
console.log('  Written: data/bible_exercises.json');

// ── Phase 5: Generate Bible vocab pool ──
console.log('\nPhase 5: Generating Bible vocab pool...');
const biblePool = {};
for (const lvl of LEVELS) {
  const ceSet = new Set(biExercises[lvl].map(e => e.lemma));
  biblePool[lvl] = biByLevel[lvl]
    .filter(w => ceSet.has(w.lemma))
    .map(w => ({ en: w.lemma, de: w.de, sub: w.sub, occ: w.freq }));
}
fs.writeFileSync('data/bible_vocab.json', JSON.stringify(biblePool));
console.log('  Written: data/bible_vocab.json');

// ── Final stats ──
console.log('\n=== Final statistics ===');
console.log('\nGeneral vocabulary (Oxford + Kaggle):');
for (const lvl of LEVELS) {
  if (vocabPool[lvl].length > 0 || oxExercises[lvl].length > 0)
    console.log(`  ${lvl}: vocab=${vocabPool[lvl].length}, cloze=${oxExercises[lvl].length}`);
}
console.log(`  Total: vocab=${Object.values(vocabPool).flat().length}, cloze=${Object.values(oxExercises).flat().length}`);
if (oxNoEx > 0) console.log(`  ${oxNoEx} without exercise`);

console.log('\nBible vocabulary (separate training):');
for (const lvl of LEVELS) {
  if (biblePool[lvl].length > 0 || biExercises[lvl].length > 0)
    console.log(`  ${lvl}: vocab=${biblePool[lvl].length}, cloze=${biExercises[lvl].length}`);
}
console.log(`  Total: vocab=${Object.values(biblePool).flat().length}, cloze=${Object.values(biExercises).flat().length}`);
if (biNoEx > 0) console.log(`  ${biNoEx} without exercise`);

// Verify 0 mismatches
let mismatch = 0;
for (const lvl of LEVELS) {
  const vpSet = new Set(vocabPool[lvl].map(w => w.en));
  const ceSet = new Set(oxExercises[lvl].map(e => e.lemma));
  vpSet.forEach(w => { if (!ceSet.has(w)) mismatch++; });
  ceSet.forEach(w => { if (!vpSet.has(w)) mismatch++; });
}
for (const lvl of LEVELS) {
  const vpSet = new Set(biblePool[lvl].map(w => w.en));
  const ceSet = new Set(biExercises[lvl].map(e => e.lemma));
  vpSet.forEach(w => { if (!ceSet.has(w)) mismatch++; });
  ceSet.forEach(w => { if (!vpSet.has(w)) mismatch++; });
}
console.log(`\nTotal mismatches: ${mismatch}`);
