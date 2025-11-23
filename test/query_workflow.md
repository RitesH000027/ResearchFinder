ResearchFinder Query Processing Workflow
==========================================

This document explains how a user query flows through the ResearchFinder system step by step.

STEP 1: Query Entry (run_research_query.py)
-------------------------------------------
- User enters natural language query via command line
- Entry point script captures the query and passes to main coordinator
- Example: "most cited neural network papers published after 2020"

STEP 2: Query Parsing (query_parser.py)
---------------------------------------
- Extracts structured components from natural language
- Identifies: topics, year filters, citation priority, analysis requests
- Determines if this is a citation-focused query or regular search
- Sets flags for downstream processing

STEP 3: AI vs Pattern Decision (main.py)
----------------------------------------
- Checks if Groq API key is available and working
- If AI available: sends to llm_parser.py
- If AI unavailable: uses pattern-based approach in sql_builder.py

STEP 4A: AI SQL Generation (llm_parser.py)
------------------------------------------
- Sends structured prompt to Groq LLM API
- LLM generates PostgreSQL SELECT statement
- Validates SQL syntax and structure
- Falls back to pattern matching if AI fails

STEP 4B: Pattern-Based SQL (sql_builder.py)
-------------------------------------------
- Uses predefined patterns to match query components
- Builds SQL using ILIKE conditions for text search
- Handles date filtering, citation sorting, limits
- Reliable fallback when AI is unavailable

STEP 5: Database Execution (federated_engine.py)
------------------------------------------------
- Connects to primary PostgreSQL database (opencitations_meta)
- Executes generated SQL query against 76.3M paper records
- Returns raw result set with paper metadata
- Handles connection pooling and error recovery

STEP 6: Citation Enhancement (citation_analysis.py)
---------------------------------------------------
- Takes paper IDs from database results
- Converts ID format: meta:br/xxxxx → omid:br/xxxxx
- Makes HTTP requests to remote citation API
- Retrieves citation counts for each paper

STEP 7: Remote API Call (citation_server.py - on remote machine)
----------------------------------------------------------------------
- Receives citation lookup requests via REST API
- Queries remote PostgreSQL database (4.9M citations)
- Returns citation data including counts and citing papers
- Handles bulk requests for efficiency

STEP 8: Result Merging (main.py)
--------------------------------
- Combines paper metadata with citation data
- Sorts results by citation count if citation-priority query
- Creates enriched paper objects with all metadata
- Prepares data for analysis phase

STEP 9: AI Analysis (llm_postprocess.py)
----------------------------------------
- Sends paper titles and metadata to Groq LLM
- Requests comprehensive research analysis
- Gets insights on trends, methodologies, innovations
- Falls back to local analysis if AI unavailable

STEP 9B: Local Analysis Fallback (local_summarizer.py)
------------------------------------------------------
- Performs keyword extraction and frequency analysis
- Identifies research themes and publication patterns
- Generates basic statistical summaries
- Used when AI API is unavailable

STEP 10: Final Formatting (results_processor.py)
------------------------------------------------
- Formats results for terminal display
- Creates summary statistics (total papers, citations, years)
- Generates venue analysis and publication trends
- Outputs professional research report format

STEP 11: Output Display (main.py)
---------------------------------
- Prints formatted results to terminal
- Shows paper titles, authors, dates, citation counts
- Displays AI-generated research analysis
- Provides comprehensive statistics summary

ERROR HANDLING & FALLBACKS
==========================

The system includes multiple fallback mechanisms:

1. AI Unavailable → Pattern-based SQL generation
2. Citation API Down → Continue with paper data only  
3. Database Errors → Retry logic with exponential backoff
4. Invalid Queries → Intelligent error messages
5. Network Issues → Local processing where possible

PERFORMANCE OPTIMIZATIONS
=========================

1. Connection Pooling: Reuses database connections
2. Bulk Citation Queries: Reduces API call overhead
3. Query Limits: Prevents excessive result sets
4. Caching: Stores frequent query results
5. Materialized Views: Pre-computed citation counts

SYSTEM ARCHITECTURE
===================

Primary Machine:
- Main ResearchFinder application
- PostgreSQL database with 76.3M papers
- AI processing and analysis

Remote Machine: 
- Citation API server (Flask)
- PostgreSQL database with 4.9M citations
- RESTful citation lookup service

Network Communication:
- HTTP API calls between machines
- JSON data exchange format
- Error handling for network failures

This workflow ensures robust, scalable research query processing with professional-grade analysis capabilities.