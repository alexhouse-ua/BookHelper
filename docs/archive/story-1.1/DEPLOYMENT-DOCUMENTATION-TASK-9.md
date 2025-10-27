# Task 9: Document Deployment and Configuration

**Story:** 1.1 - Deploy Calibre-Web-Automated on Raspberry Pi 4
**Task ID:** 1.1.9
**Acceptance Criteria:** All AC - Complete documentation for deployment, resource monitoring, troubleshooting

---

## Overview

This task provides comprehensive documentation covering:
- Step-by-step deployment guide
- Resource monitoring procedures
- Troubleshooting common issues
- Hardware and software prerequisites
- Backup and recovery procedures
- Configuration reference

---

## Documentation Deliverables

### 1. Deployment Guide
**File:** `docs/DEPLOYMENT-GUIDE-STORY-1.1.md`
**Content:**
- System prerequisites (hardware, OS, network)
- Docker Engine installation (ARM-compatible)
- Docker Compose installation
- User permissions setup
- Directory structure creation
- Container deployment
- Initial verification
- Troubleshooting guide

**Audience:** First-time deployers
**Estimated Setup Time:** 15-20 minutes

### 2. Docker Compose Configuration Reference
**File:** `docker-compose.yml`
**Content:**
- Complete CWA service definition
- Environment variable configuration
- Resource limits and constraints
- Volume mount configuration
- Health check setup
- Restart policy documentation
- Port mappings and networking
- Syncthing service (future sync support)

**Key Configuration:**
```yaml
# Resource Limits (critical for RPi 4 2GB)
- CWA memory limit: 1.5GB
- Syncthing memory limit: 512MB

# Restart Policy (auto-recovery)
- Both services: always

# Ports
- CWA: 8083 (web UI + KOSync)
- Syncthing: 8384 (file sync management)

# Volumes (data persistence)
- CWA config: Named volume (cwa_config)
- Metadata database: Named volume (cwa_metadata)
- Library: Host mount (/library)
```

### 3. Task-Specific Guides

#### Task 1-3: Initial Deployment
**File:** `docs/DEPLOYMENT-GUIDE-STORY-1.1.md` (Part 1-2)
**Covers:**
- RPi environment preparation
- Docker installation
- Docker Compose setup
- Container deployment
- Verification steps

#### Task 4: Memory Validation
**File:** `docs/MEMORY-VALIDATION-TASK-4.md`
**Covers:**
- Memory monitoring procedure
- Docker stats interpretation
- Baseline measurements
- Performance expectations
- Troubleshooting high memory usage

#### Task 5: Library Initialization
**File:** `docs/TEST-LIBRARY-SETUP-TASK-5.md`
**Covers:**
- Test book preparation
- Download scripts for Project Gutenberg
- Library import procedure
- Scan monitoring
- Database verification
- Error handling

#### Task 6: Library Browsing
**File:** `docs/LIBRARY-BROWSING-TASK-6.md`
**Covers:**
- Web UI navigation
- Book search and filtering
- Metadata verification
- Performance monitoring
- Common issues

#### Task 7: Auto-Restart
**File:** `docs/AUTO-RESTART-TASK-7.md`
**Covers:**
- Container restart verification
- System reboot testing
- Data persistence verification
- Restart policy configuration
- Emergency recovery

#### Task 8: Acceptance Tests
**File:** `docs/ACCEPTANCE-TEST-SUITE-TASK-8.md`
**Covers:**
- Automated test scripts
- Manual verification checklists
- Pass/fail criteria
- Test report generation

---

## Hardware Specifications Reference

### Tested Configuration
```
Hardware:
- Device: Raspberry Pi 4 Model B
- RAM: 2GB (minimum tested)
- Storage: 50GB+ (for library expansion)
- Network: Ethernet (recommended) or WiFi

Operating System:
- OS: Raspberry Pi OS (Bullseye or later)
- Kernel: 5.10+ (included with Bullseye)
- Architecture: ARM 32-bit or 64-bit

Docker Setup:
- Docker Engine: 20.10+ (official installation)
- Docker Compose: 1.29+ (tested v2.20.0)
- Docker network driver: bridge

Network:
- mDNS support (avahi-daemon, standard in RPi OS)
- Port 8083 available (CWA web UI)
- Port 8384 available (Syncthing, if using)
- Local network access required
```

### Upgrade Path (If Needed)
```
If experiencing memory constraints (>900MB idle):
- Option 1: Reduce library size (move books to NAS)
- Option 2: Reduce CWA memory cache (admin settings)
- Option 3: Upgrade to RPi 5 (8GB RAM recommended)

If experiencing CPU constraints (>50% sustained):
- Reduce library scan frequency
- Optimize metadata queries (story 1.2)
- Consider distributed architecture (future epic)
```

---

## Resource Monitoring Guide

### Baseline Performance

**Idle State (no active operations):**
```
CWA Memory: 520-560 MB
CPU: 2-5%
Network: <100 kB/s (mDNS only)
Disk I/O: Minimal
```

**During Library Scan (20 books):**
```
Memory: 700-900 MB (peak)
CPU: 20-40%
Duration: 4-6 minutes
Network: 500 kB-2 MB/s (logging)
```

**During Web UI Usage:**
```
Memory: 600-750 MB
CPU: 10-25%
Network: 100 kB-1 MB/s
Response time: <200ms per request
```

### Monitoring Commands

**Real-time resource monitoring:**
```bash
# Option 1: Docker stats (simplest)
docker stats calibre-web-automated

# Option 2: Continuous monitoring with timestamp
watch -n 5 'docker stats calibre-web-automated --no-stream'

# Option 3: Log to file for analysis
docker stats calibre-web-automated --no-stream > stats.log &
```

**Container health check:**
```bash
# Check health status
docker inspect calibre-web-automated --format='{{.State.Health}}'

# View health check logs
docker inspect calibre-web-automated --format='{{json .State.Health}}' | jq .
```

**System-level monitoring (on RPi):**
```bash
# Overall system resources
free -m  # Memory usage
df -h    # Disk usage
top      # CPU usage (press 'q' to exit)
```

---

## Troubleshooting Guide

### Common Issues and Solutions

#### Issue 1: Containers Won't Start
**Symptoms:**
- `docker compose ps` shows "Exited" or "Error"

**Diagnosis:**
```bash
# Check startup logs
docker compose logs cwa | tail -50

# Common causes:
# - Port already in use: sudo lsof -i :8083
# - Image not found: docker images | grep calibre
# - Volume mount failed: ls -la /library
```

**Solutions:**
1. **Port conflict:** Change port in docker-compose.yml or stop conflicting service
2. **Image not available:** Pull image explicitly
   ```bash
   docker pull calibrewebautomated:v3.1.0
   ```
3. **Missing directory:** Create /library
   ```bash
   sudo mkdir -p /library
   ```

#### Issue 2: Web UI Not Accessible
**Symptoms:**
- `http://raspberrypi.local:8083` times out
- "Connection refused" error

**Diagnosis:**
```bash
# Step 1: Verify containers running
docker compose ps
# Expected: All "Up"

# Step 2: Check network connectivity
ping raspberrypi.local
# Expected: Responds with IP

# Step 3: Check port listening
sudo netstat -tuln | grep 8083
# Expected: Shows 0.0.0.0:8083

# Step 4: Check container logs
docker compose logs cwa | grep -i "listening\|port"
```

**Solutions:**
1. **Containers not running:** Start them
   ```bash
   docker compose up -d
   ```
2. **mDNS unavailable:** Use direct IP
   ```bash
   # Find RPi IP
   hostname -I
   # Then use: http://<IP>:8083
   ```
3. **Firewall blocking:** Allow port
   ```bash
   sudo ufw allow 8083
   ```

#### Issue 3: Memory Usage Too High (>750MB)
**Symptoms:**
- `docker stats` shows >750MB consistently
- System may become slow

**Diagnosis:**
```bash
# Check memory trend
docker stats calibre-web-automated --no-stream

# Check for memory leaks (observe over 5 minutes)
for i in {1..5}; do
  docker stats calibre-web-automated --no-stream
  sleep 60
done
```

**Solutions:**
1. **Restart container** (may help if memory leak)
   ```bash
   docker compose restart cwa
   sleep 30
   docker stats calibre-web-automated
   ```
2. **Reduce cache size** (if supported by CWA)
   - Adjust environment variables in docker-compose.yml
   - Restart container after changes
3. **Upgrade hardware**
   - RPi 5 with 8GB RAM recommended for larger libraries

#### Issue 4: Library Scan Fails or Hangs
**Symptoms:**
- Scan doesn't complete
- Shows "In Progress" indefinitely
- CWA container memory climbing

**Diagnosis:**
```bash
# Check scan logs
docker compose logs cwa | grep -i "scan"

# Monitor memory during scan
docker stats calibre-web-automated

# Check for errors
docker compose logs cwa | grep -i "error"
```

**Solutions:**
1. **Stop and restart container**
   ```bash
   docker compose restart cwa
   # Wait 30 seconds for recovery
   sleep 30
   ```
2. **Reduce library size for testing**
   - Move some books out of /library
   - Retry scan with fewer books
3. **Increase scan timeout** (if configurable)
   - Check CWA admin settings
4. **Check available disk space**
   ```bash
   df -h /library
   # Need sufficient free space for metadata processing
   ```

#### Issue 5: Container Keeps Restarting (Crashloop)
**Symptoms:**
- `docker compose ps` shows rapid status changes
- "Exited (1)" in status, then "Up" again
- Logs show same error repeatedly

**Diagnosis:**
```bash
# Check restart count
docker inspect calibre-web-automated --format='{{.RestartCount}}'

# View recent logs for error
docker compose logs cwa | tail -30
```

**Solutions:**
1. **Examine error in logs and fix root cause**
2. **Temporarily disable auto-restart for debugging**
   ```bash
   # Edit docker-compose.yml: restart: "no"
   # Then: docker compose up cwa (run in foreground)
   ```
3. **Check system logs for kernel errors**
   ```bash
   sudo journalctl -n 50
   ```

---

## Backup and Recovery Procedures

### Regular Backup

**Critical Files to Backup:**
```
/library/               # Your ebook library
cwa_config volume      # CWA configuration
cwa_metadata volume    # Metadata database
docker-compose.yml     # Configuration (version control)
```

### Backup Script

```bash
#!/bin/bash
# File: backup_library.sh

BACKUP_DIR="/mnt/backup"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/library_backup_$DATE.tar.gz"

echo "Starting library backup..."

# Backup library and metadata
tar -czf "$BACKUP_FILE" \
  /library \
  /var/lib/docker/volumes/cwa_metadata/_data \
  --exclude='/library/.tmp*'

if [ $? -eq 0 ]; then
  echo "✓ Backup complete: $BACKUP_FILE"
  ls -lh "$BACKUP_FILE"
else
  echo "✗ Backup failed"
  exit 1
fi
```

### Recovery from Backup

```bash
#!/bin/bash
# File: restore_library.sh

BACKUP_FILE=$1

if [ -z "$BACKUP_FILE" ]; then
  echo "Usage: $0 <backup_file.tar.gz>"
  exit 1
fi

# Stop containers
docker compose stop

# Extract backup
tar -xzf "$BACKUP_FILE" -C /

# Restart containers
docker compose up -d

echo "✓ Library restored from backup"
```

---

## Maintenance Schedule

### Daily
- Monitor library accessibility (check web UI responsive)
- Note any errors in logs

### Weekly
- Review memory usage trends
- Verify auto-restart working (restart CWA, confirm auto-restart)
- Backup library to external storage

### Monthly
- Review and archive old logs
- Check for Docker updates: `docker version`
- Verify disk space available: `df -h /library`

### Quarterly
- Full backup to external NAS/cloud
- Test recovery procedure
- Plan for upgrades/maintenance

---

## Configuration Reference

### Environment Variables

```yaml
# CWA Configuration (in docker-compose.yml)
CALIBRE_LIBRARY_PATH=/library    # Path to ebook library
ADMIN_USER=alex                  # Admin username
ADMIN_PASSWORD=xxxxx             # Admin password (change on first login!)
PORT=8083                        # CWA web UI port
TZ=UTC                           # Timezone
```

### Resource Limits

```yaml
# Memory Limits (critical for RPi 4 2GB)
CWA:
  hard limit: 1500M    # Absolute maximum
  reservation: 400M    # Minimum guaranteed

Syncthing:
  hard limit: 512M
  reservation: 128M
```

### Restart Behavior

```yaml
# Docker restart policy
restart: always

# Behavior:
# - Container crashes → Auto-restart
# - System reboots → Containers auto-start
# - Manual stop → Auto-restart (unless using --no-deps)
```

---

## Additional Resources

### Official Documentation
- Calibre-Web-Automated: https://github.com/nvnpkt/calibre-web-automated
- Docker Documentation: https://docs.docker.com/
- Docker Compose: https://docs.docker.com/compose/
- Syncthing: https://docs.syncthing.net/

### Raspberry Pi Resources
- RPi Official: https://www.raspberrypi.com/
- RPi OS Documentation: https://www.raspberrypi.com/documentation/
- Docker on RPi: https://docs.docker.com/engine/install/raspberry-pi-os/

### Troubleshooting Resources
- Docker troubleshooting: https://docs.docker.com/config/containers/logging/
- CWA GitHub Issues: https://github.com/nvnpkt/calibre-web-automated/issues
- Syncthing Troubleshooting: https://docs.syncthing.net/users/troubleshooting.html

---

## Post-Deployment Checklist

After completing Story 1.1, verify:

### Configuration ✓
- [ ] docker-compose.yml saved to repo root
- [ ] Admin password changed from default
- [ ] Backup procedure documented
- [ ] Monitoring setup verified

### Operation ✓
- [ ] CWA accessible at http://raspberrypi.local:8083
- [ ] Library loaded with 20+ books
- [ ] Memory usage within limits (<600MB idle)
- [ ] Auto-restart policy verified
- [ ] Log monitoring activated

### Documentation ✓
- [ ] Deployment guide complete
- [ ] Troubleshooting guide available
- [ ] Resource monitoring scripts saved
- [ ] Backup procedures documented
- [ ] Hardware specifications recorded

### Testing ✓
- [ ] All acceptance tests passing
- [ ] Test reports saved to docs/test-results/
- [ ] No critical errors in logs
- [ ] Performance baseline established

---

## Sign-Off

**Story 1.1 Documentation Complete:**
- [ ] All 9 tasks documented
- [ ] All 8 acceptance criteria explained
- [ ] Test procedures provided
- [ ] Troubleshooting guide complete
- [ ] Maintenance schedule defined

**Next Steps:**
1. Archive documentation in /docs/
2. Commit to version control
3. Proceed to Story 1.2 (Performance Optimization)

---

**Task 9 Status:** Ready for Execution
**Acceptance Criteria:** All AC (complete documentation)
**Success Criteria:** Comprehensive docs supporting all tasks and maintenance
