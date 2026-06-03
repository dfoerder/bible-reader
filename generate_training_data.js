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

// ── Phase 1: Build unified lemma map from annotations ──
console.log('Phase 1: Scanning annotations...');

const lemmaData = {}; // lemma -> {levelCounts, deCounts, freq, occurrences}

fs.readdirSync(ANNO_DIR).filter(f => f.endsWith('.json')).sort().forEach(f => {
  const bookNr = parseInt(f.split('_')[0]);
  const anno = JSON.parse(fs.readFileSync(path.join(ANNO_DIR, f), 'utf8'));

  for (const [ch, verses] of Object.entries(anno.chapters || {})) {
    for (const [vn, anns] of Object.entries(verses)) {
      (anns || []).forEach(a => {
        if (a.pos_end != null) return; // skip multi-word
        if (a.phrase != null) return;  // skip phrase members
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
  const level = Object.entries(data.levelCounts).sort((a, b) => b[1] - a[1])[0][0];
  const de = Object.entries(data.deCounts).sort((a, b) => b[1] - a[1])[0][0];

  // Filter proper nouns: uppercase lemma where de is also capitalized (transliterated names)
  if (lemma[0] === lemma[0].toUpperCase() && lemma[0] !== lemma[0].toLowerCase()
      && de[0] === de[0].toUpperCase() && de[0] !== de[0].toLowerCase()) continue;

  unified.push({ lemma, level, de, freq: data.freq, occurrences: data.occurrences });
}

// Assign sublevels within each level by frequency
const byLevel = {};
LEVELS.forEach(l => { byLevel[l] = []; });
unified.forEach(w => byLevel[w.level].push(w));

for (const lvl of LEVELS) {
  byLevel[lvl].sort((a, b) => b.freq - a.freq || a.lemma.localeCompare(b.lemma));
  const total = byLevel[lvl].length;
  const third = Math.ceil(total / 3);
  byLevel[lvl].forEach((w, i) => {
    w.sub = i < third ? 1 : i < third * 2 ? 2 : 3;
  });
}

console.log('Unified word list:');
let totalWords = 0;
for (const lvl of LEVELS) {
  const s1 = byLevel[lvl].filter(w => w.sub === 1).length;
  const s2 = byLevel[lvl].filter(w => w.sub === 2).length;
  const s3 = byLevel[lvl].filter(w => w.sub === 3).length;
  console.log(`  ${lvl}: ${byLevel[lvl].length} (sub1=${s1}, sub2=${s2}, sub3=${s3})`);
  totalWords += byLevel[lvl].length;
}
console.log(`  Total: ${totalWords}`);

// ── Phase 2: Generate context_exercises.json ──
console.log('\nPhase 2: Generating context_exercises.json...');

// Load Bible texts (cached)
const textCache = {};
function loadText(bookNr) {
  if (textCache[bookNr]) return textCache[bookNr];
  const f = path.join(TEXT_DIR, `${bookNr}_web.json`);
  if (!fs.existsSync(f)) return null;
  const data = JSON.parse(fs.readFileSync(f, 'utf8'));
  // Normalize to dict format: {ch: {vn: text}}
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

  // Split into sentences
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

  // Skip direct speech intro
  const quoteIdx = targetSentence.search(/[“„«"]/);
  if (quoteIdx > 0 && quoteIdx < targetSentence.length / 2) {
    const before = targetSentence.slice(0, quoteIdx);
    const beforeWords = before.split(/\s+/).filter(w => w.length > 0).length;
    targetSentence = targetSentence.slice(quoteIdx);
    targetInSent -= beforeWords;
    if (targetInSent < 0) return null;
  }

  let sentWords = targetSentence.split(/\s+/);
  if (sentWords.length < 3) return null;

  // Truncate from end if too long
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

const exercises = {};
LEVELS.forEach(l => { exercises[l] = []; });
let noExercise = 0;

for (const w of unified) {
  // Find best occurrence: prefer verse closest to 15 words
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

    if (score === 0) break; // perfect match
  }

  if (bestExercise) {
    exercises[w.level].push(bestExercise);
  } else {
    noExercise++;
  }
}

fs.writeFileSync('data/context_exercises.json', JSON.stringify(exercises));
console.log('  Written: data/context_exercises.json');

// ── Phase 3: Generate vocab_pool.json (only words that have a cloze exercise) ──
console.log('\nPhase 3: Generating vocab_pool.json...');

const vocabPool = {};
for (const lvl of LEVELS) {
  const ceSet = new Set(exercises[lvl].map(e => e.lemma));
  vocabPool[lvl] = byLevel[lvl]
    .filter(w => ceSet.has(w.lemma))
    .map(w => ({ en: w.lemma, de: w.de, sub: w.sub }));
}
fs.writeFileSync('data/vocab_pool.json', JSON.stringify(vocabPool));
console.log('  Written: data/vocab_pool.json');

// ── Stats ──
console.log('\nFinal statistics:');
for (const lvl of LEVELS) {
  console.log(`  ${lvl}: vocab=${vocabPool[lvl].length}, cloze=${exercises[lvl].length}`);
}
if (noExercise > 0) {
  console.log(`  ${noExercise} lemmas without exercise (no suitable verse found)`);
}

// Verify overlap
let mismatch = 0;
for (const lvl of LEVELS) {
  const vpSet = new Set(vocabPool[lvl].map(w => w.en));
  const ceSet = new Set(exercises[lvl].map(e => e.lemma));
  vpSet.forEach(w => { if (!ceSet.has(w)) mismatch++; });
  ceSet.forEach(w => { if (!vpSet.has(w)) mismatch++; });
}
console.log(`  Mismatches between vocab pool and exercises: ${mismatch}`);
