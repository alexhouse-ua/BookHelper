# Story 2.4: Enable KOSync progress sync across devices

Status: Ready for Development

## Story

As a reader,
I want my reading progress synced between Boox and iOS,
So that I can switch devices and continue reading from where I left off.

## Acceptance Criteria

1. CWA KOSync server enabled and accessible
2. KOReader on Boox Palma configured with KOSync plugin pointing to CWA server
3. Readest on iOS configured with KOSync server URL and credentials
4. Test: Read several pages on Boox, verify progress syncs to CWA server
5. Test: Open same book on Readest iOS, book opens at correct page from Boox session
6. Test: Read on iOS, verify progress syncs back and visible on Boox
7. KOSync authentication configured (username/password or device ID)
8. Progress sync occurs within 2 minutes of closing book

## Context

See [2-4-enable-kosync-progress-sync-across-devices.context.xml](./2-4-enable-kosync-progress-sync-across-devices.context.xml) for full story context including acceptance criteria breakdown, testing strategy, dependencies, and implementation notes.

## Blocking Status (Course Correction)

**Story 2.2 is currently blocked:** OPDS catalog not accessible from iOS Readest due to technical integration issues.

**Impact on Story 2.4:**
- Story 2.2 (OPDS) is NOT a hard prerequisite for KOSync functionality
- File sync (Story 2.1) is COMPLETE and working ✓
- KOSync progress sync is independent of OPDS catalog
- Books can be transferred to iOS manually (AirDrop, Files app) for testing KOSync
- Story 2.4 can proceed in parallel without waiting for Story 2.2 fix

**Why unblock now:**
- Maintains forward progress on device sync capabilities
- Allows completion of Epic 2 functionality even if Story 2.2 has extended investigation
- Demonstrates reading progress sync value proposition independently
- iOS users can still access their library via manual file transfer while OPDS is being debugged

## Key Design Notes

### Architecture Alignment

This story completes the Epic 2 goal of "seamless cross-device reading" by enabling reading progress sync, independent of file transfer mechanisms.

**Progress sync decoupling:**
- **File sync:** Story 2.1 (Syncthing) handles ebook file distribution to Boox, Story 2.2 (OPDS) handles catalog access from iOS
- **Progress sync:** Story 2.4 (KOSync) handles reading position sync across all devices
- **Separate protocols prevent conflicts:** Files change via Syncthing/OPDS, progress changes via KOSync only
- **Critical safety constraint:** Documented in [Source: docs/architecture.md § 4. Critical Warnings - SQLite Corruption Prevention]

**Book identification strategy:**
- KOSync uses ISBN or file path/hash to identify books uniquely
- Boox receives files via Syncthing (Story 2.1)
- iOS receives files via OPDS (Story 2.2) or manual transfer (fallback during Story 2.2 blocking)
- Progress syncs by book identity, not file location
- Different file instances on each device is acceptable as long as content matches

### Implementation Sequence

1. **Enable KOSync on CWA server** (AC 1)
   - SSH into RPi, verify CWA KOSync server enabled
   - Confirm KOSync API endpoint accessible (http://raspberrypi.local:8083/kosync or equivalent)
   - Test endpoint with curl from development machine

2. **Configure KOReader on Boox** (AC 2, 7)
   - Open KOReader settings → Cloud Sync section
   - Enter KOSync server URL (http://raspberrypi.local:8083/kosync)
   - Configure authentication credentials (API key or username/password)
   - Test connection from settings UI

3. **Configure Readest on iOS** (AC 3, 7)
   - Open Readest settings → Sync section
   - Select KOSync integration
   - Enter server URL and authentication credentials
   - Test connection from settings UI

4. **Cross-device progress sync testing** (AC 4-6, 8)
   - Read on Boox: Open book, read 10 pages, close book
   - Verify in CWA logs: Progress submission recorded
   - Check KOSync database: Progress stored correctly
   - Read on iOS: Open same book in Readest, verify page 10 displayed
   - Read on iOS: Read 5 more pages, close book
   - Verify in CWA logs: iOS progress received
   - Verify on Boox: Re-open book, shows page 15 from iOS session
   - Measure sync latency: Record close time, check API timestamp (should be <2 minutes, typically <30 seconds on LAN)

### Testing Strategy

**Unit-level validation:**
- KOSync server running and responding to API calls
- Authentication working (correct credentials pass, wrong credentials fail)
- Progress submission API accepts valid payloads
- Progress retrieval returns correct data
- Database transactions are atomic (no partial writes)

**Integration testing:**
- KOReader successfully connects to KOSync server
- Readest successfully connects to KOSync server
- Progress syncs between Boox and iOS with latency <2 minutes
- Cross-device progress matching verified (same page number)
- Retry logic works on network interruption

**Real-device testing:**
- Test with actual books on Boox (already via Story 2.1 synced library)
- Test with actual books on iOS (manual transfer or OPDS once Story 2.2 is fixed)
- Test reading sessions >1 hour to verify latency under realistic conditions
- Test auth failure recovery (wrong password → correct password)

### Risk Mitigation

**Sync latency risk:** If progress sync exceeds 2 minutes, users lose track of reading position across devices. Mitigation: Implement API timeout + retry logic with exponential backoff.

**Auth misconfiguration:** If credentials don't match between devices, sync fails silently. Mitigation: Provide clear error messages in KOReader and Readest UI; log failed auth attempts.

**Book identification mismatch:** If Boox and iOS have same book with different file hashes/paths, KOSync may not recognize them as identical. Mitigation: Use ISBN when available; document book matching strategy; test with real ISBNs and non-ISBN books.

## Prerequisites

- ✓ Story 2.1 Complete: Syncthing file sync working, Boox has library content
- ⏳ Story 2.2 Blocked: OPDS not working, but not required for KOSync core functionality
- Story 2.3 Complete: Tailscale configured for remote access (needed for iOS remote testing)

## Tasks / Subtasks

- [ ] Task 1: Enable KOSync on CWA server (AC 1)
  - [ ] SSH into RPi and verify CWA version (v3.1.0+ required for KOSync)
  - [ ] Check CWA configuration: KOSYNC_ENABLED=true or equivalent
  - [ ] Verify KOSync API endpoint accessible: curl http://raspberrypi.local:8083/kosync/version
  - [ ] Check CWA logs for KOSync initialization message
  - [ ] Document KOSync endpoint URL and port
  - [ ] Configure authentication method (API key, username/password, or device ID)

- [ ] Task 2: Configure KOReader on Boox with KOSync (AC 2, 7)
  - [ ] On Boox, open KOReader settings
  - [ ] Navigate to Cloud Sync section
  - [ ] Select KOSync as sync provider
  - [ ] Enter KOSync server URL from Task 1
  - [ ] Enter authentication credentials
  - [ ] Test connection from settings UI (should show success message)
  - [ ] Document KOReader configuration steps for future reference

- [ ] Task 3: Configure Readest on iOS with KOSync (AC 3, 7)
  - [ ] On iPhone, open Readest app
  - [ ] Navigate to Settings → Sync
  - [ ] Select KOSync integration
  - [ ] Enter KOSync server URL
  - [ ] Enter authentication credentials (same as KOReader)
  - [ ] Test connection from settings UI (should show success message)
  - [ ] Document Readest configuration steps for future reference

- [ ] Task 4: Test Boox → KOSync → iOS progress sync (AC 4-6, 8)
  - [ ] Open book on Boox in KOReader (use book synced via Story 2.1)
  - [ ] Read 10 pages, note exact page number
  - [ ] Close book completely (force-close if needed)
  - [ ] Wait 30 seconds for sync to complete
  - [ ] Check CWA logs for progress submission: grep "KOSync.*progress" docker logs
  - [ ] Query KOSync database directly: SELECT * FROM progress WHERE book_id = X (verify page 10 recorded)
  - [ ] On iPhone, open Readest and select same book
  - [ ] Verify Readest displays page 10 (not page 1)
  - [ ] Read 5 more pages (to page 15), close book
  - [ ] Wait 30 seconds for sync to complete
  - [ ] Check CWA logs for iOS progress submission
  - [ ] Query KOSync database: Verify page 15 recorded
  - [ ] On Boox, re-open same book in KOReader
  - [ ] Verify KOReader displays page 15 (not page 10)
  - [ ] Verify progress bar reflects page 15 position
  - [ ] Record elapsed time from book close to progress display (should be <2 minutes, typically <30 seconds)

- [ ] Task 5: Verify auth failure handling (AC 7)
  - [ ] On Boox KOReader, change API key to incorrect value
  - [ ] Attempt to open book; verify error message displayed
  - [ ] Check CWA logs for auth failure: grep "401.*Unauthorized\|auth.*failed"
  - [ ] Correct API key back to original
  - [ ] Re-open book; verify sync works again
  - [ ] On Readest, repeat auth failure test
  - [ ] Document auth error messages for troubleshooting guide

- [ ] Task 6: Document and handoff to SM
  - [ ] Create story completion summary with test results
  - [ ] Document observed sync latency (should be <2 minutes per AC 8)
  - [ ] Document any deviations from AC or unexpected behaviors
  - [ ] Update sprint-status.yaml to mark Story 2.4 as done
  - [ ] Handoff to SM for retrospective and next story planning

## Implementation Notes

### Story 2.2 Blocking Context

Story 2.2 (OPDS catalog for iOS Readest access) is currently blocked due to technical issues with OPDS integration. However, this story can proceed because:

1. **Independent protocols:** KOSync is separate from OPDS; books can reach iOS via other means
2. **Manual file transfer:** AirDrop or Files app can transfer books to iOS for testing KOSync while OPDS is being debugged
3. **Progress is the blocker removal:** If OPDS remains broken, iOS users can still use KOSync for progress sync (books transferred manually)
4. **Keeps story flow moving:** Completing Story 2.4 demonstrates forward progress on device sync capabilities

### iOS Book Availability (During Story 2.2 Blocking)

Since OPDS is blocked, use these methods to get books on iOS for Story 2.4 testing:

- **AirDrop:** Share ebook files from Mac to iPhone via AirDrop; save to Files app
- **Files app:** Transfer EPUB files from Mac to iPhone via iCloud Drive or local network
- **Direct download:** Once Story 2.2 is fixed, OPDS catalog will automatically provide books

### Fallback Plan

If KOSync has issues during testing:
1. Verify CWA service running: `docker ps | grep calibre`
2. Check CWA logs: `docker logs calibre-web | grep -i kosync`
3. Verify firewall allows port (if remote testing via Tailscale)
4. Test endpoint directly: `curl -u user:pass http://raspberrypi.local:8083/kosync/progress`
5. If CWA doesn't have KOSync, consider standalone KOSync server deployment

## Dev Agent Record

### Implementation Plan

This is a **manual configuration story** requiring physical device access. Below is the comprehensive execution guide.

### Debug Log

**2025-10-29:** Story marked in-progress. Initial investigation assumed CWA would be the KOSync server.

**2025-10-29 - CRITICAL CLARIFICATION:** User does NOT want CWA as sync server. **Hardcover.app is the sync hub.**

**2025-10-29 - VALIDATED with Context7 & Web Search:**

**KOReader Hardcover Support:**
- ✅ **CONFIRMED:** KOReader has Hardcover plugin (`Billiam/hardcoverapp.koplugin`)
- Plugin updates Hardcover.app reading status automatically
- Supports automatic book linking via ISBN or title matching
- Updates progress as you read (configurable frequency, min 1 minute intervals)
- Source: https://github.com/Billiam/hardcoverapp.koplugin

**Readest Hardcover Support:**
- ❌ **NOT YET AVAILABLE:** Hardcover sync is feature request (Issue #588) - still pending
- Readest currently supports: Cloud Sync, KOReader Sync, cross-platform syncing
- Source: https://github.com/readest/readest/issues/588

**Revised Architecture (Based on Current Capabilities):**
- **Option 1 (Hardcover-centric, partial sync):**
  - KOReader (Boox) → Hardcover.app ✅ (via plugin)
  - Readest (iOS) → Hardcover.app ❌ (not available yet)
  - Manual workaround: Log progress in Hardcover manually from iOS

- **Option 2 (Full automated sync):**
  - KOReader (Boox) ↔ Readest (iOS) ✅ (direct KOReader sync)
  - KOReader (Boox) → Hardcover.app ✅ (via plugin)
  - Result: Boox ↔ iOS synced, Hardcover gets updates from Boox only

**Recommended: Option 2** - Provides full cross-device sync now while Readest adds Hardcover support

### Execution Guide (Step-by-Step)

#### Prerequisites Check
- [ ] Hardcover.app account exists (already configured in docker-compose.yml)
- [ ] Hardcover API token available (from docker-compose.yml: HARDCOVER_TOKEN)
- [ ] Boox Palma 2 has KOReader installed
- [ ] iPhone has Readest app installed
- [ ] At least one book is synced to Boox via Syncthing (Story 2.1)

---

### **Task 1: Install and Configure Hardcover Plugin on KOReader (Boox)**

**Source:** https://github.com/Billiam/hardcoverapp.koplugin (validated 2025-10-29)

#### Step 1.1: Download Hardcover Plugin

**On your Mac:**
```bash
# Download the latest release:
cd ~/Downloads
curl -L -O https://github.com/Billiam/hardcoverapp.koplugin/archive/refs/heads/master.zip
unzip master.zip
mv hardcoverapp.koplugin-master hardcoverapp.koplugin
```

**Document here:** Download date: `Oct. 2025`

#### Step 1.2: Retrieve Your Hardcover API Key

1. Navigate to https://hardcover.app/account/api
2. Generate or copy your API key

**Document here:** API key retrieved: [x] Yes / [ ] No

#### Step 1.3: Transfer Plugin to Boox Palma 2

**Transfer via USB:**
```bash
# If Boox is connected via USB and shows as external drive:
cp -r ~/Downloads/hardcoverapp.koplugin /Volumes/Boox/koreader/plugins/
```

**Transfer via Syncthing (alternative):**
- Copy plugin folder to a location that Syncthing syncs
- Or manually copy via Boox file manager

**On Boox:** Navigate to KOReader plugins folder:
- Path: `/sdcard/koreader/plugins/` or `/storage/emulated/0/koreader/plugins/`
- Confirm `hardcoverapp.koplugin` folder exists

**Document here:** Transfer method used: `already downloaded and set up prior to project`

#### Step 1.4: Configure Hardcover Plugin in KOReader

**On Boox Palma 2:**

1. Open KOReader
2. Tap top menu → Settings (gear icon)
3. Navigate to **Tools** or **Plugins**
4. Find **"Hardcover"** plugin
5. Enable the plugin
6. Configure settings:
   - **API Key:** Paste your Hardcover API key from Step 1.2
   - **Auto-link books:** Enable (uses ISBN or title matching)
   - **Update frequency:** Set to desired interval (default: every minute)
   - **Mark finished:** Enable (marks books complete in Hardcover when finished)

7. Save settings

**Document here:**
- Plugin enabled: [x] Yes / [ ] No
- API key entered: [x] Yes / [ ] No
- Auto-link enabled: [x] Yes / [ ] No

#### Step 1.5: Test Hardcover Sync

1. Open a book in KOReader (one that's already synced via Story 2.1)
2. Read a few pages
3. Close the book
4. Wait 1-2 minutes for sync

**Verify on Hardcover.app:**
- Navigate to https://hardcover.app/library
- Check if the book appears as "Currently Reading"
- Verify progress percentage matches KOReader

**Document here:**
- Book synced to Hardcover: [x] Yes / [ ] No
- Progress matches: [x] Yes / [ ] No / [ ] Partial
- Book title in Hardcover: `Blood of Hercules`

---

### **Task 2: Configure KOReader ↔ Readest Progress Sync**

**Source:** https://www.svartling.net/2025/10/how-to-sync-readest-with-koreader.html (validated 2025-10-29)

Since Readest doesn't have native Hardcover support yet, we'll use Readest's built-in KOReader sync feature for cross-device progress syncing.

#### Step 2.1: Set Up KOReader Sync Server on KOReader (Boox)

**On Boox Palma 2:**

1. Open KOReader
2. Tap top menu → Settings → Network
3. Find **"Progress Sync"** or **"Cloud Sync"**
4. Look for **"KOReader Sync"** or **"Progress Sync Server"**
5. Enable the sync server
6. Note the sync settings:
   - **Server URL/Address** (if self-hosted)
   - **Username**
   - **Password**

**KOReader may use:**
- Built-in sync server (runs on device)
- Or external sync server (self-hosted or cloud)

**Document here:**
- Sync server type: [ ] Built-in / [ ] Self-hosted / [ ] Cloud
- Server address (if applicable): `_____________________`
- Username: `_____________________`
- Password: [Store securely]

#### Step 2.2: Configure Readest to Connect to KOReader Sync

**On iPhone:**

1. Open Readest app
2. Navigate to **Settings** (gear icon)
3. Find **"Sync"** or **"Progress Sync"**
4. Select **"KOReader Sync"** option
5. Enter sync details from Step 2.1:
   - **Server URL:** From KOReader settings
   - **Username:** From KOReader settings
   - **Password:** From KOReader settings

6. Test connection
7. Enable **"Auto-sync"**

**Document here:**
- Readest sync configured: [ ] Yes / [ ] No
- Connection test result: `_____________________`

#### Step 2.3: Alternative - Use Readest Cloud Sync

If KOReader sync proves difficult, Readest offers its own cloud sync:

1. In Readest settings, enable **"Cloud Sync"**
2. Sign in or create Readest account
3. This syncs across all Readest instances (iOS, Android, Web, Desktop)

**Note:** This won't sync WITH KOReader directly, but keeps iOS/other Readest devices in sync.

**Document here:** Alternative used: [ ] Yes / [ ] No

---

### **Task 3: End-to-End Progress Sync Test**

#### Step 3.1: Test Boox → Hardcover Sync

**On Boox Palma 2:**
1. Open KOReader
2. Select a book synced via Syncthing (from Story 2.1)
3. Note the starting page/progress
4. Read 10-15 pages
5. Close the book
6. Wait 1-2 minutes for Hardcover plugin to sync

**Verify on Hardcover.app:**
- Navigate to https://hardcover.app/library
- Find the book in your list
- Verify:
  - Status: "Currently Reading"
  - Progress percentage matches KOReader

**Document here:**
- Book title: `_____________________`
- Starting page: `_____________________`
- Ending page: `_____________________`
- Hardcover sync successful: [ ] Yes / [ ] No
- Progress percentage in Hardcover: `_____%`

#### Step 3.2: Test Boox → iOS Sync (via KOReader/Readest Sync)

**Transfer book to iOS (if not already there):**
- Use AirDrop to send EPUB from Mac to iPhone
- Or transfer via iCloud Drive/Files app
- Import into Readest

**On iPhone:**
1. Open Readest app
2. Open the same book you read on Boox
3. **Expected:** Book opens at the page where you left off on Boox
4. **Actual:** Record the page number Readest shows

**Document here:**
- Book transferred to iOS: [ ] Yes / [ ] No / [ ] Already there
- Readest shows correct page: [ ] Yes / [ ] No
- Expected page: `_____________________`
- Actual page: `_____________________`
- **✓ PASS** if pages match within 1-2 pages
- **✗ FAIL** if significantly different

#### Step 3.3: Test iOS → Boox Sync (Reverse Direction)

**On iPhone:**
1. Continue reading the book in Readest
2. Read 10 more pages
3. Note the new ending page
4. Close the book
5. Wait 1-2 minutes for sync

**On Boox:**
1. Open KOReader
2. Open the same book
3. **Expected:** Book opens at the page where you left off on iOS

**Document here:**
- iOS ending page: `_____________________`
- Boox shows page: `_____________________`
- Sync worked: [ ] Yes / [ ] No
- **✓ PASS** if pages match
- **✗ FAIL** if pages don't match

#### Step 3.4: Verify Hardcover Gets Final Progress

**Check Hardcover.app:**
- Navigate to https://hardcover.app/library
- Find the same book
- Verify progress percentage updated (should reflect latest reading from iOS)

**Document here:**
- Final progress in Hardcover: `_____%`
- Hardcover updated from iOS reading: [ ] Yes / [ ] No / [ ] Only from Boox

**Note:** Hardcover may only update from Boox (since plugin is only on KOReader), NOT from iOS. This is expected until Readest adds Hardcover support.

#### Step 3.5: Measure Sync Latency

**Boox → Hardcover:**
- Close time on Boox: `_____________________`
- Hardcover update visible at: `_____________________`
- **Latency:** `_____ seconds` (target: <120s per AC 8)

**Boox → iOS:**
- Close time on Boox: `_____________________`
- iOS book opens at correct page at: `_____________________`
- **Latency:** `_____ seconds` (target: <120s)

**Document here:**
- Both latencies <2 minutes: [ ] Yes / [ ] No
- **✓ PASS** if both <120 seconds
- **✗ FAIL** if either exceeds 2 minutes

---

### **Task 4: Final Validation and Documentation**

#### Step 4.1: Summary Checklist (Revised for Hardcover Architecture)

**Original ACs adapted to Hardcover-based sync:**
- [ ] AC 1 (Adapted): Hardcover API accessible and plugin installed ✓
- [ ] AC 2: KOReader configured with Hardcover plugin on Boox ✓
- [ ] AC 3: Readest configured with KOReader sync for iOS ✓
- [ ] AC 4: Boox → Hardcover progress sync verified ✓
- [ ] AC 5: Boox → iOS progress sync verified ✓
- [ ] AC 6: iOS → Boox progress sync verified ✓
- [ ] AC 7: Hardcover API key configured and working ✓
- [ ] AC 8: Sync latency <2 minutes verified ✓

**Additional Verification:**
- [ ] Hardcover shows "Currently Reading" books from Boox
- [ ] Hardcover progress percentages match KOReader
- [ ] Cross-device reading (Boox ↔ iOS) works seamlessly
- [ ] Book identification working (ISBN or title matching)

#### Step 4.2: Update Configuration Documentation

Update `docs/KOSYNC-SETUP.md` with actual configuration:
```markdown
# KOSync Configuration

## Server Details
- **Endpoint:** [URL from Task 1]
- **Authentication:** [Method from Task 1]
- **Credentials:** [Stored in password manager or secure location]

## KOReader Configuration (Boox Palma 2)
- **Settings Path:** [From Task 2]
- **Configuration:** [Screenshot or settings dump]

## Readest Configuration (iOS)
- **Settings Path:** [From Task 3]
- **Configuration:** [Screenshot or settings dump]

## Tested Books
- **Test Book 1:** [Title, ISBN if available]
- **Sync Latency:** [Measured from Task 4]
- **Cross-device sync:** Working ✓

## Troubleshooting
- If sync fails: [Common issues from testing]
- Auth errors: [Error messages and solutions]
- Network issues: [Tailscale vs local network notes]
```

#### Step 6.3: Performance Metrics
**Document final results:**
- Average sync latency: `_____ seconds`
- Success rate: `___%` (out of test attempts)
- Cross-device consistency: `✓ Working` or `✗ Issues found`

---

### Completion Notes

**What was implemented:**
- [ ] KOSync server enabled on CWA/RPi
- [ ] KOReader (Boox) configured for progress sync
- [ ] Readest (iOS) configured for progress sync
- [ ] End-to-end progress sync validated
- [ ] Authentication tested and working
- [ ] Sync latency meets <2 minute requirement
- [ ] Configuration documented for future reference

**Files Modified:**
- `docs/KOSYNC-SETUP.md` (NEW) - Configuration documentation
- `docs/stories/2-4-enable-kosync-progress-sync-across-devices.md` (MODIFIED) - This file, execution guide added

**Technical Decisions:**
- KOSync endpoint: [To be filled after Task 1]
- Authentication method: [To be filled after Task 1]
- Book identification: [ISBN vs file path - document after testing]

**Warnings for Next Story:**
- Story 2.2 (OPDS) still blocked - iOS books must be transferred manually via AirDrop until fixed
- KOSync works independently of OPDS ✓
- Progress sync requires books to have matching content (same ISBN or file hash)

**Follow-up Items:**
- [ ] Test sync with multiple books (>3 books)
- [ ] Test sync over Tailscale (remote access scenario)
- [ ] Monitor sync reliability over 1 week period
- [ ] Document any edge cases discovered during daily use

---

## References

- [docs/epics.md § Epic 2 § Story 2.4](../epics.md#story-24-enable-kosync-progress-sync-across-devices)
- [docs/PRD.md § Functional Requirements § FR010](../PRD.md)
- [docs/architecture.md § 3.5. Progress Sync Layer](../architecture.md)
- [docs/architecture.md § 4. Critical Warnings - SQLite Corruption Prevention](../architecture.md)
- Story 2.1 context: Configure Syncthing for one-way library sync (prerequisite)
- Story 2.2 blocking notes: OPDS catalog (not required for KOSync, but useful for iOS access)

## File List
- docs/stories/2-4-enable-kosync-progress-sync-across-devices.md (MODIFIED) - Added execution guide
- docs/KOSYNC-SETUP.md (NEW) - Configuration documentation template created

## Change Log
- 2025-10-29: Story marked in-progress, comprehensive execution guide created
- 2025-10-29: Created KOSYNC-SETUP.md template for documenting configuration details
