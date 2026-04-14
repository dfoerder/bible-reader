#!/bin/bash
cd "$(dirname "$0")"

# Check if English Bible data exists
if [ ! -f "bible_nt_en.json" ]; then
    echo ""
    echo "╔══════════════════════════════════════════════╗"
    echo "║  Downloading English Bible text...           ║"
    echo "║  (only needed on first run)                  ║"
    echo "╚══════════════════════════════════════════════╝"
    echo ""
    python3 download_bible_en.py
    echo ""
fi

echo "╔══════════════════════════════════════════════╗"
echo "║  Bible Reader starting...                    ║"
echo "║  Browser will open shortly.                  ║"
echo "║  To stop: Ctrl+C or close this window        ║"
echo "╚══════════════════════════════════════════════╝"
echo ""

# Open browser after short delay
(sleep 1 && open "http://localhost:8080") &

# Start local server
python3 -m http.server 8080
