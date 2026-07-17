const fs = require('fs');

// Load Oxford 5000
const oxLines = fs.readFileSync('oxford_5000.csv', 'utf8').split('\n').slice(1);
const oxMap = {}; // word -> Set of levels (some words appear multiple times with different POS)
for (const line of oxLines) {
  if (!line.trim()) continue;
  const match = line.match(/^\d+,([^,]+),[^,]+,([^,]+)/);
  if (!match) continue;
  const word = match[1].toLowerCase().trim();
  const level = match[2].toUpperCase().trim();
  if (!['A1','A2','B1','B2','C1'].includes(level)) continue;
  if (!oxMap[word]) oxMap[word] = new Set();
  oxMap[word].add(level);
}
console.log(`Oxford 5000: ${Object.keys(oxMap).length} unique words loaded\n`);

// Load our vocab pool
const vp = JSON.parse(fs.readFileSync('bibles/eng/web/train/vocab_pool.json', 'utf8'));
const LEVELS = ['A1','A2','B1','B2','C1','C2'];
const ourWords = [];
for (const lvl of LEVELS) {
  for (const w of (vp[lvl] || [])) {
    ourWords.push({ word: w.en.toLowerCase(), level: lvl, de: w.de });
  }
}
console.log(`Our vocab pool: ${ourWords.length} words\n`);

// Compare
const LEVEL_ORDER = { A1: 0, A2: 1, B1: 2, B2: 3, C1: 4, C2: 5 };
let matched = 0, exact = 0, close = 0, off = 0, notInOxford = 0;
const diffStats = {}; // "our->ox" -> count
const offByN = { 0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0 };
const examples = { tooEasy: [], tooHard: [], exact: [] };

for (const w of ourWords) {
  const oxLevels = oxMap[w.word];
  if (!oxLevels) {
    notInOxford++;
    continue;
  }
  matched++;

  // Use the closest Oxford level to our level
  const oxArr = [...oxLevels];
  let bestOx = oxArr[0];
  let bestDiff = Math.abs(LEVEL_ORDER[bestOx] - LEVEL_ORDER[w.level]);
  for (const ol of oxArr) {
    const d = Math.abs(LEVEL_ORDER[ol] - LEVEL_ORDER[w.level]);
    if (d < bestDiff) { bestDiff = d; bestOx = ol; }
  }

  const diff = LEVEL_ORDER[w.level] - LEVEL_ORDER[bestOx];
  offByN[Math.abs(diff)] = (offByN[Math.abs(diff)] || 0) + 1;

  if (diff === 0) {
    exact++;
  } else {
    const key = `${bestOx}->${w.level}`;
    diffStats[key] = (diffStats[key] || 0) + 1;
    if (Math.abs(diff) <= 1) close++;
    else off++;

    if (diff >= 2 && examples.tooHard.length < 10) {
      examples.tooHard.push(`  ${w.word} (${w.de}): Oxford=${bestOx}, Wir=${w.level}`);
    }
    if (diff <= -2 && examples.tooEasy.length < 10) {
      examples.tooEasy.push(`  ${w.word} (${w.de}): Oxford=${bestOx}, Wir=${w.level}`);
    }
  }
}

console.log('=== ERGEBNIS ===\n');
console.log(`Übereinstimmung gefunden: ${matched} von ${ourWords.length} Wörtern (${(matched/ourWords.length*100).toFixed(1)}%)`);
console.log(`Nicht in Oxford 5000:     ${notInOxford} (${(notInOxford/ourWords.length*100).toFixed(1)}%)\n`);

console.log('--- Level-Übereinstimmung (nur gematchte Wörter) ---');
console.log(`Exakt gleich:      ${exact} (${(exact/matched*100).toFixed(1)}%)`);
console.log(`±1 Level Abweichung: ${close} (${(close/matched*100).toFixed(1)}%)`);
console.log(`≥2 Level Abweichung: ${off} (${(off/matched*100).toFixed(1)}%)\n`);

console.log('--- Abweichung nach Stufen ---');
for (const [n, count] of Object.entries(offByN)) {
  if (count > 0) console.log(`  ±${n} Level: ${count} (${(count/matched*100).toFixed(1)}%)`);
}

console.log('\n--- Häufigste Level-Verschiebungen ---');
const sorted = Object.entries(diffStats).sort((a, b) => b[1] - a[1]);
for (const [key, count] of sorted.slice(0, 15)) {
  console.log(`  Oxford ${key.split('->')[0]} → Wir ${key.split('->')[1]}: ${count}`);
}

console.log('\n--- Aufschlüsselung nach unserem Level ---');
for (const lvl of LEVELS) {
  const lvlWords = ourWords.filter(w => w.level === lvl);
  const lvlMatched = lvlWords.filter(w => oxMap[w.word]);
  const lvlExact = lvlWords.filter(w => {
    const ox = oxMap[w.word];
    if (!ox) return false;
    return ox.has(lvl);
  });
  console.log(`  ${lvl}: ${lvlWords.length} Wörter, ${lvlMatched.length} in Oxford (${lvlExact.length} exakt gleich = ${lvlMatched.length ? (lvlExact.length/lvlMatched.length*100).toFixed(0) : 0}%)`);
}

if (examples.tooHard.length > 0) {
  console.log('\n--- Beispiele: Bei uns schwerer als Oxford (≥2 Level) ---');
  examples.tooHard.forEach(e => console.log(e));
}
if (examples.tooEasy.length > 0) {
  console.log('\n--- Beispiele: Bei uns leichter als Oxford (≥2 Level) ---');
  examples.tooEasy.forEach(e => console.log(e));
}
