# Story 1.5: Implement library backup to separate storage

Status: ready-for-dev

## Story

As a reader,
I want my ebook library and CWA configuration automatically backed up to cloud storage each night,
So that I have disaster recovery protection if the Raspberry Pi fails or the Calibre library becomes corrupted.

## Acceptance Criteria

1. rclone installed on Raspberry Pi
2. Koofr WebDAV account configured as backup destination
3. Encryption configured: AES-256 encryption for all data in transit and at rest
4. Backup scope: entire ebook library folder + CWA configuration files (metadata.db, config folder)
5. Nightly backup scheduled via cron or systemd timer (e.g., 2 AM daily)
6. Initial backup completed successfully; files verified encrypted in Koofr
7. Backup logs created showing success/failure status and size transferred
8. Restore procedure documented: steps to recover library from encrypted Koofr backup

## Tasks / Subtasks

- [ ] Task 1: Install and configure rclone on Raspberry Pi (AC 1-2)
  - [ ] Install rclone: `curl https://rclone.org/install.sh | sudo bash`
  - [ ] Verify installation: `rclone version`
  - [ ] Create Koofr account and obtain WebDAV credentials
  - [ ] Run `rclone config` to add Koofr remote
  - [ ] Configure remote name: `koofr_backup`
  - [ ] Test Koofr connection: `rclone ls koofr_backup:`

- [ ] Task 2: Configure AES-256 encryption for backups (AC 3)
  - [ ] Create encrypted remote: `rclone config create koofr_encrypted crypt`
  - [ ] Point encrypted remote to koofr_backup
  - [ ] Set encryption password (store securely)
  - [ ] Test encrypted write: `rclone copy test.txt koofr_encrypted:`
  - [ ] Verify files are encrypted in Koofr (not readable as plaintext)

- [ ] Task 3: Define backup scope and paths (AC 4)
  - [ ] Identify CWA library folder path (e.g., `/home/pi/books/`)
  - [ ] Identify metadata.db location (e.g., `/home/pi/.local/share/Calibre-Web-Automated/metadata.db`)
  - [ ] Identify CWA config folder (e.g., `/home/pi/.local/share/Calibre-Web-Automated/config/`)
  - [ ] Create backup script: `/home/pi/backup/backup-library.sh`
  - [ ] Script includes:
    - Sync library folder: `rclone sync /home/pi/books/ koofr_encrypted:/bookhelper/books/`
    - Backup metadata.db: `rclone copy /home/pi/.local/share/Calibre-Web-Automated/metadata.db koofr_encrypted:/bookhelper/metadata/`
    - Backup config: `rclone sync /home/pi/.local/share/Calibre-Web-Automated/config/ koofr_encrypted:/bookhelper/config/`
    - Log output to `/var/log/bookhelper-backup.log`

- [ ] Task 4: Schedule nightly backup execution (AC 5)
  - [ ] Option A: Systemd timer
    - [ ] Create `/etc/systemd/system/bookhelper-backup.service`
    - [ ] Create `/etc/systemd/system/bookhelper-backup.timer` (2 AM daily)
    - [ ] Enable timer: `systemctl enable bookhelper-backup.timer`
    - [ ] Verify timer: `systemctl status bookhelper-backup.timer`
  - [ ] Option B: Cron job
    - [ ] Edit crontab: `crontab -e`
    - [ ] Add: `0 2 * * * /home/pi/backup/backup-library.sh >> /var/log/bookhelper-backup.log 2>&1`
    - [ ] Verify cron: `crontab -l`

- [ ] Task 5: Execute and verify initial backup (AC 6)
  - [ ] Run backup script manually: `/home/pi/backup/backup-library.sh`
  - [ ] Check execution time (should complete in <10 minutes for typical library)
  - [ ] Verify files appear in Koofr via web UI
  - [ ] Confirm files are encrypted (not readable as plaintext)
  - [ ] Check backup log: `tail -20 /var/log/bookhelper-backup.log`
  - [ ] Log should show success message and file count
  - [ ] Document initial backup size and duration

- [ ] Task 6: Create logging and monitoring (AC 7)
  - [ ] Backup script outputs to structured log file
  - [ ] Log entries include:
    - Start time and script version
    - Folder paths being backed up
    - Encryption status
    - Bytes transferred / number of files
    - Completion status (success/failure)
    - Duration
    - Any warnings or errors
  - [ ] Configure log rotation: `/etc/logrotate.d/bookhelper-backup`
    - Rotate daily, keep 7 days, max 10 MB per log
  - [ ] Create alert mechanism (e.g., email on failure)

- [ ] Task 7: Document restore procedure (AC 8)
  - [ ] Create `docs/LIBRARY-BACKUP-RECOVERY.md`
  - [ ] Document restore process:
    1. Install rclone on recovery system
    2. Configure koofr_encrypted remote with same password
    3. Decrypt and restore: `rclone copy koofr_encrypted:/bookhelper/books/ /recovery/books/`
    4. Restore metadata.db and config
    5. Restore to CWA container
  - [ ] Include disaster recovery scenarios (RPi failure, metadata corruption)
  - [ ] Include troubleshooting steps
  - [ ] Test restore from backup (dry-run or secondary instance)

## Dev Notes

### Architecture Alignment

This story implements the **Sync & Backup Layer - Library Backup** from the approved BookHelper architecture [Source: docs/architecture.md § 3.2. Sync & Backup Layer]:

- **Disaster recovery backup layer** protects against RPi hardware failure or data corruption
- **One-way backup** (RPi → Koofr) ensures backup never overwrites production library
- **AES-256 encryption** satisfies privacy-first architecture principle
- **Nightly schedule** (2 AM) balances protection with bandwidth/storage constraints
- **Separate from statistics backup** (Story 3.1 uses Syncthing for one-way device backup; this story uses rclone for cloud backup)

**Key Principle:** Backup scope includes both library FILES (books folder) and METADATA (metadata.db + config). This enables full recovery if RPi storage fails.

[Source: docs/architecture.md § 3.2. Sync & Backup Layer - Disaster Recovery Backup; docs/tech-spec-epic-1.md § Backup Infrastructure]

### Project Structure Notes

- **Backup Script:** `/home/pi/backup/backup-library.sh` (new)
- **Backup Credentials:** Koofr WebDAV username/password (secure storage)
- **Backup Log:** `/var/log/bookhelper-backup.log` (rotatable, 7-day retention)
- **Systemd Service:** `/etc/systemd/system/bookhelper-backup.service` and `.timer` (new)
- **Documentation:** `docs/LIBRARY-BACKUP-RECOVERY.md` (new file)

### Technical Implementation Notes

- **rclone version:** Latest (auto-update recommended)
- **Koofr account:** Free tier provides 1 GB storage (check size of library)
- **Encryption:** AES-256 (rclone standard); password stored locally, NOT in git
- **Performance:** Expected backup time <10 minutes for typical 100-200 book library (100-500 MB)
- **Network:** Backup runs over home WiFi; consider impact during peak usage hours (hence 2 AM schedule)

### Learnings from Epic 1 Stories

**From Story 1.1 (CWA Deployment):**
- metadata.db is critical for library; backup strategy must protect it
- Docker Compose volumes enable easy backup of persistent data

**From Story 1.2 (Performance Validation):**
- RPi resource constraints; backup should not occur during ingestion (hence nightly 2 AM schedule)
- Backup network traffic should be monitored to ensure <5 Mbps average

**From Story 1.3 (Auto-ingest):**
- Backup must occur AFTER any auto-ingest operations complete (hence 2 AM timing)
- If ingest fails, backup provides recovery point

**From Story 1.4 (Database Schema):**
- PostgreSQL backup (Neon.tech) is separate from library backup; this story handles file-level backup only
- Both backup layers required for complete disaster recovery

## Prerequisites

- ✓ Story 1.1 complete: CWA deployed, library folder structure established
- ✓ Koofr account created (free tier available)
- ✓ Internet connectivity for nightly backup upload
- ✓ sudo/root access on RPi to configure cron/systemd

## References

- [docs/tech-spec-epic-1.md § Backup Infrastructure](../tech-spec-epic-1.md#backup-infrastructure)
- [docs/architecture.md § 3.2. Sync & Backup Layer](../architecture.md#32-sync--backup-layer-corruption-safe-design)
- [docs/epics.md § Epic 1 § Story 1.5](../epics.md#story-15-implement-library-backup-to-separate-storage)
- [rclone documentation](https://rclone.org/docs/)
- [Koofr WebDAV setup](https://koofr.eu/help/)

## Dev Agent Record

### Context Reference

- Story Context XML: `docs/stories/1-5-implement-library-backup-to-separate-storage.context.xml` (generated 2025-10-30)

### Agent Model Used

claude-haiku-4-5-20251001

### Debug Log References

### Completion Notes List

### File List
