#!/usr/bin/env bash
# Bug-Empfänger + HTTPS-Tunnel in einem Rutsch.
#
# Der Tunnel liefert die App UND nimmt die Bugs entgegen — beides unter
# derselben https-Adresse. Damit funktioniert der Auto-Upload auch von
# unterwegs, ohne WLAN und ohne Mixed-Content-Blockade.
#
#   ./bugtunnel.sh          # Port 8765
#   ./bugtunnel.sh 9000
#
# Auf dem iPhone die angezeigte Adresse öffnen (QR-Code scannen, falls
# qrencode installiert ist: brew install qrencode). Das Empfänger-Feld im
# Bug-Melder bleibt leer — die App schickt die Bugs an ihre eigene Herkunft.
#
# Achtung: Die Adresse ist öffentlich erreichbar, solange dieses Fenster offen
# ist. Sie ist zufällig und wechselt bei jedem Start; nach Ctrl+C ist sie tot.
set -euo pipefail
cd "$(dirname "$0")"
PORT="${1:-8765}"

command -v cloudflared >/dev/null 2>&1 || {
  echo "cloudflared fehlt — installieren mit:  brew install cloudflared" >&2
  exit 1
}

SRV=""
if curl -sf -o /dev/null "http://127.0.0.1:$PORT/bugs" 2>/dev/null; then
  echo "→ Bug-Empfänger läuft bereits auf Port $PORT"
else
  echo "→ Bug-Empfänger starten (Port $PORT)"
  python3 bugserver.py --port "$PORT" &
  SRV=$!
  sleep 1
fi

LOG=$(mktemp -t bugtunnel)
cloudflared tunnel --url "http://localhost:$PORT" --no-autoupdate > "$LOG" 2>&1 &
TUN=$!

cleanup(){
  kill "$TUN" 2>/dev/null || true
  [ -n "$SRV" ] && kill "$SRV" 2>/dev/null || true
  rm -f "$LOG"
}
trap cleanup EXIT INT TERM

echo "→ Tunnel wird aufgebaut …"
URL=""
for _ in $(seq 1 40); do
  URL=$(grep -om1 'https://[a-z0-9-]*\.trycloudflare\.com' "$LOG" || true)
  [ -n "$URL" ] && break
  kill -0 "$TUN" 2>/dev/null || { echo "cloudflared ist abgebrochen:" >&2; tail -20 "$LOG" >&2; exit 1; }
  sleep 1
done
[ -n "$URL" ] || { echo "Keine Tunnel-Adresse erhalten:" >&2; tail -20 "$LOG" >&2; exit 1; }

echo
echo "╔══════════════════════════════════════════════════════════╗"
echo "  Auf dem iPhone öffnen:"
echo "  $URL/?bugs=1"
echo "╚══════════════════════════════════════════════════════════╝"
if command -v qrencode >/dev/null 2>&1; then
  qrencode -t ANSIUTF8 "$URL/?bugs=1"
else
  echo "  (QR-Code zum Abscannen: brew install qrencode)"
fi
echo "  Bugs landen in: $(pwd)/bugs/bugs.json"
echo "  Beenden mit Ctrl+C — danach ist die Adresse ungültig."
echo

wait "$TUN"
