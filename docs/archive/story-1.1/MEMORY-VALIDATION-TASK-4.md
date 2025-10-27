# Task 4: Validate Idle Memory Usage

**Story:** 1.1 - Deploy Calibre-Web-Automated on Raspberry Pi 4
**Task ID:** 1.1.4
**Acceptance Criteria:** AC4 - Idle memory usage validated at <600 MB for CWA container

---

## Overview

This task validates that the CWA container uses less than 600 MB of memory in idle state (after full initialization). This is critical for RPi 4 2GB stability.

**Target:** < 600 MB idle memory
**Duration:** 10 minutes

---

## Procedure

### Step 1: Start Fresh Container Monitoring

First, ensure containers are running cleanly:
```bash
# Stop and restart containers to get a clean baseline
docker compose down
docker compose up -d

# Wait 30 seconds for CWA to initialize
sleep 30
```

### Step 2: Monitor Memory Over Time

Start Docker stats monitoring in a separate terminal:
```bash
# Monitor continuously (press Ctrl+C to stop)
docker stats calibre-web-automated --no-stream

# For continuous monitoring with timestamp
watch -n 5 'docker stats calibre-web-automated --no-stream'
```

### Step 3: Capture Baseline Measurements

Measure idle memory at multiple intervals (container fully initialized, no library operations):

```bash
# Terminal 1: Continuous monitoring
docker stats calibre-web-automated --format "table {{.Container}}\t{{.MemUsage}}"

# Allow CWA to settle for 2 minutes
# Record readings at: 1 min, 2 min, 5 min
```

### Step 4: Automated Memory Capture Script

Use this script to auto-capture memory readings:

```bash
# Create file: check_memory.sh
#!/bin/bash

echo "CWA Memory Validation - Task 4"
echo "=============================="
echo "Start time: $(date)"
echo ""

# Function to capture memory reading
capture_memory() {
  local delay=$1
  local label=$2

  echo "Waiting ${delay}s ($label)..."
  sleep ${delay}

  # Extract memory usage from docker stats
  memory=$(docker stats calibre-web-automated --no-stream --format "{{.MemUsage}}" | cut -d'/' -f1 | tr -d ' ')
  cpu=$(docker stats calibre-web-automated --no-stream --format "{{.CPUPerc}}" | tr -d ' ')

  echo "${label}: Memory=${memory}, CPU=${cpu}"
}

# Wait for CWA to initialize
echo "Initializing CWA (60 seconds)..."
sleep 60

# Capture readings
capture_memory 0 "1-min idle"
capture_memory 60 "2-min idle"
capture_memory 180 "5-min idle"

# Final summary
echo ""
echo "Final status: $(docker compose ps calibre-web-automated)"
echo "End time: $(date)"
```

Save and run:
```bash
chmod +x check_memory.sh
./check_memory.sh | tee memory_validation_log.txt
```

---

## Expected Results

### Success Criteria

**Pass:** Idle memory < 600 MB at 2-minute mark
```
1-min idle:  Memory=450MB, CPU=15%
2-min idle:  Memory=520MB, CPU=5%
5-min idle:  Memory=540MB, CPU=2%
```

### Potential Issues

**Warning:** 600-750 MB
- Acceptable but monitor during actual library operations
- May indicate cache growth or plugin loading
- Safe margin: still <1.5GB limit

**Fail:** > 750 MB
- Investigate configuration:
  - Check CWA environment variables
  - Review plugin configuration
  - Check for memory leaks in logs
- Consider reducing resource allocation or investigating image bloat
- Document findings for story notes

---

## Detailed Output Format

### Format 1: Raw Docker Stats
```bash
docker stats calibre-web-automated --no-stream --format "table {{.Container}}\t{{.MemUsage}}\t{{.CPUPerc}}\t{{.NetIO}}"
```

**Output:**
```
CONTAINER               MEM USAGE     CPU %      NET I/O
calibre-web-automated  520M / 1.5G   1.2%       1.2MB / 890kB
```

### Format 2: Memory Only (Simple)
```bash
docker stats calibre-web-automated --no-stream --format "{{.MemUsage}}"
# Output: 520MiB / 1.457GiB
```

---

## Validation Checklist

- [ ] Container is running (`docker compose ps` shows "Up")
- [ ] CWA fully initialized (logs show "Server listening on port 8083")
- [ ] No active library operations (library is empty/idle)
- [ ] Measurement taken at 2-minute mark
- [ ] Memory reading < 600 MB
- [ ] Results logged to file
- [ ] Results match expected baseline

---

## If Memory is Too High (> 600 MB)

### Investigation Steps

1. **Check CWA logs for errors:**
```bash
docker compose logs calibre-web-automated | grep -i "error\|warning\|memory"
```

2. **Review container configuration:**
```bash
docker compose config | grep -A 10 "calibre-web-automated:"
```

3. **Check for running processes inside container:**
```bash
docker compose exec calibre-web-automated ps aux
```

4. **Analyze memory allocation in container:**
```bash
docker inspect calibre-web-automated --format='{{.HostConfig.Memory}}'
# Should show: 1572864000 (1.5GB in bytes)
```

5. **Document findings:**
```bash
# Create investigation log
{
  echo "Memory Investigation - Task 4"
  echo "Timestamp: $(date)"
  echo ""
  echo "=== Container Logs ==="
  docker compose logs --tail=50 calibre-web-automated
  echo ""
  echo "=== Memory Status ==="
  docker stats calibre-web-automated --no-stream
  echo ""
  echo "=== Processes ==="
  docker compose exec calibre-web-automated ps aux
} > memory_investigation.log
```

---

## Pass/Fail Decision

**PASS:** Memory ≤ 600 MB at 2-minute mark
- ✅ Meets AC4 requirement
- ✅ Proceed to Task 5

**FAIL:** Memory > 600 MB at 2-minute mark
- ❌ Does not meet AC4
- ❌ Investigate root cause
- ❌ Document issue in story completion notes
- ⚠️ May require RPi 5 or alternative configuration

---

## Output File Format

Save results as: `docs/test-results/task-4-memory-validation.txt`

```
Story: 1.1 - Deploy Calibre-Web-Automated on Raspberry Pi 4
Task: 4 - Validate Idle Memory Usage
Date: 2025-10-26
Tester: Alex
System: Raspberry Pi 4 2GB

=== Measurements ===
1-min idle:   520 MiB (✓ Pass)
2-min idle:   540 MiB (✓ Pass)
5-min idle:   560 MiB (✓ Pass)

Target: < 600 MB
Result: ✓ PASS (560 MiB)

=== Notes ===
Memory usage stable after 2 minutes.
No concerning growth pattern observed.

Task 4: ✓ COMPLETE
```

---

## Next Step

Once **Task 4 passes**, proceed to **Task 5: Initialize test library with sample books**

See: `docs/TEST-LIBRARY-SETUP-TASK-5.md`

---

**Task 4 Status:** Ready for Execution
**Acceptance Criteria:** AC4
**Pass/Fail Threshold:** < 600 MB @ 2-min
