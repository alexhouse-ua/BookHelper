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

## Table: `authors`

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
| `alternate_names` | TEXT[] | DEFAULT '{}' | Hardcover API | Array of pen names and pseudonyms |
| `author_slug` | VARCHAR(255) | | Hardcover API | URL-friendly identifier |
| `author_hardcover_id` | VARCHAR(100) | UNIQUE | Hardcover API | Hardcover API author ID |
| `books_count` | INT | | Hardcover API | Total published works |
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
| `publisher_hardcover_id` | INT | UNIQUE | Hardcover API | Hardcover API publisher ID (P1) |
| `canonical_hardcover_id` | INT | | Hardcover API | Reference to canonical if consolidated (P3) |
| `parent_publisher_id` | INT | FK to publishers | Hardcover API | Parent publisher for imprints (P4) |
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

---

## Table: `books`

### Purpose
Book master data with metadata enrichment from Hardcover API, KOReader statistics, and physical library tracking. Immutable dimension table referenced by reading sessions and editions.

### Design Rationale

**Field Organization by Data Category (not tiers):**
- Clearly separate different types of information
- Support multi-format ownership (ebook, audiobook, physical)
- Track both community ratings (Hardcover) and personal ratings (user)
- Maintain author relationship via FK while keeping colloquial name
- Support series tracking with separate name and numeric position
- Include audiobook duration for listening analytics

**Multi-Format Ownership:**
- `media_types_owned`: Formats user owns (ebook, audiobook)
- `owned_physical_formats`: Physical formats owned (hardcover, paperback, special-edition)
- `owned_special_editions`: Details of special editions collected
- Linked to `book_editions` table for detailed edition info

**Rating Clarity:**
- `hardcover_rating`: Community rating from Hardcover (0-5 scale)
- `user_rating`: Your personal rating of the book
- `user_rating_date`: When you rated it (for temporal analysis)

**Series Support:**
- `series_name`: Name of series (e.g., "Hani Khan")
- `series_number`: Position in series (NUMERIC(5,2) supports "2.5" for novellas)

### Schema

| Column | Type | Constraints | Source | Description |
|--------|------|-----------|--------|-------------|
| **CORE IDENTIFICATION** | | | | |
| `book_id` | SERIAL | PRIMARY KEY | Computed | Auto-incrementing book identifier |
| `title` | VARCHAR(255) | NOT NULL | KOReader/Hardcover | Book title |
| `author` | VARCHAR(255) | | KOReader | Primary author name (colloquial) |
| `author_id` | INT | FK to authors | Hardcover API | Foreign key to authors table |
| **ISBN / ASIN / IDENTIFIERS** | | | | |
| `isbn_13` | VARCHAR(20) | | Hardcover API | ISBN-13 identifier |
| `isbn_10` | VARCHAR(20) | | Hardcover API | ISBN-10 identifier (legacy) |
| `asin` | VARCHAR(20) | | Hardcover API | Amazon ASIN (Kindle/Audible) |
| `hardcover_book_id` | VARCHAR(100) | | Hardcover API | Hardcover API book entity ID (H1) |
| **PUBLISHER & SERIES** | | | | |
| `publisher_id` | INT | FK to publishers | Hardcover API | Foreign key to publishers table |
| `publisher_name` | VARCHAR(255) | | Hardcover API | Publisher name (convenience column) |
| `series_name` | VARCHAR(255) | | KOReader/Hardcover | Series name |
| `series_number` | NUMERIC(5,2) | | KOReader/Hardcover | Series position (supports 2.5, Prequel) |
| **BOOK DEMOGRAPHICS & METADATA** | | | | |
| `page_count` | INT | | KOReader | Total pages in book |
| `audio_seconds` | INT | | Hardcover API | Total audiobook duration in seconds |
| `language` | CHAR(2) | DEFAULT 'en' | KOReader/Hardcover | ISO 639-1 language code |
| `published_date` | DATE | | Hardcover API | Publication date |
| `description` | TEXT | | Hardcover API | Book summary/synopsis |
| **RATINGS & REVIEWS** | | | | |
| `hardcover_rating` | DECIMAL(3,2) | | Hardcover API | Hardcover community rating (0-5) |
| `hardcover_rating_count` | INT | | Hardcover API | Number of community ratings |
| `user_rating` | DECIMAL(3,2) | | Hardcover API (activities) | Your personal rating (0-5) |
| `user_rating_date` | TIMESTAMP | | Hardcover API (activities) | When you rated this book |
| **AUTHOR METRICS** | | | | |
| `author_hardcover_id` | VARCHAR(100) | | Hardcover API | Hardcover author ID for direct queries |
| `is_bipoc` | BOOLEAN | DEFAULT FALSE | Hardcover API | Author BIPOC diversity flag |
| `is_lgbtq` | BOOLEAN | DEFAULT FALSE | Hardcover API | Author LGBTQ+ diversity flag |
| `author_birth_year` | INT | | Hardcover API | Author birth year |
| `author_books_count` | INT | | Hardcover API | Author's total published works |
| **GENRE & CONTENT** | | | | |
| `cached_tags` | JSONB | DEFAULT '[]' | Hardcover API | Genre/topic tags (queryable via @>) |
| `users_read_count` | INT | | Hardcover API | Hardcover users who read this |
| `users_count` | INT | | Hardcover API | Hardcover users who own this edition |
| **KOREADER & SOURCE DATA** | | | | |
| `file_hash` | VARCHAR(32) | | KOReader | MD5 hash for deduplication |
| `notes` | INT | DEFAULT 0 | KOReader | User annotation count |
| `highlights` | INT | DEFAULT 0 | KOReader | User highlight count |
| `source` | VARCHAR(50) | DEFAULT 'koreader' | ETL | Data origin (koreader, kindle, audible, hardcover) |
| `device_stats_source` | VARCHAR(100) | | KOReader | Backup file source (statistics.sqlite3) |
| **COVER & DISPLAY** | | | | |
| `cover_url` | TEXT | | Hardcover API | CDN URL for book cover image |
| **MULTI-FORMAT OWNERSHIP** | | | | |
| `media_types_owned` | TEXT[] | DEFAULT '{"ebook"}' | User | Formats owned: ["ebook", "audiobook"] |
| `owned_physical_formats` | TEXT[] | DEFAULT '{}' | User | Physical formats: ["hardcover", "paperback", "special-edition"] |
| `owned_special_editions` | TEXT[] | DEFAULT '{}' | User | Special edition details |
| **READ TRACKING** | | | | |
| `read_count` | INT | DEFAULT 1 | Computed | Number of times read (distinct read_instance_id) |
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
| `book_id` | INT | NOT NULL FK | KOReader/Hardcover | Foreign key to books table |
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
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Computed | Record insertion timestamp |
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
SELECT
  COUNT(DISTINCT read_instance_id) as times_read,
  MIN(start_time) as first_read,
  MAX(start_time) as most_recent_read
FROM reading_sessions
WHERE book_id = 1;
```

---

## Views

### View: `book_stats`

**Purpose:** Comprehensive reading statistics with multi-media aggregation and reading speed analytics.

**Columns:**
- `last_opened`: MAX(start_time) - Most recent reading session
- `total_read_time_ebook_minutes`: SUM(duration) for ebook sessions only
- `total_read_time_audio_minutes`: SUM(duration) for audiobook sessions only
- `total_read_time_minutes`: Combined total across all formats
- `total_pages_read_ebook`: SUM(pages_read) for ebook sessions
- `ebook_session_count`: Number of ebook sessions
- `audiobook_session_count`: Number of audiobook sessions
- `total_sessions`: Combined session count
- `read_count`: COUNT(DISTINCT read_instance_id) - Number of reads/re-reads
- `avg_reading_speed_pages_per_minute`: Pages per minute (ebook only)

**Example:**
```sql
SELECT * FROM book_stats WHERE book_id = 1;
-- Result: Last opened date, time spent per format, reading speed, re-read count
```

### View: `reading_timeline`

**Purpose:** Chronological view of all reading events with enrichment from books, publishers, and authors.

**Columns:** session_id, start_time, end_time, duration_minutes, pages_read, media_type, device, data_source, read_instance_id, is_parallel_read, read_number, book_id, title, author, series_name, series_number, cached_tags, publisher, author_name

### View: `publisher_analytics`

**Purpose:** Publisher-level reading analytics including both community and personal ratings.

**Columns:** publisher_id, publisher_name, parent_publisher_id, books_read, total_sessions, total_ebook_minutes, total_audio_minutes, avg_hardcover_rating, avg_user_rating

### View: `author_analytics`

**Purpose:** Author-level analytics with diversity metrics.

**Columns:** author_id, author_name, born_year, is_bipoc, is_lgbtq, books_read, total_sessions, total_ebook_minutes, total_audio_minutes, avg_hardcover_rating, avg_user_rating

### View: `tandem_reading_sessions`

**Purpose:** Analyze overlapping reads with overlap-aware duration calculations.

**Columns:** read_instance_id, book_id, session_count, distinct_media_types, instance_start, instance_end, media_types_combined, total_duration_all_formats, overlap_aware_duration

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
- **book_id:** Primary join key for dimensional analytics
- **start_time:** Time-range queries (month/year aggregations)
- **device:** Device-specific reading patterns
- **media_type:** Partition ebook vs. audiobook queries
- **read_instance_id:** Tandem reading analysis
- **Composite indexes:** book_date, date_device for common patterns

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

See `SCHEMA-CHANGES-SUMMARY.md` for complete list of changes from v1.0.
See `ETL-MAPPING-GUIDE.md` for data transformation procedures.
