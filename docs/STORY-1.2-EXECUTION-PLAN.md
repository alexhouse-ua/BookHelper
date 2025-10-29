# Story 1.2: 1-Week Validation Execution Plan
## Tasks 2-5: Realistic Ingestion Validation & Performance Documentation

**Status:** Ready for manual execution on Raspberry Pi 4
**Generated:** 2025-10-27
**Task 1 Status:** ✅ Complete (Configuration validated with 31-test suite)

---

## Overview

This document provides step-by-step instructions for executing Tasks 2-5, which require **real-time monitoring over 1 week** on the Raspberry Pi 4 hardware. This validation confirms that Story 1.2 meets all 14 acceptance criteria under realistic usage patterns.

**Key Points:**
- Task 1 (Configuration) is complete and verified ✓
- Tasks 2-5 require actual 1-week observation with real hardware
- No simulation or acceleration is possible for this workload
- You will monitor incrementally during normal reading habits (1-2 books/week)

---

## Task 2: Execute 1-Week Realistic Ingestion Validation (AC 8-12)

### Prerequisites
- [ ] Story 1.2 Task 1 is complete (CWA configured)
- [ ] Raspberry Pi 4 with CWA running (docker-compose up)
- [ ] Monitoring script installed: `/resources/scripts/monitor-resources-1.2.py`
- [ ] SSH or direct terminal access to RPi
- [ ] 7 consecutive days available for observation

### Execution Steps

#### Step 2.1: Start Monitoring Script (Day 1)
```bash
# SSH into RPi or use terminal on RPi itself
ssh alexhouse@raspberrypi.local

# Navigate to project root
cd /path/to/BookHelper

# Start monitoring (runs continuously, collecting data every 5 minutes)
python3 resources/scripts/monitor-resources-1.2.py

# Expected output:
# Starting CWA monitoring: calibre-web-automated
# Output: /tmp/cwa-metrics-1.2.csv
# Interval: 300s
# Press Ctrl+C to stop
#
# 2025-10-27T10:00:00+00:00 | idle           |   245.3 MB |  5.2% CPU
# 2025-10-27T10:05:00+00:00 | idle           |   247.1 MB |  3.8% CPU
# ...
```

**Note:** Keep this script running continuously in a tmux/screen session:
```bash
# Option 1: Use tmux (recommended)
tmux new-session -d -s monitoring "python3 resources/scripts/monitor-resources-1.2.py"

# Option 2: Use screen
screen -dmS monitoring python3 resources/scripts/monitor-resources-1.2.py

# Later, reattach to see output:
tmux attach-session -t monitoring    # For tmux
screen -r monitoring                  # For screen
```

#### Step 2.2: Simulate Realistic Weekly Usage (Days 1-7)

**Usage Pattern:**
- Drop **1-2 test ebook files** into `/library/ingest/` once per day or every 2 days
- This simulates typical reading acquisition (1-2 books picked up during the week)
- **Do NOT** do bulk testing or stress testing
- Use real ebook files from your collection (EPUB, PDF, etc.)

**For Each Drop:**

```bash
# SSH into RPi or use file transfer
scp ~/Downloads/test-book.epub alexhouse@raspberrypi.local:/library/ingest/

# Verify in CWA web UI: http://raspberrypi.local:8083/
# You should see:
# 1. New book appears in library (auto-detected within 30s)
# 2. Metadata is enriched (title, author, cover, etc.)
# 3. Book is readable in web UI
```

**When to Add Books (Example Schedule):**
- Day 1: 1 test book (Mon)
- Day 3: 1 test book (Wed)
- Day 5: 1 test book (Fri)
- Day 7: Optional 1 test book (Sun)

**Total: 3-4 books across the week** (realistic pattern)

#### Step 2.3: Baseline Metrics Collection (Day 1, Evening)

Before adding any books, capture baseline idle metrics:

```bash
# On RPi, in CWA web UI: http://raspberrypi.local:8083/
# 1. Let CWA idle for 10 minutes with no activity
# 2. Check Docker container memory usage:

docker stats --no-stream calibre-web-automated

# Expected output:
# CONTAINER ID    NAME                    CPU %     MEM USAGE / LIMIT
# abc123...       calibre-web-automated   2.5%      245.3 MiB / 1.465 GiB

# Note this baseline value (~200-300 MB is expected)
```

#### Step 2.4: Daily Observations (Days 1-7)

**Each day, record in a manual log or notes:**
- What time you added a book (if applicable)
- Observed memory usage during import
- Any lag or delays in the web UI
- Any error messages or warnings in CWA logs
- Overall stability impression

**Check logs daily:**
```bash
# View recent CWA logs for errors
docker logs calibre-web-automated --tail 50

# Look for keywords:
# - "error" or "ERROR"
# - "import" or "ingest"
# - "metadata"
# - "crash" or "killed"
```

#### Step 2.5: Check for OOM Killer (Critical Daily Check)

**Run once per day** to check if the system has run out of memory:

```bash
# Check kernel logs for OOM killer signals
dmesg | grep -i "oom\|out of memory" | tail -5

# If you see output like:
# [xxxxx.xxxxxx] Out of memory: Kill process 1234 ...
# This indicates memory pressure (AC9 may fail)

# Also check system memory:
free -h
# If 'available' drops below 200MB, memory is constrained
```

#### Step 2.6: Trigger Library Scan & Performance Check (Mid-week, e.g., Day 4)

After adding 2 books, trigger a library scan to test AC11:

```bash
# In CWA web UI: http://raspberrypi.local:8083/
# 1. Navigate to: [Admin] → [Library Management] → [Scan Library]
# 2. Click "Start Scan"
# 3. Monitor:
#    - Time it takes to complete
#    - Memory usage peaks
#    - CPU usage
#    - Any errors in logs

# Expected: <2 minutes for ~50 books, <1GB memory peak
```

---

## Task 3: Validate Realistic Performance Targets (AC 9-11)

### Data Collection (Continuous During Days 1-7)

The monitoring script automatically captures:
- **Timestamp** (ISO 8601 format)
- **Operation type** (idle, import, metadata_fetch, library_scan)
- **Memory (MB)** from docker stats
- **CPU (%)** from docker stats

**Output file:** `/tmp/cwa-metrics-1.2.csv`

### Analysis (Day 8 Morning)

```bash
# Copy metrics to local machine for analysis
scp alexhouse@raspberrypi.local:/tmp/cwa-metrics-1.2.csv ./cwa-metrics-1.2.csv

# Analyze with Python or spreadsheet:
python3 <<'EOF'
import pandas as pd

# Load metrics
df = pd.read_csv('cwa-metrics-1.2.csv')

# Convert memory to numeric
df['memory_mb'] = pd.to_numeric(df['memory_mb'])

# AC9: Idle memory <600MB
idle_mem = df[df['operation'] == 'idle']['memory_mb']
print(f"AC9 - Idle Memory:")
print(f"  Max: {idle_mem.max():.1f} MB (target: <600 MB)")
print(f"  Avg: {idle_mem.mean():.1f} MB")
print(f"  Pass: {idle_mem.max() < 600}")

# AC9: Metadata fetch <1GB
metadata_mem = df[df['operation'] == 'metadata_fetch']['memory_mb']
print(f"\nAC9 - Metadata Fetch Peak Memory:")
print(f"  Max: {metadata_mem.max():.1f} MB (target: <1000 MB)")
print(f"  Pass: {metadata_mem.max() < 1000}")

# AC10: Metadata enrichment <30s (manual observation from logs)
print(f"\nAC10 - Metadata Enrichment Speed:")
print(f"  Review import logs and CWA web UI timestamps")
print(f"  Target: <30 seconds per book")

# AC11: Library scan <2 minutes (from manual observation)
print(f"\nAC11 - Library Scan Time:")
print(f"  Manual observation: Check CWA logs during library scan")
print(f"  Target: <2 minutes for ~50 books")

# Overall stats
print(f"\n=== Overall Statistics ===")
print(f"Total metrics collected: {len(df)}")
print(f"Monitoring duration: {df['timestamp'].iloc[-1]} to {df['timestamp'].iloc[0]}")
print(f"Memory range: {df['memory_mb'].min():.1f} - {df['memory_mb'].max():.1f} MB")
print(f"CPU range: {df['cpu_percent'].min():.1f}% - {df['cpu_percent'].max():.1f}%")
EOF
```

### Validation Checklist

- [ ] AC9 (Idle <600MB): Pass/Fail ___________
- [ ] AC9 (Metadata <1GB): Pass/Fail ___________
- [ ] AC10 (Metadata enrichment <30s): Pass/Fail ___________
  - Source: CWA logs timestamps
  - Example: "import started 10:00:15, completed 10:00:42" = 27 seconds ✓
- [ ] AC11 (Library scan <2 minutes): Pass/Fail ___________
  - Measured manually during Day 4 scan
- [ ] AC12 (No crashes/corruption): Pass/Fail ___________
  - Check: dmesg, docker logs, data integrity

---

## Task 4: Create Performance Documentation (AC 13)

### Step 4.1: Generate Performance Report

Create comprehensive report at: `/docs/STORY-1.2-PERFORMANCE-REPORT.md`

**Template:**

```markdown
# Story 1.2 Performance Report
## Auto-Ingestion + Metadata Enrichment Validation Results

**Date Generated:** 2025-11-XX
**Monitoring Period:** 2025-10-27 to 2025-11-03 (7 days)
**Hardware:** Raspberry Pi 4, 2GB RAM
**CWA Version:** 3.1.0+

## Executive Summary

[Add 1-2 sentences on overall findings]

## Resource Usage Metrics

### Memory Usage
- Idle baseline: ___ MB (AC9: <600MB target)
- Peak during metadata fetch: ___ MB (AC9: <1GB target)
- Peak during library scan: ___ MB

### CPU Usage
- Average during idle: __%
- Peak during metadata fetch: ___%
- Peak during import: ___%

### Performance Benchmarks
- Average metadata enrichment time: ___ seconds (AC10: <30s target)
- Library scan time (50 books): ___ seconds (AC11: <2 min target)
- File import time: ___ seconds (AC4: <30s target)

### Metadata Enrichment Success
- Books processed: ___
- Fields populated (average): ___ / 9 (AC5: min 7 required)
- Hardcover API hit rate: ___%
- Google Books fallback rate: ___%

## Stability Observations

### Errors & Issues
- Crashes observed: [Yes/No] - If yes, describe
- Database corruption: [Yes/No] - If yes, describe
- OOM events: [Yes/No] - If yes, dates/times
- API timeouts: [Yes/No] - If yes, frequency
- Other issues: [List any observations]

### Logs Summary
- Total error messages: ___
- Error categories: [List any patterns]
- Notable warnings: [List]

## Acceptance Criteria Validation

| AC # | Description | Target | Actual | Pass? |
|------|-------------|--------|--------|-------|
| 1 | Auto-ingest folder monitored | Yes | Yes | ✓ |
| 2 | Hardcover primary provider | Yes | Yes | ✓ |
| 3 | Google Books fallback | Yes | Yes | ✓ |
| 4 | Import <30s | <30s | ___ s | ✓/✗ |
| 5 | Enriched metadata (7-9 fields) | Yes | ___ fields | ✓/✗ |
| 6 | EPUB optimization enabled | Yes | Yes | ✓ |
| 7 | Hardcover API validated | Yes | Yes | ✓ |
| 8 | 1-week incremental validation | 1 week | 7 days | ✓ |
| 9 | Memory constraints (<600MB idle, <1GB peak) | Yes | Idle: ___ MB, Peak: ___ MB | ✓/✗ |
| 10 | Metadata <30s per book | <30s | ___ s | ✓/✗ |
| 11 | Library scan <2 minutes | <2 min | ___ s | ✓/✗ |
| 12 | No crashes/corruption/OOM | None | [Count] | ✓/✗ |
| 13 | Documentation created | Yes | [This report] | ✓ |
| 14 | Go/no-go decision | TBD | [See below] | ✓ |

## Go/No-Go Decision (AC14)

### Decision: [CONTINUE RPi 4 / CONTINUE WITH CONSTRAINTS / ESCALATE]

**Rationale:**

[Describe decision based on AC validation results]

**If All ACs Pass:**
- Decision: CONTINUE with Raspberry Pi 4
- Rationale: All performance targets met under realistic incremental usage
- Next steps: Proceed with Epic 2 (Device Sync & Remote Access)

**If Some ACs Fail:**
- Decision: CONTINUE WITH CONSTRAINTS or ESCALATE
- Failing ACs: [List which ones]
- Impact: [e.g., if memory exceeds 1GB, other epics may be constrained]
- Mitigation: [e.g., USB swap, reduced library size, RPi 5 as future option]
- Recommendation: [Proceed with noted constraints, or escalate to RPi 5]

**If Critical ACs Fail (AC12 crashes/corruption):**
- Decision: ESCALATE
- Recommendation: RPi 4 insufficient; recommend RPi 5 upgrade or alternative storage solution

## Appendix: Raw Data

### Monitoring CSV Sample
[First 10 rows of cwa-metrics-1.2.csv]

### CWA Logs (Key Excerpts)
[Selected log lines showing imports, metadata fetches, errors]

### dmesg Output (OOM Check)
[Output of: dmesg | grep -i "oom\|out of memory"]

---

Generated by Story 1.2 Dev Workflow
```

### Step 4.2: Populate Report with Data

Fill in the blanks using:
1. **Metrics CSV:** Statistical analysis from `/tmp/cwa-metrics-1.2.csv`
2. **Docker logs:** `docker logs calibre-web-automated`
3. **Manual observations:** Notes from Days 1-7 monitoring
4. **dmesg output:** `dmesg | grep -i oom` results

---

## Task 5: Go/No-Go Decision (AC 14)

### Decision Framework

Review the 14 acceptance criteria from the performance report:

**Green Light (All ACs Pass):**
```
DECISION: ✅ CONTINUE RPi 4 DEPLOYMENT

Rationale: Raspberry Pi 4 2GB successfully demonstrates:
- Automatic ingestion: <30s per book
- Memory efficiency: Idle <600MB, peak <1GB during metadata
- Reliable operation: Zero crashes, no OOM events over 7 days
- Scalability confirmed: Handles incremental 1-2 book/week pattern

Next: Proceed to Epic 2 (Device Sync & Remote Access)
```

**Yellow Light (Some ACs Fail, Non-Critical):**
```
DECISION: ⚠️  CONTINUE WITH CONSTRAINTS

Failing ACs: [List] (e.g., AC11: Library scan takes 3+ minutes)
Impact: [Description of constraints]
Workaround: [e.g., "Reduce library to <30 books" or "Schedule scans during off-peak"]

Proceed with noted constraints. Escalate to RPi 5 if constraints become untenable.
```

**Red Light (Critical ACs Fail):**
```
DECISION: 🛑 ESCALATE TO RPi 5

Failing ACs: [Critical failures, e.g., AC12: OOM crashes, AC9: Memory consistently >1GB]
Impact: [CWA reliability compromised, cannot guarantee production stability]
Recommendation: Upgrade to Raspberry Pi 5 (8GB RAM) for Epic 2+ implementation

Cost-Benefit: RPi 5 ($60-80) << Development delay cost
```

### Decision Document

Create a final decision summary in `/docs/STORY-1.2-PERFORMANCE-REPORT.md`:

```markdown
## Final Go/No-Go Decision (AC14)

**Decision Date:** [When you complete the report]
**Reporter:** Alex
**Status:** [APPROVED / CONDITIONAL / ESCALATED]

**Decision:** [CONTINUE / CONTINUE WITH CONSTRAINTS / ESCALATE]

**Justification:**
[1-2 paragraphs explaining the decision based on AC validation results]

**Constraints (if applicable):**
- [List any constraints discovered during testing]
- [Note workarounds or mitigations]

**Impact on Future Epics:**
- Epic 2 (Device Sync): [Feasible / Requires constraint mitigation / Escalate]
- Epic 3 (ETL): [Feasible / Requires constraint mitigation / Escalate]
- Epic 5 (Migration): [Feasible / Requires constraint mitigation / Escalate]

**Approval:**
- [ ] Performance targets met (AC1-13)
- [ ] Go/no-go decision documented (AC14)
- [ ] Ready to proceed with next epic

---
```

---

## Timeline Summary

| Timeline | Action | Deliverable |
|----------|--------|-------------|
| **Day 1** | Start monitoring script, add 1 test book, record baseline metrics | Monitoring running, baseline data |
| **Days 2-7** | Daily observations, add 1-2 books (total 3-4), trigger mid-week scan | 7 days of metrics, daily logs |
| **Day 8** | Stop monitoring, analyze metrics, generate report | `/docs/STORY-1.2-PERFORMANCE-REPORT.md` |
| **Day 8-9** | Make go/no-go decision, document rationale | AC14 signed off |

---

## Key Files

- **Monitoring Script:** `/resources/scripts/monitor-resources-1.2.py`
- **Metrics Output:** `/tmp/cwa-metrics-1.2.csv` (on RPi)
- **Performance Report:** `/docs/STORY-1.2-PERFORMANCE-REPORT.md` (to create)
- **Setup Guide (Reference):** `/docs/STORY-1.2-PLUGINS-SETUP.md`
- **Story File (Update):** `/docs/stories/story-1.2.md`

---

## Troubleshooting

### Q: Monitoring script crashes after a few hours
**A:** Check if docker daemon restarted. Restart monitoring:
```bash
pkill -f monitor-resources
python3 resources/scripts/monitor-resources-1.2.py
```

### Q: Memory usage stays high (>700MB idle)
**A:** Expected if other services are running. Check:
```bash
docker stats  # See memory usage of all containers
# If syncthing is using memory, that's expected and separate from CWA
```

### Q: CWA import takes >30s
**A:** Check Hardcover API is responding:
```bash
# Check CWA logs
docker logs calibre-web-automated | grep -i "hardcover\|metadata"
# If Hardcover is slow, Google Books fallback should take over (~10-15s)
```

### Q: Library scan takes >2 minutes
**A:** For 50 books, <2 min is typical. If significantly over, check:
```bash
# Is CWA CPU constrained?
docker stats --no-stream calibre-web-automated
# Is disk I/O the bottleneck?
iostat -x 1 5
```

---

## Success Criteria

Story 1.2 is **COMPLETE** when:
1. ✅ All 14 acceptance criteria are validated (AC1-13 measured, AC14 decided)
2. ✅ Performance report generated and approved
3. ✅ Go/no-go decision documented
4. ✅ Story file updated with final status
5. ✅ Ready for story-done workflow

**Estimated Total Effort:**
- Task 1 (Configuration): ✅ Complete (2-3 hours)
- Task 2-5 (Validation): 1-2 hours setup + 7 days passive monitoring + 2 hours analysis = **~2 weeks total calendar time**

---

**Last Updated:** 2025-10-27
**Next Review:** After 1-week validation period
**Version:** 1.0
