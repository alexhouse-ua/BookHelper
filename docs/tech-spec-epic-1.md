# Technical Specification: Core Library Server & Database Foundation

Date: 2025-10-26
Author: Alex
Epic ID: 1
Status: Draft

---

## Overview

Epic 1 establishes the foundational infrastructure for BookHelper by deploying a self-hosted library server (Calibre-Web-Automated) on a Raspberry Pi 4 2GB with automated ebook ingestion and Hardcover metadata enrichment. This epic creates the unified PostgreSQL database schema that will support analytics aggregation and historical data migration in subsequent epics. The infrastructure delivers immediate value by reducing library management overhead from 15-30 minutes per book to <1 minute per book through zero-touch automated metadata lookups and cross-device synchronization setup.

## Objectives and Scope

### In Scope

- **Infrastructure:** Deploy Calibre-Web-Automated v3.1.0+ in Docker Compose on Raspberry Pi 4 2GB
- **Library Management:** Configure CWA with persistent Calibre database, web UI accessible on local network
- **Auto-Ingestion:** Implement monitored folder workflow with <30 second ingestion time from file drop to library availability
- **Metadata Enrichment:** Configure Hardcover.app as primary metadata provider; implement Google Books fallback
- **Performance Validation:** Execute load tests with 100+ ebook library to validate hardware adequacy
- **Database Foundation:** Design unified PostgreSQL schema supporting ebook + audiobook reading sessions analytics
- **Backup Infrastructure:** Configure rclone + Koofr for nightly encrypted library backup
- **Fallback Procedures:** Document Calibre CLI commands for manual ingestion if CWA auto-ingest fails

### Out of Scope

- OPDS catalog configuration (addressed in Epic 2, Story 2.2)
- KOSync progress synchronization (addressed in Epic 2, Story 2.4)
- Audiobook integration (addressed in Epic 4)
- ETL pipeline implementation (addressed in Epic 3, Story 3.2)
- Historical data migration (addressed in Epic 5)
- Tailscale remote access (addressed in Epic 2, Story 2.3)

## System Architecture Alignment

This epic implements the **Library Management Layer** and **Data Layer** foundations from the approved BookHelper architecture:

- **Hardware:** Raspberry Pi 4 2GB resource constraints drive implementation choices (memory monitoring, async background tasks)
- **Core Services:** Calibre-Web-Automated Docker container with KOSync server embedded; Syncthing for file distribution
- **Data Storage:** Neon.tech PostgreSQL schema design for downstream analytics (Epic 3) and historical migration (Epic 5)
- **Backup Strategy:** Aligned with "Data Safety First" principle—rclone one-way backup to Koofr as cloud disaster recovery layer
- **Metadata:** Hardcover.app provider integration per architecture specification; fallback to Google Books ensures completeness

## Detailed Design

### Services and Modules

| Service | Responsibility | Owner | Input | Output |
|---------|-----------------|-------|-------|--------|
| **Calibre-Web-Automated** | Library server providing web UI, metadata db, KOSync server, auto-ingest trigger | Docker container (v3.1.0+) | Docker Compose config, Calibre library folder | HTTP API on port 8083, metadata.db, synced ebook files to Syncthing |
| **Syncthing** | File synchronization daemon; distributes library to devices | Docker container | rclone config, library folder path | Synced library files to configured remote folders |
| **rclone** | Encrypted backup agent; syncs library + config to Koofr | Systemd service/cron job | Koofr WebDAV credentials, local library path | Encrypted backups in Koofr storage |
| **Metadata Enrichment Pipeline** | Hardcover API lookups during auto-ingest; Google Books fallback | CWA built-in + custom script hooks | ISBN/title/author from file metadata | Enriched book records: title, author, cover art, description, page count |
| **Hardware Monitor Script** | Reports CPU/memory usage during operations for validation | Python script (cron job) | /proc/meminfo, /proc/stat | Log file with resource metrics; alerts if thresholds exceeded |

### Data Models and Contracts

#### Calibre Metadata Database (CWA `metadata.db`)

SQLite database containing:
- **Books table:** book_id (PK), title, authors, series, language, isbn, lccn, cover_path, pubdate, comments
- **Data table:** book (FK to books), data_type (e.g., EPUB, PDF), uncompressed_size, name
- **Custom columns:** Any user-defined metadata fields (e.g., "Genre", "Rating")

#### Neon.tech PostgreSQL Schema (Analytics Foundation)

**Books Dimension Table:**
```sql
CREATE TABLE books (
  book_id SERIAL PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  author VARCHAR(255),
  isbn VARCHAR(20),
  asin VARCHAR(20),  -- For Audible linking
  source VARCHAR(50),  -- 'calibre', 'kindle', 'hardcover', 'audible'
  media_type VARCHAR(20),  -- 'ebook' or 'audiobook'
  cover_url TEXT,
  page_count INT,
  duration_minutes INT,  -- For audiobooks
  published_date DATE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Reading Sessions Fact Table:**
```sql
CREATE TABLE reading_sessions (
  session_id SERIAL PRIMARY KEY,
  book_id INT NOT NULL REFERENCES books(book_id),
  start_time TIMESTAMP NOT NULL,
  end_time TIMESTAMP,
  pages_read INT,  -- Nullable for audiobooks
  duration_minutes INT,  -- Nullable for ebooks
  device VARCHAR(50),  -- 'boox', 'ios', 'pc'
  media_type VARCHAR(20),  -- 'ebook' or 'audiobook'
  device_stats_source VARCHAR(100),  -- Path to source file (e.g., statistics.sqlite3)
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_reading_sessions_book ON reading_sessions(book_id);
CREATE INDEX idx_reading_sessions_time ON reading_sessions(start_time);
```

#### Backup Manifest (Koofr)

Encrypted backup structure:
- `/books/` — Ebook EPUB/PDF files
- `/metadata.db` — Calibre database
- `/compose.yml` — Docker Compose configuration
- `/backup-manifest.json` — Backup metadata (timestamp, file count, checksum)

### APIs and Interfaces

#### Calibre-Web-Automated HTTP API

**Library Browse:**
- `GET /api/books` — List all books in library (pagination support)
- `GET /api/books/{book_id}` — Get book metadata and file location
- Response: JSON with book details, cover URL, download links

**Metadata Enrichment Hook:**
- `POST /api/metadata/enrich` — Trigger metadata lookup via Hardcover API
- Input: ISBN or title + author
- Output: Enriched metadata object or error

**KOSync Server (Embedded):**
- Progress sync protocol on port 8083/kosync
- Device clients: KOReader (Boox), Readest (iOS)
- Transactions: Read/write progress to in-memory cache, periodic flush to metadata.db

#### Syncthing Discovery Protocol

- **Discovery Server:** Default Syncthing discovery (user can self-host for full privacy)
- **Folder Share:** Library folder shared as "Send & Receive" from RPi; "Receive Only" on devices
- **Conflict Resolution:** Newer timestamp wins; conflicts logged

#### rclone WebDAV Interface

- **Protocol:** WebDAV over HTTPS to Koofr API
- **Authentication:** WebDAV username/password from Koofr account
- **Encryption:** rclone crypt remote with AES-256 encryption
- **Bandwidth:** Daily sync; estimated 1-10 GB depending on library size

### Workflows and Sequencing

#### Story 1.1: Deploy CWA on Raspberry Pi 4

**Sequence:**
1. User prepares RPi: Install OS (Raspberry Pi OS Lite), configure SSH, install Docker
2. User creates Docker Compose stack with CWA v3.1.0, Syncthing, rclone service configs
3. User starts services: `docker compose up -d`
4. Services initialize: CWA creates metadata.db, Syncthing generates device ID
5. User accesses CWA web UI: `http://raspberrypi.local:8083/` (mDNS auto-discovery)
6. User tests with 20+ books: Import sample library, verify web UI responsiveness
7. User configures auto-restart: `restart_policy: always` in Docker Compose

**Preconditions:** RPi 4 2GB with Docker installed; 50 GB storage (ebook library)

#### Story 1.2: Performance Validation

**Load Test Sequence:**
1. Test environment: 100+ ebook library (representative size)
2. Baseline measurement: Record memory/CPU before operations
3. CWA library scan: Trigger full library scan via web UI; monitor resource usage
4. Concurrent operations: Simulate simultaneous user access (metadata lookups, file downloads)
5. Stress test: 500+ book bulk import; monitor for memory exhaustion or crashes
6. Decision point: If memory < 1.5 GB total usage → Pass; else recommend upgrade
7. Document findings: Create report with observed resource patterns

**Acceptance:** System sustains 100+ book library with metadata operations under 1.5 GB peak memory

#### Story 1.3: Auto-Ingestion Workflow Configuration

**Sequence:**
1. Create monitored folder: `/library/ingest/` on RPi
2. Configure CWA auto-ingest: Point to ingest folder in CWA web UI settings
3. Configure metadata provider: Select "Hardcover.app" as primary, "Google Books" as fallback
4. Test metadata resolution:
   - Drop EPUB with ISBN → Hardcover API lookup succeeds
   - Drop EPUB without ISBN → Google Books fallback succeeds
5. Enable EPUB optimization: CWA epub-fixer enabled
6. Test ingestion: Drop test EPUB → Verify in Calibre library within 30 seconds with enriched metadata
7. Configure Hardcover API: Authenticate if required (check API limits)

**Timing:** File drop → CWA detects → Metadata lookup → Library import = <30 seconds

#### Story 1.4: Unified Database Schema Design

**Sequence:**
1. Design phase: Review Epic 3/5 requirements to ensure schema supports analytics/migration
2. Create Neon.tech account: Set up free-tier PostgreSQL database
3. Implement schema: Create books + reading_sessions tables with proper indexes
4. Test connection: `psycopg2` connection test from development environment
5. Document schema: Create entity-relationship diagram and field definitions
6. Validation query: Test example aggregations (total pages by month, books per year)

**Deliverable:** Schema documentation + connection string for ETL pipeline (Epic 3)

#### Story 1.5: Library Backup to Koofr

**Sequence:**
1. Create Koofr account: Obtain WebDAV credentials
2. Install rclone: Configure crypt remote with AES-256 encryption
3. Test backup: `rclone sync /library/ koofr:library/`
4. Create systemd timer: Schedule nightly backups (3 AM default)
5. Configure retention: Enable file versioning on Koofr (30-day default)
6. Test restore: Download backup, verify library integrity
7. Monitor: Backup logs created for success/failure tracking

**Backup Manifest:** Timestamp, file count, checksum recorded in backup-manifest.json

#### Story 1.6: Calibre CLI Fallback Documentation

**Sequence:**
1. Document basic operations: `calibredb add`, `calibredb fetch-ebook-metadata`, `calibredb list`
2. Create bulk import script: Python script accepting directory of EPUBs, batch import via calibredb
3. Document troubleshooting: Common CWA ingest errors and CLI workarounds
4. Test fallback: Simulate CWA ingest failure, verify calibredb CLI can recover
5. Document metadata.db backup/restore procedure for disaster recovery

**Deliverable:** CLI fallback guide in project documentation

## Non-Functional Requirements

### Performance

- **Library Ingestion:** <30 seconds from file drop to library availability (including metadata lookup)
- **CWA Web UI:** <2 second page load time for library browsing (50+ books)
- **Metadata Lookup:** <10 seconds per ISBN via Hardcover API with fallback to Google Books
- **Memory Efficiency:** Peak memory usage <1.5 GB during normal operations (100+ book library); idle <600 MB
- **Backup Window:** Nightly backup completes within 2 hours (estimated 1-10 GB depending on library size)

**Measurement:** Observe during Story 1.2 load test; document in validation report

### Security

- **Data Encryption:** Library backup encrypted in transit (HTTPS) and at rest (rclone AES-256) on Koofr
- **Metadata Enrichment:** Hardcover API calls over HTTPS; credentials stored in environment variables or Docker secrets
- **Local Network Access:** CWA web UI accessible only on local network (mDNS); no public internet exposure
- **Database Credentials:** Neon.tech connection string stored securely (environment variables, not in code)
- **Sync Verification:** Syncthing device IDs verified before folder sharing to prevent unauthorized access

**Threat Mitigations:**
- One-way backup (Koofr) prevents corrupted data from overwriting live library
- KOSync server embedded in CWA (no separate network exposure)
- Hardcover API rate limiting accepted; falls back to Google Books if exceeded

### Reliability/Availability

- **Uptime Target:** 99%+ for library access (NFR001 from PRD)
- **Service Restart:** Docker `restart_policy: always` ensures services auto-recover from crashes
- **Data Redundancy:**
  - Primary: On-disk library on RPi
  - Secondary: Syncthing replica on Boox Palma 2 (receive-only)
  - Tertiary: Encrypted backup on Koofr (nightly)
- **Failure Scenarios:**
  - RPi network outage → Boox/iOS can continue reading from local copies
  - RPi storage failure → Restore from Koofr backup
  - Metadata provider outage → Fallback to Google Books
  - CWA crash → Auto-restart via Docker policy

### Observability

- **Resource Monitoring:** CPU/memory metrics logged hourly via custom script; alerts if >80% usage
- **Backup Logs:** rclone logs recorded with timestamp, file count, success/failure status
- **Metadata Enrichment:** CWA logs capture API calls, failures, and fallback attempts
- **Syncthing Logs:** Standard Syncthing event logs (available in web UI and system logs)
- **Access Logs:** CWA HTTP access logs for debugging connectivity issues

**Log Retention:** 30 days minimum; older logs archived or deleted

## Dependencies and Integrations

### External Services

| Service | Version | Purpose | Dependency Type |
|---------|---------|---------|-----------------|
| **Hardcover.app API** | v1.0 | Metadata enrichment | Optional (fallback to Google Books) |
| **Google Books API** | v1.0 | Metadata fallback | Optional (fallback to manual entry) |
| **Koofr WebDAV** | HTTPS | Encrypted backup storage | Required (disaster recovery) |
| **Neon.tech PostgreSQL** | Free-tier | Analytics database schema foundation | Required (future epics) |

### Local Dependencies

| Component | Version | Purpose |
|-----------|---------|---------|
| Docker | 20.10+ | Container runtime |
| Docker Compose | 1.29+ | Multi-container orchestration |
| Calibre-Web-Automated | 3.1.0+ | Library server + KOSync |
| Syncthing | 1.20+ | File synchronization |
| rclone | 1.60+ | Encrypted backup tool |
| Python | 3.8+ | Monitoring/fallback scripts |

### Environment Variables

```bash
# Hardcover API (if required)
HARDCOVER_API_KEY=<key>

# Koofr WebDAV credentials (for rclone)
KOOFR_USERNAME=<username>
KOOFR_PASSWORD=<password>

# Neon.tech PostgreSQL connection (for future ETL)
DATABASE_URL=postgresql://<user>:<password>@<host>:<port>/<database>

# CWA admin credentials
CWA_ADMIN_USER=<admin_username>
CWA_ADMIN_PASSWORD=<secure_password>
```

## Acceptance Criteria (Authoritative)

All criteria from epics.md Stories 1.1–1.6, synthesized here:

1. ✓ **Story 1.1:** Docker Compose stack for CWA v3.1.0+ configured on RPi 4 2GB
2. ✓ **Story 1.1:** CWA web UI accessible on local network (http://raspberrypi.local:8083/)
3. ✓ **Story 1.1:** Basic Calibre library initialized and accessible through web interface
4. ✓ **Story 1.1:** Idle memory usage <600 MB for CWA container
5. ✓ **Story 1.1:** Test library scan (20+ books) completes without crashes or OOM
6. ✓ **Story 1.1:** CWA container auto-restarts on reboot (Docker restart policy)
7. ✓ **Story 1.2:** Load test with 100+ ebook library completed successfully
8. ✓ **Story 1.2:** Memory usage during scan <1.5 GB total (leaving ~500 MB buffer)
9. ✓ **Story 1.2:** Metadata fetch operations complete without timeouts/crashes
10. ✓ **Story 1.2:** Hardware validation report created with resource patterns
11. ✓ **Story 1.2:** Go/no-go decision documented (continue RPi 4 OR upgrade to RPi 5)
12. ✓ **Story 1.3:** CWA auto-ingest configured to monitor ingest folder
13. ✓ **Story 1.3:** Hardcover.app metadata provider configured as primary
14. ✓ **Story 1.3:** Google Books configured as fallback provider
15. ✓ **Story 1.3:** Test ebook auto-imported within 30 seconds with enriched metadata
16. ✓ **Story 1.3:** Imported book has title, author, cover art, description, page count
17. ✓ **Story 1.3:** EPUB optimization (epub-fixer) enabled
18. ✓ **Story 1.3:** Hardcover API authentication configured/validated (if required)
19. ✓ **Story 1.4:** Neon.tech free-tier PostgreSQL created and accessible
20. ✓ **Story 1.4:** Books dimension table designed with fields: book_id, title, author, isbn, source, media_type
21. ✓ **Story 1.4:** Reading_sessions fact table designed with: session_id, book_id, start_time, end_time, pages_read, media_type, device
22. ✓ **Story 1.4:** Schema supports ebook + audiobook data (media_type differentiates)
23. ✓ **Story 1.4:** Database connection tested from development environment
24. ✓ **Story 1.4:** Tables created with proper indexes on common query fields
25. ✓ **Story 1.4:** Schema documentation created (ERD + field definitions)
26. ✓ **Story 1.5:** Koofr WebDAV storage configured as backup destination
27. ✓ **Story 1.5:** rclone installed with encrypted remote (AES-256)
28. ✓ **Story 1.5:** Backup script syncs library (CWA → Koofr, one-way)
29. ✓ **Story 1.5:** Backup excludes temp files; includes library ebooks + metadata.db
30. ✓ **Story 1.5:** Initial backup completed successfully; files verified in Koofr
31. ✓ **Story 1.5:** Cron/systemd timer configured for nightly backups
32. ✓ **Story 1.5:** Backup logs created (success/failure status)
33. ✓ **Story 1.6:** Calibre CLI documentation created (calibredb add, fetch-ebook-metadata, list)
34. ✓ **Story 1.6:** Bulk import script provided for multiple files
35. ✓ **Story 1.6:** CWA rescan trigger instructions documented
36. ✓ **Story 1.6:** Troubleshooting guide for common CWA ingest failures
37. ✓ **Story 1.6:** metadata.db backup/restore procedure documented

## Traceability Mapping

| AC ID | PRD FR | Spec Section | Component | Test Idea |
|-------|--------|--------------|-----------|-----------|
| 1-6 | FR005 | Library Management | CWA | Deploy stack, verify web UI accessibility, monitor memory |
| 7-11 | FR005 | Performance | Load Test | Stress 100+ books, measure memory/CPU, document limits |
| 12-18 | FR005 | Auto-Ingestion | Hardcover API | Drop EPUB, verify metadata enrichment <30s |
| 19-25 | FR013 | Data Layer | Neon.tech Schema | Create tables, test connectivity, run example queries |
| 26-32 | FR009 | Backup | rclone+Koofr | Configure backup, verify encryption, test restore |
| 33-37 | FR005 | Fallback | Calibre CLI | Simulate CWA failure, test calibredb fallback |

## Risks, Assumptions, Open Questions

### Risks

1. **CWA Auto-Ingest Stability** (HIGH IMPACT, MEDIUM LIKELIHOOD)
   - **Risk:** Former contributor noted auto-ingest is a "hack"; may fail unpredictably
   - **Mitigation:** (a) Monitor CWA logs for ingest errors; (b) Calibre CLI fallback documented and tested
   - **Acceptance:** Feature benefits outweigh risk for MVP
   - **Escalation:** If failures frequent, switch to manual calibredb workflow

2. **RPi 4 2GB Memory Constraint** (MEDIUM IMPACT, LOW LIKELIHOOD)
   - **Risk:** Large library scans or concurrent metadata lookups could exhaust 2 GB RAM
   - **Mitigation:** (a) Story 1.2 load test validates memory headroom; (b) Monitor via cron script; (c) USB swap as short-term workaround; (d) RPi 5 upgrade as long-term solution
   - **Decision Gate:** Story 1.2 must pass with <1.5 GB peak usage

3. **Hardcover API Rate Limiting** (LOW IMPACT, MEDIUM LIKELIHOOD)
   - **Risk:** Bulk metadata lookups may hit Hardcover API rate limits
   - **Mitigation:** Fallback to Google Books API; cache metadata locally; spread lookups across time
   - **Acceptance:** Occasional fallback to Google Books acceptable

4. **SQLite Corruption Risk** (CRITICAL IMPACT, LOW LIKELIHOOD)
   - **Risk:** File-level sync (Syncthing) of live statistics.sqlite3 could cause corruption
   - **Mitigation:** MANDATORY: (a) Syncthing configured one-way ONLY for backup (Boox → RPi); (b) KOSync used ONLY for live progress sync; (c) Never bidirectional sync statistics.sqlite3
   - **Enforcement:** Architecture review before Story 1.1 deployment

### Assumptions

1. **Internet Connectivity:** RPi has stable internet connection for metadata APIs and Koofr backups
2. **Koofr API:** WebDAV endpoint remains stable; free tier provides sufficient storage (10 GB)
3. **Hardcover API:** Available and responsive; acceptable rate limits for one user
4. **Docker Runtime:** RPi Docker installation completed per system prerequisites
5. **mDNS Availability:** Local network supports mDNS discovery (raspberrypi.local hostname)
6. **User Technical Proficiency:** User comfortable with Docker Compose, SSH, command-line tools

### Open Questions

1. **Hardcover API Authentication:** Requires API key? Free vs. paid tier? Document in Story 1.3
2. **Metadata Enrichment Performance:** Actual response time from Hardcover API? Acceptable latency budget?
3. **Backup Scheduling:** Should backup run at fixed time (3 AM) or on-demand? Consider RPi usage patterns
4. **Library Size Scalability:** Tested only to 100 books. Will schema/CWA handle 1000+ books? Plan future validation
5. **Format Support:** Beyond EPUB/PDF, what other formats should CWA support? Impacts EPUB optimization step

## Test Strategy Summary

### Test Levels

1. **Unit Testing:** Not applicable (mostly configuration + existing tools)
2. **Integration Testing:**
   - CWA + Syncthing: Verify file sync to remote folders
   - CWA + Hardcover API: Metadata lookup success rate, fallback to Google Books
   - rclone + Koofr: Backup creation, encryption verification, restore capability
   - Neon.tech: Connection test, schema validation, example queries
3. **System Testing:**
   - End-to-end ingestion: File drop → Metadata enrichment → Library availability
   - Load testing: 100+ book library with concurrent metadata lookups (Story 1.2)
   - Failure scenarios: CWA crash, network outage, backup failure, metadata provider outage
4. **Acceptance Testing:**
   - All AC criteria verified manually by user (Alex)

### Test Coverage

**Story 1.1:**
- [ ] Docker Compose stack starts without errors
- [ ] CWA web UI accessible on local network (mDNS hostname)
- [ ] Idle memory <600 MB observed in monitoring logs
- [ ] Test library (20+ books) imported and browsable

**Story 1.2:**
- [ ] 100+ book library load test completed
- [ ] Peak memory <1.5 GB confirmed
- [ ] No crashes or OOM during scan
- [ ] Metadata operations complete within timeout

**Story 1.3:**
- [ ] Auto-ingest folder monitored; new EPUB detected
- [ ] Hardcover API lookup succeeds with ISBN
- [ ] Fallback to Google Books succeeds without ISBN
- [ ] Book imported with enriched metadata within 30 seconds
- [ ] EPUB optimization applied

**Story 1.4:**
- [ ] Neon.tech PostgreSQL connection successful
- [ ] Schema tables created with proper structure
- [ ] Example queries execute successfully
- [ ] Connection string documented

**Story 1.5:**
- [ ] rclone backup runs and completes
- [ ] Files encrypted in Koofr storage
- [ ] Restoration from backup successful
- [ ] Systemd timer scheduled correctly

**Story 1.6:**
- [ ] Calibre CLI commands document runnable
- [ ] Bulk import script processes directory correctly
- [ ] CWA rescan updates library after CLI import
- [ ] Troubleshooting guide covers common errors

### Edge Cases

- Empty ebook file (0 bytes)
- Oversized EPUB (>500 MB)
- Metadata not found in Hardcover or Google Books
- Duplicate ISBN entries in library
- Metadata provider API timeout (>30 seconds)
- Syncthing network disconnection during backup
- Koofr storage quota exceeded
- Concurrent metadata requests during bulk import

---

**Document Status:** Draft for Scrum Master Review
**Next Review:** After SM approval, proceed to Story 1.1 implementation
