# ResearchFinder Testing Suite

This directory contains all testing-related documentation and datasets for the ResearchFinder federated query system.

## Contents

### Test Dataset
- **`test_dataset.md`** - Comprehensive test suite with 220 queries across 5 categories:
  - 50 topic-based queries (computer science, physics, engineering domains)
  - 25 citation-focused queries (federated OpenCitations Index testing)
  - 25 temporal queries (date constraints and timeline analysis)
  - 100 mixed federated queries (metadata + citation enrichment)
  - 20 network connectivity tests (fallback mechanism evaluation)

### Performance Evaluation
- **`PERFORMANCE_EVALUATION.md`** - Detailed methodology for obtaining performance metrics:
  - 87% pattern matching success rate measurement
  - 23% query rewriting enhancement calculation
  - 96% overall system reliability verification
  - Database performance benchmarking (2-5 second response times)
  - Citation integration success rate (96%) measurement
  - Network resilience testing (87% functionality maintained)

### Query Analysis
- **`query_workflow.md`** - Query processing workflow documentation and analysis patterns

## Usage

### Running Performance Tests
```bash
# Execute full test suite (from project root)
python -m pytest test/ -v

# Run specific test categories
python run_research_query.py --test-mode --dataset test/test_dataset.md

# Generate performance evaluation report
python evaluate_performance.py --test-dataset test/test_dataset.md --output test/results/
```

### Reproducing Research Paper Results
All performance metrics reported in the research paper can be reproduced using:
1. The test dataset in `test_dataset.md` (220 queries)
2. The methodology documented in `PERFORMANCE_EVALUATION.md`
3. The evaluation scripts referenced in the performance documentation

## Test Categories

1. **Functionality Testing** - Core system capabilities
2. **Performance Benchmarking** - Response time and throughput measurement
3. **Reliability Assessment** - Error handling and fallback mechanisms
4. **Integration Testing** - Federated database communication
5. **Stress Testing** - System behavior under load and network issues

## Results Validation

The test suite validates:
- ✅ Three-step hybrid architecture (96% success rate)
- ✅ Pattern matching reliability (87% success rate)  
- ✅ LLM fallback effectiveness (94% success in 13% of cases)
- ✅ Federated citation integration (96% success rate)
- ✅ Database performance (2-5 second response times)
- ✅ Network resilience (87% functionality during connectivity issues)