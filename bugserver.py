#!/usr/bin/env python3
"""Bug-Empfänger für Tests auf dem iPhone.

Zwei Aufgaben in einem Prozess:

1. Er serviert die App aus dem Repo-Root (wie start.command) — auf dem iPhone
   also http://<mac-ip>:8765 aufrufen.
2. Er nimmt unter POST /bugs die im Handy gesammelten Bugs entgegen und hängt
   sie an bugs/bugs.json an (Dubletten über die id werden übersprungen).

Weil die App dann von derselben http-Adresse kommt wie der Empfänger, greift
weder Mixed-Content-Blockade noch CORS — der Sync-Knopf im Bug-Melder braucht
gar keine Endpunkt-Adresse.

    python3 bugserver.py                 # Port 8765
    python3 bugserver.py --port 9000
    python3 bugserver.py --import x.json # per AirDrop erhaltene Liste einlesen

Offene Bugs anzeigen:  python3 bugserver.py --list
Erledigt abhaken:      python3 bugserver.py --done <id> [<id> ...]
"""
import argparse, json, os, socket, sys
from datetime import datetime
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.abspath(__file__))
BUGDIR = os.path.join(ROOT, 'bugs')
BUGFILE = os.path.join(BUGDIR, 'bugs.json')
MAX_BODY = 4 * 1024 * 1024


def load():
    try:
        with open(BUGFILE, encoding='utf-8') as f:
            return json.load(f)
    except (OSError, ValueError):
        return []


def store(bugs):
    os.makedirs(BUGDIR, exist_ok=True)
    tmp = BUGFILE + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(bugs, f, ensure_ascii=False, indent=2)
    os.replace(tmp, BUGFILE)


def merge(incoming):
    """Neue Bugs anhängen; Rückgabe: Anzahl tatsächlich neuer Einträge."""
    bugs = load()
    known = {b.get('id') for b in bugs}
    added = 0
    for b in incoming:
        if not isinstance(b, dict) or b.get('id') in known:
            continue
        b.pop('synced', None)  # Handy-interner Übertragungsstatus, hier bedeutungslos
        b.setdefault('status', 'open')
        b['received'] = datetime.now().isoformat(timespec='seconds')
        bugs.append(b)
        known.add(b.get('id'))
        added += 1
    if added:
        bugs.sort(key=lambda b: b.get('ts', ''))
        store(bugs)
    return added


def describe(b):
    ctx = b.get('ctx') or {}
    where = ctx.get('phase', '?')
    if ctx.get('book'):
        where += ' · %s %s' % (ctx['book'], ctx.get('chapter', ''))
    sev = {'blocker': '🔴', 'major': '🟠', 'minor': '🟡'}.get(b.get('sev'), '·')
    return '%s [%s] %s' % (sev, where, (b.get('text') or '').replace('\n', ' ')[:100])


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def _cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')

    def _json(self, code, payload):
        body = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self._cors()
        self.end_headers()
        self.wfile.write(body)

    def end_headers(self):
        # Die App wird beim Testen ständig neu gebaut — nichts cachen lassen.
        if self.path != '/bugs':
            self.send_header('Cache-Control', 'no-store')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_GET(self):
        if self.path.split('?')[0] == '/bugs':
            self._json(200, load())
            return
        super().do_GET()

    def do_POST(self):
        if self.path.split('?')[0] != '/bugs':
            self._json(404, {'error': 'unbekannter Pfad'})
            return
        length = int(self.headers.get('Content-Length') or 0)
        if length <= 0 or length > MAX_BODY:
            self._json(400, {'error': 'leerer oder zu großer Body'})
            return
        try:
            payload = json.loads(self.rfile.read(length).decode('utf-8'))
        except ValueError as e:
            self._json(400, {'error': 'kein gültiges JSON: %s' % e})
            return
        incoming = payload.get('bugs') if isinstance(payload, dict) else payload
        if not isinstance(incoming, list):
            self._json(400, {'error': 'erwarte {"bugs": [...]}'})
            return
        added = merge(incoming)
        for b in incoming[-added:] if added else []:
            print('  ' + describe(b))
        print('→ %d neue Bug(s), %d insgesamt in bugs/bugs.json' % (added, len(load())))
        self._json(200, {'added': added, 'total': len(load())})

    def log_message(self, fmt, *args):
        if self.path.startswith('/bugs'):
            super().log_message(fmt, *args)


def lan_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('192.168.1.1', 1))
        return s.getsockname()[0]
    except OSError:
        return '127.0.0.1'
    finally:
        s.close()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--port', type=int, default=8765)
    ap.add_argument('--import', dest='imp', metavar='DATEI', help='exportierte bugs.json einlesen')
    ap.add_argument('--list', action='store_true', help='offene Bugs anzeigen')
    ap.add_argument('--all', action='store_true', help='mit --list auch erledigte zeigen')
    ap.add_argument('--done', metavar='ID', nargs='+', help='Bug(s) als erledigt markieren')
    args = ap.parse_args()

    if args.imp:
        with open(args.imp, encoding='utf-8') as f:
            data = json.load(f)
        incoming = data.get('bugs') if isinstance(data, dict) else data
        print('%d neue Bug(s) übernommen' % merge(incoming))
        return

    if args.done:
        bugs = load()
        hit = 0
        for b in bugs:
            if b.get('id') in args.done:
                b['status'] = 'fixed'
                b['fixed'] = datetime.now().isoformat(timespec='seconds')
                hit += 1
        store(bugs)
        print('%d Bug(s) als erledigt markiert' % hit)
        return

    if args.list:
        for b in load():
            if args.all or b.get('status') != 'fixed':
                print('%s  %s' % (b.get('id', '?'), describe(b)))
        return

    addr = ('0.0.0.0', args.port)
    print('Bug-Empfänger läuft.')
    print('  Auf dem iPhone öffnen:  http://%s:%d' % (lan_ip(), args.port))
    print('  Bugs landen in:         %s' % BUGFILE)
    print('  Beenden: Ctrl+C')
    try:
        ThreadingHTTPServer(addr, Handler).serve_forever()
    except KeyboardInterrupt:
        print('\nGestoppt.')


if __name__ == '__main__':
    main()
