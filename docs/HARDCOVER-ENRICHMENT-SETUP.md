# Hardcover API Metadata Enrichment Setup Guide

**Story 3.3: Integrate Hardcover API metadata and enrich books table**
**Created:** 2025-10-31
**Purpose:** Enrich Neon.tech books table with complete metadata from Hardcover.app

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Prerequisites](#prerequisites)
4. [API Credentials Setup](#api-credentials-setup)
5. [Configuration](#configuration)
6. [Manual Execution](#manual-execution)
7. [Automation (Optional)](#automation-optional)
8. [Validation](#validation)
9. [Troubleshooting](#troubleshooting)
10. [Security Considerations](#security-considerations)

---

## Overview

The Hardcover enrichment script (`enrich_hardcover_metadata.py`) queries the Hardcover GraphQL API to extract your personal library and enriches the Neon.tech `books` table with complete metadata including:

- **Authors:** Primary author with Hardcover author ID
- **Publishers:** Publisher information with Hardcover publisher ID
- **ISBNs:** ISBN-13 and ISBN-10 identifiers
- **Ratings:** Hardcover community rating
- **Cover Images:** High-quality cover URLs
- **Descriptions:** Book summaries and descriptions
- **Publication Dates:** Release dates

### Key Features

- **ISBN-based matching:** Primary matching strategy using ISBN-13/ISBN-10
- **Fuzzy title+author matching:** Fallback matching for books without ISBNs (>85% similarity threshold)
- **Hardcover ID matching:** Match by Hardcover book ID for books already in database
- **Author/Publisher dimensions:** Auto-create dimension records with conflict resolution
- **Data source tracking:** Records enrichment source and timestamp
- **Dry-run mode:** Safe preview without database writes
- **Pagination:** Handles large libraries (supports 10,000+ books)
- **Structured logging:** Comprehensive logs with rotation (10MB max, 7-day retention)

---

## Architecture

```
┌─────────────────────┐
│  Hardcover.app API  │
│   (GraphQL)         │
└──────────┬──────────┘
           │
           │ 1. Query user_books
           │    (paginated, 100/batch)
           ▼
┌─────────────────────┐
│ HardcoverExtractor  │
│  - Authentication   │
│  - Library query    │
│  - Pagination       │
└──────────┬──────────┘
           │
           │ 2. Transform
           ▼
┌─────────────────────┐
│  DataTransformer    │
│  - Authors schema   │
│  - Publishers schema│
│  - Books schema     │
└──────────┬──────────┘
           │
           │ 3. Match existing
           ▼
┌─────────────────────┐
│   ISBNMatcher /     │
│   FuzzyMatcher      │
│  - ISBN normalize   │
│  - Title+author     │
└──────────┬──────────┘
           │
           │ 4. Enrich
           ▼
┌─────────────────────┐
│   NeonEnricher      │
│  - Upsert authors   │
│  - Upsert publishers│
│  - Insert/update    │
│    books            │
└─────────────────────┘
           │
           ▼
┌─────────────────────┐
│  Neon.tech          │
│  PostgreSQL         │
│  - books table      │
│  - authors table    │
│  - publishers table │
└─────────────────────┘
```

**Pipeline Stages:**

1. **Extract:** Query Hardcover API for user's complete library
2. **Transform:** Map Hardcover fields to Neon.tech schema
3. **Match:** Find existing books by ISBN → Hardcover ID → fuzzy title+author
4. **Enrich:** Insert new books or update existing with Hardcover metadata

---

## Prerequisites

### System Requirements

- **Python:** 3.8+
- **Operating System:** Linux (Raspbian Bookworm on Raspberry Pi 4)
- **Network:** Internet access to `api.hardcover.app`
- **Database:** Neon.tech PostgreSQL 17 (initialized by Story 1.4)

### Python Dependencies

Install required packages:

```bash
pip3 install requests psycopg2-binary python-dotenv
```

**Packages:**
- `requests`: HTTP client for Hardcover GraphQL API
- `psycopg2-binary`: PostgreSQL adapter for Neon.tech
- `python-dotenv`: Environment variable management

### Database Schema

Ensure the following tables exist (created by Story 1.4):

- `authors` (author_id, author_name, hardcover_author_id, ...)
- `publishers` (publisher_id, publisher_name, hardcover_publisher_id, ...)
- `books` (book_id, title, author_id, publisher_id, isbn_13, isbn_10, hardcover_book_id, cover_url, hardcover_rating, enriched_at, ...)

**Required columns added for Story 3.3:**
- `books.hardcover_book_id` (INT, nullable, for Hardcover ID matching)
- `books.enriched_at` (TIMESTAMP, nullable, for audit trail)
- `authors.hardcover_author_id` (INT, nullable)
- `publishers.hardcover_publisher_id` (INT, nullable)

---

## API Credentials Setup

### Step 1: Get Hardcover API Token

1. Log in to [Hardcover.app](https://hardcover.app)
2. Navigate to **Settings** → **[Hardcover API](https://hardcover.app/settings/api)**
3. Copy your **API Token** from the top of the page

   **⚠️ Security Warning:**
   - API tokens provide full access to your Hardcover account
   - Never share your token or commit it to version control
   - Treat it like a password

### Step 2: Get Your User ID

1. Open the [Hardcover GraphQL Console](https://cloud.hasura.io/public/graphiql?endpoint=https://api.hardcover.app/v1/graphql)
2. Add authorization header:
   - **Header name:** `authorization`
   - **Header value:** `<your API token>`
3. Run this query:

```graphql
query {
    me {
        id
        username
    }
}
```

4. Note your `id` value (e.g., `12345`)

---

## Configuration

### Environment File Setup

Create environment file at `/home/alexhouse/.env.hardcover`:

```bash
# Hardcover API Configuration
HARDCOVER_API_KEY=<your_hardcover_api_token>
HARDCOVER_ENDPOINT=https://api.hardcover.app/v1/graphql
HARDCOVER_USER_ID=<your_user_id>

# Neon.tech Database Configuration
NEON_HOST=<your-neon-host>.neon.tech
NEON_USER=<your-username>
NEON_PASSWORD=<your-password>
NEON_DATABASE=neondb
NEON_PORT=5432

# Logging Configuration
LOG_DIR=/home/alexhouse/logs

# Matching Configuration
FUZZY_MATCH_THRESHOLD=0.85
```

### Secure the Environment File

```bash
chmod 600 /home/alexhouse/.env.hardcover
```

**Field Descriptions:**

| Variable | Required | Description | Default |
|----------|----------|-------------|---------|
| `HARDCOVER_API_KEY` | ✅ Yes | Your Hardcover API token | - |
| `HARDCOVER_ENDPOINT` | No | Hardcover GraphQL endpoint | `https://api.hardcover.app/v1/graphql` |
| `HARDCOVER_USER_ID` | No | Your Hardcover user ID (auto-detected if omitted) | - |
| `NEON_HOST` | ✅ Yes | Neon.tech database host | - |
| `NEON_USER` | ✅ Yes | Neon.tech username | - |
| `NEON_PASSWORD` | ✅ Yes | Neon.tech password | - |
| `NEON_DATABASE` | No | Database name | `neondb` |
| `NEON_PORT` | No | PostgreSQL port | `5432` |
| `LOG_DIR` | No | Log file directory | `/home/alexhouse/logs` |
| `FUZZY_MATCH_THRESHOLD` | No | Fuzzy matching threshold (0.0-1.0) | `0.85` |

---

## Manual Execution

### Dry-Run Mode (Recommended First)

Preview operations without writing to database:

```bash
python3 /home/alexhouse/resources/scripts/enrich_hardcover_metadata.py --dry-run
```

**Output:**
- Shows what books would be matched/inserted/updated
- Displays matching statistics
- No database modifications

### Production Run

Execute enrichment with database writes:

```bash
python3 /home/alexhouse/resources/scripts/enrich_hardcover_metadata.py
```

### Verbose Logging

Enable detailed debug logs:

```bash
python3 /home/alexhouse/resources/scripts/enrich_hardcover_metadata.py --verbose
```

### Custom Environment File

Use alternative environment file:

```bash
python3 /home/alexhouse/resources/scripts/enrich_hardcover_metadata.py --env-file /path/to/custom.env
```

### Command-Line Options

```
Usage: enrich_hardcover_metadata.py [OPTIONS]

Options:
  --dry-run             Preview operations without database writes
  --verbose, -v         Enable verbose debug logging
  --env-file PATH       Path to environment file (default: /home/alexhouse/.env.hardcover)
  --help, -h            Show this help message and exit
```

---

## Automation (Optional)

### Systemd Service (One-Time Execution)

Create `/etc/systemd/system/hardcover-enrichment.service`:

```ini
[Unit]
Description=Hardcover Metadata Enrichment Service
After=network-online.target
Wants=network-online.target

[Service]
Type=oneshot
User=alexhouse
WorkingDirectory=/home/alexhouse
ExecStart=/usr/bin/python3 /home/alexhouse/resources/scripts/enrich_hardcover_metadata.py
StandardOutput=journal
StandardError=journal
SyslogIdentifier=hardcover-enrichment

[Install]
WantedBy=multi-user.target
```

### Systemd Timer (Weekly Execution)

Create `/etc/systemd/system/hardcover-enrichment.timer`:

```ini
[Unit]
Description=Weekly Hardcover Metadata Enrichment
Requires=hardcover-enrichment.service

[Timer]
OnCalendar=weekly
OnBootSec=10min
Persistent=true

[Install]
WantedBy=timers.target
```

### Enable Automation

```bash
sudo systemctl daemon-reload
sudo systemctl enable hardcover-enrichment.timer
sudo systemctl start hardcover-enrichment.timer

# Check timer status
sudo systemctl status hardcover-enrichment.timer
sudo systemctl list-timers --all | grep hardcover
```

### Manual Trigger

```bash
sudo systemctl start hardcover-enrichment.service
sudo journalctl -u hardcover-enrichment.service -f
```

---

## Validation

### 1. Check Enrichment Logs

```bash
tail -f /home/alexhouse/logs/hardcover-enrichment.log
```

**Expected output:**
```
[2025-10-31 14:23:45] [INFO] [hardcover_enrichment] Starting Hardcover Metadata Enrichment Pipeline
[2025-10-31 14:23:46] [INFO] [hardcover_enrichment] Successfully connected to Hardcover API (User: yourname, ID: 12345)
[2025-10-31 14:23:47] [INFO] [hardcover_enrichment] Extracted 150 books (total: 150)
[2025-10-31 14:23:48] [INFO] [hardcover_enrichment] Extraction complete: 150 total books
[2025-10-31 14:23:49] [INFO] [hardcover_enrichment] Fetched 50 existing books from database
[2025-10-31 14:24:15] [INFO] [hardcover_enrichment] Enrichment pipeline completed successfully
[2025-10-31 14:24:15] [INFO] [hardcover_enrichment] Total books processed:     150
[2025-10-31 14:24:15] [INFO] [hardcover_enrichment]   - ISBN matched:          45
[2025-10-31 14:24:15] [INFO] [hardcover_enrichment]   - Fuzzy matched:         5
[2025-10-31 14:24:15] [INFO] [hardcover_enrichment]   - New books inserted:    100
[2025-10-31 14:24:15] [INFO] [hardcover_enrichment]   - Existing books enriched: 50
```

### 2. SQL Validation Queries

#### Count Enriched Books

```sql
-- Count books enriched by Hardcover
SELECT COUNT(*) AS enriched_books
FROM books
WHERE enriched_at IS NOT NULL;
```

#### Check Hardcover Metadata Completeness

```sql
-- Books with Hardcover metadata
SELECT
    COUNT(*) AS total_books,
    COUNT(hardcover_book_id) AS has_hardcover_id,
    COUNT(cover_url) AS has_cover,
    COUNT(hardcover_rating) AS has_rating,
    COUNT(author_id) AS has_author,
    COUNT(publisher_id) AS has_publisher
FROM books;
```

#### Sample Enriched Books

```sql
-- View sample of enriched books
SELECT
    b.book_id,
    b.title,
    a.author_name,
    p.publisher_name,
    b.isbn_13,
    b.hardcover_rating,
    b.enriched_at
FROM books b
LEFT JOIN authors a ON b.author_id = a.author_id
LEFT JOIN publishers p ON b.publisher_id = p.publisher_id
WHERE b.enriched_at IS NOT NULL
ORDER BY b.enriched_at DESC
LIMIT 10;
```

#### Check Data Source Distribution

```sql
-- Data source distribution
SELECT data_source, COUNT(*) AS book_count
FROM books
GROUP BY data_source;
```

**Expected results:**
- `koreader`: Books from KOReader ETL (Story 3.2)
- `hardcover`: New books from Hardcover enrichment
- `NULL` or `calibre`: Books from other sources

#### Find Missing Metadata

```sql
-- Books without enrichment (candidates for future runs)
SELECT book_id, title, isbn_13
FROM books
WHERE enriched_at IS NULL
  AND (isbn_13 IS NOT NULL OR isbn_10 IS NOT NULL)
LIMIT 20;
```

### 3. Manual Spot Check

Compare 5-10 enriched books against [Hardcover.app](https://hardcover.app) website:

1. Pick sample books from enrichment logs
2. Search for book on Hardcover.app
3. Verify:
   - Author name matches
   - ISBN matches
   - Rating is accurate
   - Cover URL loads correctly
   - Publisher is correct

---

## Troubleshooting

### Common Issues

#### 1. API Authentication Failed

**Error:**
```
[ERROR] [hardcover_enrichment] Connection failed: 401 Unauthorized
```

**Solution:**
- Verify `HARDCOVER_API_KEY` in `.env.hardcover` is correct
- Get fresh API token from [Hardcover Settings](https://hardcover.app/settings/api)
- Ensure no extra spaces or quotes around token

#### 2. Database Connection Failed

**Error:**
```
[ERROR] [hardcover_enrichment] Failed to initialize connection pool: could not connect to server
```

**Solution:**
- Verify Neon.tech credentials in `.env.hardcover`
- Check network connectivity: `ping <NEON_HOST>`
- Verify database is active in [Neon Console](https://console.neon.tech)
- Check firewall rules allow port 5432

#### 3. Missing Python Dependencies

**Error:**
```
ERROR: Missing required dependency: No module named 'requests'
```

**Solution:**
```bash
pip3 install requests psycopg2-binary python-dotenv
```

#### 4. ISBN Normalization Issues

**Symptom:** Books not matching despite having ISBNs

**Solution:**
- Script normalizes ISBNs (removes hyphens, spaces)
- Check logs for `ISBN-10 to ISBN-13 conversion` messages
- Verify ISBNs in database are also normalized

#### 5. Low Fuzzy Match Count

**Symptom:** Few fuzzy matches found

**Adjustment:**
- Lower threshold in `.env.hardcover`: `FUZZY_MATCH_THRESHOLD=0.80`
- Check logs for `Fuzzy match` messages with similarity scores
- Review book titles for formatting differences (e.g., "The Book" vs "Book, The")

#### 6. Duplicate Books Created

**Symptom:** Same book inserted multiple times

**Solution:**
- Script should prevent this via ISBN/Hardcover ID matching
- Check if books have different ISBNs (different editions)
- Verify database constraints are active:
  ```sql
  SELECT conname, contype FROM pg_constraint WHERE conrelid = 'books'::regclass;
  ```

#### 7. Timeout During Large Library Extraction

**Error:**
```
[ERROR] [hardcover_enrichment] Request failed at offset 500: Connection timeout
```

**Solution:**
- Script handles pagination automatically
- Increase timeout in script (line ~230): `timeout=60`
- Run in smaller batches by limiting offset
- Check network stability

---

## Security Considerations

### API Token Security

1. **Never commit tokens to Git:**
   ```bash
   # Add to .gitignore
   echo ".env.hardcover" >> .gitignore
   ```

2. **Restrict file permissions:**
   ```bash
   chmod 600 /home/alexhouse/.env.hardcover
   ```

3. **Rotate tokens periodically:**
   - Regenerate API token every 6-12 months
   - Update `.env.hardcover` with new token

### Database Security

1. **Use read-write user with minimal privileges:**
   ```sql
   GRANT SELECT, INSERT, UPDATE ON books, authors, publishers TO enrichment_user;
   ```

2. **Avoid storing credentials in scripts:**
   - Always use environment variables
   - Never hardcode passwords

3. **Audit enriched data:**
   - Regularly review `enriched_at` timestamps
   - Monitor for unexpected data changes

### Network Security

1. **Use HTTPS only:**
   - Hardcover API enforces HTTPS
   - Neon.tech uses SSL by default

2. **Restrict outbound connections:**
   - Firewall rules: Allow only `api.hardcover.app:443` and Neon.tech:5432

---

## Performance Expectations

### Runtime Benchmarks

| Library Size | Expected Runtime | Memory Usage |
|--------------|------------------|--------------|
| 100 books    | 10-15 seconds    | <50 MB       |
| 500 books    | 30-45 seconds    | <100 MB      |
| 1,500 books  | 60-90 seconds    | <200 MB      |

**Factors affecting performance:**
- Network latency to Hardcover API
- Number of new books vs enriched existing
- Database response time (Neon.tech region)

### Optimization Tips

1. **Run during off-peak hours:**
   - Schedule timer for 2-4 AM local time
   - Reduces network congestion

2. **Batch processing:**
   - Script uses 100 books/batch pagination
   - Adjust `limit` variable if needed (line ~215)

3. **Connection pooling:**
   - Script uses connection pool (1-5 connections)
   - Reduces database connection overhead

---

## Appendix

### Related Documentation

- [Story 3.3 Technical Specification](../tech-spec-epic-3.md#story-33-integrate-hardcover-api-metadata-and-enrich-books-table)
- [Database Schema Documentation](./guides/SCHEMA-DOCUMENTATION.md)
- [ETL Pipeline Setup Guide](./ETL-PIPELINE-SETUP.md)
- [Hardcover API Official Docs](https://docs.hardcover.app/api/getting-started/)

### Script Location

```
/home/alexhouse/resources/scripts/enrich_hardcover_metadata.py
```

### Log Location

```
/home/alexhouse/logs/hardcover-enrichment.log
```

### Environment File Location

```
/home/alexhouse/.env.hardcover
```

---

**Last Updated:** 2025-10-31
**Story:** 3.3 - Integrate Hardcover API metadata and enrich books table
**Status:** Active
