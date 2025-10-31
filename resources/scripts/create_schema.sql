-- BookHelper Unified Database Schema
-- Story 1.4: Design and implement unified database schema
-- Purpose: Create dimension and fact tables for reading analytics across ebook and audiobook sources
-- Database: Neon.tech PostgreSQL v17
-- Created: 2025-10-30, Updated: 2025-10-31
--
-- Schema Overview:
-- - authors: Author dimension table
-- - publishers: Publisher dimension with consolidation support (P1, P3, P4)
-- - books: Book dimension table with enriched metadata from Hardcover API
-- - book_editions: Physical/format edition tracking for owned copies
-- - reading_sessions: Fact table for reading events (ebook + audiobook)
-- - sync_status: ETL synchronization tracking
-- - Views: Computed aggregations for multi-source analytics
--
-- Key Features:
-- - Supports both ebook (page-based) and audiobook (time-based) metrics
-- - Publisher consolidation (handle "Penguin" vs "Penguin Publishing" duplication)
-- - Author dimension for author-specific analytics
-- - Edition tracking for physical library and special editions owned
-- - Tandem reading support with read_instance_id for parallel format reading
-- - Re-read tracking via read_count on books and read_instance_id in sessions
-- - Multi-format ownership tracking (ebook, audiobook, hardcover, paperback, etc.)
-- - Optimized for dimensional analytics queries
-- ============================================================

-- ============================================================================
-- TABLE 1: authors (Author Dimension)
-- ============================================================================
-- Purpose: Author master data with diversity and prolific metrics
-- Strategy: Single author record linked to multiple books
-- ============================================================================

CREATE TABLE IF NOT EXISTS authors (
  author_id SERIAL PRIMARY KEY,

  -- Core identity
  author_name VARCHAR(255) NOT NULL,
  alternate_names JSONB DEFAULT '[]',
  author_slug VARCHAR(255),

  -- Hardcover API references
  author_hardcover_id VARCHAR(100) UNIQUE,

  -- Author metrics
  book_count INT,
  contributions JSONB DEFAULT '[]',
  born_year INT,

  -- Diversity metrics
  is_bipoc BOOLEAN DEFAULT FALSE,
  is_lgbtq BOOLEAN DEFAULT FALSE,

  -- Identifiers (VIAF, Wikidata, etc.)
  identifiers JSONB DEFAULT '{}',

  -- Audit trail
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_authors_hardcover_id ON authors(author_hardcover_id);
CREATE INDEX IF NOT EXISTS idx_authors_name ON authors(author_name);

COMMENT ON TABLE authors IS 'Author dimension table with diversity metrics and prolific indicators. Source: Hardcover API.';
COMMENT ON COLUMN authors.author_name IS 'Primary author name. Source: KOReader/Hardcover.';
COMMENT ON COLUMN authors.alternate_names IS 'Array of pen names and pseudonyms (JSONB). Source: Hardcover API.';
COMMENT ON COLUMN authors.author_hardcover_id IS 'Hardcover API author ID. Source: Hardcover API.';
COMMENT ON COLUMN authors.book_count IS 'Total published works by author. Source: Hardcover API.';
COMMENT ON COLUMN authors.contributions IS 'Array of contribution types (author, editor, translator, illustrator). Source: Hardcover API.';
COMMENT ON COLUMN authors.born_year IS 'Author birth year for temporal analytics. Source: Hardcover API.';
COMMENT ON COLUMN authors.is_bipoc IS 'Author diversity flag. Source: Hardcover API.';
COMMENT ON COLUMN authors.is_lgbtq IS 'Author LGBTQ+ flag. Source: Hardcover API.';

-- ============================================================================
-- TABLE 2: publishers (Publisher Dimension)
-- ============================================================================
-- Purpose: Consolidate publisher metadata with support for name aliases and hierarchy
-- Strategy: Single source of truth for publisher identity with historical tracking
-- ============================================================================

CREATE TABLE IF NOT EXISTS publishers (
  publisher_id SERIAL PRIMARY KEY,

  -- Core identity
  publisher_name VARCHAR(255) NOT NULL UNIQUE,
  alternate_names TEXT[] DEFAULT '{}',

  -- Hardcover API references (P1)
  publisher_hardcover_id INT UNIQUE,

  -- Publisher hierarchy (P3, P4)
  canonical_hardcover_id INT,
  parent_id INT,
  parent_publisher VARCHAR(255),

  -- Metadata
  country VARCHAR(100),
  notes TEXT,

  -- Audit trail
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_publishers_hardcover_id ON publishers(publisher_hardcover_id);
CREATE INDEX IF NOT EXISTS idx_publishers_canonical_id ON publishers(canonical_hardcover_id);

COMMENT ON TABLE publishers IS 'Publisher dimension with consolidation and hierarchy tracking. Source: Hardcover API.';
COMMENT ON COLUMN publishers.publisher_name IS 'Canonical publisher name. Source: Hardcover API.';
COMMENT ON COLUMN publishers.alternate_names IS 'Known alternate names. Source: Hardcover API.';
COMMENT ON COLUMN publishers.publisher_hardcover_id IS 'Hardcover API publisher ID (P1). Source: Hardcover API.';
COMMENT ON COLUMN publishers.canonical_hardcover_id IS 'Canonical publisher if consolidated (P3). Source: Hardcover API.';
COMMENT ON COLUMN publishers.parent_id IS 'Parent publisher ID from Hardcover (reference only, not FK). Source: Hardcover API.';
COMMENT ON COLUMN publishers.parent_publisher IS 'Parent publisher name (denormalized reference). Source: Hardcover API.';

-- ============================================================================
-- TABLE 3: books (Books Dimension Table)
-- ============================================================================
-- Purpose: Book master data with metadata enrichment from multiple sources
-- Strategy: Fact-independent dimension table; enriched from Hardcover API
-- ============================================================================

CREATE TABLE IF NOT EXISTS books (
  -- PRIMARY KEY
  book_id SERIAL PRIMARY KEY,

  -- ========== CORE IDENTIFICATION ==========
  title VARCHAR(255) NOT NULL,
  author VARCHAR(255),
  author_id INT REFERENCES authors(author_id) ON DELETE SET NULL,

  -- ========== ISBN / ASIN / IDENTIFIERS ==========
  isbn_13 VARCHAR(20),
  isbn_10 VARCHAR(20),
  asin VARCHAR(20),
  hardcover_book_id VARCHAR(100),

  -- ========== PUBLISHER & SERIES ==========
  publisher_id INT REFERENCES publishers(publisher_id) ON DELETE SET NULL,
  publisher_name VARCHAR(255),
  series_name VARCHAR(255),
  series_number NUMERIC(5,2),

  -- ========== BOOK DEMOGRAPHICS & METADATA ==========
  page_count INT,
  audio_seconds INT,
  language CHAR(2) DEFAULT 'en',
  published_date DATE,
  description TEXT,

  -- ========== RATINGS & REVIEWS ==========
  hardcover_rating DECIMAL(3, 2),
  hardcover_rating_count INT,
  user_rating DECIMAL(3, 2),
  user_rating_date TIMESTAMP,

  -- ========== AUTHOR METRICS ==========
  author_hardcover_id VARCHAR(100),
  is_bipoc BOOLEAN DEFAULT FALSE,
  is_lgbtq BOOLEAN DEFAULT FALSE,
  author_birth_year INT,
  author_books_count INT,

  -- ========== GENRE & CONTENT METADATA ==========
  genres JSONB DEFAULT '[]',
  moods JSONB DEFAULT '[]',
  content_warnings JSONB DEFAULT '[]',
  cached_tags JSONB DEFAULT '[]',
  alternative_titles JSONB DEFAULT '[]',
  activities_count INT,
  cover_color JSONB,
  users_read_count INT,
  users_count INT,

  -- ========== KOREADER & SOURCE DATA ==========
  file_hash VARCHAR(32),
  notes INT DEFAULT 0,
  highlights INT DEFAULT 0,
  source VARCHAR(50) DEFAULT 'koreader',
  device_stats_source VARCHAR(100),

  -- ========== COVER & DISPLAY ==========
  cover_url TEXT,

  -- ========== USER LIBRARY TRACKING (from Hardcover Activities) ==========
  user_owns_ebook BOOLEAN DEFAULT FALSE,
  user_owns_audiobook BOOLEAN DEFAULT FALSE,
  user_owns_physical BOOLEAN DEFAULT FALSE,
  user_reading_status VARCHAR(50),
  user_added_date TIMESTAMP,

  -- ========== MULTI-FORMAT OWNERSHIP (deprecated, use user_owns_* fields) ==========
  media_types_owned TEXT[] DEFAULT '{"ebook"}',
  owned_physical_formats TEXT[] DEFAULT '{}',
  owned_special_editions TEXT[] DEFAULT '{}',

  -- ========== READ TRACKING ==========
  read_count INT DEFAULT 1,

  -- ========== AUDIT & CONTROL ==========
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_books_isbn_13 ON books(isbn_13);
CREATE INDEX IF NOT EXISTS idx_books_asin ON books(asin);
CREATE INDEX IF NOT EXISTS idx_books_author_id ON books(author_id);
CREATE INDEX IF NOT EXISTS idx_books_hardcover_id ON books(hardcover_book_id);
CREATE INDEX IF NOT EXISTS idx_books_publisher_id ON books(publisher_id);
CREATE INDEX IF NOT EXISTS idx_books_source ON books(source);
CREATE INDEX IF NOT EXISTS idx_books_published_date ON books(published_date);
CREATE INDEX IF NOT EXISTS idx_books_cached_tags ON books USING GIN(cached_tags);
CREATE INDEX IF NOT EXISTS idx_books_genres ON books USING GIN(genres);
CREATE INDEX IF NOT EXISTS idx_books_moods ON books USING GIN(moods);

COMMENT ON TABLE books IS 'Book dimension table with multi-source enrichment. Supports ebook, audiobook, and physical library tracking. Sources: KOReader, Hardcover API, computed.';
COMMENT ON COLUMN books.author IS 'Primary author name (colloquial). Source: KOReader/Hardcover.';
COMMENT ON COLUMN books.author_id IS 'Foreign key to authors table. Source: Hardcover API.';
COMMENT ON COLUMN books.publisher_name IS 'Publisher name for convenience. Source: Hardcover API.';
COMMENT ON COLUMN books.series_number IS 'Numeric series position (supports .5 for novellas). Source: KOReader/Hardcover.';
COMMENT ON COLUMN books.audio_seconds IS 'Total audiobook duration in seconds. Source: Hardcover API.';
COMMENT ON COLUMN books.hardcover_rating IS 'Hardcover community rating. Source: Hardcover API.';
COMMENT ON COLUMN books.user_rating IS 'Your personal rating of the book. Source: Hardcover API (user activities).';
COMMENT ON COLUMN books.user_rating_date IS 'When you rated this book. Source: Hardcover API (user activities).';
COMMENT ON COLUMN books.genres IS 'Array of genres from Hardcover. Source: Hardcover API.';
COMMENT ON COLUMN books.moods IS 'Array of moods (dark, cozy, inspirational). Source: Hardcover API.';
COMMENT ON COLUMN books.content_warnings IS 'Array of content warnings. Source: Hardcover API.';
COMMENT ON COLUMN books.alternative_titles IS 'Array of alternative titles (localized, original). Source: Hardcover API.';
COMMENT ON COLUMN books.user_owns_ebook IS 'Whether user owns ebook edition. Source: Hardcover API (activities).';
COMMENT ON COLUMN books.user_owns_audiobook IS 'Whether user owns audiobook edition. Source: Hardcover API (activities).';
COMMENT ON COLUMN books.user_owns_physical IS 'Whether user owns physical edition. Source: Hardcover API (activities).';
COMMENT ON COLUMN books.user_reading_status IS 'Current reading status (reading, finished, want-to-read, dnf). Source: Hardcover API (activities).';
COMMENT ON COLUMN books.user_added_date IS 'When user added book to library. Source: Hardcover API (activities).';
COMMENT ON COLUMN books.media_types_owned IS 'DEPRECATED: Use user_owns_* fields instead. Format array: ["ebook", "audiobook"]. Source: User tracking.';
COMMENT ON COLUMN books.owned_physical_formats IS 'DEPRECATED: Track via book_editions table. Physical copy formats. Source: User tracking.';
COMMENT ON COLUMN books.read_count IS 'Number of times read/heard. Increments on new read_instance_id. Source: Computed from reading_sessions.';

-- ============================================================================
-- TABLE 4: book_editions (Edition Tracking for Physical Library)
-- ============================================================================
-- Purpose: Track specific editions owned (special editions, different formats, etc.)
-- Strategy: Allow tracking multiple editions of same book with condition and notes
-- ============================================================================

CREATE TABLE IF NOT EXISTS book_editions (
  edition_id SERIAL PRIMARY KEY,
  book_id INT NOT NULL REFERENCES books(book_id) ON DELETE CASCADE,

  -- Edition details (from Hardcover Editions API)
  edition_format VARCHAR(50),
  edition_name VARCHAR(255),
  publication_year INT,
  publisher_specific VARCHAR(255),
  isbn_specific VARCHAR(20),
  language VARCHAR(10),
  pages INT,
  audio_seconds INT,
  release_date DATE,

  -- Physical library metadata (user tracking)
  condition VARCHAR(50),
  notes TEXT,
  date_acquired DATE,
  display_location VARCHAR(100),

  -- Audit
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_book_editions_book_id ON book_editions(book_id);
CREATE INDEX IF NOT EXISTS idx_book_editions_format ON book_editions(edition_format);

COMMENT ON TABLE book_editions IS 'Track specific physical editions owned (hardcover, paperback, special editions, etc.). Source: Hardcover Editions API + User tracking.';
COMMENT ON COLUMN book_editions.edition_format IS 'Format type: hardcover, paperback, special-edition, signed, limited. Source: Hardcover API / User input.';
COMMENT ON COLUMN book_editions.edition_name IS 'Edition name (Anniversary Edition, Premium Edition, etc.). Source: Hardcover API / User input.';
COMMENT ON COLUMN book_editions.condition IS 'Condition: new, like-new, good, fair, poor. Source: User input.';

-- ============================================================================
-- TABLE 5: reading_sessions (Reading Sessions Fact Table)
-- ============================================================================
-- Purpose: Individual reading session records (ebook pages or audiobook listening)
-- Strategy: Immutable append-only fact table; high cardinality; aggregated via views
-- Data Sources: KOReader, BookPlayer, Kindle (historical), Audible (historical)
-- ============================================================================

CREATE TABLE IF NOT EXISTS reading_sessions (
  -- PRIMARY KEY
  session_id BIGSERIAL PRIMARY KEY,

  -- ========== CORE READING FACTS ==========
  book_id INT NOT NULL REFERENCES books(book_id) ON DELETE CASCADE,
  start_time TIMESTAMP NOT NULL,
  duration_minutes INT NOT NULL,
  device VARCHAR(50) NOT NULL,

  -- ========== READING FORMAT DETAILS ==========
  media_type VARCHAR(20) DEFAULT 'ebook',
  pages_read INT,

  -- ========== TANDEM READING SUPPORT ==========
  read_instance_id UUID DEFAULT gen_random_uuid(),
  is_parallel_read BOOLEAN DEFAULT FALSE,

  -- ========== SESSION TRACKING ==========
  read_number INT DEFAULT 1,
  end_time TIMESTAMP,

  -- ========== DATA PROVENANCE ==========
  data_source VARCHAR(50) DEFAULT 'koreader',
  device_stats_source VARCHAR(100),

  -- ========== AUDIT & CONTROL ==========
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

  -- ========== CONSTRAINTS ==========
  UNIQUE(book_id, start_time, device),
  CONSTRAINT duration_positive CHECK (duration_minutes > 0),
  CONSTRAINT valid_start_time CHECK (start_time <= CURRENT_TIMESTAMP)
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_reading_sessions_book_id ON reading_sessions(book_id);
CREATE INDEX IF NOT EXISTS idx_reading_sessions_start_time ON reading_sessions(start_time);
CREATE INDEX IF NOT EXISTS idx_reading_sessions_device ON reading_sessions(device);
CREATE INDEX IF NOT EXISTS idx_reading_sessions_media_type ON reading_sessions(media_type);
CREATE INDEX IF NOT EXISTS idx_reading_sessions_data_source ON reading_sessions(data_source);
CREATE INDEX IF NOT EXISTS idx_reading_sessions_read_instance ON reading_sessions(read_instance_id);
CREATE INDEX IF NOT EXISTS idx_reading_sessions_book_date ON reading_sessions(book_id, start_time DESC);
CREATE INDEX IF NOT EXISTS idx_reading_sessions_date_device ON reading_sessions(start_time DESC, device);

COMMENT ON TABLE reading_sessions IS 'Reading session fact table with tandem reading support. Sources: KOReader, BookPlayer, Kindle, Audible.';
COMMENT ON COLUMN reading_sessions.duration_minutes IS 'Session duration in minutes. Works for ebook and audiobook. Source: KOReader/BookPlayer.';
COMMENT ON COLUMN reading_sessions.pages_read IS 'Pages read (ebook only). NULL for audiobook. Source: KOReader.';
COMMENT ON COLUMN reading_sessions.media_type IS 'Format: "ebook" or "audiobook". Source: Session type.';
COMMENT ON COLUMN reading_sessions.read_instance_id IS 'UUID grouping tandem reads (same book, overlapping times, different formats). Source: Computed.';
COMMENT ON COLUMN reading_sessions.is_parallel_read IS 'Flag for tandem reading sessions. Source: Computed.';
COMMENT ON COLUMN reading_sessions.read_number IS 'Which read of the book (1=first, 2=reread). Increments with new read_instance_id. Source: Computed from books.read_count.';
COMMENT ON COLUMN reading_sessions.data_source IS 'ETL source: koreader, bookplayer, kindle, audible, hardcover. Source: ETL.';

-- ============================================================================
-- TABLE 6: sync_status (ETL Synchronization Tracking)
-- ============================================================================
-- Purpose: Track ETL sync state for incremental updates and monitoring
-- Strategy: One row per data source with cursor and status tracking
-- ============================================================================

CREATE TABLE IF NOT EXISTS sync_status (
  sync_id SERIAL PRIMARY KEY,
  source_name VARCHAR(50) NOT NULL UNIQUE,
  last_sync_time TIMESTAMP,
  last_sync_cursor VARCHAR(255),
  records_synced INT DEFAULT 0,
  records_created INT DEFAULT 0,
  records_updated INT DEFAULT 0,
  sync_status VARCHAR(50) DEFAULT 'pending',
  error_message TEXT,
  sync_duration_seconds INT,
  next_scheduled_sync TIMESTAMP,
  sync_mode VARCHAR(50) DEFAULT 'incremental',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE sync_status IS 'ETL synchronization tracking for incremental updates. Sources: koreader, hardcover_books, hardcover_activities, hardcover_editions, kindle, audible.';
COMMENT ON COLUMN sync_status.source_name IS 'Data source identifier (koreader, hardcover_books, etc.). Source: ETL.';
COMMENT ON COLUMN sync_status.last_sync_cursor IS 'Cursor/bookmark for incremental queries (max timestamp, last_id, offset). Source: ETL.';
COMMENT ON COLUMN sync_status.sync_status IS 'Status: pending, in_progress, success, partial_success, failed. Source: ETL.';
COMMENT ON COLUMN sync_status.sync_mode IS 'Type of sync: full_refresh, incremental, or validation. Source: ETL.';

-- ============================================================================
-- COMPUTED VIEWS FOR MULTI-SOURCE AGGREGATION
-- ============================================================================

-- View 1: Book Statistics (K1, K2, K3 computed fields + reading speed)
CREATE OR REPLACE VIEW book_stats AS
SELECT
  b.book_id,
  b.title,
  b.author,
  MAX(rs.start_time) as last_opened,
  SUM(rs.duration_minutes) FILTER (WHERE rs.media_type = 'ebook') as total_read_time_ebook_minutes,
  SUM(rs.duration_minutes) FILTER (WHERE rs.media_type = 'audiobook') as total_read_time_audio_minutes,
  SUM(rs.duration_minutes) as total_read_time_minutes,
  SUM(rs.pages_read) FILTER (WHERE rs.media_type = 'ebook') as total_pages_read_ebook,
  COUNT(*) FILTER (WHERE rs.media_type = 'ebook') as ebook_session_count,
  COUNT(*) FILTER (WHERE rs.media_type = 'audiobook') as audiobook_session_count,
  COUNT(*) as total_sessions,
  COUNT(DISTINCT rs.read_instance_id) as read_count,
  CASE
    WHEN SUM(rs.pages_read) FILTER (WHERE rs.media_type = 'ebook') > 0
    THEN ROUND(
      SUM(rs.pages_read) FILTER (WHERE rs.media_type = 'ebook')::NUMERIC /
      NULLIF(SUM(rs.duration_minutes) FILTER (WHERE rs.media_type = 'ebook'), 0), 2
    )
    ELSE NULL
  END as avg_reading_speed_pages_per_minute
FROM books b
LEFT JOIN reading_sessions rs ON b.book_id = rs.book_id
GROUP BY b.book_id, b.title, b.author;

COMMENT ON VIEW book_stats IS 'Computed aggregation of reading statistics. Provides last_opened, total_read_time (split by media), total_pages, read_count, and reading speed. Sources: Computed from reading_sessions.';

-- View 2: Reading Timeline (chronological with enrichment)
CREATE OR REPLACE VIEW reading_timeline AS
SELECT
  rs.session_id,
  rs.start_time,
  rs.end_time,
  rs.duration_minutes,
  rs.pages_read,
  rs.media_type,
  rs.device,
  rs.data_source,
  rs.read_instance_id,
  rs.is_parallel_read,
  rs.read_number,
  b.book_id,
  b.title,
  b.author,
  b.series_name,
  b.series_number,
  b.cached_tags,
  p.publisher_name as publisher,
  a.author_name
FROM reading_sessions rs
JOIN books b ON rs.book_id = b.book_id
LEFT JOIN publishers p ON b.publisher_id = p.publisher_id
LEFT JOIN authors a ON b.author_id = a.author_id
ORDER BY rs.start_time DESC;

COMMENT ON VIEW reading_timeline IS 'Enriched chronological view of all reading events. Sources: reading_sessions, books, publishers, authors.';

-- View 3: Publisher Analytics
CREATE OR REPLACE VIEW publisher_analytics AS
SELECT
  p.publisher_id,
  p.publisher_name,
  p.parent_id,
  COUNT(DISTINCT b.book_id) as books_read,
  COUNT(DISTINCT rs.session_id) as total_sessions,
  SUM(rs.duration_minutes) FILTER (WHERE rs.media_type = 'ebook') as total_ebook_minutes,
  SUM(rs.duration_minutes) FILTER (WHERE rs.media_type = 'audiobook') as total_audio_minutes,
  AVG(b.hardcover_rating) as avg_hardcover_rating,
  AVG(b.user_rating) as avg_user_rating
FROM publishers p
LEFT JOIN books b ON p.publisher_id = b.publisher_id
LEFT JOIN reading_sessions rs ON b.book_id = rs.book_id
GROUP BY p.publisher_id, p.publisher_name, p.parent_id;

COMMENT ON VIEW publisher_analytics IS 'Publisher-level analytics. Sources: books, reading_sessions, publishers.';

-- View 4: Author Analytics
CREATE OR REPLACE VIEW author_analytics AS
SELECT
  a.author_id,
  a.author_name,
  a.born_year,
  a.is_bipoc,
  a.is_lgbtq,
  COUNT(DISTINCT b.book_id) as books_read,
  COUNT(DISTINCT rs.session_id) as total_sessions,
  SUM(rs.duration_minutes) FILTER (WHERE rs.media_type = 'ebook') as total_ebook_minutes,
  SUM(rs.duration_minutes) FILTER (WHERE rs.media_type = 'audiobook') as total_audio_minutes,
  AVG(b.hardcover_rating) as avg_hardcover_rating,
  AVG(b.user_rating) as avg_user_rating
FROM authors a
LEFT JOIN books b ON a.author_id = b.author_id
LEFT JOIN reading_sessions rs ON b.book_id = rs.book_id
GROUP BY a.author_id, a.author_name, a.born_year, a.is_bipoc, a.is_lgbtq;

COMMENT ON VIEW author_analytics IS 'Author-level analytics with diversity metrics. Sources: authors, books, reading_sessions.';

-- View 5: Tandem Reading Sessions (for overlap analysis)
CREATE OR REPLACE VIEW tandem_reading_sessions AS
SELECT
  read_instance_id,
  book_id,
  COUNT(*) as session_count,
  COUNT(DISTINCT media_type) as distinct_media_types,
  MIN(start_time) as instance_start,
  MAX(end_time) as instance_end,
  STRING_AGG(DISTINCT media_type, ', ' ORDER BY media_type) as media_types_combined,
  SUM(duration_minutes) as total_duration_all_formats,
  EXTRACT(EPOCH FROM (MAX(end_time) - MIN(start_time)))/60 as overlap_aware_duration_minutes
FROM reading_sessions
WHERE is_parallel_read = true
GROUP BY read_instance_id, book_id;

COMMENT ON VIEW tandem_reading_sessions IS 'Tandem reading session analysis. Shows overlapping reads with duration calculations. Sources: reading_sessions.';

-- ============================================================================
-- TRIGGERS FOR AUTOMATIC TIMESTAMP UPDATES
-- ============================================================================

-- Function to update modified timestamp
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = CURRENT_TIMESTAMP;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply trigger to all tables with updated_at
CREATE TRIGGER update_authors_updated_at
BEFORE UPDATE ON authors
FOR EACH ROW
EXECUTE FUNCTION update_modified_column();

CREATE TRIGGER update_publishers_updated_at
BEFORE UPDATE ON publishers
FOR EACH ROW
EXECUTE FUNCTION update_modified_column();

CREATE TRIGGER update_books_updated_at
BEFORE UPDATE ON books
FOR EACH ROW
EXECUTE FUNCTION update_modified_column();

CREATE TRIGGER update_sync_status_updated_at
BEFORE UPDATE ON sync_status
FOR EACH ROW
EXECUTE FUNCTION update_modified_column();
