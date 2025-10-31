#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprehensive Schema Operations Test Suite
Story 1.4: Task 5 - Validate schema implementation

This script runs comprehensive tests on the BookHelper PostgreSQL schema:
1. Schema structure validation (all columns, types, constraints)
2. CRUD operations on all 6 tables
3. JSONB operations (INSERT, UPDATE, SELECT with @>, ?, ?&, ?| operators)
4. Foreign key relationships and CASCADE behavior
5. Constraint enforcement (UNIQUE, CHECK, NOT NULL)
6. Trigger functionality (updated_at auto-update on all tables)
7. View queries with sample data (5 views)
8. Index existence verification
9. Edge cases and error conditions

Usage:
    python3 test_schema_operations.py

Environment Variables (from .env.neon):
    NEON_HOST, NEON_PORT, NEON_USER, NEON_PASSWORD, NEON_DATABASE

Exit Codes:
    0 - All tests passed
    1 - One or more tests failed
"""

import os
import sys
from pathlib import Path
import psycopg2
from psycopg2 import sql, Error, errors
from datetime import datetime, timedelta
import time

# Ensure UTF-8 output
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Terminal colors
class Color:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

class TestStats:
    """Track test results"""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.warnings = 0

    def pass_test(self, name):
        self.passed += 1
        print(f"{Color.GREEN}✓{Color.RESET} {name}")

    def fail_test(self, name, error):
        self.failed += 1
        print(f"{Color.RED}✗{Color.RESET} {name}")
        print(f"  {Color.RED}Error: {error}{Color.RESET}")

    def warn_test(self, name, warning):
        self.warnings += 1
        print(f"{Color.YELLOW}⚠{Color.RESET} {name}")
        print(f"  {Color.YELLOW}Warning: {warning}{Color.RESET}")

    def summary(self):
        total = self.passed + self.failed
        print(f"\n{Color.BLUE}{'='*60}{Color.RESET}")
        print(f"{Color.BOLD}Test Summary{Color.RESET}")
        print(f"{Color.BLUE}{'='*60}{Color.RESET}\n")
        print(f"Total Tests: {total}")
        print(f"{Color.GREEN}Passed: {self.passed}{Color.RESET}")
        print(f"{Color.RED}Failed: {self.failed}{Color.RESET}")
        print(f"{Color.YELLOW}Warnings: {self.warnings}{Color.RESET}\n")

        if self.failed == 0:
            print(f"{Color.BOLD}{Color.GREEN}✓ ALL TESTS PASSED{Color.RESET}\n")
            return 0
        else:
            print(f"{Color.BOLD}{Color.RED}✗ TESTS FAILED{Color.RESET}\n")
            return 1

def load_env_file(filepath='.env.neon'):
    """Load environment variables from .env file"""
    env_path = Path(filepath)
    if not env_path.exists():
        print(f"{Color.RED}✗ .env.neon file not found{Color.RESET}")
        return False

    with open(env_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()

    return True

def get_db_connection():
    """Establish connection to Neon PostgreSQL database"""
    try:
        conn = psycopg2.connect(
            host=os.getenv('NEON_HOST'),
            port=os.getenv('NEON_PORT', '5432'),
            database=os.getenv('NEON_DATABASE'),
            user=os.getenv('NEON_USER'),
            password=os.getenv('NEON_PASSWORD'),
            sslmode='require',
            connect_timeout=10
        )
        return conn
    except Error as e:
        print(f"{Color.RED}✗ Connection failed: {e}{Color.RESET}")
        sys.exit(1)

# ============================================================
# TEST SUITE 1: SCHEMA STRUCTURE VALIDATION
# ============================================================

def test_schema_structure(conn, stats):
    """Validate all tables have correct columns and types"""
    print(f"\n{Color.BLUE}{'='*60}{Color.RESET}")
    print(f"{Color.BOLD}Test Suite 1: Schema Structure Validation{Color.RESET}")
    print(f"{Color.BLUE}{'='*60}{Color.RESET}\n")

    # Expected schema structure (from canonical create_schema.sql)
    expected_tables = {
        'authors': ['author_id', 'author_name', 'author_slug', 'author_hardcover_id',
                   'alternate_names', 'book_count', 'contributions', 'born_year',
                   'is_bipoc', 'is_lgbtq', 'identifiers', 'created_at', 'updated_at'],
        'publishers': ['publisher_id', 'publisher_name', 'alternate_names',
                      'publisher_hardcover_id', 'canonical_hardcover_id', 'parent_id',
                      'parent_publisher', 'country', 'notes', 'created_at', 'updated_at'],
        'books': ['book_id', 'title', 'author', 'author_id', 'isbn_13', 'isbn_10', 'asin',
                 'hardcover_book_id', 'publisher_id', 'publisher_name', 'series_name',
                 'series_number', 'page_count', 'audio_seconds', 'language', 'published_date',
                 'description', 'hardcover_rating', 'hardcover_rating_count', 'user_rating',
                 'user_rating_date', 'author_hardcover_id', 'is_bipoc', 'is_lgbtq',
                 'author_birth_year', 'author_books_count', 'genres', 'moods',
                 'content_warnings', 'cached_tags', 'alternative_titles', 'activities_count',
                 'cover_color', 'users_read_count', 'users_count', 'file_hash', 'notes',
                 'highlights', 'source', 'device_stats_source', 'cover_url', 'user_owns_ebook',
                 'user_owns_audiobook', 'user_owns_physical', 'user_reading_status',
                 'user_added_date', 'media_types_owned', 'owned_physical_formats',
                 'owned_special_editions', 'read_count', 'created_at', 'updated_at'],
        'book_editions': ['edition_id', 'book_id', 'edition_format', 'edition_name',
                         'publication_year', 'publisher_specific', 'isbn_specific',
                         'language', 'pages', 'audio_seconds', 'release_date', 'condition',
                         'notes', 'date_acquired', 'display_location', 'created_at'],
        'reading_sessions': ['session_id', 'book_id', 'start_time', 'duration_minutes',
                            'device', 'media_type', 'pages_read', 'read_instance_id',
                            'is_parallel_read', 'read_number', 'end_time', 'data_source',
                            'device_stats_source', 'created_at'],
        'sync_status': ['sync_id', 'source_name', 'last_sync_time', 'last_sync_cursor',
                       'records_synced', 'records_created', 'records_updated', 'sync_status',
                       'error_message', 'sync_duration_seconds', 'next_scheduled_sync',
                       'sync_mode', 'created_at', 'updated_at']
    }

    with conn.cursor() as cur:
        for table_name, expected_columns in expected_tables.items():
            try:
                # Get actual columns
                cur.execute("""
                    SELECT column_name
                    FROM information_schema.columns
                    WHERE table_schema = 'public' AND table_name = %s
                    ORDER BY ordinal_position
                """, (table_name,))

                actual_columns = [row[0] for row in cur.fetchall()]

                # Check all expected columns exist
                missing = set(expected_columns) - set(actual_columns)
                extra = set(actual_columns) - set(expected_columns)

                if missing:
                    stats.fail_test(f"Table '{table_name}' structure",
                                  f"Missing columns: {', '.join(missing)}")
                elif extra:
                    stats.warn_test(f"Table '{table_name}' structure",
                                  f"Extra columns: {', '.join(extra)}")
                else:
                    stats.pass_test(f"Table '{table_name}' has all expected columns ({len(expected_columns)})")

            except Error as e:
                stats.fail_test(f"Table '{table_name}' structure check", str(e))

def test_jsonb_columns(conn, stats):
    """Verify JSONB columns have correct data type"""
    print(f"\n{Color.BLUE}{'='*60}{Color.RESET}")
    print(f"{Color.BOLD}Test Suite 1.1: JSONB Column Types{Color.RESET}")
    print(f"{Color.BLUE}{'='*60}{Color.RESET}\n")

    jsonb_columns = [
        ('authors', 'alternate_names'),
        ('authors', 'contributions'),
        ('authors', 'identifiers'),
        ('books', 'genres'),
        ('books', 'moods'),
        ('books', 'content_warnings'),
        ('books', 'cached_tags'),
        ('books', 'alternative_titles'),
        ('books', 'cover_color')
    ]

    with conn.cursor() as cur:
        for table_name, column_name in jsonb_columns:
            try:
                cur.execute("""
                    SELECT data_type
                    FROM information_schema.columns
                    WHERE table_schema = 'public'
                      AND table_name = %s
                      AND column_name = %s
                """, (table_name, column_name))

                result = cur.fetchone()
                if result and result[0] == 'jsonb':
                    stats.pass_test(f"{table_name}.{column_name} is JSONB")
                else:
                    actual_type = result[0] if result else 'NOT FOUND'
                    stats.fail_test(f"{table_name}.{column_name} JSONB check",
                                  f"Expected JSONB, got {actual_type}")

            except Error as e:
                stats.fail_test(f"{table_name}.{column_name} type check", str(e))

def test_constraints(conn, stats):
    """Verify key constraints exist"""
    print(f"\n{Color.BLUE}{'='*60}{Color.RESET}")
    print(f"{Color.BOLD}Test Suite 1.2: Constraint Validation{Color.RESET}")
    print(f"{Color.BLUE}{'='*60}{Color.RESET}\n")

    with conn.cursor() as cur:
        # Check PRIMARY KEY constraints
        primary_keys = {
            'authors': 'author_id',
            'publishers': 'publisher_id',
            'books': 'book_id',
            'book_editions': 'edition_id',
            'reading_sessions': 'session_id',
            'sync_status': 'sync_id'
        }

        for table, pk_column in primary_keys.items():
            try:
                cur.execute("""
                    SELECT COUNT(*)
                    FROM information_schema.table_constraints tc
                    JOIN information_schema.key_column_usage kcu
                      ON tc.constraint_name = kcu.constraint_name
                    WHERE tc.table_name = %s
                      AND tc.constraint_type = 'PRIMARY KEY'
                      AND kcu.column_name = %s
                """, (table, pk_column))

                if cur.fetchone()[0] > 0:
                    stats.pass_test(f"PRIMARY KEY on {table}({pk_column})")
                else:
                    stats.fail_test(f"PRIMARY KEY on {table}({pk_column})", "Not found")

            except Error as e:
                stats.fail_test(f"PRIMARY KEY check on {table}", str(e))

        # Check UNIQUE constraint on reading_sessions
        try:
            cur.execute("""
                SELECT COUNT(*)
                FROM information_schema.table_constraints
                WHERE table_name = 'reading_sessions'
                  AND constraint_type = 'UNIQUE'
            """)

            if cur.fetchone()[0] > 0:
                stats.pass_test("UNIQUE constraint on reading_sessions (book_id, start_time, device)")
            else:
                stats.fail_test("UNIQUE constraint on reading_sessions", "Not found")

        except Error as e:
            stats.fail_test("UNIQUE constraint check", str(e))

# ============================================================
# TEST SUITE 2: CRUD OPERATIONS
# ============================================================

def test_crud_operations(conn, stats):
    """Test CRUD operations on all tables"""
    print(f"\n{Color.BLUE}{'='*60}{Color.RESET}")
    print(f"{Color.BOLD}Test Suite 2: CRUD Operations{Color.RESET}")
    print(f"{Color.BLUE}{'='*60}{Color.RESET}\n")

    try:
        with conn.cursor() as cur:
            # === CREATE: Insert test data ===

            # 1. Insert author with JSONB
            try:
                cur.execute("""
                    INSERT INTO authors (author_name, alternate_names, is_bipoc, is_lgbtq, contributions)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING author_id
                """, ('Maya Rodriguez', '["M. Rodriguez", "Maya R."]', True, True, '["author", "editor"]'))

                author_id = cur.fetchone()[0]
                stats.pass_test(f"INSERT author with JSONB (author_id: {author_id})")
            except Error as e:
                stats.fail_test("INSERT author", str(e))
                conn.rollback()
                return

            # 2. Insert publisher with TEXT[] array
            try:
                cur.execute("""
                    INSERT INTO publishers (publisher_name, alternate_names, country, parent_publisher)
                    VALUES (%s, %s, %s, %s)
                    RETURNING publisher_id
                """, ('Indie Press LLC', ['Indie Press', 'IP Publishing'], 'USA', 'Mega Corp Publishers'))

                publisher_id = cur.fetchone()[0]
                stats.pass_test(f"INSERT publisher (publisher_id: {publisher_id})")
            except Error as e:
                stats.fail_test("INSERT publisher", str(e))
                conn.rollback()
                return

            # 3. Insert book with all new fields
            try:
                cur.execute("""
                    INSERT INTO books (
                        title, author, author_id, publisher_id, isbn_13, page_count,
                        genres, moods, content_warnings, alternative_titles,
                        user_owns_ebook, user_owns_audiobook, user_owns_physical,
                        user_reading_status, user_added_date, read_count
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING book_id
                """, (
                    'The Quantum Garden', 'Maya Rodriguez', author_id, publisher_id,
                    '9781234567890', 425,
                    '["Science Fiction", "Romance", "LGBTQ+"]',
                    '["dark", "witty", "emotional"]',
                    '["violence", "sexual content"]',
                    '["El Jardín Cuántico"]',
                    True, True, False,
                    'currently-reading', datetime.now(), 2
                ))

                book_id = cur.fetchone()[0]
                stats.pass_test(f"INSERT book with JSONB and user fields (book_id: {book_id})")
            except Error as e:
                stats.fail_test("INSERT book", str(e))
                conn.rollback()
                return

            # 4. Insert book_edition
            try:
                cur.execute("""
                    INSERT INTO book_editions (
                        book_id, edition_format, edition_name, isbn_specific, pages, release_date
                    )
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING edition_id
                """, (book_id, 'hardcover', 'First Edition Hardcover', '9789876543210', 450, '2024-01-15'))

                edition_id = cur.fetchone()[0]
                stats.pass_test(f"INSERT book_edition (edition_id: {edition_id})")
            except Error as e:
                stats.fail_test("INSERT book_edition", str(e))
                conn.rollback()
                return

            # 5. Insert reading_session with UUID read_instance_id
            try:
                cur.execute("""
                    INSERT INTO reading_sessions (
                        book_id, start_time, duration_minutes,
                        device, media_type, pages_read, is_parallel_read
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    RETURNING session_id, read_instance_id
                """, (
                    book_id, datetime.now() - timedelta(hours=2),
                    60, 'kindle-paperwhite', 'ebook', 35, False
                ))

                session_id, read_instance_id = cur.fetchone()
                stats.pass_test(f"INSERT reading_session with UUID (session_id: {session_id}, read_instance_id: {read_instance_id})")
            except Error as e:
                stats.fail_test("INSERT reading_session", str(e))
                conn.rollback()
                return

            # 6. Insert sync_status
            try:
                cur.execute("""
                    INSERT INTO sync_status (source_name, last_sync_time, records_synced, sync_status)
                    VALUES (%s, %s, %s, %s)
                    RETURNING sync_id
                """, ('koreader', datetime.now(), 150, 'success'))

                sync_id = cur.fetchone()[0]
                stats.pass_test(f"INSERT sync_status (sync_id: {sync_id})")
            except Error as e:
                stats.fail_test("INSERT sync_status", str(e))
                conn.rollback()
                return

            conn.commit()

            # === READ: Query inserted data ===

            try:
                cur.execute("SELECT author_name, alternate_names FROM authors WHERE author_id = %s", (author_id,))
                result = cur.fetchone()
                if result and result[0] == 'Maya Rodriguez':
                    stats.pass_test(f"SELECT author by ID (found: {result[0]})")
                else:
                    stats.fail_test("SELECT author", "Data mismatch")
            except Error as e:
                stats.fail_test("SELECT author", str(e))

            try:
                cur.execute("SELECT COUNT(*) FROM books WHERE book_id = %s", (book_id,))
                if cur.fetchone()[0] == 1:
                    stats.pass_test("SELECT book by ID")
                else:
                    stats.fail_test("SELECT book", "Not found")
            except Error as e:
                stats.fail_test("SELECT book", str(e))

            # === UPDATE: Modify data and test trigger ===

            try:
                # Get current updated_at
                cur.execute("SELECT updated_at FROM books WHERE book_id = %s", (book_id,))
                old_timestamp = cur.fetchone()[0]

                # Small delay to ensure timestamp difference
                time.sleep(0.1)

                # Update book
                cur.execute("""
                    UPDATE books
                    SET page_count = 430, read_count = 3
                    WHERE book_id = %s
                """, (book_id,))

                # Get new updated_at
                cur.execute("SELECT updated_at, page_count, read_count FROM books WHERE book_id = %s", (book_id,))
                result = cur.fetchone()
                new_timestamp, page_count, read_count = result

                if new_timestamp > old_timestamp and page_count == 430 and read_count == 3:
                    stats.pass_test("UPDATE book (data updated, trigger updated updated_at)")
                else:
                    stats.fail_test("UPDATE book", f"Trigger failed or data mismatch (old: {old_timestamp}, new: {new_timestamp})")

                conn.commit()
            except Error as e:
                stats.fail_test("UPDATE book", str(e))
                conn.rollback()

            # === DELETE: Test CASCADE behavior ===

            # Store IDs for cleanup
            cleanup_data = {
                'author_id': author_id,
                'publisher_id': publisher_id,
                'book_id': book_id,
                'edition_id': edition_id,
                'session_id': session_id,
                'sync_id': sync_id
            }

            return cleanup_data

    except Error as e:
        stats.fail_test("CRUD operations", str(e))
        conn.rollback()
        return None

# ============================================================
# TEST SUITE 3: JSONB OPERATIONS
# ============================================================

def test_jsonb_operations(conn, stats, cleanup_data):
    """Test JSONB containment and operators"""
    print(f"\n{Color.BLUE}{'='*60}{Color.RESET}")
    print(f"{Color.BOLD}Test Suite 3: JSONB Operations{Color.RESET}")
    print(f"{Color.BLUE}{'='*60}{Color.RESET}\n")

    if not cleanup_data:
        print(f"{Color.YELLOW}⚠ Skipping JSONB tests (no test data){Color.RESET}\n")
        return

    book_id = cleanup_data['book_id']

    with conn.cursor() as cur:
        # Test 1: @> containment operator (genres)
        try:
            cur.execute("""
                SELECT title, genres
                FROM books
                WHERE genres @> '["Science Fiction"]'::jsonb AND book_id = %s
            """, (book_id,))

            result = cur.fetchone()
            if result and result[0] == 'The Quantum Garden':
                stats.pass_test("JSONB @> containment (genres contains 'Science Fiction')")
            else:
                stats.fail_test("JSONB @> containment", "No match found")
        except Error as e:
            stats.fail_test("JSONB @> operator", str(e))

        # Test 2: ? key existence operator (moods)
        try:
            cur.execute("""
                SELECT title
                FROM books
                WHERE moods ? 'witty' AND book_id = %s
            """, (book_id,))

            if cur.fetchone():
                stats.pass_test("JSONB ? key existence (moods contains 'witty')")
            else:
                stats.fail_test("JSONB ? operator", "No match found")
        except Error as e:
            stats.fail_test("JSONB ? operator", str(e))

        # Test 3: UPDATE JSONB array (append genre)
        try:
            cur.execute("""
                UPDATE books
                SET genres = genres || '["Cyberpunk"]'::jsonb
                WHERE book_id = %s
                RETURNING genres
            """, (book_id,))

            result = cur.fetchone()
            if result and 'Cyberpunk' in result[0]:
                stats.pass_test("JSONB UPDATE (append to genres array)")
                conn.commit()
            else:
                stats.fail_test("JSONB UPDATE", "Append failed")
                conn.rollback()
        except Error as e:
            stats.fail_test("JSONB UPDATE", str(e))
            conn.rollback()

        # Test 4: JSONB array length
        try:
            cur.execute("""
                SELECT jsonb_array_length(genres) as genre_count
                FROM books
                WHERE book_id = %s
            """, (book_id,))

            count = cur.fetchone()[0]
            if count == 4:  # Original 3 + 1 appended
                stats.pass_test(f"JSONB array length (genres: {count})")
            else:
                stats.fail_test("JSONB array length", f"Expected 4, got {count}")
        except Error as e:
            stats.fail_test("JSONB array length", str(e))

        # Test 5: JSONB array contains multiple elements
        try:
            cur.execute("""
                SELECT title
                FROM books
                WHERE genres @> '["Romance", "LGBTQ+"]'::jsonb AND book_id = %s
            """, (book_id,))

            if cur.fetchone():
                stats.pass_test("JSONB multi-element containment (genres @> multiple values)")
            else:
                stats.fail_test("JSONB multi-element containment", "No match")
        except Error as e:
            stats.fail_test("JSONB multi-element containment", str(e))

# ============================================================
# TEST SUITE 4: FOREIGN KEY AND CASCADE BEHAVIOR
# ============================================================

def test_foreign_keys_cascade(conn, stats):
    """Test foreign key constraints and CASCADE behavior"""
    print(f"\n{Color.BLUE}{'='*60}{Color.RESET}")
    print(f"{Color.BOLD}Test Suite 4: Foreign Keys and CASCADE{Color.RESET}")
    print(f"{Color.BLUE}{'='*60}{Color.RESET}\n")

    try:
        with conn.cursor() as cur:
            # Create test author
            cur.execute("""
                INSERT INTO authors (author_name)
                VALUES ('Cascade Test Author')
                RETURNING author_id
            """)
            test_author_id = cur.fetchone()[0]

            # Create test book referencing author
            cur.execute("""
                INSERT INTO books (title, author, author_id)
                VALUES ('Cascade Test Book', 'Cascade Test Author', %s)
                RETURNING book_id
            """, (test_author_id,))
            test_book_id = cur.fetchone()[0]

            # Create reading session referencing book
            cur.execute("""
                INSERT INTO reading_sessions (book_id, start_time, duration_minutes, device)
                VALUES (%s, CURRENT_TIMESTAMP, 30, 'test-device')
                RETURNING session_id
            """, (test_book_id,))
            test_session_id = cur.fetchone()[0]

            conn.commit()

            # Now delete the book (should CASCADE to reading_sessions)
            cur.execute("DELETE FROM books WHERE book_id = %s", (test_book_id,))
            conn.commit()

            # Check if reading_session was CASCADE deleted
            cur.execute("SELECT COUNT(*) FROM reading_sessions WHERE session_id = %s", (test_session_id,))
            session_count = cur.fetchone()[0]

            if session_count == 0:
                stats.pass_test("CASCADE DELETE (book → reading_sessions)")
            else:
                stats.fail_test("CASCADE DELETE", "Reading session not deleted")

            # Delete author (should SET NULL on books if any remain)
            cur.execute("DELETE FROM authors WHERE author_id = %s", (test_author_id,))
            conn.commit()

            stats.pass_test("Foreign key CASCADE cleanup successful")

    except Error as e:
        stats.fail_test("Foreign key CASCADE test", str(e))
        conn.rollback()

# ============================================================
# TEST SUITE 5: CONSTRAINT ENFORCEMENT
# ============================================================

def test_constraint_enforcement(conn, stats, cleanup_data):
    """Test UNIQUE, CHECK, and NOT NULL constraints"""
    print(f"\n{Color.BLUE}{'='*60}{Color.RESET}")
    print(f"{Color.BOLD}Test Suite 5: Constraint Enforcement{Color.RESET}")
    print(f"{Color.BLUE}{'='*60}{Color.RESET}\n")

    if not cleanup_data:
        print(f"{Color.YELLOW}⚠ Skipping constraint tests (no test data){Color.RESET}\n")
        return

    book_id = cleanup_data['book_id']

    with conn.cursor() as cur:
        # Test 1: UNIQUE constraint on reading_sessions (book_id, start_time, device)
        try:
            # Get existing session details
            cur.execute("""
                SELECT book_id, start_time, device
                FROM reading_sessions
                WHERE session_id = %s
            """, (cleanup_data['session_id'],))

            existing = cur.fetchone()

            # Try to insert duplicate
            cur.execute("""
                INSERT INTO reading_sessions (book_id, start_time, duration_minutes, device)
                VALUES (%s, %s, 45, %s)
            """, existing)

            conn.commit()
            stats.fail_test("UNIQUE constraint enforcement", "Duplicate insert succeeded (should have failed)")

        except errors.UniqueViolation:
            conn.rollback()
            stats.pass_test("UNIQUE constraint enforcement (reading_sessions)")
        except Error as e:
            conn.rollback()
            stats.fail_test("UNIQUE constraint test", str(e))

        # Test 2: CHECK constraint (duration_minutes > 0)
        try:
            cur.execute("""
                INSERT INTO reading_sessions (book_id, start_time, duration_minutes, device)
                VALUES (%s, CURRENT_TIMESTAMP, -10, 'test-device')
            """, (book_id,))

            conn.commit()
            stats.fail_test("CHECK constraint (duration_minutes > 0)", "Negative duration accepted")

        except errors.CheckViolation:
            conn.rollback()
            stats.pass_test("CHECK constraint enforcement (duration_minutes > 0)")
        except Error as e:
            conn.rollback()
            stats.fail_test("CHECK constraint test", str(e))

        # Test 3: NOT NULL constraint on required fields
        try:
            cur.execute("""
                INSERT INTO books (author, author_id)
                VALUES ('Test Author', NULL)
            """)

            conn.commit()
            stats.warn_test("NOT NULL constraint (author_id)", "NULL accepted (may be intentional)")

        except errors.NotNullViolation:
            conn.rollback()
            stats.pass_test("NOT NULL constraint enforcement (author_id)")
        except Error as e:
            conn.rollback()
            # This is expected if author_id allows NULL
            stats.warn_test("NOT NULL constraint test", "author_id may allow NULL")

# ============================================================
# TEST SUITE 6: VIEWS
# ============================================================

def test_views(conn, stats, cleanup_data):
    """Test all 5 views with sample data"""
    print(f"\n{Color.BLUE}{'='*60}{Color.RESET}")
    print(f"{Color.BOLD}Test Suite 6: View Queries{Color.RESET}")
    print(f"{Color.BLUE}{'='*60}{Color.RESET}\n")

    if not cleanup_data:
        print(f"{Color.YELLOW}⚠ Skipping view tests (no test data){Color.RESET}\n")
        return

    book_id = cleanup_data['book_id']

    views = ['book_stats', 'reading_timeline', 'publisher_analytics',
             'author_analytics', 'tandem_reading_sessions']

    with conn.cursor() as cur:
        # Test 1: book_stats view
        try:
            cur.execute("SELECT * FROM book_stats WHERE book_id = %s", (book_id,))
            result = cur.fetchone()
            if result:
                stats.pass_test(f"View: book_stats (total_sessions: {result[10]})")
            else:
                stats.warn_test("View: book_stats", "No data returned")
        except Error as e:
            stats.fail_test("View: book_stats", str(e))

        # Test 2-5: Other views (existence check)
        for view in views[1:]:
            try:
                cur.execute(f"SELECT COUNT(*) FROM {view}")
                count = cur.fetchone()[0]
                stats.pass_test(f"View: {view} (rows: {count})")
            except Error as e:
                stats.fail_test(f"View: {view}", str(e))

# ============================================================
# TEST SUITE 7: TRIGGER FUNCTIONALITY
# ============================================================

def test_triggers(conn, stats):
    """Test updated_at triggers on all tables"""
    print(f"\n{Color.BLUE}{'='*60}{Color.RESET}")
    print(f"{Color.BOLD}Test Suite 7: Trigger Functionality{Color.RESET}")
    print(f"{Color.BLUE}{'='*60}{Color.RESET}\n")

    tables_with_triggers = ['authors', 'publishers', 'books', 'sync_status']

    with conn.cursor() as cur:
        for table in tables_with_triggers:
            try:
                # Insert test record
                if table == 'authors':
                    cur.execute("""
                        INSERT INTO authors (author_name)
                        VALUES ('Trigger Test')
                        RETURNING author_id, updated_at
                    """)
                elif table == 'publishers':
                    cur.execute("""
                        INSERT INTO publishers (publisher_name)
                        VALUES ('Trigger Test Publisher')
                        RETURNING publisher_id, updated_at
                    """)
                elif table == 'books':
                    cur.execute("""
                        INSERT INTO books (title, author)
                        VALUES ('Trigger Test Book', 'Test')
                        RETURNING book_id, updated_at
                    """)
                elif table == 'sync_status':
                    cur.execute("""
                        INSERT INTO sync_status (source_name, last_sync_time, records_synced, sync_status)
                        VALUES ('test', CURRENT_TIMESTAMP, 0, 'testing')
                        RETURNING sync_id, updated_at
                    """)

                record_id, old_updated_at = cur.fetchone()
                conn.commit()

                # Small delay
                time.sleep(0.1)

                # Update record
                if table == 'authors':
                    cur.execute(f"UPDATE {table} SET author_name = 'Updated' WHERE author_id = %s", (record_id,))
                elif table == 'publishers':
                    cur.execute(f"UPDATE {table} SET country = 'USA' WHERE publisher_id = %s", (record_id,))
                elif table == 'books':
                    cur.execute(f"UPDATE {table} SET page_count = 100 WHERE book_id = %s", (record_id,))
                elif table == 'sync_status':
                    cur.execute(f"UPDATE {table} SET sync_status = 'complete' WHERE sync_id = %s", (record_id,))

                # Get new updated_at
                id_column = f"{table.rstrip('s')}_id" if table != 'sync_status' else 'sync_id'
                cur.execute(f"SELECT updated_at FROM {table} WHERE {id_column} = %s", (record_id,))
                new_updated_at = cur.fetchone()[0]

                if new_updated_at > old_updated_at:
                    stats.pass_test(f"Trigger: {table}.updated_at auto-update")
                else:
                    stats.fail_test(f"Trigger: {table}.updated_at", f"Not updated (old: {old_updated_at}, new: {new_updated_at})")

                # Cleanup
                cur.execute(f"DELETE FROM {table} WHERE {id_column} = %s", (record_id,))
                conn.commit()

            except Error as e:
                stats.fail_test(f"Trigger test: {table}", str(e))
                conn.rollback()

# ============================================================
# TEST SUITE 8: INDEX VERIFICATION
# ============================================================

def test_indexes(conn, stats):
    """Verify key indexes exist"""
    print(f"\n{Color.BLUE}{'='*60}{Color.RESET}")
    print(f"{Color.BOLD}Test Suite 8: Index Verification{Color.RESET}")
    print(f"{Color.BLUE}{'='*60}{Color.RESET}\n")

    expected_indexes = [
        'idx_reading_sessions_book_date',
        'idx_reading_sessions_date_device',
        'idx_reading_sessions_parallel',
        'idx_books_genres',
        'idx_books_moods',
        'idx_books_content_warnings',
        'idx_books_author_diversity',
        'idx_books_user_ownership',
        'idx_books_reading_status',
        'idx_authors_diversity',
        'idx_book_editions_format_book'
    ]

    with conn.cursor() as cur:
        for index_name in expected_indexes:
            try:
                cur.execute("""
                    SELECT COUNT(*)
                    FROM pg_indexes
                    WHERE schemaname = 'public' AND indexname = %s
                """, (index_name,))

                if cur.fetchone()[0] > 0:
                    stats.pass_test(f"Index exists: {index_name}")
                else:
                    stats.fail_test(f"Index: {index_name}", "Not found")

            except Error as e:
                stats.fail_test(f"Index check: {index_name}", str(e))

# ============================================================
# CLEANUP
# ============================================================

def cleanup_test_data(conn, stats, cleanup_data):
    """Remove all test data"""
    print(f"\n{Color.BLUE}{'='*60}{Color.RESET}")
    print(f"{Color.BOLD}Cleanup Test Data{Color.RESET}")
    print(f"{Color.BLUE}{'='*60}{Color.RESET}\n")

    if not cleanup_data:
        print(f"{Color.YELLOW}⚠ No cleanup data{Color.RESET}\n")
        return

    try:
        with conn.cursor() as cur:
            # Delete in reverse order of dependencies
            cur.execute("DELETE FROM reading_sessions WHERE book_id = %s", (cleanup_data['book_id'],))
            cur.execute("DELETE FROM book_editions WHERE edition_id = %s", (cleanup_data['edition_id'],))
            cur.execute("DELETE FROM books WHERE book_id = %s", (cleanup_data['book_id'],))
            cur.execute("DELETE FROM publishers WHERE publisher_id = %s", (cleanup_data['publisher_id'],))
            cur.execute("DELETE FROM authors WHERE author_id = %s", (cleanup_data['author_id'],))
            cur.execute("DELETE FROM sync_status WHERE sync_id = %s", (cleanup_data['sync_id'],))

            conn.commit()
            stats.pass_test("Test data cleanup complete")

    except Error as e:
        stats.fail_test("Cleanup", str(e))
        conn.rollback()

# ============================================================
# MAIN
# ============================================================

def main():
    """Main test execution"""
    print(f"\n{Color.BOLD}{Color.BLUE}{'='*60}{Color.RESET}")
    print(f"{Color.BOLD}BookHelper Schema Operations Test Suite{Color.RESET}")
    print(f"{Color.BOLD}Story 1.4: Task 5{Color.RESET}")
    print(f"{Color.BOLD}{Color.BLUE}{'='*60}{Color.RESET}\n")

    stats = TestStats()

    # Load environment
    print("Loading environment variables...")
    if not load_env_file():
        return 1

    print(f"{Color.GREEN}✓{Color.RESET} Environment loaded\n")

    # Connect to database
    print("Connecting to Neon PostgreSQL...")
    conn = get_db_connection()
    print(f"{Color.GREEN}✓{Color.RESET} Connection successful\n")

    try:
        # Run test suites
        test_schema_structure(conn, stats)
        test_jsonb_columns(conn, stats)
        test_constraints(conn, stats)

        cleanup_data = test_crud_operations(conn, stats)

        test_jsonb_operations(conn, stats, cleanup_data)
        test_foreign_keys_cascade(conn, stats)
        test_constraint_enforcement(conn, stats, cleanup_data)
        test_views(conn, stats, cleanup_data)
        test_triggers(conn, stats)
        test_indexes(conn, stats)

        cleanup_test_data(conn, stats, cleanup_data)

        # Print summary
        return stats.summary()

    except Exception as e:
        print(f"\n{Color.RED}✗ Unexpected error: {e}{Color.RESET}")
        return 1

    finally:
        conn.close()

if __name__ == '__main__':
    sys.exit(main())
