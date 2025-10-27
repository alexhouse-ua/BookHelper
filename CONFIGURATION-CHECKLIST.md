# BookHelper Configuration Checklist

This document lists all configuration values you need to provide or verify before deploying.

## Required Information (Must Configure)

### 1. Timezone
**Current Value:** `UTC`
**Location:** `docker-compose.yml` → both services → `TZ` environment variable

**Action Required:**
- Update to your local timezone for accurate timestamps
- Find your timezone: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones

**Example:**
```yaml
- TZ=America/New_York  # For US Eastern Time
- TZ=Europe/London     # For UK
- TZ=Asia/Tokyo        # For Japan
```

---

## Optional Information (Enhance Functionality)

### 2. Hardcover API Token
**Current Status:** Commented out (disabled)
**Location:** `docker-compose.yml` → `calibre-web-automated` service → `HARDCOVER_TOKEN`

**Purpose:**
- Enables metadata enrichment from Hardcover API
- Automatically fetches book covers, descriptions, ratings
- Improves library metadata quality

**How to Get:**
1. Visit: https://docs.hardcover.app/api/getting-started/
2. Create a Hardcover account
3. Generate API key
4. Uncomment line in docker-compose.yml and add your token:
   ```yaml
   - HARDCOVER_TOKEN=your_actual_api_key_here
   ```

**Skip if:** You don't need automatic metadata enrichment (can add later)

---

### 3. Network Share Mode
**Current Status:** Commented out (disabled, defaults to `false`)
**Location:** `docker-compose.yml` → `calibre-web-automated` service → `NETWORK_SHARE_MODE`

**Purpose:**
- Prevents SQLite database locking issues on network file systems
- Only needed if `/library` is on NFS/SMB share

**When to Enable:**
- Your `/library` directory is on a network share (NFS, SMB, CIFS)
- You experience database locking errors

**How to Enable:**
```yaml
- NETWORK_SHARE_MODE=true
```

**Skip if:** `/library` is on local storage (RPi SD card or USB drive)

---

### 4. User/Group IDs (PUID/PGID)
**Current Value:** `1000` (default for first user on most systems)
**Location:** `docker-compose.yml` → both services → `PUID` and `PGID`

**Purpose:**
- Ensures Docker containers run with correct file permissions
- Prevents permission denied errors

**Check Your IDs:**
```bash
# On your Raspberry Pi, run:
id

# Output example:
# uid=1000(alexhouse) gid=1000(alexhouse) groups=...
```

**Action Required:**
- If your `uid` and `gid` are NOT 1000, update docker-compose.yml:
  ```yaml
  - PUID=YOUR_UID_HERE
  - PGID=YOUR_GID_HERE
  ```

**Skip if:** Your user ID is 1000 (most common)

---

## System Prerequisites (No Configuration Needed)

### 5. Raspberry Pi Requirements
✅ **Hardware:**
- Raspberry Pi 4 Model B, 2GB RAM minimum
- 50GB+ storage (SD card or external USB)
- Network connectivity (Ethernet or WiFi)

✅ **Software:**
- Raspberry Pi OS (Bullseye or later)
- Docker Engine 20.10+
- Docker Compose 1.29+

✅ **Directories:**
- `/library` - will be auto-created if missing
- `/library/ingest` - will be auto-created if missing

---

## Default Values (No Action Needed)

### Access Information
- **CWA Web UI:** http://raspberrypi.local:8083
  - Default username: `admin`
  - Default password: `admin123`
  - ⚠️ **Change password immediately after first login!**

- **Syncthing Web UI:** http://raspberrypi.local:8384
  - No default password (will prompt to set one on first access)

### Ports
- `8083` - Calibre-Web-Automated (CWA) web interface + KOSync
- `8384` - Syncthing web interface (host network mode)
- `22000` - Syncthing protocol (TCP/UDP, host network mode)

### Memory Limits
- CWA: 1.5GB hard limit, 400MB reservation
- Syncthing: 512MB hard limit, 128MB reservation
- **Total:** ~2GB allocated (suitable for RPi 4 2GB)

---

## Configuration Checklist

Before deploying, verify:

- [x] **Timezone** updated to your location
- [x] **PUID/PGID** matches your user ID (if not 1000)
- [x] **Hardcover token** added (optional, if you want metadata enrichment)
- [ ] **Network share mode** enabled (only if using NFS/SMB)
- [ ] `/library` directory exists (or will be auto-created)
- [ ] Raspberry Pi has Docker & Docker Compose installed
- [ ] At least 1GB free disk space available

---

## Quick Setup Summary

**Minimum configuration to get started:**
1. Update `TZ` to your timezone
2. Deploy with: `docker-compose up -d`
3. Access CWA at: http://raspberrypi.local:8083
4. Log in with: `admin` / `admin123`
5. Change password immediately

**Everything else is optional and can be configured later!**

---

## Post-Deployment Configuration

After containers are running, you'll configure these through web UIs:

### In CWA (http://raspberrypi.local:8083):
- Change admin password
- Add users
- Configure metadata providers
- Set up library preferences
- Configure auto-ingestion rules

### In Syncthing (http://raspberrypi.local:8384):
- Set GUI password
- Add remote devices (Boox, iOS, etc.)
- Configure folder sync (Story 1.2+)
- Set up one-way sync rules

---

## Need Help?

- CWA Documentation: https://github.com/crocodilestick/Calibre-Web-Automated/wiki
- Syncthing Documentation: https://docs.syncthing.net/
- Story 1.1 Deployment Guide: `docs/DEPLOYMENT-GUIDE-STORY-1.1.md`
