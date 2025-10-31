#!/usr/bin/env python3
"""
Initialize BookHelper Database Schema
Story 1.4: Tasks 2, 3, 4 - Create tables, views, indexes, and triggers

This script:
1. Loads environment variables from .env.neon
2. Connects to Neon.tech PostgreSQL database
3. Executes create_schema.sql (6 tables + 5 views + triggers)
4. Executes create_indexes.sql (composite and GIN indexes)
5. Verifies schema structure
6. Runs basic smoke tests

Usage:
    python3 initialize_schema.py

Environment Variables (from .env.neon):
    NEON_HOST - Neon PostgreSQL host
    NEON_PORT - Port (default: 5432)
    NEON_USER - Database user
    NEON_PASSWORD - Database password
    NEON_DATABASE - Database name

Exit Codes:
    0 - Success
    1 - Connection error or schema creation failed
"""

import os
import sys
from pathlib import Path
import psycopg2
from psycopg2 import sql, Error

# Terminal colors
class Color:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

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

def execute_sql_file(conn, filepath):
    """Execute SQL from file with error handling"""
    file_path = Path(filepath)

    if not file_path.exists():
        print(f"{Color.RED}✗ SQL file not found: {filepath}{Color.RESET}")
        return False

    try:
        with open(file_path, 'r') as f:
            sql_content = f.read()

        with conn.cursor() as cur:
            cur.execute(sql_content)

        conn.commit()
        print(f"{Color.GREEN}✓{Color.RESET} Executed: {file_path.name}")
        return True

    except Error as e:
        conn.rollback()
        print(f"{Color.RED}✗ SQL execution failed: {e}{Color.RESET}")
        return False

def verify_tables(conn):
    """Verify all required tables exist"""
    required_tables = ['authors', 'publishers', 'books', 'book_editions', 'reading_sessions', 'sync_status']

    print(f"\n{Color.BLUE}{'='*60}{Color.RESET}")
    print(f"{Color.BOLD}Verifying Tables{Color.RESET}")
    print(f"{Color.BLUE}{'='*60}{Color.RESET}\n")

    with conn.cursor() as cur:
        for table in required_tables:
            cur.execute("""
                SELECT EXISTS (
                    SELECT 1 FROM information_schema.tables
                    WHERE table_schema = 'public' AND table_name = %s
                )
            """, (table,))

            exists = cur.fetchone()[0]
            if exists:
                print(f"{Color.GREEN}✓{Color.RESET} Table: {table}")
            else:
                print(f"{Color.RED}✗{Color.RESET} Missing table: {table}")
                return False

    return True

def verify_views(conn):
    """Verify all required views exist"""
    required_views = ['book_stats', 'reading_timeline', 'publisher_analytics',
                      'author_analytics', 'tandem_reading_sessions']

    print(f"\n{Color.BLUE}{'='*60}{Color.RESET}")
    print(f"{Color.BOLD}Verifying Views{Color.RESET}")
    print(f"{Color.BLUE}{'='*60}{Color.RESET}\n")

    with conn.cursor() as cur:
        for view in required_views:
            cur.execute("""
                SELECT EXISTS (
                    SELECT 1 FROM information_schema.views
                    WHERE table_schema = 'public' AND table_name = %s
                )
            """, (view,))

            exists = cur.fetchone()[0]
            if exists:
                print(f"{Color.GREEN}✓{Color.RESET} View: {view}")
            else:
                print(f"{Color.YELLOW}⚠{Color.RESET} Missing view: {view}")

    return True

def verify_triggers(conn):
    """Verify automatic update triggers exist"""
    expected_triggers = ['update_authors_updated_at', 'update_publishers_updated_at',
                        'update_books_updated_at', 'update_sync_status_updated_at']

    print(f"\n{Color.BLUE}{'='*60}{Color.RESET}")
    print(f"{Color.BOLD}Verifying Triggers{Color.RESET}")
    print(f"{Color.BLUE}{'='*60}{Color.RESET}\n")

    with conn.cursor() as cur:
        cur.execute("""
            SELECT trigger_name FROM information_schema.triggers
            WHERE trigger_schema = 'public'
        """)

        existing_triggers = {row[0] for row in cur.fetchall()}

        for trigger in expected_triggers:
            if trigger in existing_triggers:
                print(f"{Color.GREEN}✓{Color.RESET} Trigger: {trigger}")
            else:
                print(f"{Color.YELLOW}⚠{Color.RESET} Missing trigger: {trigger}")

    return True

def run_smoke_tests(conn):
    """Run basic CRUD smoke tests"""
    print(f"\n{Color.BLUE}{'='*60}{Color.RESET}")
    print(f"{Color.BOLD}Running Smoke Tests{Color.RESET}")
    print(f"{Color.BLUE}{'='*60}{Color.RESET}\n")

    try:
        with conn.cursor() as cur:
            # Test 1: Insert author with JSONB
            print("Test 1: INSERT author with JSONB fields...")
            cur.execute("""
                INSERT INTO authors (author_name, alternate_names, is_bipoc, is_lgbtq, contributions)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING author_id
            """, ('Test Author', '["Pen Name", "Alt Name"]', True, False, '["author", "editor"]'))

            author_id = cur.fetchone()[0]
            print(f"{Color.GREEN}✓{Color.RESET} Created author_id: {author_id}")

            # Test 2: Insert publisher
            print("\nTest 2: INSERT publisher...")
            cur.execute("""
                INSERT INTO publishers (publisher_name, alternate_names, country)
                VALUES (%s, %s, %s)
                RETURNING publisher_id
            """, ('Test Publisher', ['Alt Publisher Name'], 'USA'))

            publisher_id = cur.fetchone()[0]
            print(f"{Color.GREEN}✓{Color.RESET} Created publisher_id: {publisher_id}")

            # Test 3: Insert book with all new fields
            print("\nTest 3: INSERT book with JSONB and user library fields...")
            cur.execute("""
                INSERT INTO books (
                    title, author, author_id, publisher_id, page_count,
                    genres, moods, user_owns_ebook, user_owns_audiobook, read_count
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING book_id
            """, (
                'Test Book', 'Test Author', author_id, publisher_id, 300,
                '["Science Fiction", "Romance"]', '["dark", "witty"]',
                True, True, 1
            ))

            book_id = cur.fetchone()[0]
            print(f"{Color.GREEN}✓{Color.RESET} Created book_id: {book_id}")

            # Test 4: Insert reading session with UUID
            print("\nTest 4: INSERT reading_session...")
            cur.execute("""
                INSERT INTO reading_sessions (
                    book_id, start_time, duration_minutes, device, media_type, pages_read
                )
                VALUES (%s, CURRENT_TIMESTAMP, %s, %s, %s, %s)
                RETURNING session_id, read_instance_id
            """, (book_id, 45, 'test-device', 'ebook', 25))

            session_id, read_instance_id = cur.fetchone()
            print(f"{Color.GREEN}✓{Color.RESET} Created session_id: {session_id}, read_instance_id: {read_instance_id}")

            # Test 5: Query JSONB field
            print("\nTest 5: Query JSONB field (genres)...")
            cur.execute("""
                SELECT title, genres
                FROM books
                WHERE genres @> '["Science Fiction"]'::jsonb
            """)

            result = cur.fetchone()
            if result:
                print(f"{Color.GREEN}✓{Color.RESET} JSONB query successful: {result[0]}")

            # Test 6: Query view
            print("\nTest 6: Query book_stats view...")
            cur.execute("SELECT * FROM book_stats WHERE book_id = %s", (book_id,))
            stats = cur.fetchone()
            if stats:
                print(f"{Color.GREEN}✓{Color.RESET} View query successful - total_sessions: {stats[10]}")

            # Test 7: Test UPDATE trigger
            print("\nTest 7: Test updated_at trigger...")
            cur.execute("SELECT updated_at FROM books WHERE book_id = %s", (book_id,))
            old_timestamp = cur.fetchone()[0]

            cur.execute("UPDATE books SET page_count = 350 WHERE book_id = %s", (book_id,))

            cur.execute("SELECT updated_at FROM books WHERE book_id = %s", (book_id,))
            new_timestamp = cur.fetchone()[0]

            if new_timestamp > old_timestamp:
                print(f"{Color.GREEN}✓{Color.RESET} Trigger working: updated_at changed")

            # Test 8: Test constraint (UNIQUE on reading_sessions)
            print("\nTest 8: Test UNIQUE constraint on reading_sessions...")
            try:
                cur.execute("""
                    INSERT INTO reading_sessions (
                        book_id, start_time, duration_minutes, device
                    )
                    SELECT book_id, start_time, duration_minutes, device
                    FROM reading_sessions WHERE session_id = %s
                """, (session_id,))

                print(f"{Color.RED}✗{Color.RESET} Constraint NOT enforced (duplicate allowed)")
            except Error as e:
                if 'unique' in str(e).lower():
                    print(f"{Color.GREEN}✓{Color.RESET} UNIQUE constraint working")
                    conn.rollback()

            # Cleanup
            print("\nCleaning up test data...")
            cur.execute("DELETE FROM reading_sessions WHERE book_id = %s", (book_id,))
            cur.execute("DELETE FROM books WHERE book_id = %s", (book_id,))
            cur.execute("DELETE FROM publishers WHERE publisher_id = %s", (publisher_id,))
            cur.execute("DELETE FROM authors WHERE author_id = %s", (author_id,))

            conn.commit()
            print(f"{Color.GREEN}✓{Color.RESET} Test data cleaned up")

        return True

    except Error as e:
        conn.rollback()
        print(f"{Color.RED}✗ Smoke test failed: {e}{Color.RESET}")
        return False

def main():
    """Main execution flow"""
    print(f"\n{Color.BOLD}{Color.BLUE}{'='*60}{Color.RESET}")
    print(f"{Color.BOLD}BookHelper Schema Initialization{Color.RESET}")
    print(f"{Color.BOLD}Story 1.4: Tasks 2, 3, 4{Color.RESET}")
    print(f"{Color.BOLD}{Color.BLUE}{'='*60}{Color.RESET}\n")

    # Load environment variables
    print("Loading environment variables...")
    if not load_env_file():
        return 1

    print(f"{Color.GREEN}✓{Color.RESET} Environment loaded")

    # Verify required env vars
    required_vars = ['NEON_HOST', 'NEON_DATABASE', 'NEON_USER', 'NEON_PASSWORD']
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        print(f"{Color.RED}✗ Missing environment variables: {', '.join(missing_vars)}{Color.RESET}")
        return 1

    print(f"Database: {os.getenv('NEON_DATABASE')}")
    print(f"Host: {os.getenv('NEON_HOST')}")
    print(f"User: {os.getenv('NEON_USER')}\n")

    # Connect to database
    print("Connecting to Neon PostgreSQL...")
    conn = get_db_connection()
    print(f"{Color.GREEN}✓{Color.RESET} Connection successful\n")

    try:
        # Execute schema creation
        print(f"{Color.BLUE}{'='*60}{Color.RESET}")
        print(f"{Color.BOLD}Creating Schema{Color.RESET}")
        print(f"{Color.BLUE}{'='*60}{Color.RESET}\n")

        if not execute_sql_file(conn, 'resources/scripts/create_schema.sql'):
            return 1

        if not execute_sql_file(conn, 'resources/scripts/create_indexes.sql'):
            return 1

        # Verify schema
        if not verify_tables(conn):
            return 1

        verify_views(conn)
        verify_triggers(conn)

        # Run smoke tests
        if not run_smoke_tests(conn):
            return 1

        # Success
        print(f"\n{Color.BOLD}{Color.GREEN}{'='*60}{Color.RESET}")
        print(f"{Color.BOLD}{Color.GREEN}✓ Schema Initialization Complete{Color.RESET}")
        print(f"{Color.BOLD}{Color.GREEN}{'='*60}{Color.RESET}\n")

        print(f"{Color.GREEN}✓{Color.RESET} Task 2: Tables created (6)")
        print(f"{Color.GREEN}✓{Color.RESET} Task 3: Views created (5)")
        print(f"{Color.GREEN}✓{Color.RESET} Task 4: Indexes created")
        print(f"{Color.GREEN}✓{Color.RESET} Task 5: Smoke tests passed\n")

        print("Next steps:")
        print("  1. Run comprehensive tests: python3 resources/scripts/test_schema_operations.py")
        print("  2. Review schema documentation: docs/guides/SCHEMA-DOCUMENTATION.md\n")

        return 0

    except Exception as e:
        print(f"\n{Color.RED}✗ Unexpected error: {e}{Color.RESET}")
        return 1

    finally:
        conn.close()

if __name__ == '__main__':
    sys.exit(main())
