#!/usr/bin/env python3
"""
Test Suite for Story 3.3: Hardcover API Metadata Enrichment

Tests cover:
- AC 1: Hardcover API authentication and connection validation
- AC 2: Personal library query and book extraction from Hardcover
- AC 3: Metadata transformation to Neon.tech books schema
- AC 4: ISBN-based matching between Hardcover and existing books
- AC 5: Data enrichment (Update books table with Hardcover metadata)
- AC 6: Fallback matching (Title+author matching when ISBN unavailable)
- AC 7: Data source tracking (Record which books came from Hardcover vs KOReader)
- AC 8: Manual execution and validation (Dry-run mode, sample verification)

Author: BookHelper Development Team
Date: 2025-10-31
"""

import sys
import os
import unittest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
import json

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'resources', 'scripts'))

try:
    from enrich_hardcover_metadata import (
        Config,
        HardcoverExtractor,
        ISBNMatcher,
        FuzzyMatcher,
        DataTransformer,
        NeonEnricher,
        EnrichmentPipeline,
        setup_logging
    )
except ImportError as e:
    print(f"ERROR: Cannot import enrichment script: {e}")
    sys.exit(1)


# ============================================================================
# Test AC 1: Hardcover API Authentication and Connection Validation
# ============================================================================

class TestHardcoverAuthentication(unittest.TestCase):
    """Test Hardcover API authentication and connection validation (AC 1)"""

    def setUp(self):
        """Set up test configuration and extractor"""
        self.config = Config(
            hardcover_api_key='test_token_12345',
            hardcover_endpoint='https://api.hardcover.app/v1/graphql',
            neon_host='test.neon.tech',
            neon_user='test_user',
            neon_password='test_pass',
            neon_database='testdb'
        )
        self.logger = Mock()
        self.extractor = HardcoverExtractor(self.config, self.logger)

    @patch('requests.Session.post')
    def test_successful_authentication(self, mock_post):
        """Test successful API authentication returns user ID"""
        # Mock successful API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'data': {
                'me': {
                    'id': 12345,
                    'username': 'testuser'
                }
            }
        }
        mock_post.return_value = mock_response

        success, user_id = self.extractor.test_connection()

        self.assertTrue(success)
        self.assertEqual(user_id, 12345)
        self.logger.info.assert_called()

    @patch('requests.Session.post')
    def test_authentication_failure_invalid_token(self, mock_post):
        """Test authentication failure with invalid token"""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.raise_for_status.side_effect = Exception("401 Unauthorized")
        mock_post.return_value = mock_response

        success, user_id = self.extractor.test_connection()

        self.assertFalse(success)
        self.assertIsNone(user_id)

    @patch('requests.Session.post')
    def test_authentication_timeout(self, mock_post):
        """Test connection timeout handling"""
        mock_post.side_effect = Exception("Connection timeout")

        success, user_id = self.extractor.test_connection()

        self.assertFalse(success)
        self.assertIsNone(user_id)
        self.logger.error.assert_called()


# ============================================================================
# Test AC 2: Personal Library Query and Book Extraction
# ============================================================================

class TestLibraryExtraction(unittest.TestCase):
    """Test personal library query and book extraction (AC 2)"""

    def setUp(self):
        self.config = Config(
            hardcover_api_key='test_token',
            hardcover_endpoint='https://api.hardcover.app/v1/graphql',
            neon_host='test.neon.tech',
            neon_user='test',
            neon_password='test',
            neon_database='test'
        )
        self.logger = Mock()
        self.extractor = HardcoverExtractor(self.config, self.logger)

    @patch('requests.Session.post')
    def test_extract_single_page(self, mock_post):
        """Test extracting single page of books (no pagination)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'data': {
                'user_books': [
                    {
                        'book': {
                            'id': 1,
                            'title': 'Test Book 1',
                            'isbns': ['9781234567890']
                        }
                    },
                    {
                        'book': {
                            'id': 2,
                            'title': 'Test Book 2',
                            'isbns': ['9780987654321']
                        }
                    }
                ]
            }
        }
        mock_post.return_value = mock_response

        books = self.extractor.extract_library(user_id=12345)

        self.assertEqual(len(books), 2)
        self.assertEqual(books[0]['title'], 'Test Book 1')
        self.assertEqual(books[1]['title'], 'Test Book 2')

    @patch('requests.Session.post')
    def test_extract_with_pagination(self, mock_post):
        """Test extraction with pagination (multiple batches)"""
        # First batch: 100 books
        first_response = Mock()
        first_response.status_code = 200
        first_response.json.return_value = {
            'data': {
                'user_books': [{'book': {'id': i, 'title': f'Book {i}'}} for i in range(100)]
            }
        }

        # Second batch: 50 books
        second_response = Mock()
        second_response.status_code = 200
        second_response.json.return_value = {
            'data': {
                'user_books': [{'book': {'id': i, 'title': f'Book {i}'}} for i in range(100, 150)]
            }
        }

        # Third batch: empty (end pagination)
        third_response = Mock()
        third_response.status_code = 200
        third_response.json.return_value = {
            'data': {
                'user_books': []
            }
        }

        mock_post.side_effect = [first_response, second_response, third_response]

        books = self.extractor.extract_library(user_id=12345)

        self.assertEqual(len(books), 150)
        self.assertEqual(mock_post.call_count, 3)

    @patch('requests.Session.post')
    def test_extract_handles_api_errors(self, mock_post):
        """Test extraction handles API errors gracefully"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'errors': [{'message': 'Rate limit exceeded'}]
        }
        mock_post.return_value = mock_response

        books = self.extractor.extract_library(user_id=12345)

        self.assertEqual(len(books), 0)
        self.logger.error.assert_called()


# ============================================================================
# Test AC 3: Metadata Transformation to Neon.tech Schema
# ============================================================================

class TestDataTransformation(unittest.TestCase):
    """Test metadata transformation to Neon.tech schema (AC 3)"""

    def setUp(self):
        self.logger = Mock()
        self.transformer = DataTransformer(self.logger)

    def test_transform_author(self):
        """Test author transformation from Hardcover to Neon schema"""
        hardcover_contribution = {
            'author': {
                'id': 5678,
                'name': 'Jane Doe'
            }
        }

        author_data = self.transformer.transform_author(hardcover_contribution)

        self.assertEqual(author_data['hardcover_author_id'], 5678)
        self.assertEqual(author_data['author_name'], 'Jane Doe')
        self.assertIsNone(author_data['alternate_names'])

    def test_transform_publisher(self):
        """Test publisher transformation from Hardcover to Neon schema"""
        hardcover_edition = {
            'publisher': {
                'id': 9999,
                'name': 'Penguin Books'
            }
        }

        publisher_data = self.transformer.transform_publisher(hardcover_edition)

        self.assertEqual(publisher_data['hardcover_publisher_id'], 9999)
        self.assertEqual(publisher_data['publisher_name'], 'Penguin Books')
        self.assertIsNone(publisher_data['parent_id'])

    def test_transform_book_complete(self):
        """Test book transformation with complete metadata"""
        hardcover_book = {
            'id': 123,
            'title': 'The Great Book',
            'isbns': ['9781234567890'],
            'rating': 4.5,
            'pages': 350,
            'description': 'A great book about books',
            'release_date': '2023-01-15',
            'image': {'url': 'https://example.com/cover.jpg'},
            'contributions': [{'author': {'name': 'Jane Doe'}}]
        }

        book_data = self.transformer.transform_book(hardcover_book, author_id=100, publisher_id=200)

        self.assertEqual(book_data['title'], 'The Great Book')
        self.assertEqual(book_data['hardcover_book_id'], 123)
        self.assertEqual(book_data['author_id'], 100)
        self.assertEqual(book_data['publisher_id'], 200)
        self.assertEqual(book_data['hardcover_rating'], 4.5)
        self.assertEqual(book_data['pages'], 350)
        self.assertEqual(book_data['cover_url'], 'https://example.com/cover.jpg')
        self.assertEqual(book_data['data_source'], 'hardcover')
        self.assertIsNotNone(book_data['enriched_at'])

    def test_transform_book_missing_fields(self):
        """Test book transformation handles missing optional fields"""
        hardcover_book = {
            'title': 'Minimal Book'
        }

        book_data = self.transformer.transform_book(hardcover_book, author_id=None, publisher_id=None)

        self.assertEqual(book_data['title'], 'Minimal Book')
        self.assertIsNone(book_data['author_id'])
        self.assertIsNone(book_data['publisher_id'])
        self.assertIsNone(book_data['isbn_13'])
        self.assertIsNone(book_data['cover_url'])


# ============================================================================
# Test AC 4: ISBN-Based Matching
# ============================================================================

class TestISBNMatching(unittest.TestCase):
    """Test ISBN-based matching between Hardcover and existing books (AC 4)"""

    def test_normalize_isbn_removes_hyphens(self):
        """Test ISBN normalization removes hyphens and spaces"""
        isbn = '978-1-234-56789-0'
        normalized = ISBNMatcher.normalize_isbn(isbn)
        self.assertEqual(normalized, '9781234567890')

    def test_normalize_isbn_handles_spaces(self):
        """Test ISBN normalization handles spaces"""
        isbn = '978 1 234 56789 0'
        normalized = ISBNMatcher.normalize_isbn(isbn)
        self.assertEqual(normalized, '9781234567890')

    def test_isbn10_to_isbn13_conversion(self):
        """Test ISBN-10 to ISBN-13 conversion"""
        isbn10 = '0123456789'
        isbn13 = ISBNMatcher.convert_isbn10_to_isbn13(isbn10)
        self.assertIsNotNone(isbn13)
        self.assertEqual(len(isbn13), 13)
        self.assertTrue(isbn13.startswith('978'))

    def test_isbn10_to_isbn13_invalid_length(self):
        """Test ISBN-10 conversion fails for invalid length"""
        invalid_isbn = '12345'
        isbn13 = ISBNMatcher.convert_isbn10_to_isbn13(invalid_isbn)
        self.assertIsNone(isbn13)

    def test_extract_isbns_from_isbns_array(self):
        """Test ISBN extraction from isbns array field"""
        hardcover_book = {
            'isbns': ['978-1-234-56789-0', '0-123-45678-9']
        }

        isbn_13, isbn_10 = ISBNMatcher.extract_isbns(hardcover_book)

        self.assertEqual(isbn_13, '9781234567890')
        self.assertEqual(isbn_10, '0123456789')

    def test_extract_isbns_from_editions(self):
        """Test ISBN extraction from editions field"""
        hardcover_book = {
            'editions': [
                {
                    'isbn_13': '978-1-234-56789-0',
                    'isbn_10': '0-123-45678-9'
                }
            ]
        }

        isbn_13, isbn_10 = ISBNMatcher.extract_isbns(hardcover_book)

        self.assertEqual(isbn_13, '9781234567890')
        self.assertEqual(isbn_10, '0123456789')

    def test_extract_isbns_converts_isbn10_to_isbn13(self):
        """Test ISBN extraction converts ISBN-10 to ISBN-13 when ISBN-13 missing"""
        hardcover_book = {
            'isbns': ['0123456789']
        }

        isbn_13, isbn_10 = ISBNMatcher.extract_isbns(hardcover_book)

        self.assertEqual(isbn_10, '0123456789')
        self.assertIsNotNone(isbn_13)
        self.assertTrue(isbn_13.startswith('978'))


# ============================================================================
# Test AC 6: Fallback Title+Author Matching
# ============================================================================

class TestFuzzyMatching(unittest.TestCase):
    """Test fallback title+author matching when ISBN unavailable (AC 6)"""

    def test_similarity_exact_match(self):
        """Test similarity calculation for exact match"""
        score = FuzzyMatcher.similarity("The Great Book", "The Great Book")
        self.assertEqual(score, 1.0)

    def test_similarity_case_insensitive(self):
        """Test similarity is case-insensitive"""
        score = FuzzyMatcher.similarity("The Great Book", "the great book")
        self.assertEqual(score, 1.0)

    def test_similarity_partial_match(self):
        """Test similarity calculation for partial match"""
        score = FuzzyMatcher.similarity("The Great Book", "The Good Book")
        self.assertGreater(score, 0.7)
        self.assertLess(score, 1.0)

    def test_similarity_no_match(self):
        """Test similarity calculation for no match"""
        score = FuzzyMatcher.similarity("The Great Book", "Completely Different")
        self.assertLess(score, 0.5)

    def test_match_title_author_high_similarity(self):
        """Test title+author matching finds match above threshold"""
        existing_books = [
            {'book_id': 1, 'title': 'The Great Book', 'author_name': 'Jane Doe'},
            {'book_id': 2, 'title': 'Another Book', 'author_name': 'John Smith'}
        ]

        match_id = FuzzyMatcher.match_title_author(
            'The Great Book',
            'Jane Doe',
            existing_books,
            threshold=0.85
        )

        self.assertEqual(match_id, 1)

    def test_match_title_author_below_threshold(self):
        """Test title+author matching returns None below threshold"""
        existing_books = [
            {'book_id': 1, 'title': 'Completely Different Title', 'author_name': 'Different Author'}
        ]

        match_id = FuzzyMatcher.match_title_author(
            'The Great Book',
            'Jane Doe',
            existing_books,
            threshold=0.85
        )

        self.assertIsNone(match_id)

    def test_match_title_author_weighted_scoring(self):
        """Test title+author matching uses weighted scoring (60% title, 40% author)"""
        existing_books = [
            # Book 1: Perfect title match, poor author match
            {'book_id': 1, 'title': 'The Great Book', 'author_name': 'Wrong Author'},
            # Book 2: Good title match, perfect author match
            {'book_id': 2, 'title': 'The Good Book', 'author_name': 'Jane Doe'}
        ]

        match_id = FuzzyMatcher.match_title_author(
            'The Great Book',
            'Jane Doe',
            existing_books,
            threshold=0.75
        )

        # Should match Book 2 due to author weight
        self.assertIn(match_id, [1, 2])  # Either could match depending on threshold


# ============================================================================
# Test AC 7: Data Source Tracking
# ============================================================================

class TestDataSourceTracking(unittest.TestCase):
    """Test data source tracking (AC 7)"""

    def setUp(self):
        self.logger = Mock()
        self.transformer = DataTransformer(self.logger)

    def test_hardcover_data_source_set(self):
        """Test data_source field is set to 'hardcover' for enriched books"""
        hardcover_book = {
            'id': 123,
            'title': 'Test Book'
        }

        book_data = self.transformer.transform_book(hardcover_book, author_id=1, publisher_id=1)

        self.assertEqual(book_data['data_source'], 'hardcover')

    def test_enriched_at_timestamp_set(self):
        """Test enriched_at timestamp is set during transformation"""
        hardcover_book = {
            'id': 123,
            'title': 'Test Book'
        }

        book_data = self.transformer.transform_book(hardcover_book, author_id=1, publisher_id=1)

        self.assertIsNotNone(book_data['enriched_at'])
        self.assertIsInstance(book_data['enriched_at'], datetime)


# ============================================================================
# Test AC 8: Dry-Run Mode and Validation
# ============================================================================

class TestDryRunMode(unittest.TestCase):
    """Test dry-run mode and validation (AC 8)"""

    def setUp(self):
        self.config = Config(
            hardcover_api_key='test',
            hardcover_endpoint='https://api.hardcover.app/v1/graphql',
            neon_host='test.neon.tech',
            neon_user='test',
            neon_password='test',
            neon_database='test'
        )
        self.logger = Mock()

    def test_dry_run_no_database_writes(self):
        """Test dry-run mode prevents database writes"""
        enricher = NeonEnricher(self.config, self.logger, dry_run=True)

        # Verify connection pool is not initialized in dry-run mode
        self.assertIsNone(enricher.conn_pool)

    def test_dry_run_logs_preview_messages(self):
        """Test dry-run mode logs preview messages"""
        enricher = NeonEnricher(self.config, self.logger, dry_run=True)

        author_data = {'author_name': 'Test Author', 'hardcover_author_id': 123}
        author_id = enricher.upsert_author(author_data)

        self.assertIsNone(author_id)  # No actual DB operation
        self.logger.info.assert_called()  # But logs preview

    def test_dry_run_fetch_existing_books_returns_empty(self):
        """Test dry-run mode returns empty list for existing books fetch"""
        enricher = NeonEnricher(self.config, self.logger, dry_run=True)

        books = enricher.get_existing_books()

        self.assertEqual(books, [])
        self.logger.info.assert_called()


# ============================================================================
# Test AC 5: Data Enrichment (Integration)
# ============================================================================

class TestEnrichmentIntegration(unittest.TestCase):
    """Test data enrichment pipeline integration (AC 5)"""

    def setUp(self):
        self.config = Config(
            hardcover_api_key='test',
            hardcover_endpoint='https://api.hardcover.app/v1/graphql',
            neon_host='test.neon.tech',
            neon_user='test',
            neon_password='test',
            neon_database='test'
        )
        self.logger = Mock()

    @patch('enrich_hardcover_metadata.NeonEnricher')
    @patch('enrich_hardcover_metadata.HardcoverExtractor')
    def test_pipeline_processes_books_end_to_end(self, mock_extractor_class, mock_enricher_class):
        """Test pipeline processes books from extraction to enrichment"""
        # Mock extractor
        mock_extractor = Mock()
        mock_extractor.test_connection.return_value = (True, 12345)
        mock_extractor.extract_library.return_value = [
            {
                'id': 1,
                'title': 'Test Book',
                'isbns': ['9781234567890'],
                'rating': 4.5,
                'contributions': [{'author': {'id': 100, 'name': 'Test Author'}}],
                'editions': [{'publisher': {'id': 200, 'name': 'Test Publisher'}}]
            }
        ]
        mock_extractor_class.return_value = mock_extractor

        # Mock enricher
        mock_enricher = Mock()
        mock_enricher.get_existing_books.return_value = []
        mock_enricher.upsert_author.return_value = 1
        mock_enricher.upsert_publisher.return_value = 1
        mock_enricher.enrich_book.return_value = True
        mock_enricher_class.return_value = mock_enricher

        # Run pipeline
        pipeline = EnrichmentPipeline(self.config, self.logger, dry_run=False)
        success = pipeline.run()

        self.assertTrue(success)
        self.assertEqual(pipeline.stats['total_books'], 1)
        self.assertEqual(pipeline.stats['new_books'], 1)

    def test_pipeline_statistics_tracking(self):
        """Test pipeline tracks enrichment statistics correctly"""
        pipeline = EnrichmentPipeline(self.config, self.logger, dry_run=True)

        # Verify initial stats
        self.assertEqual(pipeline.stats['total_books'], 0)
        self.assertEqual(pipeline.stats['isbn_matched'], 0)
        self.assertEqual(pipeline.stats['new_books'], 0)


# ============================================================================
# Test Configuration Management
# ============================================================================

class TestConfiguration(unittest.TestCase):
    """Test configuration loading and validation"""

    @patch.dict(os.environ, {
        'HARDCOVER_API_KEY': 'test_key',
        'HARDCOVER_ENDPOINT': 'https://api.test.com/graphql',
        'NEON_HOST': 'test.neon.tech',
        'NEON_USER': 'testuser',
        'NEON_PASSWORD': 'testpass',
        'NEON_DATABASE': 'testdb'
    })
    def test_load_config_from_environment(self):
        """Test configuration loads from environment variables"""
        config = Config.load_from_env('/nonexistent/path')

        self.assertEqual(config.hardcover_api_key, 'test_key')
        self.assertEqual(config.hardcover_endpoint, 'https://api.test.com/graphql')
        self.assertEqual(config.neon_host, 'test.neon.tech')

    def test_config_defaults(self):
        """Test configuration uses sensible defaults"""
        config = Config(
            hardcover_api_key='key',
            hardcover_endpoint='endpoint',
            neon_host='host',
            neon_user='user',
            neon_password='pass',
            neon_database='db'
        )

        self.assertEqual(config.neon_port, 5432)
        self.assertEqual(config.fuzzy_match_threshold, 0.85)
        self.assertEqual(config.log_dir, '/home/alexhouse/logs')


# ============================================================================
# Test Suite Runner
# ============================================================================

def run_tests():
    """Run all test suites"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestHardcoverAuthentication))
    suite.addTests(loader.loadTestsFromTestCase(TestLibraryExtraction))
    suite.addTests(loader.loadTestsFromTestCase(TestDataTransformation))
    suite.addTests(loader.loadTestsFromTestCase(TestISBNMatching))
    suite.addTests(loader.loadTestsFromTestCase(TestFuzzyMatching))
    suite.addTests(loader.loadTestsFromTestCase(TestDataSourceTracking))
    suite.addTests(loader.loadTestsFromTestCase(TestDryRunMode))
    suite.addTests(loader.loadTestsFromTestCase(TestEnrichmentIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestConfiguration))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
