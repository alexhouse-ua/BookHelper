# Product Brief: BookHelper

**Date:** 2025-10-24
**Author:** Alex
**Status:** Draft for PM Review

---

## Executive Summary

**BookHelper** is an automated reading infrastructure platform designed to solve the critical gaps faced by privacy-conscious readers transitioning from proprietary ecosystems (Amazon Kindle/Audible) to open-source alternatives (KOReader, self-hosted tools).

**The Problem:** Users migrating to open-source reading tools face three interconnected challenges: (1) years of historical reading data trapped in proprietary formats with no migration path, (2) valuable reading statistics at risk due to lack of automated backup, and (3) significant manual overhead for library management, metadata enrichment, and cross-device synchronization. Current solutions force users to choose between vendor lock-in and unsustainable time investment.

**The Solution:** BookHelper provides automated infrastructure across three domains: (1) one-time historical data migration from Kindle/Audible into KOReader-compatible format, (2) continuous automated backup of reading statistics to resilient cloud storage with unified database for analytics, and (3) zero-touch library management including auto-metadata enrichment, format optimization, and cross-device sync.

**Target Market:** Privacy-conscious, technically proficient readers (20+ books/year) who value data ownership, detailed reading statistics, and automation. Primary user is the product owner (self-use MVP), with potential future expansion to broader open-source reading community.

**Key Value Proposition:** Eliminate 95%+ of manual library management overhead while preserving complete reading history and enabling future analytics capabilities—all using free, open-source tools with zero ongoing costs. Users gain data sovereignty, automated workflows, and foundation for AI-powered reading insights without sacrificing privacy or investing in commercial platforms.

**MVP Success Criteria:** Complete historical data migration with zero corruption, automated library ingestion in <30 seconds per book, 99%+ backup uptime, and accessible unified database combining ebook + audiobook statistics across complete reading timeline.

---

## Problem Statement

Users transitioning from proprietary reading ecosystems (Amazon Kindle/Audible) to open-source alternatives face three critical, interconnected problems that prevent them from fully owning and leveraging their reading data:

**1. Historical Data Loss and Fragmentation**
- Years of reading history locked in proprietary formats (Kindle, Audible) cannot transfer to new tools
- Reading statistics, progress tracking, and behavioral data are siloed across incompatible platforms
- No path exists to consolidate historical ebook and audiobook data into a unified timeline

**2. Data Vulnerability and Backup Gaps**
- Reading statistics files (KOReader's statistics.sqlite3) are stored locally with no automated backup strategy
- Risk of catastrophic data loss from device failure, corruption, or accidental deletion
- No reliable cloud sync solution validated for cross-device access and disaster recovery
- Library files stored on single PC create single point of failure

**3. Manual Library Management Friction**
- Ebook ingestion requires manual steps: download → metadata lookup → format fixing → device transfer
- No automated workflow for metadata enrichment, cover art retrieval, or format standardization
- Library access limited to home network; remote access requires manual VPN/configuration
- Cross-device synchronization (iOS, Boox Palma 2) relies on fragile manual processes
- Audiobook tooling (BookPlayer) provides inconsistent sync with reading platforms (Hardcover.app)

**Quantifiable Impact:**
- Risk of losing 2+ years of detailed reading statistics representing hundreds of hours of reading activity
- 15-30 minutes per book spent on manual metadata management and device transfers
- No consolidated view of reading patterns across ebooks and audiobooks, preventing data-driven reading habit optimization
- Inability to perform historical analysis or trend identification across reading history

**Why This Matters Now:**
Having successfully transitioned away from Amazon's ecosystem to privacy-focused alternatives (Boox Palma 2 + KOReader), the infrastructure gaps are now critical blockers. Without automated solutions, continuing to read means either accepting ongoing manual overhead or risking permanent loss of valuable historical data. The window to migrate Kindle/Audible history is now—before data exports become stale or unavailable—and the daily friction of manual library management is unsustainable for long-term use.

---

## Proposed Solution

BookHelper is an automated reading infrastructure platform that unifies, protects, and enhances the open-source reading experience through three integrated capabilities:

**1. Historical Data Migration Engine with Hardcover Reconciliation**
- One-time data pipeline that ingests Kindle and Audible historical data exports
- Transforms proprietary formats into KOReader-compatible statistics.sqlite3 entries
- Reconciles and validates migrated data against Hardcover.app (primary source of truth for reading records)
- Handles books present in Hardcover but not in Kindle/Audible exports (e.g., Hoopla imports, Goodreads orphans) with graceful fallback to available metadata
- Preserves reading timeline continuity while maintaining database integrity for ongoing KOReader use
- Ensures overlapping fields match across all sources (Kindle, Audible, Hardcover, KOReader)

**2. Automated Backup, Hardcover Integration, and Unified Database**
- Continuous synchronization of reading statistics (ebooks + audiobooks) to resilient cloud storage
- Deep Hardcover.app API integration as primary source for book metadata and reading habit data
- Hardcover as system of record for ratings, annotations, and notes (non-negotiable)
- Centralized database (e.g., Supabase) consolidating all reading data with accessible API layer
- Research-validated backup strategy for KOReader statistics (cloud sync vs. alternative approaches)
- Automated conflict resolution and data merging across devices
- Future-ready data model supporting analytics, visualization, and AI-powered insights

**3. Automated Library Management System with Priority on Metadata Automation**
- Zero-touch ebook ingestion: drop files → auto-metadata enrichment (via Hardcover API) → format optimization → device sync
- Self-hosted library server (Calibre-Web-Automated or validated alternative) with remote access
- Cross-device availability (iOS Readest, Boox Palma 2 KOReader) via local and internet access
- Unified library system supporting both ebooks and audiobooks (separate only if unified solution unavailable; metadata automation prioritized)
- Automated backup separate from primary PC to prevent data loss
- Syncthing integration for seamless file synchronization

**Key Differentiators:**
- **Data Sovereignty:** Complete ownership and control of all personal reading data
- **Hardcover-Centric:** Hardcover.app serves as system of record for ratings, metadata, and reading behavior insights
- **Ecosystem Agnostic:** Works across proprietary legacy data (Kindle/Audible) and open-source tools (KOReader)
- **Zero Manual Overhead:** Automation eliminates repetitive metadata and sync tasks via intelligent API integration
- **Analytics Foundation:** Database architecture designed for future statistical analysis and AI integration, powered by comprehensive Hardcover data
- **Resilience First:** Multiple backup layers and fault-tolerant infrastructure prevent data loss

**Why This Will Succeed:**
BookHelper solves immediate pain points from transitioning to open-source reading tools (data loss risk, manual overhead) while establishing infrastructure for future personal reading analytics. The solution leverages existing tools and data (Hardcover.app, KOReader, Kindle/Audible exports) to create an automated, resilient system that enables a reading habit that would otherwise require unsustainable manual effort or compromise privacy with commercial platforms.

---

## Target Users

### Primary User Segment

**Privacy-Conscious Data-Driven Readers**

**Profile:**
- Active readers (20+ books/year) with 2+ years of digital reading history
- Technically proficient enough to adopt open-source tools (KOReader, self-hosted services)
- Strong preference for data ownership, privacy, and avoiding vendor lock-in
- "Data nerds" who value reading statistics, tracking, and quantified self-improvement

**Current Behavior:**
- Recently migrated or planning migration from Kindle/Audible to open-source alternatives
- Uses KOReader for detailed reading statistics and customization
- Relies on Hardcover.app instead of Goodreads for open API access
- Manually manages ebook library with tools like Calibre
- Frustrated by data fragmentation and lack of automation

**Pain Points:**
- Cannot access years of Kindle/Audible reading history in new tools
- Fears losing valuable KOReader statistics due to lack of backup
- Spends significant time on manual metadata management and device sync
- No consolidated view of ebook + audiobook reading patterns

**Goals:**
- Preserve complete reading history across ecosystem transitions
- Automate tedious library management tasks
- Ensure reading data is backed up and accessible long-term
- Enable data analysis and visualization of reading habits

**Success Definition:**
- Zero manual effort for library management after initial setup
- Complete reading history visible in unified database
- Confidence that reading data is protected from loss
- Ability to answer questions like "How many hours did I read in 2024?" or "What's my average reading speed by genre?"

**Note:** This is a single-user personal project with no intention to expand beyond self-use. Documentation and design decisions are optimized for personal use and to support multiple AI agents assisting with development across sessions.

---

## Goals and Success Metrics

### Business Objectives

**Personal Project Goals (Self-Use MVP):**
1. **Data Preservation:** Successfully migrate 100% of Kindle and Audible historical data into unified database without loss
2. **Automation Achievement:** Reduce library management time from 15-30 min/book to <1 min/book (95%+ reduction)
3. **Infrastructure Resilience:** Implement automated backup with 99.9% uptime for reading statistics protection
4. **Knowledge Building:** Develop reusable technical knowledge for open-source reading infrastructure that could benefit broader community

**Personal Learning & Development (Future):**
- Deep technical knowledge in data engineering, self-hosted infrastructure, and automation
- Reusable patterns and architecture for potential future personal projects
- Documentation to maintain understanding across development sessions with AI assistants

### User Success Metrics

**Data Migration Success:**
- 100% of Kindle reading history successfully imported into KOReader statistics format
- 100% of Audible listening history integrated into unified database
- Zero data corruption or loss during migration process
- KOReader continues functioning normally post-migration (existing workflows unaffected)

**Automation and Efficiency:**
- Library ingestion workflow: <30 seconds from file drop to device availability
- Zero manual metadata lookups required post-setup
- 100% automated sync success rate between devices (iOS, Boox Palma 2)
- Reading statistics backup occurs within 5 minutes of device sync

**Data Access and Reliability:**
- Library accessible remotely (off home network) with <500ms latency
- Reading statistics queryable via API/database interface
- 30-day backup retention minimum with point-in-time recovery capability
- Cross-device sync completion within 2 minutes of file changes

**User Experience:**
- Single command/action initiates complete ebook ingestion workflow
- Reading data queries answerable within seconds (e.g., "total pages read in 2024")
- Zero instances of data loss or corruption over 6-month period
- Library and statistics accessible from any approved device without manual intervention

### Key Performance Indicators (KPIs)

**Critical MVP KPIs:**
1. **Historical Data Coverage:** % of Kindle/Audible history successfully migrated (Target: 100%)
2. **Automation Rate:** % of library management tasks requiring zero manual intervention (Target: 95%+)
3. **Data Availability:** % uptime of statistics backup and library access (Target: 99%+)
4. **Sync Reliability:** % successful automated syncs without manual intervention (Target: 98%+)
5. **Migration Integrity:** Database validation checks passed post-migration (Target: 100%)

**Secondary KPIs:**
- Time saved per book on library management (Target: 15-30 min → <1 min)
- Number of reading data queries successfully executed via unified database
- Mean time to recovery (MTTR) for backup restoration if needed
- Cross-device sync latency (Target: <2 minutes)

---

## Strategic Alignment and Financial Impact

### Financial Impact

**Development Investment:**
- **Cost:** $0 (self-developed, free/open-source tools only)
- **Time Investment:** Estimated 40-80 hours development + 20-40 hours research/testing
- **Infrastructure Costs:** $0/month (self-hosted on existing hardware, free-tier cloud services where needed)

**Value Delivered:**
- **Time Savings:** 15-30 min/book × 20-50 books/year = 5-25 hours/year saved on library management
- **Data Protection:** Invaluable preservation of 2+ years reading history (hundreds of hours of reading data)
- **Avoided Costs:** Eliminated need for commercial reading analytics platforms (comparable services: $5-15/month = $60-180/year)
- **Opportunity Value:** Foundation for future analytics, AI agents, and potential productization

**ROI Calculation:**
- Break-even: Time investment recovers within 2-6 years via automation savings alone
- Intangible value: Data preservation, privacy, learning, and future capability building significantly exceed time investment

**Budget Constraints:**
- Hard requirement: $0 ongoing costs (free-tier cloud services, open-source tools only)
- Infrastructure must run on existing hardware (PC, iOS, Boox Palma 2)

### Company Objectives Alignment

**Personal Strategic Objectives:**
1. **Data Sovereignty:** Full control and ownership of personal reading data aligned with privacy values
2. **Skill Development:** Deep technical learning in data engineering, self-hosted infrastructure, automation
3. **Quantified Self:** Enable data-driven insights into reading habits for continuous improvement
4. **Open Source Contribution:** Build knowledge and potentially contribute back to KOReader/Calibre communities

**Alignment with Broader Technology Values:**
- Privacy-first infrastructure (no reliance on big tech platforms)
- Open-source ecosystem support and contribution
- Self-hosted, self-sufficient technical capabilities
- Data portability and future-proofing against platform changes

### Strategic Initiatives

**Primary Strategic Initiative: Reading Infrastructure Modernization**
- Replace fragmented, proprietary reading data systems with unified, open-source infrastructure
- Establish resilient, automated workflows that eliminate manual overhead
- Create analytics-ready data foundation for future insights and AI integration

**Supporting Initiatives:**
1. **Self-Hosting Capability Building:** Develop expertise in running production-grade self-hosted services
2. **Data Engineering Foundation:** Build reusable patterns for data migration, transformation, and consolidation
3. **Automation Excellence:** Implement zero-touch workflows across the reading lifecycle
4. **Knowledge Sharing:** Document learnings that could benefit broader open-source reading community

**Opportunity Cost:**
- **NOT Building This:** Continue losing time to manual workflows, risk data loss, forfeit reading analytics capabilities
- **Alternative Approaches Rejected:** Commercial platforms (privacy concerns, vendor lock-in), manual processes (unsustainable time cost)

---

## MVP Scope

### Core Features (Must Have)

**Epic 1: Historical Data Migration**
- Kindle data parser: Extract reading history, highlights, timestamps from Amazon data export
- Audible data parser: Extract listening history, progress, completion dates from Audible export
- KOReader statistics transformer: Convert Kindle/Audible data into statistics.sqlite3 compatible format
- Data validation engine: Verify migration integrity and KOReader compatibility post-import
- Migration rollback capability: Backup and restore mechanism if migration fails

**Epic 2: Automated Statistics Backup & Unified Database**
- Research & validate KOReader backup strategy (cloud sync vs. alternatives)
- Automated statistics sync: Continuous backup of statistics.sqlite3 to cloud storage
- Unified database implementation: Centralized store (Supabase or validated alternative) for all reading data
- Database schema: Unified model combining ebook + audiobook statistics with query API
- Conflict resolution: Handle multi-device updates without data loss

**Epic 3: Automated Library Management with Hardcover API Integration**
- Library server deployment: Self-hosted solution (Calibre-Web-Automated or validated alternative)
- Auto-ingestion workflow: Folder monitoring → Hardcover API metadata enrichment → format optimization → sync
- Metadata automation: Intelligent lookup via Hardcover API, embedded book metadata, cover art, page counts, ratings
- Cross-device sync: Syncthing or alternative for iOS (Readest) + Boox Palma 2 (KOReader) access
- Remote access configuration: Secure internet access to library from any location
- Library backup: Separate backup independent of PC storage
- Hardcover API integration: Continuous sync of ratings, metadata, and reading data

**Epic 4: Audiobook Integration with Unified Library & Statistics**
- Audiobook player evaluation: Research BookPlayer, audiobookshelf, shelfbridge for Hardcover sync reliability and library integration capability
- Selected tool implementation: Deploy and configure chosen audiobook solution
- Library integration: Unified library server supporting both ebooks and audiobooks (or separate if necessary)
- Audiobook statistics extraction: Capture listening time, progress, completion data from chosen player and Hardcover.app
- Unified database integration: Merge audiobook stats with ebook data in central database (KOReader statistics.sqlite3 remains ebook-only)
- Hardcover audiobook data sync: Ensure audiobook ratings and metadata from Hardcover are synced to unified database

**Epic 5: System Integration & Validation**
- End-to-end testing: Validate complete workflow from file drop to device availability
- Data query interface: API or query tool for reading statistics analysis
- Documentation: Setup guides, troubleshooting, maintenance procedures
- Monitoring & alerting: Automated checks for backup failures, sync issues

### Out of Scope for MVP

**Analytics & Visualization (Phase 2):**
- Visual dashboards showing reading patterns, trends, insights
- Advanced statistical analysis (reading speed by genre, time-of-day patterns, etc.)
- Predictive recommendations based on reading history

**AI Integration (Phase 2):**
- AI agent for reading data analysis and recommendations
- Natural language queries against reading database
- Automated research suggestions based on reading history

**Community/Multi-User Features (Future):**
- Support for multiple users/family members
- Shared libraries or reading lists
- Social features or reading groups

**Advanced Library Features (Future):**
- Automatic book recommendations and acquisition
- Integration with library lending systems
- Format conversion beyond basic optimization
- Advanced tagging, collections, or organizational systems

**Platform Expansion (Future):**
- Android device support
- Desktop reading apps beyond web access
- Additional e-reader hardware integrations

### MVP Success Criteria

**MVP is complete when:**

1. **Data Migration Validated:**
   - All Kindle and Audible historical data successfully imported into unified database
   - KOReader statistics.sqlite3 updated with historical data and remains functional
   - Zero data loss or corruption detected via validation checks

2. **Automation Operational:**
   - Single-action ebook ingestion (drop file → auto-processed → device available)
   - Reading statistics automatically backed up within 5 minutes of sync
   - Library accessible remotely with no manual intervention required

3. **Infrastructure Resilient:**
   - Automated backup system operational with 30-day retention
   - Library backup separate from PC (survives PC failure)
   - Cross-device sync working reliably (iOS + Boox Palma 2)

4. **Data Accessible:**
   - Unified database queryable via API/interface
   - Can answer questions like "total pages read in 2024" within seconds
   - Reading history visible as continuous timeline across Kindle/Audible/KOReader

5. **Zero Manual Overhead:**
   - No metadata lookups required for new books
   - No manual sync steps between devices
   - No manual backup procedures needed

**Validation Test:**
- Add new ebook → verify auto-metadata → verify device availability → verify statistics backup
- Query unified database for historical reading stats across all sources
- Simulate PC failure → verify library recovery from backup
- Access library remotely from phone → verify responsiveness

---

## Post-MVP Vision

### Phase 2 Features

**Analytics & Visualization Dashboard:**
- Interactive visualizations of reading patterns over time
- Reading velocity analysis (pages/hour by genre, time-of-day, etc.)
- Trend identification (reading habits evolution, genre preferences shifts)
- Goal tracking (annual reading targets, completion rates)
- Comparative analytics (ebook vs. audiobook consumption patterns)

**AI-Powered Reading Assistant:**
- Natural language query interface ("What was my average reading speed in Q1 2024?")
- Automated insights generation ("You read 40% more fiction this year")
- Reading recommendations based on historical patterns and preferences
- Predictive analytics (estimated completion dates, reading goal projections)
- Integration with Hardcover.app for enhanced recommendation context

**Enhanced Data Integration:**
- Goodreads data import (for users with historical Goodreads data)
- Integration with additional reading platforms or services
- Social reading data (book club participation, shared reading lists)
- Library lending integration (track borrowed books, due dates)

### Long-term Vision

**Personal Reading Intelligence Platform (1-2 Years):**

BookHelper evolves from infrastructure automation to an intelligent reading companion that provides deep insights and proactive assistance:

- **Comprehensive Reading Analytics:** Understand not just what you read, but how, when, and why through multi-dimensional analysis
- **Predictive Capabilities:** AI agent anticipates reading needs, suggests optimal reading times, identifies emerging interests
- **Automated Discovery:** System proactively finds and suggests books based on nuanced understanding of preferences
- **Lifetime Reading Archive:** Complete, searchable, analyzable record of every book ever read with rich contextual data
- **Cross-Platform Intelligence:** Seamlessly integrates data from any reading source (past, present, future)

### Advanced Personal Features (Post-MVP)

**Analytics & Intelligence:**
- Advanced analytics dashboards for deep reading habit analysis
- Reading velocity and comprehension metrics by genre, time-of-day, device
- Trend identification and pattern recognition across complete reading history
- AI-powered reading recommendations based on personal data and preferences
- Predictive analytics for estimated completion dates and reading projections

**Library & Integration Enhancements:**
- Advanced library organization (AI-powered tagging, smart collections)
- Format conversion and optimization capabilities for broader device compatibility
- Integration with note-taking systems (Obsidian, Notion, etc.) for reading annotations
- Enhanced metadata enrichment beyond Hardcover.app data
- Reading habit coaching and optimization recommendations

**Data & Experience:**
- Custom visualizations specific to personal reading patterns
- Multi-year trend analysis and historical comparisons
- Integration with additional reading data sources if available
- Personal insights and milestone tracking

---

## Technical Considerations

### Platform Requirements

**Device Support (Hard Requirements):**
- **iOS:** iPhone running Readest (ebook reader) and selected audiobook player
- **Boox Palma 2:** E-ink device running KOReader (primary ebook reader)
- **PC (Development/Server):** Windows/Linux for library server and development environment
- **Cross-Platform:** Web-based interfaces accessible from any device with browser

**Network Access Requirements:**
- **Home Network:** High-performance local access to library server
- **Remote Access:** Secure internet access to library from any location
- **Sync Capability:** Bidirectional synchronization between all devices
- **Offline Mode:** Devices must function offline with periodic sync when connectivity available

**Performance Requirements:**
- Library server response time: <500ms for remote access
- Metadata lookup and enrichment: <30 seconds per book
- Cross-device sync latency: <2 minutes for file changes
- Database query response: <2 seconds for complex analytics queries
- Statistics backup: <5 minutes after device sync

**Accessibility Standards:**
- Web interfaces must be responsive (mobile, tablet, desktop)
- APIs must be well-documented for future integration and extension
- Data must be exportable in standard formats (JSON, CSV, SQLite)

### Technology Decisions (Research-Validated)

**✅ FINALIZED TECHNOLOGY STACK**

**Database & Storage:**
- **Selected:** **Neon.tech PostgreSQL (Free Tier)** - 5GB storage, no inactivity pausing, no credit card required
- **Rationale:** Superior to Supabase (avoids 7-day pause issue) and Fly.io (no credit card, larger storage)
- **Data Format:** SQLite for KOReader compatibility, PostgreSQL for ebook analytics database
- **Access Method:** Direct PostgreSQL connections (psycopg2) for ETL scripts

**Library Management Server:**
- **Selected:** **Calibre-Web-Automated v3.1.0+** (ebook-only configuration)
- **Features:** Built-in KOSync server, OPDS catalog, Hardcover.app metadata provider, automated ingest
- **Infrastructure:** Docker container on Raspberry Pi 4 2GB
- **Resource Usage:** ~400-600MB RAM (validated sufficient for ebook-only workload)
- **⚠️ Known Risk:** Former contributor warnings about ingest stability ("hack," "bound to break") - accepted for feature benefits

**Host Server:**
- **Selected:** **Raspberry Pi 4 2GB**
- **Validated:** Sufficient for ebook-only CWA stack (~500-750MB total usage, ~750-1000MB buffer)
- **Future:** Upgrade to RPi 5 4GB+ if adding Audiobookshelf later

**File Synchronization:**
- **Ebook Library:** **Syncthing** (Android to RPi) - "Receive Only" on Boox Palma for one-way library sync
- **Statistics Backup:** **Syncthing** "Send Only" from Boox → RPi (disaster recovery, one-way to prevent corruption)
- **iOS:** **OPDS protocol** (NO file sync) - Readest downloads from CWA on-demand to avoid iOS background sync issues
- **⚠️ Critical:** NEVER two-way sync of `statistics.sqlite3` (causes irreversible corruption)

**Progress Synchronization:**
- **Ebook Devices:** **CWA KOSync Server** (built-in) - KOReader (Boox) ↔ Readest (iOS) progress sync
- **Application-aware protocol** (NOT file-level sync) - safe for live SQLite database

**Audiobook Management:**
- **Selected:** **BookPlayer (iOS)** - manual file management, native Hardcover.app sync
- **Rationale:** Defers Audiobookshelf complexity to future RPi 5 upgrade
- **File Transfer:** Manual (AirDrop, Files app, USB)
- **No server-side infrastructure needed** for MVP

**Hardcover.app Integration:**
- **Ebooks:** **KOReader hardcoverapp.koplugin** - links books, updates reading progress to Hardcover
- **Audiobooks:** **BookPlayer native sync** - manual trigger, updates listening progress to Hardcover
- **Result:** Hardcover.app becomes unified reading timeline for ALL media (ebooks + audiobooks)
- **✅ Complete Coverage** - No gaps in Hardcover integration

**Development Stack:**
- **Languages:** Python (ETL scripts, data transformation), Bash (automation, backups)
- **APIs:** PostgreSQL (psycopg2), Hardcover.app GraphQL API (optional for analytics enrichment)
- **Infrastructure:** Docker Compose for container orchestration

**Cloud Services (Free Tier Only):**
- **Backup Storage:** **Koofr (10GB free, WebDAV)** - primary backup via rclone encrypted remote
- **Database:** **Neon.tech PostgreSQL** - ebook analytics data warehouse
- **Remote Access:** **Tailscale** - zero-config mesh VPN, unanimous research recommendation
- **Progress Sync:** **CWA KOSync** (self-hosted) - no external cloud dependency for ebook progress

### Final Architecture (Research-Validated)

**System Architecture Philosophy:**
- **Data Safety First:** Separation of live progress sync from disaster recovery backups (prevents SQLite corruption)
- **Stability Over Features:** Proven, maintained components over cutting-edge but unstable solutions
- **Modular Design:** Independent components that can be replaced or upgraded without system-wide changes
- **Data Ownership:** All data stored in accessible, standard formats (no proprietary lock-in)
- **Resilience:** Multiple backup layers (local + cloud), one-way sync patterns, versioned backups
- **Privacy-First:** Self-hosted core services, minimal cloud dependencies, Tailscale private mesh network

**Finalized System Architecture:**

```
┌─────────────────────────────────────────────────────────────┐
│                 RASPBERRY PI 4 2GB (Host Server)            │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ Docker Compose Stack:                                  │ │
│  │  • Calibre-Web-Automated (Ebook Library + KOSync)      │ │
│  │  • Syncthing (File Sync Service)                       │ │
│  │  • Tailscale (Private Mesh VPN)                        │ │
│  │                                                         │ │
│  │ Scheduled Services:                                    │ │
│  │  • rclone → Koofr (Nightly Encrypted Backup)           │ │
│  │  • ETL Script → Neon.tech (Statistics Aggregation)     │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                            │
           ┌────────────────┴────────────────┐
           │                                  │
    ┌──────▼──────┐                  ┌───────▼────────┐
    │ BOOX PALMA 2│                  │  iPHONE (iOS)  │
    │  (Android)  │                  │                │
    │             │                  │                │
    │ • KOReader  │◄─────KOSync─────►│ • Readest      │
    │ • Syncthing │                  │ • Tailscale    │
    │   (2 modes) │                  │ • BookPlayer   │
    │ • Tailscale │                  │   (audiobooks) │
    │ • Hardcover │                  │ • Hardcover    │
    │   Plugin    │                  │   (native)     │
    └─────────────┘                  └────────────────┘
           │                                  │
           └──────────────┬───────────────────┘
                          │
                    ┌─────▼─────┐
                    │ HARDCOVER │  ← Unified Reading Timeline
                    │   .app    │     (Ebooks + Audiobooks)
                    └───────────┘

    ┌───────────────────┐
    │   Neon.tech       │  ← Ebook Analytics Database
    │   PostgreSQL      │     (Deep Statistics)
    └───────────────────┘

    ┌───────────────────┐
    │   Koofr           │  ← Encrypted Cloud Backup
    │   (WebDAV)        │     (Library + Configs)
    └───────────────────┘
```

**Key Architectural Components:**

**1. Data Layer (Multi-Tier Strategy):**
- **KOReader statistics.sqlite3** (device) - Source of truth for ebook reading statistics
- **CWA metadata.db** (server) - Calibre library database (ebook metadata, file locations)
- **Neon.tech PostgreSQL** (cloud) - Analytics data warehouse (ebook statistics only for MVP)
- **Hardcover.app** (cloud) - Unified reading timeline (ebooks + audiobooks progress and metadata)
- **Ebook files** (server + Boox) - Master library on RPi, synced copy on device
- **Audiobook files** (iOS only) - Manual management via BookPlayer

**2. Sync & Backup Layer (Corruption-Safe Design):**

**Progress Sync (Application-Aware, Live Data):**
- **KOReader ↔ Readest:** CWA KOSync server (self-hosted, database protocol, NOT file sync)
- **KOReader → Hardcover:** hardcoverapp.koplugin (updates reading progress via API)
- **BookPlayer → Hardcover:** Native BookPlayer sync (manual trigger, updates listening progress)

**File Sync (Ebook Library):**
- **Server → Boox:** Syncthing "Send Only" from RPi, "Receive Only" on Palma (one-way library distribution)
- **Server → iOS:** OPDS protocol (on-demand download via Readest, NO background file sync)

**Disaster Recovery Backup (One-Way, Versioned):**
- **Statistics Backup:** Syncthing "Send Only" from Boox → RPi `statistics.sqlite3` copy (disaster recovery only)
- **Library Backup:** rclone encrypted → Koofr (nightly sync of ebook library + CWA configs)
- **⚠️ CRITICAL:** Statistics backup is one-way ONLY - server never writes back to device (prevents corruption)

**3. Library Management Layer:**
- **Ingestion:** CWA auto-ingest (folder monitoring → Calibre import → metadata enrichment)
- **Metadata:** Hardcover.app provider (primary), Google Books fallback, manual editing via CWA web UI
- **Format Optimization:** CWA epub fixer, Calibre conversion engine
- **OPDS Catalog:** CWA OPDS feed for Readest iOS access

**4. Access Layer:**
- **Local Network:** Direct access to RPi services (CWA web UI, OPDS, KOSync)
- **Remote Access:** Tailscale mesh VPN (all devices, zero-config, private 100.x.x.x network)
- **Web UI:** CWA responsive web interface (library browsing, metadata editing)
- **Device Clients:** KOReader (Boox), Readest (iOS) via OPDS + KOSync

**5. Analytics Layer (MVP Scope):**
- **ETL Pipeline:** Nightly Python script (statistics.sqlite3 → transform → Neon.tech)
- **Data Warehouse:** Neon.tech PostgreSQL (ebook sessions, page timing, reading velocity)
- **Query Access:** Direct SQL queries via PostgreSQL clients (DBeaver, pgAdmin, psql)
- **Future:** Grafana dashboards, AI-powered insights (Phase 2)

### ⚠️ Critical Warnings & Risk Mitigation

**CRITICAL WARNING: SQLite Corruption Risk**

All three research documents unanimously identify **file-level sync of live SQLite databases as the #1 cause of catastrophic data loss**. This architecture implements mandatory safeguards:

**The Problem:**
- KOReader's `statistics.sqlite3` is a live database with frequent write operations
- File-level sync tools (Syncthing, Dropbox, Google Drive) copy files at the filesystem level
- If sync occurs during a database write transaction, the copied file contains a "torn write"
- Result: **Corrupted database = total, irreversible loss of all reading history**

**Mandatory Architecture Requirements (Non-Negotiable):**

1. **✅ Progress Sync MUST use application-aware protocols:**
   - CWA KOSync server (database-aware, handles transactions correctly)
   - KOReader hardcoverapp.koplugin (uses Hardcover API, not file sync)
   - **NEVER** use Syncthing, Dropbox, or any file-level tool for progress sync

2. **✅ Statistics Backup MUST be one-way:**
   - Syncthing configured as "Send Only" from Boox Palma to RPi
   - Device is ALWAYS source of truth
   - Server NEVER writes back to device (prevents conflicts and corruption)
   - This is disaster recovery only, NOT for progress sync

3. **✅ Separation of concerns is MANDATORY:**
   - **Live Progress Sync:** KOSync (application-aware, real-time)
   - **Disaster Recovery:** Syncthing one-way backup (file-level, scheduled)
   - These two functions MUST NEVER be mixed

**Consequences of Violation:**
- **Immediate:** Database becomes unreadable ("malformed database" errors)
- **Data Loss:** 100% of reading history lost (unrecoverable)
- **No Warning:** Corruption is silent until database is accessed
- **Research Consensus:** This is the most common cause of user data loss

**Validation Steps (Must perform during setup):**
1. Verify Syncthing folders configured as "Send Only" (Boox) and "Receive Only" (RPi)
2. Verify KOSync is configured and working independently
3. Never configure Syncthing to sync the KOReader settings folder in both directions
4. Test disaster recovery: Manually corrupt backup copy, verify device database unaffected

---

**Known Risk: CWA Ingest Stability**

**Research Finding:** Former CWA contributor describes auto-ingest as:
- "A hack built on Calibre's destructive import process"
- "Bound to break eventually"
- "Subpar metadata fetching compared to raw Calibre"

**Risk Level:** Medium
**Impact if Fails:** Ingest stops working, manual Calibre CLI intervention required
**Mitigation Strategy:**
1. Monitor CWA logs for ingest errors
2. Keep Calibre CLI tools installed on server as fallback
3. Maintain manual ingest procedure documentation
4. Test ingest with non-critical books first
5. Backup metadata.db before bulk imports

**Acceptance Criteria:** Features (KOSync, auto-ingest, Hardcover metadata) outweigh stability risk for MVP. If ingest breaks, fallback to Calibre CLI preprocessing exists.

---

**Resource Constraint: RPi 4 2GB**

**Current Headroom:** ~750-1000MB buffer with ebook-only CWA stack
**Risk Scenario:** Memory pressure during large library scans or metadata processing

**Monitoring Plan:**
- Set up system monitoring (htop, docker stats)
- Monitor during first large library import
- Watch for OOM killer activity in system logs

**Escalation Plan:**
1. If crashes occur: Add 2GB USB swap file (degrades performance but prevents crashes)
2. If persistent: Upgrade to RPi 5 4GB or 8GB
3. If adding Audiobookshelf later: Hardware upgrade required

**Current Status:** ✅ Validated sufficient for ebook-only workload per research

---

**Hardcover.app API Dependencies**

**Components Relying on Hardcover:**
- CWA metadata provider (ebook metadata enrichment)
- hardcoverapp.koplugin (ebook progress sync)
- BookPlayer (audiobook progress sync)

**Risk:** Hardcover.app API changes or becomes unavailable
**Impact:** Metadata enrichment breaks, progress sync to Hardcover stops
**Mitigation:**
- CWA has fallback metadata providers (Google Books, Open Library)
- Local reading stats (statistics.sqlite3, Neon.tech) unaffected
- Hardcover provides reading timeline, but is not critical infrastructure

**Acceptance:** Low risk - Hardcover is actively maintained, has large user base, provides migration tools

### Integration Points & Data Flow

**External Service Integrations:**
- **Hardcover.app GraphQL API:**
  - CWA metadata provider (ebook metadata enrichment during ingest)
  - hardcoverapp.koplugin (ebook reading progress updates via API)
  - BookPlayer native sync (audiobook listening progress)
  - Optional: ETL enrichment queries for Neon.tech analytics

**Device Integration Protocols:**
- **KOSync Protocol:** CWA server ↔ KOReader (Boox) ↔ Readest (iOS) - bidirectional progress sync
- **OPDS Protocol:** CWA server → Readest (iOS) - on-demand ebook downloads
- **Syncthing Protocol:**
  - Library sync: RPi → Boox Palma (one-way, "Receive Only" on device)
  - Statistics backup: Boox Palma → RPi (one-way, "Send Only" from device)

**Data Export/Migration (One-Time, Future Epics):**
- Kindle historical data export → KOReader statistics format (Epic 1)
- Audible historical data export → unified database (Epic 1)
- Hardcover API as reconciliation source for migration validation

---

## Constraints and Assumptions

### Constraints

**Financial Constraints:**
- **Zero Budget:** All solutions must use free/open-source tools and free-tier cloud services
- **No Ongoing Costs:** Infrastructure must run on existing hardware with no recurring fees
- **Time Investment:** Development time is limited; must prioritize automation over perfect solutions

**Hardware Constraints:**
- **Fixed Devices:** iOS (iPhone) and Boox Palma 2 (e-ink device) are non-negotiable
- **PC Dependency:** Library server requires PC to remain operational (mitigated by backups)
- **Storage Limits:** PC storage is finite; cloud backup limited to free-tier quotas

**Technical Constraints:**
- **KOReader Compatibility:** Cannot break or modify KOReader's statistics.sqlite3 schema
- **Data Format Lock-in:** Must work with proprietary Kindle/Audible export formats
- **iOS Limitations:** App ecosystem limited; cannot run arbitrary background services
- **Network Requirements:** Reliable internet required for remote access and sync

**Skill/Knowledge Constraints:**
- **Learning Curve:** Some technologies require research and skill development
- **Maintenance Burden:** Self-hosted services require ongoing management and troubleshooting
- **Community Support:** Reliance on open-source documentation and community forums

**Privacy & Security Constraints:**
- **No Cloud Lock-in:** Must avoid proprietary cloud platforms that could restrict data access
- **Encryption Required:** Reading data must be encrypted during sync/backup
- **Access Control:** Remote access must be secured (no public exposure of library)

### Key Assumptions

**Technical Assumptions:**
- KOReader cloud sync or alternative backup strategy exists and is reliable
- Kindle/Audible data exports contain sufficient information for reconstruction
- Metadata services (Open Library, Google Books) provide adequate coverage for library
- SQLite and PostgreSQL can coexist for different use cases (device vs. analytics)
- Syncthing or alternative can reliably sync between iOS and Linux devices

**User Behavior Assumptions:**
- Reading happens primarily on Boox Palma 2 (KOReader) with occasional iOS use
- Audiobook consumption is secondary to ebook reading
- New books added at manageable rate (not hundreds per week)
- PC library server remains powered on or can wake-on-LAN for remote access
- Historical data from Kindle/Audible is one-time migration (no ongoing sync needed)

**Data Assumptions:**
- Kindle data export includes reading history, progress, and timestamps
- Audible data export includes listening history and completion dates
- KOReader statistics schema remains stable across versions
- Historical data accuracy is "good enough" (approximate timestamps acceptable)

**Platform & Tool Assumptions (Research-Validated):**
- **Calibre-Web-Automated** provides sufficient automation capabilities (✅ validated, with known stability risks accepted)
- **Hardcover.app API** remains available and stable (✅ validated, actively maintained with large user base)
- **Open-source tools** (KOReader, Syncthing, Calibre) continue active development (✅ validated, all actively maintained 2024-2025)
- **Free-tier cloud services** (Neon.tech, Koofr) remain viable long-term (✅ validated, established providers with sustainable business models)
- **Tailscale** mesh VPN remains free for personal use (✅ validated, current free tier adequate)
- **BookPlayer** continues Hardcover.app integration support (✅ validated, native feature actively maintained)

**Project Scope Assumptions:**
- MVP can be completed as solo developer in reasonable timeframe (3-6 months part-time)
- Technical research will identify viable solutions for all critical design decisions
- Integration between components is achievable without custom code for everything
- Documentation and community resources exist for chosen technologies

**Risk Mitigation Assumptions:**
- Multiple backup strategies prevent catastrophic data loss
- Modular architecture allows component replacement if tools fail
- Export capabilities ensure data portability if migration needed
- Community support available for troubleshooting complex issues

---

## Risks and Open Questions

### Key Risks

**High Impact / High Probability:**
1. **Data Corruption During Migration**
   - **Risk:** Historical data migration corrupts KOReader statistics.sqlite3, causing data loss or app malfunction
   - **Impact:** Loss of 2+ years of existing reading statistics; KOReader becomes unusable
   - **Mitigation:** Comprehensive backups before migration, validation testing on copy of database, rollback capability

2. **Incompatible Data Formats**
   - **Risk:** Kindle/Audible exports lack necessary data fields for meaningful KOReader reconstruction
   - **Impact:** Historical data migration provides incomplete or inaccurate reading timeline
   - **Mitigation:** Early data format inspection, fallback to "best effort" migration, clear documentation of limitations

**High Impact / Medium Probability:**
3. **Backup Solution Unreliability**
   - **Risk:** Chosen backup strategy (KOReader cloud sync or alternative) fails silently or corrupts data
   - **Impact:** False confidence in backups leading to catastrophic data loss
   - **Mitigation:** Multiple independent backup strategies, regular restore testing, integrity validation

4. **Library Server Complexity**
   - **Risk:** Calibre-Web-Automated or alternative proves too complex to configure or maintain
   - **Impact:** Automation goals unmet; continue manual library management overhead
   - **Mitigation:** Proof-of-concept testing before commitment, fallback to simpler alternatives, community support research

**Medium Impact / Medium Probability:**
5. **Audiobook Integration Gaps**
   - **Risk:** No audiobook solution provides reliable Hardcover sync AND statistics export
   - **Impact:** Audiobook data remains fragmented; unified database incomplete
   - **Mitigation:** Accept partial integration for MVP; prioritize ebook statistics; iterate in Phase 2

6. **Remote Access Security Vulnerabilities**
   - **Risk:** Improper configuration exposes library or personal data to internet threats
   - **Impact:** Privacy breach, unauthorized access to reading data and library
   - **Mitigation:** Use established secure solutions (Tailscale, Cloudflare Tunnel), follow security best practices, regular audits

**Low Impact / Medium Probability:**
7. **Free Tier Service Limitations**
   - **Risk:** Free-tier cloud services (Supabase, storage) hit usage limits or change terms
   - **Impact:** Need to find alternative services or reduce functionality
   - **Mitigation:** Design for portability, monitor usage, have migration plan for data

8. **Cross-Device Sync Conflicts**
   - **Risk:** Simultaneous reading on multiple devices causes data conflicts or loss
   - **Impact:** Incomplete statistics, lost progress tracking
   - **Mitigation:** Implement conflict resolution strategy, user education on sync timing, last-write-wins acceptable

### Research-Validated Decisions (Formerly Open Questions)

**All critical technical questions have been answered through comprehensive research analysis (see Appendix A):**

1. **✅ KOReader Statistics Backup Strategy:**
   - **Decision:** Syncthing "Send Only" from device to server (one-way disaster recovery backup)
   - **Progress Sync:** CWA KOSync server (application-aware, NOT file-level sync)
   - **Rationale:** Separation of concerns prevents SQLite corruption (unanimously warned in all research)
   - **Failure Recovery:** Backup is versioned, device is source of truth, restore from server if device fails

2. **⏸️ Kindle/Audible Data Migration (Deferred to Development):**
   - **Status:** Data exports exist in `resources/` folder
   - **Plan:** Will be analyzed during Epic 1 (Historical Data Migration)
   - **Risk Mitigation:** Migration is non-destructive, test on backup database first

3. **✅ Calibre-Web-Automated Decision:**
   - **Decision:** Selected for MVP (ebook-only configuration)
   - **Strengths:** Built-in KOSync, OPDS, Hardcover metadata, auto-ingest
   - **Accepted Risks:** Ingest stability warnings (have Calibre CLI fallback plan)
   - **Audiobook Support:** Not required (BookPlayer handles audiobooks separately)

4. **✅ Audiobook Solution:**
   - **Decision:** BookPlayer (native Hardcover sync, manual file management)
   - **Rationale:** Defers Audiobookshelf/shelfbridge complexity to future RPi 5 upgrade
   - **Trade-off:** Manual file management acceptable for MVP simplicity

5. **✅ Database Architecture:**
   - **KOReader SQLite:** Remains on device (source of truth for ebook stats)
   - **Neon.tech PostgreSQL:** Analytics data warehouse (ebook-focused for MVP)
   - **Hardcover.app:** Unified reading timeline (ebooks + audiobooks progress via plugins)
   - **Schema:** Simple star schema (books dimension, reading sessions facts)
   - **Sync Strategy:** Nightly ETL from backup statistics.sqlite3 → Neon.tech

**Remaining User Experience Decisions (Deferred to Implementation):**
- Acceptable sync latency targets (will establish during performance testing)
- Metadata conflict handling procedures (manual override via CWA web UI available)
- Analytics visualization requirements (Phase 2 - MVP uses direct SQL queries)

### Completed Research & Remaining Validation Work

**✅ COMPLETED: Comprehensive Technical Research (October 2025)**

**Research Documents Created:**
1. `resources/research/Comprehensive Technical Research_ Integrated Ope.md` (192+ sources)
2. `resources/research/Open-Source Reading Infrastructure Research-2.txt` (105+ sources)
3. `resources/research/Open-Source Reading Infrastructure Research.txt` (83+ sources)
4. `docs/research-critical-analysis.md` (Consolidated findings + conflict resolution)

**Research Coverage (All 7 Critical Areas):**
1. ✅ **KOReader Statistics Backup** - Syncthing one-way + KOSync progress sync (validated)
2. ✅ **Library Server** - CWA selected, stability risks documented, fallback planned
3. ✅ **Database Platform** - Neon.tech validated superior to Supabase/Fly.io for constraints
4. ✅ **Remote Access** - Tailscale unanimous recommendation (vs Cloudflare Tunnel)
5. ✅ **Audiobook Solution** - BookPlayer selected, deferred Audiobookshelf to RPi 5 upgrade
6. ✅ **File Sync** - Hybrid approach: Syncthing (Boox), OPDS (iOS), iOS file sync rejected
7. ✅ **Integration Architecture** - Complete data flow validated, corruption risks mitigated

**Key Findings Integrated into Brief:**
- SQLite corruption prevention (mandatory one-way backups, application-aware progress sync)
- RPi 4 2GB resource validation (ebook-only CWA stack confirmed sufficient)
- iOS file sync rejection (OPDS protocol superior, unanimous research consensus)
- Neon.tech validation (better than research recommendations for specific constraints)
- Hardcover integration completeness (plugin + BookPlayer = full coverage, no gaps)

**⏸️ DEFERRED TO IMPLEMENTATION:**

**Kindle/Audible Data Migration Analysis:**
- **Status:** Data exports exist in `resources/` folder
- **Plan:** Will analyze during Epic 1 implementation
- **Scope:** Field mapping, data quality assessment, migration script prototyping
- **Risk:** Low - migration is non-destructive, test on backup database first

**Hands-On Performance Validation:**
- CWA deployment on actual RPi 4 2GB hardware
- Library scan performance benchmarking
- Memory usage monitoring during typical workloads
- Network latency measurement for Tailscale remote access

**Failure Recovery Runbook:**
- Documented disaster recovery procedures
- Backup restoration testing
- SQLite corruption detection and recovery
- Component replacement procedures

---

## Appendices

### A. Research Summary & Documentation

**✅ COMPREHENSIVE RESEARCH COMPLETED (October 2025)**

**Research Documents (380+ Total Sources Analyzed):**

1. **`resources/research/Comprehensive Technical Research_ Integrated Ope.md`**
   - **Scope:** Exhaustive 9-area analysis with 192+ cited sources
   - **Approach:** Hybrid CWA + Audiobookshelf architecture recommendation
   - **Key Contributions:** Complete system integration validation, real-world deployment examples
   - **Date:** October 24, 2025

2. **`resources/research/Open-Source Reading Infrastructure Research-2.txt`**
   - **Scope:** Detailed technical evaluation with 105+ cited sources
   - **Approach:** Hybrid server architecture (CWA + ABS dual-stack)
   - **Key Contributions:** Implementation roadmap, Docker configurations, resource usage estimates
   - **Date:** October 24, 2025

3. **`resources/research/Open-Source Reading Infrastructure Research.txt`**
   - **Scope:** Alternative unified architecture with 83+ cited sources
   - **Approach:** Audiobookshelf-only unified server + Calibre CLI preprocessing
   - **Key Contributions:** Stability-focused analysis, iOS sync rejection rationale
   - **Date:** October 24, 2025

4. **`docs/research-critical-analysis.md`**
   - **Scope:** Consolidation of all 3 research documents with conflict resolution
   - **Purpose:** Decision framework, trade-off analysis, risk assessment
   - **Key Contributions:** Validated user decisions (Neon.tech, RPi 4 2GB), identified feature gaps
   - **Date:** October 26, 2025

**Research Methodology:**
- Multi-source validation (official docs, GitHub issues, community forums, real user deployments)
- Version compatibility tracking (2024-2025 stable releases)
- Real-world implementation evidence prioritized over theoretical capabilities
- Critical evaluation of stability risks (former contributor warnings, documented failure modes)

**Key Research Findings Integrated:**

**Unanimous Consensus (All 3 Documents):**
- ⚠️ **SQLite file-level sync = catastrophic corruption risk** (mandatory one-way backups only)
- ✅ **Tailscale > Cloudflare Tunnel** for personal use (architecture, iOS client, ToS compliance)
- ❌ **iOS background file sync fundamentally broken** (OPDS protocol required)
- ✅ **Syncthing "Send Only" / "Receive Only"** = corruption-safe configuration pattern

**Conflicting Recommendations (Resolved via Decision Framework):**
- **Library Server:** Hybrid CWA+ABS vs Unified ABS → **Decision: CWA-only (ebook-focused MVP)**
- **Database:** Fly.io vs Supabase vs Self-hosted → **Decision: Neon.tech (user-specified, validated superior)**
- **Progress Sync:** KOSync vs Readest Plugin → **Decision: CWA KOSync (self-hosted preference)**

**Research Gaps Acknowledged:**
- No RPi 4 2GB hardware testing (resource estimates theoretical, validated via typical usage patterns)
- Kindle/Audible data format analysis deferred (data exists but not analyzed until Epic 1)
- CWA ingest stability monitoring required (documented risks, fallback plan established)

**Historical Data Available:**
- **Audible:** `resources/Audible/` (complete export, awaiting Epic 1 analysis)
- **Kindle:** TBD (requested, will be placed in `resources/` when received)
- **Reference Data:** `resources/outdated-for_reference_only/` (schema reference only, DO NOT use for migration)

**Next Research Activities (Implementation Phase):**
- Hands-on CWA deployment and performance validation
- Kindle/Audible migration script prototyping
- Disaster recovery testing and runbook creation
- Neon.tech ETL pipeline development and testing

### B. Stakeholder Input

**Primary Stakeholder:** Alex (Product Owner / End User)

**Key Requirements Gathered:**
- Must preserve 2+ years of Kindle/Audible reading history
- Zero tolerance for data loss of KOReader statistics
- Strong preference for privacy, self-hosting, open-source solutions
- Constraint: $0 budget for tools and infrastructure
- Non-negotiable hardware: iOS + Boox Palma 2 + KOReader
- Value proposition: Automation to eliminate 15-30 min/book manual overhead
- Future vision: Advanced analytics and AI-powered reading insights

**Stakeholder Concerns:**
- Risk of corrupting KOReader database during historical migration
- Reliability of backup solutions for reading statistics
- Complexity of self-hosted infrastructure maintenance
- Time investment vs. value delivered

**Decision Authority:**
- All technical decisions made by Alex (solo developer project)
- Flexibility to adjust scope based on research findings
- Willingness to defer features to Phase 2 if complexity exceeds value

### C. References

**Tools & Platforms:**
- KOReader: https://github.com/koreader/koreader
- Hardcover.app: https://hardcover.app / API: https://api.hardcover.app
- Calibre-Web-Automated: https://github.com/crocodilestick/Calibre-Web-Automated
- Syncthing: https://syncthing.net
- Supabase: https://supabase.com
- audiobookshelf: https://www.audiobookshelf.org
- BookPlayer: https://github.com/TortugaPower/BookPlayer
- Readest: iOS App Store

**Technical Documentation:**
- KOReader Statistics Schema: Documented in architecture_research.md
- Hardcover GraphQL API: https://docs.hardcover.app (if available)
- OPDS Specification: https://opds.io
- Calibre CLI Documentation: https://manual.calibre-ebook.com/generated/en/cli-index.html

**Community Resources:**
- KOReader Forums: https://github.com/koreader/koreader/discussions
- Calibre Forums: https://www.mobileread.com/forums/forumdisplay.php?f=166
- Hardcover Community: Discord/Forums (TBD)
- Self-Hosted Community: r/selfhosted, r/homelab

**Relevant Standards:**
- SQLite: https://www.sqlite.org/docs.html
- OPDS (Open Publication Distribution System)
- EPUB 3 Specification
- Metadata standards: ONIX, Dublin Core

**Research Methodologies:**
- Proof-of-concept testing for technology evaluation
- Schema analysis of data exports
- Community forum research for real-world reliability insights
- Comparative matrix for solution selection

---

_This Product Brief serves as the foundational input for Product Requirements Document (PRD) creation._

_Next Steps: Handoff to Product Manager for PRD development using the `workflow prd` command._
