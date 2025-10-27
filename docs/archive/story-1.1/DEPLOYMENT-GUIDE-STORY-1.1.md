# Story 1.1 Deployment Guide: Calibre-Web-Automated on Raspberry Pi 4

**Story ID:** 1.1
**Status:** Implementation
**Target System:** Raspberry Pi 4 (2GB RAM)
**Date:** 2025-10-26

---

## Overview

This guide walks through the deployment of Calibre-Web-Automated (CWA) v3.1.0+ with Syncthing on your Raspberry Pi 4. The docker-compose.yml file is pre-configured; you only need to follow the steps below on your RPi.

**Estimated Time:** 15-20 minutes for setup + 5 minutes for verification

---

## Prerequisites Checklist

Before starting, verify your RPi 4 meets these requirements:

- [ ] Raspberry Pi 4 Model B with 2GB RAM
- [ ] Raspberry Pi OS (Bullseye or later) installed and updated
- [ ] Network connectivity (Ethernet or WiFi) with local network access
- [ ] SSH access to RPi or physical console access
- [ ] At least 50GB free storage (for ebook library)

---

## Part 1: Prepare Raspberry Pi Environment (Task 1)

### Step 1.1: Update System

SSH into your RPi:
```bash
ssh pi@raspberrypi.local
# OR if using a different hostname/IP:
ssh pi@<your_rpi_ip>
```

Update package lists and system:
```bash
sudo apt update
sudo apt full-upgrade -y
```

### Step 1.2: Install Docker Engine (ARM-compatible)

Install Docker using the official Raspberry Pi installation script:
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
rm get-docker.sh
```

Verify Docker installation:
```bash
docker --version
# Output should be: Docker version 20.10+ (or higher)
```
> Docker version 28.5.1, build e180ab8

### Step 1.3: Install Docker Compose

Install the latest Docker Compose:
```bash
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

Verify installation:
```bash
docker compose --version
# Output should be: Docker Compose version 2.20.0 (or higher)
```
> Docker Compose version v2.40.2
> Came pre-installed with Docker Engine, syntax is docker compose, not docker-compose

### Step 1.4: Add User to Docker Group (No Sudo Required)

This allows running docker commands without sudo:
```bash
sudo usermod -aG docker $USER
newgrp docker
```

Verify (should work without sudo):
```bash
docker ps
# Should show empty container list (not permission denied error)
```

### Step 1.5: Create Directory Structure

Create the library directories on your RPi:
```bash
sudo mkdir -p /library/ingest /library/metadata
sudo chmod 755 /library /library/ingest /library/metadata
```

Verify:
```bash
ls -la /library
# Should show: ingest, metadata directories
```

---

## Part 2: Deploy and Verify CWA Startup (Task 3)

### Step 2.1: Clone/Copy docker-compose.yml

On your local machine (or RPi if cloning the repo):
```bash
# Option A: Clone the BookHelper repo
git clone https://github.com/alexhouse-ua/BookHelper.git
cd BookHelper

# Option B: Copy the docker-compose.yml to your RPi
# (Run this from your local machine)
scp docker-compose.yml pi@raspberrypi.local:~/BookHelper/
```

### Step 2.2: Set Admin Password Environment Variable

On the RPi, before deploying, set the CWA admin password:
```bash
# Set environment variable for CWA admin password
export ADMIN_PASSWORD="your_secure_password_here"
```

Or edit docker-compose.yml directly to set a static password (less secure):
```bash
nano docker-compose.yml
# Find: ADMIN_PASSWORD=${ADMIN_PASSWORD:-changeme123}
# Change to: ADMIN_PASSWORD=your_secure_password_here
```

### Step 2.3: Deploy Containers

From the BookHelper directory on your RPi:
```bash
cd ~/BookHelper
docker compose up -d
```

Check container startup:
```bash
docker compose ps
```

Expected output:
```
NAME                    STATUS
calibre-web-automated        Up X seconds (health: starting)
syncthing  Up X seconds (health: starting)
```

>actual names: calibre-web-automated and syncthing

### Step 2.4: Wait for Initialization

CWA takes ~30 seconds to fully initialize. Monitor progress:
```bash
docker compose logs -f cwa
```

Wait until you see messages like:
```
[INFO] Calibre-Web-Automated initialized
[INFO] Metadata database ready
[INFO] Server listening on port 8083
```

Press `Ctrl+C` to exit log view.

### Step 2.5: Verify mDNS Hostname Resolution

Verify your RPi is accessible via `raspberrypi.local`:
```bash
# On RPi:
hostname -I
# Note your RPi IP address

> 192.168.1.222 172.17.0.1 172.18.0.1 2600:1702:6c80:6400::1c 2600:1702:6c80:6400:b2ec:77eb:726f:6455

# On another device on the network:
ping raspberrypi.local
# Should resolve to your RPi IP and show responses
```

If ping fails, fall back to direct IP:
```bash
# Use the IP from hostname -I instead
ping <your_rpi_ip>
```

### Step 2.6: Access CWA Web UI

From any device on your network, open your browser:
```
http://raspberrypi.local:8083
```

Or use direct IP if mDNS unavailable:
```
http://<your_rpi_ip>:8083
```

**Expected Screen:** CWA login page with version number (v3.1.0+)

**Login with:**
- Username: `alexhouse`
- Password: The password you set in Step 2.2

### Step 2.7: Verify Basic Library Interface

After login, navigate to:
- **Books → All Books** (should be empty initially)
- **Admin → Library Management** (should show scan option)
- **Admin → Settings** (verify configuration loaded)

If all pages load without errors, **Task 3 is complete!**

---

## Part 3: View Container Health and Logs

### Check Current Status
```bash
# Full status of all services
docker compose ps

# Check service health
docker compose ps --services
```

### View Logs
```bash
# View CWA logs (last 50 lines)
docker compose logs --tail=50 cwa

# View Syncthing logs
docker compose logs --tail=50 syncthing

# Follow logs in real-time
docker compose logs -f cwa
```

### Monitor Resource Usage
```bash
# View real-time memory/CPU usage
docker stats calibre-web-automated

# Record to file for later analysis
docker stats calibre-web-automated > cwa_stats.log &
```

---

## Part 4: Troubleshooting

### Issue: Containers won't start

**Error:** `docker-compose: command not found`
- **Solution:** Reinstall Docker Compose (Step 1.3)

**Error:** `docker: permission denied`
- **Solution:** Add user to docker group again, log out and back in

**Error:** `Cannot connect to Docker daemon`
- **Solution:** Start Docker daemon: `sudo systemctl start docker`

### Issue: Web UI not accessible

**Check 1:** Verify containers are running
```bash
docker compose ps
```

**Check 2:** Verify port mappings
```bash
sudo netstat -tuln | grep 8083
# Should show port 8083 listening
```

**Check 3:** Check CWA logs for errors
```bash
docker compose logs cwa | tail -20
```

**Check 4:** Verify firewall rules
```bash
# If using UFW
sudo ufw allow 8083
sudo ufw allow 8384
```

### Issue: mDNS hostname not resolving

**Workaround:** Use direct IP address
```bash
# Find your RPi IP
hostname -I

# Use IP in browser instead of hostname
http://<your_rpi_ip>:8083
```

---

## Cleanup and Stopping Services

To temporarily stop services:
```bash
docker compose stop
```

To stop and remove containers (data persists in volumes):
```bash
docker compose down
```

To remove everything including volumes (⚠️ deletes library data):
```bash
docker compose down -v
```

---

## Next Steps After Verification

Once **Part 2.7** is complete (Web UI loads successfully):

1. **Task 4:** Monitor idle memory usage (see docs/MEMORY-VALIDATION-TASK-4.md)
2. **Task 5:** Add test books to library (see docs/TEST-LIBRARY-SETUP-TASK-5.md)
3. **Task 6:** Test library browsing functionality
4. **Task 7:** Verify auto-restart policy
5. **Task 8:** Run acceptance test suite
6. **Task 9:** Documentation complete

---

## Reference: Docker Compose Commands

```bash
# Start services
docker compose up -d

# Check status
docker compose ps

# View logs
docker compose logs -f <service_name>

# Stop services
docker compose stop

# Stop and remove containers
docker compose down

# View resource usage
docker stats

# Access CWA container shell
docker compose exec cwa bash

# Validate docker-compose.yml syntax
docker compose config
```

---

## Support and Questions

If you encounter issues:

1. Check container logs: `docker compose logs`
2. Verify prerequisites are met
3. Review troubleshooting section above
4. Document error messages and attach to story notes

---

**Story 1.1 Status:** ✏️ In Progress
**Deployment Guide:** ✅ Complete
**Next:** Monitor and verify deployment on RPi
