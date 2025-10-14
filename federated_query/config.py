# Configuration for the research query system
import os

# Database configuration
PAPERS_DB_CONFIG = {
    "dbname": os.environ.get("PAPERS_DB_NAME", "opencitations_meta"),
    "user": os.environ.get("PAPERS_DB_USER", "postgres"),
    "password": os.environ.get("PAPERS_DB_PASSWORD", "12345"),
    "host": os.environ.get("PAPERS_DB_HOST", "localhost"),
    "port": os.environ.get("PAPERS_DB_PORT", "5432")
}

# OpenAI API configuration (if needed)
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

# OpenCitations API configuration
OPENCITATIONS_API_BASE_URL = "https://api.opencitations.net/v1"
