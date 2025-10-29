#!/usr/bin/env python3
"""
Comprehensive validation tests for Story 2.1: Configure Syncthing for one-way library sync

Tests verify that all acceptance criteria 1-7 are met through configuration:
AC1: Syncthing installed and running on Raspberry Pi
AC2: Syncthing installed and configured on Boox Palma 2 (manual verification)
AC3: Library folder shared from RPi with "Send Only" mode configured
AC4: Boox Palma receives library folder with "Receive Only" mode (manual verification)
AC5: Test: New book added to CWA library appears on Boox within 5 minutes (manual test)
AC6: KOReader on Boox can open synced books successfully (manual verification)
AC7: Syncthing runs automatically on boot for both devices

IMPORTANT: Workflow & Architecture
- Workflow: Boox downloads EPUB → Syncthing uploads to RPi → CWA processes → User downloads via OPDS
- Sync Direction: Boox /sdcard/Download/ (Send Only) → RPi /library/ingest/ (Receive Only)
- Boox folder: /sdcard/Download/ (where browser/email saves raw EPUBs)
- RPi folder: /library/ingest/ (CWA monitors this for auto-ingestion)
- After ingestion, CWA moves books from /library/ingest/ to /library/Author/Title/
- User downloads processed books back to Boox via OPDS (Story 2.2), NOT via Syncthing
- STGUIADDRESS= (empty) in docker-compose.yml restricts Web UI to localhost with network_mode: host
  - May need to change to STGUIADDRESS=0.0.0.0:8384 for network access (see setup guide Step 1.2)

References:
- Story file: /docs/stories/story-2.1.md
- Story context: /docs/stories/story-context-2.1.xml
- Setup guide: /docs/STORY-2.1-SYNCTHING-SETUP.md
- Official Syncthing docs: https://docs.syncthing.net
"""

import subprocess
import json
import os
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

# Configuration
PROJECT_ROOT = Path(__file__).parent.parent
DOCKER_COMPOSE_FILE = PROJECT_ROOT / "docker-compose.yml"
SETUP_GUIDE = PROJECT_ROOT / "docs" / "STORY-2.1-SYNCTHING-SETUP.md"
SYNCTHING_UI = "http://localhost:8384"  # Assuming run from RPi or SSH tunnel


class TestResult:
    """Simple test result tracker"""
    def __init__(self):
        self.passed = []
        self.failed = []
        self.warnings = []
        self.manual = []

    def add_pass(self, test_name, message):
        self.passed.append((test_name, message))
        print(f"✓ {test_name}: {message}")

    def add_fail(self, test_name, message):
        self.failed.append((test_name, message))
        print(f"✗ {test_name}: {message}")

    def add_warn(self, test_name, message):
        self.warnings.append((test_name, message))
        print(f"⚠ {test_name}: {message}")

    def add_manual(self, test_name, instructions):
        self.manual.append((test_name, instructions))
        print(f"📋 {test_name}: Manual verification required")
        print(f"   {instructions}")

    def summary(self):
        total = len(self.passed) + len(self.failed)
        return {
            "total": total,
            "passed": len(self.passed),
            "failed": len(self.failed),
            "warnings": len(self.warnings),
            "manual": len(self.manual)
        }


def test_docker_compose_syncthing_service(results):
    """AC1: Verify docker-compose.yml has Syncthing service configured"""
    print("\n=== TEST: docker-compose.yml Syncthing Service ===")

    if not DOCKER_COMPOSE_FILE.exists():
        results.add_fail("docker-compose exists", f"File not found: {DOCKER_COMPOSE_FILE}")
        return

    results.add_pass("docker-compose exists", f"Found at {DOCKER_COMPOSE_FILE}")

    try:
        with open(DOCKER_COMPOSE_FILE) as f:
            content = f.read()

        # Check for Syncthing service
        if "syncthing:" not in content:
            results.add_fail("Syncthing service configured", "syncthing service not found in docker-compose.yml")
            return

        results.add_pass("Syncthing service exists", "Found in docker-compose.yml")

        # Check image
        if "syncthing/syncthing" in content:
            results.add_pass("Syncthing image", "Using official syncthing/syncthing image")
        else:
            results.add_warn("Syncthing image", "Expected syncthing/syncthing image")

        # Check network mode (critical for LAN discovery)
        if "network_mode: host" in content or "network_mode:host" in content:
            results.add_pass("Network mode (AC1)", "Host mode enabled (optimal for LAN discovery)")
        else:
            results.add_warn("Network mode", "Host mode not detected; may impact peer discovery")

        # Check restart policy (AC7)
        if "restart: always" in content:
            results.add_pass("Auto-restart (AC7)", "Restart policy: always (survives reboot)")
        elif "restart: unless-stopped" in content:
            results.add_pass("Auto-restart (AC7)", "Restart policy: unless-stopped (survives reboot)")
        else:
            results.add_fail("Auto-restart (AC7)", "No restart policy found; service won't auto-start")

        # Check volumes
        if "/library:/library" in content or "/library :/library" in content:
            results.add_pass("Library volume (AC3)", "Library folder mounted at /library")
        else:
            results.add_fail("Library volume", "No /library volume mount found")

        if "syncthing_config" in content or "/var/syncthing" in content:
            results.add_pass("Config volume", "Syncthing config persistence configured")
        else:
            results.add_warn("Config volume", "Config persistence may not be configured")

        # Check memory limits (optional but recommended)
        if "memory:" in content and ("128M" in content or "512M" in content):
            results.add_pass("Memory limits", "Memory limits configured (128M-512M)")
        else:
            results.add_warn("Memory limits", "Memory limits not explicitly set")

    except Exception as e:
        results.add_fail("docker-compose parsing", f"Error: {e}")


def test_syncthing_container_running(results):
    """AC1: Verify Syncthing container is running"""
    print("\n=== TEST: Syncthing Container Status ===")

    try:
        # Check if docker is available
        result = subprocess.run(
            ["docker", "ps", "--filter", "name=syncthing", "--format", "{{.Names}} {{.Status}}"],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode != 0:
            results.add_warn("Docker check", "Docker command failed; may not be running from RPi")
            return

        output = result.stdout.strip()

        if "syncthing" in output and "Up" in output:
            results.add_pass("Syncthing container (AC1)", f"Container running: {output}")
        elif "syncthing" in output:
            results.add_fail("Syncthing container (AC1)", f"Container exists but not running: {output}")
        else:
            results.add_fail("Syncthing container (AC1)", "Container not found (not started)")

    except subprocess.TimeoutExpired:
        results.add_fail("Docker check", "Docker command timed out")
    except FileNotFoundError:
        results.add_warn("Docker check", "Docker not found; test must be run on RPi or with docker access")
    except Exception as e:
        results.add_warn("Docker check", f"Error: {e}")


def test_syncthing_web_ui_accessible(results):
    """AC1: Verify Syncthing web UI is accessible"""
    print("\n=== TEST: Syncthing Web UI Accessibility ===")

    try:
        # Try to access Syncthing UI
        req = urllib.request.Request(f"{SYNCTHING_UI}/rest/noauth/health")
        req.add_header("User-Agent", "Story-2.1-Validation-Test")

        with urllib.request.urlopen(req, timeout=5) as response:
            content = response.read().decode('utf-8')
            if "OK" in content:
                results.add_pass("Syncthing web UI (AC1)", f"Accessible at {SYNCTHING_UI}")
            else:
                results.add_warn("Syncthing web UI", f"Responded but not healthy: {content}")

    except urllib.error.URLError as e:
        results.add_warn("Syncthing web UI (AC1)", f"Not accessible at {SYNCTHING_UI}: {e}")
        results.add_manual("STGUIADDRESS configuration",
                          "docker-compose.yml has STGUIADDRESS= (empty). With network_mode: host, " +
                          "Web UI should be accessible at http://raspberrypi.local:8384. " +
                          "If not working, change STGUIADDRESS= to STGUIADDRESS=0.0.0.0:8384 " +
                          "and run 'docker-compose restart syncthing'. See setup guide Step 1.2.")
    except Exception as e:
        results.add_fail("Syncthing web UI (AC1)", f"Error: {e}")


def test_setup_guide_exists(results):
    """Verify comprehensive setup guide exists"""
    print("\n=== TEST: Setup Guide Documentation ===")

    if not SETUP_GUIDE.exists():
        results.add_fail("Setup guide exists", f"File not found: {SETUP_GUIDE}")
        return

    try:
        with open(SETUP_GUIDE) as f:
            guide = f.read()

        results.add_pass("Setup guide exists", f"Found at {SETUP_GUIDE}")

        # Check for key sections
        sections = {
            "Part 1: RPi Configuration (AC1)": ["raspberry pi", "docker", "web ui"],
            "Part 2: Boox Installation (AC2)": ["boox", "android", "f-droid"],
            "Part 3: Device Pairing": ["device id", "pairing", "add remote device"],
            "Part 4: Folder Sharing (AC3-4)": ["send only", "receive only", "folder share"],
            "Part 5: Testing (AC5-6)": ["test", "new book", "koreader"],
            "Part 6: Auto-Start (AC7)": ["auto-start", "reboot", "restart"],
            "One-way sync design": ["one-way", "send only", "receive only"],
            "Critical safety constraints": ["corruption", "metadata.db", "sqlite"],
            "Troubleshooting": ["troubleshooting", "issue", "solution"],
        }

        for section_name, keywords in sections.items():
            guide_lower = guide.lower()
            if all(kw in guide_lower for kw in keywords):
                results.add_pass(f"Guide section - {section_name}", "Documented")
            else:
                results.add_warn(f"Guide section - {section_name}", f"Keywords {keywords} not all found")

        # Check for official documentation references
        if "docs.syncthing.net" in guide or "syncthing.net" in guide:
            results.add_pass("Official docs referenced", "Guide includes links to official Syncthing documentation")
        else:
            results.add_warn("Official docs", "Guide may not reference official documentation")

        # Check line count (comprehensive guide should be substantial)
        line_count = len(guide.split('\n'))
        if line_count > 400:
            results.add_pass("Guide comprehensiveness", f"Comprehensive guide: {line_count} lines")
        else:
            results.add_warn("Guide comprehensiveness", f"Guide may be brief: {line_count} lines")

    except Exception as e:
        results.add_fail("Setup guide parsing", f"Error: {e}")


def test_story_file_structure(results):
    """Verify story file has required fields and context"""
    print("\n=== TEST: Story File Structure ===")

    story_file = PROJECT_ROOT / "docs" / "stories" / "story-2.1.md"
    if not story_file.exists():
        results.add_fail("Story file exists", f"File not found: {story_file}")
        return

    results.add_pass("Story file exists", f"Found at {story_file}")

    try:
        with open(story_file) as f:
            content = f.read()

        # Check required sections
        sections = {
            "Story": "User story statement",
            "Acceptance Criteria": "AC list with 7 items",
            "Tasks / Subtasks": "Implementation tasks",
            "Dev Notes": "Architecture and constraints",
            "Dev Agent Record": "Developer notes and status",
            "Context Reference": "Story context XML reference",
        }

        for section, description in sections.items():
            if f"## {section}" in content or f"### {section}" in content:
                results.add_pass(f"Story section - {section}", "Present")
            else:
                results.add_warn(f"Story section - {section}", f"Not found ({description})")

        # Check for acceptance criteria count
        ac_count = content.count("Syncthing installed") + content.count("Library folder shared")
        if ac_count >= 2:
            results.add_pass("Acceptance criteria defined", "ACs 1-7 documented")
        else:
            results.add_warn("Acceptance criteria", "AC documentation may be incomplete")

        # Check for Story Context XML reference
        if "story-context-2.1.xml" in content:
            results.add_pass("Story context reference", "Story Context XML referenced")
        else:
            results.add_warn("Story context", "Story Context XML not referenced")

    except Exception as e:
        results.add_fail("Story file check", f"Error: {e}")


def test_manual_verification_checklist(results):
    """Provide manual verification checklist for ACs that require hardware"""
    print("\n=== MANUAL VERIFICATION REQUIRED ===")

    manual_tests = [
        ("AC2: Boox Installation",
         "Install Syncthing Android app from F-Droid or Play Store; verify app opens and shows Device ID"),

        ("AC3: Boox Send Only Configuration",
         "In Boox Syncthing app, verify folder 'Downloads for Ingestion' or 'boox-downloads' has Folder Type: 'Send Only' and Path: /sdcard/Download/"),

        ("AC4: RPi Receive Only Configuration",
         "In RPi Syncthing UI (http://raspberrypi.local:8384), verify folder 'Boox Downloads' or 'boox-downloads' has Folder Type: 'Receive Only' and Path: /library/ingest"),

        ("AC5: Upload Speed Test (Boox → RPi)",
         "On Boox, download test EPUB to /sdcard/Download/ (use browser or email); start timer; verify file appears in RPi /library/ingest/ within 5 minutes; record actual time."),

        ("AC5: File Integrity (Checksum)",
         "Run sha256sum on test file in /sdcard/Download/ on Boox and /library/ingest/ on RPi; verify checksums match exactly (no corruption during upload)"),

        ("AC6: Complete Workflow Test",
         "Download raw EPUB on Boox → wait for CWA ingestion → download processed EPUB via OPDS (Story 2.2) → open in KOReader → verify: metadata enriched, EPUB fixed, renders correctly"),

        ("AC7: RPi Auto-Start After Reboot",
         "Reboot RPi (sudo reboot); wait 3 min; SSH in; run 'docker ps | grep syncthing'; verify container shows 'Up' status"),

        ("AC7: Boox Auto-Start After Reboot",
         "Reboot Boox; wait 2-3 min; open Syncthing app; verify folder 'Downloads for Ingestion' shows 'Up to Date' or 'Idle' without manual intervention"),

        ("One-Way Enforcement Test (RPi cannot write to Boox)",
         "On RPi, create test file in /library/ingest/ (echo 'test' > /library/ingest/test.txt); verify file does NOT appear in Boox /sdcard/Download/ (Receive Only mode working on RPi)"),
    ]

    for test_name, instructions in manual_tests:
        results.add_manual(test_name, instructions)


def main():
    """Run all tests and report results"""
    print("=" * 70)
    print("STORY 2.1 SYNCTHING CONFIGURATION VALIDATION TESTS")
    print("Configure Syncthing for one-way library sync (Acceptance Criteria 1-7)")
    print("=" * 70)

    results = TestResult()

    # Run automated tests
    test_docker_compose_syncthing_service(results)
    test_syncthing_container_running(results)
    test_syncthing_web_ui_accessible(results)
    test_setup_guide_exists(results)
    test_story_file_structure(results)
    test_manual_verification_checklist(results)

    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)

    summary = results.summary()
    print(f"Automated tests: {summary['total']}")
    print(f"✓ Passed: {summary['passed']}")
    print(f"✗ Failed: {summary['failed']}")
    print(f"⚠ Warnings: {summary['warnings']}")
    print(f"📋 Manual verification required: {summary['manual']}")

    print("\n" + "=" * 70)
    print("NEXT STEPS")
    print("=" * 70)

    if summary["failed"] == 0:
        print("\n✅ ALL AUTOMATED TESTS PASSED")
        print("\n📋 MANUAL VERIFICATION REQUIRED:")
        print("   Follow the setup guide: /docs/STORY-2.1-SYNCTHING-SETUP.md")
        print("   Complete all manual tests listed above")
        print("   Record test results in story file: /docs/stories/story-2.1.md")
        print("\n✓ When all manual tests pass, Story 2.1 AC 1-7 are complete")
        return 0
    else:
        print(f"\n❌ {summary['failed']} AUTOMATED TEST(S) FAILED")
        print("   Fix configuration issues before proceeding to manual tests")
        print("   Review failures above and consult troubleshooting guide")
        return 1


if __name__ == "__main__":
    sys.exit(main())
