# Task 7: Verify Auto-Restart Policy

**Story:** 1.1 - Deploy Calibre-Web-Automated on Raspberry Pi 4
**Task ID:** 1.1.7
**Acceptance Criteria:** AC6 - Auto-restart policy verified on container stop and system reboot

---

## Overview

This task validates that the CWA and Syncthing containers automatically restart when stopped or when the system reboots. This is critical for ensuring the library server survives crashes and power cycles.

**Duration:** 10-15 minutes

---

## Test 1: Manual Container Stop and Auto-Restart

### Procedure

**Step 1: Note current container status**
```bash
docker compose ps
# Record the container ID/status
```

**Step 2: Stop CWA container**
```bash
docker compose stop calibre-web-automated
sleep 2
```

**Step 3: Verify container stopped**
```bash
docker compose ps
# Expected: calibre-web-automated shows "Exited"
```

**Step 4: Wait and verify auto-restart**
```bash
# With restart policy set to "always", container should auto-restart
# This may take 2-10 seconds depending on system
sleep 5
docker compose ps
# Expected: calibre-web-automated shows "Up X seconds"
```

**Step 5: Verify web UI is accessible**
```bash
# From local machine on network:
curl -s http://raspberrypi.local:8083/ | head -20
# OR open browser and visit: http://raspberrypi.local:8083

# Expected: HTTP 200 OK (login page loads)
```

### Validation

- [ ] Container stopped successfully
- [ ] Container restarted automatically (within 10 seconds)
- [ ] Web UI accessible after restart
- [ ] No manual intervention needed

---

## Test 2: Syncthing Auto-Restart

### Procedure

**Step 1: Stop Syncthing container**
```bash
docker compose stop syncthing
sleep 2
```

**Step 2: Verify container stopped**
```bash
docker compose ps
# Expected: syncthing shows "Exited"
```

**Step 3: Wait and verify auto-restart**
```bash
sleep 5
docker compose ps
# Expected: syncthing shows "Up X seconds"
```

**Step 4: Verify Syncthing web UI (optional)**
```bash
# If accessible from local network:
curl -s http://raspberrypi.local:8384/ | head -20
# Expected: HTTP response (may be 301 redirect or 200)
```

### Validation

- [ ] Syncthing stopped successfully
- [ ] Syncthing restarted automatically
- [ ] Both containers running after restart

---

## Test 3: System Reboot (Full Restart)

**⚠️ WARNING:** This test requires restarting your RPi. **Proceed only if you have local console access or recovery plan.**

### Prerequisites

- [ ] SSH or local console access to RPi
- [ ] No critical processes running
- [ ] Network connectivity after reboot available

### Procedure

**Step 1: Verify current state before reboot**
```bash
# Check all containers running
docker compose ps

# Record time
echo "Pre-reboot time: $(date)"
```

**Step 2: Initiate system reboot**
```bash
# Graceful reboot (safer)
sudo reboot

# OR immediate reboot (less safe)
# sudo shutdown -r now
```

**Step 3: Wait for RPi to restart**
```
Expected: RPi takes 30-60 seconds to reboot
Wait and monitor network connectivity
```

**Step 4: Reconnect and verify containers auto-started**
```bash
# After RPi comes back online:
ssh pi@raspberrypi.local

# Wait 30 seconds for Docker to initialize
sleep 30

# Check container status
docker compose ps
# Expected: All containers "Up" (not "Exited")
```

**Step 5: Verify web UI is accessible**
```bash
# From local machine:
curl -s http://raspberrypi.local:8083/ | grep -i "<!DOCTYPE\|<title" | head -5

# OR from browser:
http://raspberrypi.local:8083
# Expected: Login page loads
```

**Step 6: Check container startup logs**
```bash
# Verify clean startup (no errors)
docker compose logs --tail=30 calibre-web-automated | head -20

# Look for:
# [INFO] Calibre-Web-Automated started
# [INFO] Server listening on port 8083
# (No [ERROR] or [CRITICAL] messages)
```

### Validation

- [ ] RPi rebooted successfully
- [ ] Containers auto-started (no manual docker compose up needed)
- [ ] CWA web UI accessible
- [ ] Syncthing accessible (if checking UI)
- [ ] No critical errors in startup logs
- [ ] Library data preserved (can access library in web UI)

---

## Test 4: Verify Data Persistence Across Restarts

After any of the above restart tests, verify data is preserved:

```bash
# Step 1: Count books in library
docker compose exec calibre-web-automated bash -c 'sqlite3 /calibre-library/metadata.db "SELECT COUNT(*) FROM books;" 2>/dev/null || echo "0"'
# Should match count from Task 5

# Step 2: Access library via web UI
# Navigate to Books → All Books
# Verify same 20+ books visible (not lost)

# Step 3: Verify configuration persisted
# Login with same credentials
# Check: Admin → Settings shows same config

```

- [ ] Book count unchanged after restart
- [ ] Library accessible with same books
- [ ] Configuration persisted
- [ ] No data loss

---

## Verify Restart Policy Configuration

### Check Docker Compose Configuration

```bash
# Verify restart policy in docker-compose.yml
grep -A 2 "restart:" ~/BookHelper/docker-compose.yml

# Expected output:
#   restart: unless-stopped
#   or
#   restart: always
```

### Check Runtime Restart Policy

```bash
# Verify Docker enforces the policy
docker inspect calibre-web-automated --format='{{.HostConfig.RestartPolicy}}'
# Expected: {always 0}

docker inspect syncthing --format='{{.HostConfig.RestartPolicy}}'
# Expected: {always 0}
```

---

## Troubleshooting

### Issue: Container doesn't auto-restart

**Possible Causes:**
1. Restart policy not set in docker-compose.yml
2. Docker daemon not running
3. Container has exit code 0 (intended exit)

**Solution:**
```bash
# Verify restart policy
docker inspect calibre-web-automated --format='{{.HostConfig.RestartPolicy}}'

# If not set to "unless-stopped" or "always", update docker-compose.yml:
# services:
#   calibre-web-automated:
#     restart: unless-stopped

# Then restart:
docker compose down
docker compose up -d
```

### Issue: Container crashes on restart

**Symptoms:**
```bash
docker compose ps
# calibre-web-automated shows: Exited (1) 5 minutes ago (keeps restarting and crashing)
```

**Solution:**
1. Check logs for crash reason:
   ```bash
   docker compose logs calibre-web-automated | tail -50
   ```

2. Common causes:
   - Port 8083 already in use: `sudo lsof -i :8083`
   - Missing volume/mount: Check /library and /config existence and ownership
   - Insufficient memory: Check `docker compose stats calibre-web-automated`
   - Wrong image: Verify image version in docker-compose.yml

### Issue: Containers don't restart after system reboot

**Solution:**
1. Verify Docker daemon auto-starts:
   ```bash
   sudo systemctl enable docker
   sudo systemctl status docker
   ```

2. Verify docker compose project persists:
   ```bash
   # Ensure docker-compose.yml is in persistent location
   # ~/BookHelper/docker-compose.yml should persist across reboots
   ```

3. Check if docker daemon started:
   ```bash
   docker compose ps
   # If daemon didn't start, see error about connection
   # May take 30 seconds after boot for Docker to initialize
   ```

---

## Test Report Template

Save as: `docs/test-results/task-7-auto-restart.txt`

```
Story: 1.1 - Deploy Calibre-Web-Automated on Raspberry Pi 4
Task: 7 - Verify Auto-Restart Policy
Date: 2025-10-26
Tester: Alex

=== Test 1: Manual Container Stop ===
Container stopped: ✓
Auto-restart time: 3 seconds
Web UI accessible: ✓

=== Test 2: Syncthing Restart ===
Container stopped: ✓
Auto-restart time: 2 seconds
UI accessible: ✓

=== Test 3: System Reboot ===
RPi reboot: ✓
Boot time: 45 seconds
Containers auto-started: ✓
Startup errors: None
Web UI accessible: ✓

=== Test 4: Data Persistence ===
Book count pre-reboot: 22
Book count post-reboot: 22 ✓
Configuration persisted: ✓
No data loss: ✓

=== Restart Policy ===
CWA restart policy: always ✓
Syncthing restart policy: always ✓

=== Summary ===
✓ Containers auto-restart on stop
✓ Containers auto-start on reboot
✓ Data persists across restarts
✓ Web UI accessible after restarts

Task 7: ✓ COMPLETE
```

---

## Pass Criteria

**Task 7 PASSES if:**
1. ✅ Container auto-restarts within 10 seconds of manual stop
2. ✅ Web UI accessible after auto-restart
3. ✅ Containers auto-start after system reboot
4. ✅ Library data persists across all restarts
5. ✅ No user intervention needed for service recovery

---

## Next Steps

Once **Task 7 passes**, proceed to:
- **Task 8: Execute acceptance test suite**
- **Task 9: Document deployment and configuration**

---

**Task 7 Status:** Ready for Execution
**Acceptance Criteria:** AC6
**Success Criteria:** Auto-restart verified, data persists
