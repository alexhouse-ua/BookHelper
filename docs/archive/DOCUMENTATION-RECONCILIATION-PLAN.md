# BookHelper Documentation Reconciliation Plan

**Date:** 2025-10-30
**Status:** Recommended Actions (Awaiting Approval)
**Scope:** Alignment of epics.md, sprint-status.yaml, and tech-spec documents

---

## Executive Summary

The project documentation has **natural divergence** between planning and execution layers:

| Document | Purpose | Status | Authority |
|----------|---------|--------|-----------|
| **docs/epics.md** | Strategic epic breakdown (Phase 2) | STALE | Reference (superseded) |
| **docs/tech-spec-epic-*.md** | Detailed design specs (Phase 2) | CURRENT | Working reference |
| **docs/sprint-status.yaml** | Sprint execution tracking (Phase 4) | CURRENT & AUTHORITATIVE | Source of truth |
| **docs/stories/** | Individual story implementation | CURRENT | Working implementation |

**Root Cause:** epics.md locked in 3-story decomposition for Epic 1 during Phase 2; sprint-status.yaml evolved into 6-story decomposition during Phase 4 sprint planning without updating epics.md.

**Recommendation:** Treat sprint-status.yaml as authoritative; update epics.md to match current planning.

---

## Documentation Sync Issues

### Issue #1: Epic 1 Story Count Mismatch

**epics.md (Phase 2 - Stale):**
- Story 1.1: Deploy CWA + Unified Database Foundation
- Story 1.2: Auto-Ingestion + Metadata Enrichment
- Story 1.3: Fallback Procedures & Operational Resilience
- **Count: 3 stories**

**sprint-status.yaml (Phase 4 - Current):**
- Story 1.1: deploy-calibre-web-automated-on-raspberry-pi-4 [DONE]
- Story 1.2: configure-hardware-performance-validation-checkpoint [IN-PROGRESS]
- Story 1.3: configure-auto-ingestion-workflow-with-hardcover-metadata [BLOCKED-WAITING]
- **Story 1.4: design-and-implement-unified-database-schema [BACKLOG]**
- **Story 1.5: implement-library-backup-to-separate-storage [BACKLOG]**
- **Story 1.6: document-calibre-cli-fallback-procedures [BACKLOG]**
- **Count: 6 stories**

**tech-spec-epic-1.md (Phase 2 - Validates Expansion):**
Explicitly covers all 6 work areas under "Objectives and Scope" and "Detailed Design":
- Infrastructure → Story 1.1
- Auto-Ingestion → Story 1.2
- **Database Foundation (Neon.tech schema) → Story 1.4** ✓ Confirmed
- **Backup Infrastructure (rclone) → Story 1.5** ✓ Confirmed
- **Fallback Procedures (Calibre CLI) → Story 1.3 or 1.6** ✓ Confirmed
- Performance Validation → Story 1.2

**Root Cause Analysis:**

The 3-story breakdown in epics.md was high-level planning. During sprint planning (Phase 4), work was decomposed into finer-grained, sprint-ready stories:

- **Original 1.1** ("Deploy CWA + Unified Database Foundation") was split into:
  - **New 1.1**: Deploy CWA infrastructure only
  - **New 1.4**: Design unified database schema (separated for parallel work)
  - **New 1.5**: Implement library backup (separated as distinct deliverable)

- **Original 1.2** ("Auto-Ingestion + Metadata Enrichment") was split into:
  - **New 1.2**: Hardware performance validation checkpoint
  - **New 1.3**: Configure auto-ingestion workflow

- **Original 1.3** ("Fallback Procedures") remains as:
  - **New 1.6**: Document calibre-cli fallback procedures (renamed for clarity)

**Authority Decision:** tech-spec-epic-1.md + sprint-status.yaml are aligned and authoritative. epics.md is planning-phase reference that needs updating.

---

### Issue #2: Story 1.4 Blocking Dependencies

**Problem:** Story 3.2 (ETL Pipeline) lists Story 1.4 as a blocking dependency, but Story 1.4 doesn't exist in epics.md.

**Status:**
- Story 1.4 exists in sprint-status.yaml [BACKLOG]
- Story 1.4 is documented in tech-spec-epic-1.md [Confirmed]
- Story 1.4 **story file does NOT exist** in docs/stories/

**Resolution:** Create story files for 1.4, 1.5, 1.6 from tech-spec guidance.

---

### Issue #3: Story Status Naming Inconsistencies

**epics.md uses high-level story names:**
- "Deploy CWA + Unified Database Foundation"
- "Auto-Ingestion + Metadata Enrichment"
- "Fallback Procedures & Operational Resilience"

**sprint-status.yaml uses action-oriented story names:**
- "deploy-calibre-web-automated-on-raspberry-pi-4"
- "configure-hardware-performance-validation-checkpoint"
- "configure-auto-ingestion-workflow-with-hardcover-metadata"
- "design-and-implement-unified-database-schema"
- "implement-library-backup-to-separate-storage"
- "document-calibre-cli-fallback-procedures"

**Recommendation:** Use sprint-status.yaml names as canonical; add cross-reference in epics.md.

---

## Reconciliation Strategy

### Phase 1: Confirm Current State (Reference)

**Authoritative Source Hierarchy:**
1. **sprint-status.yaml** — Current sprint tracking (Phase 4, updated daily)
2. **tech-spec-epic-*.md** — Detailed design specifications (Phase 2, rarely change)
3. **Story files (docs/stories/)** — Implementation artifacts (Phase 4, growing)
4. **epics.md** — Strategic planning reference (Phase 2, outdated but intact)

**Rationale:**
- sprint-status.yaml reflects active development decisions
- tech-spec aligns with sprint-status decomposition
- Story files implement to sprint-status plan
- epics.md is high-level strategy (useful for context, not executable)

---

### Phase 2: Update epics.md (High Priority)

**Action:** Expand Epic 1 section to match current 6-story breakdown

**Changes Required:**

1. **Update Epic 1 Summary (Line 115-118):**
   ```
   Before: "Total Stories: 3 (consolidated from 6)"
   After: "Total Stories: 6 (decomposed during sprint planning)"
   ```

2. **Replace stories 1.1-1.3 section with:**
   - Story 1.1: Deploy Calibre-Web-Automated on Raspberry Pi 4 (DONE)
   - Story 1.2: Configure hardware performance validation checkpoint (IN-PROGRESS)
   - Story 1.3: Configure auto-ingestion workflow with Hardcover metadata (BLOCKED-WAITING)
   - **Story 1.4: Design and implement unified database schema (BACKLOG)**
   - **Story 1.5: Implement library backup to separate storage (BACKLOG)**
   - **Story 1.6: Document Calibre CLI fallback procedures (BACKLOG)**

3. **Add cross-reference table** showing epic.md names → sprint-status.yaml keys:
   ```markdown
   | Epic 1 Planning Name | Sprint Story Key | Status |
   |---|---|---|
   | Deploy CWA + Unified Database Foundation | 1-1-deploy-calibre-web-automated-on-raspberry-pi-4 | DONE |
   | (Infrastructure) | 1-4-design-and-implement-unified-database-schema | BACKLOG |
   | (Backup) | 1-5-implement-library-backup-to-separate-storage | BACKLOG |
   | Auto-Ingestion + Metadata Enrichment | 1-2-configure-hardware-performance-validation-checkpoint | IN-PROGRESS |
   | | 1-3-configure-auto-ingestion-workflow-with-hardcover-metadata | BLOCKED-WAITING |
   | Fallback Procedures & Operational Resilience | 1-6-document-calibre-cli-fallback-procedures | BACKLOG |
   ```

4. **For Stories 1.4, 1.5, 1.6:** Extract from tech-spec-epic-1.md and add full user story format:
   - User story statement (As a..., I want..., So that...)
   - Acceptance criteria (from tech-spec)
   - Prerequisites and dependencies

---

### Phase 3: Create Missing Story Files (High Priority)

**Missing Stories:** 1.4, 1.5, 1.6

**Source:** Extract from tech-spec-epic-1.md sections:
- Objectives and Scope
- Detailed Design
- Data Models

**Story File Template to Create:**

#### Story 1.4: Design and implement unified database schema

```markdown
# Story 1.4: Design and implement unified database schema

Status: drafted

## Story

As a developer,
I want a unified PostgreSQL schema designed and initialized on Neon.tech,
So that reading session data from ebooks and audiobooks can be aggregated and queried across all sources.

## Acceptance Criteria

(Extract from tech-spec-epic-1.md "Data Models and Contracts" section)

1. Neon.tech free-tier PostgreSQL created and accessible
2. Books dimension table designed with fields: book_id, title, author, isbn, asin, source, media_type, cover_url, page_count, duration_minutes, published_date, created_at
3. Reading_sessions fact table designed with fields: session_id, book_id, start_time, end_time, pages_read, duration_minutes, device, media_type, device_stats_source, created_at
4. Schema supports both ebook + audiobook data via media_type field
5. Indexes created on frequently queried fields (book_id, start_time, device)
6. Database connection tested from development environment
7. Schema documentation created (ERD + field definitions)
8. Schema version control: documented in tech-spec-epic-1.md

## Tasks / Subtasks

[Derive from tech-spec Objectives and Data Models sections]

## Dev Notes

### Architecture Alignment

This story implements the **Data Layer** analytics foundation from the approved BookHelper architecture:
- Neon.tech PostgreSQL serves as centralized analytics warehouse
- Books and reading_sessions tables support Facts & Dimensions model
- Schema designed to accommodate ebook (pages, KOReader) and audiobook (duration, BookPlayer) data
- source and media_type fields enable consolidated queries across data origins

[Source: docs/architecture.md § 3.1. Data Layer; docs/tech-spec-epic-1.md § Data Models]

## References

- [docs/tech-spec-epic-1.md § Data Models and Contracts](../tech-spec-epic-1.md#data-models-and-contracts)
- [docs/architecture.md § 3.1. Data Layer](../architecture.md#31-data-layer-multi-tier-strategy)
```

#### Story 1.5: Implement library backup to separate storage

```markdown
# Story 1.5: Implement library backup to separate storage

Status: drafted

## Story

As a reader,
I want my ebook library and CWA configuration automatically backed up to cloud storage each night,
So that I have disaster recovery protection if the Raspberry Pi fails or the Calibre library becomes corrupted.

## Acceptance Criteria

(Extract from tech-spec-epic-1.md "Backup Infrastructure" section)

1. rclone installed on Raspberry Pi
2. Koofr WebDAV account configured as backup destination
3. Encryption configured: AES-256 encryption for all data in transit and at rest
4. Backup scope: entire ebook library folder + CWA configuration files (metadata.db, config folder)
5. Nightly backup scheduled via cron or systemd timer (e.g., 2 AM daily)
6. Initial backup completed successfully; files verified encrypted in Koofr
7. Backup logs created showing success/failure status and size transferred
8. Restore procedure documented: steps to recover library from encrypted Koofr backup

## Tasks / Subtasks

[Derive from tech-spec Backup Infrastructure section]

## Dev Notes

### Architecture Alignment

This story implements the **Sync & Backup Layer - Library Backup** from the approved BookHelper architecture:
- Disaster recovery backup layer protects against RPi hardware failure or data corruption
- One-way backup (RPi → Koofr) ensures backup never overwrites production library
- Encryption satisfies privacy-first architecture principle
- Nightly schedule balances protection with bandwidth/storage constraints

[Source: docs/architecture.md § 3.2. Sync & Backup Layer - Disaster Recovery Backup; docs/tech-spec-epic-1.md § Backup Infrastructure]

## References

- [docs/tech-spec-epic-1.md § Backup Infrastructure](../tech-spec-epic-1.md#backup-infrastructure)
- [docs/architecture.md § 3.2. Sync & Backup Layer](../architecture.md#32-sync--backup-layer-corruption-safe-design)
```

#### Story 1.6: Document Calibre CLI fallback procedures

```markdown
# Story 1.6: Document Calibre CLI fallback procedures

Status: drafted

## Story

As a developer,
I want documented Calibre CLI procedures for manual library management,
So that I have fallback procedures if CWA auto-ingest fails and can troubleshoot the library database.

## Acceptance Criteria

(Extract from tech-spec-epic-1.md and epics.md Story 1.3 section)

1. Documentation created showing how to add books via calibredb CLI
2. Metadata fetch command documented (calibredb fetch-ebook-metadata)
3. Batch import script provided for processing multiple files via CLI
4. Instructions for triggering CWA rescan after manual Calibre CLI additions
5. Troubleshooting guide for common CWA ingest failure modes
6. metadata.db backup/restore procedure documented
7. Examples provided for each command with expected output

## Tasks / Subtasks

[Derive from epics.md Story 1.3 Acceptance Criteria 1-7]

## Dev Notes

### Architecture Alignment

This story documents the **Library Management Layer - Fallback Procedures** from the approved BookHelper architecture:
- Provides operational resilience if primary CWA auto-ingest feature fails
- Calibre CLI represents proven, stable alternative for manual management
- Documented procedures reduce Mean Time To Recovery (MTTR) if ingest fails
- Supports "Stability Over Features" architecture principle

[Source: docs/architecture.md § 3.3. Library Management Layer; docs/tech-spec-epic-1.md § Objectives and Scope]

## References

- [docs/epics.md § Epic 1 § Story 1.3](../epics.md#story-13-fallback-procedures--operational-resilience)
- [docs/architecture.md § 3.3. Library Management Layer](../architecture.md#33-library-management-layer)
- [docs/tech-spec-epic-1.md § Out of Scope - OPDS, KOSync](../tech-spec-epic-1.md#out-of-scope)
```

---

### Phase 4: Create Tech Specs for Remaining Epics (Medium Priority)

**Missing Tech Specs:** Epic 3, Epic 4, Epic 5

**Current Status:**
- Tech Spec Epic 1: ✓ Complete (2025-10-26)
- Tech Spec Epic 2: ✓ Complete (2025-10-29)
- Tech Spec Epic 3: ✗ Not created (Epic 3 in progress: Story 3.1 review, 3.2 ready-for-dev)
- Tech Spec Epic 4: ✗ Not created (Epic 4 backlog)
- Tech Spec Epic 5: ✗ Not created (Epic 5 backlog)

**Recommendation:** Create Tech Spec Epic 3 before Story 3.2 implementation starts, to solidify schema design and ETL requirements.

---

### Phase 5: Establish Documentation Maintenance Protocol (Ongoing)

**Protocol:**

1. **When sprint-status.yaml changes:**
   - If epic/story status changed: Update corresponding story file (or note blocking reason)
   - If story count changed: Update epics.md summary

2. **When a story is marked DONE:**
   - Create/verify story file exists with all acceptance criteria marked ✓
   - Verify implementation guide/setup guide exists if applicable
   - Mark story file Status: done

3. **When a new epic starts planning:**
   - Create tech-spec-epic-N.md before stories are drafted
   - Update epics.md with expanded story list
   - Create story files from tech-spec using create-story workflow

4. **Monthly documentation sync (recommended):**
   - Check epics.md against sprint-status.yaml
   - Verify all story files match sprint-status.yaml entries
   - Update product-brief if scope changes

---

## Discrepancy Details

### Document Dependency Chain (Current State)

```
docs/PRD.md (2025-10-26) ← Requirements baseline
  ↓
docs/epics.md (2025-10-27) ← HIGH-LEVEL PLANNING (3 stories for Epic 1)
  ↓
docs/tech-spec-epic-1.md (2025-10-26) ← DETAILED DESIGN (6 work areas)
  ↓
docs/sprint-status.yaml (2025-10-30) ← CURRENT EXECUTION (6 stories for Epic 1)
  ↓
docs/stories/*.md (2025-10-27 onwards) ← IMPLEMENTATION ARTIFACTS
```

**Problem Area:** epics.md ↔ sprint-status.yaml out of sync

**Impact on Story 3.2:**
- Story 3.2 correctly identifies Story 1.4 as blocker
- Story 1.4 is real (confirmed in tech-spec-epic-1.md and sprint-status.yaml)
- Story 1.4 is just not documented in epics.md or as a story file yet

---

## Recommended Implementation Order

1. **Immediate (This Week):**
   - ✅ Create story files for 1.4, 1.5, 1.6 (using create-story workflow)
   - ✅ Update epics.md Epic 1 section with 6-story breakdown
   - ✅ Add cross-reference table in epics.md showing mapping

2. **Before Story 3.2 Implementation:**
   - ⏳ Create tech-spec-epic-3.md (consolidate ETL, analytics, monitoring requirements)
   - ⏳ Confirm Neon.tech schema (Story 1.4 prerequisite) will be prioritized

3. **During Phase 4 (Ongoing):**
   - 🔄 Keep sprint-status.yaml updated daily
   - 🔄 Update story files when acceptance criteria are met
   - 🔄 Create setup guides for completed stories

4. **When Epic 4 starts:**
   - Create tech-spec-epic-4.md
   - Update epics.md with Epic 4 story breakdown

---

## Summary Table: What's Authoritative

| Question | Answer | Source |
|----------|--------|--------|
| How many stories does Epic 1 have? | **6 stories** | sprint-status.yaml + tech-spec-epic-1.md |
| What is the status of Story 1.4? | **BACKLOG** (real story, needs file creation) | sprint-status.yaml |
| Is Story 1.4 a real blocker for Story 3.2? | **YES** (Neon.tech schema design is prerequisite) | tech-spec-epic-1.md (Data Models section) |
| Why is epics.md different? | **Outdated planning doc** (3-story high-level breakdown) | Phase 2 artifact; superseded by Phase 4 sprint-status |
| Should I follow epics.md or sprint-status.yaml? | **Follow sprint-status.yaml** (it's the working document) | Phase 4 implementation is the source of truth |
| When was this documented? | **Different times:** epics.md 2025-10-27, sprint-status.yaml 2025-10-30 | Timestamps show divergence point |

---

## Conclusion

**The project documentation is not broken—it's evolving normally:**

- **Phase 2 (Planning):** epics.md captured high-level 3-story breakdown ✓
- **Phase 2 (Architecture):** tech-spec-epic-1.md detailed the work (revealing 6 components) ✓
- **Phase 4 (Execution):** sprint-status.yaml decomposed into sprint-ready 6 stories ✓
- **Gap:** epics.md wasn't updated when execution plan changed ← **ACTION NEEDED**

**This is standard in software projects:** planning documents are snapshots; execution documents are living. The tech-spec confirmed the decomposition was sound.

**Next step:** Update epics.md and create missing story files to restore full sync across all documentation layers.
