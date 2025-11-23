# Federated Database Setup Guide

This guide explains how to set up the federated database system that runs across multiple IP addresses as required by the professor's guidelines.

## Overview

The ResearchFinder system now supports **true database federation** across multiple IP addresses:

1. **Primary Database (localhost)**: Papers and metadata
2. **Citations Database (192.168.1.100)**: Citation analysis and impact metrics  
3. **Authors Database (192.168.1.101)**: Author and venue information

## Database Schema Requirements

### 1. Primary Database - Papers (localhost)
```sql
CREATE TABLE papers (
    id TEXT PRIMARY KEY,
    title TEXT,
    author TEXT,
    pub_date DATE,
    venue TEXT,
    type TEXT
);
```

### 2. Citations Database (192.168.1.100) 
```sql
CREATE TABLE citations (
    paper_id TEXT,
    citing_paper_id TEXT, 
    citation_count INTEGER,
    impact_factor DECIMAL,
    PRIMARY KEY (paper_id, citing_paper_id)
);
```

### 3. Authors Database (192.168.1.101)
```sql
CREATE TABLE authors (
    author_id SERIAL PRIMARY KEY,
    author_name TEXT,
    affiliation TEXT,
    h_index INTEGER
);
```

## Environment Configuration

Update your `.env` file with the IP addresses of your federated databases:

```bash
# Primary Database (Papers & Metadata)
PAPERS_DB_HOST=localhost

# Remote Database (Citations - Different IP)
CITATIONS_DB_HOST=192.168.1.100

# Tertiary Database (Authors - Different IP)  
AUTHORS_DB_HOST=192.168.1.101
```

## Testing Federated Connectivity

Run the connectivity test to verify all databases are accessible:

```python
from federated_query.federated_engine import test_federated_connectivity
test_federated_connectivity()
```

## How It Works

1. **Query Decomposition**: The system analyzes the natural language query and shows decomposition results
2. **Prompt Rewriting**: Decomposed query components are rewritten into specialized LLM prompts  
3. **Federated Execution**: SQL queries are executed in parallel across multiple databases on different IPs
4. **Result Integration**: Results from all databases are combined and analyzed using LLM

## Example Usage

```python
# This will query all three databases and integrate results
python -m federated_query.main "find machine learning papers with citations from 2020"
```

The system will:
- Query papers database on localhost
- Query citations database on 192.168.1.100  
- Query authors database on 192.168.1.101
- Integrate all results using rewritten LLM prompts

## Network Requirements

- All database servers must be accessible from the main application server
- Ensure firewalls allow PostgreSQL connections (port 5432) between servers
- Configure PostgreSQL to accept remote connections in `postgresql.conf` and `pg_hba.conf`

## Production Deployment

For production deployment:
1. Set up PostgreSQL instances on separate servers/VMs
2. Configure proper security (SSL, authentication)
3. Update environment variables with actual IP addresses
4. Test connectivity before running queries