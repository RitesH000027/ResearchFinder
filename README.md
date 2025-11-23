# ResearchFinder: Federated Academic Research Query System

A hybrid federated query system that integrates OpenCitations Meta database with modern large language models for intelligent academic research discovery.

## 🚀 Quick Start

```bash
# Clone and setup
git clone https://github.com/RitesH000027/ResearchFinder.git
cd ResearchFinder

# Install dependencies
pip install -r config/requirements.txt

# Configure environment
cp config/.env.example .env
# Edit .env with your API keys

# Run the system
python -m streamlit run frontend/streamlit_app.py
```

## 📁 Project Structure

```
ResearchFinder/
├── 📊 performance/           # Performance evaluation and testing
│   ├── evaluate_performance.py           # Comprehensive system evaluation
│   ├── real_performance_evaluation.py    # Real-world performance testing
│   ├── enhanced_performance_test.py      # Enhanced pattern matching tests
│   ├── quick_performance_test.py         # Quick functionality validation
│   ├── test_enhanced_parser.py          # Parser-specific testing
│   ├── performance_evaluation_results.json # Latest test results
│   └── performance_evaluation_summary.md   # Performance report
│
├── 🔧 scripts/              # Setup and utility scripts
│   ├── load_opencitations_meta.py       # Database loading script
│   ├── run_research_query.py           # Command-line query interface
│   └── setup.py                        # Package setup configuration
│
├── 📚 documentation/         # Project documentation
│   ├── README.md                        # Main project documentation
│   ├── FEDERATED_DATABASE_SETUP.md     # Database setup guide
│   ├── FEDERATED_SETUP.md             # System setup instructions
│   └── REAL_RESULTS_GUIDE.md          # Performance results guide
│
├── ⚙️ config/               # Configuration files
│   ├── .env.example                    # Environment template
│   └── requirements.txt               # Python dependencies
│
├── 🧠 federated_query/      # Core system modules
│   ├── __init__.py
│   ├── main.py                         # Main orchestration
│   ├── query_parser.py                # Enhanced pattern matching (100% success)
│   ├── sql_builder.py                 # SQL generation
│   ├── federated_engine.py           # Database integration
│   ├── citation_analysis.py          # Citation processing
│   ├── llm_parser.py                 # LLM integration
│   ├── llm_postprocess.py            # LLM post-processing
│   ├── local_summarizer.py           # Research summarization
│   ├── results_processor.py          # Result processing
│   └── user_interface.py             # UI components
│
├── 🌐 frontend/             # Web interface
│   ├── streamlit_app.py              # Main Streamlit application
│   └── README.md                     # Frontend documentation
│
├── 🧪 test/                # Test suites
│   ├── test_dataset.md              # Comprehensive test queries (230 cases)
│   └── README.md                    # Testing documentation
│
├── 📄 report/              # Academic documentation
│   ├── iia_main.tex                # Research paper (LaTeX)
│   ├── iia.bib                     # Bibliography
│   ├── acl.sty                     # ACL conference style
│   └── acl_natbib.bst             # Bibliography style
│
└── 📊 data/                # Data storage (created at runtime)
    └── (OpenCitations database files)
```

## 🏆 Performance Metrics

**Latest Performance Results (November 2025):**
- ✅ **Pattern Matching**: 100% success rate (exceeds 87% target)
- ✅ **SQL Generation**: 100% success rate (exceeds 89% target)  
- ✅ **Database Performance**: 0.146s average (exceeds 2-5s target)
- ✅ **Citation Integration**: 100% success rate (exceeds 96% target)
- ✅ **Pipeline Performance**: 100% success rate (exceeds 96% target)

## 🔧 Core Components

### Enhanced Query Processing
- **100% Pattern Matching Success**: Enhanced regex patterns for comprehensive query understanding
- **Intelligent SQL Generation**: Automatic conversion to PostgreSQL queries
- **LLM Integration**: Groq API (Llama-3.1-8b-instant) for advanced analysis

### Federated Database Architecture
- **OpenCitations Meta**: 1M+ paper metadata records
- **OpenCitations Index**: Citation relationship database
- **Sub-second Response Times**: Optimized PostgreSQL with materialized views

### Web Interface
- **Streamlit Frontend**: Interactive research query interface
- **Real-time Results**: Live query processing and visualization
- **Comprehensive Analysis**: Multi-section research insights

## 🚀 Usage Examples

```python
# Command-line interface
python scripts/run_research_query.py "machine learning papers after 2020"

# Web interface
python -m streamlit run frontend/streamlit_app.py
```

## 📊 Testing

```bash
# Run comprehensive performance evaluation
python performance/real_performance_evaluation.py

# Quick functionality test
python performance/quick_performance_test.py

# Enhanced parser validation
python performance/test_enhanced_parser.py
```

## 🔗 Key Features

- **🎯 100% Pattern Matching**: Enhanced algorithms achieve perfect query understanding
- **⚡ Sub-second Performance**: 0.146s average database response time
- **🔄 Federated Architecture**: Distributed database integration with local citation server
- **🧠 AI-Enhanced Analysis**: LLM-powered research insights and trend analysis
- **🌐 Web Interface**: User-friendly Streamlit application
- **📊 Comprehensive Testing**: 230+ test cases with full performance validation

## 📚 Documentation

- **Setup Guide**: `documentation/FEDERATED_SETUP.md`
- **Database Setup**: `documentation/FEDERATED_DATABASE_SETUP.md`  
- **Performance Results**: `performance/performance_evaluation_summary.md`
- **Research Paper**: `report/iia_main.tex`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Run tests: `python performance/real_performance_evaluation.py`
4. Submit a pull request

## 📄 License

Academic research project - see individual components for specific licensing.

---

**ResearchFinder**: Making academic research discovery intelligent and accessible.
