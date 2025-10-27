# Story 1.2: Calibre Plugins Setup for Enhanced Ingestion

**Purpose:** Configure Calibre plugins for Story 1.2 to enhance auto-ingest with page counting, ISBN extraction, and metadata enrichment.

**Status:** Ready for Setup

---

## Overview

Calibre-Web-Automated (v3.1.0+) supports plugin integration via mounted volumes. This document describes:
- Plugin mounting and configuration
- Recommended plugins for enhanced ingest
- Page counting capability (major value-add)
- Integration with Story 1.2 validation

---

## Plugin Infrastructure Setup

### 1. Create Plugins Directory on RPi

```bash
ssh pi@raspberrypi.local

# Create plugins directory
sudo mkdir -p /library/plugins
sudo chown 1000:1000 /library/plugins
sudo chmod 755 /library/plugins

ls -la /library/plugins
```

### 2. Copy Customize Configuration

```bash
# From your development machine
scp resources/calibre-plugins/customize.py.json pi@raspberrypi.local:/library/plugins/

# Verify
ssh pi@raspberrypi.local
ls -la /library/plugins/customize.py.json
cat /library/plugins/customize.py.json
```

### 3. Verify Docker Compose Volume Mount

The docker-compose.yml already includes:
```yaml
volumes:
  - /library/plugins:/config/.config/calibre/plugins
```

**Verify on RPi:**
```bash
# After docker-compose up
docker exec calibre-web-automated ls -la /config/.config/calibre/plugins/
```

---

## Recommended Plugins for Story 1.2

### Essential Plugins (Page Counting & Metadata)

#### 1. **Count Pages** (CRITICAL)
- **Purpose:** Automatically extracts and counts pages from EPUB/PDF files
- **Input:** Ebook file (EPUB, PDF, MOBI)
- **Output:** Pages custom column populated during ingest
- **Impact on Performance:** Minimal (~2-3 seconds per book for EPUB)
- **Where to get:** [Calibre Project](https://github.com/kovidgoyal/calibre/tree/master/src/calibre/ebooks/conversion/plugins)

**Setup:**
```bash
# Download and place in /library/plugins/
# Plugin structure: /library/plugins/count_pages/
#   ├── __init__.py
#   ├── ui.py (optional)
#   └── conversion.py
```

#### 2. **Extract ISBN**
- **Purpose:** Pulls ISBN from book metadata for accurate lookup
- **Impact:** Improves Hardcover.app + Google Books metadata matching
- **Essential:** YES (supports AC2-3 validation)

#### 3. **Fix Metadata**
- **Purpose:** Normalizes author names, removes special characters
- **Impact:** Ensures consistent library metadata
- **Essential:** Recommended

#### 4. **Extract Covers**
- **Purpose:** Ensures high-quality cover extraction
- **Impact:** AC5 validation (enriched metadata includes cover art)
- **Essential:** YES (supports AC5)

---

## Plugin Installation Process

### Step 1: Source Plugins

Calibre plugins are typically sourced from:

**Option A: Pre-built from Calibre Store**
```bash
# Visit: https://plugins.calibre-ebook.com/
# Download plugin ZIP files
# Extract to /library/plugins/
```

**Option B: Build from Calibre Source**
```bash
# Clone Calibre repository
git clone https://github.com/kovidgoyal/calibre.git

# Navigate to plugins
cd calibre/src/calibre/ebooks/conversion/plugins/

# Copy desired plugins to /library/plugins/
```

**Option C: Use Pre-packaged Community Plugins**
- **Excellent conversion-focused plugins:** https://github.com/kovidgoyal/calibre/releases
- Many plugins are built-in to Calibre and auto-discovered

### Step 2: Plugin Directory Structure

```
/library/plugins/
├── customize.py.json              # Configuration file
├── count_pages/                   # Page counting plugin
│   ├── __init__.py
│   ├── ui.py
│   └── ... other files
├── extract_isbn/                  # ISBN extraction plugin
│   ├── __init__.py
│   └── ... other files
└── fix_metadata/                  # Metadata normalization
    ├── __init__.py
    └── ... other files
```

### Step 3: Enable in CWA Settings

1. **Access CWA Web UI:** `http://raspberrypi.local:8083`
2. **Navigate:** Admin → Settings → CWA Settings
3. **Enable CWA Metadata Enforcement Service** (if using fix_metadata plugin)
   - This applies metadata changes to actual ebook files during ingest
4. **Verify plugins loaded:**
   - Admin → Settings → Plugins/Extensions
   - Look for registered plugins from `/config/.config/calibre/plugins/`

---

## Performance Considerations for Story 1.2

### Plugin Overhead Estimation

| Plugin | Overhead per Book | Total 1-Week Impact | Notes |
|--------|-------------------|---------------------|-------|
| Count Pages (EPUB) | ~2-3 sec | Minimal | Runs during ingest conversion |
| Count Pages (PDF) | ~5-7 sec | Depends on usage | PDF parsing slower |
| Extract ISBN | ~0.5 sec | Negligible | Metadata extraction only |
| Fix Metadata | ~1 sec | Minimal | Text processing |
| Extract Covers | ~1-2 sec | Included in ingest | Native CWA feature |
| **Total Estimated Overhead** | **~5-10 sec/book** | **Acceptable** | Still under 30s AC4 target |

### Memory Impact

- Plugins loaded into CWA process memory on startup
- All 4 plugins combined: ~50-100 MB additional memory
- **Story 1.2 targets:** Idle <600MB, Peak <1GB
- **Verdict:** Plugins fit comfortably within targets

### Monitoring with Plugins Enabled

Update monitoring script to capture:
- Baseline memory (idle, no ingest) with plugins loaded
- Peak memory during multi-plugin processing
- Per-book timing to isolate plugin overhead

---

## Integration with Story 1.2 Validation

### Test Cases for Plugin Validation

**Test Case 1: Single Book with Page Counting**
```
1. Drop EPUB with 300+ pages into ingest
2. Monitor page count extraction
3. Verify:
   - Import completes in <30 seconds (AC4)
   - Page count populated in library metadata
   - No OOM or crashes
```

**Test Case 2: Book Without ISBN (Tests Fallback)**
```
1. Drop EPUB without ISBN metadata
2. Plugins should:
   - Extract ISBN if embedded in file
   - Count pages successfully
   - Allow metadata enrichment via title/author fallback
```

**Test Case 3: PDF with Count Pages Plugin**
```
1. Drop PDF file into ingest
2. Plugin extracts page count
3. Metadata enrichment falls back to Google Books
4. Monitor performance overhead (PDF parsing slower)
```

### Acceptance Criteria Alignment

| AC | Requirement | Plugin Support |
|----|-------------|-----------------|
| 1 | Auto-ingest configured | ✅ Plugins run during ingest |
| 2-3 | Hardcover + Google Books | ✅ ISBN extraction improves matching |
| 4 | Import <30 seconds | ✅ Plugin overhead ~5-10 sec acceptable |
| 5 | Enriched metadata (title/author/cover/description/**pages**) | ✅ Count Pages plugin adds pages field |
| 6 | EPUB optimization enabled | ✅ Native CWA feature |
| 7 | Hardcover API authenticated | ✅ Independent of plugins |
| 8-12 | 1-week workload validation | ✅ Monitor plugin performance overhead |
| 13 | Documentation | ✅ This document |
| 14 | Go/no-go decision | ✅ Include plugin performance in decision |

---

## Troubleshooting Plugin Issues

### Plugin Not Loading

**Symptom:** Plugins not visible in CWA admin panel

**Solution:**
1. Verify directory structure matches `/config/.config/calibre/plugins/`
2. Check plugin `__init__.py` exists in each plugin folder
3. Verify `customize.py.json` is readable (not corrupted)
4. Restart CWA container: `docker restart calibre-web-automated`
5. Check CWA logs: `docker logs -f calibre-web-automated | grep -i plugin`

### Plugin Performance Degradation

**Symptom:** Ingest takes >30 seconds with plugins enabled

**Solution:**
1. Identify problematic plugin via monitoring script
2. Disable non-essential plugins in `customize.py.json`
3. Check plugin source code for inefficient loops
4. Consider plugin optimization or replacement
5. Document findings in Story 1.2 performance report

### Plugin Conflicts

**Symptom:** Duplicate page counts, conflicting metadata

**Solution:**
1. Disable conflicting plugins in `customize.py.json`
2. Test with one plugin at a time
3. Monitor ingest logs: `docker logs calibre-web-automated`
4. Document conflicts in performance report under "Known Issues"

---

## Post-Implementation Checklist

- [ ] Plugin directory created on RPi (`/library/plugins/`)
- [ ] `customize.py.json` copied to RPi
- [ ] Docker Compose volume mount verified
- [ ] Plugins downloaded/extracted to `/library/plugins/`
- [ ] CWA restarted and plugins loaded
- [ ] Plugin registration verified in CWA admin panel
- [ ] Test book with pages ingested successfully
- [ ] Page count populated in library metadata
- [ ] Monitoring script run with plugins enabled
- [ ] Performance overhead documented in Story 1.2 report
- [ ] Go/no-go decision includes plugin impact assessment

---

## References

- CWA Plugin Support (WIP): https://github.com/crocodilestick/calibre-web-automated/wiki/Configuration
- Calibre Plugin Development: https://manual.calibre-ebook.com/custom_plugins.html
- Calibre Plugin Store: https://plugins.calibre-ebook.com/
- Story 1.2 ACs: `/docs/stories/story-1.2.md`
