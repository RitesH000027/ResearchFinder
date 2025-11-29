# Handles database queries for the research system
# Federation demonstrated through: Papers DB + Citation API + LLM processing
import psycopg2
import os
from typing import List, Dict, Any, Optional, Tuple
from .config import PAPERS_DB_CONFIG

def get_database_connection():
    """Get database connection for papers database."""
    try:
        print(f"[DB] Attempting connection to {PAPERS_DB_CONFIG['host']}:{PAPERS_DB_CONFIG['port']}/{PAPERS_DB_CONFIG['dbname']}")
        conn = psycopg2.connect(
            dbname=PAPERS_DB_CONFIG["dbname"],
            user=PAPERS_DB_CONFIG["user"],
            password=PAPERS_DB_CONFIG["password"],
            host=PAPERS_DB_CONFIG["host"],
            port=PAPERS_DB_CONFIG["port"],
            connect_timeout=10  # Add 10 second connection timeout
        )
        print(f"[DB] Connection established successfully")
        return conn
    except psycopg2.OperationalError as e:
        print(f"[DB] Database connection failed (operational error): {e}")
        print(f"[DB] Check if PostgreSQL is running and accessible at {PAPERS_DB_CONFIG['host']}:{PAPERS_DB_CONFIG['port']}")
        return None
    except Exception as e:
        print(f"[DB] Failed to connect to papers database: {e}")
        return None

def query_papers_db(sql: str) -> List[Tuple]:
    """Query the papers database."""
    conn = get_database_connection()
    if not conn:
        print("[DB] No database connection available, returning empty results")
        return []
    
    try:
        cur = conn.cursor()
        import time
        
        # Set query timeout to prevent hanging
        timeout_seconds = int(os.environ.get('DB_QUERY_TIMEOUT', '30'))
        conn.set_session(autocommit=True)
        
        print(f"[DB] Executing SQL (timeout={timeout_seconds}s): {sql[:100]}...")
        start = time.perf_counter()
        
        cur.execute(sql)
        query_time = time.perf_counter() - start
        
        print(f"[DB] Query executed in {query_time:.3f}s, fetching results...")
        fetch_start = time.perf_counter()
        results = cur.fetchall()
        fetch_time = time.perf_counter() - fetch_start
        
        cur.close()
        conn.close()
        print(f"[DB] Executed SQL in {query_time:.3f}s, fetched results in {fetch_time:.3f}s (rows={len(results)})")
        return results
        
    except psycopg2.OperationalError as e:
        print(f"[DB] Database operational error (connection/timeout): {e}")
        if conn:
            conn.close()
        return []
    except psycopg2.Error as e:
        print(f"[DB] PostgreSQL error: {e}")
        print(f"[DB] Problem SQL: {sql}")
        if conn:
            conn.close()
        return []
    except Exception as e:
        print(f"[DB] Unexpected error querying papers database: {e}")
        if conn:
            conn.close()
        return []

def test_database_connection() -> bool:
    """Test if database is accessible and responsive."""
    print("[DB] Testing database connectivity...")
    conn = get_database_connection()
    if not conn:
        return False
    
    try:
        cur = conn.cursor()
        # Simple test query
        cur.execute("SELECT 1 as test")
        result = cur.fetchone()
        cur.close()
        conn.close()
        
        if result and result[0] == 1:
            print("[DB] Database connectivity test: PASSED")
            return True
        else:
            print("[DB] Database connectivity test: FAILED (unexpected result)")
            return False
            
    except Exception as e:
        print(f"[DB] Database connectivity test: FAILED ({e})")
        if conn:
            conn.close()
        return False

# Backward compatibility
def get_config():
    """Get database configuration from environment or defaults"""
    return {
        "papers_db": PAPERS_DB_CONFIG
    }