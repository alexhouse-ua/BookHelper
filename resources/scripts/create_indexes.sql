-- ============================================================
-- Story 1.4: Create Performance Indexes
-- Task 4: Indexes for Optimal Query Performance
-- ============================================================
--
-- NOTE: Most indexes are created inline in create_schema.sql
-- This file contains additional composite indexes for specific query patterns
--
-- Purpose: Create composite B-tree and GIN indexes for optimal query performance
--
-- Performance Goals:
-- - Queries should complete in < 2 seconds (from architecture.md)
-- - Support dimensional analytics (book_id aggregations)
-- - Support time-range queries (start_time filtering)
-- - Support device-specific analytics (device filtering)
-- - Support JSONB queries on genres, moods, tags
--
-- Index Strategy:
-- - Composite indexes for common query patterns
-- - GIN indexes for JSONB array queries
-- - Avoid redundant indexes (PostgreSQL auto-indexes PKs and FKs)
--
-- Generated: 2025-10-30, Updated: 2025-10-31
-- ============================================================

-- ============================================================
-- COMPOSITE INDEXES FOR READING_SESSIONS
-- ============================================================

-- Most frequent query: sessions for a book ordered by date
-- Use Case: "Show all sessions for book X, most recent first"
CREATE INDEX IF NOT EXISTS idx_reading_sessions_book_date
ON reading_sessions(book_id, start_time DESC);

-- Device + time filtering (reading patterns by device over time)
-- Use Case: "Reading sessions on device X in date range Y-Z"
CREATE INDEX IF NOT EXISTS idx_reading_sessions_date_device
ON reading_sessions(start_time DESC, device);

-- Tandem reading detection (overlapping sessions by read_instance_id)
-- Use Case: "Find all parallel reading sessions grouped by read_instance_id"
CREATE INDEX IF NOT EXISTS idx_reading_sessions_parallel
ON reading_sessions(is_parallel_read, read_instance_id)
WHERE is_parallel_read = true;

-- ============================================================
-- GIN INDEXES FOR JSONB QUERIES (BOOKS TABLE)
-- ============================================================

-- Genres array search
-- Use Case: SELECT * FROM books WHERE genres @> '["Romance"]'
CREATE INDEX IF NOT EXISTS idx_books_genres
ON books USING GIN(genres);

-- Moods array search
-- Use Case: SELECT * FROM books WHERE moods @> '["dark"]'
CREATE INDEX IF NOT EXISTS idx_books_moods
ON books USING GIN(moods);

-- Content warnings array search
-- Use Case: SELECT * FROM books WHERE content_warnings @> '["violence"]'
CREATE INDEX IF NOT EXISTS idx_books_content_warnings
ON books USING GIN(content_warnings);

-- Cached tags array search (already created in create_schema.sql)
-- Use Case: SELECT * FROM books WHERE cached_tags @> '["sci-fi"]'
-- CREATE INDEX IF NOT EXISTS idx_books_cached_tags ON books USING GIN(cached_tags);

-- ============================================================
-- COMPOSITE INDEXES FOR BOOKS TABLE
-- ============================================================

-- Author + diversity filtering
-- Use Case: "Books by BIPOC or LGBTQ+ authors"
CREATE INDEX IF NOT EXISTS idx_books_author_diversity
ON books(author_id, is_bipoc, is_lgbtq);

-- User library filtering (ownership status)
-- Use Case: "Books I own in ebook + audiobook formats"
CREATE INDEX IF NOT EXISTS idx_books_user_ownership
ON books(user_owns_ebook, user_owns_audiobook, user_owns_physical)
WHERE user_owns_ebook = true OR user_owns_audiobook = true OR user_owns_physical = true;

-- Reading status filtering
-- Use Case: "Books currently reading or want-to-read"
CREATE INDEX IF NOT EXISTS idx_books_reading_status
ON books(user_reading_status)
WHERE user_reading_status IS NOT NULL;

-- ============================================================
-- INDEXES FOR AUTHORS TABLE
-- ============================================================

-- Diversity analytics
-- Use Case: "BIPOC or LGBTQ+ authors with books in library"
CREATE INDEX IF NOT EXISTS idx_authors_diversity
ON authors(is_bipoc, is_lgbtq)
WHERE is_bipoc = true OR is_lgbtq = true;

-- ============================================================
-- INDEXES FOR BOOK_EDITIONS TABLE
-- ============================================================

-- Format + book lookup
-- Use Case: "All hardcover editions I own"
CREATE INDEX IF NOT EXISTS idx_book_editions_format_book
ON book_editions(edition_format, book_id);

-- ============================================================
-- VERIFICATION COMMANDS (for manual testing)
-- ============================================================
-- Run these in psql to verify index creation:
--
-- List all indexes:
--   \di
--
-- List reading_sessions indexes only:
--   \di reading_sessions*
--
-- List books indexes:
--   \di books*
--
-- Show table structure + indexes:
--   \d+ reading_sessions
--   \d+ books
--   \d+ authors
--   \d+ book_editions
--
-- Verify index usage with EXPLAIN ANALYZE:
--
--   EXPLAIN ANALYZE
--   SELECT COUNT(*) FROM reading_sessions
--   WHERE book_id = 1 AND start_time >= '2025-01-01'::timestamp;
--
--   EXPLAIN ANALYZE
--   SELECT * FROM books
--   WHERE genres @> '["Romance"]'::jsonb;
--
--   EXPLAIN ANALYZE
--   SELECT COUNT(*) FROM books
--   WHERE is_bipoc = true AND user_owns_ebook = true;
-- ============================================================

-- ============================================================
-- INDEX MAINTENANCE NOTES
-- ============================================================
--
-- VACUUM ANALYZE after bulk inserts:
--   VACUUM ANALYZE reading_sessions;
--   VACUUM ANALYZE books;
--
-- Rebuild indexes if needed:
--   REINDEX TABLE reading_sessions;
--
-- Monitor index bloat:
--   SELECT schemaname, tablename, indexname,
--          pg_size_pretty(pg_relation_size(indexrelid)) as size
--   FROM pg_stat_user_indexes
--   ORDER BY pg_relation_size(indexrelid) DESC;
-- ============================================================
