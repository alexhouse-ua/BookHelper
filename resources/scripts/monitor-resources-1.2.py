#!/usr/bin/env python3
"""
Resource monitoring script for Story 1.2 validation

Monitors Calibre-Web-Automated (CWA) container resource usage during 1-week
incremental ingestion validation using docker stats API (per Docker v1.24+ docs).

Collects every 5 minutes:
- Timestamp (ISO 8601)
- Operation type (idle, import, metadata_fetch, library_scan) from CWA logs
- Memory usage (MB) from docker stats
- CPU usage (%) from docker stats
- Notes field for manual observations

Output: CSV file at /tmp/cwa-metrics-1.2.csv

Performance Targets (per Story 1.2 ACs):
- Idle memory: <600 MB
- Peak memory during metadata fetch: <1 GB
- Metadata enrichment: <30 seconds per book
- Library scan (~20-50 books): <2 minutes
- No crashes or OOM errors
"""

import subprocess
import time
import csv
import sys
from datetime import datetime
from pathlib import Path

# Configuration
CONTAINER_NAME = "calibre-web-automated"
INTERVAL_SECONDS = 300  # 5 minutes
OUTPUT_FILE = "/tmp/cwa-metrics-1.2.csv"

def get_container_stats():
    """Get container CPU and memory stats using docker stats

    Uses docker stats API per Docker documentation:
    - memory_stats: current memory usage in bytes (converted to MB)
    - cpu_stats: percentage of CPU used relative to system limits

    Output format from 'docker stats --no-stream':
    MEMORY        CPU%
    512MiB / 1.465GiB    25.5%
    """
    try:
        result = subprocess.run(
            ["docker", "stats", CONTAINER_NAME, "--no-stream", "--format",
             "{{.MemUsage}}\t{{.CPUPerc}}"],
            capture_output=True,
            text=True,
            check=True
        )

        # Parse output: "512MiB / 1.465GiB    25.5%"
        parts = result.stdout.strip().split('\t')

        # Memory: "512MiB / 1.465GiB" (current usage / limit)
        mem_usage = parts[0].split('/')[0].strip()
        mem_mb = parse_memory_to_mb(mem_usage)

        # CPU: "25.5%" (percentage of available CPU)
        cpu_pct = float(parts[1].strip().rstrip('%'))

        return mem_mb, cpu_pct

    except (subprocess.CalledProcessError, IndexError, ValueError) as e:
        print(f"Error reading container stats: {e}", file=sys.stderr)
        return None, None

def parse_memory_to_mb(mem_str):
    """Convert memory string from docker stats to MB

    Handles formats: GiB (binary), MiB (binary), GB (decimal), MB (decimal)
    Per Docker documentation, uses binary units (GiB, MiB) by default.

    Args:
        mem_str: Memory string like '512MiB', '1.5GiB', '1GB', '512MB'

    Returns:
        Memory in MB as float
    """
    mem_str = mem_str.strip()

    if 'GiB' in mem_str:
        value = float(mem_str.rstrip('GiB'))
        return value * 1024  # Binary gigabyte to MB
    elif 'MiB' in mem_str:
        value = float(mem_str.rstrip('MiB'))
        return value  # Already in MB equivalent
    elif 'GB' in mem_str:
        value = float(mem_str.rstrip('GB'))
        return value * 1000  # Decimal gigabyte to MB
    elif 'MB' in mem_str:
        value = float(mem_str.rstrip('MB'))
        return value  # Already in MB
    else:
        return 0

def get_container_logs_last_line():
    """Get last line from container logs to detect operations"""
    try:
        result = subprocess.run(
            ["docker", "logs", "--tail", "1", CONTAINER_NAME],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return ""

def detect_operation(log_line):
    """Detect current operation from logs"""
    if not log_line:
        return "idle"

    log_lower = log_line.lower()

    if "import" in log_lower or "ingest" in log_lower:
        return "import"
    elif "metadata" in log_lower or "enrichment" in log_lower:
        return "metadata_fetch"
    elif "scan" in log_lower or "library scan" in log_lower:
        return "library_scan"
    else:
        return "idle"

def main():
    """Main monitoring loop"""
    output_path = Path(OUTPUT_FILE)

    # Initialize CSV file
    write_header = not output_path.exists()

    print(f"Starting CWA monitoring: {CONTAINER_NAME}")
    print(f"Output: {OUTPUT_FILE}")
    print(f"Interval: {INTERVAL_SECONDS}s")
    print("Press Ctrl+C to stop\n")

    with open(OUTPUT_FILE, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)

        if write_header:
            writer.writerow([
                'timestamp',
                'operation',
                'memory_mb',
                'cpu_percent',
                'notes'
            ])

        try:
            while True:
                timestamp = datetime.now().isoformat()
                mem_mb, cpu_pct = get_container_stats()

                if mem_mb is not None:
                    log_line = get_container_logs_last_line()
                    operation = detect_operation(log_line)

                    writer.writerow([
                        timestamp,
                        operation,
                        f"{mem_mb:.1f}",
                        f"{cpu_pct:.1f}",
                        ""
                    ])

                    csvfile.flush()

                    print(f"{timestamp} | {operation:15} | {mem_mb:7.1f} MB | {cpu_pct:5.1f}% CPU")

                time.sleep(INTERVAL_SECONDS)

        except KeyboardInterrupt:
            print("\n\nMonitoring stopped by user")
            print(f"Data saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
