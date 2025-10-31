# Schema Changes Summary - Story 1.4 Update
**Date:** 2025-10-31
**Status:** All changes implemented

---

## Overview
Complete schema redesign addressing multi-format reading, physical library tracking, author management, and tandem reading support.

---

## SCHEMA CHANGES IMPLEMENTED

### 1. **New `authors` Table**
- **Purpose:** Separate author dimension (moved from books table)
- **Key Columns:**
  - `author_id` (PK)
  - `author_name` (primary name)
  - `alternate_names` (pen names/pseudonyms)
  - `author_hardcover_id` (Hardcover API reference)
  - `books_count`, `born_year`
  - `is_bipoc`, `is_lgbtq`
  - `identifiers` (JSONB for VIAF, Wikidata)
- **Source:** Hardcover API

### 2. **Publisher Table Renames**
- `canonical_name` → `publisher_name`
- `hardcover_publisher_id` → `publisher_hardcover_id`
- **Why:** Clearer naming convention

### 3. **Books Table Reorganization**
Reorganized from tier-based to category-based structure:

#### Category: CORE IDENTIFICATION
- `title`, `author`, `author_id` (FK to authors table)

#### Category: ISBN / ASIN / IDENTIFIERS
- `isbn_13`, `isbn_10`, `asin`, `hardcover_book_id`

#### Category: PUBLISHER & SERIES
- `publisher_id`, `publisher_name`
- **NEW:** `series_name` (VARCHAR, separate from series_number)
- **NEW:** `series_number` (NUMERIC(5,2) to support "2.5", "Prequel")

#### Category: BOOK DEMOGRAPHICS & METADATA
- `page_count`
- **NEW:** `audio_seconds` (from Hardcover, total audiobook duration)
- `language`, `published_date`, `description`

#### Category: RATINGS & REVIEWS
- **RENAMED:** `rating` → `hardcover_rating`
- **NEW:** `hardcover_rating_count`
- **NEW:** `user_rating` (your personal rating)
- **NEW:** `user_rating_date` (when you rated it)

#### Category: AUTHOR METRICS
- `author_hardcover_id`, `is_bipoc`, `is_lgbtq`, `author_birth_year`, `author_books_count`

#### Category: GENRE & CONTENT
- `cached_tags` (JSONB), `users_read_count`, `users_count`

#### Category: KOREADER & SOURCE DATA
- `file_hash`, `notes`, `highlights`, `source`, `device_stats_source`

#### Category: COVER & DISPLAY
- `cover_url`

#### Category: MULTI-FORMAT OWNERSHIP TRACKING
- **NEW:** `media_types_owned` (TEXT[]) - ["ebook", "audiobook"]
- **NEW:** `owned_physical_formats` (TEXT[]) - ["hardcover", "paperback", "special-edition"]
- **NEW:** `owned_special_editions` (TEXT[]) - Edition detail array

#### Category: READ TRACKING
- **NEW:** `read_count` (INT DEFAULT 1) - Number of times read

### 4. **New `book_editions` Table**
- **Purpose:** Track specific physical editions owned
- **Columns:**
  - `edition_id` (PK)
  - `book_id` (FK)
  - `edition_format` (hardcover, paperback, special-edition, signed, limited)
  - `edition_name` (Anniversary Edition, Premium Edition, etc.)
  - `publication_year`
  - `publisher_specific`
  - `isbn_specific`
  - `condition` (new, like-new, good, fair, poor)
  - `date_acquired`, `display_location`
- **Source:** User tracking

### 5. **Reading Sessions Table Changes**

#### Category: CORE READING FACTS
- `book_id`, `start_time`, `duration_minutes`, `device`

#### Category: READING FORMAT DETAILS
- `media_type`, `pages_read`

#### Category: TANDEM READING SUPPORT
- **NEW:** `read_instance_id` (UUID) - Groups tandem reads (same book, overlapping times, different formats)
- **NEW:** `is_parallel_read` (BOOLEAN) - Flag for tandem session pairs

#### Category: SESSION TRACKING
- **NEW:** `read_number` (INT) - Which read of the book (1=first, 2=reread)
- `end_time`

#### Category: DATA PROVENANCE
- `data_source` (koreader, bookplayer, kindle, audible)
- `device_stats_source`

### 6. **New Views**

#### View: `book_stats` (ENHANCED)
- Added: `read_count` (COUNT DISTINCT read_instance_id)
- Added: `avg_reading_speed_pages_per_minute` (pages read ÷ minutes, for ebook only)
- **Source:** Computed from reading_sessions

#### View: `reading_timeline` (ENHANCED)
- Added: `series_name`, `series_number`
- Added: `read_instance_id`, `is_parallel_read`, `read_number`
- Added: `author_name` join from authors table
- Changed: `canonical_name` → `publisher_name`

#### View: `publisher_analytics` (ENHANCED)
- Added: `avg_user_rating`
- Changed: `canonical_name` → `publisher_name`

#### View: **NEW** `author_analytics`
- Author-level analytics with diversity metrics
- Shows author birth year, BIPOC/LGBTQ flags
- Aggregates reading patterns by author

#### View: **NEW** `tandem_reading_sessions`
- Analyzes overlapping reads (tandem sessions)
- Shows overlap-aware duration calculations
- Distinguishes from raw session sum

---

## TANDEM READING IMPLEMENTATION

### How It Works
```
Session A: "Mate" (audio), 9:00-10:00 → read_instance_id: xyz-789, is_parallel_read: true
Session B: "Mate" (ebook), 8:45-10:15 → read_instance_id: xyz-789, is_parallel_read: true

Both sessions linked via same read_instance_id and is_parallel_read=true
```

### Query Examples
```sql
-- Find tandem reads for a book
SELECT * FROM tandem_reading_sessions
WHERE book_id = 1;

-- Overlap-aware duration (treats overlapping time once)
SELECT book_id, read_instance_id, overlap_aware_duration
FROM tandem_reading_sessions;

-- Raw session sum (may double-count overlapping time)
SELECT book_id, read_instance_id, total_duration_all_formats
FROM tandem_reading_sessions;
```

---

## RE-READ TRACKING IMPLEMENTATION

### How It Works
- `books.read_count`: Total number of distinct read instances
- `reading_sessions.read_instance_id`: UUID grouping each read instance
- `reading_sessions.read_number`: Ordinal number of read (1, 2, 3...)

```sql
-- Count re-reads
SELECT COUNT(DISTINCT read_instance_id) as read_count
FROM reading_sessions
WHERE book_id = X;
```

---

## DATA SOURCE TRACKING

Every column now includes source documentation in COMMENT ON COLUMN:

### Sources Used:
- **KOReader:** statistics.sqlite3 (page_stat_data, book)
- **Hardcover API:** Direct API calls (book metadata, publisher, author)
- **User Input:** Direct entry (ratings, physical library)
- **Computed:** Derived from other fields (read_instance_id, read_count)
- **ETL:** Set during import process (data_source)

Example:
```sql
COMMENT ON COLUMN books.user_rating IS
  'Your personal rating of the book. Source: Hardcover API (user activities).';
```

---

## INDEXES ADDED

### books table:
- `idx_books_asin` (new)
- `idx_books_author_id` (new)

### reading_sessions table:
- `idx_reading_sessions_read_instance` (new) - For tandem read grouping

### book_editions table:
- `idx_book_editions_book_id`
- `idx_book_editions_format`

---

## BACKWARD COMPATIBILITY

**Breaking Changes:**
- Removed direct author fields from books (now use `author_id` FK)
- Renamed `rating` to `hardcover_rating`
- Renamed publisher column names

**Migration Path (for existing data):**
1. Populate authors table from distinct author records
2. Update books.author_id to reference new authors table
3. Rename `rating` column or copy to `hardcover_rating`

---

## WHAT EACH CHANGE ADDRESSES

| Change | Addresses | Benefit |
|--------|-----------|---------|
| Separate authors table | Centralized author data | Author-level analytics, author diversity tracking |
| Separate series columns | Series tracking | Query books by series position |
| audio_seconds field | Audiobook duration tracking | Analytics on audiobook listening patterns |
| hardcover_rating vs user_rating | Rating clarity | Distinguish community vs. personal ratings |
| Edition tracking | Physical library | Document owned copies, special editions, conditions |
| media_types_owned | Format ownership | Understand multi-format library composition |
| read_instance_id | Tandem reading | Handle parallel ebook+audiobook reads |
| is_parallel_read | Tandem reading | Flag overlapping reads for special handling |
| read_count | Re-reads | Track how many times book was read |
| avg_reading_speed | Reading speed analytics | Measure reading velocity per book |

---

## DOCUMENTATION STATUS

| Document | Status | Notes |
|----------|--------|-------|
| create_schema.sql | ✅ COMPLETE | All tables, columns, indexes, views, comments |
| SCHEMA-DOCUMENTATION.md | 📝 IN PROGRESS | Requires comprehensive rewrite for new structure |
| ETL-MAPPING-GUIDE.md | 📝 IN PROGRESS | Update data source mappings for all fields |
| test_schema_operations.py | ✅ READY | Can run after schema created |

---

## NEXT STEPS

1. Execute `create_schema.sql` on Neon.tech
2. Update SCHEMA-DOCUMENTATION.md with:
   - New authors table documentation
   - Reorganized books table by category
   - book_editions table documentation
   - Enhanced reading_sessions with tandem support
   - New author_analytics and tandem_reading_sessions views
3. Update ETL-MAPPING-GUIDE.md with:
   - Data source column for every field
   - Author extraction from Hardcover API
   - Edition tracking procedures
   - Tandem read detection logic
4. Run test_schema_operations.py
5. Update tech-spec with final schema
