# Task 6: Test Basic Library Browsing

**Story:** 1.1 - Deploy Calibre-Web-Automated on Raspberry Pi 4
**Task ID:** 1.1.6
**Acceptance Criteria:** AC3 - Library browsing and metadata display verified

---

## Overview

This task validates that the CWA web interface properly displays and allows interaction with the library of 20+ books imported in Task 5.

**Duration:** 10 minutes

---

## Test Procedure

### Test 1: Navigate to All Books View

**Steps:**
1. Open CWA Web UI: `http://raspberrypi.local:8083`
2. Log in with admin credentials
3. Click: **Books → All Books** (or **Library** menu)

**Expected Result:**
```
✓ Page loads without errors
✓ Shows list of 20+ books
✓ Each book shows:
  - Title
  - Author
  - Cover art (if available)
  - Series info (if applicable)
```

**Record:** Screenshot or count visible books
- [ ] Books displayed: ____ (should be 20+)
- [ ] No errors in UI or browser console
- [ ] Page loads within 3 seconds

---

### Test 2: Verify Book Metadata

For at least 3 random books, verify metadata:

**Step 1: Click on a book title**
- Expected: Book detail page opens

**Step 2: Verify detail page displays:**
- [ ] Title matches source
- [ ] Author name displayed
- [ ] Cover image visible
- [ ] Description/summary (if available)
- [ ] Book format (EPUB/PDF)
- [ ] File size

**Repeat for 3 different books**
- [ ] Book 1: Details OK
- [ ] Book 2: Details OK
- [ ] Book 3: Details OK

---

### Test 3: Library Search Functionality

**Step 1: Search by Title**
1. Click **Search** in CWA UI
2. Enter a known book title (e.g., "Pride and Prejudice")
3. Press Enter

**Expected Result:**
```
✓ Search returns the book
✓ Correct book highlighted/displayed
✓ Result clickable and shows details
✓ Search completes within 2 seconds
```

- [ ] Title search works
- [ ] Result is correct
- [ ] Detail page accessible

**Step 2: Search by Author**
1. Search for an author name (e.g., "Jane Austen")
2. Press Enter

**Expected Result:**
```
✓ Returns books by that author
✓ Multiple results if author has multiple books
✓ All results shown correctly
```

- [ ] Author search works
- [ ] All books by author displayed

---

### Test 4: Sorting and Pagination

**Test Sorting (if available):**
1. Look for sort options (by title, author, date, etc.)
2. Click different sort options
3. Verify list reorders correctly

- [ ] Sort by title A-Z works
- [ ] Sort by author works
- [ ] Sort by date works (if available)

**Test Pagination (if library is large):**
1. If page shows "Page 1 of N", test navigation
2. Click to next page
3. Verify new books appear

- [ ] Page navigation works
- [ ] Books don't repeat across pages
- [ ] Page numbers correct

---

### Test 5: Book Interaction

**For at least one book, test:**

1. **Click book cover**
   - Expected: Opens book detail or reads book

2. **If "Read" button available:**
   - Click to open reader
   - Expected: Book opens in reader (or viewer link provided)
   - Note: Don't need to fully read, just verify opens

3. **If "Download" button available:**
   - Click to download
   - Expected: Book file downloads to device
   - (Optional: verify file integrity)

4. **If metadata editing available:**
   - Verify "Edit" button exists (don't need to edit for this test)
   - Expected: Edit interface accessible

- [ ] Book interactions work
- [ ] No errors when clicking buttons
- [ ] Responses within 3 seconds

---

### Test 6: Performance and Responsiveness

Monitor while using UI:

**Performance Checks:**
- [ ] Page loads within 3 seconds
- [ ] Search results within 2 seconds
- [ ] No timeout errors
- [ ] No "server unreachable" messages
- [ ] Browser console has no critical errors (F12 → Console)

**Responsiveness:**
- [ ] UI is responsive to clicks
- [ ] Buttons respond immediately
- [ ] No frozen or spinning wheels
- [ ] Navigation between pages smooth

---

## Validation Checklist

- [ ] All Books view shows 20+ books
- [ ] Books display with title, author, cover
- [ ] 3 random books have correct metadata
- [ ] Title search works and finds correct book
- [ ] Author search returns author's books
- [ ] Pagination/sorting works (if applicable)
- [ ] Book detail pages load
- [ ] No UI errors or timeouts
- [ ] Response times acceptable (<3 sec)
- [ ] No browser console errors

---

## Pass Criteria

**Task 6 PASSES if:**
1. ✅ All 20+ books visible in library view
2. ✅ Book metadata correct (title, author, cover)
3. ✅ Search functionality works
4. ✅ No errors or timeouts during browsing
5. ✅ Response times acceptable

---

## Troubleshooting

### Issue: Books Not Displaying

**Solution:**
1. Verify Task 5 completed successfully
2. Refresh page (Ctrl+F5 or Cmd+Shift+R)
3. Check browser console (F12) for errors
4. Restart CWA:
   ```bash
   docker compose restart cwa
   sleep 30
   ```

### Issue: Search Not Working

**Solution:**
1. Verify books are indexed (Task 5 scan completed)
2. Try searching by partial title
3. Check CWA logs:
   ```bash
   docker compose logs cwa | grep -i "search"
   ```

### Issue: Slow Page Load

**Solution:**
1. Check memory usage:
   ```bash
   docker stats calibre-web-automated
   ```
2. Monitor CPU:
   ```bash
   docker stats calibre-web-automated --no-stream
   ```
3. If high memory (>1GB), restart CWA

### Issue: Metadata Missing or Incomplete

**Expected Behavior:**
- Books from Project Gutenberg typically have title/author
- Cover art may not be available (OK for this test)
- Missing metadata is acceptable; Task 1.3 handles enrichment

**Action:** Document in completion notes which books have metadata gaps

---

## Test Report Template

Save as: `docs/test-results/task-6-library-browsing.txt`

```
Story: 1.1 - Deploy Calibre-Web-Automated on Raspberry Pi 4
Task: 6 - Test Basic Library Browsing
Date: 2025-10-26
Tester: Alex

=== Test Results ===

Test 1: All Books View
  - Books visible: 22/22 ✓
  - Metadata displays: ✓
  - No errors: ✓

Test 2: Metadata Verification
  - Book 1 (Frankenstein): ✓
  - Book 2 (Jane Eyre): ✓
  - Book 3 (Moby Dick): ✓

Test 3: Search
  - Title search: ✓
  - Author search: ✓
  - Response time: < 1 sec ✓

Test 4: Sorting
  - Sort A-Z: ✓
  - Sort by author: ✓

Test 5: Performance
  - Page load: < 2 sec ✓
  - Search: < 1 sec ✓
  - No console errors: ✓

=== Summary ===
✓ All browsing functions work
✓ Metadata complete
✓ Performance acceptable
✓ No errors observed

Task 6: ✓ COMPLETE
```

---

## Next Steps

Once **Task 6 passes**, proceed to:
- **Task 7: Verify auto-restart policy**
- **Task 8: Execute acceptance test suite**

---

**Task 6 Status:** Ready for Execution
**Acceptance Criteria:** AC3 (Library browsing)
**Success Criteria:** All books visible, search works, metadata displays
