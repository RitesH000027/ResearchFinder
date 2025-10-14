# Handles database queries for the research system
import psycopg2
import os
from typing import List, Dict, Any, Optional

def get_config():
    """Get database configuration from environment or defaults"""
    return {
        "papers_db": {
            "dbname": os.environ.get("PAPERS_DB_NAME", "opencitations_meta"),
            "user": os.environ.get("PAPERS_DB_USER", "postgres"),
            "password": os.environ.get("PAPERS_DB_PASSWORD", "12345"),
            "host": os.environ.get("PAPERS_DB_HOST", "localhost"),
            "port": os.environ.get("PAPERS_DB_PORT", "5432")
        }
    }

def query_papers_db(sql):
    """Query the papers database (local)"""
    config = get_config()["papers_db"]
    
    try:
        conn = psycopg2.connect(
            dbname=config["dbname"],
            user=config["user"],
            password=config["password"],
            host=config["host"],
            port=config["port"]
        )
        cur = conn.cursor()
        cur.execute(sql)
        results = cur.fetchall()
        cur.close()
        conn.close()
        return results
    except Exception as e:
        print(f"Error querying papers DB: {e}")
        return []