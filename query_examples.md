# ResearchFinder Query Examples

This document provides sample queries organized by complexity level to help you test and demonstrate the ResearchFinder system capabilities.

## Simple Queries (Basic Functionality)

These queries test basic search functionality with single concepts or simple keywords.

### 1. Single Topic Search
```bash
python run_research_query.py "machine learning"
```
**Expected Results:** 5-10 papers containing "machine" or "learning" in titles
**Features Tested:** Basic keyword matching, pattern-based SQL generation

### 2. Basic Neural Networks
```bash
python run_research_query.py "neural networks"
```
**Expected Results:** Papers about neural networks, social networks, or network-related research
**Features Tested:** Multi-word search, citation lookup

### 3. Simple Year Filter
```bash
python run_research_query.py "quantum computing after 2020"
```
**Expected Results:** Recent quantum-related papers with temporal filtering
**Features Tested:** Date constraint parsing, AI SQL generation

### 4. Basic Citation Query
```bash
python run_research_query.py "most cited papers"
```
**Expected Results:** Papers sorted by citation count
**Features Tested:** Citation priority detection, sorting functionality

### 5. Single Domain Search
```bash
python run_research_query.py "artificial intelligence"
```
**Expected Results:** AI-related papers from various domains
**Features Tested:** Concept recognition, database querying

---

## Medium-Level Queries (Enhanced Features)

These queries test multi-concept searches, temporal analysis, and citation integration.

### 1. Multi-Topic with Citations
```bash
python run_research_query.py "most cited papers in machine learning and neural networks"
```
**Expected Results:** Citation-ranked papers from ML/NN domains, 10-30 citations per paper
**Features Tested:** Citation ranking, multi-concept parsing, API integration

### 2. Temporal Research Analysis
```bash
python run_research_query.py "artificial intelligence research published between 2018 and 2024"
```
**Expected Results:** Recent AI papers with publication year filtering
**Features Tested:** Date range parsing, temporal constraints, result filtering

### 3. Domain-Specific Citation Analysis
```bash
python run_research_query.py "most cited computer vision papers published after 2019"
```
**Expected Results:** Recent CV papers sorted by citations with professional analysis
**Features Tested:** Domain filtering, citation integration, AI analysis

### 4. Cross-Disciplinary Search
```bash
python run_research_query.py "optimization algorithms in machine learning and computer science"
```
**Expected Results:** Papers spanning multiple CS domains
**Features Tested:** Multi-domain search, keyword expansion, interdisciplinary discovery

### 5. Methodology-Focused Query
```bash
python run_research_query.py "deep learning neural network architectures with research trends analysis"
```
**Expected Results:** DL papers with AI-generated trend analysis
**Features Tested:** Methodology detection, AI postprocessing, professional summaries

---

## Complex Large Queries (Advanced Capabilities)

These queries test the full system capabilities including AI analysis, comprehensive citation integration, and multi-faceted research discovery.

### 1. Comprehensive Multi-Domain Analysis
```bash
python run_research_query.py "comprehensive analysis of artificial intelligence machine learning deep learning neural networks computer vision natural language processing published 2019-2024 with citation impact methodological innovations research trends influential authors collaborative networks"
```
**Expected Results:** 15-20 papers across AI domains with comprehensive analysis
**Features Tested:** Complex parsing, citation ranking, AI analysis, professional summaries

### 2. Citation-Focused Research Discovery
```bash
python run_research_query.py "analyze the most cited breakthrough papers in computer science artificial intelligence machine learning published after 2020 focusing on methodological innovations practical applications industry impact academic influence research collaboration patterns"
```
**Expected Results:** High-impact papers (20-50+ citations) with detailed analysis
**Features Tested:** Citation priority, impact analysis, methodology detection, collaboration insights

### 3. Temporal Evolution Analysis
```bash
python run_research_query.py "temporal analysis of computational intelligence research evolution from classical algorithms to modern deep learning including neural networks machine learning artificial intelligence quantum computing optimization published 2015-2024 showing research trends breakthrough methodologies citation patterns"
```
**Expected Results:** Papers spanning multiple years with trend analysis
**Features Tested:** Temporal analysis, evolution tracking, multi-domain integration, citation patterns

### 4. Cross-Disciplinary Innovation Study
```bash
python run_research_query.py "interdisciplinary research connections between artificial intelligence machine learning computer vision robotics natural language processing data mining distributed systems network security database systems showing methodological convergence technological innovations collaborative networks influential venues"
```
**Expected Results:** Papers showing interdisciplinary connections with venue analysis
**Features Tested:** Cross-domain discovery, innovation detection, venue analysis, collaboration patterns

### 5. Comprehensive Research Landscape
```bash
python run_research_query.py "comprehensive research landscape analysis of neural networks deep learning computer vision natural language processing reinforcement learning optimization algorithms published after 2018 including transformer architectures attention mechanisms generative models practical applications methodological advances citation leaders research trends venue prestige author reputation knowledge transfer"
```
**Expected Results:** 20+ papers with full research landscape analysis
**Features Tested:** Complete system capabilities, advanced AI analysis, citation leadership, comprehensive statistics

---

