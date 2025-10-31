# Story 3.2: Build ETL pipeline for statistics extraction

Status: ready-for-dev

## Story

As a developer,
I want reading session data automatically extracted from statistics.sqlite3 and loaded into Neon.tech,
So that I can query unified analytics across all reading sources.

## Acceptance Criteria

1. Python ETL script created to parse statistics.sqlite3 structure
2. Script extracts reading sessions: book title, start time, end time, pages read, duration
3. Script transforms data to match Neon.tech schema (books + reading_sessions tables)
4. Script handles duplicate detection (don't re-insert same sessions)
5. Script connects to Neon.tech and inserts/updates data successfully
6. Test: Run ETL manually, verify data appears correctly in Neon.tech database
7. Cron job or systemd timer configured for nightly ETL execution (e.g., 2 AM)
8. ETL logs created showing success/failure and record counts

## Tasks / Subtasks

- [ ] Task 1: Analyze statistics.sqlite3 schema and KOReader data structure (AC 1-2)
  - [ ] Load statistics.sqlite3 from Story 3.1 backup: `/home/alexhouse/backups/koreader-statistics/statistics.sqlite3`
  - [ ] Inspect KOReader schema: `.tables`, `.schema book`, `.schema page_stat_data` commands
  - [ ] Document KOReader table structure:
    - `book` table: id, title, authors, pages, language, series, md5 (file_hash)
    - `page_stat_data` table: id_book, start_time (Unix epoch), duration, page
  - [ ] Identify fields for reading session extraction: start_time, duration, page count
  - [ ] Note timezone handling: KOReader uses Unix timestamps (UTC)
  - [ ] Reference: [docs/guides/ETL-MAPPING-GUIDE.md § Source 1: KOReader statistics.sqlite3](../guides/ETL-MAPPING-GUIDE.md#source-1-koreader-statisticessqlite3-story-32---main)

- [ ] Task 2: Develop session aggregation and data transformation logic (AC 3-4)
  - [ ] Create Python ETL script: `/home/alexhouse/etl/extract_koreader_stats.py` (corrected path with alexhouse)
  - [ ] Implement KOReader extraction:
    - Query `book` table → books (title, authors, pages, file_hash)
    - Query `page_stat_data` table → aggregate into reading sessions
  - [ ] Implement session aggregation (30-minute gap threshold):
    - Group consecutive page_stat_data rows by book_id and time gaps
    - Calculate session: start_time, duration_minutes, pages_read (max page per session)
    - Reference: [docs/guides/ETL-MAPPING-GUIDE.md § Session Aggregation pseudocode](../guides/ETL-MAPPING-GUIDE.md#python-pseudocode-for-session-aggregation)
  - [ ] Transform to Neon.tech schema (Story 1.4 unified schema):
    - Books table: book_id (SERIAL), title, author_id (FK), file_hash, page_count, language, source='koreader'
    - Reading_sessions table: session_id (BIGSERIAL), book_id (FK), start_time, duration_minutes, pages_read, device='boox-palma-2', media_type='ebook', read_instance_id (UUID), read_number
    - Reference: [docs/guides/SCHEMA-DOCUMENTATION.md](../guides/SCHEMA-DOCUMENTATION.md)
  - [ ] Implement duplicate detection: UNIQUE(book_id, start_time, device) constraint with ON CONFLICT handling
  - [ ] Handle data types: Unix timestamps → PostgreSQL TIMESTAMP, pages → INT, duration → INT (minutes)

- [ ] Task 3: Implement Neon.tech database connectivity and schema validation (AC 5)
  - [ ] Verify Neon.tech PostgreSQL database exists and is accessible from RPi (test from alexhouse user)
  - [ ] Validate schema initialization:
    - Check tables: authors, publishers, books, reading_sessions, book_editions, sync_status
    - Check views: book_stats, reading_timeline, publisher_analytics, author_analytics, tandem_reading_sessions
    - Reference: [docs/guides/SCHEMA-DOCUMENTATION.md § Table Definitions](../guides/SCHEMA-DOCUMENTATION.md)
  - [ ] Test connection: `psql -h <neon-host> -U <user> -d <database>` (connection string from Story 1.4)
  - [ ] Store database credentials securely: environment variables (NEON_HOST, NEON_USER, NEON_PASSWORD, NEON_DATABASE)
  - [ ] Implement Python psycopg2 connection with error handling and retry logic
  - [ ] Reference existing test script: `resources/scripts/test_neon_connection.py`

- [ ] Task 4: Implement complete ETL script with transaction management (AC 6)
  - [ ] Complete Python ETL script with full error handling and logging:
    - Connection establishment with timeout and retry logic
    - Transaction management: BEGIN → INSERT/UPDATE → COMMIT/ROLLBACK
    - Dry-run mode (--dry-run flag) showing preview without database writes
    - Validation queries (count before/after)
  - [ ] Test manual execution: `python3 /home/alexhouse/etl/extract_koreader_stats.py`
  - [ ] Verify data in Neon.tech: `SELECT COUNT(*) FROM reading_sessions`
  - [ ] Validate sample accuracy: spot-check 5-10 session records against source statistics.sqlite3
  - [ ] Reference: [docs/guides/ETL-MAPPING-GUIDE.md § Validation & Testing](../guides/ETL-MAPPING-GUIDE.md#validation--testing)

- [ ] Task 5: Schedule nightly ETL execution with systemd timer (AC 7)
  - [ ] Create systemd service: `/etc/systemd/system/bookhelper-etl.service` (runs as alexhouse user)
  - [ ] Create systemd timer: `/etc/systemd/system/bookhelper-etl.timer` (trigger at 2 AM daily)
  - [ ] Alternative (legacy): cron job: `crontab -e` for alexhouse user → `0 2 * * * /home/alexhouse/etl/extract_koreader_stats.py >> /home/alexhouse/logs/etl.log 2>&1`
  - [ ] Test timer execution: `sudo systemctl start bookhelper-etl.timer` and monitor logs
  - [ ] Verify logs appear in timer's journal: `journalctl -u bookhelper-etl.service`
  - [ ] Confirm scheduled execution happens at designated time

- [ ] Task 6: Implement structured logging and monitoring (AC 8)
  - [ ] Add comprehensive logging to ETL script (reference: existing monitor-resources-1.2.py pattern):
    - Script start: timestamp, version, execution mode (normal/dry-run)
    - Database connection: host, user, status (success/failure)
    - KOReader extraction: records read from statistics.sqlite3, books/sessions extracted
    - Neon.tech load: records inserted, updated, skipped (duplicates), failed
    - Timing: duration, records/second throughput
    - Errors/warnings: detailed stack traces for debugging
  - [ ] Log file location: `/home/alexhouse/logs/etl.log` (with rotation: daily, max 10 MB, 7-day retention)
  - [ ] Log format: `[TIMESTAMP] [LEVEL] [COMPONENT] message` (e.g., `[2025-10-31 02:15:23] [INFO] [ETL] Starting extraction`)
  - [ ] Configure logrotate: `/etc/logrotate.d/bookhelper-etl` for automatic rotation
  - [ ] Reference: `resources/scripts/monitor-resources-1.2.py` for logging patterns

- [ ] Task 7: Create comprehensive ETL documentation and runbook (AC 8)
  - [ ] Create `docs/ETL-PIPELINE-SETUP.md` documenting:
    - Purpose: Extract KOReader statistics and load into Neon.tech PostgreSQL for analytics
    - Architecture: statistics.sqlite3 (Boox) → Syncthing → RPi backup → Python ETL → Neon.tech
    - Data flow: KOReader (book + page_stat_data) → session aggregation → Neon schema transformation → PostgreSQL insert
    - Schema mapping: Reference [docs/guides/ETL-MAPPING-GUIDE.md § Source 1 & 2](../guides/ETL-MAPPING-GUIDE.md)
    - Configuration: Database credentials, file paths, timing, logging
    - Manual execution: `python3 /home/alexhouse/etl/extract_koreader_stats.py --dry-run`
    - Systemd execution: `sudo systemctl start bookhelper-etl.service`
    - Troubleshooting: Common errors, connection issues, duplicate handling
    - Monitoring: Log location, query examples for validation
  - [ ] Include SQL validation queries:
    - Count sessions: `SELECT COUNT(*) FROM reading_sessions WHERE data_source = 'koreader'`
    - Books loaded: `SELECT COUNT(*) FROM books WHERE source = 'koreader'`
    - Latest sync: `SELECT last_sync_time FROM sync_status WHERE source_name = 'koreader'`
  - [ ] Include dry-run example output showing what would be loaded
  - [ ] Include troubleshooting section for common issues (connection timeouts, duplicate conflicts, etc.)

## Dev Notes

### Architecture Alignment

This story implements the **Analytics Layer** from the system architecture [Source: docs/architecture.md § 3.5. Analytics Layer]:

- **ETL Pipeline:** Nightly Python script reading statistics.sqlite3 backup and loading into Neon.tech
- **Data Warehouse:** Neon.tech PostgreSQL stores structured reading session data
- **Query Access:** SQL queries against analytics database enable reading habit analysis
- **Dependency Chain:** Depends on Story 3.1 (statistics backup available on RPi) and Story 1.1 (schema exists in Neon.tech)

### Project Structure Notes

- **Backup source:** `/home/alexhouse/backups/koreader-statistics/statistics.sqlite3` (from Story 3.1, corrected username)
- **ETL script location:** `/home/alexhouse/etl/extract_koreader_stats.py` (new, corrected path with alexhouse)
- **ETL logs:** `/home/alexhouse/logs/etl.log` (new, user-writable location)
- **Systemd service:** `/etc/systemd/system/bookhelper-etl.service` (runs as alexhouse)
- **Systemd timer:** `/etc/systemd/system/bookhelper-etl.timer` (triggers at 2 AM daily)
- **Configuration:** Environment variables for database credentials: NEON_HOST, NEON_USER, NEON_PASSWORD, NEON_DATABASE
- **Scripts reference:** `resources/scripts/` contains test and monitoring patterns:
  - `test_neon_connection.py` - Connection validation
  - `monitor-resources-1.2.py` - Logging and monitoring pattern
  - `test_schema_operations.py` - Schema interaction patterns
- **Documentation:** `docs/ETL-PIPELINE-SETUP.md` (new, to be created)
- **Schema references:**
  - `docs/guides/SCHEMA-DOCUMENTATION.md` (Story 1.4) - Complete schema definitions
  - `docs/guides/ETL-MAPPING-GUIDE.md` (Story 1.4) - ETL field mappings and procedures

### Technical Implementation Notes

- **Language:** Python 3.9+ (available on RPi running Raspbian)
- **Core Libraries:** sqlite3 (builtin), psycopg2 (for PostgreSQL), python-dotenv (for env var management)
- **Database Credentials:** Secure storage using environment variables (not hardcoded)
  - Set in `/home/alexhouse/.env` or systemd service file
  - Never commit credentials to git
- **Session Aggregation:** Implement 30-minute gap threshold for grouping consecutive page_stat_data rows (ref: ETL-MAPPING-GUIDE.md)
- **Duplicate Detection:** Use PostgreSQL `ON CONFLICT (book_id, start_time, device) DO NOTHING` constraint
- **Error Handling:** Comprehensive logging with retry logic for transient connection issues
  - API timeout: 30 seconds with 3 retries
  - Malformed data: Log warning, skip record, continue
  - Constraint violations: Log, skip, mark for manual review
- **Data Types Transformation:**
  - KOReader Unix timestamps (seconds) → PostgreSQL TIMESTAMP (UTC)
  - Page counts → INTEGER
  - Duration (minutes) → INTEGER
- **Performance:** Expected runtime <30 seconds for typical backup size (~100 MB, 2,000-10,000 sessions)
- **Testing:** Dry-run mode (--dry-run flag) for validation before writes

### Learnings from Previous Story (Story 3.1)

**From Story 3.1 (Status: review, completed 2025-10-30)**

Story 3.1 established the statistics backup system with one-way Syncthing sync from Boox to RPi. Key learnings critical to Story 3.2 implementation:

- **Statistics backup location confirmed:** `/home/alexhouse/backups/koreader-statistics/statistics.sqlite3` (verified working in Story 3.1, username is alexhouse not pi)
- **File sync is one-way and stable:** Story 3.1 verified Syncthing syncs within <1 minute, no missed syncs, checked 2025-10-30
- **File versioning is working:** RPi maintains 30-day backup history with Staggered retention for disaster recovery
- **Backup is reliable source:** One-way sync from Boox → RPi prevents any risk of corrupting source device's database
- **Separation of concerns:** Syncthing (file-level backup) is distinct from KOSync (progress synchronization across devices)
  - Don't confuse: statistics backup ≠ progress sync
  - Syncthing for data preservation, KOSync for device-to-device sync
- **Architecture validated:** One-way sync pattern prevents accidental overwrites [Source: docs/STATISTICS-BACKUP-SETUP.md]
- **Performance expectation:** ~2,700+ reading sessions per device

Key documentation from Story 3.1:
- `docs/STATISTICS-BACKUP-SETUP.md` explains backup configuration, file structure, and safety constraints
- `docs/stories/3-1-configure-one-way-statistics-backup-from-boox-to-rpi.md` full story details

[Source: Story 3.1 completion notes]

## Prerequisites

- ✓ **Story 1.4 Complete:** Neon.tech PostgreSQL schema fully initialized with unified database design
  - Tables: authors, publishers, books, reading_sessions, book_editions, sync_status
  - Views: book_stats, reading_timeline, publisher_analytics, author_analytics, tandem_reading_sessions
  - Schema reference: `docs/guides/SCHEMA-DOCUMENTATION.md` (2025-10-31)
- ✓ **Story 3.1 Complete:** Statistics backup available and operational at `/home/alexhouse/backups/koreader-statistics/statistics.sqlite3`
  - Syncthing one-way sync from Boox Palma 2 → RPi verified working
  - File versioning enabled with 30-day retention
- ✓ **Epic 1 Complete:** Calibre-Web-Automated (CWA) operational on RPi with Docker Compose
- ✓ **Epic 2 Partially Complete:** Device sync infrastructure (Syncthing, Tailscale, KOSync) operational
- **No blocking dependencies:** Story 3.2 is ready to implement

## References

### Schema & ETL Documentation
- [docs/guides/SCHEMA-DOCUMENTATION.md](../guides/SCHEMA-DOCUMENTATION.md) - Complete unified database schema (Story 1.4, 2025-10-31)
  - Table definitions, relationships, computed views, analytics queries
  - Reference for all field mappings in ETL
- [docs/guides/ETL-MAPPING-GUIDE.md](../guides/ETL-MAPPING-GUIDE.md) - ETL field mappings and procedures (Story 1.4, 2025-10-31)
  - Source 1: KOReader statistics.sqlite3 extraction and session aggregation
  - Source 2-6: Hardcover API, Kindle, Audible, historical data handling
  - Validation and testing procedures, troubleshooting guide
- [docs/STATISTICS-BACKUP-SETUP.md](../STATISTICS-BACKUP-SETUP.md) - Backup configuration details (Story 3.1)
  - Syncthing configuration, file versioning, safety constraints

### Story References
- [docs/epics.md § Epic 3 § Story 3.2](../epics.md#story-32-build-etl-pipeline-for-statistics-extraction) - Epic overview
- [docs/architecture.md § 3.5. Analytics Layer](../architecture.md#35-analytics-layer) - Architecture alignment
- [docs/stories/3-1-configure-one-way-statistics-backup-from-boox-to-rpi.md](./3-1-configure-one-way-statistics-backup-from-boox-to-rpi.md) - Prerequisite story (complete)

### Testing & Implementation Patterns
- [resources/scripts/test_neon_connection.py](../../resources/scripts/test_neon_connection.py) - Connection validation template
- [resources/scripts/test_schema_operations.py](../../resources/scripts/test_schema_operations.py) - Schema interaction patterns
- [resources/scripts/monitor-resources-1.2.py](../../resources/scripts/monitor-resources-1.2.py) - Logging and monitoring patterns

## Dev Agent Record

### Context Reference

- Story Context XML: `docs/stories/3-2-build-etl-pipeline-for-statistics-extraction.context.xml` (generated 2025-10-30)

### Agent Model Used

claude-haiku-4-5-20251001

### Debug Log References

### Completion Notes List

### File List
