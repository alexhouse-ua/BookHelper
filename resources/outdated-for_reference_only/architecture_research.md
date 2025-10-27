# Unified Reading Database: Technical Investigation Report

This comprehensive investigation examines reading-related services and data formats to inform the design of an automated data consolidation pipeline. The research covers five reading sources, their data access methods, and architectural recommendations for a unified database system.

## KOReader ecosystem: Sync methods and database architecture

KOReader provides native cloud sync for its statistics database and offers multiple paths for synchronization, each with distinct trade-offs for automated pipelines.

### Cloud sync configuration

**Native cloud sync** supports three storage backends through KOReader's built-in functionality (introduced in PR #9709):

**Dropbox setup** requires creating a developer app and generating OAuth credentials. The process involves visiting the Dropbox Developer Page, creating an app with full Dropbox access, and generating three key pieces of information: App Key, App Secret, and a Refresh Token. The refresh token generation requires constructing an OAuth URL, authorizing the app, and executing a curl command to exchange the authorization code. Configuration can be done through the KOReader menu (`Menu > Tools > Reading Statistics > Settings > Cloud Sync`) or by directly editing the Lua configuration file with the credentials stored in specific fields.

**WebDAV configuration** offers a more privacy-focused alternative. Setup involves adding a cloud storage account through `Top Menu > Cloud storage`, entering server details including the full WebDAV URL, username, password, and folder path. The sync is then enabled through `Menu > Tools > Reading Statistics > Settings > Cloud Sync` by selecting the configured WebDAV account and designating a sync folder. Supported WebDAV services include NextCloud, InfiniCLOUD, Synology NAS, and any standard WebDAV-compliant server. Note that there was a reported issue (#13394) regarding folder selection that may have been resolved in recent versions.

The cloud sync system performs bidirectional sync with merge capabilities, storing data in SQLite databases (statistics.sqlite3, vocabulary_builder.sqlite3). Database size typically ranges from a few KB to a few MB depending on reading history. **Critical limitation**: There is no automatic sync by default—users must trigger sync manually via "Synchronize now" in the Reading Statistics menu.

### Syncthing as an alternative

Multiple community solutions exist for integrating Syncthing with KOReader, including dedicated plugins (jasonchoimtt/koreader-syncthing and arthurrump/syncthing.koplugin) and manual installation approaches. The plugins work on tested devices including Kobo (Clara BW, Elipsa 2E, Libra 2) and Kindle (Oasis, Scribe, Voyage), but are not compatible with Android devices.

**Manual installation** provides the most stable approach based on user experiences. The process involves downloading the ARM 32-bit Syncthing binary, placing it in the `.../KOBOeReader/.adds/` directory, creating configuration files, copying CA certificates for discovery server connections, and creating start/stop scripts. Access to the Syncthing GUI is via `http://<device-ip>:8384`.

**Critical configuration for e-readers**: FAT filesystems used on many e-readers have 2-second timestamp granularity. Without setting `modTimeWindowS=2` in Syncthing's folder advanced settings, constant conflicts and unnecessary re-syncs will occur. Additional essential settings include enabling "Ignore Permissions" and disabling "Sync Ownership," "Send Ownership," "Sync Extended Attributes," and "Send Extended Attributes."

**Syncthing pros for unified database pipelines**:
- **Flexibility**: Sync any files including book collections, annotations, and metadata folders (.sdr)
- **Privacy**: Peer-to-peer with end-to-end encryption, no third-party cloud service required
- **Functionality**: Bidirectional sync, automatic conflict detection, version history, works offline on local network
- **Cost**: Completely free and open source with no storage limits

**Syncthing cons specific to SQLite databases**:
- **File locking problems**: SQLite databases write frequently during active use, and syncing while KOReader is using the database can cause corruption with potential loss of all reading statistics
- **Conflict resolution challenges**: SQLite files cannot be meaningfully merged; if the same book is read on two devices, last-synced wins with possible data loss
- **Technical complexity**: Requires manual installation, configuration, understanding of filesystem permissions, and troubleshooting with command-line knowledge
- **Device limitations**: Global discovery/relay not working (local network only), cannot sync over internet without VPN or port forwarding

**Best practices for SQLite sync**: Close KOReader completely before syncing, start Syncthing manually when needed (not on boot), wait for sync to complete before opening KOReader, maintain regular backups of statistics.sqlite3 before syncing, and read on one device at a time (sync between device switches).

### KOReader database schema

The statistics.sqlite3 database uses a well-defined schema stored in the KOReader settings directory (typically `.../koreader/settings/statistics.sqlite3`).

**Book table structure**:
```sql
CREATE TABLE IF NOT EXISTS book
(
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    title             TEXT,
    authors           TEXT,
    notes             INTEGER,
    last_open         INTEGER,
    highlights        INTEGER,
    pages             INTEGER,
    series            TEXT,
    language          TEXT,
    md5               TEXT,
    total_read_time   INTEGER,
    total_read_pages  INTEGER
);

CREATE UNIQUE INDEX IF NOT EXISTS book_title_authors_md5 ON book(title, authors, md5);
```

Key columns include: id (primary key), title and authors (book identification), md5 (hash of book file for identification), last_open (Unix timestamp), pages (total page count), total_read_time (seconds), and total_read_pages (pages read).

**Page statistics table structure**:
```sql
CREATE TABLE IF NOT EXISTS page_stat_data
(
    id_book     INTEGER,
    page        INTEGER NOT NULL DEFAULT 0,
    start_time  INTEGER NOT NULL DEFAULT 0,
    duration    INTEGER NOT NULL DEFAULT 0,
    total_pages INTEGER NOT NULL DEFAULT 0,
    UNIQUE (id_book, page, start_time),
    FOREIGN KEY(id_book) REFERENCES book(id)
);

CREATE INDEX IF NOT EXISTS page_stat_data_start_time ON page_stat_data(start_time);
```

This table stores granular reading session data where each row represents a reading session for a specific page. The columns include: id_book (foreign key to book table), page (page number read), start_time (Unix timestamp in seconds), duration (session duration in seconds), and total_pages (total pages at time of reading, critical for handling layout changes from font size adjustments).

The schema includes a `page_stat` SQL view that rescales page_stat_data to account for document layout changes, using a `numbers` helper table and complex SQL to interpolate reading data when the total page count changes. The current schema version is 20201022, with automatic migrations that create backups before changes (e.g., `statistics.sqlite3.bkp.<old_version>-to-<new_version>`).

**Access and querying**: The database can be accessed via standard SQLite tools (`sqlite3 /path/to/statistics.sqlite3`), but KOReader must always be closed before accessing the database to prevent corruption. Never modify the database while KOReader is running.

## Hardcover.app API: GraphQL-based book metadata

Hardcover.app provides a comprehensive GraphQL API currently in beta, actively developed and used by Hardcover's own website and mobile applications.

### API architecture and access

**Base endpoint**: `https://api.hardcover.app/v1/graphql`  
**Type**: GraphQL (Hasura-based)  
**Method**: POST  
**Interactive console**: https://cloud.hasura.io/public/graphiql?endpoint=https://api.hardcover.app/v1/graphql

**Required headers**:
```
Content-Type: application/json
Authorization: Bearer YOUR_API_TOKEN
User-Agent: YourApp/1.0 (optional but recommended)
```

**Obtaining authentication tokens**: Create an account at hardcover.app, navigate to account settings at hardcover.app/account/api, click the "Hardcover API" link, and the token is displayed at the top of the page. Tokens automatically expire after 1 year and all tokens reset on January 1st annually. May be reset without notice during the beta period.

### ISBN and ASIN lookup methods

**Method 1: Search API** (recommended for ISBN lookup):
```graphql
query SearchByISBN {
  search(
    query: "9780140328721",
    query_type: "Book",
    per_page: 5,
    page: 1
  ) {
    results
  }
}
```

The search API searches the `isbns` field by default when query_type is "book". Parameters include query (required ISBN), query_type ("Book"), per_page (default 25), page (default 1), sort (e.g., "users_count:desc"), fields (default: "title,isbns,series_names,author_names,alternative_titles"), and weights (default: "5,5,3,1,1"). **Important note**: The search API returns results as a blob that requires manual parsing through the `results` field.

**Method 2: Direct editions query**:
```graphql
query GetEditionByISBN {
  editions(where: {isbn_13: {_eq: "9780140328721"}}) {
    id
    title
    edition_format
    pages
    release_date
    isbn_10
    isbn_13
    asin
    publisher {
      name
    }
    book {
      title
      subtitle
      release_date
      slug
      description
      rating
      ratings_count
      pages
      contributions {
        author {
          name
        }
      }
    }
  }
}
```

Alternative queries using `isbn_10` are also supported with the same structure.

### Complete response format

**Edition query response structure** (JSON):
```json
{
  "data": {
    "editions": [
      {
        "id": 21953653,
        "title": "Fantastic Mr. Fox",
        "edition_format": "Hardcover",
        "pages": 96,
        "release_date": "1970-01-01",
        "isbn_10": "0140328721",
        "isbn_13": "9780140328721",
        "asin": "0140328721",
        "publisher": {
          "name": "Puffin Books"
        },
        "book": {
          "title": "Fantastic Mr. Fox",
          "subtitle": null,
          "release_date": "1970-01-01",
          "slug": "fantastic-mr-fox",
          "description": "Book description here...",
          "rating": 4.2,
          "ratings_count": 1523,
          "pages": 96,
          "contributions": [
            {
              "author": {
                "name": "Roald Dahl"
              }
            }
          ]
        }
      }
    ]
  }
}
```

**Verified fields available**: The response contains all requested fields including title, authors (via contributions array), page count (both edition-level and book-level), publisher name, publication date (release_date), ISBN-10, ISBN-13, and ASIN. **Note**: ASIN is typically the same as ISBN-10 for printed books; for eBooks, ASIN usually starts with "B" and differs from ISBN.

Additional available fields include: edition_format, subtitle, description, slug (URL slug), rating (average rating), ratings_count, reviews_count, users_read_count, users_count, and cached_tags.

### Page count data reliability

Hardcover uses a hierarchical data system with three levels:

1. **dto_external**: Combined external source data prioritized by language (English favored), weighted by most-read editions, considering data completeness
2. **dto**: User/librarian-entered data manually added or corrected by community
3. **dto_combined**: Final merged data where user data overrides external data field-by-field

**Primary data sources** (from official documentation at hardcover.app/pages/book-data):
- **OpenLibrary**: Initial database population from data dumps; API for refreshing data
- **Google Books API**: Supplementary book information
- **Goodreads**: Data from user imports and associated Goodreads IDs
- **Inventaire**: High-quality book covers
- **Abe Books**: Additional cover images
- **User-generated data**: Reader contributions and librarian edits

**Reliability assessment**: High reliability when sourced from OpenLibrary or Google Books (major databases), very high reliability when verified by librarians (Editor/Librarian roles), moderate reliability for less common editions (fewer data sources), and variable for international editions depending on source coverage.

**Verification system**: Books must be "verified" to appear in search (fetched from external source OR verified by librarian). The librarian hierarchy includes Appender Librarians (can add missing data, default for all users), Editor Librarians (can edit data, requires 100+ books read and 1+ month account age), and Librarians (can edit any field including protected fields).

### Rate limits and restrictions

**Standard limits**:
- **60 requests per minute** across all endpoints
- **30 second** maximum query timeout
- **Query depth limit**: Maximum depth of 3 (added 2025)
- **No per-day/per-hour limits** beyond per-minute restriction

**Response codes**: 200 (success), 401 (expired or invalid token), 403 (access denied), 404 (not found), 429 (too many requests, "Throttled"), 500 (internal server error).

**Rate limit best practices**: Implement exponential backoff for 429 errors, use batch queries when possible, cache responses appropriately, add delays between requests (>1 second), and use `loading="lazy"` for image elements to prevent rate limiting.

**Usage restrictions**: Localhost access and API-to-API calls are allowed, but browser execution is blocked (must keep token secure). Cannot access other users' private data. Queries limited to: your own user data, public data, and data from users you follow. Disabled operators for performance: `_like`, `_nlike`, `_ilike`, `_niregex`, `_nregex`, `_iregex`, `_regex`, `_nsimilar`, `_similar`.

**Future plans**: OAuth support planned for 2025, developer allowlist for specific sites (planned), external application support (planned).

**Token lifecycle**: Tokens automatically expire after 1 year, all tokens reset on January 1st annually, and may be reset without notice during beta period.

## Calibre-web-automated: Multiple data access paths

Calibre-web-automated (CWA) is a Docker container fork of calibre-web combining the lightweight web UI with Calibre's full feature set. While CWA itself does not provide dedicated REST API endpoints, multiple programmatic access methods exist.

### Docker container shell access

Standard Docker exec commands provide full shell access to the running container:

```bash
# Interactive shell access
docker exec -it calibre-web-automated /bin/bash

# Or with docker-compose
docker compose exec calibre-web-automated /bin/bash

# Alpine-based images may use
docker exec -it calibre-web-automated /bin/sh
```

**Single command execution** without entering the shell:
```bash
# List library contents
docker exec calibre-web-automated ls /calibre-library

# Check calibre version
docker exec calibre-web-automated calibre --version

# Run calibredb commands
docker exec calibre-web-automated calibredb list --library-path=/calibre-library
```

**Python script execution** inside the container:
```bash
# Execute Python script from host
docker exec calibre-web-automated python3 /path/to/script.py

# Copy script into container and execute
docker cp script.py calibre-web-automated:/tmp/
docker exec calibre-web-automated python3 /tmp/script.py
```

### Database format and direct access

**Format**: SQLite3 database  
**Filename**: metadata.db  
**Location within container**: `/calibre-library/metadata.db`  
**Standard**: 100% compatible with standard Calibre desktop application

**Additional databases**:
- **CWA Database**: `/config/cwa.db` - Stores CWA-specific statistics and history
- **App Database**: `/config/app.db` - Calibre-Web configuration and user data

**Schema structure**: The metadata.db follows standard Calibre schema with key tables including `books` (core book records), `authors` (author information), `tags` (tag data), `series` (series information), `data` (file format information like EPUB, MOBI), `comments` (book descriptions), and `custom_columns_*` (user-defined custom fields).

**Direct database access methods**:

Using SQLite CLI:
```bash
# Enter container shell
docker exec -it calibre-web-automated /bin/bash

# Query database directly
sqlite3 /calibre-library/metadata.db

# Example queries
SELECT title, author_sort FROM books LIMIT 10;
SELECT name FROM tags;
```

Using Python:
```python
import sqlite3
conn = sqlite3.connect('/calibre-library/metadata.db')
cursor = conn.cursor()
cursor.execute("SELECT title FROM books")
print(cursor.fetchall())
```

**Critical warning**: Direct database write operations are NOT RECOMMENDED. SQLite3 locking can cause corruption if CWA is running. Read-only access is generally safe. Always backup before direct manipulation.

### Built-in export features via calibredb

CWA includes the full `calibredb` command-line tool providing comprehensive export capabilities.

**Export books with metadata**:
```bash
# Export specific books by ID
docker exec calibre-web-automated \
  calibredb export --library-path=/calibre-library \
  --to-dir=/tmp/export 1,2,3

# Export all books
docker exec calibre-web-automated \
  calibredb export --all \
  --library-path=/calibre-library \
  --to-dir=/tmp/export
```

Exports include all book formats (EPUB, MOBI, PDF, etc.), cover images, metadata in OPF XML format, and extra data files associated with books. Export options include `--formats EPUB,PDF` (specific formats only), `--dont-save-cover` (skip cover image), `--dont-write-opf` (skip metadata OPF file), `--single-dir` (export all to one folder), and `--template "{title}"` (custom filename template).

**Metadata export to CSV**:
```bash
# Export to CSV format
docker exec calibre-web-automated \
  calibredb list \
  --library-path=/calibre-library \
  --fields=title,authors,tags,series,pubdate \
  --separator="," > library.csv

# Export all fields as JSON
docker exec calibre-web-automated \
  calibredb list \
  --library-path=/calibre-library \
  --fields=all \
  --for-machine > library.json
```

**Available fields** include: author_sort, authors, comments, cover, formats, identifiers, isbn, languages, last_modified, pubdate, publisher, rating, series, series_index, size, tags, timestamp, title, uuid, and custom columns as `*field_name`.

**Generate comprehensive catalog**:
```bash
# Generate catalog
docker exec calibre-web-automated \
  calibredb catalog /tmp/catalog.csv \
  --library-path=/calibre-library

# With search filter
docker exec calibre-web-automated \
  calibredb catalog /tmp/catalog.csv \
  --library-path=/calibre-library \
  --search "tag:fiction"
```

Supported catalog formats include CSV (spreadsheet), XML (structured data), and EPUB, MOBI, AZW3 (e-book catalogs).

**JSON export for machine processing**:
```bash
# Export complete metadata as JSON
docker exec calibre-web-automated \
  calibredb list \
  --library-path=/calibre-library \
  --for-machine > metadata.json
```

The `--for-machine` flag outputs JSON-formatted data ideal for parsing by scripts and applications.

### Volume mount structure and file access

**Default volume configuration**:
```yaml
volumes:
  - /path/to/config:/config          # App config, logs, databases
  - /path/to/ingest:/cwa-book-ingest # Temporary ingest folder
  - /path/to/library:/calibre-library # Main Calibre library
```

**Direct file access from host**: Direct access to mounted directories is possible. The metadata.db is located at `<library_mount>/metadata.db`, books are organized as `<library_mount>/Author/Title/`, and config files are in `/config` mount including `app.db` (CWA settings).

**Copy files between container and host**:
```bash
# Copy from container to host
docker cp calibre-web-automated:/calibre-library/metadata.db ./backup/

# Copy from host to container
docker cp ./script.py calibre-web-automated:/tmp/
```

### Alternative access methods

**OPDS catalog**: CWA provides an OPDS feed for programmatic access at `http://localhost:8083/opds` in XML-based catalog standard format, suitable for e-reader apps and automated library browsers.

**Calibre Python API**: Available via `calibre.library.db` Python module inside the container with multi-reader, single-writer locking scheme:
```python
from calibre.library import db
db = db('/calibre-library').new_api
# Access database operations
```

Key API functions include `all_book_ids()`, `field_for(field, book_id)`, `all_field_names()`, and `search(query)`.

### Network considerations and limitations

**Network share warning**: CWA documentation explicitly states SQLite3 databases don't work well over NFS/CIFS, which can cause corruption due to file locking issues. If using network storage, ensure library folder is on local filesystem or well-supported network mount.

**Container permissions**: Default environment variables are PUID=1000 and PGID=1000. Ensure host filesystem permissions match these IDs to avoid access issues.

## Audiobook listening history: Format comparison

Listening history tracking varies significantly across audiobook platforms, from comprehensive REST APIs to limited or no export capabilities.

### BookPlayer iOS: Limited documented export

**Current export feature status**: The "Improved Export" feature was introduced in recent versions, described in the App Store as "Exports now include all book details, listening time, and notes for a comprehensive and seamless transfer of your data."

**Access method**: Via the Options menu → swipe left on book in library or use Edit button → select book → tap "..." button → Share/Export option.

**Known data included**: Book details (title, author, artwork), listening time/progress, notes/bookmarks (added in recent versions), and book completion status.

**Critical limitation**: Specific technical documentation about the exact export format (CSV vs JSON), column headers, and precise data structure is not publicly available in official documentation or GitHub repository. The app's export feature appears designed for data backup/transfer rather than detailed analytics.

**Inferred data structure** (based on app features):
```
Likely Fields:
- Book Title
- Author
- File Path/Name
- Current Progress (seconds or percentage)
- Total Duration
- Last Played Date/Time
- Completion Status (finished/unfinished)
- Notes (if any)
- Bookmarks (timestamps with optional notes)
```

### Audiobookshelf: Comprehensive REST API

Audiobookshelf provides the most comprehensive and accessible listening history data with full REST API documentation at api.audiobookshelf.org.

**Primary listening sessions endpoint**: GET `/api/users/{userId}/listening-sessions`

Returns detailed listening session history with pagination support. Query parameters include `itemsPerPage` (limit results per page) and `page` (page number, 0-indexed).

**Complete response structure** (JSON):
```json
{
  "sessions": [
    {
      "id": "play_c786ke3wajqzpno01w",
      "userId": "root",
      "libraryId": "lib_c1u6t4p45c35rf0nzd",
      "libraryItemId": "li_8gch9ve09orgn4fdz8",
      "bookId": "book_12345",
      "episodeId": null,
      "mediaType": "book",
      "mediaMetadata": {
        "title": "The Name of the Wind",
        "titleIgnorePrefix": "Name of the Wind",
        "subtitle": "The Kingkiller Chronicle: Day One",
        "authorName": "Patrick Rothfuss",
        "narratorName": "Nick Podehl",
        "seriesName": "The Kingkiller Chronicle",
        "genres": ["Fantasy"],
        "publishedYear": "2007",
        "publisher": "DAW Books",
        "isbn": "9780756404079",
        "asin": "B002UZMLXM",
        "language": "English",
        "explicit": false
      },
      "chapters": [
        {
          "id": 0,
          "start": 0,
          "end": 1834.56,
          "title": "Chapter 1: A Place for Demons"
        },
        {
          "id": 1,
          "start": 1834.56,
          "end": 3456.78,
          "title": "Chapter 2: A Beautiful Day"
        }
      ],
      "displayTitle": "The Name of the Wind",
      "displayAuthor": "Patrick Rothfuss",
      "duration": 27907.836,
      "playMethod": 0,
      "mediaPlayer": "audiobookshelf-app",
      "deviceInfo": {
        "deviceId": "12a4b5c6d7e8f9",
        "clientName": "Audiobookshelf",
        "clientVersion": "2.4.3",
        "manufacturer": "Apple",
        "model": "iPhone 14 Pro"
      },
      "serverVersion": "2.15.0",
      "date": "2025-10-22",
      "dayOfWeek": "Wednesday",
      "timeListening": 3642.5,
      "startTime": 12453.2,
      "currentTime": 16095.7,
      "startedAt": 1729612800000,
      "updatedAt": 1729616442500
    }
  ],
  "total": 147,
  "numPages": 15,
  "itemsPerPage": 10
}
```

**Field data types and meanings**:
- `timeListening`: Float - Duration listened in seconds during this session
- `startTime`: Float - Position in seconds where session started in book
- `currentTime`: Float - Position in seconds where session ended in book
- `startedAt`: Integer - Unix timestamp in milliseconds
- `updatedAt`: Integer - Unix timestamp in milliseconds
- `duration`: Float - Total book duration in seconds

**Additional endpoints**:

GET `/api/users/{userId}/listening-stats` - Returns aggregated listening statistics with totalTime, per-item statistics, daily breakdown, day-of-week breakdown, today's listening, and recent sessions.

GET `/api/me/progress` - Returns current user's media progress for all items with fields including id, libraryItemId, duration, progress, currentTime, isFinished, lastUpdate, startedAt, and finishedAt.

**Tracking granularity**: Session-level tracking where each listening session is recorded separately, timestamp precision at millisecond level (Unix timestamps), continuous progress tracking with position updates, device information tracking (which device/app was used), and chapter information including metadata and positions.

### Plex with third-party audiobook players

**Plex native functionality**: Plex does NOT have native audiobook support. Users rely on third-party metadata agents (Audnexus.bundle) and third-party player apps (Prologue, BookCamp, Chronicle).

**Plex session history API**: GET `/status/sessions/history/all`

URL format: `http://{server}:32400/status/sessions/history/all?X-Plex-Token={token}`

**Response format** (XML):
```xml
<?xml version="1.0" encoding="UTF-8"?>
<MediaContainer size="count">
  <Track 
    historyKey="/status/sessions/history/{id}"
    key="/library/metadata/{ratingKey}"
    ratingKey="{id}"
    librarySectionID="{id}"
    title="Book Title"
    grandparentTitle="Author Name"
    type="track"
    viewedAt="{unix_timestamp}"
    accountID="{id}"
    viewOffset="{milliseconds}"
    duration="{milliseconds}"
  />
</MediaContainer>
```

**Key fields**: `viewedAt` (Unix timestamp of when item was played), `viewOffset` (playback position in milliseconds), `duration` (total duration in milliseconds), `title` (track/book title), `grandparentTitle` (author/artist name).

**Limitations**: Treats audiobooks as music tracks, limited metadata specific to audiobooks, no native export feature for listening history, and requires parsing XML responses.

**Third-party player overview**:

**Prologue** (iOS, $4.99): Premium iOS app for Plex audiobooks with iCloud sync for playback position, bookmarks, listening history, and reading list. No public API or export feature. Data storage is local to device + iCloud sync.

**BookCamp** (iOS & Android, $12/year or $3/month): Subscription-based requiring Plex library with progress tracking, bookmarks, listening history, and statistics. No documented API or export feature. Data synced through Plex.

**Chronicle** (Android, free/premium): Free/Premium Android app for Plex (GitHub: github.com/mattttvaughn/chronicle) with offline support and variable playback speed (0.5x-3x). No public API or export feature. Progress sync on device and across devices via Plex, with chapter support (m4b) and sleep timer sessions.

**Critical finding**: None of the third-party Plex audiobook players offer data export. All sync listening position through Plex's tracking system which stores current playback position (milliseconds), last played timestamp, completion status, and device information.

### Platform comparison summary

| Platform | API Available | Export Format | Progress Tracking | Timestamps | Notes/Bookmarks |
|----------|--------------|---------------|-------------------|------------|----------------|
| BookPlayer | ❌ No | Limited (format unclear) | ✅ Per book | ✅ Last played | ✅ Yes |
| Audiobookshelf | ✅ Full REST API | JSON (via API) | ✅ Session-level | ✅ Millisecond precision | ✅ Yes |
| Plex | ✅ XML API | XML | ✅ Per track | ✅ Unix timestamps | ❌ No |
| Prologue | ❌ No | ❌ None | ✅ Position only | ✅ Via Plex | ✅ Yes (local) |
| BookCamp | ❌ No | ❌ None | ✅ Position + stats | ✅ Via Plex | ✅ Yes |
| Chronicle | ❌ No | ❌ None | ✅ Position only | ✅ Via Plex | ❌ No |

**Recommendation for unified database**: Audiobookshelf is the clear winner for analytics and detailed tracking with its well-documented REST API, session-level granular tracking, rich metadata (author, narrator, series, chapters), device tracking, progress percentages calculated automatically, multiple export options (JSON via API), and easy integration with analytics tools.

## Architectural recommendations for unified database

Based on the technical findings across all five research areas, the following architecture optimizes for data integrity, automation efficiency, and practical implementation.

### Database technology selection

**Recommendation: PostgreSQL over SQLite**

While the source systems predominantly use SQLite (KOReader, Calibre), PostgreSQL is strongly recommended for the unified consolidated database for several critical reasons:

**Data integrity advantages**:
- **ACID compliance at higher levels**: Better handling of concurrent operations during data sync processes
- **Write-ahead logging (WAL)**: More robust recovery from system crashes during automated imports
- **Foreign key enforcement**: Stronger referential integrity when consolidating data from multiple sources
- **Check constraints**: Better data validation at the database level

**Operational benefits**:
- **Concurrent access**: Multiple sync scripts or analysis tools can safely query while imports run
- **Better JSON support**: Native JSONB type ideal for storing variable metadata from APIs (Hardcover.app responses, Audiobookshelf sessions)
- **Full-text search**: Built-in support for searching book titles, authors, notes across all sources
- **Scheduled tasks**: Native pg_cron extension for maintenance operations

**Scalability considerations**:
- **Performance at scale**: Better query optimization for complex analytics across thousands of reading sessions
- **Indexing options**: More sophisticated index types (GiST, GIN) for specialized queries
- **Materialized views**: Efficient pre-computed statistics and aggregations

**When SQLite would be acceptable**: Single-user system with no concurrent access requirements, infrequent sync operations (daily or less), minimal complex querying or analytics, local-only deployment with no remote access needs, and total data under 100,000 reading sessions.

**Recommended schema structure**:
```sql
-- Core entities
CREATE TABLE books (
    id UUID PRIMARY KEY,
    title TEXT NOT NULL,
    authors TEXT[], -- Array for multiple authors
    isbn_13 TEXT,
    isbn_10 TEXT,
    asin TEXT,
    page_count INTEGER,
    series TEXT,
    publisher TEXT,
    publication_date DATE,
    source_system TEXT NOT NULL, -- 'koreader', 'calibre', 'hardcover'
    source_id TEXT,
    metadata JSONB, -- Flexible storage for system-specific fields
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Reading sessions (ebooks and audiobooks)
CREATE TABLE reading_sessions (
    id UUID PRIMARY KEY,
    book_id UUID REFERENCES books(id),
    source_system TEXT NOT NULL, -- 'koreader', 'audiobookshelf', 'plex'
    start_time TIMESTAMPTZ NOT NULL,
    end_time TIMESTAMPTZ,
    duration_seconds INTEGER,
    start_position JSONB, -- {page: X, percentage: Y, timestamp: Z}
    end_position JSONB,
    device_info JSONB, -- Device, app version, etc.
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Book-specific metadata from different sources
CREATE TABLE book_enrichment (
    id UUID PRIMARY KEY,
    book_id UUID REFERENCES books(id),
    source TEXT NOT NULL, -- 'hardcover', 'calibre', 'koreader'
    enrichment_data JSONB, -- Ratings, descriptions, tags, etc.
    fetched_at TIMESTAMPTZ DEFAULT NOW()
);

-- Notes and highlights
CREATE TABLE annotations (
    id UUID PRIMARY KEY,
    book_id UUID REFERENCES books(id),
    source_system TEXT NOT NULL,
    annotation_type TEXT, -- 'highlight', 'note', 'bookmark'
    content TEXT,
    position JSONB, -- Page number, timestamp, location, etc.
    created_at TIMESTAMPTZ NOT NULL
);

-- Indexes for common queries
CREATE INDEX idx_books_title ON books USING gin(to_tsvector('english', title));
CREATE INDEX idx_books_authors ON books USING gin(authors);
CREATE INDEX idx_sessions_book_time ON reading_sessions(book_id, start_time);
CREATE INDEX idx_sessions_time ON reading_sessions(start_time DESC);
CREATE INDEX idx_enrichment_book ON book_enrichment(book_id, source);
```

### Automation architecture strategy

**Recommendation: Scheduled local Python script with modular pipeline stages**

Given the mix of local data sources (KOReader SQLite, Calibre Docker container) and API data sources (Hardcover.app, Audiobookshelf), a scheduled local script architecture is most appropriate.

**Why scheduled local script over event-driven cloud functions**:

**Access to local data**: Direct access to local filesystems, Docker containers, and SQLite databases without requiring network transfer or cloud storage intermediaries. Cloud functions would require uploading all local data first.

**Cost efficiency**: No cloud function invocation costs, no data transfer costs, no cloud storage costs for intermediate data. Runs on existing hardware.

**Complexity reduction**: Single codebase in one location versus distributed functions with orchestration, state management, and error handling across cloud boundaries.

**API rate limit management**: Better control over Hardcover.app's 60 requests/minute limit with local script state and caching. Cloud functions may hit limits with parallel invocations.

**Debugging and monitoring**: Simpler logging and debugging on local system with full access to logs, file outputs, and process state. Cloud functions require separate monitoring infrastructure.

**When cloud functions would be appropriate**: Geographically distributed data sources requiring proximity to cloud APIs, need for automatic scaling during high-volume sync operations, requirement for serverless infrastructure with no local hosting capacity, or integration with other cloud-native services.

**Recommended implementation architecture**:

```python
# Pipeline stages with clear separation of concerns

class ReadingDataPipeline:
    def __init__(self, config):
        self.config = config
        self.db = PostgreSQLConnection(config.database)
        
    def run_full_sync(self):
        """Execute complete sync pipeline"""
        try:
            # Stage 1: Extract from local sources
            koreader_data = self.extract_koreader()
            calibre_data = self.extract_calibre()
            
            # Stage 2: Fetch from remote APIs
            audiobookshelf_data = self.extract_audiobookshelf()
            # Hardcover enrichment happens later per-book
            
            # Stage 3: Transform and deduplicate
            unified_books = self.deduplicate_books(
                koreader_data['books'],
                calibre_data['books']
            )
            
            # Stage 4: Enrich with Hardcover metadata
            enriched_books = self.enrich_with_hardcover(unified_books)
            
            # Stage 5: Load into database
            self.load_books(enriched_books)
            self.load_sessions(
                koreader_data['sessions'],
                audiobookshelf_data['sessions']
            )
            
            # Stage 6: Generate sync report
            self.generate_report()
            
        except Exception as e:
            self.handle_error(e)
            
    def extract_koreader(self):
        """Extract from KOReader SQLite database"""
        # Locate statistics.sqlite3 via WebDAV mount or Syncthing folder
        # Query book and page_stat_data tables
        # Return structured data
        pass
        
    def extract_calibre(self):
        """Extract from calibre-web-automated Docker container"""
        # Execute docker exec calibredb list --for-machine
        # Parse JSON output
        # Return structured data
        pass
        
    def extract_audiobookshelf(self):
        """Fetch from Audiobookshelf REST API"""
        # GET /api/users/{userId}/listening-sessions with pagination
        # Rate limit: No restrictions beyond general API limits
        # Return structured data with exponential backoff on errors
        pass
        
    def enrich_with_hardcover(self, books):
        """Enrich book metadata via Hardcover.app GraphQL API"""
        enriched = []
        for book in books:
            if book.isbn_13:
                # Rate limit: 60/min, implement throttling
                time.sleep(1.2)  # Conservative: 50 requests/minute
                metadata = self.fetch_hardcover_metadata(book.isbn_13)
                book.update_metadata(metadata)
            enriched.append(book)
        return enriched
```

**Scheduling recommendations**:

**Frequency**: Run daily at low-activity times (e.g., 3 AM local time) to minimize impact on source systems. More frequent sync (every 6-12 hours) if real-time analytics are important.

**Implementation options**:
- **Linux cron**: `0 3 * * * /usr/bin/python3 /path/to/sync_pipeline.py >> /var/log/reading_sync.log 2>&1`
- **systemd timer**: More robust with better error handling and dependency management
- **Python schedule library**: Within long-running Python service for more control

**Incremental vs full sync**: Use incremental sync after initial full sync by tracking `last_sync_time` in database, querying only records modified since last sync (using `last_open` in KOReader, `last_modified` in Calibre, `updatedAt` in Audiobookshelf), and performing full reconciliation sync weekly to catch any missed updates.

**Error handling and retry logic**:
```python
# Exponential backoff for API failures
def fetch_with_retry(url, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.get(url)
            if response.status_code == 429:  # Rate limited
                wait = (2 ** attempt) * 60  # 1min, 2min, 4min
                time.sleep(wait)
                continue
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)
```

### Conceptual data flow diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     DATA EXTRACTION STAGE                        │
└─────────────────────────────────────────────────────────────────┘
                                 │
        ┌────────────────────────┼────────────────────────┐
        │                        │                        │
        ▼                        ▼                        ▼
┌──────────────┐        ┌──────────────┐        ┌──────────────┐
│  KOReader    │        │   Calibre    │        │ Audiobook-   │
│  SQLite DB   │        │  Docker      │        │   shelf      │
│              │        │  Container   │        │   REST API   │
│ • statistics │        │              │        │              │
│   .sqlite3   │        │ • calibredb  │        │ • Listening  │
│ • book table │        │   list       │        │   sessions   │
│ • page_stat  │        │ • metadata   │        │ • Progress   │
│   _data      │        │   .db        │        │   data       │
└──────────────┘        └──────────────┘        └──────────────┘
        │                        │                        │
        │  Direct file access    │  Docker exec          │  HTTPS GET
        │  or WebDAV/Syncthing   │  commands             │  requests
        │                        │                        │
        └────────────────────────┼────────────────────────┘
                                 ▼
                        ┌─────────────────┐
                        │ Python Pipeline │
                        │   (Local Host)  │
                        │                 │
                        │ • Extract       │
                        │ • Transform     │
                        │ • Deduplicate   │
                        └─────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                    ENRICHMENT STAGE                              │
└─────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │ Hardcover.app   │
                        │  GraphQL API    │
                        │                 │
                        │ • ISBN lookup   │
                        │ • Metadata      │
                        │ • Page counts   │
                        │ Rate: 60/min    │
                        └─────────────────┘
                                 │
                          Enriched data
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                     LOAD \u0026 STORAGE STAGE                        │
└─────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │  PostgreSQL     │
                        │   Database      │
                        │                 │
                        │ • books         │
                        │ • reading_      │
                        │   sessions      │
                        │ • annotations   │
                        │ • book_         │
                        │   enrichment    │
                        └─────────────────┘
                                 │
                     Unified, queryable data
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                    CONSUMPTION STAGE                             │
└─────────────────────────────────────────────────────────────────┘
                                 │
        ┌────────────────────────┼────────────────────────┐
        │                        │                        │
        ▼                        ▼                        ▼
┌──────────────┐        ┌──────────────┐        ┌──────────────┐
│  Analytics   │        │  Dashboard   │        │  Export to   │
│  Queries     │        │  (Grafana,   │        │  External    │
│              │        │   Metabase)  │        │  Tools       │
└──────────────┘        └──────────────┘        └──────────────┘
```

**Key data flow characteristics**:

**Parallel extraction**: KOReader, Calibre, and Audiobookshelf extractions can run concurrently in separate threads/processes to reduce total sync time.

**Sequential enrichment**: Hardcover.app enrichment must be sequential due to rate limits (60/min), with throttling between requests.

**Batch loading**: Database inserts/updates should use batch operations (INSERT ... ON CONFLICT, COPY statements) for performance.

**Idempotent operations**: All pipeline stages designed to be safely re-runnable without data duplication using upserts and unique constraints.

### Security best practices for credentials

**API key and credential management**:

**Environment variables** (recommended approach):
```bash
# .env file (add to .gitignore)
HARDCOVER_API_TOKEN=your_token_here
AUDIOBOOKSHELF_API_TOKEN=your_token_here
POSTGRES_PASSWORD=secure_password
CALIBRE_HOST=localhost
CALIBRE_PORT=8083
```

```python
# Load in Python script
from dotenv import load_dotenv
import os

load_dotenv()
HARDCOVER_TOKEN = os.getenv('HARDCOVER_API_TOKEN')
```

**Alternative: Secrets management tools** for production environments:
- **HashiCorp Vault**: Enterprise-grade secrets management
- **AWS Secrets Manager / Azure Key Vault**: Cloud provider options
- **pass**: Unix password manager with GPG encryption
- **SOPS**: Encrypted file storage for configuration

**File permissions**: Ensure configuration files with credentials have restricted permissions:
```bash
chmod 600 .env
chmod 700 /path/to/config/
```

**Docker secrets** for calibre-web-automated access:
```yaml
# docker-compose.yml
services:
  calibre-web-automated:
    environment:
      - POSTGRES_PASSWORD_FILE=/run/secrets/postgres_password
    secrets:
      - postgres_password

secrets:
  postgres_password:
    file: ./secrets/postgres_password.txt
```

**API token rotation**: 
- **Hardcover.app tokens**: Expire after 1 year, all reset January 1st. Monitor expiration and implement token refresh logic.
- **Audiobookshelf tokens**: Check documentation for expiration policy and implement rotation procedure.
- **Store token creation dates** in configuration for proactive rotation.

**Network security**:
- **PostgreSQL**: Bind to localhost only unless remote access required. Use SSL/TLS for remote connections.
- **Hardcover/Audiobookshelf APIs**: Always use HTTPS. Validate SSL certificates in code (`verify=True` in requests).
- **Docker container access**: Restrict Docker socket access to authorized users only.

**Logging security**:
- **Never log credentials**: Use sanitization functions to remove tokens from logs
- **Sanitize URLs**: Remove tokens from logged API request URLs
```python
import re

def sanitize_url(url):
    return re.sub(r'(token=|Bearer\s+)[^\s&]+', r'\1***', url)
```

**Backup security**:
- **Encrypt database backups** containing reading history and personal data
- **Secure backup locations**: Use encrypted storage for backup files
- **Access control**: Limit backup file access to necessary users/processes only

## Implementation roadmap

**Phase 1: Foundation** (Week 1-2)
- Set up PostgreSQL database with schema
- Implement basic extraction for one data source (start with Calibre as simplest)
- Establish credential management system
- Create basic logging and error handling framework

**Phase 2: Core Pipeline** (Week 3-4)
- Implement extraction for KOReader and Audiobookshelf
- Build deduplication and transformation logic
- Create database loading functions with upsert logic
- Test incremental sync capabilities

**Phase 3: Enrichment** (Week 5)
- Integrate Hardcover.app API with rate limiting
- Implement ISBN matching logic
- Add metadata enrichment to pipeline
- Create caching layer to minimize redundant API calls

**Phase 4: Automation** (Week 6)
- Set up scheduled execution (cron/systemd timer)
- Implement comprehensive error handling and retry logic
- Create monitoring and alerting for pipeline failures
- Build sync status reporting

**Phase 5: Optimization** (Week 7+)
- Performance tuning for large datasets
- Add analytics views and materialized views
- Create dashboard for unified reading statistics
- Document maintenance procedures

This architecture provides a robust, maintainable foundation for consolidating reading data from multiple sources while maintaining data integrity, security, and operational efficiency.