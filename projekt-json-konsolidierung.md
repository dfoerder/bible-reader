# Plan: Konsolidierung der JSON-Dateien

Neu erstellt am 17.06.2026 (ursprünglicher Plan aus früherer Session nicht mehr auffindbar).
Ziel: Die vielen JSON-Dateien auf eine klare *Single Source of Truth* zurückführen,
Duplikate/Drift beseitigen und Repo-Bloat entfernen.

## Ist-Zustand (verifiziert 17.06.2026)

| Bereich | Dateien | Größe | Git | Rolle |
|---|---|---|---|---|
| `data/` | 2 | 1,3 MB | getrackt | **Quelle** Vokabel-/Übungsdaten |
| `bibles/` | 793 | ~100 MB | getrackt | **Quelle** Bibeltexte + Annotationen (lazy pro Buch) |
| `www/` | 663 | ~75 MB | ignored | Capacitor `webDir` — Kopie von root |
| `ios/App/App/public/` | 663 | ~75 MB | ignored | Capacitor-Sync von `www/` (md5-identisch) |
| `alt/` | 16 | ~37 MB | **getrackt** | Legacy-Daten + Altskripte, nirgends referenziert |

- App lädt zur Laufzeit aus **root** (`index.html` → `data/*.json`, `bibles/...`). GitHub Pages bedient root von `main`.
- `www/` und `ios/` sind reine Ableitungen, werden aber **manuell** kopiert → bereits **auseinandergedriftet** (POS-Update vom 17.06. fehlt dort).

## Arbeitspakete

### AP1 — Legacy `alt/` aus dem Tracking entfernen  ·  Status: ERLEDIGT (17.06.2026)
Größter, risikoärmster Gewinn: ~37 MB, 0 Referenzen.
- [x] Große Datenblobs aus `alt/` untracked (`git rm --cached`): `nt_annotations_en.json`, `ot_annotations_en.json`, `bible_ot_en.json`, `bible_nt_en.json`, `phrase_levels.json`, `ita-riveduta.osis.xml` — Dateien bleiben lokal
- [x] Altskripte (`convert_osis_to_json.py`, `extract_vocab.py`, `generate_context_exercises.py`, `merge_phrases.py`, `modernize_*.py`, …) als Provenienz **behalten** (weiter getrackt)
- [x] `.gitignore` um `alt/*.json` + `alt/*.xml` ergänzt
- [ ] Optional: `git`-History-Rewrite (`git filter-repo`) falls Repo-Größe stört — separat entscheiden, da Force-Push nötig (noch nicht durchgeführt; Blobs bleiben in der History)

### AP2 — Capacitor-Sync reproduzierbar machen (Drift beheben)  ·  Status: ERLEDIGT (17.06.2026)
Root bleibt einzige Quelle; `www/` + `ios/` werden deterministisch erzeugt, nie von Hand bearbeitet.
- [x] `sync_www.sh` angelegt: spiegelt `index.html`, `sw.js`, `manifest.json`, `icon-192/512.png`, `data/`, `bibles/`, `lib/` → `www/` (rsync `--delete`), danach `npx cap sync` (`--no-cap` für www-only)
- [x] In `projekt-regeln.md` verankert: vor jedem iOS-Build `./sync_www.sh`; `www/` nie manuell editieren
- [x] Aktuellen Stand gesynct — POS-Update jetzt in `www/` **und** `ios/` (md5 stimmt mit root überein, Drift weg)

### AP3 — Zwei data-Dateien aus einer Pipeline erzeugen  ·  Status: TEILWEISE
Einheitlicher Pool existiert seit v1.9.5b; `pos` heute in **beide** Dateien geschrieben (dupliziert).
- `vocab_pool.json`: `{en, de, pos, occ, sub}` je CEFR-Level
- `context_exercises.json`: `{text, answer, de, lemma, pos, ref, book, sub}` je CEFR-Level
- [ ] Gemeinsame Wort-Identität (`en`/`lemma` + `de` + `pos` + `sub`) aus **einer** Master-Quelle ableiten, statt `pos` parallel zu pflegen
- [ ] Prüfen, ob Laufzeit zwei getrennte Dateien braucht (Quiz vs. Lückentext) — falls ja: getrennt **lassen**, aber gemeinsam generieren; falls nein: zu einer Datei mit Wort-Tabelle + referenzierenden Übungen zusammenführen
- [ ] Generierungs-Skripte (`assign_cefr_levels.py`, `generate_pos.py`, `generate_training_data.js`) auf gemeinsame Quelle ausrichten

### AP4 — `bibles/`-Struktur: bewusste Entscheidung dokumentieren  ·  Status: OFFEN
793 Dateien, lazy pro Buch geladen.
- [ ] Empfehlung festhalten: **nicht** zusammenführen — Per-Buch-Lazy-Loading ist ein Feature (Offline, Teil-Download, kleinere Fetches). Konsolidierung würde Ladeverhalten verschlechtern.

## Empfohlene Reihenfolge
1. **AP1** (sofortiger Aufräum-Gewinn, kein Risiko)
2. **AP2** (behebt aktive Drift, schützt iOS-Build)
3. **AP3** (Daten-Hygiene, mittlerer Aufwand)
4. **AP4** (nur Doku-Entscheidung)
