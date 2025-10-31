# Story 1.4: Design and implement unified database schema

Status: ready-for-dev

## Story

As a developer,
I want a unified PostgreSQL schema designed and initialized on Neon.tech,
So that reading session data from ebooks and audiobooks can be aggregated and queried for analytics.

## Acceptance Criteria

1. Neon.tech free-tier PostgreSQL created and accessible
2. Books dimension table created with fields: book_id, title, author, isbn, asin, source, media_type, cover_url, page_count, duration_minutes, published_date, created_at
3. Reading_sessions fact table created with fields: session_id, book_id, start_time, end_time, pages_read, duration_minutes, device, media_type, device_stats_source, created_at
4. Schema supports both ebook + audiobook data via media_type field
5. Indexes created on frequently queried fields (book_id, start_time, device)
6. Database connection tested from development environment
7. Schema documentation created (ERD + field definitions)
8. Schema version control: documented in tech-spec-epic-1.md

## Tasks / Subtasks

- [ ] Task 1: Provision Neon.tech PostgreSQL database (AC 1)
  - [ ] Create Neon.tech account and project
  - [ ] Provision free-tier PostgreSQL instance
  - [ ] Configure connection settings (host, port, credentials)
  - [ ] Test connectivity from RPi development environment
  - [ ] Document connection string (store credentials securely)

- [ ] Task 2: Design and create Books dimension table (AC 2)
  - [ ] Define Books table schema with all required fields
  - [ ] Implement data types: SERIAL PK, VARCHAR, INT, TIMESTAMP, DATE
  - [ ] Add NOT NULL constraints where appropriate
  - [ ] Create table in Neon.tech PostgreSQL
  - [ ] Verify table structure with `\d books` psql command
  - [ ] Test INSERT statement with sample data

- [ ] Task 3: Design and create Reading_sessions fact table (AC 3)
  - [ ] Define Reading_sessions table schema with all required fields
  - [ ] Implement foreign key constraint to books(book_id)
  - [ ] Handle nullable fields for ebook-only data (pages_read, duration_minutes)
  - [ ] Create table in Neon.tech PostgreSQL
  - [ ] Verify table structure with `\d reading_sessions` psql command
  - [ ] Test INSERT statement with sample data

- [ ] Task 4: Create performance indexes (AC 5)
  - [ ] Create index on reading_sessions(book_id) for join performance
  - [ ] Create index on reading_sessions(start_time) for time-range queries
  - [ ] Create index on reading_sessions(device) for device-specific analytics
  - [ ] Verify indexes created: `\di reading_sessions*` psql command
  - [ ] Test query performance with EXPLAIN ANALYZE

- [ ] Task 5: Test database connectivity and operations (AC 6)
  - [ ] Install psycopg2 Python library (required for Story 3.2 ETL)
  - [ ] Test psycopg2 connection to Neon.tech from RPi
  - [ ] Test SELECT query: `SELECT COUNT(*) FROM books;`
  - [ ] Test INSERT: Add sample book and reading session
  - [ ] Test UPDATE and DELETE operations
  - [ ] Verify transaction handling (COMMIT/ROLLBACK)
  - [ ] Document any connection issues or workarounds

- [ ] Task 6: Create schema documentation (AC 7)
  - [ ] Generate ERD (Entity-Relationship Diagram) showing tables and relationships
  - [ ] Document Books table: purpose, fields, constraints, indexing
  - [ ] Document Reading_sessions table: purpose, fields, constraints, indexing, foreign keys
  - [ ] Create sample SQL queries for common analytics use cases
  - [ ] Document schema version and any migration notes
  - [ ] Create `docs/NEON-SCHEMA-DOCUMENTATION.md` with full details

- [ ] Task 7: Update tech-spec with final schema (AC 8)
  - [ ] Update tech-spec-epic-1.md § Data Models section with final schema
  - [ ] Include actual SQL DDL statements (not just descriptions)
  - [ ] Document any schema changes from planning to implementation
  - [ ] Add notes on Neon.tech-specific considerations (if any)
  - [ ] Mark schema as "Finalized" and ready for downstream stories

## Dev Notes

### Architecture Alignment

This story implements the **Data Layer** analytics foundation from the approved BookHelper architecture [Source: docs/architecture.md § 3.1. Data Layer]:

- **Neon.tech PostgreSQL** serves as centralized analytics warehouse for ebook + audiobook reading data
- **Books and reading_sessions tables** enable Facts & Dimensions model for dimensional analytics
- **media_type field** enables consolidated queries across ebook and audiobook sources
- **source and device fields** support multi-device tracking and historical migration (Epic 5)
- Schema designed to support Story 3.2 (ETL Pipeline) and Story 3.3 (Analytics Query Interface)

**Key Design Principle:** Schema separates ebook-specific fields (pages_read) from audiobook-specific fields (duration_minutes), using nullable fields to avoid data model impedance mismatch.

[Source: docs/tech-spec-epic-1.md § Data Models and Contracts]

### Project Structure Notes

- **Database Host:** Neon.tech free-tier PostgreSQL (cloud-hosted)
- **Schema Location:** Neon.tech project, database name: `bookhelper` (or configured name)
- **Connection Credentials:** Store in environment variables (NEON_HOST, NEON_USER, NEON_PASSWORD, NEON_DATABASE)
- **Backup:** Neon.tech provides automatic backups; no manual backup required for this story
- **Documentation:** `docs/NEON-SCHEMA-DOCUMENTATION.md` (new file)

### Technical Implementation Notes

- **Language:** PostgreSQL v14+ (Neon.tech standard)
- **Data Types:**
  - `SERIAL PRIMARY KEY` — Auto-incrementing integer primary key
  - `VARCHAR(255)` — Flexible string lengths for book metadata
  - `TIMESTAMP` — UTC timezone for session timestamps
  - `INT` — Page count and duration in minutes
  - `TIMESTAMP DEFAULT CURRENT_TIMESTAMP` — Server-side default for created_at
- **Indexes:** B-tree indexes on book_id, start_time, device for optimal query performance
- **Foreign Keys:** `REFERENCES books(book_id)` with implicit `ON DELETE RESTRICT` (prevent orphaned sessions)

### Learnings from Epic 1 Stories

**From Story 1.1 (CWA Deployment):**
- Docker Compose pattern established on RPi; Neon.tech integration adds cloud data layer
- Persistence strategy: metadata.db (Calibre) + PostgreSQL (analytics)

**From Story 1.2 (Performance Validation):**
- RPi 4 2GB is memory-constrained; PostgreSQL queries must be optimized with indexes
- ETL pipeline (Story 3.2) will be bottleneck if schema not properly indexed

**From Story 1.3 (Auto-ingest):**
- Metadata enrichment produces book records; these become rows in Books table
- Need to plan for schema migration when Kindle/Audible data added (Epic 5)

## Prerequisites

- ✓ Epic 1: Planning complete; Story 1.1 deployed (CWA operational)
- ✓ Neon.tech account created (free tier available)
- ✓ PostgreSQL client tools available (psql, or Python psycopg2)

## References

- [docs/tech-spec-epic-1.md § Data Models and Contracts](../tech-spec-epic-1.md#data-models-and-contracts)
- [docs/architecture.md § 3.1. Data Layer](../architecture.md#31-data-layer-multi-tier-strategy)
- [docs/epics.md § Epic 1 § Story 1.4](../epics.md#story-14-design-and-implement-unified-database-schema)
- Downstream dependencies: Story 3.2 (ETL Pipeline), Story 3.3 (Analytics Query Interface)

## Dev Agent Record

### Context Reference

- Story Context XML: `docs/stories/1-4-design-and-implement-unified-database-schema.context.xml` (generated 2025-10-30)

### Agent Model Used

claude-haiku-4-5-20251001

### Debug Log References

### Completion Notes List

### File List
