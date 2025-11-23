# Handles database queries for the research system
# Federation demonstrated through: Papers DB + Citation API + LLM processing
import psycopg2
import os
from typing import List, Dict, Any, Optional, Tuple
from .config import PAPERS_DB_CONFIG

def get_database_connection():
    """Get database connection for papers database."""
    try:
        conn = psycopg2.connect(
            dbname=PAPERS_DB_CONFIG["dbname"],
            user=PAPERS_DB_CONFIG["user"],
            password=PAPERS_DB_CONFIG["password"],
            host=PAPERS_DB_CONFIG["host"],
            port=PAPERS_DB_CONFIG["port"]
        )
        return conn
    except Exception as e:
        print(f"Failed to connect to papers database: {e}")
        return None

def query_papers_db(sql: str) -> List[Tuple]:
    """Query the papers database."""
    conn = get_database_connection()
    if not conn:
        return []
    
    try:
        cur = conn.cursor()
        cur.execute(sql)
        results = cur.fetchall()
        cur.close()
        conn.close()
        return results
    except Exception as e:
        print(f"Error querying papers database: {e}")
        if conn:
            conn.close()
        return []

# Backward compatibility
def get_config():
    """Get database configuration from environment or defaults"""
    return {
        "papers_db": PAPERS_DB_CONFIG
    }