# Story 1.6: Document Calibre CLI fallback procedures

Status: ready-for-dev

## Story

As a developer,
I want documented Calibre CLI procedures for manual library management,
So that I have fallback procedures if CWA auto-ingest fails and can troubleshoot the library database.

## Acceptance Criteria

1. Documentation created showing how to add books via calibredb CLI
2. Metadata fetch command documented (calibredb fetch-ebook-metadata)
3. Batch import script provided for processing multiple files via CLI
4. Instructions for triggering CWA rescan after manual Calibre CLI additions
5. Troubleshooting guide for common CWA ingest failure modes
6. metadata.db backup/restore procedure documented
7. Examples provided for each command with expected output

## Tasks / Subtasks

- [ ] Task 1: Document calibredb basic commands (AC 1)
  - [ ] Create `docs/CALIBRE-CLI-FALLBACK.md`
  - [ ] Document command: `calibredb add <file.epub> --library-path=<path>`
  - [ ] Document command: `calibredb list --library-path=<path>`
  - [ ] Document command: `calibredb remove <book_id> --library-path=<path>`
  - [ ] Document command: `calibredb set-custom --library-path=<path> <field> <book_id> <value>`
  - [ ] Include examples with sample output for each command
  - [ ] Note permissions and path requirements

- [ ] Task 2: Document metadata enrichment via CLI (AC 2)
  - [ ] Document command: `calibredb fetch-ebook-metadata <book_id> --library-path=<path>`
  - [ ] Explain metadata sources (Google Books API requirements)
  - [ ] Document how to trigger metadata fetch for entire library
  - [ ] Include examples and expected output
  - [ ] Note rate limiting for Google Books API
  - [ ] Troubleshooting: What to do if metadata fetch fails

- [ ] Task 3: Create batch import script (AC 3)
  - [ ] Create `/home/pi/scripts/batch-import-calibre.sh`
  - [ ] Script accepts directory path as argument
  - [ ] Script iterates through .epub/.pdf files
  - [ ] For each file, calls `calibredb add`
  - [ ] Script includes:
    - Error handling (skip corrupted files, log failures)
    - Progress tracking (display file count)
    - Completion summary (X files added, Y failed)
  - [ ] Make script executable: `chmod +x batch-import-calibre.sh`
  - [ ] Document usage: `./batch-import-calibre.sh /path/to/ebooks/`
  - [ ] Include example run output

- [ ] Task 4: Document CWA rescan procedure (AC 4)
  - [ ] When to rescan: After manual calibredb additions
  - [ ] How to trigger CWA rescan:
    - Via web UI: Admin → Library → Rescan Library
    - Via API: `curl -X POST http://raspberrypi.local:8083/api/rescan`
    - Via CLI: Document if available
  - [ ] Expected rescan duration (e.g., <2 minutes for 100 books)
  - [ ] How to monitor rescan progress
  - [ ] Verification: Check CWA web UI to confirm new books appear

- [ ] Task 5: Create troubleshooting guide (AC 5)
  - [ ] Common failure modes:
    1. **CWA auto-ingest not triggering:** Check monitored folder permissions, verify CWA logs
    2. **Metadata enrichment failing:** Check Google Books API quota, verify ISBN accuracy
    3. **Database locked errors:** Check for running CWA processes, wait before retry
    4. **Corrupted EPUB files:** Skip file, try different format (PDF alternative)
    5. **Permission denied errors:** Check file ownership and RPi user permissions
  - [ ] For each failure mode, include:
    - Symptoms (error message)
    - Root cause explanation
    - Resolution steps
    - Prevention tips
  - [ ] Include CWA log locations: `/home/pi/.local/share/Calibre-Web-Automated/logs/`
  - [ ] Include how to check CWA container status: `docker logs calibre-web-automated`

- [ ] Task 6: Document metadata.db backup and recovery (AC 6)
  - [ ] Why backup metadata.db: It's the library database; corruption requires recovery
  - [ ] Backup procedure:
    - Manual: `cp ~/.local/share/Calibre-Web-Automated/metadata.db ~/backups/metadata.db.backup`
    - Automated: Included in Story 1.5 library backup
  - [ ] Recovery procedure (if corruption detected):
    1. Stop CWA container: `docker stop calibre-web-automated`
    2. Restore backup: `cp ~/backups/metadata.db.backup ~/.local/share/Calibre-Web-Automated/metadata.db`
    3. Restart CWA: `docker start calibre-web-automated`
    4. Verify library loads correctly
  - [ ] How to detect corruption: CWA fails to start, errors in logs mentioning "database disk image malformed"
  - [ ] What NOT to do: Don't modify metadata.db directly; use calibredb CLI only

- [ ] Task 7: Provide command examples and reference (AC 7)
  - [ ] Create `docs/CALIBRE-CLI-REFERENCE.md` with quick reference
  - [ ] Include copy-paste ready commands:
    - Add single book
    - Add batch of books
    - Fetch metadata
    - List library contents
    - Remove book
    - Database backup
    - Database restore
  - [ ] Include expected output for each example
  - [ ] Include explanations of parameters and options
  - [ ] Organize by use case (Add, Manage, Troubleshoot, Backup)

## Dev Notes

### Architecture Alignment

This story documents the **Library Management Layer - Fallback Procedures** from the approved BookHelper architecture [Source: docs/architecture.md § 3.3. Library Management Layer]:

- **Calibre CLI represents proven, stable alternative** for manual management if CWA auto-ingest feature fails
- **Documented procedures reduce Mean Time To Recovery (MTTR)** if ingest fails or database corruption occurs
- **Supports "Stability Over Features" architecture principle** by providing low-tech fallback options
- **Separate from CWA auto-ingest** — this is the manual, admin-driven alternative path

**Key Principle:** The Calibre library is the source of truth; direct manipulation via calibredb CLI is safe and supported. CWA is a convenience layer on top.

[Source: docs/architecture.md § 3.3. Library Management Layer; docs/tech-spec-epic-1.md § Fallback Procedures]

### Project Structure Notes

- **Documentation:** `docs/CALIBRE-CLI-FALLBACK.md` (main guide, new)
- **Quick Reference:** `docs/CALIBRE-CLI-REFERENCE.md` (copy-paste commands, new)
- **Batch Import Script:** `/home/pi/scripts/batch-import-calibre.sh` (new)
- **Calibre Library:** `~/.local/share/Calibre/` (standard location)
- **Metadata Database:** `~/.local/share/Calibre/metadata.db` (critical file)

### Technical Implementation Notes

- **Calibre CLI Tool:** `calibredb` comes with Calibre or Calibre Server installation
- **Library Path:** Use `--library-path=/path/to/library` for all commands
- **Permissions:** calibredb must have read/write access to metadata.db
- **Google Books API:** Free tier available; document quota limits
- **Database Locking:** Calibre locks metadata.db during writes; wait if locked
- **Batch Processing:** Script should include error handling and progress tracking

### Learnings from Epic 1 Stories

**From Story 1.1 (CWA Deployment):**
- Calibre is installed as part of CWA setup
- metadata.db is managed by CWA; direct access requires careful coordination

**From Story 1.2 (Performance Validation):**
- Auto-ingest is the preferred path; fallback is only for failures
- Performance targets show <30 sec/book; manual CLI is slower but reliable

**From Story 1.3 (Auto-ingest):**
- If auto-ingest fails due to bugs or corruption, manual CLI is the recovery path
- This story provides runbooks for that recovery scenario

**From Story 1.4 (Database Schema):**
- Books added via calibredb CLI must still appear in Neon.tech PostgreSQL
- ETL pipeline (Story 3.2) reads books added manually; no special handling needed

**From Story 1.5 (Backup):**
- metadata.db backup is automated; this story documents manual recovery from that backup

## Prerequisites

- ✓ Story 1.1 complete: CWA deployed, Calibre CLI tools available
- ✓ Story 1.2 complete: Auto-ingest operational (to understand the normal flow before documenting fallback)
- ✓ Calibre installed on RPi (comes with CWA Docker image)

## References

- [docs/tech-spec-epic-1.md § Fallback Procedures](../tech-spec-epic-1.md#out-of-scope)
- [docs/architecture.md § 3.3. Library Management Layer](../architecture.md#33-library-management-layer)
- [docs/epics.md § Epic 1 § Story 1.6](../epics.md#story-16-document-calibre-cli-fallback-procedures)
- [Calibre CLI documentation](https://manual.calibre-ebook.com/cli/calibredb.html)
- [CWA auto-ingest documentation](https://github.com/OzzieIsaacs/Calibre-Web-Automated)

## Dev Agent Record

### Context Reference

- Story Context XML: `docs/stories/1-6-document-calibre-cli-fallback-procedures.context.xml` (generated 2025-10-30)

### Agent Model Used

claude-haiku-4-5-20251001

### Debug Log References

### Completion Notes List

### File List
