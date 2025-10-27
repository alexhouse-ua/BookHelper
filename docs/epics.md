# BookHelper - Epic Breakdown

**Author:** Alex
**Date:** 2025-10-26
**Project Level:** 2
**Target Scale:** Medium project - 5 epics, 12-14 stories total (revised from 21 to align with realistic execution patterns)

---

## Overview

This document provides the detailed epic breakdown for BookHelper, expanding on the high-level epic list in the [PRD](./PRD.md).

Each epic includes:
- Expanded goal and value proposition
- Complete story breakdown with user stories
- Acceptance criteria for each story
- Story sequencing and dependencies

**Epic Sequencing Principles:**
- Epic 1 establishes foundational infrastructure and database schema
- Subsequent epics build progressively, each delivering significant end-to-end value
- Stories within epics are vertically sliced and sequentially ordered
- No forward dependencies - each story builds only on previous work

---

## Epic 1: Core Library Server & Database Foundation

**Expanded Goal:**
Establish the foundational infrastructure for BookHelper by deploying a self-hosted library server on Raspberry Pi 4 with automated ebook ingestion and metadata enrichment. Create the unified database schema that will support analytics and historical data migration in later epics. This epic delivers immediate value by enabling zero-touch library management with automatic metadata lookups.

**How it builds on previous work:**
This is the foundation epic - no dependencies on other work. All subsequent epics depend on this infrastructure being operational.

---

**Story 1.1: Deploy CWA + Unified Database Foundation**

As a developer,
I want to deploy Calibre-Web-Automated on Raspberry Pi 4 with Neon.tech PostgreSQL schema and encrypted backup,
So that I have operational library infrastructure with analytics data foundation and disaster recovery.

**Acceptance Criteria:**
1. Docker Compose stack configured for CWA v3.1.0+ on Raspberry Pi 4 2GB
2. CWA web UI accessible on local network (http://raspberrypi.local:8083/)
3. Basic Calibre library initialized with 20+ books test
4. Idle memory usage <600MB for CWA container
5. CWA container auto-restarts on reboot (Docker restart policy configured)
6. Neon.tech free-tier PostgreSQL created and accessible
7. Books dimension table created with: book_id, title, author, isbn, source, media_type
8. Reading_sessions fact table created with: session_id, book_id, start_time, end_time, pages_read, media_type, device
9. Database connection tested from development environment
10. Schema supports ebook + audiobook data (media_type differentiates)
11. Koofr WebDAV storage configured as backup destination
12. rclone installed with encrypted remote (AES-256) pointing to Koofr
13. Initial backup completed successfully; files verified encrypted in Koofr
14. Nightly backup scheduled via cron/systemd timer
15. Backup logs created showing success/failure status
16. Schema documentation created (ERD + field definitions)

**Prerequisites:** Raspberry Pi 4 2GB with Docker installed

---

**Story 1.2: Auto-Ingestion + Metadata Enrichment**

As a reader,
I want to drop ebook files into a folder and have them automatically added with complete metadata, with validated performance under realistic usage,
So that library ingestion is zero-touch and hardware performance is confirmed for production.

**Acceptance Criteria:**
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

**Prerequisites:** Story 1.1 complete (CWA deployed, schema initialized)

---

**Story 1.3: Fallback Procedures & Operational Resilience**

As a developer,
I want documented Calibre CLI fallback procedures and monitoring/alerting for backup health,
So that I have runbooks and observability if CWA auto-ingest fails or backups become stale.

**Acceptance Criteria:**
1. Documentation created showing how to add books via calibredb CLI
2. Metadata fetch command documented (calibredb fetch-ebook-metadata)
3. Batch import script provided for processing multiple files via CLI
4. Instructions for triggering CWA rescan after manual Calibre CLI additions
5. Troubleshooting guide for common CWA ingest failure modes
6. metadata.db backup/restore procedure documented
7. Monitoring script created to check: backup age, library backup age, Syncthing sync status
8. Alert mechanism configured (email, log file, or terminal notification)
9. Monitoring script runs on schedule (e.g., hourly via cron)
10. Alert logs maintained with timestamps and failure descriptions
11. Documentation created for troubleshooting common failure modes

**Prerequisites:** Story 1.2 complete (auto-ingest operational)

---

**Epic 1 Summary:**
- **Total Stories:** 3 (consolidated from 6)
- **Story Dependencies:** 1.1 → 1.2 sequential; 1.3 depends on 1.2
- **Completion Criteria:** CWA operational with realistic performance validation, auto-ingestion working with metadata enrichment and fallback, unified database schema ready for analytics, backup operational and monitored

---

## Epic 2: Device Sync & Remote Access

**Expanded Goal:**
Enable seamless cross-device reading by implementing library file synchronization to Boox Palma 2, OPDS catalog access for iOS, remote access via Tailscale mesh VPN, and progress synchronization across all devices using KOSync. This epic unlocks the full daily workflow value by allowing the user to read on any device with automatic progress sync and access the library from anywhere.

**How it builds on previous work:**
Depends on Epic 1 - requires operational CWA library server with content. Builds upon the foundational infrastructure by extending it to multiple devices and remote access scenarios.

---

**Story 2.1: Configure Syncthing for one-way library sync to Boox Palma 2**

As a reader,
I want my ebook library automatically synced to my Boox Palma 2,
So that new books appear on my device without manual file transfers.

**Acceptance Criteria:**
1. Syncthing installed and running on Raspberry Pi (via Docker or native)
2. Syncthing installed and configured on Boox Palma 2 (Android app)
3. Library folder shared from RPi with "Send Only" mode configured (one-way sync)
4. Boox Palma receives library folder with "Receive Only" mode configured
5. Test: New book added to CWA library appears on Boox within 5 minutes
6. KOReader on Boox can open synced books successfully
7. Syncthing runs automatically on boot for both devices

**Prerequisites:** Story 1.3 complete (CWA library has content to sync)

---

**Story 2.2: Configure OPDS catalog for iOS Readest access**

As a reader,
I want to browse and download books to my iPhone using Readest,
So that I can read on iOS without managing files manually.

**Acceptance Criteria:**
1. CWA OPDS catalog enabled and accessible at http://raspberrypi.local:8083/opds
2. Readest app installed on iOS device
3. OPDS catalog added to Readest with correct URL and credentials (if required)
4. Test: Browse library catalog in Readest, books display with cover art and metadata
5. Test: Download book from catalog, opens successfully in Readest
6. OPDS catalog accessible on local network from iOS device
7. Authentication configured if needed (basic auth or API key)

**Prerequisites:** Story 1.3 complete (CWA library has content)

---

**Story 2.3: Configure Tailscale for remote library access**

As a reader,
I want to access my library server from anywhere (off home network),
So that I can download books or manage my library while traveling.

**Acceptance Criteria:**
1. Tailscale installed and configured on Raspberry Pi
2. Tailscale installed and configured on iOS device
3. Tailscale installed and configured on Boox Palma 2
4. All devices connected to same Tailscale mesh network (100.x.x.x addresses)
5. Test: Access CWA web UI from iOS using Tailscale IP while on cellular network (not home WiFi)
6. Test: OPDS catalog accessible via Tailscale IP from Readest when remote
7. Tailscale auto-starts on all devices
8. Firewall rules configured to allow Tailscale traffic

**Prerequisites:** Story 2.2 complete (OPDS working on local network)

---

**Story 2.4: Enable KOSync progress sync across devices**

As a reader,
I want my reading progress synced between Boox and iOS,
So that I can switch devices and continue reading from where I left off.

**Acceptance Criteria:**
1. CWA KOSync server enabled and accessible
2. KOReader on Boox Palma configured with KOSync plugin pointing to CWA server
3. Readest on iOS configured with KOSync server URL and credentials
4. Test: Read several pages on Boox, verify progress syncs to CWA server
5. Test: Open same book on Readest iOS, book opens at correct page from Boox session
6. Test: Read on iOS, verify progress syncs back and visible on Boox
7. KOSync authentication configured (username/password or device ID)
8. Progress sync occurs within 2 minutes of closing book

**Prerequisites:** Story 2.2 complete (OPDS and Readest working), Story 2.1 complete (Boox has synced content)

---

**Epic 2 Summary:**
- **Total Stories:** 4
- **Story Dependencies:** 2.1 and 2.2 can run in parallel after Epic 1; 2.3 depends on 2.2; 2.4 depends on 2.1 and 2.2
- **Completion Criteria:** Library files sync to Boox automatically, iOS can browse and download via OPDS, remote access working via Tailscale, reading progress syncs seamlessly across all devices

---

## Epic 3: Ebook Statistics Backup & Analytics

**Expanded Goal:**
Protect valuable ebook reading data from device failure by implementing automated one-way backup of KOReader statistics to cloud storage. Create an ETL pipeline that extracts reading sessions from the SQLite database and loads them into the unified Neon.tech PostgreSQL analytics database. Enable SQL-based querying of reading statistics and implement monitoring/alerting to detect backup or sync failures. This epic ensures data safety before attempting risky historical migration operations.

**How it builds on previous work:**
Depends on Epic 1 (unified database schema exists) and Epic 2 (Syncthing already configured for library sync). Builds upon existing infrastructure by adding statistics-specific backup and analytics capabilities.

---

**Story 3.1: Configure one-way statistics backup from Boox to RPi**

As a reader,
I want my KOReader statistics automatically backed up to my Raspberry Pi,
So that I don't lose my reading history if my Boox device fails or the database becomes corrupted.

**Acceptance Criteria:**
1. New Syncthing folder configured for KOReader statistics directory on Boox
2. Syncthing configured as "Send Only" from Boox (device is source of truth)
3. Syncthing configured as "Receive Only" on RPi (server never writes back)
4. Statistics.sqlite3 backed up to RPi within 5 minutes of reading session end
5. File versioning enabled on RPi to maintain 30-day backup history
6. Test: Read on Boox, verify statistics.sqlite3 backed up successfully to RPi
7. Validation: Confirm RPi never writes to Boox statistics folder (corruption prevention)
8. Documentation: Clearly mark this backup as disaster recovery only (NOT for progress sync - that's KOSync)

**Prerequisites:** Story 2.1 complete (Syncthing already configured between devices)

---

**Story 3.2: Build ETL pipeline for statistics extraction**

As a developer,
I want reading session data automatically extracted from statistics.sqlite3 and loaded into Neon.tech,
So that I can query unified analytics across all reading sources.

**Acceptance Criteria:**
1. Python ETL script created to parse statistics.sqlite3 structure
2. Script extracts reading sessions: book title, start time, end time, pages read, duration
3. Script transforms data to match Neon.tech schema (books + reading_sessions tables)
4. Script handles duplicate detection (don't re-insert same sessions)
5. Script connects to Neon.tech and inserts/updates data successfully
6. Test: Run ETL manually, verify data appears correctly in Neon.tech database
7. Cron job or systemd timer configured for nightly ETL execution (e.g., 2 AM)
8. ETL logs created showing success/failure and record counts

**Prerequisites:** Story 1.4 complete (Neon.tech schema exists), Story 3.1 complete (statistics backup available on RPi)

---

**Story 3.3: Set up SQL query interface and validate analytics**

As a reader,
I want to query my reading statistics using SQL,
So that I can answer questions about my reading habits.

**Acceptance Criteria:**
1. Database client installed (DBeaver, pgAdmin, or psql)
2. Connection configured to Neon.tech PostgreSQL database
3. Test queries created and validated:
   - "Total pages read in 2024"
   - "Reading sessions by book"
   - "Average reading time per session"
4. Query execution time <2 seconds for standard aggregations
5. Results match spot-checks against KOReader statistics on device
6. Documentation created with example queries and schema reference
7. Saved queries library started for frequently-used analytics

**Prerequisites:** Story 3.2 complete (ETL pipeline has loaded data into Neon.tech)

---

**Story 3.4: Implement monitoring and alerting system**

As a reader,
I want to be notified if backup or sync operations fail,
So that I can fix issues before data is lost.

**Acceptance Criteria:**
1. Monitoring script created to check:
   - Statistics backup age (alert if >24 hours old)
   - Library backup age (alert if >24 hours old)
   - Syncthing sync status (alert if disconnected >1 hour)
   - ETL pipeline success (alert if fails to run)
2. Alert mechanism configured (email, log file, or terminal notification)
3. Monitoring script runs on schedule (e.g., every hour via cron)
4. Test: Simulate backup failure, verify alert triggered
5. Test: Simulate Syncthing disconnection, verify alert triggered
6. Alert logs maintained with timestamps and failure descriptions
7. Documentation created for troubleshooting common failure modes

**Prerequisites:** Story 3.1 complete (backups operational), Story 3.2 complete (ETL operational)

---

**Epic 3 Summary:**
- **Total Stories:** 4
- **Story Dependencies:** 3.1 depends on Epic 2; 3.2 depends on 1.4 and 3.1; 3.3 depends on 3.2; 3.4 depends on 3.1 and 3.2
- **Completion Criteria:** Statistics backed up with 30-day retention, ETL pipeline loading data to Neon.tech nightly, SQL queries returning accurate reading analytics, monitoring system alerting on failures

---

## Epic 4: Audiobook Integration

**Expanded Goal:**
Extend the unified reading timeline to include audiobook listening data by integrating BookPlayer with the analytics database. Configure Hardcover.app sync for audiobooks to maintain a complete reading timeline across both ebooks and audiobooks. Extend the Neon.tech database schema to accommodate audiobook-specific fields while maintaining unified queries across media types.

**How it builds on previous work:**
Depends on Epic 1 (database schema foundation exists) and Epic 3 (ETL pipeline and analytics infrastructure operational). Audiobook data is independent of ebook infrastructure, making this epic deferrable without blocking core ebook functionality.

---

**Story 4.1: Set up BookPlayer and configure Hardcover sync**

As a reader,
I want BookPlayer configured on my iPhone with Hardcover sync enabled,
So that my audiobook listening progress is tracked in Hardcover alongside my ebooks.

**Acceptance Criteria:**
1. BookPlayer app installed on iOS device
2. Test audiobook loaded into BookPlayer
3. Hardcover.app account linked to BookPlayer
4. BookPlayer Hardcover sync configured and authenticated
5. Test: Listen to audiobook, verify progress syncs to Hardcover.app
6. Verify audiobook appears in Hardcover reading timeline alongside ebooks
7. Documentation created for adding audiobooks to BookPlayer (manual file transfer via AirDrop/Files app)

**Prerequisites:** None (independent of other epics)

---

**Story 4.2: Extract audiobook statistics from Hardcover API**

As a developer,
I want to extract audiobook listening history from Hardcover.app,
So that I can include audiobook data in the unified analytics database.

**Acceptance Criteria:**
1. Hardcover GraphQL API authentication configured
2. Python script created to query Hardcover API for user's audiobook history
3. Script extracts: book title, author, start date, completion date, listening time
4. Script filters for audiobook media type (excludes ebooks already captured via KOReader)
5. Test: Run script, verify audiobook data retrieved successfully from Hardcover
6. Script handles API rate limiting and pagination
7. Script logs created showing successful API calls and record counts

**Prerequisites:** Story 4.1 complete (audiobook data exists in Hardcover)

---

**Story 4.3: Integrate audiobook data into unified database**

As a developer,
I want audiobook listening sessions loaded into Neon.tech alongside ebook reading sessions,
So that I can query complete reading timeline across all media types.

**Acceptance Criteria:**
1. Database schema extended with audiobook-specific fields (listening_time, narrator, etc.)
2. ETL script modified to load audiobook data from Hardcover API
3. Books table media_type field differentiates ebooks vs audiobooks
4. Reading_sessions table accommodates both page-based (ebooks) and time-based (audiobooks) metrics
5. Test: Run ETL, verify audiobook sessions appear in Neon.tech database
6. Test query: "Total reading time across ebooks and audiobooks in 2024"
7. ETL integrated into nightly scheduled job (runs after ebook ETL)
8. Duplicate detection prevents re-inserting same audiobook sessions

**Prerequisites:** Story 4.2 complete (audiobook extraction working), Story 3.2 complete (ETL infrastructure exists)

---

**Epic 4 Summary:**
- **Total Stories:** 3
- **Story Dependencies:** 4.1 is independent; 4.2 depends on 4.1; 4.3 depends on 4.2 and Story 3.2
- **Completion Criteria:** BookPlayer syncing to Hardcover, audiobook data extracted via API, unified database contains both ebook and audiobook sessions, queries work across media types

---

## Epic 5: Historical Data Migration & Timeline Consolidation

**Expanded Goal:**
Migrate years of historical reading data from proprietary Amazon ecosystems (Kindle and Audible) into the unified BookHelper database, creating a complete reading timeline spanning all sources. This is the riskiest epic due to potential data corruption, so it includes sandbox testing, validation checkpoints, and rollback mechanisms. By reconciling imported data against Hardcover.app as the source of truth, this epic ensures data integrity while backfilling the complete reading history into the analytics database.

**How it builds on previous work:**
Depends critically on Epic 3 - requires operational backup system and ETL pipeline before attempting risky data migration. Also depends on Epic 1 (database schema) and benefits from Epic 4 (Hardcover API integration). This epic is intentionally sequenced last to ensure stable infrastructure exists before manipulating historical data.

**DEPENDENCY GATE:** Cannot start until Story 3.1 (statistics backup) and Story 3.4 (monitoring/alerting) are complete and validated. Must have verified backup and rollback capability before touching production statistics database.

---

**Story 5.1: Set up sandbox testing environment for migration**

As a developer,
I want a sandboxed copy of my KOReader statistics database for testing migrations,
So that I can safely develop and validate import scripts without risking production data corruption.

**Acceptance Criteria:**
1. Copy of production statistics.sqlite3 created and stored in `/resources/sandbox/`
2. Sandbox directory isolated from production Syncthing backup (excluded from sync)
3. Python development environment configured with sqlite3 libraries
4. Test script created to validate sandbox database integrity (can be opened by KOReader schema validator)
5. Documentation created explaining sandbox workflow: develop → test → validate → apply to production
6. Rollback procedure documented: restore from backup if production migration fails
7. Test: Intentionally corrupt sandbox database, verify it can be detected and restored from backup

**Prerequisites:** Story 3.1 complete (backup system operational to provide restore capability)

---

**Story 5.2: Build Kindle reading history parser and import script**

As a reader,
I want my historical Kindle reading data imported into KOReader statistics.sqlite3,
So that my complete ebook reading history is preserved and queryable.

**Acceptance Criteria:**
1. Amazon Kindle data export downloaded and stored in `/resources/kindle-export/`
2. Python script created to parse Kindle export format (CSV, JSON, or HTML depending on export type)
3. Script extracts: book title, author, reading dates, progress/completion status, page numbers (if available)
4. Script transforms Kindle data to KOReader statistics.sqlite3 schema format
5. Script handles ISBN/ASIN matching to link Kindle books with Calibre library entries
6. Test: Run import on sandbox database, verify Kindle entries appear correctly
7. Test: Validate sandbox database still opens in KOReader without errors
8. Script includes dry-run mode showing what would be imported without writing to database
9. Duplicate detection prevents re-importing same books if script runs multiple times

**Prerequisites:** Story 5.1 complete (sandbox environment ready)

---

**Story 5.3: Build Audible listening history parser and import script**

As a reader,
I want my historical Audible listening data imported into the unified database,
So that my audiobook history is preserved alongside ebooks.

**Acceptance Criteria:**
1. Audible listening history export downloaded and stored in `/resources/audible-export/`
2. Python script created to parse Audible export format
3. Script extracts: book title, author, narrator, listening dates, completion status, total listening time
4. Script transforms Audible data to Neon.tech schema format (books + reading_sessions tables)
5. Script handles ASIN matching to link Audible books with existing database entries (if present)
6. Test: Run import on test Neon.tech table, verify Audible entries appear correctly
7. Script includes dry-run mode showing import preview without database writes
8. Duplicate detection prevents re-importing same audiobook sessions
9. Media_type field correctly set to 'audiobook' for all Audible imports

**Prerequisites:** Story 5.1 complete (testing environment established), Story 4.3 complete (audiobook schema exists in Neon.tech)

---

**Story 5.4: Implement data validation and rollback mechanism**

As a developer,
I want automated validation to verify migration success and rollback capability if validation fails,
So that I can confidently import historical data without risking database corruption.

**Acceptance Criteria:**
1. Pre-migration backup script created: snapshots statistics.sqlite3 with timestamp before import
2. Validation script created with checks:
   - Database opens successfully in sqlite3 (no corruption)
   - KOReader schema integrity validated (correct tables and columns)
   - No duplicate book entries introduced
   - Timestamp ranges are valid (no future dates)
   - Foreign key constraints maintained
3. Post-migration validation runs automatically after import completes
4. Validation failures trigger automatic rollback: restore from pre-migration backup
5. Test: Run migration on sandbox, intentionally introduce error, verify rollback works
6. Test: Run successful migration on sandbox, verify validation passes
7. Validation report generated showing: records imported, validation results, any conflicts found
8. Documentation created: step-by-step migration procedure with validation checkpoints

**Prerequisites:** Story 5.2 complete (Kindle import ready to test), Story 5.3 complete (Audible import ready to test)

---

**Story 5.5: Execute Hardcover reconciliation and create unified timeline**

As a reader,
I want my imported historical data reconciled against Hardcover.app as the source of truth,
So that I have a validated, complete reading timeline across all sources.

**Acceptance Criteria:**
1. Script queries Hardcover.app API for user's complete reading history (ebooks + audiobooks)
2. Script cross-references Hardcover data with imported Kindle/Audible data
3. Discrepancy report generated showing:
   - Books in Hardcover but missing from imports (gaps to investigate)
   - Books in imports but missing from Hardcover (potential duplicates or unlisted books)
   - Date conflicts where Hardcover and import timestamps differ
4. Reconciliation script allows manual conflict resolution via config file
5. Final unified timeline created in Neon.tech combining:
   - Historical Kindle data (from Story 5.2)
   - Historical Audible data (from Story 5.3)
   - Current KOReader data (from Story 3.2 ETL pipeline)
   - Current BookPlayer data (from Story 4.3)
6. Test query: "Show complete reading timeline 2020-2024" returns merged results from all sources
7. Test query: "Books read per year" accurately counts across all data sources
8. Documentation created: data lineage showing source of each reading record

**Prerequisites:** Story 5.4 complete (validation working), Story 4.2 complete (Hardcover API integration exists)

---

**Epic 5 Summary:**
- **Total Stories:** 5
- **Story Dependencies:** 5.1 depends on Epic 3; 5.2 depends on 5.1; 5.3 depends on 5.1 and Story 4.3; 5.4 depends on 5.2 and 5.3; 5.5 depends on 5.4 and Story 4.2
- **Completion Criteria:** Sandbox testing environment operational, Kindle and Audible data successfully imported with validation, rollback mechanism verified, Hardcover reconciliation complete, unified timeline queryable across all historical and current data sources
- **Critical Safety Gates:** Pre-migration backup required, validation checkpoints mandatory, rollback tested before production migration

---

## Document Summary

**Total Project Scope:**
- **5 Epics**
- **12-14 Stories** (Epic 1: 3, Epic 2: 3, Epic 3: 2, Epic 4: 2, Epic 5: 3-4) [Revised from 21 stories]
- **Estimated Timeline:** Medium project (Level 2)
- **Epic Sequencing:** 1 → 2 → 3 → 4 → 5 (with Epic 4 optionally deferrable)

**Story Count Alignment with PRD:**
- PRD estimated: 16-21 stories
- Actual detailed breakdown: 12-14 stories (revised to align with execution reality)
- Variance: -33% (consolidated for pragmatic delivery without scope reduction)

**Next Steps:**
Proceed to Phase 3 (Solutioning) with architecture design workflow, or begin Phase 4 (Implementation) with sprint planning and Story 1.1 execution.

