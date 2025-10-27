# Task 5: Initialize Test Library with Sample Books

**Story:** 1.1 - Deploy Calibre-Web-Automated on Raspberry Pi 4
**Task ID:** 1.1.5
**Acceptance Criteria:** AC3, AC5 - Library initialized with 20+ books, scan completes without crashes/OOM

---

## Overview

This task loads 20+ sample books into the CWA library via automatic ingestion. Success criteria:
- All 20+ books copied to ingest folder
- CWA automatically processes and imports books
- All books appear in the library with no errors
- No OOM (Out of Memory) errors or container restarts

**Duration:** 15-20 minutes (including automatic ingestion time)

---

## Part 1: Prepare Test Books

### Option A: Use Public Domain Books (Recommended)

Create a directory with sample books:
```bash
# On RPi, create temp directory
mkdir -p ~/test_books
cd ~/test_books

# Download sample EPUB files from Project Gutenberg
# Using wget to download multiple books

cat > download_books.sh << 'EOF'
#!/bin/bash

# Project Gutenberg EPUB URLs (20+ books)
BOOKS=(
  "https://www.gutenberg.org/cache/epub/84/pg84.epub"      # Frankenstein
  "https://www.gutenberg.org/cache/epub/1661/pg1661.epub"  # Sherlock Holmes
  "https://www.gutenberg.org/cache/epub/98/pg98.epub"      # Tale of Two Cities
  "https://www.gutenberg.org/cache/epub/11/pg11.epub"      # Alice in Wonderland
  "https://www.gutenberg.org/cache/epub/1342/pg1342.epub"  # Pride and Prejudice
  "https://www.gutenberg.org/cache/epub/4300/pg4300.epub"  # Ulysses
  "https://www.gutenberg.org/cache/epub/174/pg174.epub"    # Picture of Dorian Gray
  "https://www.gutenberg.org/cache/epub/1497/pg1497.epub"  # The Odyssey
  "https://www.gutenberg.org/cache/epub/2701/pg2701.epub"  # Moby Dick
  "https://www.gutenberg.org/cache/epub/6130/pg6130.epub"  # Jane Eyre
  "https://www.gutenberg.org/cache/epub/1661/pg1661.epub"  # The Adventures of Sherlock Holmes
  "https://www.gutenberg.org/cache/epub/3825/pg3825.epub"  # The Scarlet Letter
  "https://www.gutenberg.org/cache/epub/2814/pg2814.epub"  # Anna Karenina
  "https://www.gutenberg.org/cache/epub/27827/pg27827.epub"  # Crime and Punishment
  "https://www.gutenberg.org/cache/epub/64317/pg64317.epub"  # Dracula
  "https://www.gutenberg.org/cache/epub/514/pg514.epub"    # Little Women
  "https://www.gutenberg.org/cache/epub/1258/pg1258.epub"  # The Three Musketeers
  "https://www.gutenberg.org/cache/epub/8/pg8.epub"        # Wuthering Heights
  "https://www.gutenberg.org/cache/epub/4085/pg4085.epub"  # The Voyage Out
  "https://www.gutenberg.org/cache/epub/7849/pg7849.epub"  # Great Expectations
  "https://www.gutenberg.org/cache/epub/1274/pg1274.epub"  # Robinson Crusoe
  "https://www.gutenberg.org/cache/epub/2500/pg2500.epub"  # Don Quixote
)

echo "Downloading ${#BOOKS[@]} test books from Project Gutenberg..."
for i in "${!BOOKS[@]}"; do
  url="${BOOKS[$i]}"
  filename="book_$(printf "%02d" $((i+1))).epub"

  echo "[$((i+1))/${#BOOKS[@]}] Downloading $filename..."
  wget -q "$url" -O "$filename"

  # Check if download succeeded
  if [ -f "$filename" ] && [ -s "$filename" ]; then
    size=$(du -h "$filename" | cut -f1)
    echo "  ✓ Downloaded: $size"
  else
    echo "  ✗ Failed to download"
    rm -f "$filename"
  fi
done

echo ""
echo "Download complete. Books in: $(pwd)"
ls -lh *.epub | wc -l
EOF

chmod +x download_books.sh
./download_books.sh
```

### Option B: Use Local PDF Files

If you have local PDF files:
```bash
# Copy your PDFs to the test directory
cp ~/Documents/*.pdf ~/test_books/
cp ~/Downloads/*.pdf ~/test_books/

# Verify
ls -lh ~/test_books/
```

### Option C: Create Minimal Test Files

For quick testing (not representative):
```bash
# Create dummy EPUB files
for i in {1..20}; do
  cp /usr/share/doc/shared-mime-info/README ~/test_books/test_book_$i.pdf
done
```

**Verify you have 20+ files:**
```bash
ls ~/test_books/ | wc -l
# Should show >= 20
```

---

## Part 2: Copy Books to CWA Ingest Folder

### Important: Volume Mount Note

The `docker-compose.yml` mounts volumes as follows:
```yaml
volumes:
  - /library/ingest:/cwa-book-ingest      # Ingest folder for new books
  - /library:/calibre-library              # Final library after processing
```

- **Ingest folder** (`/library/ingest` on RPi → `/cwa-book-ingest` in container): Place books here for automatic processing
- **Library folder** (`/library` on RPi → `/calibre-library` in container): Final destination after CWA processes books

### Step 1: Copy Files to /library/ingest

```bash
# Create ingest directory if it doesn't exist
mkdir -p /library/ingest

# Copy all books to CWA ingest folder
cp ~/test_books/* /library/ingest/

# Verify copy
ls -lh /library/ingest/ | head -25
# Should show 20+ book files
```

### Step 2: Verify File Permissions

```bash
# Check permissions (on RPi host)
ls -l /library/ingest/ | head -10
chmod 644 /library/ingest/*

# Verify container can see ingest folder
docker compose exec cwa ls -la /cwa-book-ingest | head -10
# Should show your book files
```

### Step 3: Important Note on File Ownership

⚠️ Ensure files are owned by the container user (UID 1000):
```bash
# Check current owner
ls -l /library/ingest/

# If owned by root, change ownership
sudo chown 1000:1000 /library/ingest/*

# Verify
ls -l /library/ingest/ | head -5
```

---

## Part 3: Monitor Automatic Book Ingestion

### How CWA Ingest Works

Books placed in `/cwa-book-ingest` are **automatically processed** by CWA:
1. Files are analyzed and converted if necessary
2. Books are imported into the Calibre library
3. Files are deleted from ingest folder after successful import

This process happens automatically. No manual scan button needed.

### Step 1: Monitor Resource Usage During Ingestion

In a separate terminal, start monitoring:
```bash
# Terminal 1: Monitor system resources
watch -n 2 'docker stats calibre-web-automated'

# Terminal 2: Monitor CWA logs (watch for ingest progress)
docker compose logs -f cwa
```

CWA will begin processing books automatically. Watch for log messages indicating:
- Books being analyzed
- Conversion in progress (if needed)
- Books being imported into library

### Step 2: If Books Don't Auto-Ingest - Manual Trigger

If after 2-3 minutes books haven't appeared in the library:

1. Open CWA web UI: `http://raspberrypi.local:8083`
2. Log in with admin credentials
3. Look for **"Library Refresh"** button on the upper navbar
4. Click it to manually trigger ingestion
5. Monitor logs for progress

### Step 3: Common Issue - Permission Problems

If books aren't being ingested, it's likely a permission issue:

```bash
# Check file ownership in ingest folder
ls -l /library/ingest/

# Must be owned by user 1000 (alexhouse), not root
# If owned by root, change it:
sudo chown 1000:1000 /library/ingest/*

# Then delete any partially processed books from ingest folder
# (CWA leaves them there if they fail)
ls /library/ingest/

# Wait 30 seconds and check logs again
docker compose logs -f cwa | grep -i "ingest\|error\|import"
```

---

## Part 4: Expected Behavior During Ingestion

### Expected CWA Logs Output

**Successful ingestion:**
```
[INFO] Ingest: Processing /cwa-book-ingest/book_01.epub
[INFO] Ingest: Analyzing metadata for book_01.epub
[INFO] Ingest: Importing book_01.epub to library
[INFO] Ingest: Processing /cwa-book-ingest/book_02.epub
...
[INFO] Ingest: Successfully imported 20 books
[INFO] Ingest: Cleaning up processed files
```

**Docker Stats (should see activity):**
```
CONTAINER                CPU %    MEM USAGE
calibre-web-automated    15-30%   600-800 MiB / 1.5GiB
```

### Error Indicators (Watch For)

```
❌ PERMISSION ERRORS:
   "Permission denied"
   "Cannot read file"
   "Operation not permitted"
   → Solution: Check file ownership with ls -l /library/ingest/

❌ MEMORY ERRORS:
   "Out of memory"
   "OOMKilled"
   "Container restart"
   → Solution: Reduce number of books or increase memory allocation

❌ DATABASE ERRORS:
   "SQLite locked"
   "Database corruption"
   → Solution: Restart container and retry

❌ CONVERSION ERRORS:
   "Cannot convert format"
   "Unsupported file type"
   → Solution: Ensure files are valid EPUB/PDF; check CWA settings
```

---

## Part 5: Verify Library Import

### Step 1: Check Library via Web UI

1. In CWA UI, navigate: **Books → All Books**
2. Verify:
   - [ ] Shows 20+ books
   - [ ] Metadata displays (title, author, cover art)
   - [ ] No error messages

### Step 2: Count Books in Database

```bash
# Query library count from Calibre database
cwa bash -c 'sqlite3 /calibre-library/metadata.db "SELECT COUNT(*) FROM books;"'

# Should output: 20 (or your book count)
```

### Step 3: Test Search

In CWA UI:
1. Click **Search**
2. Search for a book title (e.g., "Frankenstein")
3. Verify result appears

### Step 4: Test Book Detail Page

1. Click on any book
2. Verify detail page loads with:
   - [ ] Title and author
   - [ ] Cover art (if available)
   - [ ] Description (if available)
   - [ ] No errors or timeouts

---

## Part 6: Validation Checklist

### Memory Constraints (AC4, AC5)

During ingestion:
- [ ] Memory usage < 1.5GB (resource limit)
- [ ] No OOM errors in logs
- [ ] No container restarts
- [ ] Peak memory < 1.0GB (safety margin)

After ingestion:
- [ ] Memory returns to baseline (<600 MB idle)
- [ ] No memory leaks evident

### Library Integrity (AC3, AC5)

- [ ] All 20+ books imported successfully
- [ ] Books visible in web UI
- [ ] Book search works
- [ ] Detail pages load without errors
- [ ] Cover art displays (if included in source)

### Error Conditions (AC5)

- [ ] No crashes during ingestion
- [ ] No OOM killer invocations
- [ ] No "permission denied" errors
- [ ] All books successfully moved to library
- [ ] Ingest folder cleaned after processing

---

## Troubleshooting

### Issue: Books Not Appearing in Library After Ingest

**Check 1:** Verify files are in ingest folder
```bash
ls -la /library/ingest/
# Files should be there (unless they've already been processed and deleted)
```

**Check 2:** Check container can see ingest folder
```bash
docker compose exec cwa ls -la /cwa-book-ingest/
# Should match the files above
```

**Check 3:** Check CWA logs for ingest errors
```bash
docker compose logs cwa | grep -i "ingest\|error\|import\|permission"
```

**Check 4:** Verify file ownership (most common issue)
```bash
ls -l /library/ingest/
# Files must be owned by user 1000, not root
# If incorrect:
sudo chown 1000:1000 /library/ingest/*
```

**Check 5:** Manually trigger Library Refresh
1. Open CWA UI: `http://raspberrypi.local:8083`
2. Click "Library Refresh" button on navbar
3. Check logs: `docker compose logs -f cwa`

### Issue: Ingestion Hangs or Times Out

**Check 1:** Monitor container memory
```bash
docker stats calibre-web-automated
# Peak should be < 1.5 GB
```

**Check 2:** Check for stuck processes
```bash
docker compose logs -f cwa | tail -20
# Look for last log entries to see where it got stuck
```

**Check 3:** Force restart CWA
```bash
docker compose restart cwa
# Wait 2 minutes, then check logs again
docker compose logs cwa | grep -i "ingest\|processing"
```

### Issue: OOM (Out of Memory) Errors During Ingestion

**Symptom:**
```
Killed process XXX (CWA) due to OOM
Container restarted
```

**Checks:**
```bash
# Check memory limit in docker-compose.yml
cat docker-compose.yml | grep -A 5 "deploy:"

# Check peak memory usage
docker stats calibre-web-automated --no-stream
```

**Actions:**
- [ ] Document memory peak in logs
- [ ] Check if books are unusually large (> 100 MB each)
- [ ] Try ingesting fewer books at a time (e.g., 10 instead of 20)
- [ ] If still failing, consider: "Memory constraint - RPi 4 2GB may not support 20+ large books"

### Issue: File Format Not Supported

**Symptom:**
```
[ERROR] Ingest: Unsupported file format: book_01.xyz
```

**Action:**
- Ensure all files are EPUB, PDF, or other supported formats
- Check CWA settings for ignored file types
- Remove unsupported files from ingest folder
- Retry: `docker compose restart cwa`

---

## Performance Log Template

Save as: `docs/test-results/task-5-library-ingest.txt`

```
Story: 1.1 - Deploy Calibre-Web-Automated on Raspberry Pi 4
Task: 5 - Initialize Test Library
Date: 2025-10-27
Tester: Alex

=== Test Books ===
Source: Project Gutenberg
Count: 22 books
Total Size: 150 MB
Format: EPUB + PDF mix
Location: /library/ingest/

=== Ingestion Results ===
Books Copied to Ingest: 22 books
Auto-Ingest Start Time: 14:30:15
Ingest Complete Time: 14:35:42
Duration: 5 min 27 sec
Books in Library DB: 22/22 ✓
Ingest Folder Cleaned: ✓

=== Memory Usage ===
Idle Before: 520 MB
Peak During Ingest: 850 MB
Idle After: 540 MB
Max Limit: 1500 MB ✓

=== Status ===
✓ All books copied to /library/ingest/
✓ Auto-ingest completed without manual refresh
✓ All books imported to library
✓ No crashes
✓ No OOM errors
✓ Search working
✓ Detail pages load
✓ Ingest folder cleaned after processing

Task 5: ✓ COMPLETE
```

---

## Next Steps

Once **Task 5 passes**:
1. Proceed to **Task 6: Test basic library browsing**
2. Then **Task 7: Verify auto-restart policy**
3. Then **Task 8: Execute acceptance test suite**

---

**Task 5 Status:** Ready for Execution
**Acceptance Criteria:** AC3, AC5
**Success Criteria:** 20+ books imported, scan completes, no crashes
