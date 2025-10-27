# Story 1.2: Auto-Ingestion + Metadata Enrichment

Status: In Progress (Tooling Complete - Manual Execution Required - 2025-10-27)

## Story

As a reader,
I want to drop ebook files into a folder and have them automatically added with complete metadata, with validated performance under realistic usage,
So that library ingestion is zero-touch and hardware performance is confirmed for production.

## Acceptance Criteria

1. CWA auto-ingest configured to monitor designated ingest folder
2. Hardcover.app metadata provider configured as primary source
3. Google Books configured as fallback metadata provider
4. Test ebook dropped into folder is automatically imported within 30 seconds
5. Imported book has enriched metadata: title, author, cover art, description, page count
6. EPUB format optimization (epub-fixer) enabled in CWA settings
7. Hardcover API authentication configured and validated
8. Realistic workload validation: Monitor CWA during 1-week incremental ingestion (1-2 books/drop, typical usage)
9. Memory remains <600MB idle, <1GB during metadata fetch
10. Metadata enrichment maintains <30 seconds per book average
11. Library scan (~20-50 books) completes in <2 minutes
12. No crashes, database corruption, or OOM errors observed
13. Documentation created with observed resource usage patterns
14. Go/no-go decision documented: Continue RPi 4 OR note constraints for future planning

## Tasks / Subtasks

- [ ] Configure CWA auto-ingest (AC: 1-7)
  - [ ] Create monitored ingest folder on RPi (`/library/ingest/`)
  - [ ] Configure CWA auto-ingest in web UI settings to point to folder
  - [ ] Set Hardcover.app as primary metadata provider
  - [ ] Configure Google Books as fallback provider
  - [ ] Enable EPUB optimization (epub-fixer)
  - [ ] Test with single EPUB: verify import <30 seconds with enriched metadata
  - [ ] Authenticate Hardcover API (if required)

- [ ] Execute 1-week realistic ingestion validation (AC: 8-12)
  - [ ] Start monitoring script to capture CPU/memory metrics every 5 minutes
  - [ ] Drop 1-2 test ebooks into ingest folder (simulating typical weekly usage)
  - [ ] Record baseline metrics: idle memory, CPU during typical operations
  - [ ] Monitor CWA web UI performance during metadata enrichment
  - [ ] Verify no crashes, database errors, or OOM conditions
  - [ ] After 1 week: collect peak memory usage, metadata enrichment times, scan performance
  - [ ] Document findings in spreadsheet (timestamp, operation, memory, CPU, duration)

- [ ] Validate realistic performance targets (AC: 9-11)
  - [ ] Confirm idle memory <600MB
  - [ ] Confirm metadata fetch <1GB peak during operation
  - [ ] Confirm metadata enrichment <30 seconds per book
  - [ ] Confirm library scan (20-50 books) <2 minutes
  - [ ] Verify no timeouts or fallback cascades required

- [ ] Create performance documentation (AC: 13)
  - [ ] Generate resource usage summary report from collected metrics
  - [ ] Create table: operation type, peak memory, duration, success/failure
  - [ ] Document any anomalies or constraints discovered
  - [ ] Save to `/docs/STORY-1.2-PERFORMANCE-REPORT.md`

- [ ] Go/no-go decision (AC: 14)
  - [ ] Review performance against criteria
  - [ ] Decision checkpoint: Do all 14 ACs pass?
    - [ ] YES: Document "Continue RPi 4 with incremental ingestion pattern"
    - [ ] NO (e.g., memory >1GB): Document constraints and workarounds
  - [ ] Update report with decision and rationale
  - [ ] If constraints found, note impact for future epics (storage, audiobooks)

## Dev Notes

### Architecture Alignment

This story validates the **Resource Constraint: Raspberry Pi 4 2GB** risk from architecture.md (section 4). Unlike the original Story 1.2 which assumed bulk 100+ book processing, this revised version tests the **actual usage pattern**: incremental weekly ingestion of 1-2 books.

Performance targets (<600MB idle, <1GB during metadata) ensure headroom for downstream epics:
- Epic 2: Syncthing daemon (file sync)
- Epic 3: ETL pipeline (concurrent with CWA)
- Epic 5: Migration scripts during import operations

**Reference:** [Source: docs/architecture.md § 4 - Resource Constraint: Raspberry Pi 4 2GB]

### Performance Targets

Per consolidated tech-spec-epic-1.md:
- Metadata Lookup: <30 seconds per book (Hardcover + fallback to Google Books)
- Memory Efficiency: Idle <600MB, <1GB during metadata enrichment
- Library Scan: <2 minutes for ~50 book library
- Ingestion Time: <30 seconds from file drop to library availability

**Reference:** [Source: docs/tech-spec-epic-1.md § Performance § Story 1.2]

### Testing Strategy

**Realistic Workload Approach:**
- 1-week observation period (actual usage pattern)
- 1-2 book drops per cycle (matches typical Friday or weekend reading acquisition)
- Light metadata load (single concurrent lookup, not bulk batch)
- No stress testing or artificial load

**Success Criteria:**
- All 14 ACs pass under realistic usage
- If any AC fails: document constraint and note for future epics
- No hard blocker if memory slightly exceeds 1GB (acceptable with mitigation planning)

### Project Structure Notes

**Files to create:**
- `/docs/STORY-1.2-PERFORMANCE-REPORT.md` — Resource metrics and go/no-go decision
- `/resources/scripts/monitor-resources-1.2.py` — Python monitoring script (collects CPU/memory via /proc)

**Test artifacts:**
- Monitoring CSV: timestamps, operation, memory_mb, cpu_pct, duration_sec
- CWA logs: Docker container logs for error detection
- Kernel logs: dmesg for OOM detection

### Known Dependencies

**Prerequisite:** Story 1.1 must be complete
- CWA deployed and operational
- Neon.tech schema initialized
- Koofr backup configured
- Monitoring environment ready

**Blocking follow-up:** If any AC fails
- Document constraints in performance report
- Plan mitigation (e.g., USB swap, reduced library size, RPi 5 upgrade as future option)
- No epic-level blocker; proceed with noted constraints

### References

- [Source: docs/epics.md § Epic 1 § Story 1.2]
- [Source: docs/tech-spec-epic-1.md § Workflows & Sequencing § Story 1.2 (revised)]
- [Source: docs/architecture.md § 4. Critical Warnings - Resource Constraint: Raspberry Pi 4 2GB]
- [Course Correction: Epic granularity reduction from 21 → 12-14 stories applied 2025-10-27]

## Dev Agent Record

### Context Reference

- Story Context XML: `/docs/stories/story-context-1.2.xml` (generated by story-context workflow 2025-10-27)

### Agent Model Used

Claude Sonnet 4.5 (claude-sonnet-4-5-20250929)

### Debug Log References

**Implementation Phase 1: Tooling & Documentation (2025-10-27)**

Prepared all tooling and documentation required for Story 1.2 execution:

1. **Monitoring Script:** Created `/resources/scripts/monitor-resources-1.2.py`
   - Monitors CWA container via `docker stats` every 5 minutes
   - Captures: timestamp, operation type, memory (MB), CPU (%), notes
   - Outputs CSV format to `/tmp/cwa-metrics-1.2.csv`
   - Detects operations from container logs (import/metadata_fetch/library_scan/idle)

2. **Performance Report Template:** Created `/docs/STORY-1.2-PERFORMANCE-REPORT.md`
   - Includes complete configuration steps for CWA auto-ingest setup
   - Sections: baseline metrics, test ingestion events, peak usage, stability observations
   - AC validation checklist (all 14 ACs)
   - Go/no-go decision framework with assessment criteria

3. **Infrastructure Verification:** Reviewed `docker-compose.yml`
   - ✅ Ingest folder already configured: `/library/ingest` → `/cwa-book-ingest`
   - ✅ Hardcover API token already present in environment
   - ✅ Memory limits appropriate: 1500M limit, 400M reservation
   - ✅ Auto-restart policy: unless-stopped

**Manual Execution Required:**

This story requires **1-week observation period** with real hardware and real-time monitoring:
- Configuration steps documented in performance report (steps 1-5)
- Execute configuration on Raspberry Pi (CWA web UI settings)
- Start monitoring script on RPi
- Drop 1-2 test books per cycle (simulating realistic weekly usage)
- Collect metrics over 7-day period
- Analyze data and complete AC validation
- Make go/no-go decision based on observed performance

**Current State:** All tooling prepared and validated against official documentation. Ready for manual execution by user on RPi hardware.

**Documentation Validation (2025-10-27):**
- Validated monitoring script against Docker API docs (v1.24+) - ✅ Correct
- Validated CWA configuration steps against official CWA v3 docs - ✅ Correct
- Noted: Hardcover.app integration marked "in progress" in CWA v3 docs - ⚠️ Added caveat to report
- Validated Google Books API as fallback - ✅ Available, 1000 req/day free tier
- Confirmed EPUB fixer feature and configuration - ✅ Available
- Confirmed auto-ingest behavior (files removed after processing) - ✅ Correct

### Completion Notes List

*Story not yet complete - awaiting 1-week validation execution and data collection*

**Known Risks Documented:**
- Hardcover.app integration status: In-progress per CWA v3 documentation
- Mitigation: Performance report includes Google Books fallback validation
- CWA auto-ingest noted as "implementation hack" in architecture.md - monitoring will catch failures

### File List

- Story file: `/docs/stories/story-1.2.md` (updated 2025-10-27)
- Performance report template: `/docs/STORY-1.2-PERFORMANCE-REPORT.md` (created 2025-10-27)
- Monitoring script: `/resources/scripts/monitor-resources-1.2.py` (created 2025-10-27)
- Docker configuration: `/docker-compose.yml` (reviewed, no changes needed)
