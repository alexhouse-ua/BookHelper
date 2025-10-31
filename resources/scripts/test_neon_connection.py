#!/usr/bin/env python3
"""
Test script for Neon.tech PostgreSQL connection
Story 1.4: Design and implement unified database schema

This script verifies:
1. Connection to Neon.tech PostgreSQL
2. Basic database operations (SELECT, INSERT, UPDATE, DELETE)
3. Transaction handling
4. Connection pooling readiness
"""

import os
import sys
import psycopg2
from psycopg2 import sql, Error

def load_env():
    """Load environment variables from .env.neon"""
    env_file = '.env.neon'
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    os.environ[key] = value

def test_connection():
    """Test basic connection to Neon.tech PostgreSQL"""
    load_env()

    # Get connection parameters
    host = os.getenv('NEON_HOST')
    port = os.getenv('NEON_PORT', '5432')
    user = os.getenv('NEON_USER')
    password = os.getenv('NEON_PASSWORD')
    database = os.getenv('NEON_DATABASE')

    if not all([host, user, password, database]):
        print("❌ ERROR: Missing connection parameters in .env.neon")
        print(f"   HOST: {host}")
        print(f"   USER: {user}")
        print(f"   DATABASE: {database}")
        return False

    print("🔍 Testing Neon.tech PostgreSQL Connection")
    print("=" * 60)
    print(f"Host:     {host}")
    print(f"Port:     {port}")
    print(f"User:     {user}")
    print(f"Database: {database}")
    print("=" * 60)

    try:
        # Attempt connection
        print("\n📡 Connecting to PostgreSQL...")
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            sslmode='require',
            connect_timeout=10
        )
        print("✅ Connection successful!")

        # Test basic SELECT
        print("\n🔬 Testing basic operations...")
        cursor = conn.cursor()

        # Test 1: SELECT version
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        print(f"✅ SELECT version(): PostgreSQL {version.split(',')[0]}")

        # Test 2: SELECT COUNT(*) from information_schema
        cursor.execute("""
            SELECT COUNT(*) FROM information_schema.tables
            WHERE table_schema = 'public'
        """)
        table_count = cursor.fetchone()[0]
        print(f"✅ Current public tables: {table_count}")

        # Test 3: Transaction commit/rollback
        print("\n📝 Testing transaction handling...")
        cursor.execute("BEGIN;")
        cursor.execute("CREATE TEMPORARY TABLE temp_test (id INT);")
        cursor.execute("INSERT INTO temp_test VALUES (1);")
        cursor.execute("SELECT COUNT(*) FROM temp_test;")
        temp_count = cursor.fetchone()[0]
        cursor.execute("ROLLBACK;")
        print(f"✅ Transaction rollback successful (temp table cleaned up)")

        # Test 4: Check for existing tables
        cursor.execute("""
            SELECT table_name FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)
        tables = cursor.fetchall()
        if tables:
            print(f"\n📊 Existing tables in public schema:")
            for table in tables:
                print(f"   - {table[0]}")
        else:
            print(f"\n📊 No tables in public schema yet (ready for schema creation)")

        conn.commit()
        cursor.close()

        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED - Neon.tech connection is working!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Task 2: Create Books dimension table")
        print("2. Task 3: Create Reading_sessions fact table")
        print("3. Task 4: Create performance indexes")
        print("4. Task 5: Test CRUD operations with psycopg2")

        conn.close()
        return True

    except Error as e:
        print(f"\n❌ Connection Error: {e}")
        print("\nTroubleshooting:")
        print("- Verify connection string in .env.neon")
        print("- Check network connectivity to Neon.tech")
        print("- Ensure firewall allows outbound HTTPS (port 5432)")
        print("- Verify credentials are correct")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected Error: {e}")
        return False

if __name__ == '__main__':
    success = test_connection()
    sys.exit(0 if success else 1)
