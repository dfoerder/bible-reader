#!/bin/bash
# Spiegelt die Web-App aus dem Repo-Root in das Capacitor-Bundle www/ und
# synct anschließend nach ios/. Root ist die EINZIGE Quelle — www/ und ios/
# sind reine Ableitungen und werden NIE von Hand bearbeitet.
#
#   ./sync_www.sh        normales Spiegeln + cap sync
#   ./sync_www.sh --no-cap   nur nach www/ spiegeln (ohne npx cap sync)
#
set -euo pipefail
cd "$(dirname "$0")"

# Runtime-Assets, die die Web-App braucht (vgl. www/-Top-Level)
FILES=(index.html sw.js manifest.json icon-192.png icon-512.png)
DIRS=(data bibles lib)

mkdir -p www

echo "→ Dateien spiegeln nach www/"
for f in "${FILES[@]}"; do
  cp -p "$f" "www/$f"
  echo "  $f"
done

echo "→ Verzeichnisse spiegeln nach www/ (rsync --delete)"
for d in "${DIRS[@]}"; do
  rsync -a --delete "$d/" "www/$d/"
  echo "  $d/"
done

if [[ "${1:-}" == "--no-cap" ]]; then
  echo "✓ www/ aktualisiert (cap sync übersprungen)"
  exit 0
fi

echo "→ npx cap sync (www/ → ios/)"
npx cap sync

echo "✓ Sync abgeschlossen: root → www/ → ios/"
