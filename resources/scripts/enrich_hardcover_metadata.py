#!/usr/bin/env python3
"""
Hardcover API Metadata Enrichment Script
Story 3.3: Integrate Hardcover API metadata and enrich books table

This script queries the Hardcover GraphQL API for the user's personal library
and enriches the Neon.tech books table with complete metadata (author, publisher,
ISBN, rating, cover image). Follows patterns established in Story 3.2 ETL pipeline.

Architecture:
- HardcoverExtractor: Query Hardcover GraphQL API for personal library
- DataTransformer: Map Hardcover fields to Neon.tech schema
- NeonEnricher: Insert/update books, authors, publishers with conflict resolution
- Structured logging with file rotation
- Dry-run mode for safe testing

Author: BookHelper Development Team
Date: 2025-10-31
"""

import os
import sys
import json
import logging
import argparse
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
from dataclasses import dataclass, asdict
import re

try:
    import requests
    import psycopg2
    from psycopg2 import pool
    from psycopg2.extras import execute_values, RealDictCursor
    from dotenv import load_dotenv
    from difflib import SequenceMatcher
except ImportError as e:
    print(f"ERROR: Missing required dependency: {e}")
    print("Install with: pip3 install requests psycopg2-binary python-dotenv")
    sys.exit(1)


# ============================================================================
# Configuration Management
# ============================================================================

@dataclass
class Config:
    """Configuration loaded from environment variables"""
    # Hardcover API
    hardcover_api_key: str
    hardcover_endpoint: str
    hardcover_user_id: Optional[int] = None

    # Neon.tech Database
    neon_host: str
    neon_user: str
    neon_password: str
    neon_database: str
    neon_port: int = 5432

    # Logging
    log_dir: str = "/home/alexhouse/logs"
    log_file: str = "hardcover-enrichment.log"

    # Matching thresholds
    fuzzy_match_threshold: float = 0.85

    @classmethod
    def load_from_env(cls, env_file: str = "/home/alexhouse/.env.hardcover") -> 'Config':
        """Load configuration from environment file"""
        if os.path.exists(env_file):
            load_dotenv(env_file)
            logging.info(f"Loaded configuration from {env_file}")
        else:
            logging.warning(f"Environment file not found: {env_file}, using system environment variables")

        try:
            return cls(
                hardcover_api_key=os.getenv('HARDCOVER_API_KEY', ''),
                hardcover_endpoint=os.getenv('HARDCOVER_ENDPOINT', 'https://api.hardcover.app/v1/graphql'),
                hardcover_user_id=int(os.getenv('HARDCOVER_USER_ID')) if os.getenv('HARDCOVER_USER_ID') else None,
                neon_host=os.getenv('NEON_HOST', ''),
                neon_user=os.getenv('NEON_USER', ''),
                neon_password=os.getenv('NEON_PASSWORD', ''),
                neon_database=os.getenv('NEON_DATABASE', 'neondb'),
                neon_port=int(os.getenv('NEON_PORT', '5432')),
                log_dir=os.getenv('LOG_DIR', '/home/alexhouse/logs'),
                fuzzy_match_threshold=float(os.getenv('FUZZY_MATCH_THRESHOLD', '0.85'))
            )
        except (ValueError, TypeError) as e:
            logging.error(f"Configuration error: {e}")
            raise


# ============================================================================
# Logging Setup
# ============================================================================

def setup_logging(config: Config, verbose: bool = False) -> logging.Logger:
    """Configure structured logging with file rotation"""
    os.makedirs(config.log_dir, exist_ok=True)
    log_path = os.path.join(config.log_dir, config.log_file)

    # Create logger
    logger = logging.getLogger('hardcover_enrichment')
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)

    # File handler with rotation
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler(
        log_path,
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=7
    )
    file_handler.setLevel(logging.DEBUG)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG if verbose else logging.INFO)

    # Formatter
    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


# ============================================================================
# Hardcover API Extractor
# ============================================================================

class HardcoverExtractor:
    """Query Hardcover GraphQL API for personal library metadata"""

    def __init__(self, config: Config, logger: logging.Logger):
        self.config = config
        self.logger = logger
        self.session = requests.Session()
        self.session.headers.update({
            'authorization': config.hardcover_api_key,
            'Content-Type': 'application/json'
        })

    def test_connection(self) -> Tuple[bool, Optional[int]]:
        """Test API connection and retrieve user ID"""
        query = """
        query {
            me {
                id
                username
            }
        }
        """

        try:
            self.logger.info(f"Testing Hardcover API connection: {self.config.hardcover_endpoint}")
            response = self.session.post(
                self.config.hardcover_endpoint,
                json={'query': query},
                timeout=10
            )
            response.raise_for_status()

            data = response.json()
            if 'errors' in data:
                self.logger.error(f"API error: {data['errors']}")
                return False, None

            user_id = data['data']['me']['id']
            username = data['data']['me']['username']
            self.logger.info(f"Successfully connected to Hardcover API (User: {username}, ID: {user_id})")
            return True, user_id

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Connection failed: {e}")
            return False, None
        except (KeyError, json.JSONDecodeError) as e:
            self.logger.error(f"Invalid API response: {e}")
            return False, None

    def extract_library(self, user_id: int) -> List[Dict[str, Any]]:
        """Extract complete personal library from Hardcover API with pagination"""
        self.logger.info(f"Extracting library for user_id: {user_id}")

        all_books = []
        offset = 0
        limit = 100  # Hardcover API limit per request

        query = """
        query GetUserBooks($user_id: Int!, $limit: Int!, $offset: Int!) {
            user_books(
                where: {user_id: {_eq: $user_id}},
                distinct_on: book_id,
                limit: $limit,
                offset: $offset
            ) {
                book {
                    id
                    title
                    subtitle
                    description
                    rating
                    pages
                    release_date
                    isbns
                    slug
                    image {
                        url
                    }
                    contributions {
                        author {
                            id
                            name
                        }
                    }
                    editions {
                        id
                        isbn_10
                        isbn_13
                        publisher {
                            id
                            name
                        }
                    }
                }
            }
        }
        """

        while True:
            try:
                self.logger.debug(f"Fetching batch: offset={offset}, limit={limit}")
                response = self.session.post(
                    self.config.hardcover_endpoint,
                    json={
                        'query': query,
                        'variables': {
                            'user_id': user_id,
                            'limit': limit,
                            'offset': offset
                        }
                    },
                    timeout=30
                )
                response.raise_for_status()

                data = response.json()
                if 'errors' in data:
                    self.logger.error(f"API error: {data['errors']}")
                    break

                books = data['data']['user_books']
                if not books:
                    break  # No more books to fetch

                all_books.extend([item['book'] for item in books])
                self.logger.info(f"Extracted {len(books)} books (total: {len(all_books)})")

                offset += limit

                # Safety limit to prevent infinite loops
                if offset > 10000:
                    self.logger.warning("Reached safety limit of 10,000 books")
                    break

            except requests.exceptions.RequestException as e:
                self.logger.error(f"Request failed at offset {offset}: {e}")
                break
            except (KeyError, json.JSONDecodeError) as e:
                self.logger.error(f"Invalid response at offset {offset}: {e}")
                break

        self.logger.info(f"Extraction complete: {len(all_books)} total books")
        return all_books


# ============================================================================
# ISBN Normalization and Matching
# ============================================================================

class ISBNMatcher:
    """Handle ISBN normalization and matching logic"""

    @staticmethod
    def normalize_isbn(isbn: str) -> str:
        """Remove hyphens, spaces, and convert to uppercase"""
        if not isbn:
            return ""
        return re.sub(r'[\s\-]', '', str(isbn)).upper()

    @staticmethod
    def convert_isbn10_to_isbn13(isbn10: str) -> Optional[str]:
        """Convert ISBN-10 to ISBN-13 format"""
        isbn10 = ISBNMatcher.normalize_isbn(isbn10)
        if len(isbn10) != 10:
            return None

        # ISBN-13 = 978 + first 9 digits of ISBN-10 + new check digit
        isbn13_prefix = '978' + isbn10[:9]

        # Calculate check digit
        check_sum = sum(int(digit) * (1 if i % 2 == 0 else 3)
                       for i, digit in enumerate(isbn13_prefix))
        check_digit = (10 - (check_sum % 10)) % 10

        return isbn13_prefix + str(check_digit)

    @staticmethod
    def extract_isbns(hardcover_book: Dict[str, Any]) -> Tuple[Optional[str], Optional[str]]:
        """Extract and normalize ISBN-13 and ISBN-10 from Hardcover book data"""
        isbn_13 = None
        isbn_10 = None

        # Check isbns array field
        if 'isbns' in hardcover_book and hardcover_book['isbns']:
            for isbn in hardcover_book['isbns']:
                normalized = ISBNMatcher.normalize_isbn(isbn)
                if len(normalized) == 13:
                    isbn_13 = normalized
                elif len(normalized) == 10:
                    isbn_10 = normalized

        # Check editions for ISBNs
        if 'editions' in hardcover_book:
            for edition in hardcover_book['editions']:
                if not isbn_13 and edition.get('isbn_13'):
                    isbn_13 = ISBNMatcher.normalize_isbn(edition['isbn_13'])
                if not isbn_10 and edition.get('isbn_10'):
                    isbn_10 = ISBNMatcher.normalize_isbn(edition['isbn_10'])

        # If we have ISBN-10 but not ISBN-13, try conversion
        if isbn_10 and not isbn_13:
            isbn_13 = ISBNMatcher.convert_isbn10_to_isbn13(isbn_10)

        return isbn_13, isbn_10


# ============================================================================
# Fuzzy Matching for Title + Author
# ============================================================================

class FuzzyMatcher:
    """Fuzzy string matching for title and author fallback"""

    @staticmethod
    def similarity(a: str, b: str) -> float:
        """Calculate similarity ratio between two strings"""
        if not a or not b:
            return 0.0
        return SequenceMatcher(None, a.lower().strip(), b.lower().strip()).ratio()

    @staticmethod
    def match_title_author(hardcover_title: str, hardcover_author: str,
                          existing_books: List[Dict[str, Any]], threshold: float = 0.85) -> Optional[int]:
        """Find matching book by fuzzy title+author matching"""
        if not hardcover_title or not hardcover_author:
            return None

        best_match_id = None
        best_score = 0.0

        for book in existing_books:
            title_sim = FuzzyMatcher.similarity(hardcover_title, book.get('title', ''))
            author_sim = FuzzyMatcher.similarity(hardcover_author, book.get('author_name', ''))

            # Combined score (weighted average: 60% title, 40% author)
            combined_score = (title_sim * 0.6) + (author_sim * 0.4)

            if combined_score > best_score and combined_score >= threshold:
                best_score = combined_score
                best_match_id = book['book_id']

        return best_match_id


# ============================================================================
# Data Transformation
# ============================================================================

class DataTransformer:
    """Transform Hardcover API data to Neon.tech schema"""

    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def transform_author(self, contribution: Dict[str, Any]) -> Dict[str, Any]:
        """Transform Hardcover author to Neon.tech authors schema"""
        author = contribution.get('author', {})
        return {
            'hardcover_author_id': author.get('id'),
            'author_name': author.get('name', 'Unknown Author'),
            'alternate_names': None,  # Not available in API
            'book_count': None,  # Will be computed
            'contributions': None,  # Not available
            'born_year': None,  # Not available in basic API
            'is_bipoc': None,
            'is_lgbtq': None
        }

    def transform_publisher(self, edition: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Transform Hardcover publisher to Neon.tech publishers schema"""
        publisher = edition.get('publisher')
        if not publisher:
            return None

        return {
            'hardcover_publisher_id': publisher.get('id'),
            'publisher_name': publisher.get('name', 'Unknown Publisher'),
            'alternate_names': None,
            'parent_id': None,  # Imprint hierarchy not available
            'country': None
        }

    def transform_book(self, hardcover_book: Dict[str, Any], author_id: Optional[int],
                      publisher_id: Optional[int]) -> Dict[str, Any]:
        """Transform Hardcover book to Neon.tech books schema"""
        isbn_13, isbn_10 = ISBNMatcher.extract_isbns(hardcover_book)

        # Extract cover URL
        cover_url = None
        if 'image' in hardcover_book and hardcover_book['image']:
            cover_url = hardcover_book['image'].get('url')

        # Extract primary author name for title matching
        primary_author = None
        if 'contributions' in hardcover_book and hardcover_book['contributions']:
            primary_author = hardcover_book['contributions'][0].get('author', {}).get('name')

        return {
            'title': hardcover_book.get('title', 'Unknown Title'),
            'author_id': author_id,
            'isbn_13': isbn_13,
            'isbn_10': isbn_10,
            'hardcover_book_id': hardcover_book.get('id'),
            'publisher_id': publisher_id,
            'cover_url': cover_url,
            'pages': hardcover_book.get('pages'),
            'hardcover_rating': hardcover_book.get('rating'),
            'description': hardcover_book.get('description'),
            'release_date': hardcover_book.get('release_date'),
            'data_source': 'hardcover',
            'enriched_at': datetime.now(),
            'primary_author_name': primary_author  # For fuzzy matching only
        }


# ============================================================================
# Neon.tech Database Enrichment
# ============================================================================

class NeonEnricher:
    """Insert and update books, authors, publishers in Neon.tech database"""

    def __init__(self, config: Config, logger: logging.Logger, dry_run: bool = False):
        self.config = config
        self.logger = logger
        self.dry_run = dry_run
        self.conn_pool = None

        if not dry_run:
            self._init_connection_pool()

    def _init_connection_pool(self):
        """Initialize PostgreSQL connection pool"""
        try:
            self.conn_pool = pool.SimpleConnectionPool(
                1,  # minconn
                5,  # maxconn
                host=self.config.neon_host,
                port=self.config.neon_port,
                user=self.config.neon_user,
                password=self.config.neon_password,
                database=self.config.neon_database,
                connect_timeout=10
            )
            self.logger.info("Database connection pool initialized")
        except psycopg2.Error as e:
            self.logger.error(f"Failed to initialize connection pool: {e}")
            raise

    def get_connection(self):
        """Get connection from pool"""
        if self.dry_run:
            return None
        return self.conn_pool.getconn()

    def release_connection(self, conn):
        """Return connection to pool"""
        if conn and self.conn_pool:
            self.conn_pool.putconn(conn)

    def close_pool(self):
        """Close all connections in pool"""
        if self.conn_pool:
            self.conn_pool.closeall()
            self.logger.info("Database connection pool closed")

    def get_existing_books(self) -> List[Dict[str, Any]]:
        """Fetch all existing books from database for matching"""
        if self.dry_run:
            self.logger.info("[DRY-RUN] Would fetch existing books from database")
            return []

        conn = self.get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT b.book_id, b.title, b.isbn_13, b.isbn_10, b.hardcover_book_id,
                           a.author_name
                    FROM books b
                    LEFT JOIN authors a ON b.author_id = a.author_id
                """)
                books = cur.fetchall()
                self.logger.info(f"Fetched {len(books)} existing books from database")
                return [dict(book) for book in books]
        except psycopg2.Error as e:
            self.logger.error(f"Failed to fetch existing books: {e}")
            return []
        finally:
            self.release_connection(conn)

    def upsert_author(self, author_data: Dict[str, Any]) -> Optional[int]:
        """Insert or update author, return author_id"""
        if self.dry_run:
            self.logger.info(f"[DRY-RUN] Would upsert author: {author_data['author_name']}")
            return None

        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO authors (author_name, hardcover_author_id, alternate_names, born_year, is_bipoc, is_lgbtq)
                    VALUES (%(author_name)s, %(hardcover_author_id)s, %(alternate_names)s, %(born_year)s, %(is_bipoc)s, %(is_lgbtq)s)
                    ON CONFLICT (author_name)
                    DO UPDATE SET hardcover_author_id = EXCLUDED.hardcover_author_id
                    RETURNING author_id
                """, author_data)
                author_id = cur.fetchone()[0]
                conn.commit()
                self.logger.debug(f"Upserted author: {author_data['author_name']} (ID: {author_id})")
                return author_id
        except psycopg2.Error as e:
            conn.rollback()
            self.logger.error(f"Failed to upsert author: {e}")
            return None
        finally:
            self.release_connection(conn)

    def upsert_publisher(self, publisher_data: Dict[str, Any]) -> Optional[int]:
        """Insert or update publisher, return publisher_id"""
        if self.dry_run:
            self.logger.info(f"[DRY-RUN] Would upsert publisher: {publisher_data['publisher_name']}")
            return None

        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO publishers (publisher_name, hardcover_publisher_id, alternate_names, parent_id, country)
                    VALUES (%(publisher_name)s, %(hardcover_publisher_id)s, %(alternate_names)s, %(parent_id)s, %(country)s)
                    ON CONFLICT (publisher_name)
                    DO UPDATE SET hardcover_publisher_id = EXCLUDED.hardcover_publisher_id
                    RETURNING publisher_id
                """, publisher_data)
                publisher_id = cur.fetchone()[0]
                conn.commit()
                self.logger.debug(f"Upserted publisher: {publisher_data['publisher_name']} (ID: {publisher_id})")
                return publisher_id
        except psycopg2.Error as e:
            conn.rollback()
            self.logger.error(f"Failed to upsert publisher: {e}")
            return None
        finally:
            self.release_connection(conn)

    def enrich_book(self, book_data: Dict[str, Any], matched_book_id: Optional[int] = None) -> bool:
        """Insert new book or update existing book with Hardcover metadata"""
        if self.dry_run:
            action = "update" if matched_book_id else "insert"
            self.logger.info(f"[DRY-RUN] Would {action} book: {book_data['title']}")
            return True

        # Remove primary_author_name (used only for matching)
        book_data.pop('primary_author_name', None)

        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                if matched_book_id:
                    # Update existing book
                    cur.execute("""
                        UPDATE books SET
                            author_id = %(author_id)s,
                            publisher_id = %(publisher_id)s,
                            isbn_13 = COALESCE(%(isbn_13)s, isbn_13),
                            isbn_10 = COALESCE(%(isbn_10)s, isbn_10),
                            hardcover_book_id = %(hardcover_book_id)s,
                            cover_url = %(cover_url)s,
                            pages = COALESCE(%(pages)s, pages),
                            hardcover_rating = %(hardcover_rating)s,
                            description = %(description)s,
                            release_date = %(release_date)s,
                            enriched_at = %(enriched_at)s
                        WHERE book_id = %(book_id)s
                    """, {**book_data, 'book_id': matched_book_id})
                    self.logger.info(f"Enriched existing book: {book_data['title']} (ID: {matched_book_id})")
                else:
                    # Insert new book
                    cur.execute("""
                        INSERT INTO books (title, author_id, isbn_13, isbn_10, hardcover_book_id,
                                         publisher_id, cover_url, pages, hardcover_rating,
                                         description, release_date, data_source, enriched_at)
                        VALUES (%(title)s, %(author_id)s, %(isbn_13)s, %(isbn_10)s, %(hardcover_book_id)s,
                               %(publisher_id)s, %(cover_url)s, %(pages)s, %(hardcover_rating)s,
                               %(description)s, %(release_date)s, %(data_source)s, %(enriched_at)s)
                        RETURNING book_id
                    """, book_data)
                    book_id = cur.fetchone()[0]
                    self.logger.info(f"Inserted new book: {book_data['title']} (ID: {book_id})")

                conn.commit()
                return True
        except psycopg2.Error as e:
            conn.rollback()
            self.logger.error(f"Failed to enrich book: {e}")
            return False
        finally:
            self.release_connection(conn)


# ============================================================================
# Main Enrichment Pipeline
# ============================================================================

class EnrichmentPipeline:
    """Orchestrate complete Hardcover enrichment process"""

    def __init__(self, config: Config, logger: logging.Logger, dry_run: bool = False):
        self.config = config
        self.logger = logger
        self.dry_run = dry_run

        self.extractor = HardcoverExtractor(config, logger)
        self.transformer = DataTransformer(logger)
        self.enricher = NeonEnricher(config, logger, dry_run)

        self.stats = {
            'total_books': 0,
            'isbn_matched': 0,
            'fuzzy_matched': 0,
            'new_books': 0,
            'enriched_books': 0,
            'skipped_books': 0,
            'authors_created': 0,
            'publishers_created': 0,
            'errors': 0
        }

    def run(self):
        """Execute complete enrichment pipeline"""
        self.logger.info("=" * 80)
        self.logger.info("Starting Hardcover Metadata Enrichment Pipeline")
        self.logger.info(f"Mode: {'DRY-RUN' if self.dry_run else 'PRODUCTION'}")
        self.logger.info("=" * 80)

        # Step 1: Test connection and get user ID
        success, user_id = self.extractor.test_connection()
        if not success:
            self.logger.error("Failed to connect to Hardcover API")
            return False

        if not user_id:
            if self.config.hardcover_user_id:
                user_id = self.config.hardcover_user_id
                self.logger.info(f"Using configured user_id: {user_id}")
            else:
                self.logger.error("Could not determine user ID")
                return False

        # Step 2: Extract library from Hardcover
        hardcover_books = self.extractor.extract_library(user_id)
        self.stats['total_books'] = len(hardcover_books)

        if not hardcover_books:
            self.logger.warning("No books extracted from Hardcover library")
            return True

        # Step 3: Get existing books for matching
        existing_books = self.enricher.get_existing_books()

        # Step 4: Process each book
        for hc_book in hardcover_books:
            try:
                self._process_book(hc_book, existing_books)
            except Exception as e:
                self.logger.error(f"Error processing book '{hc_book.get('title', 'Unknown')}': {e}")
                self.stats['errors'] += 1

        # Step 5: Report statistics
        self._report_statistics()

        # Cleanup
        self.enricher.close_pool()

        self.logger.info("Enrichment pipeline completed successfully")
        return True

    def _process_book(self, hc_book: Dict[str, Any], existing_books: List[Dict[str, Any]]):
        """Process a single Hardcover book"""
        title = hc_book.get('title', 'Unknown')
        self.logger.debug(f"Processing book: {title}")

        # Extract ISBNs
        isbn_13, isbn_10 = ISBNMatcher.extract_isbns(hc_book)

        # Step 1: Try ISBN-based matching
        matched_book_id = None
        if isbn_13 or isbn_10:
            for book in existing_books:
                if (isbn_13 and book.get('isbn_13') == isbn_13) or \
                   (isbn_10 and book.get('isbn_10') == isbn_10):
                    matched_book_id = book['book_id']
                    self.stats['isbn_matched'] += 1
                    self.logger.debug(f"ISBN match found: {title} (book_id: {matched_book_id})")
                    break

        # Step 2: Try Hardcover ID matching
        if not matched_book_id and hc_book.get('id'):
            for book in existing_books:
                if book.get('hardcover_book_id') == hc_book['id']:
                    matched_book_id = book['book_id']
                    self.logger.debug(f"Hardcover ID match found: {title} (book_id: {matched_book_id})")
                    break

        # Step 3: Try fuzzy title+author matching
        if not matched_book_id:
            primary_author = None
            if 'contributions' in hc_book and hc_book['contributions']:
                primary_author = hc_book['contributions'][0].get('author', {}).get('name')

            if primary_author:
                matched_book_id = FuzzyMatcher.match_title_author(
                    title, primary_author, existing_books, self.config.fuzzy_match_threshold
                )
                if matched_book_id:
                    self.stats['fuzzy_matched'] += 1
                    self.logger.debug(f"Fuzzy match found: {title} (book_id: {matched_book_id})")

        # Step 4: Process author
        author_id = None
        if 'contributions' in hc_book and hc_book['contributions']:
            author_data = self.transformer.transform_author(hc_book['contributions'][0])
            author_id = self.enricher.upsert_author(author_data)
            if author_id and not self.dry_run:
                self.stats['authors_created'] += 1

        # Step 5: Process publisher
        publisher_id = None
        if 'editions' in hc_book and hc_book['editions']:
            publisher_data = self.transformer.transform_publisher(hc_book['editions'][0])
            if publisher_data:
                publisher_id = self.enricher.upsert_publisher(publisher_data)
                if publisher_id and not self.dry_run:
                    self.stats['publishers_created'] += 1

        # Step 6: Transform and enrich book
        book_data = self.transformer.transform_book(hc_book, author_id, publisher_id)
        success = self.enricher.enrich_book(book_data, matched_book_id)

        if success:
            if matched_book_id:
                self.stats['enriched_books'] += 1
            else:
                self.stats['new_books'] += 1
        else:
            self.stats['skipped_books'] += 1

    def _report_statistics(self):
        """Report enrichment statistics"""
        self.logger.info("=" * 80)
        self.logger.info("ENRICHMENT STATISTICS")
        self.logger.info("=" * 80)
        self.logger.info(f"Total books processed:     {self.stats['total_books']}")
        self.logger.info(f"  - ISBN matched:          {self.stats['isbn_matched']}")
        self.logger.info(f"  - Fuzzy matched:         {self.stats['fuzzy_matched']}")
        self.logger.info(f"  - New books inserted:    {self.stats['new_books']}")
        self.logger.info(f"  - Existing books enriched: {self.stats['enriched_books']}")
        self.logger.info(f"  - Skipped/errors:        {self.stats['skipped_books']}")
        self.logger.info(f"Authors created/updated:   {self.stats['authors_created']}")
        self.logger.info(f"Publishers created/updated: {self.stats['publishers_created']}")
        self.logger.info(f"Errors:                    {self.stats['errors']}")
        self.logger.info("=" * 80)


# ============================================================================
# Command-Line Interface
# ============================================================================

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Enrich Neon.tech books table with Hardcover API metadata'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview operations without writing to database'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    parser.add_argument(
        '--env-file',
        default='/home/alexhouse/.env.hardcover',
        help='Path to environment file (default: /home/alexhouse/.env.hardcover)'
    )

    args = parser.parse_args()

    # Load configuration
    try:
        config = Config.load_from_env(args.env_file)
    except Exception as e:
        print(f"ERROR: Failed to load configuration: {e}")
        sys.exit(1)

    # Setup logging
    logger = setup_logging(config, args.verbose)

    # Validate configuration
    if not config.hardcover_api_key:
        logger.error("HARDCOVER_API_KEY not set in environment")
        sys.exit(1)

    if not all([config.neon_host, config.neon_user, config.neon_password]):
        logger.error("Neon.tech database credentials not set in environment")
        sys.exit(1)

    # Run pipeline
    try:
        pipeline = EnrichmentPipeline(config, logger, args.dry_run)
        success = pipeline.run()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
        sys.exit(130)
    except Exception as e:
        logger.exception(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
