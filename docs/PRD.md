# BookHelper Product Requirements Document (PRD)

**Author:** Alex
**Date:** 2025-10-26
**Project Level:** 2
**Target Scale:** Medium project - multiple epics, 10+ stories total

---

## Goals and Background Context

### Goals

- **Data Preservation:** Successfully migrate 100% of Kindle and Audible historical data into unified database without loss or corruption
- **Automation Excellence:** Reduce library management overhead from 15-30 min/book to <1 min/book (95%+ reduction in manual effort)
- **Infrastructure Resilience:** Implement automated backup with 99%+ uptime protecting reading statistics from device failure
- **Unified Reading Timeline:** Create consolidated view of ebook and audiobook reading history enabling data-driven insights

### Background Context

BookHelper addresses critical infrastructure gaps faced by privacy-conscious readers transitioning from proprietary ecosystems (Amazon Kindle/Audible) to open-source alternatives (KOReader, self-hosted tools). The project tackles three interconnected problems: (1) years of historical reading data trapped in proprietary formats with no migration path, (2) valuable reading statistics at risk due to lack of automated backup, and (3) significant manual overhead for library management and cross-device synchronization.

Having successfully transitioned to privacy-focused hardware (Boox Palma 2 + KOReader), the infrastructure gaps are now critical blockers—without automated solutions, the window to migrate historical data closes while daily manual library management remains unsustainable for long-term use.

---

## Requirements

### Functional Requirements

**Foundation Layer (Independent Components):**

- **FR001:** System shall parse and import 100% of Kindle reading history from Amazon data exports into KOReader-compatible statistics.sqlite3 format
- **FR002:** System shall parse and import 100% of Audible listening history from Audible exports into unified database
- **FR003:** System shall automatically backup KOReader statistics.sqlite3 to cloud storage with one-way sync (device as source of truth) maintaining 30-day retention minimum
- **FR004:** System shall sync reading progress across devices using CWA KOSync server (application-aware protocol)
- **FR005:** System shall automatically ingest ebooks through monitored folder with Hardcover API metadata enrichment and format optimization

**Integration Layer (Single Dependencies):**

- **FR006:** System shall validate migrated data integrity using non-destructive testing and provide rollback capability if validation fails *(Depends on: FR001, FR002)*
- **FR007:** System shall provide remote library access via Tailscale mesh VPN with OPDS protocol support for iOS *(Depends on: FR005)*
- **FR008:** System shall sync library files to Boox Palma 2 via Syncthing (one-way: server → device) *(Depends on: FR005)*
- **FR009:** System shall backup library files to separate storage from primary PC to prevent data loss *(Depends on: FR005)*
- **FR010:** System shall integrate audiobook statistics from BookPlayer into unified database
- **FR011:** System shall sync audiobook reading progress to Hardcover.app via BookPlayer native integration *(Depends on: FR010)*

**Aggregation Layer (Multiple Dependencies):**

- **FR012:** System shall reconcile imported data against Hardcover.app as source of truth for reading records *(Depends on: FR001, FR002, FR006)*
- **FR013:** System shall maintain unified database (Neon.tech PostgreSQL) consolidating ebook and audiobook reading data via nightly ETL pipeline with automated conflict resolution for multi-device updates *(Depends on: FR003, FR010)*

**Query & Monitoring Layer (User-Facing):**

- **FR014:** System shall provide SQL query interface for reading statistics (e.g., "total pages read in 2024") with <2 second response time *(Depends on: FR013)*
- **FR015:** System shall monitor backup operations, sync status, and library health with automated alerting for failures *(Depends on: FR003, FR008, FR009)*

### Non-Functional Requirements

- **NFR001:** System shall maintain 99%+ uptime for backup and sync operations to prevent data loss
- **NFR002:** Library ingestion workflow shall complete in <30 seconds from file drop to device availability
- **NFR003:** System shall operate with $0 ongoing costs using free-tier cloud services and open-source tools only

---

## User Journeys

### Journey 1: Adding a New Ebook and Reading Across Devices

**Actor:** Alex (primary user)
**Goal:** Add a new ebook and seamlessly read it across Boox Palma 2 and iOS devices with automatic metadata and sync

**Flow:**

1. **Acquisition:** User downloads ebook file (EPUB/PDF) to PC
2. **Ingestion:** User drops file into monitored folder
   - System detects new file within seconds
   - CWA auto-ingest triggers Hardcover API metadata lookup
   - System enriches metadata (title, author, cover art, page count, ratings)
   - System optimizes format if needed
   - Book added to Calibre library database
3. **Sync to Devices:**
   - **Boox Palma 2:** Syncthing automatically syncs library folder (one-way from server)
   - **iOS:** User opens Readest app, browses OPDS catalog, book appears instantly
4. **Reading on Boox:**
   - User opens book in KOReader
   - Reads several chapters, KOReader tracks progress in statistics.sqlite3
   - KOSync automatically syncs progress to CWA server
5. **Cross-Device Continuity:**
   - User switches to iOS Readest
   - Readest pulls latest progress from KOSync server
   - Book opens at exact page where user left off on Boox
6. **Statistics Backup:**
   - User finishes reading session on Boox
   - Syncthing detects statistics.sqlite3 change
   - One-way backup to RPi completes within 5 minutes
   - Nightly ETL pipeline extracts reading session data to Neon.tech
7. **Progress Sync to Hardcover:**
   - KOReader hardcoverapp.koplugin updates reading progress to Hardcover.app
   - Reading timeline visible in Hardcover alongside audiobooks

**Success Criteria:**
- Total time from file drop to device availability: <30 seconds
- Progress sync across devices: within 2 minutes
- Zero manual metadata lookups required
- Statistics backup: within 5 minutes of reading session end

---

### Journey 2: Historical Data Migration and Validation

**Actor:** Alex (one-time migration)
**Goal:** Migrate years of Kindle and Audible reading history into unified database without data loss

**Flow:**

1. **Export Historical Data:**
   - User requests Amazon Kindle data export (via privacy settings)
   - User requests Audible listening history export
   - Exports saved to `resources/` folder
2. **Pre-Migration Backup:**
   - System creates backup of current KOReader statistics.sqlite3
   - Backup stored with timestamp for rollback capability
3. **Kindle Data Import:**
   - User triggers FR001 migration script
   - System parses Kindle export (reading history, progress, timestamps)
   - Transforms to KOReader statistics.sqlite3 compatible format
   - Inserts historical entries without modifying existing data
4. **Audible Data Import:**
   - User triggers FR002 migration script
   - System parses Audible export (listening history, completion dates)
   - Loads into unified database (Neon.tech PostgreSQL)
5. **Data Validation (FR006):**
   - System runs integrity checks on statistics.sqlite3
   - Validates KOReader can still read database (non-destructive verification)
   - Checks for duplicate entries or timestamp conflicts
   - **Decision Point:** If validation fails → automatic rollback to backup
6. **Hardcover Reconciliation (FR012):**
   - System queries Hardcover.app API for user's complete reading history
   - Cross-references imported Kindle/Audible data with Hardcover records
   - Identifies discrepancies (books in Hardcover but not in exports)
   - Flags overlapping fields for manual review if conflicts exist
7. **Unified Timeline Creation:**
   - ETL pipeline consolidates Kindle + Audible + KOReader data
   - Creates continuous reading timeline in Neon.tech database
   - Ebooks and audiobooks merged chronologically
8. **Validation Query:**
   - User runs test query: "Show all books read in 2023"
   - System returns combined results from historical imports + recent KOReader data
   - User spot-checks against personal records/Hardcover

**Success Criteria:**
- 100% of Kindle and Audible history imported without data loss
- Zero corruption of existing KOReader statistics
- Successful rollback capability demonstrated
- Unified timeline queryable with complete historical coverage

---

### Journey 3: Querying Reading Statistics

**Actor:** Alex (ongoing analytics use)
**Goal:** Answer questions about reading habits using unified database

**Flow:**

1. **User Has Question:**
   - Example: "How many pages did I read in 2024?"
   - Example: "What's my average reading speed by genre?"
   - Example: "Total listening time for audiobooks this year?"
2. **Access Query Interface:**
   - User opens database client (DBeaver, pgAdmin, or psql CLI)
   - Connects to Neon.tech PostgreSQL database
3. **Execute SQL Query:**
   - User writes or uses saved query:
     ```sql
     SELECT SUM(pages_read) FROM reading_sessions
     WHERE session_date >= '2024-01-01' AND session_date < '2025-01-01'
     AND media_type = 'ebook';
     ```
   - Query executes in <2 seconds (NFR per FR014)
4. **Review Results:**
   - System returns aggregated statistics
   - Data includes both historical imports and recent reading
   - Covers ebooks (KOReader) and audiobooks (BookPlayer)
5. **Cross-Reference Validation:**
   - User compares result with Hardcover.app timeline
   - Checks if major books are accounted for
   - Investigates any discrepancies using drill-down queries
6. **Save Query for Reuse:**
   - User saves frequently-used queries as SQL scripts
   - Builds personal analytics query library over time

**Alternative Flow - Complex Analytics:**
1. User wants multi-dimensional analysis: "Reading velocity by genre over time"
2. Writes JOIN query combining books dimension + sessions facts
3. System returns tabular results
4. User exports to CSV for visualization in external tool (Phase 2: built-in dashboards)

**Success Criteria:**
- Query response time: <2 seconds for standard queries
- Data accuracy: matches Hardcover.app timeline within expected variance
- Complete coverage: ebooks + audiobooks + historical imports all queryable
- No data gaps in unified timeline

---

## UX Design Principles

- **Automation First:** Minimize user touchpoints; system operates in background with zero manual intervention for routine operations
- **Data Transparency:** All data accessible and exportable in standard formats (SQLite, PostgreSQL, CSV) with no proprietary lock-in
- **Error Visibility:** Clear alerts when backups or syncs fail through monitoring system (FR015)
- **Non-Destructive Operations:** Rollback capability for critical operations (migration) to prevent data loss

---

## User Interface Design Goals

**Platform & Screens:**
- **Primary Interfaces:** Command-line scripts (Python/Bash) for migration and ETL operations
- **Web UI:** Calibre-Web-Automated responsive interface for library management and metadata editing
- **Database Access:** SQL clients (DBeaver, pgAdmin, psql) for analytics queries
- **Monitoring:** Log files and automated alert notifications for system health
- **No Custom UI Development:** Leverage existing tool interfaces (CWA, KOReader, Readest, BookPlayer)

**Design Constraints:**
- Must work within Calibre-Web-Automated's existing UI framework (no custom modifications)
- Database queries require SQL knowledge (acceptable for single technical user)
- Command-line comfort assumed (user is technically proficient)
- No mobile app development (uses KOReader, Readest, BookPlayer as-is)

---

## Epic List

**Epic 1: Core Library Server & Database Foundation**
- **Goal:** Deploy self-hosted library server with automated ingestion and establish unified database schema
- **Value Delivered:** Working library management system; ebooks automatically enriched with metadata and accessible via web UI
- **Estimated stories:** 4-5 stories
- **Key deliverables:** CWA deployment on Raspberry Pi 4 with performance validation, auto-ingestion with Hardcover metadata, unified database schema design (Neon.tech), library backup to separate storage, CWA fallback documentation
- **Risk Mitigation:** Hardware validation checkpoint, Calibre CLI fallback documented

**Epic 2: Device Sync & Remote Access**
- **Goal:** Enable cross-device reading with progress sync and remote library access
- **Value Delivered:** Read on any device (Boox, iOS) with seamless progress sync; access library from anywhere
- **Estimated stories:** 3-4 stories
- **Key deliverables:** Syncthing library sync (RPi → Boox), OPDS catalog for iOS access, Tailscale remote access, KOSync progress sync across devices

**Epic 3: Ebook Statistics Backup & Analytics**
- **Goal:** Implement automated statistics backup and analytics database for ebook reading data
- **Value Delivered:** Ebook reading data protected from loss and queryable via SQL for insights
- **Estimated stories:** 3-4 stories
- **Key deliverables:** Statistics backup (one-way Syncthing to RPi with 30-day retention), ETL pipeline (statistics.sqlite3 → Neon.tech), SQL query interface (pgAdmin/DBeaver), monitoring/alerting system
- **MVP Scope:** Direct SQL queries only; dashboards deferred to Phase 2

**Epic 4: Audiobook Integration**
- **Goal:** Integrate audiobook statistics and sync into unified reading timeline
- **Value Delivered:** Audiobooks tracked alongside ebooks in unified database; Hardcover sync for complete reading timeline
- **Estimated stories:** 2-3 stories
- **Key deliverables:** BookPlayer setup and configuration, audiobook stats extraction, Hardcover.app sync integration, unified database schema extension for audiobook fields

**Epic 5: Historical Data Migration & Timeline Consolidation**
- **Goal:** Migrate historical Kindle/Audible data and create complete unified reading timeline spanning all sources
- **Value Delivered:** Complete reading history accessible in unified database with validation and reconciliation
- **Estimated stories:** 4-5 stories
- **Key deliverables:** Kindle import parser, Audible import parser, sandbox migration testing, data validation/rollback mechanism, Hardcover.app reconciliation, unified timeline creation
- **Dependency Gate:** Cannot start until Epic 3 backup system is operational and validated

**Total: 5 epics, 16-21 stories**

**Epic Sequencing Rationale:**
1. **Epic 1 establishes foundation** - Core library server operational with database schema; immediate value for library management
2. **Epic 2 enables mobility** - Cross-device reading unlocks full daily workflow value
3. **Epic 3 protects ebook data** - Backup and analytics operational before risky operations; ebook-focused keeps scope manageable
4. **Epic 4 adds audiobooks** - Independent integration; can be deferred if needed without blocking ebook functionality
5. **Epic 5 backfills history** - Riskiest work done last when infrastructure is stable; dependency gate ensures backup safety net exists

> **Note:** Detailed epic breakdown with full story specifications is available in [epics.md](./epics.md)

---

## Out of Scope

**Analytics & Visualization (Phase 2):**
- Visual dashboards showing reading patterns, trends, and insights
- Advanced statistical analysis (reading speed by genre, time-of-day patterns)
- Predictive recommendations based on reading history
- Grafana or custom dashboard implementations

**AI Integration (Phase 2):**
- AI agent for reading data analysis and recommendations
- Natural language queries against reading database
- Automated research suggestions based on reading history
- AI-powered reading insights generation

**Community/Multi-User Features (Future):**
- Support for multiple users or family members
- Shared libraries or reading lists
- Social features or reading groups
- Multi-tenant architecture

**Advanced Library Features (Future):**
- Automatic book recommendations and acquisition
- Integration with library lending systems (Libby, Hoopla beyond manual import)
- Format conversion beyond basic optimization
- Advanced tagging, collections, or organizational systems beyond Calibre defaults

**Platform Expansion (Future):**
- Android device support beyond Boox Palma 2
- Desktop reading apps beyond web access
- Additional e-reader hardware integrations
- Native mobile app development

**Extended Integrations (Future):**
- Goodreads data import for historical data
- Additional reading platforms or services beyond Hardcover
- Note-taking system integrations (Obsidian, Notion)
- Browser extension for web article tracking

**Infrastructure Enhancements (Deferred):**
- Audiobookshelf server implementation (deferred to RPi 5 upgrade)
- Custom web UI development (using CWA as-is)
- Advanced monitoring dashboards (basic alerting only in MVP)
- Automated hardware scaling or failover
