#!/usr/bin/env bash
set -e

# Auto-bump APP_VERSION, APP_DATE and sw.js cache version, write changelog
# entry to projekt-log.md, update version header in dokumentation.md,
# then merge to main and push.
# Usage: ./deploy.sh "Changelog-Zeile (was wurde geändert)"

if [ -z "$1" ]; then
  echo "Fehler: Changelog-Zeile fehlt."
  echo "Usage: ./deploy.sh \"Was wurde geändert\""
  exit 1
fi
CHANGELOG="$1"

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

echo "Cache:     bible-full-v${CURRENT_CACHE} → bible-full-v${NEW_CACHE}"
echo "Version:   ${CURRENT_VER} → ${NEW_VER}"
echo "Date:      ${TODAY}"
echo "Changelog: ${CHANGELOG}"

# ── Apply changes ──
sed -i '' "s/bible-full-v${CURRENT_CACHE}/bible-full-v${NEW_CACHE}/" sw.js
sed -i '' "s/APP_VERSION = '${CURRENT_VER}'/APP_VERSION = '${NEW_VER}'/" index.html
sed -i '' "s/APP_DATE = '[^']*'/APP_DATE = '${TODAY}'/" index.html

# Versionskopf in dokumentation.md aktuell halten
sed -i '' "s/^- \*\*Aktuelle Version:\*\* .*/- **Aktuelle Version:** ${NEW_VER} (${TODAY})/" dokumentation.md

# Changelog-Eintrag vor dem ersten Versions-Abschnitt in projekt-log.md einfügen
awk -v ver="$NEW_VER" -v today="$TODAY" -v msg="$CHANGELOG" '
  !done && /^## v/ { print "## v" ver " (" today ")\n\n- " msg "\n"; done=1 }
  { print }
' projekt-log.md > projekt-log.md.tmp && mv projekt-log.md.tmp projekt-log.md

# ── Commit ──
git add sw.js index.html dokumentation.md projekt-log.md
git commit -m "Deploy ${NEW_VER} — ${CHANGELOG}

Co-Authored-By: Claude Code <noreply@anthropic.com>"

# ── Merge and push ──
git checkout main
git merge dev
git push origin main
git checkout dev

echo "✓ Deployed ${NEW_VER}"
