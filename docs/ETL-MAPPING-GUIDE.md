# ETL Mapping Guide - Story 1.4 Schema Implementation
**Database:** Neon.tech PostgreSQL v17
**Date:** 2025-10-31 (Updated from 2025-10-30)
**Status:** Implementation reference for Story 3.2 and future stories

---

## Overview

This document provides the complete field mapping for ETL pipelines that populate the unified database schema. It shows how to transform data from each source (KOReader, Hardcover API, historical imports) into the canonical Neon.tech schema.

**Data Source Tracking:** Every field mapping includes a "Source" column indicating where data originates (KOReader, Hardcover API, User tracking, Computed, ETL).

---

## Source 0: Hardcover API Author Extraction

### Purpose
Populate the new `authors` table with author metadata before importing books.

### Table: Hardcover API `author` → `authors` (Neon)

| Hardcover Field | Neon Field | Type | Source | Transform | Notes |
|---|---|---|---|---|---|
| `author.id` | `author_hardcover_id` | VARCHAR(100) | Hardcover API | 1:1 copy | Unique author identifier |
| `author.name` | `author_name` | VARCHAR(255) | Hardcover API | 1:1 copy | Primary author name |
| `author.alternate_names` | `alternate_names` | TEXT[] | Hardcover API | 1:1 copy | Array of pen names |
| `author.slug` | `author_slug` | VARCHAR(255) | Hardcover API | 1:1 copy | URL-friendly identifier |
| `author.books_count` | `books_count` | INT | Hardcover API | 1:1 copy | Total published works |
| `author.born_year` | `born_year` | INT | Hardcover API | 1:1 copy | Birth year |
| `author.is_bipoc` | `is_bipoc` | BOOLEAN | Hardcover API | 1:1 copy | BIPOC diversity flag |
| `author.is_lgbtq` | `is_lgbtq` | BOOLEAN | Hardcover API | 1:1 copy | LGBTQ+ diversity flag |
| `author.identifiers` | `identifiers` | JSONB | Hardcover API | 1:1 copy | VIAF, Wikidata IDs |
| — | `created_at` | TIMESTAMP | Computed | CURRENT_TIMESTAMP | Record insertion time |

### Example Insert:
```sql
INSERT INTO authors (author_name, author_hardcover_id, alternate_names, born_year, is_bipoc, is_lgbtq)
VALUES ('Ali Hazelwood', 'author_123', ARRAY['Ali Hazelwood'], 1986, true, false);
```

---

## Source 1: KOReader statistics.sqlite3 (Story 3.2 - Main)

### Database Location
- **Path:** `~/.config/koreader/statistics/statistics.sqlite3`
- **Backup Location:** (via Syncthing) Raspberry Pi → `/backups/koreader/statistics.sqlite3`
- **Tables:** `book`, `page_stat_data`
- **Records:** 9 books, ~2,734 reading sessions

### Table: `book` (KOReader) → `books` (Neon)

| KOReader Field | Neon Field | Type | Source | Transform | Notes |
|---|---|---|---|---|---|
| `id` | `book_id` | INT | KOReader | 1:1 copy | Primary key for book reference |
| `title` | `title` | VARCHAR(255) | KOReader | 1:1 copy | Required; displayed in UI |
| `authors` | `author` | VARCHAR(255) | KOReader | 1:1 copy | comma-separated if multiple |
| `pages` | `page_count` | INT | KOReader | 1:1 copy | Total page count of book |
| `series` | `series_name` | VARCHAR(255) | KOReader | Split field | Extract name (e.g., "Hani Khan" from "Hani Khan #2") |
| — | `series_number` | NUMERIC(5,2) | KOReader | Extract/Parse | Extract number (e.g., 2 from "Hani Khan #2") |
| `language` | `language` | CHAR(2) | KOReader | 1:1 copy | ISO 639-1 code (en, es, fr, etc.) |
| `md5` | `file_hash` | VARCHAR(32) | KOReader | 1:1 copy | Deduplication identifier |
| `notes` | `notes` | INT | KOReader | 1:1 copy | Annotation count |
| `highlights` | `highlights` | INT | KOReader | 1:1 copy | Highlight count |
| — | `source` | VARCHAR(50) | ETL | Constant | Set to 'koreader' |
| — | `media_type` | VARCHAR(20) | ETL | Constant | Set to 'ebook' |
| — | `device_stats_source` | VARCHAR(100) | ETL | Constant | Set to 'statistics.sqlite3' |
| — | `created_at` | TIMESTAMP | Computed | CURRENT_TIMESTAMP | Record insertion time |

**Fields NOT imported (computed via views):**
- `last_open`: Available as MAX(reading_sessions.start_time)
- `total_read_time`: Available as SUM(reading_sessions.duration_minutes)
- `total_read_pages`: Available as SUM(reading_sessions.pages_read)

**Hardcover enrichment (separate ETL step via Story 3.2):**
- `isbn_13`: Fetch via Hardcover API title+author match
- `publisher_id`: Lookup via publisher consolidation table
- `rating`: Hardcover book rating
- `cached_tags`: Hardcover genre/topic tags
- All TIER 2/3/4 fields

### Table: `page_stat_data` (KOReader) → `reading_sessions` (Neon)

**Strategy:** Aggregate consecutive page_stat_data rows into logical reading sessions.

**Session Definition:** Time gap > 30 minutes = new session

| KOReader Field | Neon Field | Type | Transform | Notes |
|---|---|---|---|---|
| `id_book` | `book_id` | INT | 1:1 copy | Foreign key to books |
| `start_time` | `start_time` | TIMESTAMP | FROM_UNIXTIME(start_time) | Convert Unix → TIMESTAMP |
| `duration` | `duration_minutes` | INT | 1:1 copy | Minutes of reading in session |
| `page` | `pages_read` | INT | 1:1 copy (session max) | Aggregate pages: MAX(page) per session |
| — | `device` | VARCHAR(50) | Constant | Set to 'boox-palma-2' (inferred from source) |
| — | `media_type` | VARCHAR(20) | Constant | Set to 'ebook' |
| — | `device_stats_source` | VARCHAR(100) | Constant | Set to 'statistics.sqlite3' |
| — | `data_source` | VARCHAR(50) | Constant | Set to 'koreader' |
| — | `created_at` | TIMESTAMP | CURRENT_TIMESTAMP | Record insertion time |

**Python Pseudocode for Session Aggregation:**

```python
def aggregate_sessions(page_stat_data, session_gap_minutes=30):
    """
    Aggregate consecutive page_stat_data rows into reading sessions.

    Args:
        page_stat_data: List of records from KOReader database
        session_gap_minutes: Time gap threshold for new session

    Returns:
        List of reading_sessions records
    """
    sessions = []
    current_session = None

    for record in sorted(page_stat_data, key=lambda x: x['start_time']):
        if current_session is None:
            # Start new session
            current_session = {
                'book_id': record['id_book'],
                'start_time': record['start_time'],
                'duration_minutes': record['duration'],
                'pages_read': record['page'],
                'session_start_time': record['start_time']
            }
        else:
            # Check if we should continue current session or start new one
            time_gap = (record['start_time'] - current_session['session_start_time']) / 60

            if time_gap > session_gap_minutes:
                # Gap exceeds threshold - save current session and start new one
                sessions.append(current_session)
                current_session = {
                    'book_id': record['id_book'],
                    'start_time': record['start_time'],
                    'duration_minutes': record['duration'],
                    'pages_read': record['page'],
                    'session_start_time': record['start_time']
                }
            else:
                # Continue current session - accumulate duration
                current_session['duration_minutes'] += record['duration']
                current_session['pages_read'] = record['page']  # Track max page

    # Don't forget final session
    if current_session:
        sessions.append(current_session)

    return sessions
```

**Deduplication Strategy:**

Use UNIQUE constraint on (book_id, start_time, device):
```sql
INSERT INTO reading_sessions (book_id, start_time, duration_minutes, pages_read, device, ...)
VALUES (...)
ON CONFLICT (book_id, start_time, device) DO NOTHING;  -- Skip if exists
```

---

## Source 2: Hardcover API (Story 3.2 + Story 4.2)

### API Endpoints

**Authentication:** Bearer token (free tier, obtain from hardcover.app)

**GraphQL Endpoint:** `https://api.hardcover.app/graphql`

### Query: Fetch Book Metadata for Enrichment

**Use Case:** Match KOReader books to Hardcover and fetch metadata

```graphql
query SearchBook($query: String!) {
  bookSearch(query: $query, first: 5) {
    edges {
      node {
        id
        title
        isbn13
        isbn10
        description
        rating
        ratingCount: rating_count
        usersReadCount: users_read_count
        usersCount: users_count
        listCount: lists_count
        releaseDate: release_date
        releaseYear: release_year
        language
        cachedTags: cached_tags
        editions(first: 1) {
          edges {
            node {
              id
              isbn13
              publisher {
                id
                name
                slug
              }
              imageId: image_id
              description
              physicalFormat: physical_format
              releaseDate: release_date
              usersReadCount: users_read_count
            }
          }
        }
        contributors(first: 10) {
          edges {
            node {
              author {
                id
                name
                bio
                birthDate: birth_date
                deathDate: death_date
                isBipoc: is_bipoc
                isLgbtq: is_lgbtq
                booksCount: books_count
              }
              role
            }
          }
        }
      }
    }
  }
}
```

### KOReader → Hardcover Matching Logic

**Step 1: Exact ISBN match (highest confidence)**
```sql
SELECT hc_book_id FROM hardcover_cache
WHERE isbn_13 = ? OR isbn_10 = ?
LIMIT 1;
```

**Step 2: Title + Author fuzzy match (if no ISBN)**
```python
# Use fuzzy string matching (e.g., Levenshtein distance)
# Match KOReader title/author to Hardcover book
from fuzzywuzzy import fuzz

def find_hardcover_match(koreader_title, koreader_author, candidates):
    """
    Find best Hardcover match for KOReader book.

    Scoring:
    - Title match: 70% weight
    - Author match: 30% weight
    """
    best_match = None
    best_score = 0

    for candidate in candidates:
        title_score = fuzz.ratio(koreader_title.lower(), candidate['title'].lower())
        author_score = fuzz.ratio(koreader_author.lower(), candidate['author'].lower())

        combined_score = (title_score * 0.7) + (author_score * 0.3)

        if combined_score > best_score and combined_score >= 80:  # 80% confidence threshold
            best_score = combined_score
            best_match = candidate

    return best_match
```

### Neon `books` Table Enrichment Mapping

| Hardcover Field | Neon Field | Type | Source | Notes |
|---|---|---|---|---|
| `book.id` | `hardcover_book_id` | VARCHAR(100) | API | For future direct Hardcover queries (H1) |
| `edition.isbn13` | `isbn_13` | VARCHAR(20) | API | ISBN for cross-service linking |
| `publisher.id` | `publisher_id` | INT | API→publishers table | Lookup publisher ID from consolidation |
| `edition.description` | `description` | TEXT | API | Book summary |
| `book.rating` | `rating` | DECIMAL(3,2) | API | 0-5 scale |
| `book.rating_count` | `rating_count` | INT | API | Number of ratings |
| `book.cached_tags` | `cached_tags` | JSONB | API | Genre/topic array |
| `edition.image_id` | `cover_url` | TEXT | Transform | Construct CDN URL |
| `edition.release_date` | `published_date` | DATE | API | Publication date |
| `book.users_read_count` | `users_read_count` | INT | API | Hardcover users who read |
| `edition.users_count` | `users_count` | INT | API | Hardcover users who own |
| `author.id` | `author_id` | VARCHAR(100) | API | Author ID for analytics (A1) |
| `author.born_year` | `birth_year` | INT | API | Author birth year (A4) |
| `author.books_count` | `author_books_count` | INT | API | Author's prolific count (A7) |
| `author.is_bipoc` | `is_bipoc` | BOOLEAN | API | Author diversity flag |
| `author.is_lgbtq` | `is_lgbtq` | BOOLEAN | API | Author LGBTQ+ flag |

**Cover URL Construction:**
```python
def build_cover_url(image_id):
    """Construct Hardcover CDN URL from image ID"""
    return f"https://images.hardcover.app/{image_id}/medium.jpg"
```

---

## Source 3: Hardcover API Audiobook History (Story 4.2)

### Query: Fetch User's Audiobook Reading History

```graphql
query UserAudiobookHistory($userId: ID!) {
  user(id: $userId) {
    readingStatuses(mediaType: AUDIOBOOK) {
      edges {
        node {
          id
          status  # "READING", "COMPLETED", etc.
          startedAt: started_at
          finishedAt: finished_at
          book {
            id
            title
            isbn13
            edition {
              audioSeconds: audio_seconds
            }
            authors {
              edges {
                node {
                  name
                }
              }
            }
          }
        }
      }
    }
  }
}
```

### Audiobook Session Mapping

| Hardcover Field | Neon Field | Transform | Notes |
|---|---|---|---|
| `readingStatus.book.id` | `book_id` | Lookup in books table | Match via ISBN or title |
| `readingStatus.startedAt` | `start_time` | 1:1 copy | Session start |
| `readingStatus.finishedAt` | `end_time` | 1:1 copy | Session end |
| (calculated) | `duration_minutes` | (finishedAt - startedAt) / 60 | Computed |
| — | `media_type` | Constant 'audiobook' | Media type identifier |
| — | `device` | Variable | Depends on BookPlayer device |
| — | `pages_read` | NULL | Not applicable for audiobooks |
| — | `data_source` | Constant 'hardcover' | Audiobook source identifier |

---

## Source 4: Kindle Historical Data (Story 5.2)

### Data Export Format
- **Source:** Amazon account → Kindle reading history export
- **Format:** CSV or JSON (varies by export method)
- **Fields:** Title, Author, Progress (%), Date Started, Date Finished

### CSV Parsing Example

```python
import csv
from datetime import datetime

def parse_kindle_export(csv_file):
    """Parse Kindle reading history CSV"""
    sessions = []

    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Map Kindle export to reading_sessions
            session = {
                'title': row.get('Title'),
                'author': row.get('Author'),
                'start_time': datetime.strptime(row.get('Date Started'), '%Y-%m-%d'),
                'end_time': datetime.strptime(row.get('Date Finished'), '%Y-%m-%d'),
                'progress': float(row.get('Progress %', '0')),
                'source': 'kindle',
                'media_type': 'ebook'
            }
            sessions.append(session)

    return sessions
```

### Kindle → Neon Mapping

| Kindle Export | Neon Field | Notes |
|---|---|---|
| Title | books.title | Match to existing book |
| Author | books.author | Fuzzy match logic |
| Date Started | reading_sessions.start_time | UTC conversion |
| Date Finished | reading_sessions.end_time | UTC conversion |
| (calculated) | reading_sessions.duration_minutes | end_time - start_time |
| Progress % | Estimate pages_read | progress * books.page_count |
| — | reading_sessions.media_type | Set to 'ebook' |
| — | reading_sessions.data_source | Set to 'kindle' |
| — | reading_sessions.device | Inferred: 'kindle-device' or similar |

---

## Source 5: Audible Historical Data (Story 5.3)

### Data Export
- **Source:** Audible account → Download listening history
- **Format:** CSV or Audible API
- **Fields:** Title, Author, Narrator, Date Added, Progress

### CSV Parsing

```python
def parse_audible_export(csv_file):
    """Parse Audible listening history CSV"""
    sessions = []

    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            session = {
                'title': row.get('Title'),
                'author': row.get('Author'),
                'narrator': row.get('Narrator'),
                'start_time': datetime.strptime(row.get('Date Added'), '%Y-%m-%d'),
                'progress': float(row.get('Progress %', '0')),
                'source': 'audible',
                'media_type': 'audiobook'
            }
            sessions.append(session)

    return sessions
```

### Audible → Neon Mapping

| Audible Field | Neon Field | Notes |
|---|---|---|
| Title | books.title | Match to existing book |
| Author | books.author | Fuzzy match |
| Narrator | (future) | Store in extended schema (Epic 4) |
| ASIN | books.asin | Cross-reference for linking |
| Date Added | reading_sessions.start_time | Session start |
| Progress % | Estimate duration | progress * books.duration_minutes (from Hardcover) |
| — | reading_sessions.media_type | Set to 'audiobook' |
| — | reading_sessions.data_source | Set to 'audible' |
| — | reading_sessions.device | Inferred: 'audible-app' |

---

## Publisher Consolidation (P1, P3, P4)

### Strategy: Handle Duplicate Publisher Names

**Step 1: Fetch from Hardcover API**
```graphql
query {
  publisher(id: $publisherId) {
    id
    name
    slug
    canonicalId: canonical_id
    parentId: parent_id
  }
}
```

**Step 2: Consolidation Logic**
```python
def consolidate_publishers(hardcover_publisher):
    """
    Consolidate publishers in Neon table.

    - If canonical_id exists: point to canonical record
    - If parent_id exists: link as imprint
    - Otherwise: create new canonical record
    """

    # Check if already consolidated
    existing = query_publishers(
        hardcover_publisher_id=hardcover_publisher['id']
    )

    if existing and existing['canonical_hardcover_id']:
        # Already consolidated - skip
        return existing

    # Check if this is a duplicate of another
    canonical = find_canonical_publisher(
        hardcover_publisher['canonical_id']
    )

    if canonical:
        # This is a duplicate - point to canonical
        return {
            'hardcover_publisher_id': hardcover_publisher['id'],
            'canonical_hardcover_id': canonical['publisher_id'],
            'alternate_names': [...hardcover_publisher['name']]
        }
    else:
        # This is the canonical - create new record
        return {
            'canonical_name': hardcover_publisher['name'],
            'hardcover_publisher_id': hardcover_publisher['id'],
            'parent_publisher_id': find_parent_publisher(
                hardcover_publisher['parent_id']
            )
        }
```

### Database Inserts

```sql
-- Insert canonical publisher
INSERT INTO publishers (
  canonical_name,
  hardcover_publisher_id,
  alternate_names
) VALUES (
  'Penguin Books',
  123,
  ARRAY['Penguin', 'Penguin Publishing', 'Penguin Random House']
);

-- Insert duplicate pointing to canonical
INSERT INTO publishers (
  canonical_name,
  hardcover_publisher_id,
  canonical_hardcover_id,
  alternate_names
) VALUES (
  'Penguin Publishing',
  456,
  123,  -- Points to canonical
  ARRAY['Penguin Publishing Group']
);

-- Insert imprint with parent reference
INSERT INTO publishers (
  canonical_name,
  hardcover_publisher_id,
  parent_publisher_id
) VALUES (
  'Berkley',
  789,
  123  -- Parent is Penguin Books
);
```

---

## ETL Execution Order & Dependencies

### Phase 1: Initial Schema Setup
1. Create `publishers` table
2. Create `books` table
3. Create `reading_sessions` table
4. Create views: `book_stats`, `reading_timeline`, `publisher_analytics`

### Phase 2: KOReader Import (Story 3.2)
1. Import `book` table → `books` (Neon)
2. Aggregate `page_stat_data` → `reading_sessions` (Neon)
3. Enrich via Hardcover API:
   - Fetch book metadata
   - Consolidate publishers
   - Update books table with TIER 2/3 fields

### Phase 3: Publisher Consolidation
1. Load all publishers from Hardcover API
2. Detect duplicates (canonical_id)
3. Create publisher records with hierarchy

### Phase 4: Audiobook Integration (Story 4.2)
1. Query user's audiobook history from Hardcover API
2. Match audiobooks to existing books
3. Insert `reading_sessions` with `media_type = 'audiobook'`

### Phase 5: Historical Imports (Story 5.2, 5.3)
1. Parse Kindle export → create `reading_sessions`
2. Parse Audible export → create `reading_sessions`
3. Validate no duplicates via UNIQUE constraint

---

## Validation & Testing

### Unit Tests (Per Source)

**Test KOReader Import:**
```python
def test_koreader_import():
    # Arrange
    koreader_db = sqlite3.connect('statistics.sqlite3')
    cursor = koreader_db.cursor()
    cursor.execute('SELECT * FROM book LIMIT 1')
    book = cursor.fetchone()

    # Act
    neon_record = transform_koreader_book(book)

    # Assert
    assert neon_record['title'] == book['title']
    assert neon_record['source'] == 'koreader'
    assert neon_record['media_type'] == 'ebook'
```

**Test Session Aggregation:**
```python
def test_session_aggregation():
    # Arrange
    page_stats = [
        {'start_time': 1000, 'duration': 30, 'page': 10},
        {'start_time': 1050, 'duration': 25, 'page': 15},  # 50 sec gap - same session
        {'start_time': 3000, 'duration': 45, 'page': 50},  # 30+ min gap - new session
    ]

    # Act
    sessions = aggregate_sessions(page_stats, session_gap_minutes=30)

    # Assert
    assert len(sessions) == 2
    assert sessions[0]['duration_minutes'] == 55
    assert sessions[0]['pages_read'] == 15
```

### Integration Tests

**Test Hardcover Enrichment:**
```python
def test_hardcover_enrichment():
    # Arrange
    book_title = 'Mate'
    book_author = 'Ali Hazelwood'

    # Act
    hc_data = fetch_hardcover_metadata(book_title, book_author)
    neon_record = enrich_book(book_id=1, hc_data=hc_data)

    # Assert
    assert neon_record['isbn_13'] is not None
    assert neon_record['rating'] > 0
    assert len(neon_record['cached_tags']) > 0
```

### End-to-End Validation

**Check for consistency:**
```sql
-- Verify no orphaned sessions
SELECT COUNT(*) FROM reading_sessions rs
WHERE NOT EXISTS (SELECT 1 FROM books b WHERE b.book_id = rs.book_id);

-- Should return 0

-- Verify no duplicates
SELECT book_id, start_time, device, COUNT(*) as count
FROM reading_sessions
GROUP BY book_id, start_time, device
HAVING COUNT(*) > 1;

-- Should return no rows
```

---

## Performance Optimization Tips

1. **Batch inserts:** Use COPY or multi-value INSERT for large volumes
2. **Disable triggers:** Temporarily disable constraints during bulk import
3. **Deferred constraint checking:** Use DEFERRABLE constraints
4. **VACUUM ANALYZE:** Run after bulk imports to optimize indexes

```sql
-- Batch insert with explicit values
COPY reading_sessions (book_id, start_time, duration_minutes, pages_read, device, created_at)
FROM STDIN WITH (FORMAT csv);

-- Vacuum to optimize indexes
VACUUM ANALYZE reading_sessions;
```

---

## Advanced ETL Procedures: Tandem Reading Detection

### Definition
Tandem reading occurs when the same book is read in multiple formats simultaneously (e.g., ebook + audiobook), with overlapping time periods of 7+ days.

### ETL Detection Algorithm

**Input:** All reading_sessions for a single book_id, sorted by start_time

**Process:**
```python
def detect_tandem_reads(sessions_for_book):
    """
    Identify and flag tandem reads within a book's reading history.

    Returns: List of read_instance_id assignments
    """
    reads = []
    current_read_sessions = []
    min_overlap_days = 7

    for session in sorted(sessions_for_book, key=lambda s: s['start_time']):
        # Check if this session overlaps with existing sessions
        overlapping = []
        for existing in current_read_sessions:
            overlap_start = max(session['start_time'], existing['start_time'])
            overlap_end = min(session['end_time'], existing['end_time'])
            overlap_days = (overlap_end - overlap_start).days

            if overlap_days >= min_overlap_days:
                overlapping.append(existing)

        if overlapping:
            # Session overlaps with existing ones → tandem read
            read_instance_id = overlapping[0]['read_instance_id']  # Use first group's ID
            session['read_instance_id'] = read_instance_id
            session['is_parallel_read'] = True
            current_read_sessions.append(session)
        else:
            # No overlap → new read instance
            read_instance_id = uuid.uuid4()
            session['read_instance_id'] = read_instance_id
            session['is_parallel_read'] = False
            reads.append(current_read_sessions)
            current_read_sessions = [session]

    if current_read_sessions:
        reads.append(current_read_sessions)

    return reads
```

### SQL Implementation for ETL

```sql
-- Step 1: Identify all tandem read pairs (requires manual review/approval)
WITH tandem_pairs AS (
  SELECT
    rs1.session_id as session_1,
    rs2.session_id as session_2,
    rs1.media_type as format_1,
    rs2.media_type as format_2,
    (GREATEST(rs1.start_time, rs2.start_time)::date -
     LEAST(rs1.end_time, rs2.end_time)::date) as overlap_days
  FROM reading_sessions rs1
  JOIN reading_sessions rs2 ON
    rs1.book_id = rs2.book_id AND
    rs1.session_id < rs2.session_id AND
    rs1.media_type != rs2.media_type
  WHERE
    rs1.start_time <= rs2.end_time AND
    rs2.start_time <= rs1.end_time AND
    GREATEST(rs1.start_time, rs2.start_time)::date -
    LEAST(rs1.end_time, rs2.end_time)::date >= 7
)
SELECT * FROM tandem_pairs;

-- Step 2: Assign read_instance_id to tandem pairs
WITH tandem_groups AS (
  SELECT
    rs1.book_id,
    array_agg(DISTINCT rs1.session_id) as session_group,
    gen_random_uuid() as read_instance_id
  FROM reading_sessions rs1
  WHERE rs1.book_id IN (SELECT DISTINCT book_id FROM tandem_pairs)
  GROUP BY rs1.book_id
)
UPDATE reading_sessions
SET
  read_instance_id = tg.read_instance_id,
  is_parallel_read = TRUE
FROM tandem_groups tg
WHERE reading_sessions.book_id = tg.book_id
  AND reading_sessions.session_id = ANY(tg.session_group);
```

### Configuration
- **Overlap Threshold:** 7 days (configurable)
- **Format Requirement:** Must be different media_types (ebook ≠ audiobook)
- **Validation:** Manual review recommended before marking is_parallel_read=TRUE

---

## Advanced ETL Procedures: Re-read Detection & ID Assignment

### Definition
A re-read is identified when multiple distinct temporal blocks of reading_sessions exist for the same book_id.

### ETL Detection Algorithm

**Input:** All reading_sessions for a single book_id, sorted by start_time

**Process:**
```python
def detect_and_assign_re_reads(sessions_for_book):
    """
    Assign read_instance_id and read_number to identify re-reads.

    Logic:
    1. Sort all sessions by start_time
    2. Group sessions with gaps < 30 days as same read
    3. Assign unique UUID per group (read_instance_id)
    4. Assign ordinal number (read_number: 1, 2, 3...)
    """
    reads = []
    current_group = []
    max_gap_days = 30  # Configurable

    sorted_sessions = sorted(sessions_for_book, key=lambda s: s['start_time'])

    for i, session in enumerate(sorted_sessions):
        if current_group:
            last_session = current_group[-1]
            gap_days = (session['start_time'] - last_session['end_time']).days

            if gap_days <= max_gap_days:
                # Same read → add to current group
                current_group.append(session)
            else:
                # New read → start new group
                reads.append(current_group)
                current_group = [session]
        else:
            current_group = [session]

    if current_group:
        reads.append(current_group)

    # Assign read_instance_id and read_number
    results = []
    for read_num, group in enumerate(reads, 1):
        read_instance_id = uuid.uuid4()
        for session in group:
            session['read_instance_id'] = read_instance_id
            session['read_number'] = read_num
            results.append(session)

    return results
```

### SQL Implementation for ETL

```sql
-- Step 1: Identify temporal gaps to find read boundaries
WITH session_gaps AS (
  SELECT
    session_id,
    book_id,
    start_time,
    end_time,
    LAG(end_time) OVER (PARTITION BY book_id ORDER BY start_time) as prev_end_time,
    (start_time::date - LAG(end_time)::date OVER (PARTITION BY book_id ORDER BY start_time)) as gap_days
  FROM reading_sessions
  WHERE book_id = ?  -- Process one book at a time
)
SELECT * FROM session_gaps WHERE gap_days > 30 OR gap_days IS NULL;

-- Step 2: Assign read_instance_id and read_number
WITH read_boundaries AS (
  SELECT
    session_id,
    book_id,
    start_time,
    SUM(CASE WHEN gap_days > 30 OR gap_days IS NULL THEN 1 ELSE 0 END)
      OVER (PARTITION BY book_id ORDER BY start_time) as read_group
  FROM (
    SELECT
      session_id,
      book_id,
      start_time,
      (start_time::date - LAG(end_time)::date OVER (PARTITION BY book_id ORDER BY start_time)) as gap_days
    FROM reading_sessions
  ) grouped
),
read_assignments AS (
  SELECT
    session_id,
    read_group as read_number,
    gen_random_uuid() as read_instance_id
  FROM read_boundaries
)
UPDATE reading_sessions rs
SET
  read_number = ra.read_number,
  read_instance_id = ra.read_instance_id
FROM read_assignments ra
WHERE rs.session_id = ra.session_id;
```

### Configuration
- **Gap Threshold:** 30 days (configurable; if reading gap > 30 days, treat as new read)
- **Initial read_number:** Always starts at 1 for first read
- **read_instance_id:** UUID to group sessions belonging to same read

---

## Advanced ETL Procedures: Edition Tracking

### Definition
Each unique physical book owned is tracked as a `book_editions` record. One book can have multiple editions (hardcover, paperback, special edition).

### ETL Procedures

**When to create a book_editions record:**
1. **ISBN changes** - Different ISBN = different edition
2. **Format changes** - hardcover, paperback, special edition, audiobook (physical)
3. **Publisher changes** - Different publisher = different edition
4. **Special editions** - Anniversary, signed, limited, etc.
5. **User tracking** - Physical library curation (you own multiple copies)

### Edition Detection & Population

```python
def process_physical_editions(book_record, user_library):
    """
    Extract edition information from user's physical library
    and populate book_editions table.
    """
    editions = []

    for owned_copy in user_library.get(book_record['book_id'], []):
        edition = {
            'book_id': book_record['book_id'],
            'edition_format': owned_copy['format'],  # hardcover, paperback, special
            'edition_name': owned_copy.get('edition_name', None),  # Anniversary, Signed, etc.
            'publication_year': owned_copy.get('publication_year', None),
            'isbn_specific': owned_copy.get('isbn', None),
            'condition': owned_copy.get('condition', 'unknown'),  # new, like-new, good, fair, poor
            'date_acquired': owned_copy.get('date_acquired', None),
            'display_location': owned_copy.get('shelf_location', None),  # "Bedroom shelf A3"
        }
        editions.append(edition)

    return editions
```

### SQL Implementation

```sql
-- Insert new editions for a book (with deduplication)
INSERT INTO book_editions (book_id, edition_format, edition_name, isbn_specific, condition)
VALUES (?, ?, ?, ?, ?)
ON CONFLICT (book_id, isbn_specific, edition_format) DO UPDATE
SET edition_name = EXCLUDED.edition_name, condition = EXCLUDED.condition;

-- Query: Show all owned editions of a book
SELECT
  b.title,
  be.edition_format,
  be.edition_name,
  be.isbn_specific,
  be.condition,
  be.display_location
FROM books b
JOIN book_editions be ON b.book_id = be.book_id
WHERE b.title = 'Dune'
ORDER BY be.date_acquired DESC;
```

### Example: Multi-Edition Book

**Book:** "The Lord of the Rings" by J.R.R. Tolkien

| Edition | Format | Publisher | ISBN | Condition | Acquired | Notes |
|---------|--------|-----------|------|-----------|----------|-------|
| 1 | Hardcover | Houghton Mifflin | 978-0544003415 | Good | 2018-05-15 | Original reading copy |
| 2 | Paperback | Penguin | 978-0008322953 | Like-New | 2020-10-20 | Travel copy |
| 3 | Special Edition | Harper Voyager | 978-0062415639 | New | 2024-12-01 | Collectible edition |

**Corresponding book_editions records:**
```sql
INSERT INTO book_editions (book_id, edition_format, publisher_specific, isbn_specific, condition, date_acquired)
VALUES
  (1, 'hardcover', 'Houghton Mifflin', '978-0544003415', 'good', '2018-05-15'),
  (1, 'paperback', 'Penguin', '978-0008322953', 'like-new', '2020-10-20'),
  (1, 'special-edition', 'Harper Voyager', '978-0062415639', 'new', '2024-12-01');
```

---

## Data Quality & Error Handling

### Validation Rules by Field Type

#### Date Fields
- **Format:** YYYY-MM-DD or TIMESTAMP
- **Constraints:** start_time <= end_time, both <= CURRENT_DATE
- **On Violation:** Log error with session_id, skip record, send alert

#### ISBN Fields
- **Format:** ISBN-10 (10 digits) or ISBN-13 (13 digits)
- **Validation:** Check digit algorithm (mod 11 for ISBN-10, mod 10 for ISBN-13)
- **On Invalid:** Log warning, attempt lookup by title+author, fallback to NULL

#### Page Count
- **Range:** 1 to 9,999 pages
- **On Invalid:** Log warning, skip if 0, estimate if > 10,000
- **On NULL:** Use Hardcover API value if available

#### Numeric Fields (rating, duration_minutes, pages_read)
- **Range:** Rating (0-5), duration (0-10,080), pages (0-9,999)
- **On Violation:** Log error, set to NULL, check data source

### Error Handling Flowchart

```
ETL Pipeline Start
        ↓
Extract from Source → Validate Fields
        ↓
Validation Fails? ──YES→ Log Error
        │                 ↓
        └────── Attempt Recovery/Fallback
                 ↓
Recovery Succeeds? ──YES→ Continue with fixed data
        │
        └─NO─→ Mark Record as SKIPPED, Send Alert
                 ↓
               Continue to Next Record
        ↓
Transform Data ──ERROR→ Log Transform Error, Skip
        ↓
Check Constraints ──VIOLATION→ Log Constraint Error, Rollback
        ↓
Insert to Database
        ↓
Log Success Metrics (rows_inserted, rows_skipped, rows_failed)
        ↓
Pipeline Complete
```

### Error Logging Requirements

```python
# Log format for all ETL errors
{
  'timestamp': ISO 8601,
  'pipeline_id': unique UUID,
  'stage': 'extraction|transformation|validation|load',
  'error_type': 'validation|constraint|api|network',
  'source_record_id': original record identifier,
  'message': human-readable description,
  'severity': 'info|warning|error|critical',
  'action_taken': 'skip|retry|fallback|alert'
}

# Example:
{
  'timestamp': '2025-10-31T14:30:45Z',
  'pipeline_id': 'etl_koreader_20251031',
  'stage': 'validation',
  'error_type': 'validation',
  'source_record_id': 'session_1234',
  'message': 'ISBN "978-00000000000" failed mod-10 check',
  'severity': 'warning',
  'action_taken': 'fallback to title+author lookup'
}
```

### Retry Policies

| Error Type | Retry Count | Backoff | Max Time | Action on Fail |
|-----------|-----------|---------|----------|---|
| **API Timeout** | 3 | Exponential (1s, 2s, 4s) | 10 minutes | Queue for manual review |
| **Network Error** | 5 | Exponential (5s, 10s, 20s) | 1 hour | Pause pipeline, alert ops |
| **Validation Fail** | 0 | — | — | Log & skip |
| **Constraint Violation** | 1 | — | 30 seconds | Rollback & skip |
| **API Rate Limit** | Wait | Exponential backoff | 24 hours | Pause pipeline |

---

## Example ETL Workflows

### Workflow 1: Load Single Reading Session from KOReader

**Input:** One `page_stat_data` row from KOReader history

**Steps:**
```
1. Extract from page_stat_data
   - Extract: id_book, start_time (Unix timestamp), duration
   - Validate: start_time valid, duration > 0

2. Lookup book in books table
   - Query: SELECT book_id FROM books WHERE file_hash = ?
   - Result: book_id = 42

3. Create reading session
   - Transform: duration (minutes), start_time → TIMESTAMP
   - Assign: device='boox-palma-2', media_type='ebook', data_source='koreader'

4. Detect tandem/re-read
   - Check: Any overlapping sessions for this book?
   - If yes: Assign read_instance_id, set is_parallel_read=TRUE
   - If no: Generate new read_instance_id, set is_parallel_read=FALSE

5. Insert to reading_sessions
   - INSERT INTO reading_sessions (...) VALUES (...)
   - Log: "Session 42_001 loaded, 45 minutes, ebook"

6. Update book_stats view
   - View automatically reflects new session
```

### Workflow 2: Batch Import from KOReader History

**Input:** 100+ page_stat_data rows

**Steps:**
```
1. Disable indexes on reading_sessions (performance)
   - ALTER INDEX idx_reading_sessions_* UNUSABLE

2. Batch aggregate sessions
   - Group page_stat_data rows into reading sessions (30-min gap threshold)
   - FOR each session:
       a. Transform to reading_sessions format
       b. Validate fields
       c. Detect tandem/re-read
       d. Prepare INSERT batch (1000 rows)

3. Insert in batches
   - INSERT INTO reading_sessions (...) VALUES (...), (...), ...
   - Commit after each 1000-row batch

4. Rebuild indexes
   - ALTER INDEX idx_reading_sessions_* REBUILD
   - ANALYZE reading_sessions

5. Verify counts
   - SELECT COUNT(*) FROM reading_sessions → expected count
   - Log: "Imported 2,734 sessions in 45 batches"

6. Update book_stats
   - Views automatically refresh
```

### Workflow 3: Detect Tandem Reads (Batch Process)

**Input:** reading_sessions table with preliminary data

**Steps:**
```
1. FOR each book_id with multiple sessions:

2. Retrieve all sessions for book_id
   - SELECT * FROM reading_sessions WHERE book_id = ?

3. Check for overlaps (different formats)
   - Use detection algorithm (see Advanced ETL Procedures)
   - Calculate overlap_days for each pair

4. Filter pairs with overlap >= 7 days
   - Mark both sessions: is_parallel_read=TRUE
   - Assign same read_instance_id (UUID)

5. Manual review step (optional)
   - Output report of detected tandem reads
   - Ask user: "Approve these as tandem reads?"
   - If approved: Commit. If not: Skip

6. Update reading_sessions
   - UPDATE reading_sessions SET is_parallel_read=TRUE, read_instance_id=?
   - Log: "Detected 3 tandem reads (12 sessions affected)"
```

### Workflow 4: Backfill Hardcover Metadata

**Input:** books table (populated from KOReader, missing Hardcover enrichment)

**Steps:**
```
1. FOR each book in books table:

2. Call Hardcover API
   - Query: /search/books?title={title}&author={author}
   - Handle: No match, multiple matches, API errors

3. Evaluate match quality
   - Score: (title_similarity * 0.7) + (author_similarity * 0.3)
   - If score >= 80: Accept match
   - If score < 80: Log as "manual review needed"

4. Extract metadata from API response
   - hardcover_rating, rating_count
   - isbn_13, asin
   - description, cover_url
   - cached_tags (JSON)
   - publisher_name, author details

5. Update books table
   - UPDATE books SET hardcover_rating=?, isbn_13=?, ...
   - WHERE book_id = ?

6. Extract/update authors table
   - Check: Does author exist? (UPSERT)
   - If not: INSERT new author from API response
   - Update books.author_id FK

7. Extract/update publishers table
   - Check: Does publisher exist? (UPSERT)
   - If not: INSERT new publisher
   - Update books.publisher_id FK

8. Log results
   - Count: 9 matched, 0 manual review, 0 failed
   - Duration: 12 seconds
   - Average API time: 1.3s per book
```

### Workflow 5: Handle API Failure & Retry

**Input:** Hardcover API call fails (timeout, rate limit, network error)

**Steps:**
```
1. API call fails
   - Exception: Timeout after 30 seconds
   - Record: book_id=42, title="Project Hail Mary"

2. Check retry count
   - Current: 0 of 3 allowed
   - Action: Retry with exponential backoff

3. Wait & retry
   - Sleep: 1 second
   - Retry API call

4. Retry succeeds
   - Continue with normal processing
   - Log: "Retry #1 succeeded for book_id 42"

5. All retries exhausted
   - Current: 3 of 3 retries done
   - Mark record: status='manual_review_needed'
   - Queue for human inspection: user reviews and manually provides metadata
   - Log: "book_id 42 queued for manual enrichment"

6. Monitoring
   - Alert: "ETL rate: 95% success (1 failure in 20 attempts)"
   - If > 5% failures: Page on-call engineer
```

---

## Troubleshooting Guide

### Issue: Duplicate sessions detected
**Solution:** Check UNIQUE constraint logic; verify session gap definition

```sql
SELECT * FROM reading_sessions rs
WHERE rs.book_id = ? AND rs.start_time BETWEEN ? AND ?
ORDER BY rs.start_time;
```

### Issue: Book matches not found
**Solution:** Improve fuzzy matching threshold or add manual mapping file

```python
# Increase threshold for stricter matching
combined_score = (title_score * 0.7) + (author_score * 0.3)
if combined_score >= 85:  # Stricter: was 80
    best_match = candidate
```

### Issue: Publisher consolidation errors
**Solution:** Verify canonical_id relationships before insert

```sql
-- Check for circular references
WITH RECURSIVE pub_hierarchy AS (
  SELECT publisher_id, parent_publisher_id, 1 as depth
  FROM publishers
  WHERE parent_publisher_id IS NULL

  UNION

  SELECT p.publisher_id, p.parent_publisher_id, ph.depth + 1
  FROM publishers p
  JOIN pub_hierarchy ph ON p.parent_publisher_id = ph.publisher_id
  WHERE ph.depth < 10  -- Prevent infinite recursion
)
SELECT * FROM pub_hierarchy;
```

---

## Next Steps

- **Story 3.2:** Implement full ETL pipeline with error handling
- **Story 4.2:** Audiobook history extraction
- **Story 5.2, 5.3:** Historical data import with validation
