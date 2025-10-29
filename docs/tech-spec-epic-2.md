# Technical Specification: Device Sync & Remote Access

**Date:** 2025-10-29
**Author:** Alex
**Epic ID:** 2
**Status:** Draft

---

## Overview

Epic 2 extends the foundational BookHelper infrastructure (Epic 1) by enabling seamless cross-device reading and remote access. Users can sync their ebook library to a Boox Palma 2 e-reader, browse and download books on iOS via the Readest app using OPDS catalog access, access their library from anywhere using Tailscale mesh VPN, and synchronize reading progress across devices using KOSync. This epic unlocks the full daily workflow value by allowing the user to read on any device with automatic progress sync.

---

## Objectives and Scope

### In Scope

- **Syncthing Sync:** One-way library synchronization from RPi to Boox Palma 2 (Story 2.1 - Already Done)
- **OPDS Catalog:** Enable OPDS catalog in CWA for iOS Readest access with metadata and cover art (Story 2.2)
- **Remote Access:** Configure Tailscale mesh VPN for off-network library access from iOS and Boox (Story 2.3)
- **Progress Sync:** Configure KOSync server in CWA for cross-device reading progress synchronization (Story 2.4 - Consolidated)

### Out of Scope

- Android-specific optimizations (beyond Boox Palma 2)
- Web UI remote access hardening (basic Tailscale security model assumed)
- Advanced authentication (OAuth, SAML) - basic auth or API key sufficient
- Book recommendations based on progress
- Historical data analytics (Epic 3)

---

## System Architecture Alignment

This epic implements the **Device Synchronization Layer** and **Remote Access Layer** from the approved BookHelper architecture:

- **Cross-Device Sync:** Syncthing handles file distribution (one-way from RPi to Boox); KOSync handles progress metadata sync
- **Remote Access:** Tailscale provides secure mesh VPN without exposing RPi to public internet
- **Standards Compliance:** OPDS 1.2 catalog standard ensures compatibility with multiple iOS readers (Readest, Kindle, etc.)
- **Resource Constraints:** KOSync runs embedded in CWA; no additional services required on RPi
- **Data Safety:** Syncthing one-way mode prevents accidental deletion propagation; progress data encrypted in transit via Tailscale

---

## Detailed Design

### Services and Modules

| Service | Responsibility | Technology | Integration |
|---------|-----------------|------------|-------------|
| **Syncthing** | One-way library file sync (RPi → Boox) | Syncthing daemon | File-level synchronization |
| **OPDS Server** | Library catalog for iOS clients | CWA built-in OPDS module | HTTP API at `/opds` endpoint |
| **Readest App** | iOS ebook reader | Third-party iOS app | OPDS catalog client |
| **KOSync Server** | Cross-device reading progress sync | CWA built-in KOSync module | Embedded in CWA container |
| **Tailscale VPN** | Secure mesh network for remote access | Tailscale daemon | WireGuard-based VPN |

### Story 2.2: OPDS Catalog Configuration

**Goal:** Enable iOS users to browse and download books from the library using the Readest app without manual file management.

**Technical Approach:**

1. **Enable OPDS in CWA:**
   - OPDS catalog endpoint: `http://raspberrypi.local:8083/opds`
   - Uses existing Calibre library metadata (title, author, cover art, etc.)
   - No configuration required - built into CWA by default in v3.1.0+

2. **iOS Configuration (Readest):**
   - Install Readest app from App Store
   - Add OPDS catalog: URL = `http://raspberrypi.local:8083/opds`
   - Authentication: Basic auth if CWA web UI requires login; API key alternative if available
   - Test: Browse library categories, view cover art, download book

3. **Testing:**
   - Browse library catalog in Readest (should display 20+ books with metadata)
   - Download a test book from Readest
   - Open book in Readest and verify readable (EPUB support)
   - Verify cover art displays correctly
   - Verify author/title metadata matches CWA library

**Acceptance Criteria:**
- AC1: CWA OPDS endpoint responds at `http://raspberrypi.local:8083/opds`
- AC2: Readest can add and browse the OPDS catalog
- AC3: Book metadata (title, author, cover art) displays in Readest
- AC4: Book download from OPDS catalog works without errors
- AC5: Downloaded book opens and reads correctly in Readest
- AC6: OPDS catalog remains functional after CWA restart
- AC7: Authentication configured if CWA requires login

**Implementation Notes:**
- OPDS is lightweight and built into CWA - no additional configuration beyond enabling in admin panel if needed
- Readest handles all OPDS client logic - BookHelper side is passive
- No new database tables or schema changes required
- Works alongside existing Syncthing sync (complementary, not conflicting)

**Dependencies:**
- Story 1.1 complete (CWA operational with library content)
- Story 2.1 complete (Syncthing sync working - optional but recommended context)

---

## Story Sequencing

**Epic 2 Story Order:**

1. ✅ **Story 2.1** - Syncthing sync (DONE)
2. 📋 **Story 2.2** - OPDS catalog (READY FOR DRAFTING)
3. ⏳ **Story 2.3** - Tailscale remote access (depends on 2.2)
4. ⏳ **Story 2.4** - KOSync progress sync (depends on 2.3, can be parallel)

**Rationale:**
- Story 2.2 is independent and can proceed immediately after 2.1
- Story 2.3 builds on 2.2 (enables remote OPDS access via Tailscale IP)
- Story 2.4 can run in parallel with 2.3 or after, as KOSync is independent of Tailscale

---

## Performance & Resource Targets

| Metric | Target | Notes |
|--------|--------|-------|
| OPDS Catalog Response Time | <2 seconds | CWA built-in, no additional load |
| Syncthing Sync Latency | <5 minutes | File system notification-based |
| KOSync Sync Latency | <10 seconds | Progress metadata only, small payload |
| Tailscale Connection Time | <5 seconds | Mesh network, local LAN optimal |
| Memory Impact (Epic 2 services) | <50MB additional | KOSync + Tailscale lightweight |

---

## Known Risks & Mitigations

| Risk | Severity | Mitigation |
|------|----------|-----------|
| OPDS endpoint not enabled in CWA | Medium | Document admin panel steps; verify in test |
| Readest authentication failure | Medium | Document basic auth setup; test before deploy |
| Syncthing conflicts if Boox modifies files | Low | Configure "Receive Only" mode on Boox (one-way) |
| Tailscale requires user account setup | Low | Document Tailscale auth flow; test on all devices |
| KOSync server conflicts with reading app | Low | Use KOSync embedded in CWA (avoid duplicate servers) |

---

## Rollout Plan

1. **Story 2.2 Development:** 2-3 days
   - Enable OPDS in CWA admin panel
   - Install Readest on iOS device
   - Test catalog browsing and book download
   - Document setup steps

2. **Story 2.3 Development:** 2-3 days
   - Install Tailscale on RPi and iOS
   - Configure mesh network
   - Test remote OPDS access via Tailscale IP

3. **Story 2.4 Development:** 2-3 days
   - Enable KOSync in CWA admin panel
   - Configure KOReader on Boox with KOSync server
   - Configure Readest on iOS with KOSync
   - Test progress sync between devices

**Total Epic 2 Estimate:** 1.5-2 weeks (assumes parallel development of 2.3/2.4)

---

## References

- **OPDS Standard:** [Open Publication Distribution System 1.2 Spec](https://specs.opds.io/opds-1.2)
- **Readest App:** [Readest - iOS Ebook Reader](https://apps.apple.com/us/app/readest/id1573929596)
- **Tailscale:** [Tailscale Docs](https://tailscale.com/kb/)
- **KOSync:** [KOSync Plugin for KOReader](https://github.com/koreader/KOReader/wiki/KOSync)
- **CWA OPDS:** [Calibre-Web-Automated OPDS Support](https://github.com/crocodilestick/calibre-web-automated)

---

**Status:** Ready for Epic 2 story drafting (Story 2.2 first)
