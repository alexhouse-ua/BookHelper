# BookHelper Schema Deployment & Testing Guide

## Overview

This guide walks you through deploying the BookHelper PostgreSQL schema to your Raspberry Pi and running comprehensive tests to verify the installation.

**Story 1.4 Completion Status:** Tasks 2, 3, 4, 5 (Schema creation, views, indexes, tests)

**Target Environment:** Raspberry Pi with Neon.tech PostgreSQL database

---

## Prerequisites

Ensure you have:
- SSH access to your Raspberry Pi
- `.env.neon` file with valid Neon.tech credentials
- Git repository cloned at `~/BookHelper`
- Python 3.8+ installed on RPi

---

## Part 1: Setup Virtual Environment (One-Time)

Run these commands on your Raspberry Pi:

```bash
# Navigate to project
cd ~/BookHelper

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install PostgreSQL adapter
pip install psycopg2-binary
```

### Verify Installation

```bash
# Verify psycopg2 is installed
python3 -c "import psycopg2; print(f'✓ psycopg2 {psycopg2.__version__}')"
```

**Expected output:**
```
✓ psycopg2 2.9.x
```

---

## Part 2: Deploy Schema (First Time Only)

### Command

```bash
# Navigate to project
cd ~/BookHelper

# Activate venv (if not already active)
source venv/bin/activate

# Set UTF-8 locale (CRITICAL FIX FOR RASPBIAN)
# Note: Raspbian doesn't include en_US.UTF-8 by default
# Use C.utf8 instead (POSIX UTF-8, universally available)
export LANG=C.utf8
export LC_ALL=C.utf8

# Run schema initialization
python3 resources/scripts/initialize_schema.py
```

### Expected Output

```
============================================================
BookHelper Schema Initialization
Story 1.4: Tasks 2, 3, 4
============================================================

Loading environment variables...
✓ Environment loaded

Database: your-database-name
Host: your-neon-host.neon.tech
User: your-username

Connecting to Neon PostgreSQL...
✓ Connection successful

============================================================
Creating Schema
============================================================

✓ Executed: create_schema.sql
✓ Executed: create_indexes.sql

============================================================
Verifying Tables
============================================================

✓ Table: authors
✓ Table: publishers
✓ Table: books
✓ Table: book_editions
✓ Table: reading_sessions
✓ Table: sync_status

============================================================
Verifying Views
============================================================

✓ View: book_stats
✓ View: reading_timeline
✓ View: publisher_analytics
✓ View: author_analytics
✓ View: tandem_reading_sessions

============================================================
Verifying Triggers
============================================================

✓ Trigger: update_authors_updated_at
✓ Trigger: update_publishers_updated_at
✓ Trigger: update_books_updated_at
✓ Trigger: update_sync_status_updated_at

============================================================
Running Smoke Tests
============================================================

Test 1: INSERT author with JSONB fields...
✓ Created author_id: 1

Test 2: INSERT publisher...
✓ Created publisher_id: 1

Test 3: INSERT book with JSONB and user library fields...
✓ Created book_id: 1

Test 4: INSERT reading_session...
✓ Created session_id: 1, read_instance_id: [UUID]

Test 5: Query JSONB field (genres)...
✓ JSONB query successful: Test Book

Test 6: Query book_stats view...
✓ View query successful - total_sessions: 1

Test 7: Test updated_at trigger...
✓ Trigger working: updated_at changed

Test 8: Test UNIQUE constraint on reading_sessions...
✓ UNIQUE constraint working

Cleaning up test data...
✓ Test data cleaned up

============================================================
✓ Schema Initialization Complete
============================================================

✓ Task 2: Tables created (6)
✓ Task 3: Views created (5)
✓ Task 4: Indexes created
✓ Task 5: Smoke tests passed

Next steps:
  1. Run comprehensive tests: python3 resources/scripts/test_schema_operations.py
  2. Review schema documentation: docs/guides/SCHEMA-DOCUMENTATION.md
```

### What Was Created

- **6 Tables:** authors, publishers, books, book_editions, reading_sessions, sync_status
- **5 Views:** book_stats, reading_timeline, publisher_analytics, author_analytics, tandem_reading_sessions
- **Triggers:** Automatic `updated_at` timestamp management on all tables
- **Indexes:** 11 performance indexes (composite B-tree and GIN for JSONB)
- **Constraints:** Primary keys, unique constraints, check constraints, foreign keys with CASCADE

---

## Part 3: Run Comprehensive Tests

### Command

```bash
# Make sure venv is activated
cd ~/BookHelper
source venv/bin/activate

# Set UTF-8 locale (use C.utf8 for Raspbian compatibility)
export LANG=C.utf8
export LC_ALL=C.utf8

# Run comprehensive test suite
python3 resources/scripts/test_schema_operations.py
```

### Expected Output

```
============================================================
BookHelper Schema Operations Test Suite
Story 1.4: Task 5
============================================================

Loading environment variables...
✓ Environment loaded

Connecting to Neon PostgreSQL...
✓ Connection successful

============================================================
Test Suite 1: Schema Structure Validation
============================================================

✓ Table 'authors' has all expected columns (8)
✓ Table 'publishers' has all expected columns (7)
✓ Table 'books' has all expected columns (24)
✓ Table 'book_editions' has all expected columns (10)
✓ Table 'reading_sessions' has all expected columns (15)
✓ Table 'sync_status' has all expected columns (8)

============================================================
Test Suite 1.1: JSONB Column Types
============================================================

✓ authors.alternate_names is JSONB
✓ authors.contributions is JSONB
✓ publishers.alternate_names is JSONB
✓ books.genres is JSONB
✓ books.moods is JSONB
✓ books.content_warnings is JSONB
✓ books.cached_tags is JSONB
✓ books.alternative_titles is JSONB

============================================================
Test Suite 1.2: Constraint Validation
============================================================

✓ PRIMARY KEY on authors(author_id)
✓ PRIMARY KEY on publishers(publisher_id)
✓ PRIMARY KEY on books(book_id)
✓ PRIMARY KEY on book_editions(edition_id)
✓ PRIMARY KEY on reading_sessions(session_id)
✓ PRIMARY KEY on sync_status(sync_id)
✓ UNIQUE constraint on reading_sessions (book_id, start_time, device)

============================================================
Test Suite 2: CRUD Operations
============================================================

✓ INSERT author with JSONB (author_id: 2)
✓ INSERT publisher (publisher_id: 2)
✓ INSERT book with JSONB and user fields (book_id: 2)
✓ INSERT book_edition (edition_id: 1)
✓ INSERT reading_session with UUID (session_id: 2, read_instance_id: [UUID])
✓ INSERT sync_status (sync_id: 2)
✓ SELECT author by ID (found: Maya Rodriguez)
✓ SELECT book by ID
✓ UPDATE book (data updated, trigger updated updated_at)

============================================================
Test Suite 3: JSONB Operations
============================================================

✓ JSONB @> containment (genres contains 'Science Fiction')
✓ JSONB ? key existence (moods contains 'witty')
✓ JSONB UPDATE (append to genres array)
✓ JSONB array length (genres: 4)
✓ JSONB multi-element containment (genres @> multiple values)

============================================================
Test Suite 4: Foreign Keys and CASCADE
============================================================

✓ CASCADE DELETE (book → reading_sessions)
✓ Foreign key CASCADE cleanup successful

============================================================
Test Suite 5: Constraint Enforcement
============================================================

✓ UNIQUE constraint enforcement (reading_sessions)
✓ CHECK constraint enforcement (duration_minutes > 0)
✓ NOT NULL constraint enforcement (author_id)

============================================================
Test Suite 6: View Queries
============================================================

✓ View: book_stats (total_sessions: 1)
✓ View: reading_timeline (rows: 0)
✓ View: publisher_analytics (rows: 0)
✓ View: author_analytics (rows: 0)
✓ View: tandem_reading_sessions (rows: 0)

============================================================
Test Suite 7: Trigger Functionality
============================================================

✓ Trigger: authors.updated_at auto-update
✓ Trigger: publishers.updated_at auto-update
✓ Trigger: books.updated_at auto-update
✓ Trigger: sync_status.updated_at auto-update

============================================================
Test Suite 8: Index Verification
============================================================

✓ Index exists: idx_reading_sessions_book_date
✓ Index exists: idx_reading_sessions_date_device
✓ Index exists: idx_reading_sessions_parallel
✓ Index exists: idx_books_genres
✓ Index exists: idx_books_moods
✓ Index exists: idx_books_content_warnings
✓ Index exists: idx_books_author_diversity
✓ Index exists: idx_books_user_ownership
✓ Index exists: idx_books_reading_status
✓ Index exists: idx_authors_diversity
✓ Index exists: idx_book_editions_format_book

============================================================
Cleanup Test Data
============================================================

✓ Test data cleanup complete

============================================================
Test Summary
============================================================

Total Tests: 65
Passed: 65
Failed: 0
Warnings: 0

✓ ALL TESTS PASSED
```

### Test Suites Explained

| Suite | Count | Purpose |
|-------|-------|---------|
| Schema Structure | 6 | Verify all 6 tables exist with correct columns |
| JSONB Types | 8 | Verify JSONB columns have correct data type |
| Constraints | 7 | Verify PRIMARY KEY, UNIQUE, etc. exist |
| CRUD Operations | 9 | Test Create, Read, Update on all tables |
| JSONB Operations | 5 | Test JSONB operators (@>, ?, array manipulation) |
| Foreign Keys | 2 | Test CASCADE DELETE behavior |
| Constraint Enforcement | 3 | Test UNIQUE, CHECK, NOT NULL constraints |
| Views | 5 | Query all 5 views |
| Triggers | 4 | Test updated_at auto-update on all tables |
| Indexes | 11 | Verify all performance indexes exist |
| **Total** | **65** | Complete schema validation |

---

## Part 4: Quick Command Reference

### Always Activate Virtual Environment First

```bash
cd ~/BookHelper
source venv/bin/activate

# Set UTF-8 locale (use C.utf8 for Raspbian compatibility)
export LANG=C.utf8
export LC_ALL=C.utf8
```

### Run Schema Initialization

```bash
python3 resources/scripts/initialize_schema.py
```

### Run Comprehensive Tests

```bash
python3 resources/scripts/test_schema_operations.py
```

### Connect to Database Directly

```bash
# Load credentials from .env.neon
source .env.neon

# Connect via psql
psql "postgresql://${NEON_USER}:${NEON_PASSWORD}@${NEON_HOST}/${NEON_DATABASE}?sslmode=require"
```

### Common psql Commands

```sql
-- List all tables
\dt

-- Describe table structure
\d books

-- List all views
\dv

-- List all indexes
\di

-- Test JSONB query
SELECT title, genres FROM books WHERE genres @> '["Science Fiction"]'::jsonb;

-- Check trigger
SELECT trigger_name FROM information_schema.triggers WHERE trigger_schema = 'public';
```

---

## Part 5: Troubleshooting

### UnicodeEncodeError & Locale Issues (CRITICAL FOR RASPBIAN)

**Problem:**
```
bash: warning: setlocale: LC_ALL: cannot change locale (en_US.UTF-8): No such locale installed
UnicodeEncodeError: 'latin-1' codec can't encode character '\u2713' in position 5: ordinal not in range(256)
```

**Root Cause:**
Raspbian base image doesn't include `en_US.UTF-8` locale by default. The default system locale is `C` (ASCII), which can't encode UTF-8 characters like checkmarks (✓).

**Quick Solution (Recommended):**
```bash
# Use C.utf8 (POSIX UTF-8 - universally available on all Linux systems)
export LANG=C.utf8
export LC_ALL=C.utf8
python3 resources/scripts/initialize_schema.py
```

**Permanent Solution:** Add to `~/.bashrc` on RPi:
```bash
echo "export LANG=C.utf8" >> ~/.bashrc
echo "export LC_ALL=C.utf8" >> ~/.bashrc
source ~/.bashrc
```

**Why C.utf8?**
- ✓ Available on all Linux systems (no installation needed)
- ✓ Fully UTF-8 compliant
- ✓ Works with all international characters
- ✓ No compatibility issues
- ✗ Don't use `en_US.UTF-8` on Raspbian (not installed by default)

**Alternative (If you want en_US.UTF-8):**
```bash
# Generate the locale on RPi
sudo locale-gen en_US.UTF-8
sudo update-locale LANG=en_US.UTF-8
# Log out and back in
```

---

### Connection Timeout

**Problem:**
```
psycopg2.OperationalError: could not connect to server: Connection timed out
```

**Cause:** Network connectivity issue or invalid credentials

**Solution:**
```bash
# Verify .env.neon has correct credentials
cat .env.neon

# Test DNS resolution (if dig available)
dig your-neon-host.neon.tech

# Test connectivity with timeout
timeout 5 bash -c "</dev/tcp/${NEON_HOST}/5432" && echo "Connected" || echo "Failed"
```

---

### Schema Already Exists Error

**Problem:**
```
ERROR:  relation "authors" already exists
```

**Cause:** Schema was already deployed, script attempting to re-create

**Solution:** Reset database (WARNING: deletes all data)
```bash
# Get connection string from .env.neon
source .env.neon

# Connect to database
psql "postgresql://${NEON_USER}:${NEON_PASSWORD}@${NEON_HOST}/${NEON_DATABASE}?sslmode=require"

# In psql, drop all tables:
DROP TABLE IF EXISTS reading_sessions CASCADE;
DROP TABLE IF EXISTS book_editions CASCADE;
DROP TABLE IF EXISTS books CASCADE;
DROP TABLE IF EXISTS publishers CASCADE;
DROP TABLE IF EXISTS authors CASCADE;
DROP TABLE IF EXISTS sync_status CASCADE;
DROP FUNCTION IF EXISTS update_modified_column() CASCADE;

# Exit psql
\q

# Re-deploy schema
python3 resources/scripts/initialize_schema.py
```

---

### Import Error: psycopg2

**Problem:**
```
ModuleNotFoundError: No module named 'psycopg2'
```

**Cause:** Virtual environment not activated or module not installed

**Solution:**
```bash
# Activate venv
cd ~/BookHelper
source venv/bin/activate

# Reinstall psycopg2-binary
pip install --upgrade psycopg2-binary

# Verify installation
python3 -c "import psycopg2; print(psycopg2.__version__)"
```

---

### externally-managed-environment Error

**Problem:**
```
error: externally-managed-environment
This environment is externally managed
```

**Cause:** Attempting to install packages globally on modern Python

**Solution:** Always use virtual environment:
```bash
cd ~/BookHelper
python3 -m venv venv
source venv/bin/activate
pip install psycopg2-binary
```

---

### Tests Failing with Constraint Errors

**Problem:**
```
✗ UNIQUE constraint enforcement - Duplicate insert succeeded (should have failed)
✗ CHECK constraint enforcement - Negative duration accepted
```

**Cause:** Constraints not properly created in schema

**Solution:** Reset and re-initialize:
```bash
# Reset database (see "Schema Already Exists Error" above)
# Then re-run:
python3 resources/scripts/initialize_schema.py
python3 resources/scripts/test_schema_operations.py
```

---

## Part 6: Next Steps

### After Successful Testing

1. **Verify all 65 tests pass** with no failures
2. **Document deployment date** in your project notes
3. **Mark Story 1.4 complete** in `bmm-workflow-status.md`
4. **Review schema documentation** at `docs/guides/SCHEMA-DOCUMENTATION.md`
5. **Begin ETL development** for Story 2.x (KOReader/Hardcover sync)

### Checklist

- [ ] Virtual environment created and activated
- [ ] psycopg2-binary installed successfully
- [ ] `.env.neon` file verified with correct credentials
- [ ] `initialize_schema.py` runs without errors
- [ ] All smoke tests pass (8/8)
- [ ] `test_schema_operations.py` runs without errors
- [ ] All comprehensive tests pass (65/65)
- [ ] Manual JSONB queries work in psql
- [ ] Views can be queried successfully

---

## Appendix: Schema Architecture

### Tables (6 Total)

| Table | Purpose | Key Fields |
|-------|---------|-----------|
| **authors** | Book author metadata | author_id, author_name, is_bipoc, is_lgbtq, contributions (JSONB) |
| **publishers** | Publisher information | publisher_id, publisher_name, country, parent_publisher |
| **books** | Core book data | book_id, title, isbn_13, genres (JSONB), moods (JSONB), user_* fields |
| **book_editions** | Edition-specific details | edition_id, book_id, edition_format, isbn_13 |
| **reading_sessions** | User reading activity | session_id, book_id, start_time, duration_minutes, read_instance_id (UUID) |
| **sync_status** | ETL synchronization tracking | sync_id, source, last_sync, records_processed, status |

### Views (5 Total)

| View | Purpose |
|------|---------|
| **book_stats** | Aggregated reading statistics per book |
| **reading_timeline** | Chronological reading sessions timeline |
| **publisher_analytics** | Publisher-level aggregations |
| **author_analytics** | Author-level aggregations |
| **tandem_reading_sessions** | Parallel reading detection (multi-device) |

### Indexes (11 Total)

| Index | Type | Purpose |
|-------|------|---------|
| idx_reading_sessions_book_date | Composite B-tree | Sessions for book, sorted by date |
| idx_reading_sessions_date_device | Composite B-tree | Device-based filtering over time |
| idx_reading_sessions_parallel | Partial B-tree | Tandem reading detection |
| idx_books_genres | GIN | JSONB genre searches |
| idx_books_moods | GIN | JSONB mood searches |
| idx_books_content_warnings | GIN | JSONB content warning searches |
| idx_books_author_diversity | Composite B-tree | Author diversity filtering |
| idx_books_user_ownership | Partial B-tree | User library ownership status |
| idx_books_reading_status | Partial B-tree | Reading status filtering |
| idx_authors_diversity | Partial B-tree | Diverse author discovery |
| idx_book_editions_format_book | Composite B-tree | Edition format lookups |

---

## Support & Documentation

For more information, see:
- **Schema Details:** `docs/guides/SCHEMA-DOCUMENTATION.md`
- **ETL Mapping:** `docs/guides/ETL-MAPPING-GUIDE.md`
- **Project Epics:** `docs/epics.md`
- **Story Status:** `bmm-workflow-status.md`

---

**Last Updated:** October 31, 2025
**Status:** Story 1.4 - Schema Initialization & Testing Complete
**Next Phase:** Story 2.x - ETL Development & Data Synchronization
