const fs = require('fs');
const path = require('path');

const ANNO_DIR = 'bibles/eng/web/anno';
const LEVELS = ['A1','A2','B1','B2','C1','C2'];
const LEVEL_ORDER = { A1: 0, A2: 1, B1: 2, B2: 3, C1: 4, C2: 5 };

// Load Oxford 5000
const oxLines = fs.readFileSync('oxford_5000.csv', 'utf8').split('\n').slice(1);
const oxMap = {};
for (const line of oxLines) {
  if (!line.trim()) continue;
  const match = line.match(/^\d+,([^,]+),[^,]+,([^,]+)/);
  if (!match) continue;
  const word = match[1].toLowerCase().trim();
  const level = match[2].toUpperCase().trim();
  if (!LEVELS.includes(level)) continue;
  if (!oxMap[word]) oxMap[word] = [];
  if (!oxMap[word].includes(level)) oxMap[word].push(level);
}

// Load Kaggle CEFR
const kagLines = fs.readFileSync('kaggle_cefr.csv', 'utf8').split('\n').slice(1);
const kagMap = {};
for (const line of kagLines) {
  if (!line.trim()) continue;
  const lastComma = line.lastIndexOf(',');
  const word = line.slice(0, lastComma).toLowerCase().trim();
  const level = line.slice(lastComma + 1).trim().toUpperCase();
  if (!LEVELS.includes(level)) continue;
  if (oxMap[word]) continue;
  if (!kagMap[word]) kagMap[word] = level;
}

// Load Opus CEFR levels
const opusMap = JSON.parse(fs.readFileSync('opus_cefr_levels.json', 'utf8'));

function getBestLevel(lemma, annoLevel) {
  const key = lemma.toLowerCase();
  const oxLevels = oxMap[key];
  if (oxLevels) {
    let best = oxLevels[0];
    let bestDiff = Math.abs(LEVEL_ORDER[best] - LEVEL_ORDER[annoLevel]);
    for (const ol of oxLevels) {
      const d = Math.abs(LEVEL_ORDER[ol] - LEVEL_ORDER[annoLevel]);
      if (d < bestDiff) { bestDiff = d; best = ol; }
    }
    return best;
  }
  if (kagMap[key]) return kagMap[key];
  if (opusMap[key]) return opusMap[key];
  return annoLevel;
}

// Process all annotation files
const files = fs.readdirSync(ANNO_DIR).filter(f => f.endsWith('.json') && !f.endsWith('.bak'));
let totalChanged = 0, totalAnnotations = 0;

for (const f of files) {
  const fpath = path.join(ANNO_DIR, f);
  const anno = JSON.parse(fs.readFileSync(fpath, 'utf8'));
  let fileChanged = 0;

  for (const [ch, verses] of Object.entries(anno.chapters || {})) {
    for (const [vn, anns] of Object.entries(verses)) {
      for (const a of (anns || [])) {
        if (!a.lemma || !a.level || !LEVELS.includes(a.level)) continue;
        totalAnnotations++;
        const newLevel = getBestLevel(a.lemma, a.level);
        if (newLevel !== a.level) {
          a.level = newLevel;
          fileChanged++;
        }
      }
    }
  }

  if (fileChanged > 0) {
    fs.writeFileSync(fpath, JSON.stringify(anno));
    totalChanged += fileChanged;
  }
  process.stdout.write(`  ${f}: ${fileChanged} changed\n`);
}

console.log(`\nTotal: ${totalChanged} of ${totalAnnotations} annotations updated`);
