# Technical Specification: Ebook Statistics Backup & Analytics

**Date:** 2025-10-30
**Author:** Alex
**Epic ID:** 3
**Status:** Draft

---

## Overview

Epic 3 implements the **Analytics Layer** from the approved BookHelper architecture, enabling deep reading statistics analysis and historical data preservation. This epic delivers a complete backup and analytics pipeline: one-way backup of KOReader statistics.sqlite3 from Boox to RPi (disaster recovery), nightly ETL pipeline extracting reading session data to Neon.tech PostgreSQL (aggregation warehouse), SQL query interface for analytics, and monitoring/alerting for backup health and pipeline status.

The infrastructure delivers analytics value by enabling questions like: "How many pages did I read in 2024?", "What is my average reading velocity?", "Which books took longest to finish?", and "What is my reading consistency across devices?"

---

## Objectives and Scope

### In Scope

- **Statistics Backup:** One-way Syncthing backup of KOReader statistics.sqlite3 from Boox to RPi with 30-day file versioning
- **ETL Pipeline:** Nightly Python script parsing statistics.sqlite3 and loading reading session data to Neon.tech PostgreSQL
- **Data Transformation:** Extract KOReader fields (timestamps, pages read, duration) → Neon.tech schema (books, reading_sessions tables)
- **Duplicate Detection:** ETL prevents re-inserting identical sessions on repeated runs
- **Query Interface:** SQL access to Neon.tech for analytics queries with <2 second response time
- **Monitoring & Alerting:** Health checks for backup freshness, ETL execution success/failure, and analytics database uptime
- **Schema Integration:** Neon.tech schema (from Story 1.4) serves as authoritative data warehouse

### Out of Scope

- Real-time streaming analytics (nightly batch processing only)
- Mobile app for analytics (SQL queries via DBeaver or pgAdmin sufficient for MVP)
- Historical data migration from Kindle/Audible (addressed in Epic 5)
- Audiobook statistics integration (addressed in Epic 4, Story 4.2)
- Advanced visualization/dashboarding (SQL interface sufficient for MVP)
- Automated reporting via email (manual query execution sufficient)

---

## System Architecture Alignment

This epic implements the **Analytics Layer** from the approved BookHelper architecture:

- **Data Safety:** One-way backup pattern (Syncthing Send Only) prevents corruption of source statistics.sqlite3
- **Modular Design:** ETL pipeline, query interface, and monitoring are independent, replaceable components
- **Data Ownership:** All data stored in standard formats (SQLite backup on RPi, PostgreSQL on Neon.tech); no vendor lock-in
- **Resilience:** Nightly ETL with 30-day backup retention enables recovery from missed ETL runs
- **Privacy-First:** All data remains private; Neon.tech is self-controlled PostgreSQL

**Alignment with Architecture Principles:**
- **Data Safety First:** Statistics backup is read-only on source device; ETL reads from RPi backup, never writes to Boox
- **Stability Over Features:** Uses proven tools (Syncthing for sync, Python for ETL, PostgreSQL for storage)
- **Modular Design:** Each story delivers independent value; can be implemented/replaced separately

[Source: docs/architecture.md § 3.5. Analytics Layer; docs/architecture.md § 1. System Architecture Philosophy]

---

## Detailed Design

### Services and Modules

| Service | Responsibility | Owner | Input | Output |
|---------|-----------------|-------|-------|--------|
| **KOReader** | Source of reading statistics | Boox Palma 2 device | Reading actions (open book, read pages, close book) | statistics.sqlite3 file (updated in real-time) |
| **Syncthing** | One-way backup of statistics to RPi | Docker container on RPi | Boox: Send Only folder; RPi: Receive Only folder | `/home/alexhouse/backups/koreader-statistics/statistics.sqlite3` on RPi |
| **ETL Pipeline** | Extract-Transform-Load reading session data | Python script on RPi | statistics.sqlite3 backup | Reading session records inserted to Neon.tech `reading_sessions` table |
| **Neon.tech PostgreSQL** | Analytics data warehouse | Cloud-hosted (free tier) | Reading session data from ETL | SQL query results for analytics |
| **Query Interface** | User-facing analytics access | DBeaver / pgAdmin / CLI | SQL queries | Query results (statistics about reading habits) |
| **Monitoring Script** | Health checks for backup/ETL | Python script on RPi (cron) | Backup age, ETL logs, database connection | Alert logs, health status |

---

### Data Models and Flow

#### Input: KOReader statistics.sqlite3 Schema (Source)

The source statistics.sqlite3 contains multiple tables; key tables for ETL extraction:

```
Table: documents
├── docfile (VARCHAR) — Book file path or title
├── page (INT) — Current page position
├── totalPages (INT) — Total pages in book
├── time (TIMESTAMP) — Last read timestamp
└── ... (other fields)

Table: doc_settings
├── document_id (FK to documents.docfile)
├── settings (JSON) — Book-specific settings
└── ... (other fields)
```

**ETL Challenge:** KOReader tracks cumulative page position, not session-based data. ETL must infer sessions from:
1. Time intervals between consecutive updates (e.g., >30 min gap = new session)
2. Page position resets (e.g., position went backward = new session or re-read)
3. Timestamp gaps (calculate session duration from start → end timestamps)

#### Output: Neon.tech PostgreSQL Schema (Warehouse)

**Books Dimension Table** (created in Story 1.4):
```sql
CREATE TABLE books (
  book_id SERIAL PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  author VARCHAR(255),
  isbn VARCHAR(20),
  source VARCHAR(50),  -- 'calibre', 'koreader', 'kindle', 'audible'
  media_type VARCHAR(20),  -- 'ebook', 'audiobook'
  page_count INT,
  published_date DATE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Reading Sessions Fact Table** (created in Story 1.4):
```sql
CREATE TABLE reading_sessions (
  session_id SERIAL PRIMARY KEY,
  book_id INT NOT NULL REFERENCES books(book_id),
  start_time TIMESTAMP NOT NULL,
  end_time TIMESTAMP,
  pages_read INT,
  duration_minutes INT,
  device VARCHAR(50),  -- 'boox', 'ios', 'kindle'
  media_type VARCHAR(20),  -- 'ebook', 'audiobook'
  device_stats_source VARCHAR(100),  -- 'statistics.sqlite3' for KOReader
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

  -- Constraints
  CONSTRAINT valid_pages CHECK (pages_read >= 0),
  CONSTRAINT valid_duration CHECK (duration_minutes >= 0),

  -- Indexes for performance
  INDEX idx_book_id (book_id),
  INDEX idx_start_time (start_time),
  INDEX idx_device (device)
);
```

#### ETL Transformation Logic (Story 3.2)

**Pipeline Steps:**
1. **Extract:** Read statistics.sqlite3 backup on RPi
   - Query documents table for all books with reading history
   - Query doc_settings for page position and timestamps

2. **Transform:** Infer reading sessions from KOReader data
   - Algorithm: Group consecutive page updates by time gaps
   - If time gap > 30 minutes, mark as new session
   - Calculate session metrics: start_time, end_time, pages_read, duration_minutes

3. **Lookup:** Match KOReader book titles to Neon.tech books table
   - Query books table for matching title/author
   - If no match, create new book record (with media_type='ebook')

4. **Load:** Insert session records to reading_sessions table
   - Use PostgreSQL `ON CONFLICT` to prevent duplicate inserts
   - Uniqueness key: (book_id, start_time, pages_read)
   - If duplicate detected, skip insert and log

5. **Validate:** Spot-check sample records
   - Compare 5-10 records against source statistics.sqlite3
   - Verify timestamps, page counts, durations are accurate

---

### Story Workflows

#### Story 3.1: Configure one-way statistics backup from Boox to RPi

**Goal:** Establish reliable backup of reading statistics with disaster recovery capability.

**Design:**
- Syncthing folder configured on Boox as "Send Only" (source of truth stays on device)
- Syncthing folder configured on RPi as "Receive Only" (server never modifies)
- File versioning enabled on RPi with Staggered retention (30-day history)
- One-way sync pattern prevents device from receiving corrupted version if server has issue

**Success Criteria:**
- statistics.sqlite3 syncs from Boox to RPi within 5 minutes of reading session end
- RPi maintains 30-day rolling backup history
- Corruption prevention: RPi cannot write back to Boox

**Status:** REVIEW (completed, awaiting peer review)

---

#### Story 3.2: Build ETL pipeline for statistics extraction

**Goal:** Automate nightly extraction of reading session data from backup to analytics warehouse.

**Design:**
- Python script reads statistics.sqlite3 backup (read-only)
- Infers reading sessions from KOReader timestamps and page positions
- Transforms to Neon.tech schema (books + reading_sessions tables)
- Handles duplicates using PostgreSQL ON CONFLICT
- Nightly execution via systemd timer (2 AM)
- Structured logging: start time, connection status, records extracted, records inserted, errors

**Success Criteria:**
- ETL script parses statistics.sqlite3 schema correctly
- Reads session data extracted with <30 second runtime
- Duplicate detection prevents re-insertion on repeated runs
- Manual test run verifies data appears in Neon.tech
- Nightly execution scheduled and verified
- Logs created showing success/failure metrics

**Status:** DONE (completed 2025-10-31, 27-test suite 100% passing)

**Blocking Dependency:** Story 1.4 (Neon.tech schema must exist before ETL can insert data)

---

#### Story 3.3: Integrate Hardcover API metadata and enrich books table

**Goal:** Enrich books dimension table with Hardcover API metadata (author, publisher, cover image, rating) and establish data source consolidation.

**Design:**
- Authenticate with Hardcover.com API using personal library export
- Query Hardcover API for all books in personal library
- Extract metadata: author, publisher, ISBN, rating, cover URL, publication date
- Transform to Neon.tech books table schema (story 1.4)
- Match books by ISBN (primary) or title+author (fallback)
- Handle duplicates: Prefer Hardcover metadata over KOReader minimal metadata
- Create data source mapping: Track which book metadata came from which source (koreader, hardcover, calibre)
- Structured logging: Books matched, books enriched, API call counts, errors

**Acceptance Criteria:**
1. Hardcover API authentication and connection validation
2. Personal library query and book extraction from Hardcover
3. Metadata transformation to Neon.tech books schema
4. ISBN-based matching between Hardcover and existing books
5. Data enrichment: Update books table with Hardcover metadata (author_id, publisher_id, rating, cover_url)
6. Fallback matching: Title+author matching when ISBN unavailable
7. Data source tracking: Record which books came from Hardcover vs KOReader
8. Manual execution and validation: Dry-run mode, sample verification

**Success Criteria:**
- Hardcover API connection established and authenticated
- All books from Hardcover library extracted and matched
- Books table enriched with complete metadata (author, publisher, rating, cover)
- Duplicate detection prevents overwriting KOReader minimal data with empty Hardcover fields
- Manual test run verifies enriched data in Neon.tech
- Structured logging shows match statistics and any failures
- Documentation explains API usage, authentication, and enrichment strategy

**Status:** READY-FOR-DEV (story drafted with full context, ready for implementation)

**Blocking Dependency:** Story 3.2 (ETL must be operational; Hardcover enriches the books table created by ETL)

**Technical Notes:**
- Hardcover API: Free personal library export available at https://hardcover.app/settings/integrations
- API rate limiting: Reasonable limits for small personal library (<500 books)
- Data enrichment strategy: Preserve KOReader fields; add Hardcover fields; use Hardcover as authoritative for metadata
- Author/Publisher dimension: Insert new authors/publishers if not in dimension tables

---

#### Story 3.4: Set up SQL query interface and validate analytics

**Goal:** Enable user to query analytics database and validate data accuracy.

**Design:**
- No application code; use DBeaver or pgAdmin for SQL access to Neon.tech
- Provide example queries:
  - Total pages read in calendar year: `SELECT SUM(pages_read) FROM reading_sessions WHERE YEAR(start_time) = 2024`
  - Average reading velocity: `SELECT AVG(pages_read/duration_minutes) FROM reading_sessions`
  - Books by device: `SELECT device, COUNT(*) FROM reading_sessions GROUP BY device`
  - Reading consistency: `SELECT DATE(start_time), COUNT(*) FROM reading_sessions GROUP BY DATE(start_time)`

- Document Neon.tech schema with field definitions
- Performance validation: Verify <2 second query response time
- Data accuracy validation: Spot-check 10-20 records against source statistics.sqlite3

**Success Criteria:**
- DBeaver/pgAdmin connection to Neon.tech documented
- 10+ example queries provided with explanations
- Query performance validated (<2 sec for typical analytics queries)
- Data accuracy validated (spot-check results match source)
- Schema documentation with field meanings

**Status:** BACKLOG (planned, not yet drafted)

---

#### Story 3.5: Implement monitoring and alerting system

**Goal:** Detect backup and ETL pipeline failures before data loss occurs.

**Design:**
- Monitoring script runs hourly via cron
- Checks:
  1. **Backup Freshness:** Is statistics.sqlite3 on RPi less than 24 hours old?
  2. **ETL Execution:** Did nightly ETL script complete successfully?
  3. **Database Uptime:** Can PostgreSQL connection be established?
  4. **Record Count Trend:** Are reading_sessions records growing as expected (at least 1 new session per week)?

- Alert Mechanisms:
  - Log file: `/var/log/bookhelper-monitoring.log` (rotated daily)
  - Console alert: Print warning if checks fail
  - Email alert (optional): Send notification on critical failure

**Success Criteria:**
- Monitoring script created and executable
- All 4 health checks implemented
- Alert logs created showing status and any failures
- Monitoring runs hourly without errors
- Documentation explaining alerts and response procedures

**Status:** BACKLOG (planned, not yet drafted)

---

### Workflows and Sequencing

```
Epic 2: Device Sync Complete
  ↓
Story 1.4: Design Neon.tech Schema (Epic 1, parallel track)
  ↓ (schema created)
  ↓
Story 3.1: Configure Statistics Backup (Syncthing)
  ↓ (backup established)
  ↓
Story 3.2: Build ETL Pipeline
  ├─ Input: statistics.sqlite3 backup from 3.1
  ├─ Output: reading_sessions in Neon.tech schema from 1.4
  ↓ (pipeline operational)
  ↓
Story 3.3: Integrate Hardcover API
  ├─ Enriches books table from 3.2
  ├─ Adds metadata: author, publisher, rating, cover
  ↓ (books table enriched with Hardcover metadata)
  ↓
Story 3.4: SQL Query Interface
  ├─ Access enriched analytics in Neon.tech from 3.2+3.3
  ↓ (queries working with enriched metadata)
  ↓
Story 3.5: Monitoring & Alerting
  ├─ Monitor 3.1 (backup freshness)
  ├─ Monitor 3.2 (ETL execution)
  ├─ Monitor 3.3 (Hardcover API sync)
  ├─ Monitor Neon.tech (database uptime)
  ↓ (Epic 3 complete)
```

**Sequencing Logic:**
- 3.1 (backup) and 1.4 (schema) are independent; can proceed in parallel
- 3.2 (ETL) depends on both 3.1 and 1.4; must proceed after both
- 3.3 (Hardcover API) depends on 3.2; enriches books created by ETL
- 3.4 (query) depends on 3.2 and 3.3; requires working ETL + enriched metadata
- 3.5 (monitoring) depends on 3.1, 3.2, and 3.3; monitors all components

---

### Performance & Constraints

#### ETL Pipeline Performance

| Metric | Target | Notes |
|--------|--------|-------|
| Extract time | <5 sec | Read statistics.sqlite3 on local RPi storage |
| Transform time | <10 sec | Session inference algorithm |
| Load time | <15 sec | Insert to Neon.tech PostgreSQL |
| **Total runtime** | **<30 sec** | Total end-to-end for typical 200-book library |
| Memory footprint | <200 MB | Streaming/batch processing, not full load into memory |
| Duplicate detection accuracy | 100% | ON CONFLICT or hash-based comparison |

#### Backup Performance

| Metric | Target | Notes |
|--------|--------|-------|
| Sync latency | <5 min | Syncthing one-way from Boox to RPi |
| Backup retention | 30 days | Staggered file versioning on RPi |
| Storage overhead | ~200-500 MB | 30-day history of ~200-500 KB statistics.sqlite3 |

#### Query Performance

| Metric | Target | Notes |
|--------|--------|-------|
| Query response time | <2 sec | Neon.tech PostgreSQL with indexes on (book_id, start_time, device) |
| Concurrent connections | 2-3 | Free tier limit; sufficient for analytics queries |

---

## Critical Warnings

### Data Integrity in ETL

**Risk:** ETL parsing of KOReader statistics.sqlite3 is complex; incorrect session inference could produce invalid analytics.

**Mitigation:**
1. **Spot-check validation:** Manually verify 10-20 records against source statistics.sqlite3
2. **Duplicate detection:** Prevent re-insertion of identical sessions
3. **Logging:** Log all inferred sessions with decision reasoning for audit trail
4. **Dry-run mode:** Implement `--dry-run` flag to show what would be loaded without writing

### One-Way Backup Integrity

**Risk:** If Boox device receives backup (corrupted) version from RPi, statistics.sqlite3 on device could be permanently corrupted.

**Mitigation:**
- Syncthing configured as Send Only on Boox (cannot receive)
- Syncthing configured as Receive Only on RPi (cannot send back)
- Configuration verified and locked during Story 3.1

[Source: docs/architecture.md § 4. Critical Warnings - SQLite Corruption Risk]

---

## Dependencies & Blockers

### Story 3.2 (ETL Pipeline) Blockers

- **Story 1.4 (Unified Schema)** — BLOCKER: Neon.tech schema (books + reading_sessions tables) must exist before ETL can insert data
  - **Status:** Done ✅
  - **Impact:** 3.2 requires target schema

### Story 3.3 (Hardcover API Enrichment) Blockers

- **Story 3.2 (ETL Pipeline)** — BLOCKER: ETL must create books table with KOReader data before Hardcover enrichment can match and update
  - **Status:** Done ✅ (2025-10-31)
  - **Impact:** 3.3 depends on 3.2 populating books table

### Story 3.4 (Query Interface) Blockers

- **Story 3.2 + Story 3.3** — BLOCKER: ETL must populate reading_sessions, and Hardcover must enrich books table before queries return meaningful results
  - **Status:** 3.2 done ✅, 3.3 ready-for-dev → Must complete 3.3 before 3.4 can validate enriched metadata

### Story 3.5 (Monitoring) Blockers

- **Story 3.1 + 3.2 + 3.3** — DEPENDENCY: Monitoring checks backup freshness, ETL execution, and Hardcover sync; all must exist
  - **Status:** 3.1 review, 3.2 done ✅, 3.3 ready-for-dev → All must be operational before 3.5 begins

---

## References

- [docs/architecture.md § 3.5. Analytics Layer](../architecture.md#35-analytics-layer-mvp)
- [docs/architecture.md § 4. Critical Warnings - SQLite Corruption Risk](../architecture.md#critical-warning-sqlite-corruption-risk)
- [docs/PRD.md § FR013 - Unified Database with nightly ETL](../PRD.md)
- [docs/tech-spec-epic-1.md § Data Models (Neon.tech Schema)](../tech-spec-epic-1.md#data-models-and-contracts)
- [docs/stories/3-1-*](../stories/3-1-configure-one-way-statistics-backup-from-boox-to-rpi.md)
- [docs/stories/3-2-*](../stories/3-2-build-etl-pipeline-for-statistics-extraction.md)
- [docs/STATISTICS-BACKUP-SETUP.md](../STATISTICS-BACKUP-SETUP.md)

---

## Appendix: Example ETL Session Inference Algorithm

```python
# Pseudo-code: Session inference from KOReader timestamps

def infer_sessions(koreader_records):
    """
    Input: List of (timestamp, page_position, book_title) from statistics.sqlite3
    Output: List of (start_time, end_time, pages_read, duration_minutes)
    """
    sessions = []
    current_session = None

    for record in sorted_by_timestamp(koreader_records):
        time, pages, title = record

        if current_session is None:
            # Start new session
            current_session = {
                'start_time': time,
                'book': title,
                'start_pages': pages
            }
        elif time - current_session['last_time'] > 30 * 60:
            # Gap > 30 minutes: end current session, start new
            sessions.append(finalize_session(current_session, current_session['last_time'], current_session['last_pages']))
            current_session = {
                'start_time': time,
                'book': title,
                'start_pages': pages
            }
        elif pages < current_session['last_pages']:
            # Pages went backward: assume re-read or new session
            sessions.append(finalize_session(current_session, current_session['last_time'], current_session['last_pages']))
            current_session = {
                'start_time': time,
                'book': title,
                'start_pages': pages
            }

        current_session['last_time'] = time
        current_session['last_pages'] = pages

    # Finalize last session
    if current_session:
        sessions.append(finalize_session(current_session, current_session['last_time'], current_session['last_pages']))

    return sessions

def finalize_session(session, end_time, end_pages):
    """Convert partial session data to final session record"""
    duration_minutes = (end_time - session['start_time']).total_seconds() / 60
    pages_read = max(0, end_pages - session['start_pages'])

    return {
        'book': session['book'],
        'start_time': session['start_time'],
        'end_time': end_time,
        'pages_read': pages_read,
        'duration_minutes': duration_minutes
    }
```

---

**Document Status:** Ready for Story Implementation

**Next Steps:**
1. Story 3.2 (ETL) implementation can begin once Story 1.4 (schema) is complete
2. Story 3.3 (query interface) can begin after Story 3.2 produces data
3. Story 3.4 (monitoring) can begin after Stories 3.1 and 3.2 are operational
