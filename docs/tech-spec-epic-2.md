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

## Data Models & Schemas

### Entities

**Book (inherited from Calibre)**
- source: Calibre metadata.db
- Fields: title (string), author (string), series (string), cover_art (image), formats (array), language (string), pub_date (date)
- Relationships: 1 Book → N Formats (EPUB, MOBI, KEPUB, etc.)

**ReadingProgress (KOSync)**
- source: KOSync server
- Fields: book_id (UUID), device_id (UUID), progress_percent (0-100), timestamp (datetime), reading_position (object)
- Relationships: N ReadingProgress → 1 Book; N ReadingProgress → 1 Device
- Storage: KOSync metadata table in CWA database

**Device**
- source: KOSync registration + Tailscale peer list
- Fields: device_id (UUID), device_name (string), device_type (enum: ios, android, ereader), tailscale_ip (string), last_sync (datetime)
- Relationships: N Devices → N Books (via ReadingProgress)

---

## API Specification

### OPDS Catalog Endpoints

**GET /opds**
- Description: Root OPDS 1.2 catalog feed (XML)
- Response Format: OPDS 1.2 Atom XML
- Authentication: None (if CWA login disabled) OR Basic Auth (if enabled)
- Status Codes:
  - 200: Valid OPDS feed returned
  - 401: Unauthorized (if auth required and credentials invalid)
  - 500: Server error
- Response Body Example:
  ```xml
  <?xml version="1.0" encoding="utf-8"?>
  <feed xmlns="http://www.w3.org/2005/Atom" xmlns:opds="http://opds-spec.org/2010/catalog">
    <title>BookHelper Library</title>
    <id>urn:uuid:bookhelper-root</id>
    <updated>2025-10-29T12:00:00Z</updated>
    <link rel="start" href="/opds" type="application/atom+xml;profile=opds-catalog;kind=navigation" />
    <entry>
      <title>Fiction</title>
      <link rel="subsection" href="/opds/categories/fiction" type="application/atom+xml;profile=opds-catalog;kind=navigation" />
    </entry>
  </feed>
  ```

**GET /opds/categories/{category}**
- Description: Browse books in a specific category
- Parameters: category (string: fiction, nonfiction, science, etc.)
- Authentication: Same as /opds
- Status Codes: 200, 401, 404, 500
- Response: OPDS Atom feed with book entries and cover art links

**GET /opds/books/{book_id}**
- Description: Retrieve specific book metadata and download link
- Parameters: book_id (integer or UUID)
- Authentication: Same as /opds
- Response: OPDS Atom entry with title, author, cover, formats, download links
- Download Link: `/opds/books/{book_id}/download/{format}` (e.g., `/opds/books/42/download/epub`)

### KOSync Server Endpoints

**POST /api/kosync/registerdevice**
- Description: Register a new device for progress sync
- Request Body:
  ```json
  {
    "device_id": "uuid",
    "device_name": "iPhone 14 Pro",
    "device_type": "ios"
  }
  ```
- Response (201 Created):
  ```json
  {
    "device_id": "uuid",
    "server_id": "kosync-server-uuid",
    "registered_at": "2025-10-29T12:00:00Z"
  }
  ```
- Status Codes: 201, 400 (bad request), 500

**POST /api/kosync/bookmark**
- Description: Sync reading progress for a book
- Request Body:
  ```json
  {
    "device_id": "uuid",
    "book_id": "uuid",
    "progress_percent": 45,
    "bookmark_data": { "page": 120, "chapter": "5" },
    "timestamp": "2025-10-29T14:30:00Z"
  }
  ```
- Response (200 OK):
  ```json
  {
    "synced": true,
    "server_timestamp": "2025-10-29T14:30:01Z",
    "conflict": false
  }
  ```
- Status Codes: 200, 400, 409 (conflict), 500

**GET /api/kosync/bookmark/{device_id}/{book_id}**
- Description: Retrieve latest reading progress for a book on a device
- Response (200 OK):
  ```json
  {
    "device_id": "uuid",
    "book_id": "uuid",
    "progress_percent": 45,
    "bookmark_data": { "page": 120, "chapter": "5" },
    "timestamp": "2025-10-29T14:30:00Z"
  }
  ```
- Status Codes: 200, 404 (no progress yet), 500

### Tailscale Integration

**VPN Configuration (not a traditional API)**
- Device Registration: Manual via Tailscale auth flow on RPi and iOS
- Access Method: All services (OPDS, KOSync) accessible via Tailscale IP (e.g., `100.x.x.x`)
- Authentication: WireGuard VPN layer (encrypted by default)
- Commands:
  - Enable on RPi: `tailscale up` (one-time setup)
  - Enable on iOS: Install Tailscale app, scan QR code or authenticate via web UI

---

## Non-Functional Requirements

### Security

- **OPDS Over Tailscale:** All remote OPDS traffic encrypted via WireGuard (VPN-level encryption)
- **Authentication:** Basic Auth for CWA admin panel (if enabled); supports OAuth 2.0 via CWA config
- **Device Registration:** KOSync device IDs registered server-side; devices must register before sync access
- **Token/Credential Rotation:** Basic auth credentials can be changed in CWA admin; KOSync device IDs persist until unregistered
- **Rate Limiting:** No explicit rate limiting in CWA 3.1.0; recommend 100 requests/min per IP in reverse proxy (if deployed)
- **TLS:** Not required for LAN access; if accessing over untrusted networks, configure TLS reverse proxy in front of CWA

### Reliability

- **Uptime Target:** 99% (allows ~7 hours/month downtime)
- **OPDS Availability:** Must respond within 2 seconds; if >3 seconds, log warning and investigate CWA load
- **Syncthing Sync Recovery:** Auto-resumes on network restore; no manual intervention needed
- **KOSync Conflict Resolution:** Last-write-wins; conflicting progress syncs keep server version and notify client
- **Failover Strategy:** None (single RPi deployment); for HA, consider database replication (out of scope for Epic 2)

### Observability

**Logging:**
- OPDS catalog requests: Log client IP, book accessed, response status, response time
- KOSync device registrations: Log device_id, device_name, registration time
- KOSync bookmark syncs: Log device_id, book_id, progress change, conflict status
- Log Level: INFO for normal operations; DEBUG for troubleshooting
- Log Location: `/var/log/calibre-web/app.log` (configurable in CWA)

**Metrics (Prometheus format if monitoring enabled):**
- `opds_requests_total` (counter): Total OPDS requests by endpoint
- `opds_response_time_seconds` (histogram): OPDS response latency
- `kosync_device_registrations_total` (counter): Total device registrations
- `kosync_bookmark_syncs_total` (counter): Total bookmark sync operations
- `kosync_conflicts_total` (counter): Total sync conflicts detected

**Alerting:**
- Alert if OPDS endpoint unreachable >1 minute (check via HTTP GET /opds every 30s)
- Alert if KOSync server down >5 minutes (check connectivity every 60s)
- Alert if Syncthing stalled >15 minutes (no files synced in interval)
- Alert if CWA logs show error rate >1% in rolling 5-min window

---

## Dependencies & Versions

### Required Components

| Component | Version | Rationale | Notes |
|-----------|---------|-----------|-------|
| Calibre-Web-Automated | v3.1.0+ | OPDS support, KOSync plugin | Must support OPDS 1.2 standard |
| Readest iOS App | v1.5+ | OPDS 1.2 client | Requires iOS 13+; check App Store for latest |
| iOS | 13+ | Readest minimum requirement | Supports iPhone/iPad |
| RPi OS | Bullseye (recommended) | Stable Docker support | Buster still supported but deprecated |
| Syncthing | v1.23+ | One-way mode, file watching | Critical for Story 2.1 context |
| Tailscale | v1.52+ (RPi), v1.x (iOS) | Stable mesh networking | Latest recommended; backward compatible |
| KOReader | v2024.10+ | KOSync plugin integration | Boox Palma 2 uses KOReader as default reader |
| KOSync (CWA plugin) | Built-in (v3.1.0+) | Progress sync server | No separate installation needed |
| WireGuard | v1.0.20220627+ | Tailscale VPN layer | Included with Tailscale; no manual install |

### Optional Components

| Component | Purpose | Version |
|-----------|---------|---------|
| Nginx/Caddy | Reverse proxy + TLS termination | Latest stable | For HTTPS on untrusted networks |
| Prometheus | Metrics collection (if observability enabled) | v2.x | For production monitoring |
| Loki | Log aggregation (if observability enabled) | v2.x | Lightweight log storage |

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
