# KOReader Statistics Backup Setup Guide

**Purpose:** One-way backup of reading statistics from Boox to Raspberry Pi for **disaster recovery only**

⚠️ **CRITICAL WARNING:** This backup is for disaster recovery (recovering from corrupted/lost files), NOT for live progress synchronization. For progress sync across devices, use **KOSync** (Story 2.4).

---

## Overview

This guide configures Syncthing to back up your KOReader `statistics.sqlite3` file from your Boox Palma 2 to your Raspberry Pi. The backup is **one-way only**—your Boox sends updates to the RPi, but the RPi never sends data back. This design prevents corruption if the backup ever becomes damaged.

### Key Characteristics

- **One-Way Sync:** Boox "Send Only" → RPi "Receive Only"
- **Frequency:** Updated automatically within <1 minute of reading session end
- **Retention:** 30-day rolling history with Staggered File Versioning
- **Storage:** ~100-150 MB for 30 days of backup history
- **Corruption Prevention:** RPi cannot write back to Boox, preventing data loss if backup is corrupted

---

## Architecture

### Data Flow

```
Boox Palma 2                          Raspberry Pi
┌──────────────────┐                  ┌──────────────────┐
│ KOReader         │                  │ Syncthing (RO)   │
│ statistics.sqlite3 │ ─Send Only──→  │ /home/alexhouse/ │
│                  │                  │  backups/        │
│                  │                  │  koreader-stats/ │
│ Syncthing (SO)   │                  │                  │
│ /storage/emulated│                  │ .stversions/     │
│  /0/koreader/    │                  │ (30-day history) │
│ settings/        │                  │                  │
└──────────────────┘                  └──────────────────┘
      Send Only                            Receive Only
```

### Why One-Way Sync?

SQLite databases are extremely sensitive to corruption during file-level sync. If the RPi backup ever became corrupted and the Boox received that corrupted version back (two-way sync), you would lose all statistics permanently.

**One-way sync guarantees:**
1. Boox is always the source of truth
2. RPi backup can never corrupt the source on Boox
3. If backup corrupts, you can recover from a versioned copy

---

## Prerequisites

✅ Syncthing installed and running on both Boox and RPi (from Story 2.1)
✅ Devices already paired and communicating
✅ Docker Compose with volume mapping for `/home/alexhouse/backups/`

---

## Configuration

### Part 1: Boox Configuration (Send Only)

**On your Boox Palma 2:**

1. **Open Syncthing app**

2. **Create new folder:**
   - Tap "+" button (Add Folder)
   - **Folder Label:** `KOReader Statistics` (or preferred name)
   - **Folder ID:** `koreader-statstics` (technical identifier)
   - **Folder Path:** `/storage/emulated/0/koreader/settings/`
   - **Folder Type:** `Send Only` (critical)
   - **Shared With:** Select your RPi device

3. **Configure ignore patterns:**
   - Click folder → Edit → Ignore Patterns
   - Add: `!statistics.sqlite3` (only sync this file)
   - This prevents syncing unneeded KOReader config files

4. **Save configuration**
   - Status should show "Syncing" briefly, then "Idle"

### Part 2: Raspberry Pi Configuration (Receive Only)

**On your Raspberry Pi:**

1. **Verify Syncthing is running:**
   ```bash
   docker ps | grep syncthing
   ```
   Should show Syncthing container running.

2. **Access Syncthing Web UI:**
   - Open browser: `http://raspberrypi.local:8384`
   - Should show folder share notification from Boox

3. **Accept folder share:**
   - Click "Add" when prompted for `koreader-statstics` folder
   - Or go to Folders → Add Folder

4. **Configure folder settings:**
   - **Folder Label:** `KOReader Statistics` (or match Boox)
   - **Folder ID:** `koreader-statstics` (must match Boox exactly)
   - **Folder Path:** `/home/alexhouse/backups/koreader-statistics/`
   - **Folder Type:** `Receive Only` (critical for one-way sync)

5. **Create destination directory (if not exists):**
   ```bash
   mkdir -p /home/alexhouse/backups/koreader-statistics/
   ```

6. **Enable file versioning:**
   - In folder settings, find "File Versioning" section
   - **Type:** `Staggered File Versioning`
   - **maxAge:** `30` (days)
   - This creates a rolling 30-day backup history using ~100-150 MB storage

7. **Save configuration**
   - Wait for status to show "Idle"
   - File should begin syncing immediately

---

## Verification Steps

### Verify Boox → RPi Sync

1. **On Boox:**
   - Open a book in KOReader
   - Read some pages to update statistics.sqlite3
   - Close the book completely
   - Note the current time

2. **On RPi:**
   ```bash
   # Check file was synced
   ls -lh /home/alexhouse/backups/koreader-statistics/statistics.sqlite3

   # Check modification timestamp (should be very recent)
   stat /home/alexhouse/backups/koreader-statistics/statistics.sqlite3 | grep Modify
   ```

3. **In Syncthing Web UI:**
   - Open `http://raspberrypi.local:8384`
   - Click `koreader-statstics` folder
   - Status should show "Idle" or "Up to Date"
   - Should show "1 file, 212 KB" (or current size)

### Verify One-Way Sync (No Corruption Risk)

1. **In Syncthing Web UI:**
   - Open `koreader-statstics` folder details
   - Verify **Folder Type** shows: `Receive Only`
   - This confirms RPi cannot write back to Boox

2. **Expected latency:**
   - <1 minute: Normal operation (files synced within 30 seconds typical)
   - <5 minutes: Still acceptable per AC requirement
   - >5 minutes: Check network connectivity and Syncthing status

---

## File Versioning & Recovery

### How Versioning Works

**Staggered File Versioning** automatically keeps backup snapshots at intervals:
- **Last hour:** Every 30 seconds
- **Last day:** Every hour
- **Last 30 days:** Every day
- **Beyond 30 days:** Deleted automatically

This gives you a comprehensive recovery window without excessive storage usage.

### Accessing Versioned Files

If you need to recover from a corruption or accidental change:

1. **In Syncthing Web UI:**
   - Open `koreader-statstics` folder
   - Click folder path to open in file browser (if available)
   - Navigate to `.stversions/` (hidden folder)
   - Old versions stored with timestamp: `statistics.sqlite3~YYYYMMDD-HHMMSS`

2. **From RPi command line:**
   ```bash
   # List versioned copies
   ls -la /home/alexhouse/backups/koreader-statistics/.stversions/

   # Copy a specific version back (if needed)
   cp /home/alexhouse/backups/koreader-statistics/.stversions/statistics.sqlite3~20251110-143022 \
      /home/alexhouse/backups/koreader-statistics/statistics.sqlite3
   ```

---

## Troubleshooting

### Issue: File Not Syncing to RPi

**Symptoms:** Boox Syncthing shows "Up to Date" but file doesn't appear on RPi

**Solutions:**
1. **Verify Docker container has volume mounted:**
   ```bash
   docker inspect syncthing | grep -A5 "Mounts"
   # Should show: /home/alexhouse/backups mounted in container
   ```

2. **Restart Docker container with new volume mapping:**
   ```bash
   cd ~/BookHelper
   docker-compose down
   docker-compose up -d syncthing
   sleep 10
   ```

3. **Force Syncthing rescan:**
   - Web UI → `koreader-statstics` folder → Actions → Rescan

4. **Check Syncthing logs:**
   ```bash
   docker logs syncthing | tail -50 | grep -i error
   ```

### Issue: Sync is Very Slow (>5 minutes)

**Symptoms:** File syncs but takes longer than expected

**Check:**
1. Network connectivity between Boox and RPi:
   ```bash
   # From RPi, ping Boox IP (replace with actual IP)
   ping 192.168.1.100
   ```

2. Syncthing bandwidth limits:
   - Web UI → Actions → Settings → Bandwidth
   - Verify no bandwidth caps are set

3. Large file size:
   - Statistics.sqlite3 should be ~200-300 KB
   - If it's much larger, check if corruption occurred
   ```bash
   ls -lh /home/alexhouse/backups/koreader-statistics/statistics.sqlite3
   ```

### Issue: Sync Status Shows "Out of Sync"

**Symptoms:** Syncthing shows items out of sync but file doesn't change

**Solution:**
1. **Check ignore patterns on Boox:**
   - Boox Syncthing → folder → Edit → Ignore Patterns
   - Should have: `!statistics.sqlite3` (allow this file)
   - All other patterns should exclude other files

2. **Verify folder type:**
   - Boox: Should be "Send Only"
   - RPi: Should be "Receive Only"

3. **Force rescan:**
   - Both sides → folder → Actions → Rescan

### Issue: File Versioning Not Creating Backups

**Symptoms:** Only current `statistics.sqlite3` visible, no `.stversions` folder

**Check:**
1. **Verify versioning is enabled:**
   ```bash
   # On RPi, check folder settings in Web UI
   # Should show "Staggered File Versioning" with maxAge: 30
   ```

2. **Create a version manually:**
   - Modify (touch) a file on Boox to trigger sync
   - Check RPi:
   ```bash
   ls -la /home/alexhouse/backups/koreader-statistics/.stversions/
   ```

3. **Restart Syncthing if versions still don't appear:**
   ```bash
   docker-compose restart syncthing
   ```

---

## Important Notes

### Do NOT Use This for Progress Sync

This is **disaster recovery only**. For live progress synchronization across devices:
- Use **KOSync** (Story 2.4) for application-aware progress sync
- KOSync is safe for live data and syncs progress between Boox and other devices
- File-level sync is only for backup purposes, not live progress

### Backup vs. Sync

| Feature | Statistics Backup | Progress Sync (KOSync) |
|---------|------------------|----------------------|
| **Purpose** | Disaster recovery | Live progress sync |
| **Data** | statistics.sqlite3 only | Progress metadata |
| **Direction** | One-way (Boox → RPi) | Two-way (device ↔ device) |
| **Method** | Syncthing file-level | Application-aware |
| **Frequency** | Updated on file change | Real-time |
| **Corruption Risk** | None (one-way) | None (application-aware) |

**Never attempt to use Syncthing two-way sync for SQLite files.** This will cause catastrophic data loss.

---

## Monitoring

### Daily Checklist

1. **Verify sync is working:**
   ```bash
   # Check file modification time (should be recent)
   stat /home/alexhouse/backups/koreader-statistics/statistics.sqlite3
   ```

2. **Check Syncthing status:**
   - Open `http://raspberrypi.local:8384`
   - `koreader-statstics` folder should show "Idle" or "Up to Date"

3. **Monitor disk usage (optional):**
   ```bash
   # Check backup directory size (should be <200 MB)
   du -sh /home/alexhouse/backups/koreader-statistics/
   ```

### Recovery Procedure (if needed)

If you ever need to restore from a versioned backup:

1. **Identify the corruption date/time**
2. **Find the appropriate version:**
   ```bash
   ls -la /home/alexhouse/backups/koreader-statistics/.stversions/ | grep statistics
   ```
3. **Copy the version to active location:**
   ```bash
   cp /home/alexhouse/backups/koreader-statistics/.stversions/statistics.sqlite3~YYYYMMDD-HHMMSS \
      /home/alexhouse/backups/koreader-statistics/statistics.sqlite3
   ```
4. **Verify the file (optional):**
   ```bash
   # Check file size and timestamp
   ls -lh /home/alexhouse/backups/koreader-statistics/statistics.sqlite3
   ```

---

## References

- **Architecture:** See `docs/architecture.md` § 3.2 Sync & Backup Layer
- **Story:** `docs/stories/3-1-configure-one-way-statistics-backup-from-boox-to-rpi.md`
- **Syncthing Docs:** https://docs.syncthing.net/
- **File Versioning:** https://docs.syncthing.net/v2.0.0/users/versioning

---

## Questions?

If you encounter issues not covered here:
1. Check Syncthing Web UI logs: `http://raspberrypi.local:8384`
2. Check Docker container logs: `docker logs syncthing`
3. Verify network connectivity between devices
4. Ensure folder IDs match exactly on both sides
