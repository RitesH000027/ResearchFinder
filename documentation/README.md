# ResearchFinder: Advanced Federated Research Query System

## Project Overview

ResearchFinder is a sophisticated federated research system that combines AI-powered query processing with comprehensive citation analysis across multiple databases. It enables researchers to perform complex queries on academic papers with real-time citation data integration and intelligent analysis.

### Key Features
- **Federated Architecture**: Dual-database system (76.3M papers + 4.9M citations)
- **AI-Powered Analysis**: Groq LLM integration with local fallback systems
- **Citation Integration**: Real-time citation lookup and ranking
- **Natural Language Queries**: Convert complex research questions to SQL
- **Cross-Domain Research**: Multi-disciplinary paper discovery
- **Professional Analysis**: Comprehensive research summaries and trend analysis

---

## System Architecture

### Primary Components

1. **Main Research Database (Primary Machine)**
   - PostgreSQL database: `opencitations_meta` 
   - 76.3M research papers with metadata
   - Fields: DOI, title, author, publication date, venue, type

2. **Citation Database (Remote Machine)**
   - PostgreSQL database: `citations_db`
   - 4.9M citation relationships  
   - Real-time citation API server

3. **Federated Query Engine**
   - Natural language to SQL conversion
   - AI-powered analysis and summarization
   - Citation ranking and impact assessment

---

## Project Structure

```
ResearchFinder/
├── README.md                          # This comprehensive guide
├── requirements.txt                   # Python dependencies  
├── setup.py                          # Package installation
├── run_research_query.py             # Main entry point
├── load_opencitations_meta.py        # Database loader script
├── .gitignore                        # Git ignore patterns
│
├── federated_query/                  # Core system modules
│   ├── __init__.py                   # Package initialization
│   ├── main.py                       # Central coordinator
│   ├── config.py                     # System configuration
│   ├── query_parser.py               # Natural language parsing
│   ├── sql_builder.py                # SQL query construction
│   ├── llm_parser.py                 # AI-powered query processing
│   ├── federated_engine.py           # Database query execution
│   ├── citation_analysis.py          # Citation data integration
│   ├── llm_postprocess.py            # AI analysis and summarization
│   ├── local_summarizer.py           # Local analysis fallback
│   ├── results_processor.py          # Output formatting
│   └── user_interface.py             # Interactive query interface
│
├── test/                             # Testing suite and evaluation
│   ├── README.md                     # Testing documentation
│   ├── test_dataset.md               # Comprehensive test dataset (220 queries)
│   ├── PERFORMANCE_EVALUATION.md     # Performance metrics methodology
│   └── query_workflow.md             # Query processing analysis
│
├── frontend/                         # Web interface and visualizations
│   ├── README.md                     # Frontend documentation
│   ├── streamlit_app.py              # Main Streamlit web application
│   ├── streamlit_requirements.txt    # Frontend dependencies
│   ├── plotly_fallback.py            # Visualization fallback system
│   └── STREAMLIT_DEMO_GUIDE.md       # Demo and deployment guide
│
└── report/                           # Academic documentation
    ├── iia_main.tex                  # Research paper LaTeX source
    ├── iia.bib                       # Bibliography references
    ├── acl.sty                       # ACL conference style
    ├── acl_natbib.bst               # Bibliography style
    └── acl_lualatex.tex             # LaTeX configuration
```

---

## Setup and Installation

### Prerequisites

1. **Python 3.8+** with pip
2. **PostgreSQL 12+** (both machines)
3. **Network connectivity** between machines
4. **Groq API Key** (free at https://console.groq.com/)

### Primary Machine Setup

1. **Clone the repository:**
```bash
git clone https://github.com/RitesH000027/ResearchFinder.git
cd ResearchFinder
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables:**
```bash
# Windows PowerShell
$env:GROQ_API_KEY = "your_groq_api_key_here"
$env:PAPERS_DB_NAME = "opencitations_meta"
$env:PAPERS_DB_USER = "postgres"
$env:PAPERS_DB_PASSWORD = "your_password"
$env:PAPERS_DB_HOST = "localhost"
$env:PAPERS_DB_PORT = "5432"
```

4. **Load the research papers database:**
```bash
python load_opencitations_meta.py
```

### Citation Database Setup

**Note**: The citation database runs on a separate machine to demonstrate federated architecture. Set up requires:

1. **PostgreSQL database for citations:**
```sql
CREATE DATABASE citations_db;
CREATE USER citations_user WITH PASSWORD 'citations_password';
GRANT ALL PRIVILEGES ON DATABASE citations_db TO citations_user;
```

2. **Citation server configuration:**
   - Install Flask and PostgreSQL dependencies
   - Load OpenCitations Index CSV data
   - Configure REST API endpoints for citation retrieval

3. **Update citation server IP in citation_analysis.py:**
```python
# Update this line with your citation server's IP
CITATION_API_URL = "http://192.168.41.167:5000"  # Replace with actual IP
```

**Citation API Endpoints:**
- `GET /api/status` - Health check and database stats
- `GET /api/paper/citations/<doi>` - Get citations for a paper
- `GET /api/stats` - Comprehensive database statistics
- `POST /api/bulk/citations` - Bulk citation lookup

---

## Core Components Explained

### 1. **main.py** - Central Coordinator
The heart of the system that orchestrates the entire query processing pipeline:

```python
def run_query():
    # 1. Parse natural language query
    parsed_query = extract_query_components(query)
    
    # 2. Generate SQL using AI or pattern matching
    llm_parsed = parse_query_with_llm(query)
    structured_query = build_sql_query(parsed_query, query)
    
    # 3. Execute database query
    papers_results = query_papers_db(structured_query)
    
    # 4. Enrich with citation data
    papers_with_citations = get_citations(papers_results)
    
    # 5. AI-powered analysis
    analysis = postprocess_with_llm(papers_with_citations)
    
    return results
```

**Key Functions:**
- Query workflow coordination
- Error handling and fallbacks
- Result formatting and display
- Citation prioritization logic

### 2. **query_parser.py** - Natural Language Processing
Extracts structured components from natural language queries:

```python
def extract_query_components(query):
    components = {
        'topic': extract_research_topics(query),
        'year': extract_year_filter(query),
        'citation_priority': detect_citation_focus(query),
        'want_summary': detect_analysis_request(query),
        'specific_paper_lookup': detect_specific_paper(query)
    }
    return components
```

**Features:**
- Keyword extraction and matching
- Temporal constraint detection
- Citation analysis priority detection
- Research domain classification

### 3. **llm_parser.py** - AI Query Processing
Converts natural language to SQL using Groq AI:

```python
def parse_query_with_llm(query):
    """Convert natural language query to SQL using Groq AI"""
    prompt = create_sql_generation_prompt(query)
    
    response = groq_client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.1-8b-instant",
        temperature=0.1,
        max_tokens=1000
    )
    
    return extract_sql_from_response(response)
```

**Capabilities:**
- Advanced SQL generation
- Query optimization
- Error handling and retries
- Pattern-based fallback

### 4. **citation_analysis.py** - Citation Integration
Manages real-time citation data retrieval and ranking:

```python
class CitationClient:
    def get_citations_for_paper(self, paper_id):
        # Convert ID format: meta:br/xxx -> omid:br/xxx
        omid = self.convert_meta_to_omid(paper_id)
        
        # Query citation API
        response = requests.get(f"{CITATION_API_URL}/api/paper/citations/{omid}")
        
        return self.process_citation_data(response.json())
    
    def sort_papers_by_citations(self, papers):
        return sorted(papers, 
                     key=lambda x: x.get('citation_count', 0), 
                     reverse=True)
```

**Features:**
- ID format conversion (meta:br/ ↔ omid:br/)
- Real-time API communication
- Citation ranking algorithms
- Error handling for network issues

### 5. **federated_engine.py** - Database Query Execution
Handles PostgreSQL database interactions:

```python
def query_papers_db(sql_query):
    """Execute SQL query against papers database"""
    conn = psycopg2.connect(**PAPERS_DB_CONFIG)
    cursor = conn.cursor()
    
    cursor.execute(sql_query)
    results = cursor.fetchall()
    
    conn.close()
    return results
```

**Features:**
- Connection pooling
- Query optimization
- Error handling and retries
- Result formatting

### 6. **llm_postprocess.py** - AI Analysis
Provides intelligent research analysis and summarization:

```python
def postprocess_with_llm(papers, instruction):
    """Generate comprehensive research analysis using Groq AI"""
    analysis_prompt = create_analysis_prompt(papers, instruction)
    
    response = groq_client.chat.completions.create(
        messages=[{"role": "user", "content": analysis_prompt}],
        model="llama-3.1-8b-instant",
        temperature=0.3,
        max_tokens=2000
    )
    
    return format_analysis_response(response)
```

**Analysis Includes:**
- Research trend identification
- Methodological innovations
- Cross-disciplinary connections
- Impact assessment
- Future research directions

---

## Usage Guide

### Command Line Interface

**Basic Query:**
```bash
python run_research_query.py "machine learning algorithms"
```

**Complex Research Query:**
```bash
python run_research_query.py "analyze the most cited papers in neural networks and deep learning published after 2020 focusing on computer vision applications with emphasis on methodological innovations and practical implementations"
```

**Citation-Focused Query:**
```bash
python run_research_query.py "most cited papers in artificial intelligence machine learning optimization"
```

**Temporal Analysis:**
```bash
python run_research_query.py "evolution of quantum computing research from 2018 to 2024 with citation analysis and trend identification"
```

### Interactive Mode

```bash
python run_research_query.py
# System will prompt for interactive query input
```

---

## Sample Queries and Expected Results

### Simple Queries

1. **Basic Topic Search:**
```
Query: "neural networks"
Expected: 5-15 papers with basic metadata
Processing: Pattern-based SQL generation
Citation Data: Available if citation server running
```

2. **Year-Filtered Search:**
```
Query: "machine learning papers published after 2020"
Expected: Recent papers with temporal filtering
Processing: Date constraint extraction
Analysis: Publication trends
```

### Intermediate Queries

3. **Multi-Domain Research:**
```
Query: "artificial intelligence computer vision natural language processing"
Expected: 10-20 papers across AI domains
Processing: Multi-keyword matching
Citation Ranking: Papers sorted by impact
```

4. **Citation-Priority Query:**
```
Query: "most cited papers in deep learning optimization"
Expected: Citation-ranked results (15-30 citations per paper)
Processing: Citation API integration
Analysis: Impact assessment and trends
```

### Complex Queries

5. **Comprehensive Research Analysis:**
```
Query: "comprehensive analysis of quantum computing artificial intelligence machine learning published 2019-2024 including optimization algorithms distributed systems with focus on methodological innovations research trends citation impact"

Expected Output:
- 15+ relevant papers
- Citation counts: 10-35 per paper
- AI-powered analysis summary
- Research trend identification
- Venue and author analysis
- Publication timeline: 2019-2024
- Cross-domain connections
```

6. **Advanced Multi-Faceted Query:**
```
Query: "analyze breakthrough research in neural networks deep learning published after 2018 including convolutional networks transformer architectures attention mechanisms reinforcement learning generative models optimization techniques computer vision applications natural language understanding showing methodological innovations theoretical advances practical applications research trends"

Expected Output:
- 20+ papers from computer vision, NLP, ML domains
- Citation analysis with 10-40 citations per paper
- Professional research summary including:
  * Key research themes and innovations
  * Methodological advances
  * Practical applications
  * Industry impact assessment
  * Academic collaboration patterns
  * Publication venue analysis
- Temporal trend analysis
- Cross-disciplinary insights
```

---

## System Workflow

### Query Processing Pipeline

1. **Input Processing**
   - Command line argument parsing
   - Natural language query normalization
   - Component extraction (topics, years, priorities)

2. **Query Translation**
   - AI-powered SQL generation (Groq LLM)
   - Pattern-based fallback system
   - Query optimization and validation

3. **Database Execution**
   - Primary database query (papers)
   - Result set filtering and ranking
   - Error handling and retries

4. **Citation Enhancement**
   - ID format conversion (meta:br/ → omid:br/)
   - Real-time citation API calls
   - Citation count aggregation and ranking

5. **Analysis Generation**
   - AI-powered research analysis (Groq LLM)
   - Local analysis fallback system
   - Professional summary generation

6. **Result Presentation**
   - Formatted output display
   - Statistical summaries
   - Citation rankings and insights

### Error Handling and Fallbacks

- **AI API Unavailable**: Automatic fallback to pattern-based processing
- **Citation Server Down**: Graceful degradation with local paper data
- **Database Connection Issues**: Retry logic with exponential backoff
- **Invalid Queries**: Intelligent error messages and suggestions

---

## API Documentation

### Citation Server Endpoints

#### Health Check
```http
GET /api/status
Response: {
  "status": "ok",
  "total_citations": 4900000,
  "database_size": "2.3GB",
  "timestamp": "2024-11-14T10:30:00Z"
}
```

#### Get Paper Citations
```http
GET /api/paper/citations/{doi}?limit=100&details=true
Response: {
  "status": "ok",
  "doi": "10.1000/example",
  "count": 25,
  "citations": [...],
  "pagination": {...}
}
```

#### Bulk Citation Lookup
```http
POST /api/bulk/citations
Body: {"dois": ["10.1000/example1", "10.1000/example2"]}
Response: {
  "status": "ok",
  "citation_counts": {
    "10.1000/example1": 15,
    "10.1000/example2": 8
  }
}
```

---

## Configuration Options

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GROQ_API_KEY` | Groq AI API key for query processing | Required |
| `PAPERS_DB_NAME` | Primary database name | `opencitations_meta` |
| `PAPERS_DB_USER` | Database username | `postgres` |
| `PAPERS_DB_PASSWORD` | Database password | Required |
| `PAPERS_DB_HOST` | Database host | `localhost` |
| `PAPERS_DB_PORT` | Database port | `5432` |

### Citation Server Configuration

Update `federated_query/citation_analysis.py`:
```python
# Change this to your citation server's IP address
CITATION_API_URL = "http://192.168.41.167:5000"
```

### Database Configuration

Primary database (`config.py`):
```python
PAPERS_DB_CONFIG = {
    "dbname": "opencitations_meta",
    "user": "postgres", 
    "password": "your_password",
    "host": "localhost",
    "port": "5432"
}
```

Citation database (on remote machine):
```python
DB_CONFIG = {
    'host': 'localhost',
    'database': 'citations_db', 
    'user': 'citations_user',
    'password': 'citations_password',
    'port': 5432
}
```

---

## Testing and Diagnostics

### System Health Checks

1. **Database Connectivity:**
```bash
python -c "from federated_query.federated_engine import test_connection; test_connection()"
```

2. **Citation API Status:**
```bash
python -c "from federated_query.citation_analysis import CitationClient; print(CitationClient().test_connection())"
```

3. **Full System Test:**
```bash
python run_research_query.py "machine learning test"
```

### Performance Testing

Test with increasingly complex queries:
```bash
# Simple test
python run_research_query.py "machine learning"

# Medium complexity
python run_research_query.py "most cited neural network papers"

# High complexity  
python run_research_query.py "comprehensive analysis artificial intelligence machine learning deep learning published 2020-2024 citation trends methodological innovations"
```

### Expected Performance Metrics

- **Simple queries**: 2-5 seconds
- **Citation-enhanced queries**: 5-15 seconds  
- **Complex AI analysis**: 10-30 seconds
- **Database capacity**: 76.3M papers, 4.9M citations
- **Concurrent users**: 10-50 (depends on hardware)

---

## Troubleshooting

### Common Issues and Solutions

#### 1. Groq API Key Issues
**Problem**: `Groq API key not found` or `401 - Invalid API Key`
**Solution**: 
```bash
# Get free key from https://console.groq.com/
$env:GROQ_API_KEY = "gsk_your_actual_key_here"
```

#### 2. Citation Server Connection Failed
**Problem**: `Citation server not responding`
**Solutions**:
- Check if citation server is running on the remote machine
- Verify IP address in `citation_analysis.py`
- Check network connectivity between machines
- Ensure firewall allows port 5000

#### 3. Database Connection Issues
**Problem**: `Database connection failed`
**Solutions**:
- Verify PostgreSQL is running
- Check database credentials in environment variables
- Ensure database exists and is populated
- Test connection using system diagnostics

#### 4. ID Format Mismatch
**Problem**: `Citations not found` for valid papers
**Solution**: The system automatically converts between ID formats:
- Primary DB uses: `meta:br/06110436993`
- Citation DB uses: `omid:br/06110436993`
- Conversion handled in `citation_analysis.py`

#### 5. Memory Issues with Large Queries
**Problem**: System runs out of memory
**Solutions**:
- Reduce query scope or add time constraints
- Implement query result pagination
- Increase system RAM or optimize SQL queries

---

## 📈 Performance Optimization

### Database Optimization

1. **Index Creation:**
```sql
-- Primary database indexes
CREATE INDEX idx_papers_title_gin ON papers USING gin(to_tsvector('english', title));
CREATE INDEX idx_papers_author_gin ON papers USING gin(to_tsvector('english', author));
CREATE INDEX idx_papers_pub_date ON papers(pub_date);

-- Citation database indexes  
CREATE INDEX idx_citations_cited_doi ON citations(cited_paper_doi);
CREATE INDEX idx_citations_citing_doi ON citations(citing_paper_doi);
CREATE INDEX idx_citations_creation_date ON citations(creation_date);
```

2. **Materialized Views:**
```sql
-- Pre-computed citation counts
CREATE MATERIALIZED VIEW citation_counts AS
SELECT cited_paper_doi as doi, COUNT(*) as citation_count
FROM citations 
GROUP BY cited_paper_doi;

CREATE INDEX idx_citation_counts_count ON citation_counts(citation_count DESC);
```

### Application Optimization

1. **Connection Pooling**: Implemented in citation server
2. **Caching**: Cache frequent queries and citation data
3. **Parallel Processing**: Process multiple citation lookups concurrently
4. **Query Limitations**: Limit result sets for interactive use

---

## Contributing

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make changes and test thoroughly
4. Submit a pull request with detailed description

### Code Standards

- Follow PEP 8 style guidelines
- Add comprehensive docstrings
- Include unit tests for new features
- Update documentation for API changes

### Testing Requirements

- All new features must include tests
- Maintain test coverage above 80%
- Test on both Windows and Linux environments
- Validate with multiple database sizes

---


## Acknowledgments

- **OpenCitations**: Citation data source
- **DBLP**: Computer science bibliography
- **Groq**: AI-powered query processing
- **PostgreSQL**: Robust database foundation
- **Flask**: Citation server framework

---


## 🔮 Future Enhancements

### Planned Features

1. **Advanced Analytics**
   - Author collaboration networks
   - Research trend prediction
   - Cross-disciplinary impact analysis

2. **Enhanced AI Integration**
   - Multiple AI provider support
   - Custom model fine-tuning
   - Advanced prompt engineering

3. **Scalability Improvements**
   - Horizontal database scaling
   - Distributed query processing
   - Cloud deployment options

4. **User Interface**
   - Web-based dashboard
   - Interactive query builder
   - Visualization tools

5. **Additional Data Sources**
   - arXiv integration
   - PubMed support
   - Patent databases

---
