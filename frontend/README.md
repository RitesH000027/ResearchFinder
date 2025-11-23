# ResearchFinder Frontend Interface

This directory contains the web-based frontend interface for the ResearchFinder federated query system, built with Streamlit.

## Contents

### Main Application
- **`streamlit_app.py`** - Main Streamlit web application providing:
  - Natural language query interface
  - Real-time query processing and results display
  - Interactive visualizations (citation analysis, trend charts)
  - Multi-step architecture transparency (query rewriting, pattern extraction, SQL generation)
  - Professional result formatting with citation enrichment

### Dependencies & Configuration
- **`streamlit_requirements.txt`** - Frontend-specific Python dependencies:
  - streamlit - Web application framework
  - plotly - Interactive visualization library  
  - pandas - Data manipulation for results display
  - Additional UI/UX libraries

### Visualization Components
- **`plotly_fallback.py`** - Fallback visualization system for environments without full Plotly support
- **`STREAMLIT_DEMO_GUIDE.md`** - Comprehensive guide for running demonstrations

## Features

### Interactive Query Interface
- Natural language input field
- Query enhancement suggestions
- Real-time processing feedback
- Step-by-step architecture visualization

### Results Display
- Formatted paper listings with metadata
- Citation count integration from federated database
- Interactive charts and graphs
- Export functionality for results

### System Transparency
- Query rewriting process visualization
- Pattern extraction results display
- SQL generation method indication
- Fallback mechanism status

## Quick Start

### Installation
```bash
# Navigate to frontend directory
cd frontend

# Install frontend dependencies
pip install -r streamlit_requirements.txt

# Install main project dependencies (if not already installed)
pip install -r ../requirements.txt
```

### Running the Application
```bash
# Start Streamlit server
streamlit run streamlit_app.py

# Access via browser at: http://localhost:8501
```

### Configuration
Ensure the following environment variables are set:
```bash
# In .env file (project root)
GROQ_API_KEY=your_groq_api_key_here
DATABASE_URL=postgresql://username:password@localhost:5432/opencitations_meta
CITATION_API_BASE_URL=http://192.168.41.167:5000
```

## Development

### Architecture Integration
The frontend integrates with the core federated query system:
- `federated_query/` - Core system modules
- `run_research_query.py` - Main query execution engine
- OpenCitations Meta PostgreSQL database
- Remote citation database (via REST API)

### Customization
- Modify UI layout in `streamlit_app.py`
- Add new visualizations using Plotly components
- Extend result formatting in display functions
- Integrate additional data sources or analysis types

### Performance Optimization
- Results caching for repeated queries
- Lazy loading of citation data
- Progressive result display for large datasets
- Responsive design for various screen sizes

## Deployment

### Local Development
```bash
streamlit run streamlit_app.py --server.port 8501
```

### Production Deployment
```bash
# Using Streamlit Cloud, Docker, or cloud platforms
# See STREAMLIT_DEMO_GUIDE.md for detailed deployment instructions
```

## Demo Capabilities

The frontend demonstrates:
- ✅ Natural language query processing
- ✅ Three-step hybrid architecture transparency
- ✅ Real-time federated database integration
- ✅ Interactive citation analysis visualizations  
- ✅ Professional research result formatting
- ✅ System performance metrics display
- ✅ Error handling and graceful degradation