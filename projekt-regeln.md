# Projektregeln

## Deployment
- Entwickelt wird auf dem Branch `dev`
- Zum Deployen: `dev` in `main` mergen und `main` pushen
- `dev` wird nie direkt gepusht

## Daten-Quelle (Single Source of Truth)
- Die Web-App lädt zur Laufzeit aus dem Repo-**Root** (`data/`, `bibles/`, `index.html` …);
  GitHub Pages bedient root von `main`
- `www/` (Capacitor `webDir`) und `ios/` sind **reine Ableitungen** und werden NIE von Hand bearbeitet
  (beide sind gitignored)
- Vor jedem iOS-Build: `./sync_www.sh` ausführen — spiegelt root → `www/` und synct `www/` → `ios/`
  (`./sync_www.sh --no-cap` nur nach `www/`, ohne Capacitor-Sync)
