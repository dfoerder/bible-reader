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

### AP3 — Zwei data-Dateien aus einer Pipeline erzeugen  ·  Status: ANALYSIERT (17.06.2026), Umsetzung offen

**Befund (verifiziert):** Die beiden Dateien sind eine perfekte **1:1-Bijektion**.
- `context_exercises`: 5086 Einträge = genau 1 Übung pro Lemma
- `vocab_pool`: 5086 eindeutige Wörter
- 100 % Lemma-Überlappung (0 fehlend), `pos` zu 100 % aus Pool ableitbar
- `de` in beiden Dateien **identisch** (5086 gleich, 0 abweichend)
- Gemeinsam (redundant): `lemma`/`en`, `de`, `pos`, `sub` · nur CE: `text`,`answer`,`ref`,`book` · nur VP: `occ`

**Runtime:** `vocab_pool`→`VOCAB_POOL` (Quiz, Frequenz, Statistik, POS-Distraktoren);
`context_exercises`→`CLOZE_EXERCISES` nur für Buch-Lückentext (`startBookCloze`).
Kapitel-Lückentext wird live aus Annotationen erzeugt → **nicht** betroffen. Beide Dateien werden
beim Start zusammen geladen (2 Fetches).

**Optionen (Größen gemessen):**
| | Ergebnis | Ersparnis | Risiko |
|---|---|---|---|
| Aktuell | 2 Dateien, 1214 KB, 2 Fetches | — | — |
| A — schlank | CE ohne `de`+`pos`, Lookup aus Pool | −142 KB (12 %) | gering |
| B — zusammengeführt | ein `words.json`, 1 Eintrag/Wort | −280 KB (23 %), 1 Fetch | mittel |

**Empfehlung: Variante B** (`words.json`) — echte Konsolidierung, beendet Parallelpflege von `de`/`pos`,
ein Fetch, größte Ersparnis. A als risikoärmerer Zwischenschritt möglich.

**Umsetzung Variante B — Status: ERLEDIGT (17.06.2026)**
- [x] `data/words.json` erzeugt (5086 Wörter, 1 Eintrag/Wort, alle Felder); Round-trip + Node-Simulation der App-Ladelogik beweisen Feld-für-Feld-Gleichheit zu den Alt-Dateien
- [x] `index.html`: ein Fetch `data/words.json` → leitet `VOCAB_POOL` + `CLOZE_EXERCISES` (mit `lemma`-Alias) ab; zwei alte Fetches entfernt
- [x] `sw.js`: precached nur noch `words.json`; `CACHE_NAME` → `bible-full-v199`, `APP_VERSION` → `1.9.9b`
- [x] `generate_training_data.js`: Phase 4 ergänzt → schreibt `words.json`; `generate_pos.py`: schreibt `pos` jetzt in `words.json`
- [x] Alt-Dateien `vocab_pool.json` + `context_exercises.json` aus Tracking entfernt, gitignored (lokale Build-Intermediates); Einmal-Migration `build_words.py` gelöscht
- Hinweis: `compare_levels.js` (historisches Analyse-Tool) liest noch den lokalen `vocab_pool.json`-Intermediate — unkritisch, nicht Teil der App.

### AP4 — `bibles/`-Struktur: bewusste Entscheidung dokumentieren  ·  Status: ERLEDIGT (17.06.2026)
793 Dateien, lazy pro Buch geladen.
- [x] **Entscheidung: `bibles/` NICHT zusammenführen.** Per-Buch-Lazy-Loading ist ein
  bewusstes Feature — die App lädt nur das gerade gelesene Buch (`{nr}_web.json`) bzw. dessen
  Annotationen (`anno/{nr}_web_deu.json`) statt eines Monolithen. Vorteile: schnelle Erst-Fetches,
  geringer Speicher, Offline-Teilbestände, granulares SW-Caching. Eine Zusammenführung (~100 MB
  Einzeldatei) würde Start- und Ladeverhalten deutlich verschlechtern und PWA-Caching verschlechtern.

## Empfohlene Reihenfolge
1. **AP1** (sofortiger Aufräum-Gewinn, kein Risiko)
2. **AP2** (behebt aktive Drift, schützt iOS-Build)
3. **AP3** (Daten-Hygiene, mittlerer Aufwand)
4. **AP4** (nur Doku-Entscheidung)
