# Task 5: Initialize Test Library with Sample Books

**Story:** 1.1 - Deploy Calibre-Web-Automated on Raspberry Pi 4
**Task ID:** 1.1.5
**Acceptance Criteria:** AC3, AC5 - Library initialized with 20+ books, scan completes without crashes/OOM

---

## Overview

This task loads 20+ sample books into the CWA library and triggers a library scan. Success criteria:
- All 20+ books imported successfully
- Library scan completes without errors
- No OOM (Out of Memory) errors or container restarts

**Duration:** 15-20 minutes (including scan time)

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

## Part 2: Copy Books to CWA Library

### Step 1: Copy Files to /library

```bash
# Copy all books to CWA library
cp ~/test_books/* /library/

# Verify copy
ls -lh /library/ | head -25
# Should show 20+ book files
```

### Step 2: Verify File Permissions

```bash
# Check permissions (should be readable by CWA container)
ls -l /library/ | head -10
chmod 644 /library/*

# Verify no permission errors
docker-compose exec cwa ls -la /library | head -10
```

---

## Part 3: Trigger Library Scan

### Step 1: Monitor Resource Usage During Scan

In a separate terminal, start monitoring:
```bash
# Terminal 1: Monitor system resources
watch -n 2 'docker stats bookhelper_cwa_1'

# Terminal 2: Monitor CWA logs
docker-compose logs -f cwa
```

### Step 2: Trigger Library Scan via Web UI

1. Open CWA web UI: `http://raspberrypi.local:8083`
2. Log in with admin credentials
3. Navigate to: **Admin → Library Management**
4. Click: **Scan for new books** (or similar option)
5. Watch progress in UI and logs

### Step 3: Alternative: Trigger via API/CLI

If web UI doesn't have scan button:
```bash
# Access CWA container
docker-compose exec cwa bash

# Inside container, trigger scan (command varies by CWA version)
# Check CWA documentation for exact command
# Examples:
#   calibredb add-books /library/*
#   cwa-cli scan-library /library
```

---

## Part 4: Monitor Scan Progress

### Expected Output

**CWA Logs:**
```
[INFO] Library scan initiated
[INFO] Scanning directory: /library
[INFO] Found 20 books
[INFO] Processing: book_01.epub
[INFO] Processing: book_02.epub
...
[INFO] Indexing metadata...
[INFO] Library scan complete: 20 books imported
```

**Docker Stats (should see activity):**
```
CONTAINER            CPU %    MEM USAGE
bookhelper_cwa_1     25%      650MiB / 1.5GiB
```

### Error Indicators (Watch For)

```
❌ MEMORY ERRORS:
   "Out of memory"
   "OOMKilled"
   Container restart loops

❌ SCAN ERRORS:
   "Cannot read file"
   "Corrupt book"
   "Permission denied"

❌ DATABASE ERRORS:
   "SQLite locked"
   "Database corruption"
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
# Query library count (method varies by CWA)
docker-compose exec cwa bash -c 'sqlite3 /metadata/metadata.db "SELECT COUNT(*) FROM books;"'

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

During scan:
- [ ] Memory usage < 1.5GB (resource limit)
- [ ] No OOM errors in logs
- [ ] No container restarts
- [ ] Peak memory < 1.0GB (safety margin)

After scan:
- [ ] Memory returns to baseline (<600 MB idle)
- [ ] No memory leaks evident

### Library Integrity (AC3, AC5)

- [ ] All 20+ books imported successfully
- [ ] Books visible in web UI
- [ ] Book search works
- [ ] Detail pages load without errors
- [ ] Cover art displays (if included in source)

### Error Conditions (AC5)

- [ ] No crashes during scan
- [ ] No OOM killer invocations
- [ ] No "database locked" errors
- [ ] Scan completes to 100%

---

## Troubleshooting

### Issue: Books Not Appearing in UI

**Check 1:** Verify files in container
```bash
docker-compose exec cwa ls -la /library/
# Should list your book files
```

**Check 2:** Check scan logs
```bash
docker-compose logs cwa | grep -i "scan\|error\|import"
```

**Check 3:** Restart CWA and retry scan
```bash
docker-compose restart cwa
# Wait 30 seconds, then trigger scan again
```

### Issue: Scan Timeout or Hangs

**Check 1:** Monitor logs
```bash
docker-compose logs -f cwa
```

**Check 2:** Check available memory
```bash
docker stats bookhelper_cwa_1
```

**Check 3:** If truly hung, force restart
```bash
docker-compose restart cwa
# Wait for recovery, check if scan persisted
```

### Issue: OOM Errors During Scan

**Symptom:**
```
Killed process XXX (CWA) due to OOM
```

**Action:**
- [ ] Document memory peak in logs
- [ ] Check if books are unusually large
- [ ] Consider reducing library size for RPi 4 2GB
- [ ] Note as "Memory constraint - may require RPi 5"

---

## Performance Log Template

Save as: `docs/test-results/task-5-library-scan.txt`

```
Story: 1.1 - Deploy Calibre-Web-Automated on Raspberry Pi 4
Task: 5 - Initialize Test Library
Date: 2025-10-26
Tester: Alex

=== Test Books ===
Source: Project Gutenberg
Count: 22 books
Total Size: 150 MB
Format: EPUB + PDF mix

=== Scan Results ===
Start Time: 14:30:15
End Time: 14:35:42
Duration: 5 min 27 sec
Books Imported: 22/22 ✓

=== Memory Usage ===
Idle Before: 520 MB
Peak During Scan: 850 MB
Idle After: 540 MB
Max Limit: 1500 MB ✓

=== Status ===
✓ All books imported
✓ No crashes
✓ No OOM errors
✓ Search working
✓ Detail pages load

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
