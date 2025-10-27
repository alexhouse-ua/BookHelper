# Story 1.2: Performance Validation Report

**Story:** Auto-Ingestion + Metadata Enrichment
**Validation Period:** [START_DATE] to [END_DATE] (1 week)
**Status:** In Progress

---

## Configuration Steps (Execute Before Monitoring)

### 1. Verify Ingest Folder
```bash
# SSH to Raspberry Pi
ssh pi@raspberrypi.local

# Create ingest folder if not exists
sudo mkdir -p /library/ingest
sudo chown 1000:1000 /library/ingest
ls -la /library/ingest
```

### 2. Configure CWA Auto-Ingest
1. Open CWA web UI: `http://raspberrypi.local:8083`
2. Login with admin credentials
3. Navigate to: **Admin** → **Settings** → **Import Settings**
4. Configure:
   - ✅ Enable Auto-Import: ON
   - ✅ Import Folder: `/cwa-book-ingest`
   - ✅ Watch Folder: Enable
   - ✅ Auto-convert EPUB: Enable epub-fixer

### 3. Configure Metadata Providers
Navigate to: **Admin** → **Settings** → **Metadata Providers**

**Primary: Hardcover.app**
- ✅ Enable Hardcover
- ✅ API Token: Already configured in docker-compose.yml (HARDCOVER_TOKEN env var)
- Test: Click "Test Connection" → Verify success

**Fallback: Google Books**
- ✅ Enable Google Books
- ✅ Set as fallback (priority 2)

### 4. Start Monitoring
```bash
# Copy monitoring script to RPi
scp resources/scripts/monitor-resources-1.2.py pi@raspberrypi.local:/tmp/

# SSH to RPi and start monitoring
ssh pi@raspberrypi.local
chmod +x /tmp/monitor-resources-1.2.py
nohup /tmp/monitor-resources-1.2.py > /tmp/monitor.log 2>&1 &

# Verify running
tail -f /tmp/monitor.log
```

### 5. Initial Baseline Test
```bash
# Drop test EPUB into ingest folder
# Use a book with ISBN for Hardcover metadata test
scp test-book.epub pi@raspberrypi.local:/library/ingest/

# Watch CWA logs
docker logs -f calibre-web-automated

# Expected: Import completes in <30 seconds with full metadata
```

---

## Monitoring Data Collection

### Baseline Metrics (Initial State)

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Idle Memory | <600MB | [FILL] MB | [PASS/FAIL] |
| Idle CPU | N/A | [FILL]% | N/A |
| Initial Library Size | ~22 books | [FILL] books | - |

### Test Book Ingestion Events

| Date/Time | Book File | Import Time (s) | Metadata Source | Memory Peak (MB) | Success |
|-----------|-----------|-----------------|-----------------|------------------|---------|
| [FILL] | test-book-1.epub | [FILL] | [Hardcover/Google] | [FILL] | [Y/N] |
| [FILL] | test-book-2.epub | [FILL] | [Hardcover/Google] | [FILL] | [Y/N] |
| ... | ... | ... | ... | ... | ... |

### Peak Resource Usage

| Operation | Peak Memory (MB) | Peak CPU (%) | Duration (s) | Notes |
|-----------|------------------|--------------|--------------|-------|
| Idle | [FILL] | [FILL] | N/A | Baseline |
| Single Import | [FILL] | [FILL] | [FILL] | |
| Metadata Fetch | [FILL] | [FILL] | [FILL] | |
| Library Scan | [FILL] | [FILL] | [FILL] | ~[X] books |

### Stability Observations

**Docker Logs Review:**
```bash
# Check for errors
docker logs calibre-web-automated | grep -i error
# [PASTE RESULTS]
```

**OOM Detection:**
```bash
# Check kernel logs
dmesg | grep -i "out of memory"
# [PASTE RESULTS - should be empty]
```

**Observed Issues:**
- [FILL: List any crashes, timeouts, errors]
- [FILL: Or "None observed" if stable]

---

## Acceptance Criteria Validation

| AC | Criteria | Status | Evidence |
|----|----------|--------|----------|
| 1 | CWA auto-ingest monitoring designated folder | [PASS/FAIL] | [Config screenshot/logs] |
| 2 | Hardcover.app configured as primary source | [PASS/FAIL] | [Settings verification] |
| 3 | Google Books configured as fallback | [PASS/FAIL] | [Settings verification] |
| 4 | Test ebook imported within 30 seconds | [PASS/FAIL] | [Measured: X seconds] |
| 5 | Enriched metadata present (title/author/cover/description/pages) | [PASS/FAIL] | [Book details inspection] |
| 6 | EPUB optimization (epub-fixer) enabled | [PASS/FAIL] | [Settings verification] |
| 7 | Hardcover API authenticated and validated | [PASS/FAIL] | [Test connection result] |
| 8 | 1-week incremental ingestion (1-2 books/drop) | [PASS/FAIL] | [X test cycles completed] |
| 9 | Memory <600MB idle, <1GB during metadata fetch | [PASS/FAIL] | [Idle: X MB, Peak: X MB] |
| 10 | Metadata enrichment <30 seconds/book average | [PASS/FAIL] | [Average: X seconds] |
| 11 | Library scan (~20-50 books) <2 minutes | [PASS/FAIL] | [Measured: X seconds] |
| 12 | No crashes, corruption, OOM errors | [PASS/FAIL] | [Zero errors observed] |
| 13 | Documentation created with resource patterns | [PASS/FAIL] | [This document] |
| 14 | Go/no-go decision documented | [PENDING] | [See below] |

---

## Performance Summary

### Statistics
- **Total Test Books Ingested:** [X]
- **Average Import Time:** [X.X] seconds
- **Average Memory Usage (Idle):** [X] MB
- **Peak Memory Usage (Metadata Fetch):** [X] MB
- **Library Scan Time ([X] books):** [X] seconds
- **Hardcover API Success Rate:** [X]%
- **Google Books Fallback Rate:** [X]%

### Observations
[Summarize key findings:]
- Performance characteristics observed
- Any constraints or bottlenecks identified
- Comparison to targets

---

## Go/No-Go Decision

**Decision Date:** [FILL]

### Analysis

**Memory Performance:**
- Idle: [X] MB ([UNDER/OVER] 600MB target)
- Peak: [X] MB ([UNDER/OVER] 1GB target)
- Assessment: [ACCEPTABLE/CONCERN]

**Timing Performance:**
- Import: [X] sec avg ([UNDER/OVER] 30s target)
- Scan: [X] sec ([UNDER/OVER] 120s target)
- Assessment: [ACCEPTABLE/CONCERN]

**Stability:**
- Errors: [X] ([ZERO/NON-ZERO])
- Assessment: [ACCEPTABLE/CONCERN]

### Decision

**[✅ GO / ⚠️ GO WITH CONSTRAINTS / ❌ NO-GO]**

**Rationale:**
[FILL: Explain decision based on data]

**If GO:** Continue with RPi 4 2GB for Epic 1. Incremental ingestion pattern validated for production.

**If GO WITH CONSTRAINTS:**
- Document specific constraints: [e.g., "Memory peaks near 1GB limit; avoid bulk imports"]
- Mitigation plan: [e.g., "Monitor during Epic 2 Syncthing addition"]
- Impact on future epics: [e.g., "Epic 5 migration may require staged approach"]

**If NO-GO:**
- Blockers identified: [List]
- Recommended path: [e.g., "RPi 5 8GB upgrade" or "Reduce library scope"]

---

## Next Steps

- [ ] If GO: Proceed to Story 1.3 (Fallback Procedures)
- [ ] If CONSTRAINTS: Document in Epic 1 tech spec addendum
- [ ] If NO-GO: Escalate to PM for hardware decision

---

**Prepared by:** Dev Agent (Amelia)
**Completed:** [DATE]
**Story Status:** [In Progress / Ready for Review]
