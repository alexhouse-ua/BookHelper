# BookHelper System Architecture

**Author:** BMad Architect
**Date:** 2025-10-26
**Status:** Approved

---

## 1. System Architecture Philosophy

The BookHelper system architecture is guided by the following principles, derived from the project's core goals of data sovereignty, automation, and resilience:

- **Data Safety First:** The architecture prioritizes the prevention of data loss and corruption. This is achieved through a strict separation of live progress synchronization from disaster recovery backups, using different mechanisms for each.
- **Stability Over Features:** The system favors proven, well-maintained components over cutting-edge solutions that may lack stability. This ensures the long-term viability of the infrastructure.
- **Modular Design:** Components are designed to be independent, allowing for replacement or upgrades without requiring a full system overhaul. This modularity is key to the system's maintainability.
- **Data Ownership:** All data is stored in standard, accessible formats (SQLite, PostgreSQL, plain files), ensuring that the user retains full control and can migrate away from any component without data loss.
- **Resilience:** Multiple layers of backups (local and cloud), one-way synchronization patterns, and versioned backups are implemented to protect against various failure scenarios.
- **Privacy-First:** Core services are self-hosted, and cloud dependencies are minimized. Remote access is secured through a private mesh VPN (Tailscale), avoiding public exposure of any services.

---

## 2. Finalized System Architecture

The following diagram illustrates the final, research-validated architecture for the BookHelper system.

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

---

## 3. Key Architectural Components

### 3.1. Data Layer (Multi-Tier Strategy)

- **KOReader `statistics.sqlite3`** (on device): The source of truth for all ebook reading statistics. This file is treated as sacred and is protected by multiple layers of one-way backups.
- **Calibre-Web-Automated `metadata.db`** (on server): The Calibre library database, containing all ebook metadata and file locations.
- **Neon.tech PostgreSQL** (cloud): A cloud-hosted PostgreSQL database serving as the analytics data warehouse. For the MVP, this will house ebook statistics extracted from the `statistics.sqlite3` backup.
- **Hardcover.app** (cloud): Acts as the unified reading timeline, aggregating both ebook and audiobook progress and metadata through dedicated plugins and native app integrations.
- **Ebook files** (server and Boox device): The master library of ebook files resides on the Raspberry Pi server and is synced one-way to the Boox Palma device.
- **Audiobook files** (iOS device only): Audiobook files are managed manually on the iOS device using the BookPlayer app.

### 3.2. Sync & Backup Layer (Corruption-Safe Design)

This layer is the most critical part of the architecture, designed specifically to prevent the corruption of the `statistics.sqlite3` database.

**Progress Sync (Application-Aware, for Live Data):**
- **KOReader ↔ Readest:** Progress is synced bidirectionally between the Boox device and the iOS device using the **KOSync server** built into Calibre-Web-Automated. This is an application-aware protocol that understands database transactions and is safe for live sync.
- **KOReader → Hardcover:** The `hardcoverapp.koplugin` on KOReader updates reading progress directly to Hardcover.app via its API.
- **BookPlayer → Hardcover:** The BookPlayer app on iOS has native Hardcover.app integration to sync listening progress.

**File Sync (for Ebook Library Distribution):**
- **Server → Boox:** The ebook library is synced one-way from the Raspberry Pi server to the Boox Palma device using **Syncthing**. The Boox device is configured as "Receive Only".
- **Server → iOS:** There is **no background file sync** to iOS. The Readest app on iOS uses the **OPDS protocol** to download ebooks on-demand from the Calibre-Web-Automated server.

**Disaster Recovery Backup (One-Way, for Recovery):**
- **Statistics Backup:** The `statistics.sqlite3` file is backed up from the Boox device to the Raspberry Pi server using **Syncthing**. This is a **one-way sync**, with the Boox device configured as "Send Only". This backup is for disaster recovery only and is never synced back to the device.
- **Library Backup:** The entire ebook library and the Calibre-Web-Automated configuration files are backed up nightly from the Raspberry Pi to **Koofr** (a WebDAV-compatible cloud storage provider) using `rclone` with encryption.

### 3.3. Library Management Layer

- **Ingestion:** New ebooks are automatically ingested into the library. A user drops a file into a monitored folder, which triggers the Calibre-Web-Automated auto-ingest process.
- **Metadata:** Metadata is automatically enriched during ingestion using the **Hardcover.app provider** as the primary source, with fallbacks to Google Books and Open Library.
- **Format Optimization:** Calibre-Web-Automated provides an EPUB fixer and can leverage the Calibre conversion engine for format optimization.
- **OPDS Catalog:** Calibre-Web-Automated provides an OPDS feed, which is used by the Readest app on iOS for library browsing and on-demand downloads.

### 3.4. Access Layer

- **Local Network:** All services on the Raspberry Pi (Calibre-Web-Automated web UI, OPDS, KOSync) are directly accessible on the local network.
- **Remote Access:** **Tailscale**, a zero-config mesh VPN, is installed on all devices (server, Boox, iOS) to provide secure remote access to the services without exposing them to the public internet.
- **Web UI:** The responsive web interface of Calibre-Web-Automated is used for library browsing and metadata editing.
- **Device Clients:** KOReader on the Boox Palma 2 and Readest on iOS are the primary client applications.

### 3.5. Analytics Layer (MVP)

- **ETL Pipeline:** A nightly Python script will run on the Raspberry Pi. It will read the `statistics.sqlite3` backup, transform the data, and load it into the **Neon.tech PostgreSQL** database.
- **Data Warehouse:** The Neon.tech database will store structured data on reading sessions, pages read, reading velocity, etc.
- **Query Access:** In the MVP, analytics will be performed by writing direct SQL queries against the Neon.tech database using a standard PostgreSQL client (like DBeaver or pgAdmin).

---

## 4. Critical Warnings & Risk Mitigation

### CRITICAL WARNING: SQLite Corruption Risk

The research for this project unanimously identified that **file-level synchronization of a live SQLite database is the number one cause of catastrophic and irreversible data loss.** This architecture is designed with non-negotiable safeguards to prevent this.

- **The Problem:** File-level sync tools (like Syncthing or Dropbox) can copy a database file while it is in the middle of a write transaction, resulting in a "torn write" and a corrupted file.
- **The Consequence:** A corrupted `statistics.sqlite3` file means the loss of all reading history.

**Mandatory Safeguards:**

1.  **Progress Sync MUST use application-aware protocols.** We use the KOSync server for this. **NEVER** use Syncthing or any other file-level sync tool for progress synchronization.
2.  **Statistics Backup MUST be one-way.** Syncthing is configured as "Send Only" from the Boox device to the server. The server **NEVER** writes this file back to the device. This is for disaster recovery only.
3.  **Separation of concerns is MANDATORY.** Live progress sync (KOSync) and disaster recovery backup (Syncthing one-way) are completely separate processes and must never be mixed.

### Known Risk: Calibre-Web-Automated Ingest Stability

- **The Risk:** A former contributor has noted that the auto-ingest feature is a "hack" and may be unstable.
- **Mitigation:**
    - CWA logs will be monitored for ingest errors.
    - The Calibre CLI will be installed on the server as a fallback for manual ingestion if needed.
    - The `metadata.db` file will be backed up before any large bulk imports.
- **Acceptance:** The feature benefits of CWA (KOSync, auto-ingest, Hardcover metadata) are deemed to outweigh the stability risk for the MVP.

### Resource Constraint: Raspberry Pi 4 2GB

- **The Risk:** The 2GB of RAM on the Raspberry Pi 4 could be a bottleneck during large library scans or other intensive operations.
- **Validation:** Research indicates that the memory is sufficient for an ebook-only CWA stack.
- **Mitigation:**
    - System resource usage will be monitored.
    - If memory pressure becomes an issue, a USB swap file can be added.
    - A hardware upgrade to a Raspberry Pi 5 with more RAM is the long-term solution, especially if Audiobookshelf is added in the future.
