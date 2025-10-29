# KOSync Configuration

**Last Updated:** [DATE]
**Story:** Story 2.4 - Enable KOSync progress sync across devices
**Status:** [In Configuration / Complete]

---

## Overview

KOSync enables reading progress synchronization across devices. This document records the configuration details for the BookHelper KOSync deployment.

**Devices:**
- **Server:** Raspberry Pi 4 2GB (Calibre-Web-Automated)
- **Reader Device 1:** Boox Palma 2 (KOReader)
- **Reader Device 2:** iPhone (Readest app)

---

## Server Configuration

### CWA KOSync Server Details

**Endpoint URL:** `_____________________`
- Example: `http://raspberrypi.local:8083/kobo-sync`
- Alternative: `http://raspberrypi.local:8083/api/kosync`
- Tailscale IP (remote access): `http://[TAILSCALE_IP]:8083/kobo-sync`

**CWA Version:** `_____________________`
- Minimum required: v3.1.0+
- Actual deployed: [VERSION]

**KOSync Feature:**
- [ ] Built-in to CWA (preferred)
- [ ] Deployed as standalone service (if CWA doesn't include it)

**Authentication Method:** `_____________________`
- Options: Basic Auth (username/password), API Key, Device ID

**Credentials:**
- **Username:** `_____________________` (if using Basic Auth)
- **Password:** [Stored in password manager - DO NOT COMMIT]
- **API Key:** `_____________________` (if using API key auth)

**Configuration Location:**
- CWA Admin UI: Admin → Configuration → Feature Configuration → KOSync
- Docker compose env vars: [List any KOSYNC_* environment variables added]

**Endpoint Verification:**
```bash
# Test from development machine:
curl -v http://raspberrypi.local:8083/kobo-sync
# Expected: HTTP 200 or 401 (auth required), NOT 404

# Test from Tailscale (remote):
curl -v http://[TAILSCALE_IP]:8083/kobo-sync
```

**Server Logs Location:**
```bash
# View KOSync logs:
docker logs calibre-web-automated | grep -i kosync

# Monitor real-time:
docker logs -f calibre-web-automated | grep -i progress
```

**Database:**
- Location: `/config/app.db` (inside container)
- Table: `kobo_reading_state` (or equivalent)
- Query example:
  ```bash
  docker exec calibre-web-automated sqlite3 /config/app.db \
    "SELECT * FROM kobo_reading_state ORDER BY last_modified DESC LIMIT 5;"
  ```

---

## KOReader Configuration (Boox Palma 2)

**Settings Path:** `_____________________`
- Example: KOReader → Settings (gear icon) → Network → Cloud Sync
- Or: Settings → Advanced → Cloud Services → KOSync

**Configuration:**
```
Server URL: [URL from above]
Username: [USERNAME from above]
Password: [PASSWORD from above]
Auto-sync: Enabled
Sync on book close: Yes
```

**Connection Test Result:** `_____________________`
- Date tested: [DATE]
- Result: [ ] Success / [ ] Failed
- Error message (if any): [ERROR]

**KOReader Version:** `_____________________`
- Check: KOReader → About

**Screenshots/Notes:**
- [Add screenshot of KOReader sync settings here]
- [Note any specific UI quirks or configuration tips]

---

## Readest Configuration (iOS)

**Settings Path:** `_____________________`
- Example: Readest → Settings (gear) → Sync → KOSync
- Or: Settings → Reading → Progress Sync

**Configuration:**
```
Server URL: [URL from above - use Tailscale IP if remote]
Username: [USERNAME from above]
Password: [PASSWORD from above]
Auto-sync: Enabled
```

**Network Configuration:**
- [ ] Local network (raspberrypi.local)
- [ ] Tailscale (remote access via Tailscale IP)
- Tailscale IP used: `_____________________`

**Connection Test Result:** `_____________________`
- Date tested: [DATE]
- Result: [ ] Success / [ ] Failed
- Error message (if any): [ERROR]

**Readest Version:** `_____________________`
- Check: Readest → Settings → About

**Screenshots/Notes:**
- [Add screenshot of Readest sync settings here]
- [Note any specific configuration steps]

---

## Tested Books

### Test Book 1
- **Title:** `_____________________`
- **Author:** `_____________________`
- **ISBN:** `_____________________` (if available)
- **File format:** EPUB / MOBI / AZW3
- **Sync test date:** [DATE]
- **Result:** [ ] Success / [ ] Failed
- **Notes:** [Any issues or observations]

### Test Book 2
- **Title:** `_____________________`
- **Author:** `_____________________`
- **ISBN:** `_____________________`
- **File format:** EPUB / MOBI / AZW3
- **Sync test date:** [DATE]
- **Result:** [ ] Success / [ ] Failed
- **Notes:** [Any issues or observations]

### Test Book 3
- **Title:** `_____________________`
- **Author:** `_____________________`
- **ISBN:** `_____________________`
- **File format:** EPUB / MOBI / AZW3
- **Sync test date:** [DATE]
- **Result:** [ ] Success / [ ] Failed
- **Notes:** [Any issues or observations]

---

## Performance Metrics

### Sync Latency

**Boox → Server:**
- Average latency: `_____ seconds`
- Minimum observed: `_____ seconds`
- Maximum observed: `_____ seconds`
- **Target:** <120 seconds (2 minutes)
- **Status:** [ ] Meets requirement / [ ] Exceeds requirement

**iOS → Server:**
- Average latency: `_____ seconds`
- Minimum observed: `_____ seconds`
- Maximum observed: `_____ seconds`
- **Target:** <120 seconds (2 minutes)
- **Status:** [ ] Meets requirement / [ ] Exceeds requirement

**Server → Client (retrieval):**
- Typical retrieval time: `_____ seconds`
- Tested on: [DATE]

### Reliability

**Test Period:** `_____________________` (e.g., "1 week starting 2025-10-29")

**Success Rate:**
- Total sync attempts: `_____`
- Successful syncs: `_____`
- Failed syncs: `_____`
- Success rate: `_____%`

**Cross-Device Consistency:**
- [ ] ✓ Working - Progress syncs correctly across all devices
- [ ] ⚠️ Issues - [Describe issues found]
- [ ] ✗ Not working - [Describe failure mode]

### Network Performance

**Local Network (WiFi):**
- Sync latency: `_____ seconds`
- Reliability: `_____%`

**Remote Network (Tailscale):**
- Sync latency: `_____ seconds`
- Reliability: `_____%`
- Notes: [Any performance differences vs local]

---

## Troubleshooting

### Common Issues

#### Issue 1: KOSync endpoint returns 404
**Symptom:** `curl` test returns "404 Not Found"

**Possible causes:**
- KOSync not enabled in CWA configuration
- Wrong endpoint URL
- CWA version doesn't include KOSync

**Solution:**
1. Check CWA version: `docker exec calibre-web-automated calibre-web --version`
2. Check CWA admin UI for KOSync settings
3. Verify endpoint URL in CWA logs
4. If not available, consider deploying standalone KOSync service

---

#### Issue 2: Authentication failures (401 Unauthorized)
**Symptom:** "401 Unauthorized" or "Authentication failed" errors

**Possible causes:**
- Incorrect username/password
- Credentials don't match between devices
- API key expired or invalid

**Solution:**
1. Verify credentials in CWA admin UI
2. Ensure same credentials configured on all devices (Boox + iOS)
3. Check CWA logs for auth attempts: `docker logs calibre-web-automated | grep -i "401\|unauthorized"`
4. Re-enter credentials on both KOReader and Readest

**Error messages observed:**
- Boox KOReader: `_____________________`
- iOS Readest: `_____________________`
- Server logs: `_____________________`

---

#### Issue 3: Progress doesn't sync between devices
**Symptom:** Book opens at page 1 instead of last read page

**Possible causes:**
- Book identification mismatch (different file hashes/ISBNs)
- Sync disabled or not triggered
- Network connectivity issue
- Server not reachable from device

**Solution:**
1. Verify book has ISBN metadata (preferred for matching)
2. Check sync is enabled on both devices
3. Manually trigger sync on both devices
4. Verify network connectivity: `ping raspberrypi.local` from device
5. Check server logs for progress submissions
6. Ensure books are identical files (same content)

**Debugging:**
```bash
# Check recent progress submissions:
docker logs calibre-web-automated --tail 100 | grep -i progress

# Check database for progress records:
docker exec calibre-web-automated sqlite3 /config/app.db \
  "SELECT * FROM kobo_reading_state WHERE book_id LIKE '%[BOOK_TITLE]%';"
```

---

#### Issue 4: Sync latency exceeds 2 minutes
**Symptom:** Progress takes >2 minutes to sync

**Possible causes:**
- Network congestion
- Server overload
- Large sync queue
- Remote connection (Tailscale) slower than local

**Solution:**
1. Test on local network first (should be <30 seconds)
2. Check server CPU/memory: `docker stats`
3. Verify Tailscale connection quality if remote
4. Check for other active syncs (Syncthing may compete for bandwidth)
5. Monitor CWA logs for processing delays

**Measured latencies:**
- Local network: `_____ seconds`
- Tailscale remote: `_____ seconds`

---

#### Issue 5: iOS can't reach server (raspberrypi.local doesn't resolve)
**Symptom:** Readest shows "Server unreachable" or connection timeout

**Possible causes:**
- iOS not on same network as RPi
- mDNS (`.local`) not working on iOS network
- Firewall blocking port 8083

**Solution:**
1. **Preferred:** Use Tailscale IP instead of `raspberrypi.local`
   - Format: `http://100.x.x.x:8083/kobo-sync`
2. **Alternative:** Use RPi's local IP address: `http://192.168.x.x:8083/kobo-sync`
   - Find IP: `ssh pi@raspberrypi.local "hostname -I"`
3. Ensure Tailscale is running on both RPi and iPhone
4. Verify port 8083 is accessible from iOS:
   - Try accessing CWA web UI from Safari on iPhone

---

### Edge Cases Discovered

**Edge Case 1:** `_____________________`
- Description: [What happened]
- Books affected: [Which books]
- Solution: [How you fixed it]
- Reproducible: [ ] Yes / [ ] No

**Edge Case 2:** `_____________________`
- Description: [What happened]
- Books affected: [Which books]
- Solution: [How you fixed it]
- Reproducible: [ ] Yes / [ ] No

---

## Maintenance

### Regular Checks

**Weekly:**
- [ ] Verify sync is working on both devices
- [ ] Check server logs for errors: `docker logs calibre-web-automated | grep -i error`
- [ ] Monitor sync latency (should remain <2 minutes)

**Monthly:**
- [ ] Review database size: `docker exec calibre-web-automated du -sh /config/app.db`
- [ ] Check for KOSync updates in CWA
- [ ] Verify Tailscale connectivity still working

### Backup

**KOSync Database:**
```bash
# Backup reading progress database:
docker exec calibre-web-automated sqlite3 /config/app.db \
  ".backup /config/kosync_backup_$(date +%Y%m%d).db"

# Copy backup to local machine:
docker cp calibre-web-automated:/config/kosync_backup_*.db ~/backups/
```

**Configuration:**
- CWA config is backed up via Docker volume: `cwa_config`
- Device settings (KOReader, Readest) should be documented here

---

## Version History

| Date | Change | Author |
|------|--------|--------|
| [DATE] | Initial KOSync setup completed | Alex |
| [DATE] | Updated endpoint URL | Alex |
| [DATE] | Added Tailscale configuration | Alex |

---

## References

- Story 2.4 documentation: `docs/stories/2-4-enable-kosync-progress-sync-across-devices.md`
- Architecture documentation: `docs/architecture.md § 3.5. Progress Sync Layer`
- CWA documentation: https://github.com/crocodilestick/Calibre-Web-Automated
- KOReader documentation: https://koreader.rocks/
- Readest app: https://readest.com/

---

## Notes

**Additional observations:**
- [Any other notes about the configuration]
- [Tips for future maintenance]
- [Known limitations or workarounds]

**Future improvements:**
- [ ] Test sync with multiple simultaneous devices
- [ ] Monitor long-term reliability (>1 month)
- [ ] Investigate sync performance with large library (>100 books)
- [ ] Test sync over cellular network (iOS)
- [ ] Document any edge cases discovered during daily use
