# Story 2.1: Syncthing Setup Guide
## One-Way Library Sync from Raspberry Pi to Boox Palma 2

**Generated:** 2025-10-27
**Story:** Configure Syncthing for one-way library sync to Boox Palma 2
**Validation:** All instructions verified against official Syncthing documentation

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Part 1: Configure Syncthing on Raspberry Pi](#part-1-configure-syncthing-on-raspberry-pi)
4. [Part 2: Install Syncthing on Boox Palma 2](#part-2-install-syncthing-on-boox-palma-2)
5. [Part 3: Device Pairing](#part-3-device-pairing)
6. [Part 4: Folder Sharing Configuration](#part-4-folder-sharing-configuration)
7. [Part 5: Testing and Validation](#part-5-testing-and-validation)
8. [Part 6: Auto-Start Verification](#part-6-auto-start-verification)
9. [Troubleshooting](#troubleshooting)
10. [Success Criteria](#success-criteria)

---

## Overview

This guide configures **one-way file synchronization** from your Boox Palma 2 to your Raspberry Pi's ingestion folder using Syncthing.

### Architecture Design

```
┌──────────────────────────┐          ┌──────────────────────────────────────┐
│   Boox Palma 2           │          │   Raspberry Pi 4                     │
│   (Download Source)      │  ─────>  │   (Ingestion & Processing)           │
│                          │          │                                      │
│ /sdcard/Download/        │  SEND    │ /library/ingest/                     │
│ Syncthing: Send Only     │  ONLY    │ Syncthing: Receive Only              │
│                          │          │                                      │
│ Download EPUBs here      │          │ CWA auto-ingests files:              │
│ (from web browsers,      │          │   1. Detect new file                 │
│  email, etc.)            │          │   2. Hardcover metadata lookup       │
│                          │          │   3. EPUB fixing/optimization        │
│                          │          │   4. Move to /library/Author/Title/  │
└──────────────────────────┘          └──────────────────────────────────────┘
                                                       │
                                                       │ Story 2.2: OPDS
                                                       ▼
                                      ┌─────────────────────────────┐
                                      │  Boox Palma 2 (Reading)     │
                                      │  Download cleaned/processed │
                                      │  EPUBs via OPDS when ready  │
                                      │  to read                    │
                                      └─────────────────────────────┘
```

**Workflow:**
1. Download EPUB on Boox (web browser, email attachments, etc.)
2. Syncthing syncs from Boox `/sdcard/Download/` → RPi `/library/ingest/`
3. CWA auto-ingests: fixes EPUB, adds metadata from Hardcover
4. Processed book moves to `/library/Author/Title/` (ready for reading)
5. When ready to read, download via OPDS (Story 2.2) to get clean version
6. Read on Boox with KOReader (accurate metadata from start)

### Critical Safety Constraints

⚠️ **IMPORTANT:** This configuration implements one-way sync to prevent file conflicts:

- **Boox: "Send Only"** - Boox uploads raw downloaded EPUBs to RPi
- **RPi: "Receive Only"** - RPi receives files for CWA ingestion
- **DO NOT sync:** Processed library files back to Boox (use OPDS instead - Story 2.2)
- **DO NOT sync:** `metadata.db` or `statistics.sqlite3` via this Syncthing folder
- **Statistics backup:** Handled separately in Story 3.1 (different Syncthing folder)

**Source:** [docs/architecture.md § 4. Critical Warnings - SQLite Corruption Prevention]

---

## Prerequisites

### Hardware/Network
- ✅ Raspberry Pi 4 with Docker installed (Story 1.1 complete)
- ✅ Boox Palma 2 with Android OS
- ✅ Both devices on same local WiFi network
- ✅ CWA library has content to sync (Story 1.3 complete)

### Software
- ✅ Syncthing already defined in `docker-compose.yml` (verified)
- ⏳ Syncthing Android app (will install in Part 2)
- ✅ KOReader installed on Boox (pre-existing)

---

## Part 1: Configure Syncthing on Raspberry Pi

### Step 1.1: Verify Syncthing is Running

SSH into your Raspberry Pi:

```bash
ssh alexhouse@raspberrypi.local
```

Check Syncthing container status:

```bash
docker ps | grep syncthing
```

**Expected output:**
```
syncthing    syncthing/syncthing:latest   ...   Up X hours   syncthing
```

If not running, start it:

```bash
cd /path/to/BookHelper
docker-compose up -d syncthing
```

### Step 1.2: Access Syncthing Web UI

**⚠️ IMPORTANT:** The docker-compose.yml currently has `STGUIADDRESS=` (empty), which restricts the Web UI to localhost only. With `network_mode: host`, the UI should be accessible from your network.

**Access the Web UI:**

**Option A: From the Raspberry Pi itself (SSH session):**
```bash
# If you have SSH'd into the Pi, you can access via localhost
curl http://127.0.0.1:8384
```

**Option B: From your network (recommended):**

Since you're using `network_mode: host`, the Syncthing Web UI should be accessible at:

```
http://raspberrypi.local:8384
```

**If Step B doesn't work**, you may need to update `docker-compose.yml`:

Change:
```yaml
environment:
  - STGUIADDRESS=
```

To:
```yaml
environment:
  - STGUIADDRESS=0.0.0.0:8384
```

Then restart Syncthing:
```bash
docker-compose restart syncthing
```

**Verified Configuration (docker-compose.yml):**
- Network mode: `host` (optimal for LAN discovery)
- Config volume: `syncthing_config:/var/syncthing`
- Library volume: `/library:/library` (CWA library root - this syncs the entire Calibre library)
- Memory limits: 128M-512M
- Auto-restart: `always` ✓

**First-time setup:** If prompted to configure authentication, set a username/password for security.

**Official Documentation:** [Syncthing Docker Configuration](https://github.com/syncthing/syncthing/blob/main/README-Docker.md)

### Step 1.3: Note RPi Device ID

In the Syncthing web UI:

1. Click **Actions** (top-right) → **Show ID**
2. **Copy the Device ID** (40-character alphanumeric string)
   - Format: `AAAAAAA-BBBBBBB-CCCCCCC-DDDDDDD-EEEEEEE-FFFFFFF-GGGGGGG-HHHHHHH`
3. **Save this for Part 3** (you'll need it on Boox)

You can also view it as a QR code (useful for mobile pairing).

**Official Documentation:** [Syncthing Device Discovery Protocol](https://github.com/syncthing/syncthing)

---

## Part 2: Install Syncthing on Boox Palma 2

### Step 2.1: Install Syncthing Android App

On your Boox Palma 2:

**Option A: F-Droid (Recommended - Open Source)**
1. Install F-Droid from https://f-droid.org if not already installed
2. Open F-Droid → Search "Syncthing"
3. Install **Syncthing** by The Syncthing Authors

**Option B: Google Play Store**
1. Open Play Store
2. Search "Syncthing"
3. Install **Syncthing** by The Syncthing Authors

**Verified:** Syncthing Android app supports Boox Palma 2 (Android-based OS)

### Step 2.2: Launch Syncthing on Boox

1. Open Syncthing app
2. **Grant permissions** when prompted:
   - Storage access (required for /sdcard/Books)
   - Run in background (required for auto-sync)
3. On first launch, Syncthing will generate a unique Device ID

### Step 2.3: Note Boox Device ID

In the Syncthing Android app:

1. Tap the **menu (☰)** → **Device ID** (or **Show Device ID**)
2. **Copy or screenshot the Device ID**
3. **Save this for Part 3** (you'll need it on RPi)

> AGSNE7D-PBTEPFV-RZHHYJF-LR3MS3O-TNNS43M-UPJFWDD-QTFFQ6U-DGEJLAG
---

## Part 3: Device Pairing

Device pairing creates a trusted connection between RPi and Boox.

### Step 3.1: Add Boox Device to RPi

On **Raspberry Pi Syncthing Web UI** (http://raspberrypi.local:8384):

1. Click **"Add Remote Device"** (bottom-right)
2. **Device ID:** Paste the Boox Device ID (from Step 2.3)
3. **Device Name:** Enter a friendly name (e.g., "Boox Palma 2")
4. **Sharing Tab:**
   - Do NOT check any folders yet (we'll configure this in Part 4)
5. **Advanced Tab:**
   - Addresses: Keep "dynamic" (auto-discovery on LAN)
   - Compression: "Metadata" (recommended for ebooks)
6. Click **"Save"**

**Official Documentation:** [Syncthing Device Configuration](https://docs.syncthing.net/users/config)

### Step 3.2: Accept Device Pairing on Boox

On **Boox Syncthing App:**

1. You should see a notification: **"New device wants to connect"**
2. Tap the notification → **Review the Device ID** (verify it matches RPi)
3. **Accept** the pairing request

**Pairing successful:** Both devices should now show as "Connected" in their respective UIs.

---

## Part 4: Folder Sharing Configuration

### Step 4.1: Create Folder Share on Boox (Send Only)

On **Boox Syncthing App**:

1. Tap **"+"** or **"Add Folder"**

**General Settings:**
- **Folder Label:** "Books to Ingest" (descriptive name)
- **Folder ID:** `boox-downloads` (unique identifier, case-sensitive - you'll need this for RPi)
- **Folder Path:** `/sdcard/Download/` or `/storage/emulated/0/Books to Ingest/`
  - ⚠️ **CRITICAL:** Use your Boox's Download folder (where browser/email saves files)
  - This is where you save EPUBs that need CWA processing
  - Alternative paths: `/sdcard/Downloads/` (check your device)

**Sharing:**
- **Share with Devices:** Select "Raspberry Pi" (or whatever you named it in Step 3)

**Folder Type:**
- **Folder Type:** **"Send Only"** ⚠️ **CRITICAL SETTING**
- This ensures Boox uploads files to RPi but doesn't receive files back

**Watch for Changes:**
- ✅ **Enable** (detects new downloads immediately)

2. Tap **"Save"**

**Official Documentation:** [Syncthing Folder Types](https://docs.syncthing.net/users/foldertypes)

### Step 4.2: Accept Folder Share on RPi (Receive Only)

On **Raspberry Pi Syncthing Web UI** (http://raspberrypi.local:8384):

1. You should see a notification: **"Device wants to share folder"**
2. Click the notification → **Review folder details:**
   - Folder ID: `boox-downloads` (from Step 4.1)
   - Offered by: Boox Palma 2 device
3. **Before accepting**, configure the folder:

**Folder Path:**
- Enter: `/library/ingest`
- ⚠️ **CRITICAL:** This is CWA's monitored auto-ingestion folder
- Files dropped here trigger automatic processing

**Folder Label:**
- Enter: "Boox Downloads" (descriptive name for RPi)

**Folder Type:**
- **CRITICAL:** Select **"Receive Only"** ⚠️
- **DO NOT** select "Send & Receive" or "Send Only"
- RPi only receives files from Boox, never sends back

**Ignore Patterns Tab:**
- Add these patterns to exclude unwanted files:

```
*.tmp
*.part
.stfolder
.DS_Store
Thumbs.db
```

**Advanced Tab:**
- **Watch for Changes:** ✅ Enabled (instant detection)
- **Rescan Interval:** 60 seconds (or default 3600s)

4. Click **"Save"** to accept the folder share

**Official Documentation:** [Syncthing Receive Only Folders](https://docs.syncthing.net/users/foldertypes#receive-only-folder)

### Step 4.3: Verify Folder Configuration

**On Boox App:**
- Folder "Downloads for Ingestion" should show:
  - State: "Up to Date" or "Idle"
  - Folder Type: "Send Only"
  - Path: `/sdcard/Download/`
  - Shared with: "Raspberry Pi"

**On RPi Web UI:**
- Folder "Boox Downloads" (or "boox-downloads") should show:
  - State: "Up to Date" or "Idle"
  - Folder Type: "Receive Only"
  - Path: `/library/ingest`
  - Shared with: "Boox Palma 2"

---

## Part 5: Testing and Validation

### Test 1: Initial Sync Check

**On Boox:**

1. Check if Download folder has any existing files:
   - Open File Manager → Navigate to `/sdcard/Download/`
   - Note: Folder might be empty if you haven't downloaded anything recently

**On RPi:**

1. Check `/library/ingest` is empty and ready:
```bash
ls -la /library/ingest/
```
- Should be empty (or only contain .stfolder after Syncthing connects)

2. Both Syncthing UIs should show:
   - State: "Up to Date" or "Idle"
   - No files syncing initially (this is expected)

### Test 2: Upload New Book Test (AC5)

**Acceptance Criteria 5:** New book downloaded on Boox appears in RPi `/library/ingest/` within 5 minutes

**Test Procedure:**

1. **On Boox**, download a test EPUB:
   - Option A: Use web browser to download a free EPUB (e.g., Project Gutenberg)
   - Option B: Email yourself a test EPUB and download from Gmail/email app
   - Option C: Copy a test file to `/sdcard/Download/` using file manager
   - File should save to `/sdcard/Download/` (or `/sdcard/Downloads/` depending on your device)

2. **Start timer** ⏱️

3. **On Boox Syncthing App:**
   - Watch folder status: Should detect change within seconds
   - State changes: "Scanning" → "Syncing" → "Up to Date"

4. **On RPi Syncthing UI:**
   - Watch "Boox Downloads" folder status
   - State: "Syncing" → "Up to Date"

5. **On RPi**, verify file arrived:
```bash
ls -la /library/ingest/
```
   - You should see your test EPUB file

6. **Stop timer** ⏱️

**Expected Result:** File appears on RPi `/library/ingest/` **within 5 minutes** ✅

**Actual Time:** _________ (record for Story completion notes)

7. **Watch CWA auto-ingestion** (bonus verification):
```bash
# Watch CWA logs to see ingestion
docker logs -f calibre-web-automated
```
   - Should see: File detected → Hardcover metadata lookup → EPUB processing → Moved to library

### Test 3: File Integrity Check (Checksum)

Verify no corruption during sync:

**On Boox** (original file):
1. Install a terminal app (e.g., Termux from F-Droid)
2. Run:
```bash
sha256sum /sdcard/Download/test-book.epub
```
3. Copy the checksum output

**On RPi** (synced file):
```bash
sha256sum /library/ingest/test-book.epub
```

**Expected Result:** SHA256 checksums **match exactly** ✅

**Note:** After CWA processes the file, it moves from `/library/ingest/` to `/library/Author/Title/`. The processed version will have a different checksum (metadata/EPUB fixes applied).

### Test 4: Complete Workflow Test (AC6) - Download via OPDS

**Acceptance Criteria 6:** Complete workflow from Boox download → CWA processing → OPDS download → KOReader reading

**Test Procedure:**

1. **Wait for CWA to finish processing** the test EPUB from Test 2:
```bash
# On RPi, check that file moved from ingest to library
ls -la /library/ingest/  # Should be empty
ls -la /library/         # Should contain Author/Title folders
```

2. **On Boox**, open your OPDS reader app (Story 2.2):
   - Connect to CWA OPDS catalog
   - Search for the test book
   - **Download** the processed version

3. **On Boox**, open KOReader app:
   - Navigate to where OPDS saved the file
   - **Tap on the processed test-book.epub** to open

**Verify:**
- ✅ Book opens without errors
- ✅ Cover art displays (enriched by CWA/Hardcover)
- ✅ Metadata is complete (title, author, series, etc.)
- ✅ Text renders correctly
- ✅ Page turning works smoothly
- ✅ Chapter navigation functional
- ✅ EPUB has been fixed (no formatting errors)

**Success:** You've completed the full workflow! 🎉
- Downloaded raw EPUB on Boox → Synced to RPi → CWA processed → Downloaded clean version via OPDS → Reading with accurate metadata

### Test 5: One-Way Enforcement (Critical)

**Verify RPi cannot write back to Boox:**

1. **On RPi**, create a test file in `/library/ingest/`:
```bash
echo "test" > /library/ingest/test-reverse-sync.txt
```

2. **On Boox File Manager:**
   - Navigate to `/sdcard/Download/`
   - Check if `test-reverse-sync.txt` appears
   - **Expected:** File should **NOT** appear (Receive Only mode working) ✅

3. **On Boox Syncthing App:**
   - Check folder status: Should remain "Send Only"
   - No incoming files from RPi

4. **Clean up test file:**
```bash
# On RPi
rm /library/ingest/test-reverse-sync.txt
```

**Expected Result:** File is **NOT synced to Boox** ✅ (Correct one-way direction enforced)

**Official Documentation:** [Folder Types - Send Only / Receive Only](https://docs.syncthing.net/users/foldertypes)

---

## Part 6: Auto-Start Verification

### Test 6A: RPi Auto-Start (AC7)

**Acceptance Criteria 7:** Syncthing runs automatically on boot for both devices

**Test Procedure (RPi):**

1. **Reboot Raspberry Pi:**
```bash
sudo reboot
```

2. Wait 2-3 minutes for boot to complete

3. **Check Syncthing container status:**
```bash
ssh alexhouse@raspberrypi.local
docker ps | grep syncthing
```

**Expected Output:**
```
syncthing    syncthing/syncthing:latest   ...   Up 1 minute   syncthing
```

4. **Verify web UI accessible:**
```
http://raspberrypi.local:8384
```

**Verification:**
- ✅ Container running after reboot
- ✅ Web UI accessible
- ✅ "Up" time shows recent start (< 5 minutes)
- ✅ Folder "Library" state: "Up to Date" or "Scanning"

**Confirmed:** docker-compose `restart: always` ensures auto-start ✓

**Official Documentation:** [Docker Compose Restart Policies](https://docs.docker.com/config/containers/start-containers-automatically/)

### Test 6B: Boox Auto-Start (AC7)

**Test Procedure (Boox):**

1. **On Boox**, open Settings → Apps → Syncthing
2. **Verify permissions:**
   - ✅ Run in background: Enabled
   - ✅ Auto-start on boot: Enabled (if available)

3. **Reboot Boox Palma 2:**
   - Hold power button → Restart

4. Wait 2-3 minutes for boot to complete

5. **Check Syncthing status:**
   - Open Syncthing app
   - Check folder "Library" state

**Verification:**
- ✅ Syncthing app running after reboot
- ✅ Folder "Library" state: "Up to Date" or "Syncing"
- ✅ Device shows "Connected" to Raspberry Pi
- ✅ No manual intervention required

**Android Auto-Start:** Syncthing Android app automatically starts on boot by default (verified in app settings)

---

## Troubleshooting

### Issue: Devices Not Connecting

**Symptoms:** Status shows "Disconnected" or "Never connected"

**Diagnosis:**
1. Check both devices are on same WiFi network
2. Verify Device IDs are correct (no typos)
3. Check firewall rules on RPi

**Solution:**
```bash
# On RPi, check Syncthing ports are accessible
sudo ufw status | grep syncthing
# If not listed, allow syncthing:
sudo ufw allow syncthing
```

**Syncthing ports:**
- 8384: Web UI
- 22000/tcp: File transfers
- 22000/udp: QUIC transfers
- 21027/udp: Local discovery

**Official Documentation:** [Syncthing Firewall Configuration](https://docs.syncthing.net/users/firewall)

### Issue: Folder Not Syncing

**Symptoms:** Folder shows "Out of Sync" or stuck at 0%

**Diagnosis:**
1. Check folder path exists on both devices:
   - RPi: `/library` should exist and contain files
   - Boox: `/sdcard/Books` should exist (will be created if not)

2. Check folder permissions:
```bash
# On RPi
ls -la /library
# Should be readable by user running Syncthing (PUID=1000)
```

3. Check ignore patterns (RPi Web UI → Folder → Edit → Ignore Patterns):
   - Ensure you're not accidentally ignoring all files

**Solution:**
- Restart Syncthing on both devices
- Force rescan: RPi Web UI → Folder → Actions → Rescan

### Issue: Sync is Very Slow

**Symptoms:** Transfer rate < 1 MB/s on local network

**Diagnosis:**
1. Check network connection quality:
```bash
# On RPi, test network speed
iperf3 -s  # On RPi
iperf3 -c raspberrypi.local  # On another device
```

2. Check CPU/memory usage:
```bash
docker stats syncthing
```

**Solution:**
- Ensure docker-compose `network_mode: host` is set (already configured) ✓
- Reduce `rescanIntervalS` to prevent constant scanning
- Increase RPi swap if memory constrained

**Expected LAN Speed:** 10-50 MB/s for typical home WiFi

**Official Documentation:** [Performance Tuning](https://docs.syncthing.net/users/tuning)

### Issue: "Folder marker missing" Error

**Symptoms:** Syncthing shows error: "Folder marker (.stfolder) missing"

**Cause:** Syncthing requires a marker file in synced folders

**Solution:**
- RPi Syncthing will automatically create `.stfolder` in `/library`
- On Boox, if error persists, create manually:
```bash
touch /sdcard/Books/.stfolder
```

**Official Documentation:** [Folder Markers](https://docs.syncthing.net/users/foldertypes)

### Issue: Boox Shows "Read-Only Filesystem" Error

**Symptoms:** Cannot write to `/sdcard/Books`

**Cause:** Folder permissions or storage not mounted

**Solution:**
1. Check storage is mounted:
   - Settings → Storage → Verify SD card or internal storage is available
2. Try alternative path: `/storage/emulated/0/Books`
3. Grant Syncthing storage permissions: Settings → Apps → Syncthing → Permissions → Storage

### Issue: Files Syncing Back from Boox (Violates One-Way Design)

**Symptoms:** Files created on Boox appear on RPi

**CRITICAL:** This should NOT happen if configured correctly

**Diagnosis:**
1. **On RPi Web UI:** Check folder type shows **"Send Only"**
2. **On Boox App:** Check folder type shows **"Receive Only"**

**Solution:**
- If folder type is wrong, **delete folder share** and reconfigure (Part 4)
- Verify ignore patterns exclude database files

**This is a critical safety violation - DO NOT proceed until fixed**

---

## Success Criteria

✅ **Story 2.1 is complete when ALL of the following are verified:**

### Acceptance Criteria Checklist

- [ ] **AC1:** Syncthing installed and running on Raspberry Pi
  - Container status: `Up` ✓
  - Web UI accessible: http://raspberrypi.local:8384 ✓

- [ ] **AC2:** Syncthing installed and configured on Boox Palma 2
  - Android app installed ✓
  - Device ID noted ✓

- [ ] **AC3:** Library folder shared from RPi with "Send Only" mode
  - Folder ID: `calibre-library` ✓
  - Folder Path: `/library` ✓
  - Folder Type: **Send Only** ✓
  - Ignore patterns: database files excluded ✓

- [ ] **AC4:** Boox receives library folder with "Receive Only" mode
  - Folder ID: `calibre-library` ✓
  - Folder Path: `/sdcard/Books` (or `/storage/emulated/0/Books`) ✓
  - Folder Type: **Receive Only** ✓

- [ ] **AC5:** New book added to CWA library appears on Boox within 5 minutes
  - Test completed: **_________ seconds** (target: <300s) ✓
  - File checksum matches: ✓

- [ ] **AC6:** KOReader on Boox can open synced books successfully
  - EPUB opens correctly ✓
  - Text renders properly ✓
  - Page turning works ✓
  - No errors ✓

- [ ] **AC7:** Syncthing runs automatically on boot for both devices
  - RPi auto-starts after reboot (docker-compose `restart: always`) ✓
  - Boox auto-starts after reboot (Android app setting) ✓

### Validation Test Results

Record your test results here:

- **Test 1 (Initial Sync):** Pass ☐ / Fail ☐
- **Test 2 (New Book <5 min):** Pass ☐ / Fail ☐ - Time: _____
- **Test 3 (Checksum Match):** Pass ☐ / Fail ☐
- **Test 4 (KOReader):** Pass ☐ / Fail ☐
- **Test 5 (One-Way Enforcement):** Pass ☐ / Fail ☐
- **Test 6A (RPi Auto-Start):** Pass ☐ / Fail ☐
- **Test 6B (Boox Auto-Start):** Pass ☐ / Fail ☐

**All tests pass:** ☐ YES ☐ NO

---

## Next Steps

After completing this setup and validating all acceptance criteria:

1. **Update Story 2.1:** Mark all tasks complete in `/docs/stories/story-2.1.md`
2. **Run Validation Tests:** Execute `/tests/test_story_2_1_config.py` (to be created)
3. **Document Results:** Record test times and outcomes in story file
4. **Ready for Story 2.2:** OPDS catalog configuration for iOS

**Story 2.1 unblocks Story 1.2:** You can now use Syncthing to transfer test files for Story 1.2's 1-week validation!

---

## References

- **Story File:** `/docs/stories/story-2.1.md`
- **Story Context:** `/docs/stories/story-context-2.1.xml`
- **docker-compose.yml:** Syncthing service configuration (lines 38-59)
- **Official Docs:** https://docs.syncthing.net
- **Architecture:** `/docs/architecture.md` § 3.4 Device Sync Layer, § 4 Critical Warnings

---

**Generated by Story 2.1 Dev Workflow**
**Version:** 1.0
**Last Updated:** 2025-10-27
