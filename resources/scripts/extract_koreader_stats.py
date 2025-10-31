#!/usr/bin/env python3
"""
ETL Pipeline: Extract KOReader Statistics and Load into Neon.tech PostgreSQL

Story 3.2: Build ETL pipeline for statistics extraction

This script:
1. Reads statistics.sqlite3 from KOReader backup (via Syncthing on RPi)
2. Extracts books and aggregates reading sessions with 30-minute gap threshold
3. Transforms data to match Neon.tech schema (books + reading_sessions tables)
4. Handles duplicate detection via ON CONFLICT clause
5. Loads data into Neon.tech PostgreSQL database
6. Logs all operations with timestamps and record counts

Usage:
    python3 extract_koreader_stats.py [--dry-run]

Environment Variables (required):
    NEON_HOST: Neon.tech PostgreSQL hostname
    NEON_USER: Neon.tech database username
    NEON_PASSWORD: Neon.tech database password
    NEON_DATABASE: Neon.tech database name

Optional:
    KOREADER_BACKUP: Path to statistics.sqlite3 (default: /home/alexhouse/backups/koreader-statistics/statistics.sqlite3)
    ETL_LOG_PATH: Path for log file (default: /home/alexhouse/logs/etl.log)
    DEVICE_ID: Device identifier (default: boox-palma-2)
    SESSION_GAP_MINUTES: Gap threshold for session aggregation (default: 30)
"""

import sqlite3
import psycopg2
from psycopg2.extras import execute_values
import logging
import sys
import os
from datetime import datetime, timezone
from pathlib import Path
import argparse
from uuid import uuid4
from typing import List, Dict, Tuple, Optional
import json


# ============================================================================
# Configuration
# ============================================================================

class Config:
    """ETL Configuration from environment variables"""

    NEON_HOST = os.getenv('NEON_HOST')
    NEON_USER = os.getenv('NEON_USER')
    NEON_PASSWORD = os.getenv('NEON_PASSWORD')
    NEON_DATABASE = os.getenv('NEON_DATABASE')

    KOREADER_BACKUP = os.getenv(
        'KOREADER_BACKUP',
        '/home/alexhouse/backups/koreader-statistics/statistics.sqlite3'
    )
    ETL_LOG_PATH = os.getenv(
        'ETL_LOG_PATH',
        '/home/alexhouse/logs/etl.log'
    )
    DEVICE_ID = os.getenv('DEVICE_ID', 'boox-palma-2')
    SESSION_GAP_MINUTES = int(os.getenv('SESSION_GAP_MINUTES', '30'))

    @classmethod
    def validate(cls) -> bool:
        """Validate required configuration"""
        required = ['NEON_HOST', 'NEON_USER', 'NEON_PASSWORD', 'NEON_DATABASE']
        missing = [var for var in required if not getattr(cls, var)]
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
        return True


# ============================================================================
# Logging Setup
# ============================================================================

def setup_logging(log_path: str, dry_run: bool = False) -> logging.Logger:
    """Configure structured logging with file and console handlers"""

    # Ensure log directory exists
    Path(log_path).parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger('etl_koreader')
    logger.setLevel(logging.DEBUG)

    # File handler (detailed)
    file_handler = logging.FileHandler(log_path)
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # Console handler (info and above)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        '[%(levelname)s] %(message)s'
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    return logger


# ============================================================================
# KOReader Statistics Extraction
# ============================================================================

class KOReaderExtractor:
    """Extract data from KOReader statistics.sqlite3"""

    def __init__(self, db_path: str, logger: logging.Logger):
        self.db_path = db_path
        self.logger = logger
        self.conn: Optional[sqlite3.Connection] = None

    def connect(self) -> bool:
        """Open connection to statistics.sqlite3"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
            self.logger.info(f"Connected to KOReader backup: {self.db_path}")
            return True
        except sqlite3.Error as e:
            self.logger.error(f"Failed to connect to KOReader database: {e}")
            return False

    def disconnect(self):
        """Close connection"""
        if self.conn:
            self.conn.close()
            self.logger.debug("Disconnected from KOReader database")

    def extract_books(self) -> List[Dict]:
        """Extract books from KOReader book table"""
        if not self.conn:
            return []

        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT id, title, authors, pages, language, md5,
                       notes, highlights, series
                FROM book
                ORDER BY id
            """)

            books = [dict(row) for row in cursor.fetchall()]
            self.logger.info(f"Extracted {len(books)} books from KOReader")
            return books

        except sqlite3.Error as e:
            self.logger.error(f"Failed to extract books: {e}")
            return []

    def extract_page_stat_data(self) -> List[Dict]:
        """Extract reading sessions from page_stat_data"""
        if not self.conn:
            return []

        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT id_book, page, start_time, duration, total_pages
                FROM page_stat_data
                ORDER BY id_book, start_time
            """)

            sessions = [dict(row) for row in cursor.fetchall()]
            self.logger.info(f"Extracted {len(sessions)} page_stat_data records from KOReader")
            return sessions

        except sqlite3.Error as e:
            self.logger.error(f"Failed to extract page_stat_data: {e}")
            return []


# ============================================================================
# Session Aggregation
# ============================================================================

class SessionAggregator:
    """Aggregate page_stat_data into reading sessions"""

    def __init__(self, gap_minutes: int, logger: logging.Logger):
        self.gap_minutes = gap_minutes
        self.logger = logger

    def aggregate(self, page_stat_data: List[Dict]) -> List[Dict]:
        """
        Aggregate consecutive page_stat_data rows into reading sessions.

        A new session starts when:
        1. Book ID changes
        2. Time gap > gap_minutes (default 30 minutes)
        """
        sessions = []
        current_session = None

        for record in page_stat_data:
            book_id = record['id_book']
            start_time = record['start_time']
            duration = record['duration']
            page = record['page']

            if current_session is None:
                # Start first session
                current_session = {
                    'id_book': book_id,
                    'session_start_time': start_time,
                    'session_end_time': start_time,
                    'duration_minutes': duration,
                    'pages_read': page
                }
            else:
                # Check if we should continue or start new session
                if book_id != current_session['id_book']:
                    # Different book - save and start new
                    sessions.append(current_session)
                    current_session = {
                        'id_book': book_id,
                        'session_start_time': start_time,
                        'session_end_time': start_time,
                        'duration_minutes': duration,
                        'pages_read': page
                    }
                else:
                    # Same book - check time gap
                    time_gap_minutes = (start_time - current_session['session_end_time']) / 60

                    if time_gap_minutes > self.gap_minutes:
                        # Gap exceeds threshold - save and start new
                        sessions.append(current_session)
                        current_session = {
                            'id_book': book_id,
                            'session_start_time': start_time,
                            'session_end_time': start_time,
                            'duration_minutes': duration,
                            'pages_read': page
                        }
                    else:
                        # Continue current session
                        current_session['session_end_time'] = start_time
                        current_session['duration_minutes'] += duration
                        current_session['pages_read'] = max(
                            current_session['pages_read'], page
                        )

        # Don't forget final session
        if current_session:
            sessions.append(current_session)

        self.logger.info(f"Aggregated {len(page_stat_data)} records into {len(sessions)} sessions")
        return sessions


# ============================================================================
# Data Transformation
# ============================================================================

class DataTransformer:
    """Transform KOReader data to Neon.tech schema"""

    def __init__(self, device_id: str, logger: logging.Logger):
        self.device_id = device_id
        self.logger = logger

    def transform_books(self, koreader_books: List[Dict]) -> List[Dict]:
        """Transform KOReader books to Neon.tech books table schema"""
        books = []

        for book in koreader_books:
            transformed = {
                'title': book['title'],
                'file_hash': book['md5'],
                'page_count': book['pages'],
                'language': book['language'] or 'en',
                'notes': book.get('notes', 0),
                'highlights': book.get('highlights', 0),
                'source': 'koreader',
                'device_stats_source': 'statistics.sqlite3',
                # These will be populated by Hardcover enrichment in a future story
                'author_id': None,
                'publisher_id': None,
                'series_name': self._extract_series_name(book.get('series')),
                'series_number': self._extract_series_number(book.get('series')),
            }
            books.append(transformed)

        self.logger.info(f"Transformed {len(books)} KOReader books to schema")
        return books

    def transform_sessions(
        self,
        aggregated_sessions: List[Dict],
        koreader_books: List[Dict]
    ) -> List[Dict]:
        """Transform aggregated sessions to reading_sessions table schema"""

        # Create book_id lookup by file_hash (KOReader MD5)
        book_id_by_md5 = {book['md5']: book['id'] for book in koreader_books}

        sessions = []
        for session in aggregated_sessions:
            book_id = book_id_by_md5.get(session['id_book'])

            if not book_id:
                self.logger.warning(
                    f"Book ID {session['id_book']} not found in books list - skipping session"
                )
                continue

            transformed = {
                'book_id': book_id,
                'start_time': datetime.fromtimestamp(
                    session['session_start_time'],
                    tz=timezone.utc
                ),
                'duration_minutes': max(1, session['duration_minutes']),  # Ensure > 0
                'pages_read': session['pages_read'],
                'device': self.device_id,
                'media_type': 'ebook',
                'data_source': 'koreader',
                'device_stats_source': 'statistics.sqlite3',
                'read_instance_id': str(uuid4()),
                'read_number': 1,
                'is_parallel_read': False,
            }
            sessions.append(transformed)

        self.logger.info(f"Transformed {len(sessions)} sessions to schema")
        return sessions

    @staticmethod
    def _extract_series_name(series_str: Optional[str]) -> Optional[str]:
        """Extract series name from KOReader series field"""
        if not series_str:
            return None
        # Remove series number if present (e.g., "Hani Khan #2" → "Hani Khan")
        return series_str.split('#')[0].strip()

    @staticmethod
    def _extract_series_number(series_str: Optional[str]) -> Optional[float]:
        """Extract series number from KOReader series field"""
        if not series_str or '#' not in series_str:
            return None
        try:
            return float(series_str.split('#')[1].strip())
        except (ValueError, IndexError):
            return None


# ============================================================================
# Neon.tech Database Operations
# ============================================================================

class NeonLoader:
    """Load transformed data into Neon.tech PostgreSQL"""

    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.conn: Optional[psycopg2.extensions.connection] = None
        self.cursor: Optional[psycopg2.extensions.cursor] = None

    def connect(self, host: str, user: str, password: str, database: str) -> bool:
        """Connect to Neon.tech PostgreSQL"""
        try:
            self.conn = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=database,
                connect_timeout=30
            )
            self.cursor = self.conn.cursor()
            self.logger.info(f"Connected to Neon.tech: {host}/{database}")
            return True
        except psycopg2.Error as e:
            self.logger.error(f"Failed to connect to Neon.tech: {e}")
            return False

    def disconnect(self):
        """Close connection"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            self.logger.debug("Disconnected from Neon.tech")

    def validate_schema(self) -> bool:
        """Validate that required tables exist"""
        required_tables = ['books', 'reading_sessions', 'authors', 'publishers']

        try:
            for table in required_tables:
                self.cursor.execute(
                    "SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = %s)",
                    (table,)
                )
                if not self.cursor.fetchone()[0]:
                    self.logger.error(f"Required table '{table}' not found in Neon.tech")
                    return False

            self.logger.info("Schema validation passed - all required tables exist")
            return True

        except psycopg2.Error as e:
            self.logger.error(f"Schema validation failed: {e}")
            return False

    def load_books(self, books: List[Dict], dry_run: bool = False) -> int:
        """Load books into Neon.tech (with ON CONFLICT for duplicates)"""
        if not books:
            return 0

        try:
            # Build SQL with ON CONFLICT for duplicate handling
            # Note: Deduplication is by file_hash (MD5) which is unique per KOReader book
            sql = """
                INSERT INTO books (
                    title, file_hash, page_count, language, notes, highlights,
                    source, device_stats_source, series_name, series_number
                ) VALUES %s
                ON CONFLICT (file_hash) DO NOTHING
                RETURNING book_id
            """

            values = [
                (
                    book['title'],
                    book['file_hash'],
                    book['page_count'],
                    book['language'],
                    book['notes'],
                    book['highlights'],
                    book['source'],
                    book['device_stats_source'],
                    book['series_name'],
                    book['series_number'],
                )
                for book in books
            ]

            if dry_run:
                self.logger.info(f"[DRY-RUN] Would insert {len(books)} books")
                return len(books)

            self.cursor.execute(sql, (values,))
            inserted = len(self.cursor.fetchall())
            self.conn.commit()
            self.logger.info(f"Inserted {inserted} new books into Neon.tech (duplicates skipped)")
            return inserted

        except psycopg2.Error as e:
            self.conn.rollback()
            self.logger.error(f"Failed to load books: {e}")
            return 0

    def load_reading_sessions(self, sessions: List[Dict], dry_run: bool = False) -> int:
        """Load reading_sessions into Neon.tech (with ON CONFLICT for duplicates)"""
        if not sessions:
            return 0

        try:
            sql = """
                INSERT INTO reading_sessions (
                    book_id, start_time, duration_minutes, pages_read, device,
                    media_type, data_source, device_stats_source,
                    read_instance_id, read_number, is_parallel_read
                ) VALUES %s
                ON CONFLICT (book_id, start_time, device) DO NOTHING
                RETURNING session_id
            """

            values = [
                (
                    session['book_id'],
                    session['start_time'],
                    session['duration_minutes'],
                    session['pages_read'],
                    session['device'],
                    session['media_type'],
                    session['data_source'],
                    session['device_stats_source'],
                    session['read_instance_id'],
                    session['read_number'],
                    session['is_parallel_read'],
                )
                for session in sessions
            ]

            if dry_run:
                self.logger.info(f"[DRY-RUN] Would insert {len(sessions)} reading sessions")
                return len(sessions)

            self.cursor.execute(sql, (values,))
            inserted = len(self.cursor.fetchall())
            self.conn.commit()
            self.logger.info(f"Inserted {inserted} new reading sessions (duplicates skipped)")
            return inserted

        except psycopg2.Error as e:
            self.conn.rollback()
            self.logger.error(f"Failed to load reading_sessions: {e}")
            return 0

    def get_record_counts(self) -> Dict[str, int]:
        """Get current record counts from Neon.tech"""
        try:
            counts = {}
            for table in ['books', 'reading_sessions']:
                self.cursor.execute(f"SELECT COUNT(*) FROM {table}")
                counts[table] = self.cursor.fetchone()[0]
            return counts
        except psycopg2.Error as e:
            self.logger.error(f"Failed to get record counts: {e}")
            return {}


# ============================================================================
# Main ETL Pipeline
# ============================================================================

def run_etl(dry_run: bool = False) -> bool:
    """Execute complete ETL pipeline"""

    # Validate configuration
    try:
        Config.validate()
    except ValueError as e:
        print(f"Configuration Error: {e}")
        return False

    # Setup logging
    logger = setup_logging(Config.ETL_LOG_PATH, dry_run)

    logger.info("=" * 70)
    logger.info("ETL Pipeline: KOReader Statistics → Neon.tech PostgreSQL")
    logger.info("=" * 70)
    logger.info(f"Started at {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
    logger.info(f"Mode: {'DRY-RUN' if dry_run else 'NORMAL'}")
    logger.info(f"Source: {Config.KOREADER_BACKUP}")
    logger.info(f"Target: {Config.NEON_HOST}/{Config.NEON_DATABASE}")
    logger.info(f"Device: {Config.DEVICE_ID}")
    logger.info(f"Session Gap Threshold: {Config.SESSION_GAP_MINUTES} minutes")

    # Step 1: Extract from KOReader
    logger.info("\n[STEP 1] Extracting from KOReader statistics.sqlite3...")
    extractor = KOReaderExtractor(Config.KOREADER_BACKUP, logger)

    if not extractor.connect():
        logger.error("Failed to connect to KOReader database - aborting")
        return False

    koreader_books = extractor.extract_books()
    koreader_sessions = extractor.extract_page_stat_data()
    extractor.disconnect()

    if not koreader_books or not koreader_sessions:
        logger.error("No data extracted from KOReader - aborting")
        return False

    # Step 2: Aggregate sessions
    logger.info("\n[STEP 2] Aggregating reading sessions...")
    aggregator = SessionAggregator(Config.SESSION_GAP_MINUTES, logger)
    aggregated_sessions = aggregator.aggregate(koreader_sessions)

    # Step 3: Transform data
    logger.info("\n[STEP 3] Transforming data to Neon.tech schema...")
    transformer = DataTransformer(Config.DEVICE_ID, logger)
    books = transformer.transform_books(koreader_books)
    sessions = transformer.transform_sessions(aggregated_sessions, koreader_books)

    # Step 4: Connect to Neon.tech
    logger.info("\n[STEP 4] Connecting to Neon.tech...")
    loader = NeonLoader(logger)

    if not loader.connect(
        Config.NEON_HOST,
        Config.NEON_USER,
        Config.NEON_PASSWORD,
        Config.NEON_DATABASE
    ):
        logger.error("Failed to connect to Neon.tech - aborting")
        return False

    # Step 5: Validate schema
    logger.info("\n[STEP 5] Validating Neon.tech schema...")
    if not loader.validate_schema():
        logger.error("Schema validation failed - aborting")
        loader.disconnect()
        return False

    # Get pre-load counts
    counts_before = loader.get_record_counts()
    logger.info(f"Pre-load counts: books={counts_before.get('books', 0)}, "
                f"sessions={counts_before.get('reading_sessions', 0)}")

    # Step 6: Load data
    logger.info("\n[STEP 6] Loading data into Neon.tech...")
    books_inserted = loader.load_books(books, dry_run=dry_run)
    sessions_inserted = loader.load_reading_sessions(sessions, dry_run=dry_run)

    # Get post-load counts
    counts_after = loader.get_record_counts()
    logger.info(f"Post-load counts: books={counts_after.get('books', 0)}, "
                f"sessions={counts_after.get('reading_sessions', 0)}")

    loader.disconnect()

    # Summary
    logger.info("\n" + "=" * 70)
    logger.info("ETL SUMMARY")
    logger.info("=" * 70)
    logger.info(f"KOReader books extracted: {len(koreader_books)}")
    logger.info(f"Page stat data records: {len(koreader_sessions)}")
    logger.info(f"Aggregated sessions: {len(aggregated_sessions)}")
    logger.info(f"Books inserted into Neon.tech: {books_inserted}")
    logger.info(f"Reading sessions inserted: {sessions_inserted}")
    logger.info(f"Completed at {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
    logger.info("=" * 70)

    return True


# ============================================================================
# CLI Entry Point
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Extract KOReader statistics and load into Neon.tech PostgreSQL'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview what would be loaded without writing to database'
    )

    args = parser.parse_args()

    success = run_etl(dry_run=args.dry_run)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
