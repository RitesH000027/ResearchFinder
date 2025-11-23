# Quick Federated Database Setup for Demo

## Option 1: Multiple PostgreSQL Instances on Different Ports (Localhost)

### 1. Create Additional PostgreSQL Instances

```powershell
# Install PostgreSQL if not already installed
# Then create additional instances on different ports

# Create second instance (Citations DB) on port 5433
pg_ctl init -D "C:\PostgreSQL\data_citations" 
# Edit postgresql.conf to set port = 5433

# Create third instance (Authors DB) on port 5434  
pg_ctl init -D "C:\PostgreSQL\data_authors"
# Edit postgresql.conf to set port = 5434
```

### 2. Start the Additional Instances

```powershell
# Start citations database on port 5433
pg_ctl start -D "C:\PostgreSQL\data_citations"

# Start authors database on port 5434
pg_ctl start -D "C:\PostgreSQL\data_authors"
```

### 3. Create the Database Schemas

```sql
-- Connect to citations DB (port 5433)
CREATE DATABASE citations_db;
\c citations_db;

CREATE TABLE citations (
    paper_id TEXT,
    citing_paper_id TEXT, 
    citation_count INTEGER,
    impact_factor DECIMAL,
    PRIMARY KEY (paper_id, citing_paper_id)
);

-- Connect to authors DB (port 5434)  
CREATE DATABASE authors_venues_db;
\c authors_venues_db;

CREATE TABLE authors (
    author_id SERIAL PRIMARY KEY,
    author_name TEXT,
    affiliation TEXT,
    h_index INTEGER
);
```

### 4. Update Environment Variables

```bash
# Primary Database (Papers)
PAPERS_DB_HOST=localhost
PAPERS_DB_PORT=5432

# Citations Database (Different Port)
CITATIONS_DB_HOST=localhost
CITATIONS_DB_PORT=5433

# Authors Database (Different Port)
AUTHORS_DB_HOST=localhost  
AUTHORS_DB_PORT=5434
```

## Option 2: Use Remote Machine (Real Federation)

### 1. On Remote Machine (192.168.41.167):
```powershell
# Install PostgreSQL
# Create citations_db and authors_venues_db
# Configure to accept remote connections
```

### 2. Configure PostgreSQL for Remote Access:
```ini
# postgresql.conf
listen_addresses = '*'
port = 5432

# pg_hba.conf  
host    all    all    192.168.0.0/16    md5
```

### 3. Update Environment Variables:
```bash
CITATIONS_DB_HOST=192.168.41.167
AUTHORS_DB_HOST=192.168.41.167
```

## Option 3: Demo Mode (Skip Federation)

Update the code to skip federated databases for demo:

```python
# In federated_engine.py - add demo mode
def federate_research_query(paper_sql: str, include_citations: bool = False, include_authors: bool = False, demo_mode: bool = True):
    if demo_mode:
        print("🎯 Demo Mode: Using single database with federated simulation")
        # Only query papers database but simulate federation
```