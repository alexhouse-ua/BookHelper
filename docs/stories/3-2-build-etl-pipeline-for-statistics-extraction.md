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

- [ ] Task 1: Analyze statistics.sqlite3 schema (AC 1-2)
  - [ ] Load sample statistics.sqlite3 from Story 3.1 backup on RPi
  - [ ] Use sqlite3 CLI to inspect schema: `.tables`, `.schema` commands
  - [ ] Document table structure (reading_sessions, book references, timestamps)
  - [ ] Identify all relevant fields for reading analytics
  - [ ] Note any schema version differences or variations

- [ ] Task 2: Develop data transformation logic (AC 3-4)
  - [ ] Create Python script structure: `/home/pi/etl/extract_koreader_stats.py`
  - [ ] Implement SQLite3 query to extract: book_title, start_time, end_time, pages_read, duration_minutes
  - [ ] Transform KOReader schema fields to Neon.tech PostgreSQL schema:
    - Books table: (id, title, author, isbn, media_type, added_date)
    - Reading_sessions table: (id, book_id, start_time, end_time, pages_read, duration_minutes, device, device_name)
  - [ ] Implement duplicate detection: hash comparison or timestamp-based uniqueness check
  - [ ] Handle data types and timezone conversions

- [ ] Task 3: Implement Neon.tech database connectivity (AC 5)
  - [ ] Verify Neon.tech PostgreSQL database exists and is accessible from RPi
  - [ ] Validate schema exists: `books` and `reading_sessions` tables (from Story 1.1)
  - [ ] Test connection from RPi: `psql -h <neon-host> -U <user> -d <database>`
  - [ ] Store database credentials securely (environment variables, not hardcoded)
  - [ ] Implement Python psycopg2 connection in ETL script

- [ ] Task 4: Implement ETL execution and validation (AC 6)
  - [ ] Complete Python ETL script with error handling
  - [ ] Implement transaction management: begin → insert/update → commit/rollback
  - [ ] Add dry-run mode (show what would be loaded without writing)
  - [ ] Test ETL script manually: `python3 /home/pi/etl/extract_koreader_stats.py`
  - [ ] Verify data appears in Neon.tech: select count(*) from reading_sessions
  - [ ] Validate sample data accuracy (spot-check 5-10 records against source)

- [ ] Task 5: Schedule nightly ETL execution (AC 7)
  - [ ] Create systemd service file: `/etc/systemd/system/bookhelper-etl.service`
  - [ ] Create systemd timer file: `/etc/systemd/system/bookhelper-etl.timer` (2 AM daily)
  - [ ] Or configure cron job: `crontab -e` → `0 2 * * * /home/pi/etl/extract_koreader_stats.py >> /var/log/etl.log 2>&1`
  - [ ] Test timer/cron: verify execution at scheduled time
  - [ ] Verify logs appear in `/var/log/etl.log`

- [ ] Task 6: Implement logging and monitoring (AC 8)
  - [ ] Add structured logging to ETL script:
    - Start time, script version
    - Database connection status
    - Records extracted from statistics.sqlite3
    - Records inserted/updated to Neon.tech
    - Duplicates skipped (count)
    - Duration and completion status
    - Any errors or warnings encountered
  - [ ] Log file location: `/var/log/etl.log` (rotatable, max 10 MB, keep 7 days)
  - [ ] Log format: timestamp + severity (INFO/WARNING/ERROR) + message
  - [ ] Configure log rotation: `/etc/logrotate.d/bookhelper-etl` (daily, 7 days retention)

- [ ] Task 7: Documentation and runbook (AC 8)
  - [ ] Create `docs/ETL-PIPELINE-SETUP.md` documenting:
    - Purpose: Extract and load statistics to Neon.tech for analytics
    - Data flow diagram: statistics.sqlite3 → Python ETL → Neon.tech PostgreSQL
    - Schema mapping: KOReader fields → Neon.tech tables
    - Configuration: Database credentials, logging
    - Execution: Manual run vs. scheduled nightly
    - Troubleshooting: Common errors and recovery steps
    - Log monitoring: Where to check for issues
  - [ ] Include example SQL queries to validate loaded data
  - [ ] Include dry-run example showing preview without writes

## Dev Notes

### Architecture Alignment

This story implements the **Analytics Layer** from the system architecture [Source: docs/architecture.md § 3.5. Analytics Layer]:

- **ETL Pipeline:** Nightly Python script reading statistics.sqlite3 backup and loading into Neon.tech
- **Data Warehouse:** Neon.tech PostgreSQL stores structured reading session data
- **Query Access:** SQL queries against analytics database enable reading habit analysis
- **Dependency Chain:** Depends on Story 3.1 (statistics backup available on RPi) and Story 1.1 (schema exists in Neon.tech)

### Project Structure Notes

- Backup source: `/home/alexhouse/backups/koreader-statistics/statistics.sqlite3` (from Story 3.1)
- ETL script location: `/home/pi/etl/extract_koreader_stats.py` (new)
- Logging: `/var/log/etl.log` (new)
- Systemd service: `/etc/systemd/system/bookhelper-etl.service` and `.timer` (new)
- Configuration: Environment variables for database credentials (secure, not in git)
- Documentation: `docs/ETL-PIPELINE-SETUP.md` (new)

### Technical Implementation Notes

- **Language:** Python 3.9+ (available on RPi)
- **Libraries:** sqlite3 (builtin), psycopg2 (install with pip3)
- **Database Credentials:** Use environment variables `NEON_HOST`, `NEON_USER`, `NEON_PASSWORD`, `NEON_DATABASE`
- **Duplicate Detection:** Use `ON CONFLICT` clause in PostgreSQL INSERT or hash comparison before insert
- **Error Handling:** Log errors but don't fail silently; retry logic for transient connection issues
- **Performance:** Expected runtime <30 seconds for realistic backup size (typically <1 GB)

### Learnings from Previous Story (Story 3.1)

**From Story 3.1 (Status: review)**

Story 3.1 established the statistics backup system with one-way Syncthing sync from Boox to RPi. Key learnings that apply to Story 3.2:

- **Statistics backup location confirmed:** `/home/alexhouse/backups/koreader-statistics/statistics.sqlite3` (verified working in Story 3.1)
- **File sync is one-way and stable:** Story 3.1 verified Syncthing syncs within <1 minute, no missed syncs
- **File versioning is working:** RPi maintains 30-day backup history with Staggered versioning
- **Separation of concerns:** Story 3.1 emphasized that Syncthing (file-level) is for disaster recovery, NOT for progress sync (that's KOSync)
- **Architecture validated:** One-way sync pattern prevents corruption of source database [Source: docs/architecture.md § 4. Critical Warnings]

Key file from Story 3.1:
- Documentation created: `docs/STATISTICS-BACKUP-SETUP.md` explains the backup configuration and safety constraints

[Source: docs/stories/3-1-configure-one-way-statistics-backup-from-boox-to-rpi.md]

## Prerequisites

- ⏳ Story 1.4 Prerequisite: Neon.tech PostgreSQL schema must be initialized (books + reading_sessions tables)
- ✓ Story 3.1 Complete: Statistics backup available at `/home/alexhouse/backups/koreader-statistics/statistics.sqlite3`
- ✓ Epic 1: CWA operational, database schema initialized

**BLOCKING DEPENDENCY:** Story 1.4 (Unified Database Schema) must be complete before this story can be implemented. Currently blocked.

## References

- [docs/epics.md § Epic 3 § Story 3.2](../epics.md#story-32-build-etl-pipeline-for-statistics-extraction)
- [docs/architecture.md § 3.5. Analytics Layer](../architecture.md#35-analytics-layer)
- [docs/stories/3-1-configure-one-way-statistics-backup-from-boox-to-rpi.md](./3-1-configure-one-way-statistics-backup-from-boox-to-rpi.md)
- [docs/STATISTICS-BACKUP-SETUP.md](../STATISTICS-BACKUP-SETUP.md)
- Story 1.1 context: Neon.tech PostgreSQL database initialized

## Dev Agent Record

### Context Reference

- Story Context XML: `docs/stories/3-2-build-etl-pipeline-for-statistics-extraction.context.xml` (generated 2025-10-30)

### Agent Model Used

claude-haiku-4-5-20251001

### Debug Log References

### Completion Notes List

### File List
