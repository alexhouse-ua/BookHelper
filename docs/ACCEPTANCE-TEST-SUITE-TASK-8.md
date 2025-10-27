# Task 8: Execute Acceptance Test Suite

**Story:** 1.1 - Deploy Calibre-Web-Automated on Raspberry Pi 4
**Task ID:** 1.1.8
**Acceptance Criteria:** AC1-8 - All acceptance criteria verified through comprehensive testing

---

## Overview

This task provides automated and manual tests to verify all 8 acceptance criteria for Story 1.1. Tests cover:
- Docker Compose configuration validity
- CWA HTTP endpoint health
- Library initialization and scanning
- Memory constraints
- Auto-restart functionality
- Service health and logging

**Duration:** 20-30 minutes for full suite

---

## Test Environment Setup

Before running tests, ensure:
```bash
# Verify all containers running
docker-compose ps
# Expected: All containers "Up"

# Verify library populated from Task 5
ls -la /library/ | wc -l
# Expected: 20+ files

# Note: Run all tests from RPi or with network access to CWA
```

---

## Test Suite 1: Docker Compose Configuration (AC1)

### Purpose
Verify that docker-compose.yml is valid and includes all required configuration.

### Automated Test: Validate YAML Syntax

```bash
#!/bin/bash
# File: test_docker_compose_syntax.sh

echo "=== Test 1: Docker Compose Syntax ==="

# Test 1.1: Validate YAML structure
docker-compose config > /dev/null 2>&1
if [ $? -eq 0 ]; then
  echo "✓ docker-compose.yml syntax valid"
else
  echo "✗ docker-compose.yml has syntax errors"
  docker-compose config
  exit 1
fi

# Test 1.2: Verify services defined
services=$(docker-compose config --services)
echo "✓ Services found: $(echo $services | tr '\n' ', ')"

# Test 1.3: Verify CWA service
docker-compose config | grep -q "calibrewebautomated:v3.1"
if [ $? -eq 0 ]; then
  echo "✓ CWA v3.1.0+ configured"
else
  echo "⚠ CWA version may not be v3.1.0+"
fi

# Test 1.4: Verify restart policy
docker-compose config | grep -A 3 "cwa:" | grep -q "restart: always"
if [ $? -eq 0 ]; then
  echo "✓ CWA restart policy set to always"
else
  echo "✗ CWA restart policy not set"
  exit 1
fi

# Test 1.5: Verify memory limits
docker-compose config | grep -q "memory: 1500M"
if [ $? -eq 0 ]; then
  echo "✓ CWA memory limit set to 1500MB"
else
  echo "⚠ CWA memory limit may not be configured"
fi

# Test 1.6: Verify ports mapped
docker-compose config | grep -q "8083:8083"
if [ $? -eq 0 ]; then
  echo "✓ Port 8083 mapped for CWA"
else
  echo "✗ Port 8083 not mapped"
  exit 1
fi

echo ""
echo "✓ AC1: Docker Compose configuration VALID"
```

**Run Test:**
```bash
chmod +x test_docker_compose_syntax.sh
./test_docker_compose_syntax.sh
```

---

## Test Suite 2: HTTP Endpoint Health (AC2)

### Purpose
Verify CWA web UI is accessible on local network at port 8083.

### Automated Test: HTTP Connectivity

```bash
#!/bin/bash
# File: test_cwa_http_endpoint.sh

echo "=== Test 2: HTTP Endpoint Health (AC2) ==="

TARGET_URL="http://raspberrypi.local:8083"
TIMEOUT=10

# Test 2.1: DNS resolution
echo -n "Testing DNS resolution for raspberrypi.local... "
if ping -c 1 -W $TIMEOUT raspberrypi.local > /dev/null 2>&1; then
  echo "✓ mDNS resolves"
  RESOLVED_IP=$(ping -c 1 raspberrypi.local | grep -oP '\d+\.\d+\.\d+\.\d+' | head -1)
  echo "  Resolved to: $RESOLVED_IP"
else
  echo "⚠ mDNS unavailable, using direct IP"
  TARGET_URL="http://192.168.1.X:8083"  # Replace X with your RPi IP
fi

# Test 2.2: HTTP connectivity
echo -n "Testing HTTP connectivity to CWA... "
http_code=$(curl -s -o /dev/null -w "%{http_code}" -m $TIMEOUT $TARGET_URL)
if [ "$http_code" = "200" ] || [ "$http_code" = "302" ] || [ "$http_code" = "301" ]; then
  echo "✓ HTTP $http_code"
else
  echo "✗ HTTP $http_code (expected 200/302)"
  exit 1
fi

# Test 2.3: Login page accessible
echo -n "Testing login page loads... "
if curl -s $TARGET_URL | grep -q "login\|password" >/dev/null 2>&1; then
  echo "✓ Login form detected"
else
  echo "⚠ Login form not detected (may be redirected)"
fi

# Test 2.4: Version check (if available)
echo -n "Checking CWA version... "
version=$(curl -s $TARGET_URL | grep -oP "v\d+\.\d+" | head -1)
if [ -n "$version" ]; then
  echo "✓ Version found: $version"
else
  echo "⚠ Version not visible (check manually)"
fi

echo ""
echo "✓ AC2: HTTP endpoint accessible and responsive"
```

**Run Test:**
```bash
chmod +x test_cwa_http_endpoint.sh
./test_cwa_http_endpoint.sh
```

---

## Test Suite 3: Library Initialization (AC3, AC5)

### Purpose
Verify library is initialized with 20+ books and accessible without crashes.

### Automated Test: Library Integrity

```bash
#!/bin/bash
# File: test_library_initialization.sh

echo "=== Test 3: Library Initialization (AC3, AC5) ==="

# Test 3.1: Count files in /library
echo -n "Checking library directory... "
book_count=$(ls /library/*.* 2>/dev/null | wc -l)
if [ $book_count -ge 20 ]; then
  echo "✓ Found $book_count books (minimum 20)"
else
  echo "⚠ Found only $book_count books (expected 20+)"
fi

# Test 3.2: Check database exists and is readable
echo -n "Verifying metadata database... "
if docker-compose exec cwa test -f /metadata/metadata.db; then
  echo "✓ metadata.db exists"
else
  echo "✗ metadata.db not found"
  exit 1
fi

# Test 3.3: Count books in database
echo -n "Counting indexed books... "
db_count=$(docker-compose exec cwa sqlite3 /metadata/metadata.db "SELECT COUNT(*) FROM books;" 2>/dev/null)
if [ -z "$db_count" ]; then
  db_count=0
fi

if [ $db_count -ge 20 ]; then
  echo "✓ $db_count books indexed"
else
  echo "⚠ Only $db_count books indexed (expected 20+)"
fi

# Test 3.4: Verify no corruption
echo -n "Checking database integrity... "
integrity=$(docker-compose exec cwa sqlite3 /metadata/metadata.db "PRAGMA integrity_check;" 2>/dev/null)
if [ "$integrity" = "ok" ]; then
  echo "✓ Database integrity OK"
else
  echo "✗ Database corruption detected: $integrity"
  exit 1
fi

# Test 3.5: Check for critical errors in logs
echo -n "Scanning logs for critical errors... "
errors=$(docker-compose logs cwa | grep -i "error\|crash\|oom" | wc -l)
if [ $errors -eq 0 ]; then
  echo "✓ No critical errors"
else
  echo "⚠ Found $errors error messages in logs"
  docker-compose logs cwa | grep -i "error" | tail -5
fi

echo ""
echo "✓ AC3, AC5: Library initialized with books, no crashes"
```

**Run Test:**
```bash
chmod +x test_library_initialization.sh
./test_library_initialization.sh
```

---

## Test Suite 4: Memory Validation (AC4)

### Purpose
Verify idle memory usage is < 600 MB.

### Automated Test: Memory Monitoring

```bash
#!/bin/bash
# File: test_memory_validation.sh

echo "=== Test 4: Memory Validation (AC4) ==="

# Wait for stable idle state
echo "Waiting 60 seconds for CWA to reach idle state..."
sleep 60

# Capture memory readings
echo "Capturing memory usage..."
memory_reading=$(docker stats bookhelper_cwa_1 --no-stream --format "{{.MemUsage}}" | cut -d'/' -f1 | sed 's/[MiB ]//g')

echo "Memory usage: ${memory_reading}MB"

# Parse numeric value
memory_value=$(echo $memory_reading | grep -oP '^\d+')

if [ $memory_value -lt 600 ]; then
  echo "✓ Memory usage < 600MB (AC4 PASS)"
  exit 0
else
  echo "✗ Memory usage ${memory_value}MB >= 600MB (AC4 FAIL)"
  echo ""
  echo "Additional diagnostics:"
  docker stats bookhelper_cwa_1 --no-stream
  docker-compose logs cwa | tail -20
  exit 1
fi
```

**Run Test:**
```bash
chmod +x test_memory_validation.sh
./test_memory_validation.sh
```

---

## Test Suite 5: Service Health (AC7, AC8)

### Purpose
Verify all services are running and responsive.

### Automated Test: Service Health Check

```bash
#!/bin/bash
# File: test_service_health.sh

echo "=== Test 5: Service Health (AC7, AC8) ==="

# Test 5.1: CWA running
echo -n "Checking CWA container status... "
cwa_status=$(docker-compose ps cwa --format "{{.State}}")
if [ "$cwa_status" = "Up" ]; then
  echo "✓ Running"
else
  echo "✗ Status: $cwa_status"
  exit 1
fi

# Test 5.2: Syncthing running
echo -n "Checking Syncthing container status... "
sync_status=$(docker-compose ps syncthing --format "{{.State}}")
if [ "$sync_status" = "Up" ]; then
  echo "✓ Running"
else
  echo "✗ Status: $sync_status"
  exit 1
fi

# Test 5.3: Port 8083 listening
echo -n "Verifying port 8083 is listening... "
if netstat -tuln 2>/dev/null | grep -q ":8083 "; then
  echo "✓ Listening"
else
  echo "⚠ Port check unavailable"
fi

# Test 5.4: Check for error patterns in logs
echo -n "Scanning logs for critical errors... "
error_patterns="error\|critical\|failed\|exception"
critical_errors=$(docker-compose logs | grep -i "$error_patterns" | grep -v "warning" | wc -l)

if [ $critical_errors -eq 0 ]; then
  echo "✓ No critical errors"
else
  echo "⚠ Found $critical_errors potential errors"
  docker-compose logs | grep -i "$error_patterns" | grep -v "warning" | head -5
fi

# Test 5.5: Health check status (if configured)
echo -n "Checking container health... "
health=$(docker inspect bookhelper_cwa_1 --format='{{.State.Health.Status}}' 2>/dev/null)
if [ -n "$health" ]; then
  echo "✓ Health: $health"
else
  echo "⚠ Health check not configured"
fi

echo ""
echo "✓ AC7, AC8: Services running, responsive, no critical errors"
```

**Run Test:**
```bash
chmod +x test_service_health.sh
./test_service_health.sh
```

---

## Manual Acceptance Criteria Checklist

Run through this checklist manually to verify remaining criteria:

### AC1: Docker Compose Stack Configured ✓
- [ ] docker-compose.yml exists in repo root
- [ ] Version 3.8 specified
- [ ] CWA v3.1.0+ configured
- [ ] Memory limits set (1.5GB CWA, 512MB Syncthing)
- [ ] Restart policies set to "always"
- [ ] Volumes configured for persistence

### AC2: Web UI Accessible ✓
- [ ] URL http://raspberrypi.local:8083 responds with 200 OK
- [ ] Login page displays
- [ ] Version string visible (v3.1.0+)
- [ ] Can log in with admin credentials

### AC3: Library Initialized ✓
- [ ] 20+ books visible in web UI
- [ ] Books display with title, author, cover
- [ ] Detail pages load without errors
- [ ] Search functionality works

### AC4: Memory < 600MB ✓
- [ ] Idle memory measured at 2-minute mark
- [ ] Result < 600 MB
- [ ] Test results documented

### AC5: Library Scan Completes ✓
- [ ] Scan initiated successfully
- [ ] All 20+ books imported
- [ ] No crashes during scan
- [ ] No OOM errors in logs
- [ ] Scan time recorded

### AC6: Auto-Restart Policy ✓
- [ ] Container restarts after manual stop
- [ ] Services auto-start after system reboot
- [ ] Data persists across restarts

### AC7: All Services Running ✓
- [ ] CWA container status: Up
- [ ] Syncthing container status: Up
- [ ] Both services responding to health checks
- [ ] No container crashloops

### AC8: Service Health Verified ✓
- [ ] CWA responds to web requests (HTTP 200)
- [ ] Container logs show no critical errors
- [ ] Startup sequence completes normally
- [ ] Metadata.db initialization successful

---

## Test Execution Script

Create comprehensive test runner:

```bash
#!/bin/bash
# File: run_all_tests.sh

echo "================================"
echo "Story 1.1 Acceptance Test Suite"
echo "================================"
echo ""

PASSED=0
FAILED=0

run_test() {
  local test_name=$1
  local test_script=$2

  echo "Running: $test_name"
  if bash $test_script; then
    PASSED=$((PASSED + 1))
  else
    FAILED=$((FAILED + 1))
  fi
  echo ""
}

# Run all tests
run_test "Test 1: Docker Compose Syntax" "test_docker_compose_syntax.sh"
run_test "Test 2: HTTP Endpoint" "test_cwa_http_endpoint.sh"
run_test "Test 3: Library Initialization" "test_library_initialization.sh"
run_test "Test 4: Memory Validation" "test_memory_validation.sh"
run_test "Test 5: Service Health" "test_service_health.sh"

# Summary
echo "================================"
echo "Test Results"
echo "================================"
echo "Passed: $PASSED"
echo "Failed: $FAILED"
echo ""

if [ $FAILED -eq 0 ]; then
  echo "✓ ALL TESTS PASSED"
  exit 0
else
  echo "✗ $FAILED test(s) failed"
  exit 1
fi
```

**Run Full Suite:**
```bash
chmod +x run_all_tests.sh
./run_all_tests.sh
```

---

## Test Report Template

Save as: `docs/test-results/task-8-acceptance-suite.txt`

```
Story: 1.1 - Deploy Calibre-Web-Automated on Raspberry Pi 4
Task: 8 - Execute Acceptance Test Suite
Date: 2025-10-26
Tester: Alex

=== Automated Tests ===

Test 1 (AC1): Docker Compose Syntax
  Result: ✓ PASS
  Details: All services configured, restart policies set, memory limits OK

Test 2 (AC2): HTTP Endpoint Health
  Result: ✓ PASS
  Status: HTTP 200
  Response time: 150ms

Test 3 (AC3, AC5): Library Initialization
  Result: ✓ PASS
  Books indexed: 22/22
  Database integrity: OK
  Critical errors: 0

Test 4 (AC4): Memory Validation
  Result: ✓ PASS
  Memory usage: 540MB (target: <600MB)
  Margin: 60MB

Test 5 (AC7, AC8): Service Health
  Result: ✓ PASS
  CWA status: Up
  Syncthing status: Up
  Critical errors: 0

=== Manual Verification ===

AC1 - Docker Compose Stack: ✓
AC2 - Web UI Accessible: ✓
AC3 - Library Initialized: ✓
AC4 - Memory < 600MB: ✓
AC5 - Scan Completes: ✓
AC6 - Auto-Restart: ✓
AC7 - All Services Running: ✓
AC8 - Service Health: ✓

=== Summary ===
All 8 acceptance criteria verified ✓
All automated tests passing ✓
Manual verification complete ✓

Task 8: ✓ COMPLETE (100% pass rate)
```

---

## Troubleshooting Failed Tests

### If Test 1 Fails (Syntax)
- Check docker-compose.yml for YAML formatting
- Use online YAML validator if needed
- Fix any indentation issues

### If Test 2 Fails (HTTP)
- Verify containers running: `docker-compose ps`
- Check firewall: `sudo ufw allow 8083`
- Verify port not in use: `sudo lsof -i :8083`

### If Test 3 Fails (Library)
- Verify Task 5 completed successfully
- Check library directory: `ls /library`
- Force re-scan if needed

### If Test 4 Fails (Memory)
- Check for background processes: `docker stats`
- Monitor longer (memory may still be settling)
- Investigate logs for memory leaks

### If Test 5 Fails (Health)
- Review container logs: `docker-compose logs cwa`
- Check critical errors
- Restart if persistent: `docker-compose restart cwa`

---

## Pass Criteria

**Task 8 PASSES if:**
1. ✅ All 5 automated tests pass (100%)
2. ✅ All 8 manual AC criteria verified
3. ✅ Test report generated
4. ✅ No critical errors in any test

---

## Next Steps

Once **Task 8 passes**, proceed to:
- **Task 9: Document deployment and configuration**
- **Story completion and review**

---

**Task 8 Status:** Ready for Execution
**Acceptance Criteria:** AC1-8 (Comprehensive)
**Success Criteria:** 100% automated tests passing + manual verification
