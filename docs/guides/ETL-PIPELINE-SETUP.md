# BookHelper ETL Pipeline Setup & Operations Guide

**Story:** 3.2: Build ETL pipeline for statistics extraction
**Status:** Implemented
**Last Updated:** 2025-10-31

---

## Overview

The BookHelper ETL pipeline automatically extracts reading statistics from KOReader (via Syncthing backup on Raspberry Pi) and loads them into Neon.tech PostgreSQL for unified reading analytics.

### Architecture

```
KOReader on Boox Device
        ↓ (via KOSync)
statistics.sqlite3
        ↓ (via Syncthing)
RPi Backup: /home/alexhouse/backups/koreader-statistics/statistics.sqlite3
        ↓ (nightly ETL)
Python ETL Script: extract_koreader_stats.py
        ↓ (transforms + aggregates)
Neon.tech PostgreSQL
        ↓ (SQL analytics)
Reading Analytics
```

### Data Flow

1. **Source:** KOReader `statistics.sqlite3` backup on RPi
   - `book` table: 16 books (titles, page counts, file hashes)
   - `page_stat_data` table: 4,027 reading session records

2. **Transformation:**
   - Extract books and map to Neon.tech `books` table
   - Aggregate `page_stat_data` into sessions (30-minute gap threshold)
   - Transform timestamps (Unix → PostgreSQL TIMESTAMP)
   - Handle duplicates (ON CONFLICT clauses)

3. **Target:** Neon.tech PostgreSQL
   - Insert/update into `books` table
   - Append to `reading_sessions` table
   - Maintain audit trail with `created_at` timestamps

---

## Prerequisites

### RPi Setup (One-time)

1. **Python 3.9+** (verify):
   ```bash
   python3 --version
   ```

2. **SQLite3 CLI** (for manual inspection):
   ```bash
   sudo apt update
   sudo apt install -y sqlite3
   ```

3. **PostgreSQL client** (optional, for manual testing):
   ```bash
   sudo apt install -y postgresql-client
   ```

4. **Python dependencies** (install):
   ```bash
   pip3 install psycopg2-binary python-dotenv
   ```

5. **Statistics backup** location verified:
   ```bash
   ls -lh /home/alexhouse/backups/koreader-statistics/statistics.sqlite3
   ```

6. **Log directory** exists:
   ```bash
   mkdir -p /home/alexhouse/logs
   chmod 750 /home/alexhouse/logs
   ```

### Database Prerequisites

- ✓ Neon.tech PostgreSQL database created (Story 1.4)
- ✓ Schema tables initialized:
  - `authors`
  - `publishers`
  - `books`
  - `reading_sessions`
  - `book_editions`
  - `sync_status` (optional)
- ✓ Views created:
  - `book_stats`
  - `reading_timeline`
  - And others per Story 1.4

### Environment Variables

The ETL script requires database credentials. Set these **before running the script**:

```bash
export NEON_HOST="<your-neon-host>.neon.tech"
export NEON_USER="<database-user>"
export NEON_PASSWORD="<database-password>"
export NEON_DATABASE="<database-name>"
```

**Optional overrides:**

```bash
export DEVICE_ID="boox-palma-2"                    # Default
export SESSION_GAP_MINUTES=30                       # Default
export KOREADER_BACKUP="/home/alexhouse/backups/koreader-statistics/statistics.sqlite3"
export ETL_LOG_PATH="/home/alexhouse/logs/etl.log"
```

---

## Installation

### 1. Copy ETL Script to RPi

From your Mac/development machine:

```bash
scp resources/scripts/extract_koreader_stats.py alexhouse@<rpi-ip>:/home/alexhouse/etl/
ssh alexhouse@<rpi-ip> chmod +x /home/alexhouse/etl/extract_koreader_stats.py
```

Or manually on RPi:

```bash
mkdir -p /home/alexhouse/etl
# Copy extract_koreader_stats.py to /home/alexhouse/etl/
chmod +x /home/alexhouse/etl/extract_koreader_stats.py
```

### 2. Create Environment File

On RPi, create `/home/alexhouse/.env.etl`:

```bash
cat > /home/alexhouse/.env.etl << 'EOF'
NEON_HOST="your-neon-host.neon.tech"
NEON_USER="postgres"
NEON_PASSWORD="your-secure-password"
NEON_DATABASE="bookhelper"

# Optional
DEVICE_ID="boox-palma-2"
SESSION_GAP_MINUTES=30
KOREADER_BACKUP="/home/alexhouse/backups/koreader-statistics/statistics.sqlite3"
ETL_LOG_PATH="/home/alexhouse/logs/etl.log"
EOF

chmod 600 /home/alexhouse/.env.etl
```

**⚠️ Security Note:** Never commit `.env.etl` to git. It contains database credentials.

### 3. Install Systemd Timer (Preferred)

For automatic nightly execution at 2 AM:

```bash
# Copy systemd files to RPi
scp resources/systemd/bookhelper-etl.service alexhouse@<rpi-ip>:/tmp/
scp resources/systemd/bookhelper-etl.timer alexhouse@<rpi-ip>:/tmp/

# On RPi, install as root:
sudo cp /tmp/bookhelper-etl.service /etc/systemd/system/
sudo cp /tmp/bookhelper-etl.timer /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable bookhelper-etl.timer
sudo systemctl start bookhelper-etl.timer
```

**Verify installation:**

```bash
sudo systemctl status bookhelper-etl.timer
sudo systemctl list-timers bookhelper-etl.timer
```

### 4. Alternative: Cron Job

If you prefer cron instead of systemd:

```bash
crontab -e
```

Add this line:

```cron
# Run ETL at 2 AM daily
0 2 * * * source /home/alexhouse/.env.etl && /usr/bin/python3 /home/alexhouse/etl/extract_koreader_stats.py >> /home/alexhouse/logs/etl.log 2>&1
```

---

## Manual Execution

### Test with Dry-Run Mode

Preview what would be loaded **without** writing to database:

```bash
source /home/alexhouse/.env.etl
python3 /home/alexhouse/etl/extract_koreader_stats.py --dry-run
```

**Expected output:**

```
[INFO] ===============================================================================
[INFO] ETL Pipeline: KOReader Statistics → Neon.tech PostgreSQL
[INFO] ===============================================================================
[INFO] Started at 2025-10-31 14:30:00 UTC
[INFO] Mode: DRY-RUN
[INFO] Source: /home/alexhouse/backups/koreader-statistics/statistics.sqlite3
[INFO] Target: your-host.neon.tech/bookhelper
[INFO] Device: boox-palma-2
[INFO] Session Gap Threshold: 30 minutes
...
[INFO] [DRY-RUN] Would insert 16 books
[INFO] [DRY-RUN] Would insert 4027 reading sessions
...
[INFO] ===============================================================================
```

### Run ETL (Normal Mode)

Load data into Neon.tech (writes to database):

```bash
source /home/alexhouse/.env.etl
python3 /home/alexhouse/etl/extract_koreader_stats.py
```

**Expected output:**

```
[INFO] Inserted 16 new books into Neon.tech (duplicates skipped)
[INFO] Inserted 4027 new reading sessions (duplicates skipped)
```

### Check Logs

View ETL execution logs:

```bash
tail -f /home/alexhouse/logs/etl.log

# Or search for specific run:
grep "2025-10-31" /home/alexhouse/logs/etl.log

# View journal logs (systemd timer):
sudo journalctl -u bookhelper-etl.service -n 50
```

---

## Verification & Testing

### Validate Data in Neon.tech

After running ETL, verify data loaded correctly:

#### Using psql CLI:

```bash
psql -h <neon-host> -U <user> -d bookhelper -c "
SELECT COUNT(*) as total_books,
       COUNT(DISTINCT source) as sources
FROM books;
"
```

**Expected:** `16 books from koreader source`

#### Count reading sessions:

```bash
psql -h <neon-host> -U <user> -d bookhelper -c "
SELECT COUNT(*) as total_sessions,
       COUNT(DISTINCT book_id) as unique_books,
       MIN(start_time) as earliest_session,
       MAX(start_time) as latest_session
FROM reading_sessions
WHERE data_source = 'koreader';
"
```

**Expected:** `~4,027 sessions across 16 books`

#### Spot-check sample records:

```bash
psql -h <neon-host> -U <user> -d bookhelper -c "
SELECT
  b.title,
  COUNT(rs.session_id) as session_count,
  SUM(rs.duration_minutes) as total_minutes,
  SUM(rs.pages_read) as total_pages
FROM books b
LEFT JOIN reading_sessions rs ON b.book_id = rs.book_id
WHERE b.source = 'koreader'
GROUP BY b.book_id, b.title
ORDER BY session_count DESC
LIMIT 5;
"
```

### Test Duplicate Handling

Run ETL twice on same backup file:

```bash
# First run
python3 /home/alexhouse/etl/extract_koreader_stats.py
# Check logs: "Inserted 4027 new reading sessions"

# Second run
python3 /home/alexhouse/etl/extract_koreader_stats.py
# Check logs: "Inserted 0 new reading sessions (all duplicates skipped)"
```

### Validate Schema Alignment

Verify ETL output matches Neon.tech schema:

```sql
-- Check books table structure
\d bookhelper.public.books

-- Check reading_sessions table structure
\d bookhelper.public.reading_sessions

-- Verify constraints are in place
SELECT constraint_name, constraint_type
FROM information_schema.table_constraints
WHERE table_name IN ('books', 'reading_sessions');
```

---

## Monitoring & Troubleshooting

### View Systemd Timer Status

```bash
# Check if timer is active
sudo systemctl status bookhelper-etl.timer

# View next scheduled run
sudo systemctl list-timers bookhelper-etl.timer

# View recent executions
sudo journalctl -u bookhelper-etl.service --since "1 hour ago"
```

### Check Log Rotation

Logs are automatically rotated daily:

```bash
# View log files
ls -lh /home/alexhouse/logs/

# Check current log size
du -h /home/alexhouse/logs/etl.log
```

### Common Issues

#### "Failed to connect to Neon.tech"

**Cause:** Invalid credentials or network issue

**Solution:**

```bash
# Test credentials manually
source /home/alexhouse/.env.etl
psql -h $NEON_HOST -U $NEON_USER -d $NEON_DATABASE -c "SELECT 1;"

# Check network connectivity
ping <neon-host>
```

#### "Required table 'books' not found"

**Cause:** Schema not initialized in Neon.tech

**Solution:**

Re-run Story 1.4 schema initialization script

#### "Duplicate insertion errors"

**Cause:** Integrity constraint violations

**Solution:**

The ETL script handles duplicates automatically via `ON CONFLICT` clauses. Logs will show records skipped. Check logs for specific errors.

#### ETL running slowly

**Cause:** Large backup file or slow network

**Monitor performance:**

```bash
# Check ETL script memory usage during execution
watch -n 1 'ps aux | grep extract_koreader_stats'

# Check backup file size
ls -lh /home/alexhouse/backups/koreader-statistics/statistics.sqlite3

# Performance target: <30 seconds for typical backup
```

---

## Configuration Reference

### ETL Script Options

```bash
usage: extract_koreader_stats.py [-h] [--dry-run]

options:
  -h, --help     show this help message and exit
  --dry-run      Preview what would be loaded without writing
```

### Environment Variables

| Variable | Required | Default | Purpose |
|----------|----------|---------|---------|
| `NEON_HOST` | Yes | — | Neon.tech PostgreSQL hostname |
| `NEON_USER` | Yes | — | Database username |
| `NEON_PASSWORD` | Yes | — | Database password |
| `NEON_DATABASE` | Yes | — | Database name |
| `DEVICE_ID` | No | `boox-palma-2` | Device identifier for sessions |
| `SESSION_GAP_MINUTES` | No | `30` | Minutes threshold for session aggregation |
| `KOREADER_BACKUP` | No | `/home/alexhouse/backups/koreader-statistics/statistics.sqlite3` | Backup file location |
| `ETL_LOG_PATH` | No | `/home/alexhouse/logs/etl.log` | Log file location |

### Systemd Timer

```bash
# Trigger time (UTC)
OnCalendar=*-*-* 02:00:00  # 2 AM every day

# Randomization (±5 minutes to avoid load spikes)
RandomizedDelaySec=5min

# Run missed execution if system was offline
Persistent=true
```

---

## Schema Mapping Reference

### Books Table

KOReader fields → Neon.tech schema:

| KOReader | Neon Field | Type | Notes |
|----------|-----------|------|-------|
| `id` | (not stored) | — | Local ID; use file_hash instead |
| `title` | `title` | VARCHAR(255) | Book title |
| `pages` | `page_count` | INT | Page count |
| `language` | `language` | CHAR(2) | ISO 639-1 code |
| `md5` | `file_hash` | VARCHAR(32) | Deduplication key |
| `notes` | `notes` | INT | Annotation count |
| `highlights` | `highlights` | INT | Highlight count |
| — | `source` | VARCHAR(50) | Constant: 'koreader' |
| — | `device_stats_source` | VARCHAR(100) | Constant: 'statistics.sqlite3' |

### Reading Sessions Table

Aggregated `page_stat_data` → `reading_sessions`:

| KOReader | Neon Field | Type | Transform |
|----------|-----------|------|-----------|
| `id_book` | `book_id` | INT | Lookup by file_hash |
| `start_time` | `start_time` | TIMESTAMP | Unix epoch → UTC |
| `duration` | `duration_minutes` | INT | Sum of aggregated records |
| `page` | `pages_read` | INT | Max page in session |
| — | `device` | VARCHAR(50) | Constant: device_id param |
| — | `media_type` | VARCHAR(20) | Constant: 'ebook' |
| — | `data_source` | VARCHAR(50) | Constant: 'koreader' |
| — | `read_instance_id` | UUID | Generated UUID per session |
| — | `read_number` | INT | Constant: 1 (first read) |

### Session Aggregation Logic

**Algorithm:** Group consecutive `page_stat_data` by:
1. Book ID (if changes → new session)
2. Time gap (if > 30 minutes → new session)

**Example:**

```
page_stat_data records:
10:00-10:15 (15 min) ─┐
10:20-10:35 (15 min) ├→ Session 1 (30 min, max page 25)
                      │
11:45-12:00 (15 min) ─┤ (70-minute gap)
12:05-12:20 (15 min) ─┴→ Session 2 (30 min, max page 35)
```

---

## Maintenance

### Log Rotation

Logs are rotated automatically via logrotate (if configured):

```bash
# Check logrotate configuration (optional)
sudo cat /etc/logrotate.d/bookhelper-etl 2>/dev/null || echo "Not configured"

# Manual rotation if needed
sudo logrotate -f /etc/logrotate.d/bookhelper-etl
```

### Database Maintenance

Periodically verify database health:

```bash
-- Check for constraint violations
SELECT COUNT(*) FROM reading_sessions
WHERE duration_minutes <= 0;  -- Should be 0

-- Check for orphaned sessions (book_id not in books table)
SELECT COUNT(*) FROM reading_sessions rs
WHERE NOT EXISTS (SELECT 1 FROM books b WHERE b.book_id = rs.book_id);

-- View deduplication effectiveness
SELECT
  data_source,
  COUNT(*) as sessions,
  COUNT(DISTINCT start_time) as unique_starts
FROM reading_sessions
GROUP BY data_source;
```

### Backup Verification

Ensure Syncthing backup is working:

```bash
# Check backup file timestamp (should be recent)
stat /home/alexhouse/backups/koreader-statistics/statistics.sqlite3

# Verify file integrity
sqlite3 /home/alexhouse/backups/koreader-statistics/statistics.sqlite3 "PRAGMA integrity_check;"
# Expected output: "ok"
```

---

## Support & Troubleshooting

### Getting Help

1. **Check logs first:**
   ```bash
   tail -100 /home/alexhouse/logs/etl.log
   ```

2. **Verify environment:**
   ```bash
   source /home/alexhouse/.env.etl
   echo $NEON_HOST $NEON_USER  # Should show values, not passwords
   ```

3. **Test connectivity:**
   ```bash
   psql -h $NEON_HOST -U $NEON_USER -d $NEON_DATABASE -c "SELECT COUNT(*) FROM books;"
   ```

### Performance Expectations

| Metric | Target | Typical |
|--------|--------|---------|
| Books extracted | — | 16 |
| Sessions aggregated | — | 4,027 |
| ETL runtime | <30 seconds | 8-12 seconds |
| Books inserted | First run: 16 | Subsequent: 0 (duplicates) |
| Sessions inserted | First run: 4,027 | Subsequent: 0 (duplicates) |
| Memory usage | <200 MB | ~100 MB |

---

## Next Steps

### Story 3.3: Hardcover API Integration

Once Story 3.2 is operational:

1. Extend ETL script to call Hardcover API
2. Enrich books table with metadata (genres, ratings, authors)
3. Populate author and publisher dimensions
4. Update reading_sessions with tandem read detection

### Story 4.1+: Multi-Source Analytics

Future enhancement to support:
- Kindle/Audible statistics
- BookPlayer audiobook sessions
- Tandem reading (ebook + audiobook simultaneously)
- Cross-device reading continuity

---

## Related Documentation

- [SCHEMA-DOCUMENTATION.md](guides/SCHEMA-DOCUMENTATION.md) - Full database schema
- [ETL-MAPPING-GUIDE.md](guides/ETL-MAPPING-GUIDE.md) - Detailed field mappings
- [STATISTICS-BACKUP-SETUP.md](STATISTICS-BACKUP-SETUP.md) - Backup configuration
- [Story 1.4](stories/1-4-unified-database-schema.md) - Schema initialization
- [Story 3.1](stories/3-1-configure-one-way-statistics-backup-from-boox-to-rpi.md) - Backup setup
