# Projektregeln

## Deployment
- Entwickelt wird auf dem Branch `dev`; `dev` wird nie direkt gepusht
- Deploy: `./deploy.sh "Changelog-Zeile"` — bumpt `APP_VERSION`/`APP_DATE` (index.html) und Cache-Name (sw.js), schreibt den Changelog-Eintrag nach `projekt-log.md`, aktualisiert den Versionskopf in `dokumentation.md`, committet, merged `dev` → `main` und pusht (GitHub Pages)
- Die Changelog-Zeile ist Pflicht — sie wird Commit-Message und Log-Eintrag
- `APP_VERSION` trägt bis auf Weiteres den Suffix `b` (Beta)

## Daten-Quelle (Single Source of Truth)
- Die Web-App lädt zur Laufzeit aus dem Repo-**Root** (`data/`, `bibles/`, `index.html` …);
  GitHub Pages bedient root von `main`
- `www/` (Capacitor `webDir`) und `ios/` sind **reine Ableitungen** und werden NIE von Hand bearbeitet
  (beide sind gitignored)
- Vor jedem iOS-Build: `./sync_www.sh` ausführen — spiegelt root → `www/` und synct `www/` → `ios/`
  (`./sync_www.sh --no-cap` nur nach `www/`, ohne Capacitor-Sync)
