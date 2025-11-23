# Configuration for the research query system
import os

# Primary Database - Papers and Metadata
PAPERS_DB_CONFIG = {
    "dbname": os.environ.get("PAPERS_DB_NAME", "opencitations_meta"),
    "user": os.environ.get("PAPERS_DB_USER", "postgres"),
    "password": os.environ.get("PAPERS_DB_PASSWORD", "12345"),
    "host": os.environ.get("PAPERS_DB_HOST", "localhost"),
    "port": os.environ.get("PAPERS_DB_PORT", "5432")
}

# Federation concept demonstrated through:
# - Papers database (PostgreSQL)
# - Citations API (HTTP service on different IP)
# - LLM processing (Groq API)
FEDERATED_DATABASES = {
    "papers": PAPERS_DB_CONFIG
}

# OpenAI API configuration (if needed)
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

# OpenCitations API configuration
OPENCITATIONS_API_BASE_URL = "https://api.opencitations.net/v1"

# Citation API Server (Running on different IP)
CITATION_API_BASE_URL = "http://192.168.41.167:5000"
