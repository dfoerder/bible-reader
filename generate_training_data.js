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

// Determine canonical level, de, and filter
const unified = [];

for (const [lemma, data] of Object.entries(lemmaData)) {
  const annoLevel = Object.entries(data.levelCounts).sort((a, b) => b[1] - a[1])[0][0];
  const de = Object.entries(data.deCounts).sort((a, b) => b[1] - a[1])[0][0];

  // Filter proper nouns: uppercase lemma where de is also capitalized (transliterated names)
  if (lemma[0] === lemma[0].toUpperCase() && lemma[0] !== lemma[0].toLowerCase()
      && de[0] === de[0].toUpperCase() && de[0] !== de[0].toLowerCase()) continue;

  // Determine level: use Oxford if available, otherwise annotation level
  const oxLevels = oxMap[lemma.toLowerCase()];
  let level = annoLevel;
  let isOxford = false;
  if (oxLevels) {
    // Use the Oxford level closest to our annotation level
    const LEVEL_ORDER = { A1: 0, A2: 1, B1: 2, B2: 3, C1: 4, C2: 5 };
    let bestOx = oxLevels[0];
    let bestDiff = Math.abs(LEVEL_ORDER[bestOx] - LEVEL_ORDER[annoLevel]);
    for (const ol of oxLevels) {
      const d = Math.abs(LEVEL_ORDER[ol] - LEVEL_ORDER[annoLevel]);
      if (d < bestDiff) { bestDiff = d; bestOx = ol; }
    }
    level = bestOx;
    isOxford = true;
  }

  unified.push({ lemma, level, annoLevel, de, freq: data.freq, occurrences: data.occurrences, isOxford });
}

// Split into Oxford words and Bible-specific words
const oxfordWords = unified.filter(w => w.isOxford);
const bibleWords = unified.filter(w => !w.isOxford);

console.log(`  Total: ${unified.length} (Oxford: ${oxfordWords.length}, Bible: ${bibleWords.length})`);

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

console.log('\nOxford word list:');
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
let changed = 0, unchanged = 0;
for (const w of oxfordWords) {
  if (w.level !== w.annoLevel) changed++;
  else unchanged++;
}
console.log(`\nOxford level adjustments: ${changed} changed, ${unchanged} unchanged`);

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
    .map(w => ({ en: w.lemma, de: w.de, sub: w.sub }));
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
    .map(w => ({ en: w.lemma, de: w.de, sub: w.sub }));
}
fs.writeFileSync('data/bible_vocab.json', JSON.stringify(biblePool));
console.log('  Written: data/bible_vocab.json');

// ── Final stats ──
console.log('\n=== Final statistics ===');
console.log('\nOxford vocabulary (general training):');
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
