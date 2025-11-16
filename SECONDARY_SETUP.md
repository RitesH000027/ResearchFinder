# Secondary Machine Setup Files

The following files are needed for the secondary machine (citation server) but are NOT included in the main ResearchFinder codebase to keep it clean.

## Required Files for Secondary Machine

Create these files on your secondary machine:

### 1. Citation Server (`citation_server.py`)
```python
#!/usr/bin/env python3
"""
Citation API Server for ResearchFinder Secondary Laptop
Download this file from: https://github.com/RitesH000027/ResearchFinder/releases
Or copy from the main documentation in README.md
"""
```

### 2. Citation Data Loader (`load_citations.py`)
```python
#!/usr/bin/env python3
"""
Load OpenCitations Index data into PostgreSQL database
Download OpenCitations Index dump and run this script
"""
```

### 3. Database Schema (`citation_database_schema.sql`)
```sql
-- PostgreSQL schema for citation database
CREATE TABLE citations (
    id SERIAL PRIMARY KEY,
    oci VARCHAR(255) UNIQUE,
    citing_paper_doi TEXT,
    cited_paper_doi TEXT,
    creation_date DATE,
    timespan VARCHAR(20),
    journal_citing TEXT,
    journal_cited TEXT,
    author_citing TEXT,
    author_cited TEXT
);

CREATE INDEX idx_citations_cited_doi ON citations(cited_paper_doi);
CREATE INDEX idx_citations_citing_doi ON citations(citing_paper_doi);
```

### 4. Installation Script (`install_dependencies.sh`)
```bash
#!/bin/bash
# Install PostgreSQL and Python dependencies for citation server
sudo apt update
sudo apt install postgresql postgresql-contrib python3-pip
pip3 install flask psycopg2-binary requests
```

## Setup Instructions

1. **Set up PostgreSQL database**
2. **Download OpenCitations Index data** 
3. **Run the citation data loader**
4. **Start the citation server**
5. **Update the IP address in main system**

See the main README.md for complete setup instructions.

## Note

These files are maintained separately to keep the main ResearchFinder codebase clean and focused on the primary functionality. The secondary machine setup is documented in the README.md file.