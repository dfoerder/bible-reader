#!/bin/bash
cd "$(dirname "$0")"

# Check if French Bible data exists
if [ ! -f "bible_nt.json" ]; then
    echo ""
    echo "╔══════════════════════════════════════════════╗"
    echo "║  Franz. Bibeltext wird heruntergeladen...    ║"
    echo "║  (nur beim ersten Mal nötig)                 ║"
    echo "╚══════════════════════════════════════════════╝"
    echo ""
    python3 download_bible.py
    echo ""
fi

# Check if English Bible data exists
if [ ! -f "bible_nt_en.json" ]; then
    echo ""
    echo "╔══════════════════════════════════════════════╗"
    echo "║  Engl. Bibeltext wird heruntergeladen...     ║"
    echo "║  (nur beim ersten Mal nötig)                 ║"
    echo "╚══════════════════════════════════════════════╝"
    echo ""
    python3 download_bible_en.py
    echo ""
fi

echo "╔══════════════════════════════════════════════╗"
echo "║  Bible Reader startet...                     ║"
echo "║  Browser öffnet sich gleich.                 ║"
echo "║  Zum Beenden: Ctrl+C oder Fenster schliessen ║"
echo "╚══════════════════════════════════════════════╝"
echo ""

# Open browser after short delay
(sleep 1 && open "http://localhost:8080") &

# Start local server
python3 -m http.server 8080
