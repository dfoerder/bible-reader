#!/usr/bin/env bash
set -e

# Auto-bump APP_VERSION, APP_DATE and sw.js cache version, then merge to main and push.
# Usage: ./deploy.sh [optional commit message suffix]

# ── Read current values ──
CURRENT_CACHE=$(grep -o 'bible-full-v[0-9]*' sw.js | grep -o '[0-9]*$')
CURRENT_VER=$(grep -o "APP_VERSION = '[^']*'" index.html | grep -o "'[^']*'" | tr -d "'")
NEW_CACHE=$((CURRENT_CACHE + 1))

# Bump minor version number (e.g. 1.9.58b → 1.9.59b)
BASE=$(echo "$CURRENT_VER" | sed "s/b$//")
MAJOR=$(echo "$BASE" | cut -d. -f1-2)
MINOR=$(echo "$BASE" | cut -d. -f3)
NEW_MINOR=$((MINOR + 1))
NEW_VER="${MAJOR}.${NEW_MINOR}b"

TODAY=$(date +"%d.%m.%Y")

echo "Cache:   bible-full-v${CURRENT_CACHE} → bible-full-v${NEW_CACHE}"
echo "Version: ${CURRENT_VER} → ${NEW_VER}"
echo "Date:    ${TODAY}"

# ── Apply changes ──
sed -i '' "s/bible-full-v${CURRENT_CACHE}/bible-full-v${NEW_CACHE}/" sw.js
sed -i '' "s/APP_VERSION = '${CURRENT_VER}'/APP_VERSION = '${NEW_VER}'/" index.html
sed -i '' "s/APP_DATE = '[^']*'/APP_DATE = '${TODAY}'/" index.html

# ── Commit ──
MSG="Deploy ${NEW_VER} — bump cache, version and date"
if [ -n "$1" ]; then MSG="$MSG ($1)"; fi

git add sw.js index.html
git commit -m "$MSG

Co-Authored-By: Claude Sonnet 4.6 (1M context) <noreply@anthropic.com>"

# ── Merge and push ──
git checkout main
git merge dev
git push origin main
git checkout dev

echo "✓ Deployed ${NEW_VER}"
