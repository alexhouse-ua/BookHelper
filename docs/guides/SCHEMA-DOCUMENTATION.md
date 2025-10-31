# BookHelper Database Schema Documentation
**Story 1.4: Unified Database Schema**
**Database:** Neon.tech PostgreSQL v17
**Date:** 2025-10-31 (Updated from 2025-10-30)

---

## Overview

The BookHelper unified database schema enables comprehensive reading analytics across ebook and audiobook sources through a dimensional model with:
- **5 core tables:** `authors`, `publishers`, `books`, `book_editions`, `reading_sessions`
- **5 computed views:** `book_stats`, `reading_timeline`, `publisher_analytics`, `author_analytics`, `tandem_reading_sessions`
- **Multi-format support:** Track same book across ebook, audiobook, and physical formats
- **Author dimension:** Separate author table with diversity and prolific metrics
- **Edition tracking:** Document owned physical editions and special editions
- **Tandem reading:** Support parallel ebook + audiobook reading with overlap-aware analytics
- **Publisher consolidation:** Handle duplicate publisher names and imprint hierarchies
- **Re-read tracking:** Track how many times each book has been read
- **Dynamic aggregation:** Computed fields support future multi-source integration (Epic 4, 5)

---

## Entity-Relationship Diagram (ERD)

### Visual Schema Structure

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│  UNIFIED DATABASE ARCHITECTURE - BookHelper (Version 2.0)                 │
│  ════════════════════════════════════════════════════════════════          │
│                                                                             │
│         ┌────────────────────┐           ┌─────────────────┐              │
│         │     authors        │           │   publishers    │              │
│         │    (DIMENSION)     │           │   (DIMENSION)   │              │
│         │   🟢 Hardcover     │           │  🟢 Hardcover   │              │
│         ├────────────────────┤           ├─────────────────┤              │
│         │ author_id ◄PK      │           │publisher_id◄PK  │              │
│         │ author_name 🟢     │           │publisher_name🟢 │              │
│         │ alternate_names 🟢 │           │alternate_names🟢│              │
│         │ book_count 🟢      │           │parent_id 🟢     │              │
│         │ contributions 🟢   │           │parent_publisher │              │
│         │ born_year 🟢       │           │  🟢              │              │
│         │ is_bipoc 🟢        │           │country 🟢        │              │
│         │ is_lgbtq 🟢        │           │                 │              │
│         └────────────────────┘           └─────────────────┘              │
│              ▲                                   ▲                         │
│              │ 1:N                              │ 1:N                     │
│              │                                   │                         │
│         ┌────────────────────────────────────────────────────┐            │
│         │          books (CORE FACT TABLE)                   │            │
│         │         🟢🟠🔵🟡 Multi-Source                      │            │
│         ├────────────────────────────────────────────────────┤            │
│         │ IDENTIFICATION:                                     │            │
│         │  book_id ◄PK 🟡                                    │            │
│         │  title 🟢🔵, author 🟡 (computed from author_id)  │            │
│         │  author_id ──FK──►authors 🟢                       │            │
│         │                                                      │            │
│         │ IDENTIFIERS & LINKS:                                │            │
│         │  isbn_13, isbn_10, asin 🟢                         │            │
│         │  hardcover_book_id 🟢                              │            │
│         │  publisher_id ──FK──►publishers 🟢                 │            │
│         │  publisher_name 🟡 (computed from publisher_id)    │            │
│         │  file_hash 🔵 (KOReader dedup)                     │            │
│         │                                                      │            │
│         │ HARDCOVER BOOKS METADATA:                          │            │
│         │  pages 🟢, description 🟢                          │            │
│         │  genres 🟢, moods 🟢                               │            │
│         │  content_warnings 🟢                               │            │
│         │  alternative_titles 🟢                             │            │
│         │  cover_color 🟢, cover_url 🟢                      │            │
│         │  activities_count 🟢                               │            │
│         │                                                      │            │
│         │ RATINGS & REVIEWS:                                  │            │
│         │  hardcover_rating 🟢, rating_count 🟢              │            │
│         │  user_rating 🟠, user_rating_date 🟠               │            │
│         │  users_read_count 🟢, users_count 🟢               │            │
│         │                                                      │            │
│         │ USER LIBRARY (from Activities):                    │            │
│         │  user_owns_ebook 🟠                                │            │
│         │  user_owns_audiobook 🟠                            │            │
│         │  user_owns_physical 🟠                             │            │
│         │  user_reading_status 🟠                            │            │
│         │  user_added_date 🟠                                │            │
│         │                                                      │            │
│         │ KOREADER TRACKING:                                  │            │
│         │  notes 🔵, highlights 🔵                           │            │
│         │  read_count 🟡 (computed)                          │            │
│         └────────────────────────────────────────────────────┘            │
│              ▲                   ▼ 1:N                                     │
│              │        ┌────────────────────────────────────┐              │
│              │        │  reading_sessions (FACT TABLE)     │              │
│              │        │      🔵 KOReader Primary           │              │
│              │        ├────────────────────────────────────┤              │
│              │        │ session_id ◄PK 🟡                  │              │
│              │        │ book_id ──FK──►books 🔵            │              │
│              │        │ start_time 🔵, duration 🔵         │              │
│              │        │ pages_read 🔵, media_type 🔵       │              │
│              │        │ read_instance_id 🟡 (UUID)         │              │
│              │        │ is_parallel_read 🟡                │              │
│              │        │ read_number 🟡 (tandem tracking)   │              │
│              │        └────────────────────────────────────┘              │
│              │                                                             │
│         1:N  │                                                             │
│              │                                                             │
│         ┌────────────────────────────────────┐                           │
│         │    book_editions (DIMENSION)       │                           │
│         │    🟢 Hardcover Editions API       │                           │
│         ├────────────────────────────────────┤                           │
│         │ edition_id ◄PK 🟡                  │                           │
│         │ book_id ──FK──►books               │                           │
│         │ isbn_13, isbn_10, asin 🟢          │                           │
│         │ physical_format 🟢                 │                           │
│         │ publisher_id 🟢                    │                           │
│         │ language 🟢, pages 🟢              │                           │
│         │ release_date 🟢, audio_seconds 🟢  │                           │
│         └────────────────────────────────────┘                           │
│                                                                             │
│  ───────────────────────────────────────────────────────────────────────  │
│  LEGEND:                                                                   │
│    🔵 KOReader (statistics.sqlite3) - Reading activity & book basics     │
│    🟢 Hardcover API (Books, Editions) - Metadata, ratings, library       │
│    🟠 Hardcover API (Activities) - UserBookActivity events, ownership    │
│    🟡 Computed - Generated during ETL (IDs, aggregations, derived)       │
│                                                                             │
│  KEY CHARACTERISTICS:                                                     │
│    FACT TABLES: books, reading_sessions (transaction data)               │
│    DIMENSION TABLES: authors, publishers, book_editions (reference)      │
│    SOURCES: NO user input - all from KOReader or Hardcover API          │
│  ───────────────────────────────────────────────────────────────────────  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Cardinality Summary

| Relationship | Cardinality | Notes |
|---|---|---|
| authors ← books | 1:N | One author has many books (pen names consolidated) |
| publishers ← books | 1:N | One publisher publishes many books |
| books → book_editions | 1:N | One book has multiple editions (hardcover, paperback, special) |
| books → reading_sessions | 1:N | One book has many reading sessions |
| publishers ← publishers | 1:N | Self-referential for imprints (parent_publisher_id) |

**Detailed Table Documentation References:**
- **authors** → See [Table: authors](#table-authors) (line ~211)
- **publishers** → See [Table: publishers](#table-publishers) (line ~266)
- **books** → See [Table: books](#table-books) (line ~330)
- **book_editions** → See [Table: book_editions](#table-book_editions) (line ~497)
- **reading_sessions** → See [Table: reading_sessions](#table-reading_sessions) (line ~561)

---

## Data Flow Architecture

### High-Level ETL Pipeline

```
SOURCE DATA LAYER
═════════════════════════════════════════════════════════════════
        ↓ KOReader (SQLite)           ↓ Hardcover API           ↓ User Input
    history.db                   (REST JSON)              (Web Form / Sync)
    - reading_sessions          - book metadata          - ratings
    - page progress             - author details         - edition data
    - device stats              - publisher info         - physical library
        ↓                               ↓                        ↓
        └───────────────────────────────┼────────────────────────┘
                                        ↓
EXTRACTION & TRANSFORMATION LAYER
═════════════════════════════════════════════════════════════════
    • Parse KOReader history
    • Validate/normalize dates
    • Call Hardcover API for enrichment
    • Detect tandem reads (overlap analysis)
    • Assign read_instance_id
    • Extract author/publisher hierarchies
                                        ↓
NORMALIZED TABLE LAYER (PostgreSQL)
═════════════════════════════════════════════════════════════════
    publishers table  ←  author table  ←  books table
         ↓                   ↓               ↓
    (publisher_id)    (author_id)     (all 5 dimensions)
                            ↓
                    reading_sessions
                       (fact table)
                            ↓
                    book_editions
                   (special editions)
                                        ↓
ANALYTICS & VIEWS LAYER
═════════════════════════════════════════════════════════════════
    book_stats              reading_timeline
    (per-book metrics)      (session details with metadata)
         ↓                           ↓
    author_analytics        publisher_analytics
    (author-level            (publisher-level
     diversity tracking)      aggregations)
         ↓
    tandem_reading_sessions
    (parallel read analysis)
```

### Data Source Attribution

Every field is tagged with its source to ensure traceability:

| Source | Description | Refresh | Reliability |
|--------|-------------|---------|-------------|
| **KOReader** | Reading statistics from KOReader statistics.sqlite3 (book table, page_stat_data) - reading sessions, page counts, highlights, notes | User syncs (via KOSync) | High - direct reading data |
| **Hardcover API - Books** | Book metadata: genres, moods, content_warnings, tags, pages, description, release_date, rating, alternative_titles, author_names | On-demand enrichment during ETL | High - curated metadata source |
| **Hardcover API - Editions** | Edition metadata: ISBN, ASIN, physical_format, pages, audio_seconds, publisher, language, release_date | On-demand enrichment during ETL | High - canonical edition data |
| **Hardcover API - Activities (UserBookActivity)** | User library tracking: reading_status, ownership (ebook/audiobook/physical), user_rating, review, activity timestamps | Real-time sync from activities endpoint | High - reflects user's current library |
| **Computed** | book_id (SERIAL), read_instance_id, read_count, views, aggregations, page statistics | Derived during ETL/load | Deterministic |
| **ETL Pipeline** | Metadata fields set during transformation (load timestamp, job ID, source origin) | Once per pipeline run | Deterministic |

---

## Table: `authors`

*See [Cardinality Summary](#cardinality-summary) and [ERD](#entity-relationship-diagram-erd) for relationship context.*

### Purpose
Author master data with diversity metrics, prolific indicators, and alternate names support.

### Design Rationale
Separate author table enables:
- Author-level analytics (books written, genres published)
- Diversity tracking (BIPOC, LGBTQ+ representation)
- Pen name consolidation (Stephen King / Richard Bachman)
- Temporal analysis (birth year for contemporary vs. classic authors)

### Schema

| Column | Type | Constraints | Source | Description |
|--------|------|-----------|--------|-------------|
| `author_id` | SERIAL | PRIMARY KEY | Computed | Auto-incrementing author identifier |
| `author_name` | VARCHAR(255) | NOT NULL | KOReader/Hardcover | Primary author name |
| `author_slug` | VARCHAR(255) | | Hardcover API | URL-friendly identifier |
| `author_hardcover_id` | VARCHAR(100) | UNIQUE | Hardcover API | Hardcover API author ID (UNIQUE: each Hardcover author ID maps to exactly one author record; NULL allowed for non-Hardcover authors) |
| `alternate_names` | JSONB | DEFAULT '[]' | Hardcover API | Array of pen names and pseudonyms (from Hardcover alternate_names) |
| `book_count` | INT | | Hardcover API | Total published works (from Hardcover books_count) |
| `contributions` | JSONB | DEFAULT '[]' | Hardcover API | Array of contribution types (author, editor, translator, illustrator, etc.) |
| `born_year` | INT | | Hardcover API | Author birth year |
| `is_bipoc` | BOOLEAN | DEFAULT FALSE | Hardcover API | BIPOC diversity flag |
| `is_lgbtq` | BOOLEAN | DEFAULT FALSE | Hardcover API | LGBTQ+ diversity flag |
| `identifiers` | JSONB | DEFAULT '{}' | Hardcover API | Cross-reference IDs (VIAF, Wikidata) |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Computed | Record creation timestamp |
| `updated_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Computed | Last modification timestamp |

### Indexes

```sql
CREATE INDEX idx_authors_hardcover_id ON authors(author_hardcover_id);
CREATE INDEX idx_authors_name ON authors(author_name);
```

### Example Usage

**Insert author from Hardcover:**
```sql
INSERT INTO authors (author_name, author_hardcover_id, alternate_names, born_year, is_bipoc, is_lgbtq)
VALUES ('Ali Hazelwood', 'author_123', ARRAY['Ali Hazelwood'], 1986, true, false);
```

**Query author diversity:**
```sql
SELECT author_name, books_count, is_bipoc, is_lgbtq
FROM authors
WHERE is_bipoc = true OR is_lgbtq = true
ORDER BY books_count DESC;
```

---

## Table: `publishers`

*See [Cardinality Summary](#cardinality-summary) and [ERD](#entity-relationship-diagram-erd) for relationship context.*

### Purpose
Consolidate publisher metadata with support for name aliases and organizational hierarchy (imprints, parent companies).

### Design Rationale
Publishers often have multiple names across different systems:
- "Penguin" vs. "Penguin Books" vs. "Penguin Random House"
- Imprints (e.g., Berkley is imprint of Penguin)
- Mergers/consolidations (e.g., Random House merged with Penguin)

This table provides a single source of truth while maintaining historical relationships.

### Schema

| Column | Type | Constraints | Source | Description |
|--------|------|-----------|--------|-------------|
| `publisher_id` | SERIAL | PRIMARY KEY | Computed | Auto-incrementing publisher identifier |
| `publisher_name` | VARCHAR(255) | NOT NULL, UNIQUE | Hardcover API | Canonical publisher name |
| `alternate_names` | TEXT[] | DEFAULT '{}' | Hardcover API | Known alternate names |
| `publisher_hardcover_id` | INT | UNIQUE | Hardcover API | Hardcover API publisher ID (UNIQUE: each Hardcover publisher ID maps to one record; NULL allowed for non-Hardcover publishers) |
| `canonical_hardcover_id` | INT | | Hardcover API | Reference to canonical if consolidated (P3) |
| `parent_id` | INT | | Hardcover API | Parent publisher ID from Hardcover (reference only, not FK) |
| `parent_publisher` | VARCHAR(255) | | Hardcover API | Parent publisher name (denormalized reference) |
| `country` | VARCHAR(100) | | Hardcover API | Country of publication |
| `notes` | TEXT | | User | Administrative notes |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Computed | Record creation timestamp |
| `updated_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Computed | Last modification timestamp |

### Indexes

```sql
CREATE INDEX idx_publishers_hardcover_id ON publishers(publisher_hardcover_id);
CREATE INDEX idx_publishers_canonical_id ON publishers(canonical_hardcover_id);
```

### Example Usage

**Consolidate duplicate publishers:**
```sql
INSERT INTO publishers (publisher_name, publisher_hardcover_id, alternate_names)
VALUES ('Penguin Books', 123, ARRAY['Penguin', 'Penguin Publishing', 'Penguin Random House']);

INSERT INTO publishers (publisher_name, publisher_hardcover_id, canonical_hardcover_id, alternate_names)
VALUES ('Penguin Publishing', 456, 123, ARRAY['Penguin Publishing Group']);
```

**Track imprint relationships:**
```sql
INSERT INTO publishers (publisher_name, publisher_hardcover_id, parent_publisher_id)
VALUES ('Berkley', 789, 123);  -- Berkley's parent is Penguin Books
```

**Query publisher analytics:**
```sql
SELECT p.publisher_name, COUNT(*) as books_read
FROM publishers p
JOIN books b ON p.publisher_id = b.publisher_id
GROUP BY p.publisher_name
ORDER BY books_read DESC;
```

### Constraint Logic & Design Patterns

**Publisher Name Uniqueness (NOT NULL, UNIQUE):**
- Each canonical publisher name can appear only once (enforced by UNIQUE constraint)
- This prevents duplicate entries for the same publisher
- Example: Cannot have two rows with publisher_name = 'Penguin Books'
- Use `canonical_hardcover_id` to link duplicate rows to a single canonical entry

**Hardcover ID Mapping (UNIQUE, nullable):**
- Each Hardcover publisher ID maps to at most one publisher record (UNIQUE)
- NULL values allowed for non-Hardcover publishers (publishers without Hardcover presence)
- This enables tracking of source: if `publisher_hardcover_id` is NULL, data came from non-Hardcover source

**Publisher Consolidation Pattern:**
```
1. Create canonical entry:
   INSERT INTO publishers(publisher_name, publisher_hardcover_id, ...)
   VALUES ('Penguin Random House', 999, ...);

2. Link duplicate/alternate entries:
   UPDATE publishers SET canonical_hardcover_id = 999
   WHERE publisher_name IN ('Penguin Books', 'Penguin Publishing');

3. Query consolidated view:
   SELECT COALESCE(canonical_hardcover_id, publisher_hardcover_id) as canonical_id,
          publisher_name
   FROM publishers
   WHERE canonical_hardcover_id IS NULL or publisher_id = 999;
```

**Imprint Hierarchy Pattern:**
- `parent_id` and `parent_publisher` track imprint relationships
- NOT a foreign key (denormalized reference for flexibility)
- Use for queries like: "Show all imprints of Penguin" or "Find parent of Berkley"
- Example: `SELECT * FROM publishers WHERE parent_publisher = 'Penguin Books'`

---

## Table: `books`

*See [Cardinality Summary](#cardinality-summary) and [ERD](#entity-relationship-diagram-erd) for relationship context.*

### Purpose
Book master data with metadata enrichment from Hardcover API, KOReader statistics, and physical library tracking. Immutable dimension table referenced by reading sessions and editions.

### Design Rationale

**Field Organization by Data Category:**
- Organize by information type rather than data hierarchy
- Capture comprehensive Hardcover metadata: genres, moods, content warnings, tags
- Track library ownership from Hardcover Activities (UserBookActivity events)
- Maintain both community and personal ratings with timestamps
- Support series tracking, formats, and edition metadata

**Hardcover Metadata (from Books & Editions schemas):**
- `genres`, `moods`, `content_warnings`, `tags`: Content classification array fields from Hardcover
- `pages`, `audio_seconds`: Media format specifics (physical pages vs. audiobook duration)
- `alternative_titles`: Localized titles and original titles (as array)
- `cover_color`: Dominant color extracted from cover image
- `activities_count`: Count of related activities on Hardcover (engagement indicator)
- `rating`, `ratings_count`, `users_read_count`, `users_count`: Community statistics

**User Library Tracking (from Hardcover Activities - UserBookActivity events):**
- `user_owns_ebook`, `user_owns_audiobook`, `user_owns_physical`: Format ownership flags from readingFormatId tracking
- `user_reading_status`: Reading progress state (reading, finished, want-to-read, dnf) derived from UserBookActivity statusId
- `user_rating`, `user_rating_date`: Personal rating from UserBookActivity event data
- `user_added_date`: When book was added to library (from activity created_at timestamp)
- **All values sourced from Hardcover Activities API (no manual user input)**

**Rating Architecture:**
- `hardcover_rating`: Community average from Hardcover books schema (0-5 scale)
- `hardcover_rating_count`: Count of community ratings
- `user_rating`: Personal rating from Hardcover Activities UserBookActivity events
- `user_rating_date`: Timestamp of when rating was set (from activities)

**Series Support:**
- `series_name`: Series name extracted from Hardcover series_names array
- `series_number`: Position in series (NUMERIC(5,2) supports "2.5" for novellas, "Prequel" logic)

**book_id Design:**
- `book_id` is a SERIAL (auto-incrementing) PRIMARY KEY **generated during ETL**, NOT from KOReader
- **Why computed?** KOReader's book IDs are local to the database and change across devices/exports (not reliable as canonical identifiers). Since we're consolidating data from multiple sources (KOReader, Hardcover, Kindle, Audible), a new canonical book_id is generated to ensure consistency across all future imports and maintain a unified book catalog independent of source system IDs
- **Traceability:** The book's original KOReader ID is retained in `file_hash` (MD5 deduplication), and Hardcover ID is stored in `hardcover_book_id` for cross-referencing
- **Alternative considered:** Using Hardcover book ID directly would create dependency on Hardcover API for all book lookups, which would fail for books not in Hardcover catalog. The SERIAL approach is agnostic to data sources

### Schema

| Column | Type | Constraints | Source | Description |
|--------|------|-----------|--------|-------------|
| **CORE IDENTIFICATION** | | | | |
| `book_id` | SERIAL | PRIMARY KEY | Computed | Auto-incrementing book identifier (generated during ETL, not from KOReader) |
| `title` | VARCHAR(255) | NOT NULL | KOReader | Book title from KOReader or Hardcover |
| `author` | VARCHAR(255) | | Computed | Primary author name (computed from authors.author_name via author_id FK) |
| `author_id` | INT | FK to authors | Hardcover API | Foreign key to authors table (canonical author reference) |
| **ISBN / ASIN / IDENTIFIERS** | | | | |
| `isbn_13` | VARCHAR(20) | | Hardcover API | ISBN-13 identifier for cross-service linking (13 digit, nullable; multiple books may have NULL) |
| `isbn_10` | VARCHAR(20) | | Hardcover API | ISBN-10 identifier for legacy systems (10 digit, nullable; multiple books may have NULL) |
| `asin` | VARCHAR(20) | | Hardcover API | Amazon ASIN for Kindle/Audible matching (nullable; multiple books may have NULL) |
| `hardcover_book_id` | VARCHAR(100) | | Hardcover API | Hardcover API book entity ID (H1 reference, nullable; multiple books may have NULL) |
| **PUBLISHER & SERIES** | | | | |
| `publisher_id` | INT | FK to publishers | Hardcover API | Foreign key to publishers table (consolidated/canonical publisher) |
| `publisher_name` | VARCHAR(255) | | Computed | Publisher name (computed from publishers.publisher_name via publisher_id FK) |
| `series_name` | VARCHAR(255) | | KOReader/Hardcover | Series name (e.g., "Hani Khan", "Project X") |
| `series_number` | NUMERIC(5,2) | | KOReader/Hardcover | Series position as number (supports 2.5 for novellas, Prequel logic) |
| **BOOK DEMOGRAPHICS & METADATA** | | | | |
| `page_count` | INT | | KOReader | Total pages in primary ebook format |
| `audio_seconds` | INT | | Hardcover API | Total audiobook duration in seconds (from audiobook edition) |
| `language` | CHAR(2) | DEFAULT 'en' | KOReader/Hardcover | ISO 639-1 language code (en=English, es=Spanish, fr=French, etc.) |
| `published_date` | DATE | | Hardcover API | Original publication date |
| `description` | TEXT | | Hardcover API | Book summary/synopsis from Hardcover |
| **RATINGS & REVIEWS** | | | | |
| `hardcover_rating` | DECIMAL(3,2) | | Hardcover API | Hardcover community rating on 0-5 scale (e.g., 4.23) |
| `hardcover_rating_count` | INT | | Hardcover API | Number of community ratings on Hardcover |
| `user_rating` | DECIMAL(3,2) | | Hardcover API (activities) | Your personal rating on 0-5 scale (from activities endpoint) |
| `user_rating_date` | TIMESTAMP | | Hardcover API (activities) | When you rated this book (timestamp from activities) |
| **AUTHOR METRICS** | | | | |
| `author_hardcover_id` | VARCHAR(100) | | Hardcover API | Hardcover author ID for direct API queries |
| `is_bipoc` | BOOLEAN | DEFAULT FALSE | Hardcover API | Author BIPOC diversity flag from Hardcover metadata |
| `is_lgbtq` | BOOLEAN | DEFAULT FALSE | Hardcover API | Author LGBTQ+ diversity flag from Hardcover metadata |
| `author_birth_year` | INT | | Hardcover API | Author birth year for temporal analysis (classics vs. contemporary) |
| `author_books_count` | INT | | Hardcover API | Author's total published works (prolific indicator) |
| **GENRE & CONTENT METADATA** | | | | |
| `genres` | JSONB | DEFAULT '[]' | Hardcover API | Array of genres from Hardcover books schema (queryable via @> operator) |
| `moods` | JSONB | DEFAULT '[]' | Hardcover API | Array of moods from Hardcover books schema (e.g., "dark", "cozy", "inspirational") |
| `content_warnings` | JSONB | DEFAULT '[]' | Hardcover API | Array of content warnings from Hardcover books schema (e.g., "violence", "sexual content") |
| `cached_tags` | JSONB | DEFAULT '[]' | Hardcover API | Genre/topic tags from Hardcover as JSON array (queryable via @> operator) |
| `users_read_count` | INT | | Hardcover API | Count of Hardcover users who have read this book |
| `users_count` | INT | | Hardcover API | Count of Hardcover users who own this edition |
| `activities_count` | INT | | Hardcover API | Count of activities associated with this book on Hardcover |
| `cover_color` | JSONB | | Hardcover API | Dominant color extracted from book cover (auto field) |
| `alternative_titles` | JSONB | DEFAULT '[]' | Hardcover API | Array of alternative titles (other language editions, original titles) |
| **KOREADER & SOURCE TRACKING** | | | | |
| `file_hash` | VARCHAR(32) | | KOReader | MD5 hash of KOReader book file (deduplication key) |
| `notes` | INT | DEFAULT 0 | KOReader | Count of user annotations in KOReader |
| `highlights` | INT | DEFAULT 0 | KOReader | Count of user highlights in KOReader |
| `source` | VARCHAR(50) | DEFAULT 'koreader' | ETL | Data origin identifier: koreader, kindle, audible, hardcover, bookplayer |
| `device_stats_source` | VARCHAR(100) | | KOReader | Backup file source reference (statistics.sqlite3 path/identifier) |
| **COVER & DISPLAY** | | | | |
| `cover_url` | TEXT | | Hardcover API | CDN URL for book cover image (Hardcover images.hardcover.app CDN) |
| **USER LIBRARY TRACKING (from Hardcover Activities)** | | | | |
| `user_owns_ebook` | BOOLEAN | DEFAULT FALSE | Hardcover API (activities) | Whether user owns ebook edition (from UserBookActivity with readingFormatId tracking) |
| `user_owns_audiobook` | BOOLEAN | DEFAULT FALSE | Hardcover API (activities) | Whether user owns audiobook edition (from UserBookActivity with readingFormatId tracking) |
| `user_owns_physical` | BOOLEAN | DEFAULT FALSE | Hardcover API (activities) | Whether user owns physical edition (from UserBookActivity with readingFormatId tracking) |
| `user_reading_status` | VARCHAR(50) | | Hardcover API (activities) | Current reading status (reading, finished, want-to-read, dnf) from UserBookActivity statusId |
| `user_added_date` | TIMESTAMP | | Hardcover API (activities) | When user added this book to their library (from activity created_at) |
| **READ TRACKING** | | | | |
| `read_count` | INT | DEFAULT 1 | Computed | Number of times book has been read. Formula: `COUNT(DISTINCT reading_sessions.read_instance_id) WHERE reading_sessions.book_id = books.book_id` |
| **AUDIT & CONTROL** | | | | |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Computed | Record creation timestamp |
| `updated_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Computed | Last modification timestamp |

### Indexes

```sql
CREATE INDEX idx_books_isbn_13 ON books(isbn_13);
CREATE INDEX idx_books_asin ON books(asin);
CREATE INDEX idx_books_author_id ON books(author_id);
CREATE INDEX idx_books_hardcover_id ON books(hardcover_book_id);
CREATE INDEX idx_books_publisher_id ON books(publisher_id);
CREATE INDEX idx_books_source ON books(source);
CREATE INDEX idx_books_published_date ON books(published_date);
CREATE INDEX idx_books_cached_tags ON books USING GIN(cached_tags);
```

### Example Usage

**Insert book with full metadata:**
```sql
INSERT INTO books (
  title, author, author_id, isbn_13, publisher_id, publisher_name,
  series_name, series_number, page_count, audio_seconds, language,
  hardcover_rating, user_rating, user_rating_date,
  media_types_owned, owned_physical_formats, read_count
) VALUES (
  'Mate', 'Ali Hazelwood', 1, '978-0063119596',
  (SELECT publisher_id FROM publishers WHERE publisher_name='Harper Voyager'),
  'Harper Voyager', 'Hani Khan', 2, 901, 20000, 'en',
  4.23, 4.5, '2025-10-31'::TIMESTAMP,
  ARRAY['ebook', 'audiobook'],
  ARRAY['hardcover', 'paperback'],
  1
);
```

**Query books by genre:**
```sql
SELECT title, author, cached_tags, hardcover_rating, user_rating
FROM books
WHERE cached_tags @> '["romance"]'::jsonb
ORDER BY hardcover_rating DESC;
```

**Multi-format ownership query:**
```sql
SELECT
  title,
  media_types_owned,
  owned_physical_formats,
  (SELECT COUNT(*) FROM reading_sessions WHERE book_id = b.book_id AND media_type='ebook') as ebook_sessions,
  (SELECT COUNT(*) FROM reading_sessions WHERE book_id = b.book_id AND media_type='audiobook') as audio_sessions
FROM books b
WHERE 'audiobook' = ANY(media_types_owned) AND 'ebook' = ANY(media_types_owned)
ORDER BY ebook_sessions + audio_sessions DESC;
```

---

## Table: `book_editions`

*See [Cardinality Summary](#cardinality-summary) and [ERD](#entity-relationship-diagram-erd) for relationship context.*

### Purpose
Track specific physical editions owned (hardcover, paperback, special editions, signed copies, limited editions, etc.) with condition and acquisition metadata.

### Design Rationale
Separate editions table enables:
- Document multiple copies of same book (different formats, special editions)
- Track special edition details (Anniversary Edition, Premium Edition, etc.)
- Record condition for valuable/collectible copies
- Track acquisition date and display location
- Detailed ISBN-specific information per edition

### Schema

| Column | Type | Constraints | Source | Description |
|--------|------|-----------|--------|-------------|
| `edition_id` | SERIAL | PRIMARY KEY | Computed | Auto-incrementing edition identifier |
| `book_id` | INT | NOT NULL FK | User | Foreign key to books table |
| `edition_format` | VARCHAR(50) | | User | Format: hardcover, paperback, special-edition, signed, limited |
| `edition_name` | VARCHAR(255) | | User | Edition name (Anniversary Edition, Premium Edition, etc.) |
| `publication_year` | INT | | User | Year this edition published |
| `publisher_specific` | VARCHAR(255) | | User | Publisher name for this specific edition |
| `isbn_specific` | VARCHAR(20) | | User | ISBN for this specific edition |
| `condition` | VARCHAR(50) | | User | Condition: new, like-new, good, fair, poor |
| `notes` | TEXT | | User | Additional edition notes |
| `date_acquired` | DATE | | User | When you acquired this copy |
| `display_location` | VARCHAR(100) | | User | Where displayed on shelf |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Computed | Record creation timestamp |

### Indexes

```sql
CREATE INDEX idx_book_editions_book_id ON book_editions(book_id);
CREATE INDEX idx_book_editions_format ON book_editions(edition_format);
```

### Example Usage

**Track multiple editions of same book:**
```sql
-- Original paperback read on KOReader
INSERT INTO book_editions (book_id, edition_format, edition_name, condition, date_acquired)
VALUES (1, 'paperback', 'Standard Paperback', 'good', '2023-01-15');

-- Special hardcover purchased later
INSERT INTO book_editions (book_id, edition_format, edition_name, condition, date_acquired, display_location)
VALUES (1, 'hardcover', 'Anniversary Edition', 'like-new', '2025-10-31', 'Shelf A');

-- Signed copy
INSERT INTO book_editions (book_id, edition_format, edition_name, condition, date_acquired, display_location)
VALUES (1, 'special-edition', 'Signed by Author', 'new', '2025-10-30', 'Display Case');
```

**Query physical library:**
```sql
SELECT b.title, b.author, be.edition_format, be.edition_name, be.condition, be.display_location
FROM books b
JOIN book_editions be ON b.book_id = be.book_id
ORDER BY display_location, b.title;
```

---

## Table: `reading_sessions`

*See [Cardinality Summary](#cardinality-summary) and [ERD](#entity-relationship-diagram-erd) for relationship context.*

### Purpose
Immutable append-only fact table storing individual reading/listening events with tandem reading support for parallel ebook + audiobook consumption.

### Design Rationale

**Immutable Append-Only:**
- Sessions never updated, only inserted
- Enables efficient aggregation and time-series analysis
- Safe for concurrent ETL from multiple sources

**Tandem Reading Support:**
- `read_instance_id` (UUID): Groups related sessions (same book, overlapping times, different formats)
- `is_parallel_read` (BOOLEAN): Flags tandem reading pairs
- Example: Reading Ch1-5 via audiobook while simultaneously reading Ch1-5 via ebook
- Enables overlap-aware duration calculations

**Re-Read Tracking:**
- `read_instance_id`: Each read gets unique UUID
- `read_number`: Ordinal read (1=first, 2=reread, etc.)
- `books.read_count`: Computed as COUNT(DISTINCT read_instance_id)

**Data Provenance:**
- `data_source`: Tracks origin (koreader, bookplayer, kindle, audible)
- `device_stats_source`: For KOReader, which backup file
- Enables audit trail and debugging

### Schema

| Column | Type | Constraints | Source | Description |
|--------|------|-----------|--------|-------------|
| **CORE READING FACTS** | | | | |
| `session_id` | BIGSERIAL | PRIMARY KEY | Computed | Auto-incrementing session identifier |
| `book_id` | INT | NOT NULL FK | KOReader/Hardcover | Foreign key to books table (one-to-many: one book has many reading sessions) |
| `start_time` | TIMESTAMP | NOT NULL | KOReader/BookPlayer | Session start (UTC) |
| `duration_minutes` | INT | NOT NULL, >0 | KOReader/BookPlayer | Session duration in minutes |
| `device` | VARCHAR(50) | NOT NULL | ETL | Device ID (boox-palma-2, iphone-x, etc.) |
| **READING FORMAT DETAILS** | | | | |
| `media_type` | VARCHAR(20) | DEFAULT 'ebook' | Session type | Format: "ebook" or "audiobook" |
| `pages_read` | INT | | KOReader | Pages read (ebook only, NULL for audiobook) |
| **TANDEM READING SUPPORT** | | | | |
| `read_instance_id` | UUID | DEFAULT gen_random_uuid() | Computed | UUID grouping tandem reads |
| `is_parallel_read` | BOOLEAN | DEFAULT FALSE | Computed | Flag for tandem session pairs |
| **SESSION TRACKING** | | | | |
| `read_number` | INT | DEFAULT 1 | Computed | Which read of book (1=first, 2=reread) |
| `end_time` | TIMESTAMP | | Computed/ETL | Session end (start_time + duration_minutes) |
| **DATA PROVENANCE** | | | | |
| `data_source` | VARCHAR(50) | DEFAULT 'koreader' | ETL | Source: koreader, bookplayer, kindle, audible |
| `device_stats_source` | VARCHAR(100) | | KOReader | Backup file source (statistics.sqlite3) |
| **AUDIT & CONTROL** | | | | |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Computed | Record creation timestamp |
| **CONSTRAINTS** | | | | |
| | | UNIQUE(book_id, start_time, device) | | Prevent duplicate imports |
| | | CHECK(duration_minutes > 0) | | Duration must be positive |
| | | CHECK(start_time <= CURRENT_TIMESTAMP) | | No future dates |

### Indexes

```sql
CREATE INDEX idx_reading_sessions_book_id ON reading_sessions(book_id);
CREATE INDEX idx_reading_sessions_start_time ON reading_sessions(start_time);
CREATE INDEX idx_reading_sessions_device ON reading_sessions(device);
CREATE INDEX idx_reading_sessions_media_type ON reading_sessions(media_type);
CREATE INDEX idx_reading_sessions_data_source ON reading_sessions(data_source);
CREATE INDEX idx_reading_sessions_read_instance ON reading_sessions(read_instance_id);
CREATE INDEX idx_reading_sessions_book_date ON reading_sessions(book_id, start_time DESC);
CREATE INDEX idx_reading_sessions_date_device ON reading_sessions(start_time DESC, device);
```

### Example Usage

**Insert single ebook reading session:**
```sql
INSERT INTO reading_sessions (
  book_id, start_time, duration_minutes, pages_read, device, media_type, data_source
) VALUES (
  (SELECT book_id FROM books WHERE title='Mate'),
  '2025-10-31 14:30:00'::TIMESTAMP,
  45, 23, 'boox-palma-2', 'ebook', 'koreader'
);
```

**Insert tandem reading sessions (audio + ebook simultaneously):**
```sql
-- Audio session: 9:00-10:00
INSERT INTO reading_sessions (
  book_id, start_time, duration_minutes, device, media_type, data_source, read_instance_id, is_parallel_read
) VALUES (
  1, '2025-10-31 09:00:00'::TIMESTAMP, 60, 'iphone-x', 'audiobook', 'bookplayer',
  'a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6'::UUID, true
);

-- Ebook session: 8:45-10:15 (overlaps with audio)
INSERT INTO reading_sessions (
  book_id, start_time, duration_minutes, pages_read, device, media_type, data_source, read_instance_id, is_parallel_read
) VALUES (
  1, '2025-10-31 08:45:00'::TIMESTAMP, 90, 45, 'boox-palma-2', 'ebook', 'koreader',
  'a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6'::UUID, true
);
```

**Query tandem reading sessions:**
```sql
SELECT
  read_instance_id,
  COUNT(*) as session_count,
  STRING_AGG(DISTINCT media_type, '+') as formats,
  MIN(start_time) as start,
  MAX(end_time) as end
FROM reading_sessions
WHERE is_parallel_read = true
GROUP BY read_instance_id;
```

**Track re-reads of a book:**
```sql
-- Example: Track how many times book with ID=1 has been read ("Project Hail Mary" in example scenario)
SELECT
  COUNT(DISTINCT read_instance_id) as times_read,
  MIN(start_time) as first_read,
  MAX(start_time) as most_recent_read
FROM reading_sessions
WHERE book_id = 1;  -- book_id is SERIAL, auto-generated during ETL (unique per book in catalog)
```

---

## Automated Behaviors & Constraints

### Triggers and Automatic Updates

**Updated_at Timestamp Triggers** (on all tables with updated_at column)
```sql
-- Automatically update 'updated_at' whenever a record is modified
CREATE TRIGGER update_authors_updated_at
BEFORE UPDATE ON authors
FOR EACH ROW
EXECUTE FUNCTION update_modified_column();

-- Creates function (once per database):
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = CURRENT_TIMESTAMP;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

**Read_count Computed Field** (on books table)
- Automatically computed when queried via VIEW or application logic
- Formula: `COUNT(DISTINCT read_instance_id) FROM reading_sessions WHERE book_id = books.book_id`
- **Note:** Not materialized in table; calculated on-demand for freshness

### Database-Level Constraints

| Table | Constraint | Purpose | Impact |
|-------|-----------|---------|--------|
| reading_sessions | UNIQUE(book_id, start_time, device) | Prevent duplicate imports from same device | Insert rejected if exact match exists |
| reading_sessions | CHECK(duration_minutes > 0) | No zero-duration sessions | Insert/update rejected if duration ≤ 0 |
| reading_sessions | CHECK(start_time <= CURRENT_TIMESTAMP) | No future dates | Insert/update rejected for future times |
| authors | UNIQUE(author_hardcover_id) | Single Hardcover author mapping | NULL allowed; only non-NULL must be unique |
| publishers | UNIQUE(publisher_hardcover_id) | Single Hardcover publisher mapping | NULL allowed; only non-NULL must be unique |
| publishers | UNIQUE(publisher_name) | Canonical publisher names | No duplicates in canonical names |
| books | NOT NULL(title, author_id) | Required identification | Both must be present |

### Foreign Key Constraints

All foreign keys enforce referential integrity with CASCADE DELETE (where noted):

| FK Column | References | Delete Behavior | Notes |
|-----------|-----------|-----------------|-------|
| books.author_id | authors.author_id | RESTRICT | Cannot delete author with books |
| books.publisher_id | publishers.publisher_id | RESTRICT | Cannot delete publisher with books |
| book_editions.book_id | books.book_id | CASCADE | Editions deleted if book is deleted |
| reading_sessions.book_id | books.book_id | CASCADE | Sessions deleted if book is deleted |

---

## Advanced Analytics: Tandem Reading Detection

### Overview

Tandem reading is when you read the same book in parallel using multiple formats (e.g., ebook chapters 1-5 while listening to audiobook chapters 6-15). The schema supports detecting and analyzing these overlapping reads.

### Detection Algorithm

**Definition:** Two reading sessions of the same book are "tandem" if they overlap in time by 7+ days (configurable threshold).

**Logic:**
```
FOR each book_id:
  GET all reading_sessions for that book
  FOR each pair of sessions with different media_types:
    IF session_a.start_time <= session_b.end_time AND
       session_b.start_time <= session_a.end_time AND
       (overlap_days >= 7):
      Mark both sessions: is_parallel_read = TRUE
      Assign same read_instance_id (UUID)
      Set read_number to distinguish read #1, #2, #3 etc.
    END IF
  END FOR
END FOR
```

### SQL Implementation: Identifying Tandem Reads

```sql
-- Find all books with overlapping reading sessions (tandem reads)
SELECT
  b.book_id,
  b.title,
  rs1.session_id as session_1_id,
  rs2.session_id as session_2_id,
  rs1.media_type as format_1,
  rs2.media_type as format_2,
  rs1.start_time as session_1_start,
  rs2.start_time as session_2_start,
  GREATEST(rs1.start_time, rs2.start_time)::date -
  LEAST(rs1.end_time, rs2.end_time)::date as overlap_days,
  rs1.read_instance_id,
  rs1.is_parallel_read
FROM reading_sessions rs1
JOIN reading_sessions rs2 ON
  rs1.book_id = rs2.book_id AND
  rs1.session_id < rs2.session_id AND  -- Avoid duplicates
  rs1.media_type != rs2.media_type      -- Different formats only
JOIN books b ON rs1.book_id = b.book_id
WHERE
  -- Check for overlap: session_1 starts before session_2 ends AND vice versa
  rs1.start_time <= rs2.end_time AND
  rs2.start_time <= rs1.end_time AND
  -- Overlap is 7+ days (configurable)
  GREATEST(rs1.start_time, rs2.start_time)::date -
  LEAST(rs1.end_time, rs2.end_time)::date >= 7
ORDER BY rs1.book_id, rs1.start_time;
```

### Overlap Duration Calculation

**Overlap-aware duration** (don't double-count overlapping time):

```sql
-- For tandem reads, calculate actual reading time (not sum of overlaps)
SELECT
  book_id,
  read_instance_id,
  -- Overlap-aware: one continuous block of reading time
  (MAX(end_time) - MIN(start_time)) as overlap_aware_duration_minutes,
  -- Raw sum: may double-count overlapping time
  SUM(duration_minutes) as total_duration_all_formats
FROM reading_sessions
WHERE is_parallel_read = TRUE
GROUP BY book_id, read_instance_id;
```

### Example Tandem Reading Scenario

**Book:** "The Midnight Library" by Matt Haig

| Session | Format | Start Date | End Date | Pages/Duration | Overlap |
|---------|--------|-----------|----------|-----------------|---------|
| 1 | Ebook | 2024-10-01 | 2024-10-10 | 150 pages | ← |
| 2 | Audiobook | 2024-10-05 | 2024-10-12 | 420 minutes | → |

**Overlap Analysis:**
- Session 1: Oct 1-10 (ebook reading)
- Session 2: Oct 5-12 (audiobook listening)
- **Overlap dates:** Oct 5-10 (6 days) — BELOW 7-day threshold, so NOT tandem
- If Session 2 extended to Oct 14: Oct 5-10 (10 days) — ABOVE threshold, IS tandem

**Assigned read_instance_id:** `550e8400-e29b-41d4-a716-446655440000`
**Overlap-aware duration:** Oct 1 - Oct 12 = 11 days = 15,840 minutes
**Raw sum:** 420 + 150 pages ≠ comparable to audiobook minutes (different units)

---

## Table: `sync_status`

### Purpose
Tracks ETL synchronization state and metadata for each data source, enabling incremental updates, progress monitoring, and error recovery across pipeline runs.

### Schema

| Column | Type | Constraints | Source | Description |
|--------|------|-----------|--------|-------------|
| `sync_id` | SERIAL | PRIMARY KEY | Computed | Auto-incrementing sync operation identifier |
| `source_name` | VARCHAR(50) | NOT NULL, UNIQUE | ETL | Data source identifier (koreader, hardcover_books, hardcover_activities, hardcover_editions, kindle, audible) |
| `last_sync_time` | TIMESTAMP | | ETL | Most recent successful sync completion timestamp |
| `last_sync_cursor` | VARCHAR(255) | | ETL | Cursor/bookmark for incremental queries (e.g., max timestamp, last_id, offset) |
| `records_synced` | INT | DEFAULT 0 | ETL | Count of records processed in last sync run |
| `records_created` | INT | DEFAULT 0 | ETL | Count of new records inserted in last sync |
| `records_updated` | INT | DEFAULT 0 | ETL | Count of existing records modified in last sync |
| `sync_status` | VARCHAR(50) | DEFAULT 'pending' | ETL | Status: pending, in_progress, success, partial_success, failed |
| `error_message` | TEXT | | ETL | Error details if sync_status = 'failed' or 'partial_success' |
| `sync_duration_seconds` | INT | | ETL | Elapsed time for sync operation (for performance tracking) |
| `next_scheduled_sync` | TIMESTAMP | | ETL | When next sync is scheduled to run |
| `sync_mode` | VARCHAR(50) | DEFAULT 'incremental' | ETL | Type of sync: full_refresh (all records), incremental (delta only), or validation (integrity check) |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Computed | Record creation timestamp |
| `updated_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Computed | Last modification timestamp |

### Design Rationale

**Incremental Sync Strategy:**
- `last_sync_cursor`: Stores the last value processed (e.g., max timestamp from Hardcover API activities). On next run, query only records created after this cursor. This reduces API calls and database load.
- Example cursors:
  - KOReader: `"2025-10-31T14:30:00Z"` (last modified timestamp in statistics.sqlite3)
  - Hardcover Activities: `activity_id=12345` or `created_at > 2025-10-31T14:30:00Z`
  - Kindle: `export_batch_5` (last processed export batch identifier)

**Status Tracking:**
- `sync_status`: Enables monitoring and alerting:
  - `pending`: Not yet run in this cycle
  - `in_progress`: Currently executing
  - `success`: Completed without errors
  - `partial_success`: Completed but some records failed (e.g., 950/1000 records loaded)
  - `failed`: Aborted due to error (see `error_message`)

**Performance Monitoring:**
- `sync_duration_seconds`: Helps identify performance regressions or API bottlenecks
- `records_synced`, `records_created`, `records_updated`: Indicates data volume and provides audit trail

**Sync Modes:**
- `full_refresh`: Re-fetch all records from source (slower, safer for validation)
- `incremental`: Only fetch new/changed records since last_sync_cursor (fast, normal operation)
- `validation`: Integrity check - verify counts, spot-check records, detect anomalies

### Example Sync Records

```sql
INSERT INTO sync_status (
  source_name, last_sync_time, last_sync_cursor,
  records_synced, records_created, records_updated, sync_status, sync_mode
) VALUES
  ('hardcover_activities', '2025-10-31 14:35:00', 'activity_id=125432',
   342, 12, 330, 'success', 'incremental'),
  ('koreader', '2025-10-31 14:20:00', '2025-10-31 14:20:00',
   1850, 0, 1850, 'success', 'incremental'),
  ('hardcover_books', '2025-10-31 13:45:00', 'book_id=999999',
   0, 0, 0, 'success', 'incremental'),
  ('kindle', '2025-10-30 22:15:00', 'batch_export_2025_10_30',
   0, 0, 0, 'success', 'incremental');
```

### SQL: Initialize or Reset Sync Status for a Source

```sql
-- Initialize new sync source
INSERT INTO sync_status (source_name, sync_status, sync_mode)
VALUES ('new_source_name', 'pending', 'full_refresh')
ON CONFLICT (source_name) DO NOTHING;

-- Reset a failed sync to retry (full_refresh mode)
UPDATE sync_status
SET sync_status = 'pending',
    sync_mode = 'full_refresh',
    last_sync_cursor = NULL
WHERE source_name = 'hardcover_activities'
  AND sync_status = 'failed';
```

### SQL: Update After Successful Sync

```sql
UPDATE sync_status
SET
  last_sync_time = NOW(),
  last_sync_cursor = $1,  -- New cursor value (e.g., max timestamp or ID)
  records_synced = $2,
  records_created = $3,
  records_updated = $4,
  sync_status = 'success',
  sync_duration_seconds = EXTRACT(EPOCH FROM (NOW() - sync_start_time))::INT,
  next_scheduled_sync = NOW() + INTERVAL '1 hour',
  updated_at = NOW()
WHERE source_name = $5;
```

---

## Advanced Analytics: Re-read Detection and Tracking

### Overview

Re-reads are when you read the same book multiple times. The schema supports tracking:
- Number of times a book has been read
- Which read it is (1st, 2nd, 3rd, etc.)
- Different formats across reads
- Time between reads

### Detection Algorithm

**Definition:** A re-read is identified when multiple `reading_sessions` exist for the same `book_id`. Each distinct read is grouped by `read_instance_id` (UUID).

**Logic:**
```
FOR each book_id:
  GET all reading_sessions ordered by start_time
  FOR each session group (contiguous temporal block):
    Assign new UUID → read_instance_id
    Assign ordinal number → read_number (1st, 2nd, 3rd)
    Set is_parallel_read flag based on overlap with other sessions
  END FOR
END FOR
```

### SQL Implementation: Identifying Re-reads

```sql
-- Method 1: Count distinct reads per book
SELECT
  b.book_id,
  b.title,
  COUNT(DISTINCT rs.read_instance_id) as times_read,
  MIN(rs.start_time) as first_read_date,
  MAX(rs.start_time) as most_recent_read_date,
  (MAX(rs.start_time)::date - MIN(rs.start_time)::date) as days_between_reads
FROM reading_sessions rs
JOIN books b ON rs.book_id = b.book_id
GROUP BY b.book_id, b.title
HAVING COUNT(DISTINCT rs.read_instance_id) > 1
ORDER BY times_read DESC;
```

```sql
-- Method 2: Assign read_instance_id (for ETL backfill)
WITH re_reads AS (
  SELECT
    rs.session_id,
    rs.book_id,
    rs.start_time,
    ROW_NUMBER() OVER (PARTITION BY rs.book_id ORDER BY rs.start_time) as read_number,
    gen_random_uuid() as new_read_instance_id  -- Generate UUID for each group
  FROM reading_sessions rs
)
UPDATE reading_sessions
SET
  read_instance_id = re_reads.new_read_instance_id,
  read_number = re_reads.read_number
FROM re_reads
WHERE reading_sessions.session_id = re_reads.session_id;
```

```sql
-- Method 3: Show re-reads with format diversity
SELECT
  b.title,
  rs.read_number as which_read,
  rs.start_time as read_date,
  STRING_AGG(DISTINCT rs.media_type, ', ') as formats_used,
  COUNT(DISTINCT rs.media_type) as format_count,
  SUM(rs.duration_minutes) as total_time_this_read
FROM reading_sessions rs
JOIN books b ON rs.book_id = b.book_id
WHERE rs.read_instance_id IS NOT NULL
GROUP BY b.book_id, b.title, rs.read_instance_id, rs.read_number, rs.start_time
ORDER BY b.book_id, rs.read_number;
```

### Example Re-read Scenario

**Book:** "Project Hail Mary" by Andy Weir

| Read # | Format | Start Date | End Date | Duration |
|--------|--------|-----------|----------|----------|
| 1 | Ebook | 2023-02-15 | 2023-03-05 | 18 hours |
| 2 | Audiobook | 2024-01-10 | 2024-01-20 | 14 hours |
| 3 | Ebook | 2025-09-01 | 2025-10-31 | 20 hours |

**Tracking Fields:**
- `book_id`: 42
- `books.read_count`: 3 (computed from COUNT(DISTINCT read_instance_id))
- `reading_sessions.read_instance_id`: UUID assigned per read
- `reading_sessions.read_number`: 1, 2, 3 (sequential)

**Query Example:**
```sql
-- Example: Show all reads of book with ID=42 (book_id is auto-assigned during ETL, stable per book)
SELECT
  read_number,
  media_type,
  DATE(start_time) as read_date,
  (end_time - start_time) as duration
FROM reading_sessions
WHERE book_id = 42  -- Use book_id (SERIAL pk) to identify the specific book across all reading sessions
ORDER BY read_number;

-- Result:
-- read_number | media_type | read_date  | duration
-- 1           | ebook      | 2023-02-15 | 18:00:00
-- 2           | audiobook  | 2024-01-10 | 14:00:00
-- 3           | ebook      | 2025-09-01 | 20:00:00
```

### Edge Cases & Handling

| Scenario | Handling | Notes |
|----------|----------|-------|
| **Same-day re-read** | Assign different read_instance_id | Different UUID even if same day |
| **Different editions** | Same book_id, same read_instance_id | Focus is on book content, not format |
| **Interruption gap** | If gap > 30 days, likely new read | Configurable threshold |
| **Format switching mid-read** | Same read_instance_id | Tandem reading detected via is_parallel_read flag |
| **Null start/end times** | Skip from re-read count | Require valid dates for tracking |

---

## Data Type Rationale

### Choosing the Right Data Types

| Data Type | Usage | Rationale | Examples |
|-----------|-------|-----------|----------|
| **VARCHAR(n)** | Text with max length | Bounded strings prevent typos/corrupted imports; indexes more efficient | author_name (255), publisher_name (255), title (255) |
| **TEXT** | Unbounded text | No length limit; slower indexing but handles long content | description, notes, content_warnings |
| **INT / BIGSERIAL** | Sequential IDs | Auto-incrementing; efficient for PRIMARY KEYs and FKs | book_id (SERIAL), session_id (BIGSERIAL) |
| **TIMESTAMP** | Date + time | UTC-aware; supports time-series queries without conversion | start_time, created_at, updated_at |
| **DATE** | Date only | Smaller storage than TIMESTAMP; for calendar dates | published_date, date_acquired |
| **DECIMAL(3,2)** | Precise decimals | Avoids floating-point rounding; critical for ratings | hardcover_rating (0-5.00), user_rating |
| **NUMERIC(5,2)** | Flexible precision | Larger range than DECIMAL; supports 1-999.99 | series_number (supports 2.5 for novellas) |
| **BOOLEAN** | True/False flags | Minimal storage; clear intent for binary states | is_bipoc, is_lgbtq, is_parallel_read, user_owns_ebook |
| **UUID** | Globally unique IDs | No collisions across distributed systems; supports tandem reading tracking | read_instance_id |
| **JSONB** | Nested data | Queryable with operators (@>, contains); supports arrays and objects | alternate_names, genres, moods, content_warnings, cached_tags |
| **INT[]** | Arrays | Efficient for lists of integers; GIN-indexable | (formerly used, now JSONB preferred) |
| **TEXT[]** | String arrays | Simple lists of text; used for historical compatibility | alternate_names (publishers table) |

### Type Decisions & Trade-offs

**Why SERIAL for book_id vs. Hardcover IDs?**
- SERIAL is agnostic to data sources (KOReader, Hardcover, Kindle, Audible)
- Hardcover ID would fail for books not in Hardcover catalog
- Traceability: `hardcover_book_id` field stores the source ID for cross-referencing

**Why DECIMAL(3,2) for ratings instead of FLOAT?**
- Ratings are finite (0-5.00) with exactly 2 decimals
- DECIMAL avoids floating-point rounding errors (important for averaging)
- FLOAT would risk 4.23 ≈ 4.229999999... during calculations

**Why JSONB for genres/moods instead of separate tables?**
- Genres are read-only (from Hardcover API)
- No need for FK relationships
- Queryable with `@>` operator and GIN index
- Flexible: new genres don't require schema migrations

**Why BIGSERIAL for session_id instead of SERIAL?**
- Projected: 50,000-100,000 records per year (scaling expectation)
- SERIAL max: ~2.1 billion (sufficient but close to limit at scale)
- BIGSERIAL: ~9.2 quintillion (future-proof)

---

## Views

### View: `book_stats`

**Purpose:** Comprehensive reading statistics with multi-media aggregation and reading speed analytics.

**Columns with Formulas:**
- `last_opened`: `MAX(start_time)` - Most recent reading session
- `total_read_time_ebook_minutes`: `SUM(duration_minutes)` WHERE media_type='ebook'
- `total_read_time_audio_minutes`: `SUM(duration_minutes)` WHERE media_type='audiobook'
- `total_read_time_minutes`: `total_read_time_ebook_minutes + total_read_time_audio_minutes`
- `total_pages_read_ebook`: `SUM(pages_read)` WHERE media_type='ebook' AND pages_read IS NOT NULL
- `ebook_session_count`: `COUNT(*)` WHERE media_type='ebook'
- `audiobook_session_count`: `COUNT(*)` WHERE media_type='audiobook'
- `total_sessions`: `ebook_session_count + audiobook_session_count`
- `read_count`: `COUNT(DISTINCT read_instance_id)` - Number of distinct reads
- `avg_reading_speed_pages_per_minute`: `total_pages_read_ebook::NUMERIC / NULLIF(total_read_time_ebook_minutes, 0)` - Ebook only

**Example:**
```sql
-- Query aggregated stats for a specific book (book_id is SERIAL, generated during ETL)
SELECT * FROM book_stats WHERE book_id = 1;
-- Result: Last opened date, time spent per format, reading speed, re-read count
-- Note: book_id=1 represents a specific book in your catalog (e.g., "Mate" by Ali Hazelwood)
```

### View: `reading_timeline`

**Purpose:** Chronological view of all reading events with enrichment from books, publishers, and authors.

**Columns:** session_id, start_time, end_time (computed: start_time + duration_minutes), duration_minutes, pages_read, media_type, device, data_source, read_instance_id, is_parallel_read, read_number, book_id, title, author, series_name, series_number, cached_tags, publisher, author_name

**Note:** End_time is computed during query time, not stored (pure computed column)

### View: `publisher_analytics`

**Purpose:** Publisher-level reading analytics including both community and personal ratings.

**Columns with Formulas:**
- `books_read`: `COUNT(DISTINCT books.book_id)` WHERE books.publisher_id = publishers.publisher_id
- `total_sessions`: `COUNT(reading_sessions.session_id)` for all books by publisher
- `total_ebook_minutes`: `SUM(duration_minutes)` WHERE media_type='ebook'
- `total_audio_minutes`: `SUM(duration_minutes)` WHERE media_type='audiobook'
- `avg_hardcover_rating`: `AVG(books.hardcover_rating)` across all publisher's books
- `avg_user_rating`: `AVG(books.user_rating)` across all publisher's books

### View: `author_analytics`

**Purpose:** Author-level analytics with diversity metrics.

**Columns with Formulas:**
- `books_read`: `COUNT(DISTINCT books.book_id)` WHERE books.author_id = authors.author_id
- `total_sessions`: `COUNT(reading_sessions.session_id)` for all books by author
- `total_ebook_minutes`: `SUM(duration_minutes)` WHERE media_type='ebook'
- `total_audio_minutes`: `SUM(duration_minutes)` WHERE media_type='audiobook'
- `avg_hardcover_rating`: `AVG(books.hardcover_rating)` across all author's books
- `avg_user_rating`: `AVG(books.user_rating)` across all author's books
- `is_bipoc`, `is_lgbtq`: Inherited directly from authors table

### View: `tandem_reading_sessions`

**Purpose:** Analyze overlapping reads with overlap-aware duration calculations.

**Columns with Formulas:**
- `session_count`: `COUNT(reading_sessions.session_id)` grouped by read_instance_id
- `distinct_media_types`: `COUNT(DISTINCT media_type)` (1=single format, 2=tandem reading)
- `instance_start`: `MIN(start_time)` - Earliest session in this read instance
- `instance_end`: `MAX(start_time + INTERVAL '1 minute' * duration_minutes)` - Latest session end
- `media_types_combined`: `STRING_AGG(DISTINCT media_type, '+')` (e.g., "ebook+audiobook")
- `total_duration_all_formats`: `SUM(duration_minutes)` across all sessions (may double-count overlaps)
- `overlap_aware_duration`: `(instance_end - instance_start)` in minutes - True elapsed time (avoids double-counting)

---

## Query Examples

### Basic Analytics

**Total reading time in 2024 (ebook only):**
```sql
SELECT SUM(duration_minutes) as total_minutes
FROM reading_sessions
WHERE EXTRACT(YEAR FROM start_time) = 2024 AND media_type = 'ebook';
```

**Reading time by month:**
```sql
SELECT
  DATE_TRUNC('month', start_time)::DATE as month,
  SUM(duration_minutes) as total_minutes,
  COUNT(DISTINCT book_id) as unique_books,
  COUNT(*) as session_count
FROM reading_sessions
GROUP BY DATE_TRUNC('month', start_time)
ORDER BY month DESC;
```

### Multi-Format Analytics

**Books read in both formats:**
```sql
SELECT
  b.title,
  b.author,
  COUNT(*) FILTER (WHERE rs.media_type='ebook') as ebook_sessions,
  COUNT(*) FILTER (WHERE rs.media_type='audiobook') as audio_sessions,
  SUM(rs.duration_minutes) FILTER (WHERE rs.media_type='ebook') as ebook_minutes,
  SUM(rs.duration_minutes) FILTER (WHERE rs.media_type='audiobook') as audio_minutes,
  AVG(rs.duration_minutes) FILTER (WHERE rs.media_type='audiobook') as avg_audiobook_session
FROM books b
JOIN reading_sessions rs ON b.book_id = rs.book_id
WHERE 'ebook' = ANY(b.media_types_owned) AND 'audiobook' = ANY(b.media_types_owned)
GROUP BY b.book_id, b.title, b.author
ORDER BY audio_minutes DESC;
```

**Reading speed by device:**
```sql
SELECT
  rs.device,
  AVG((rs.pages_read::NUMERIC / NULLIF(rs.duration_minutes, 0))) as avg_pages_per_minute,
  COUNT(*) as session_count,
  SUM(rs.duration_minutes) as total_minutes
FROM reading_sessions rs
WHERE rs.media_type = 'ebook'
GROUP BY rs.device
ORDER BY avg_pages_per_minute DESC;
```

### Re-Read Analytics

**Books re-read multiple times:**
```sql
SELECT
  b.title,
  b.author,
  COUNT(DISTINCT rs.read_instance_id) as times_read,
  MIN(rs.start_time) as first_read,
  MAX(rs.start_time) as latest_read,
  SUM(rs.duration_minutes) as total_time_invested
FROM books b
JOIN reading_sessions rs ON b.book_id = rs.book_id
GROUP BY b.book_id, b.title, b.author
HAVING COUNT(DISTINCT rs.read_instance_id) > 1
ORDER BY times_read DESC;
```

### Author & Diversity Analytics

**Reading patterns by author diversity:**
```sql
SELECT
  CASE
    WHEN a.is_bipoc THEN 'BIPOC Authors'
    WHEN a.is_lgbtq THEN 'LGBTQ+ Authors'
    ELSE 'Other Authors'
  END as author_category,
  COUNT(DISTINCT b.book_id) as books_read,
  SUM(rs.duration_minutes) as total_reading_time,
  AVG(b.user_rating) as avg_user_rating
FROM books b
LEFT JOIN authors a ON b.author_id = a.author_id
LEFT JOIN reading_sessions rs ON b.book_id = rs.book_id
GROUP BY author_category
ORDER BY total_reading_time DESC;
```

### Tandem Reading Analysis

**Identify overlapping reads:**
```sql
SELECT * FROM tandem_reading_sessions
WHERE distinct_media_types = 2
ORDER BY instance_start DESC;
```

**Compare overlap-aware vs. raw duration:**
```sql
SELECT
  book_id,
  read_instance_id,
  total_duration_all_formats,
  overlap_aware_duration,
  (total_duration_all_formats - overlap_aware_duration) as overlapping_time_minutes
FROM tandem_reading_sessions
WHERE distinct_media_types = 2
ORDER BY overlapping_time_minutes DESC;
```

---

## Performance Considerations

### Index Strategy

**Single-Column Indexes (Primary Keys, Foreign Keys):**
- **book_id:** Primary join key for dimensional analytics
- **start_time:** Time-range queries (month/year aggregations)
- **device:** Device-specific reading patterns
- **media_type:** Partition ebook vs. audiobook queries
- **read_instance_id:** Tandem reading analysis

**Composite Indexes for Common Query Patterns:**
```sql
-- Most frequent query: sessions for a book ordered by date
CREATE INDEX idx_reading_sessions_book_date ON reading_sessions(book_id, start_time DESC);

-- Device + time filtering (reading patterns by device)
CREATE INDEX idx_reading_sessions_device_date ON reading_sessions(device, start_time DESC);

-- Tandem reading detection (overlapping sessions)
CREATE INDEX idx_reading_sessions_parallel ON reading_sessions(is_parallel_read, read_instance_id);

-- Author analytics (books by author, filtered by diversity)
CREATE INDEX idx_books_author_diversity ON books(author_id, is_bipoc, is_lgbtq);

-- Genre queries (JSONB tag filtering)
CREATE INDEX idx_books_tags_gin ON books USING GIN(cached_tags);
```

**Index Maintenance:**
- Monitor index bloat with `pg_stat_user_indexes`
- Vacuum reading_sessions weekly due to append-only pattern
- REINDEX on large insertions (>10,000 rows) to maintain query performance

### Scaling Expectations
- **Current data:** ~2,734 sessions (KOReader)
- **After audiobook integration (Epic 4):** ~5,000-10,000 sessions
- **After historical import (Epic 5):** ~50,000-100,000 sessions

### Query Optimization Tips
1. Always filter by `start_time` range when possible
2. Use `media_type` to partition queries
3. Aggregate via views when possible
4. Use JSONB `@>` operator for tag queries (GIN index optimized)
5. For tandem reads, check `is_parallel_read = true` first

---

## Schema Evolution & Versioning

**Schema Version:** 2.0 (2025-10-31)

**Backward Compatible Additions:**
- New columns with defaults (all nullable)
- New indexes
- New views

**Breaking Changes from v1.0:**
- Separate authors table (requires FKs)
- Rating field renamed (hardcover_rating)
- Publisher column renames
- New required tracking fields

**Future Enhancements (Planned):**
- **Epic 4:** Narrator field for audiobook analytics
- **Epic 5:** Historical reading sessions from Kindle/Audible
- **Future:** Materialized views for complex aggregations
- **Future:** Partitioning reading_sessions by year for scale

---

## Migration & Deployment

### Migrating from Schema v1.0 to v2.0

**Pre-Migration Checklist:**
- [ ] Backup production database: `pg_dump bookhelper > backup_v1.0.sql`
- [ ] Test migration on staging environment first
- [ ] Estimated downtime: 5-10 minutes for <50,000 records
- [ ] Have rollback plan: restore from backup

**Migration Steps:**

**Step 1: Create new tables (non-destructive)**
```sql
-- Create authors table
CREATE TABLE authors AS SELECT DISTINCT author FROM books_v1 WHERE author IS NOT NULL;
ALTER TABLE authors ADD COLUMN author_id SERIAL PRIMARY KEY;
-- ... (populate from Hardcover API)

-- Create publishers table similarly
-- ...

-- Create new books table with v2.0 schema
CREATE TABLE books_v2 (...);  -- See table definitions above
```

**Step 2: Migrate data (with transformation)**
```sql
-- Migrate from v1.0 books to v2.0 books
INSERT INTO books (
  title, author_id, isbn_13, publisher_id, page_count, language,
  hardcover_rating, user_rating, created_at, updated_at
)
SELECT
  b1.title,
  a.author_id,
  b1.isbn_13,
  p.publisher_id,
  b1.page_count,
  b1.language,
  b1.rating as hardcover_rating,
  b1.user_rating,
  b1.created_at,
  CURRENT_TIMESTAMP
FROM books_v1 b1
LEFT JOIN authors a ON b1.author = a.author_name
LEFT JOIN publishers p ON b1.publisher = p.publisher_name;
```

**Step 3: Validation**
```sql
-- Verify row counts
SELECT COUNT(*) FROM books_v1;     -- Original count
SELECT COUNT(*) FROM books_v2;     -- New count (should match)

-- Check for NULL foreign keys
SELECT COUNT(*) FROM books_v2 WHERE author_id IS NULL;
SELECT COUNT(*) FROM books_v2 WHERE publisher_id IS NULL;
```

**Step 4: Switch and cleanup (zero-downtime possible with views)**
```sql
-- Option A: Rename tables
ALTER TABLE books RENAME TO books_v1_backup;
ALTER TABLE books_v2 RENAME TO books;

-- Option B: Use views for backward compatibility
CREATE VIEW books_v1_compat AS
SELECT b.book_id, b.title, a.author_name as author, ...
FROM books b
LEFT JOIN authors a ON b.author_id = a.author_id;
```

**Post-Migration:**
- [ ] Verify application functionality with v2.0 schema
- [ ] Run ANALYZE to update query planner statistics
- [ ] Monitor performance for 24 hours
- [ ] Archive v1.0 backup after 30-day retention period

See `SCHEMA-CHANGES-SUMMARY.md` for complete list of changes from v1.0.
See `ETL-MAPPING-GUIDE.md` for data transformation procedures.

---

## Appendix A: Sample Data Set

Use these INSERT statements to populate a development database with realistic test data:

```sql
-- Sample Authors
INSERT INTO authors (author_name, author_hardcover_id, alternate_names, born_year, is_bipoc, is_lgbtq, book_count)
VALUES
  ('Ali Hazelwood', 'hc_author_1001', '["Ali Hazelwood"]', 1986, true, false, 8),
  ('Matt Haig', 'hc_author_1002', '["Matt Haig"]', 1975, false, false, 25),
  ('Andy Weir', 'hc_author_1003', '["Andy Weir"]', 1972, false, false, 5),
  ('N.K. Jemisin', 'hc_author_1004', '["N.K. Jemisin"]', 1972, true, true, 12);

-- Sample Publishers
INSERT INTO publishers (publisher_name, publisher_hardcover_id, alternate_names, country)
VALUES
  ('Harper Voyager', 123, ARRAY['Harper', 'Harper Fiction'], 'USA'),
  ('Canongate Books', 456, ARRAY['Canongate'], 'UK'),
  ('Crown Publishing', 789, ARRAY['Crown', 'Random House Crown'], 'USA'),
  ('Orbit', 321, ARRAY['Orbit Books'], 'UK');

-- Sample Books
INSERT INTO books (title, author_id, isbn_13, publisher_id, page_count, language,
                   hardcover_rating, user_rating, user_rating_date,
                   genres, moods, user_owns_ebook, user_owns_audiobook, user_owns_physical,
                   user_reading_status, user_added_date, created_at)
VALUES
  ('Mate', 1, '978-0063119596', 1, 320, 'en', 4.23, 4.5, '2025-10-31'::TIMESTAMP,
   '["Romance", "Science Fiction"]'::jsonb, '["spicy", "witty"]'::jsonb, true, true, true,
   'finished', '2025-09-01'::TIMESTAMP, CURRENT_TIMESTAMP),

  ('The Midnight Library', 2, '978-1620405666', 2, 448, 'en', 4.14, 4.0, '2025-10-15'::TIMESTAMP,
   '["Fantasy", "Literary Fiction"]'::jsonb, '["reflective", "hopeful"]'::jsonb, true, false, true,
   'finished', '2024-06-15'::TIMESTAMP, CURRENT_TIMESTAMP),

  ('Project Hail Mary', 3, '978-0593135204', 3, 544, 'en', 4.73, 5.0, '2025-10-31'::TIMESTAMP,
   '["Science Fiction", "Adventure"]'::jsonb, '["thrilling", "inspirational"]'::jsonb, true, true, false,
   'finished', '2023-02-01'::TIMESTAMP, CURRENT_TIMESTAMP),

  ('The City We Became', 4, '978-0316509848', 4, 512, 'en', 4.08, 4.5, '2025-10-28'::TIMESTAMP,
   '["Science Fiction", "Fantasy"]'::jsonb, '["dark", "urban"]'::jsonb, true, false, false,
   'reading', '2025-10-01'::TIMESTAMP, CURRENT_TIMESTAMP);

-- Sample Reading Sessions
INSERT INTO reading_sessions (book_id, start_time, duration_minutes, pages_read, device, media_type, data_source, read_instance_id)
VALUES
  (1, '2025-10-25 19:00:00'::TIMESTAMP, 45, 32, 'boox-palma-2', 'ebook', 'koreader', 'a1b2c3d4-e5f6-4a8a-9b0c-d1e2f3a4b5c6'::uuid),
  (1, '2025-10-26 14:30:00'::TIMESTAMP, 60, 40, 'boox-palma-2', 'ebook', 'koreader', 'a1b2c3d4-e5f6-4a8a-9b0c-d1e2f3a4b5c6'::uuid),
  (1, '2025-10-25 09:00:00'::TIMESTAMP, 90, 0, 'iphone-14', 'audiobook', 'bookplayer', 'a1b2c3d4-e5f6-4a8a-9b0c-d1e2f3a4b5c7'::uuid),

  (2, '2024-10-15 20:00:00'::TIMESTAMP, 40, 28, 'boox-palma-2', 'ebook', 'koreader', 'b2c3d4e5-f6a7-4b9a-9c0d-e1f2a3b4c5d6'::uuid),
  (2, '2024-10-16 18:30:00'::TIMESTAMP, 55, 35, 'boox-palma-2', 'ebook', 'koreader', 'b2c3d4e5-f6a7-4b9a-9c0d-e1f2a3b4c5d6'::uuid),

  (3, '2023-02-15 14:00:00'::TIMESTAMP, 120, 60, 'boox-palma-2', 'ebook', 'koreader', 'c3d4e5f6-a7b8-4c9a-9d0e-f2a3b4c5d6e7'::uuid),
  (3, '2024-01-10 09:00:00'::TIMESTAMP, 120, 0, 'iphone-13', 'audiobook', 'bookplayer', 'c3d4e5f6-a7b8-4c9a-9d0e-f2a3b4c5d6e8'::uuid),

  (4, '2025-10-01 19:00:00'::TIMESTAMP, 50, 35, 'boox-palma-2', 'ebook', 'koreader', 'd4e5f6a7-b8c9-4d9a-9e0f-a3b4c5d6e7f8'::uuid);

-- Sample Book Editions (physical library)
INSERT INTO book_editions (book_id, edition_format, edition_name, publication_year, condition, date_acquired)
VALUES
  (1, 'hardcover', 'First Edition Hardcover', 2023, 'like-new', '2023-10-15'::date),
  (1, 'paperback', 'Mass Market Paperback', 2024, 'good', '2024-06-01'::date),
  (2, 'hardcover', 'UK Hardcover', 2020, 'like-new', '2024-06-20'::date),
  (3, 'hardcover', 'First Edition', 2021, 'excellent', '2023-02-10'::date);
```

**Testing the Sample Data:**

```sql
-- Verify inserts
SELECT COUNT(*) as author_count FROM authors;       -- Expected: 4
SELECT COUNT(*) as publisher_count FROM publishers; -- Expected: 4
SELECT COUNT(*) as book_count FROM books;           -- Expected: 4
SELECT COUNT(*) as session_count FROM reading_sessions; -- Expected: 8

-- Test book_stats view
SELECT * FROM book_stats WHERE book_id = 1;

-- Test tandem reading detection
SELECT read_instance_id, COUNT(*) as session_count,
       STRING_AGG(DISTINCT media_type, '+') as formats
FROM reading_sessions
WHERE book_id = 1
GROUP BY read_instance_id;

-- Test diversity analytics
SELECT a.author_name, COUNT(DISTINCT b.book_id) as books_authored,
       a.is_bipoc, a.is_lgbtq
FROM authors a
LEFT JOIN books b ON a.author_id = b.author_id
GROUP BY a.author_id, a.author_name, a.is_bipoc, a.is_lgbtq;
```

---

## Appendix B: Quick Reference

**Key Formulas:**
- **read_count:** `COUNT(DISTINCT read_instance_id)` per book
- **overlap_aware_duration:** `MAX(end_time) - MIN(start_time)` for tandem reads
- **avg_reading_speed:** `SUM(pages_read) / SUM(duration_minutes)` for ebook only

**Common Queries:**
1. Books re-read multiple times: `SELECT * FROM books WHERE read_count > 1`
2. Reading time by month: `SELECT DATE_TRUNC('month', start_time), SUM(duration_minutes) FROM reading_sessions GROUP BY DATE_TRUNC('month', start_time)`
3. Tandem reading instances: `SELECT * FROM tandem_reading_sessions WHERE distinct_media_types = 2`
4. Diversity metrics: `SELECT * FROM author_analytics WHERE is_bipoc = true OR is_lgbtq = true`

**Production Checklist:**
- [ ] Backup before applying schema
- [ ] Test migrations on staging
- [ ] Run VACUUM and ANALYZE after initial data load
- [ ] Monitor query performance for 24 hours
- [ ] Verify application against all views
- [ ] Document any custom indexes needed for your queries
