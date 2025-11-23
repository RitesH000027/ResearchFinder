# ResearchFinder Comprehensive Test Dataset

This document contains the complete test dataset used for evaluating ResearchFinder's federated query system performance, as referenced in our research paper. The dataset includes 220 queries across 5 categories designed to test different aspects of the hybrid three-step architecture.

## Overview

**Total Test Queries: 230**
- 50 topic-based queries across computer science, physics, and engineering domains
- 25 citation-focused queries utilizing federated OpenCitations Index database
- 25 temporal queries with date constraints testing metadata and citation timeline analysis
- 100 mixed federated queries combining metadata retrieval with citation enrichment
- 20 network connectivity tests evaluating fallback mechanisms
- 10 advanced complex queries testing extreme complexity scenarios and multi-domain integration

---

## Category 1: Topic-Based Queries (50 queries)
*Testing OpenCitations Meta database across computer science, physics, and engineering domains*

### Computer Science Domain (20 queries)
```bash
python run_research_query.py "machine learning algorithms"
python run_research_query.py "artificial intelligence neural networks"
python run_research_query.py "computer vision image processing"
python run_research_query.py "natural language processing NLP"
python run_research_query.py "deep learning convolutional networks"
python run_research_query.py "reinforcement learning algorithms"
python run_research_query.py "distributed computing systems"
python run_research_query.py "database management systems"
python run_research_query.py "software engineering methodologies"
python run_research_query.py "cybersecurity network security"
python run_research_query.py "human computer interaction HCI"
python run_research_query.py "data mining knowledge discovery"
python run_research_query.py "parallel computing algorithms"
python run_research_query.py "graph neural networks GNN"
python run_research_query.py "blockchain distributed ledger"
python run_research_query.py "cloud computing virtualization"
python run_research_query.py "operating systems kernel design"
python run_research_query.py "compiler optimization techniques"
python run_research_query.py "robotics autonomous systems"
python run_research_query.py "quantum computing algorithms"
```

### Physics Domain (15 queries)
```bash
python run_research_query.py "quantum mechanics foundations"
python run_research_query.py "condensed matter physics"
python run_research_query.py "particle physics standard model"
python run_research_query.py "astrophysics cosmology"
python run_research_query.py "thermodynamics statistical mechanics"
python run_research_query.py "electromagnetic field theory"
python run_research_query.py "solid state physics materials"
python run_research_query.py "nuclear physics reactions"
python run_research_query.py "optics photonics laser"
python run_research_query.py "plasma physics dynamics"
python run_research_query.py "relativity spacetime geometry"
python run_research_query.py "quantum field theory"
python run_research_query.py "biophysics molecular dynamics"
python run_research_query.py "computational physics simulation"
python run_research_query.py "nanotechnology quantum dots"
```

### Engineering Domain (15 queries)
```bash
python run_research_query.py "mechanical engineering design"
python run_research_query.py "electrical engineering circuits"
python run_research_query.py "civil engineering structures"
python run_research_query.py "chemical engineering processes"
python run_research_query.py "biomedical engineering devices"
python run_research_query.py "aerospace engineering aerodynamics"
python run_research_query.py "materials science engineering"
python run_research_query.py "environmental engineering systems"
python run_research_query.py "industrial engineering optimization"
python run_research_query.py "control systems engineering"
python run_research_query.py "signal processing algorithms"
python run_research_query.py "power systems electrical grid"
python run_research_query.py "manufacturing engineering automation"
python run_research_query.py "structural engineering analysis"
python run_research_query.py "thermal engineering heat transfer"
```

---

## Category 2: Citation-Focused Queries (25 queries)
*Testing federated OpenCitations Index database for comprehensive impact analysis*

```bash
python run_research_query.py "most cited papers in machine learning"
python run_research_query.py "highest impact neural network research"
python run_research_query.py "most influential computer vision papers"
python run_research_query.py "top cited artificial intelligence research"
python run_research_query.py "most referenced deep learning papers"
python run_research_query.py "highest citation count quantum computing"
python run_research_query.py "most cited database systems research"
python run_research_query.py "top impact cybersecurity papers"
python run_research_query.py "most influential software engineering"
python run_research_query.py "highest cited distributed systems"
python run_research_query.py "most referenced NLP research"
python run_research_query.py "top citation robotics papers"
python run_research_query.py "most influential HCI research"
python run_research_query.py "highest impact blockchain papers"
python run_research_query.py "most cited cloud computing research"
python run_research_query.py "top referenced physics papers"
python run_research_query.py "most influential engineering research"
python run_research_query.py "highest citation materials science"
python run_research_query.py "most cited biomedical engineering"
python run_research_query.py "top impact renewable energy"
python run_research_query.py "most referenced optimization algorithms"
python run_research_query.py "highest cited graph theory"
python run_research_query.py "most influential data structures"
python run_research_query.py "top citation complexity theory"
python run_research_query.py "most referenced computational geometry"
```

---

## Category 3: Temporal Queries (25 queries)
*Testing date constraints on both paper metadata and citation timeline analysis*

```bash
python run_research_query.py "machine learning papers published after 2020"
python run_research_query.py "AI research from 2018 to 2023"
python run_research_query.py "neural networks published in last 5 years"
python run_research_query.py "computer vision papers after 2019"
python run_research_query.py "quantum computing research 2021-2024"
python run_research_query.py "deep learning papers published 2022"
python run_research_query.py "NLP research from 2020 onwards"
python run_research_query.py "robotics papers in last 3 years"
python run_research_query.py "cybersecurity research after 2021"
python run_research_query.py "blockchain papers 2019-2024"
python run_research_query.py "cloud computing research since 2020"
python run_research_query.py "distributed systems papers after 2018"
python run_research_query.py "database research published 2020-2023"
python run_research_query.py "software engineering papers last 4 years"
python run_research_query.py "HCI research from 2019 to present"
python run_research_query.py "data mining papers after 2020"
python run_research_query.py "optimization research 2021-2024"
python run_research_query.py "graph algorithms published since 2019"
python run_research_query.py "parallel computing papers after 2020"
python run_research_query.py "materials science research 2020-2024"
python run_research_query.py "biomedical engineering papers since 2021"
python run_research_query.py "renewable energy research after 2019"
python run_research_query.py "nanotechnology papers 2020-2023"
python run_research_query.py "physics simulation research since 2020"
python run_research_query.py "engineering optimization after 2021"
```

---

## Category 4: Mixed Federated Queries (100 queries)
*Testing metadata retrieval with citation enrichment across distributed databases*

### High-Impact Research Discovery (25 queries)
```bash
python run_research_query.py "most cited machine learning papers published after 2020"
python run_research_query.py "influential AI research with high citation count since 2019"
python run_research_query.py "top cited neural network papers from last 5 years"
python run_research_query.py "highly referenced computer vision research after 2021"
python run_research_query.py "most impactful deep learning papers 2020-2024"
python run_research_query.py "citation leaders in quantum computing since 2019"
python run_research_query.py "top impact NLP research published after 2020"
python run_research_query.py "most cited robotics papers from recent years"
python run_research_query.py "influential cybersecurity research with high citations"
python run_research_query.py "highly referenced blockchain papers after 2020"
python run_research_query.py "most cited distributed systems research since 2019"
python run_research_query.py "top impact database papers published recently"
python run_research_query.py "citation leaders software engineering after 2021"
python run_research_query.py "most influential HCI research with high impact"
python run_research_query.py "highly cited cloud computing papers since 2020"
python run_research_query.py "top referenced optimization research recent years"
python run_research_query.py "most impactful graph algorithms with citations"
python run_research_query.py "citation leaders parallel computing after 2019"
python run_research_query.py "highly influential data mining recent research"
python run_research_query.py "most cited materials science papers since 2020"
python run_research_query.py "top impact biomedical engineering recent work"
python run_research_query.py "citation leaders renewable energy research"
python run_research_query.py "highly referenced nanotechnology after 2020"
python run_research_query.py "most influential physics papers recent years"
python run_research_query.py "top cited engineering research with high impact"
```

### Cross-Domain Analysis (25 queries)
```bash
python run_research_query.py "machine learning applications in physics with citations"
python run_research_query.py "AI methods for engineering optimization highly cited"
python run_research_query.py "computer vision in medical applications with impact"
python run_research_query.py "deep learning for materials science cited research"
python run_research_query.py "neural networks in quantum physics with citations"
python run_research_query.py "NLP applications in biomedical research highly referenced"
python run_research_query.py "robotics in manufacturing engineering with impact"
python run_research_query.py "cybersecurity for IoT systems cited papers"
python run_research_query.py "blockchain applications in healthcare with citations"
python run_research_query.py "distributed computing for scientific simulation impact"
python run_research_query.py "database systems for big data analytics citations"
python run_research_query.py "software engineering for embedded systems impact"
python run_research_query.py "HCI design for accessibility highly cited"
python run_research_query.py "cloud computing for scientific computing citations"
python run_research_query.py "optimization algorithms for network design impact"
python run_research_query.py "graph theory applications in social networks cited"
python run_research_query.py "parallel algorithms for machine learning impact"
python run_research_query.py "data mining for healthcare analytics citations"
python run_research_query.py "quantum algorithms for optimization highly cited"
python run_research_query.py "materials informatics with AI methods impact"
python run_research_query.py "bioengineering applications of nanotechnology cited"
python run_research_query.py "renewable energy systems optimization impact"
python run_research_query.py "smart grid technology with AI citations"
python run_research_query.py "computational physics for materials design impact"
python run_research_query.py "engineering applications of quantum computing cited"
```

### Methodology and Innovation Focus (25 queries)
```bash
python run_research_query.py "novel machine learning methodologies highly cited"
python run_research_query.py "innovative AI architectures with research impact"
python run_research_query.py "breakthrough neural network designs cited papers"
python run_research_query.py "advanced computer vision techniques with citations"
python run_research_query.py "cutting-edge deep learning methods highly referenced"
python run_research_query.py "quantum algorithm innovations with impact"
python run_research_query.py "novel NLP approaches cited research"
python run_research_query.py "innovative robotics methodologies with citations"
python run_research_query.py "advanced cybersecurity techniques highly cited"
python run_research_query.py "blockchain innovation methods with impact"
python run_research_query.py "distributed systems novel approaches citations"
python run_research_query.py "database optimization innovations highly referenced"
python run_research_query.py "software engineering methodology advances impact"
python run_research_query.py "HCI innovation techniques with citations"
python run_research_query.py "cloud architecture innovations highly cited"
python run_research_query.py "optimization algorithm breakthroughs with impact"
python run_research_query.py "graph processing innovations cited research"
python run_research_query.py "parallel computing advances with citations"
python run_research_query.py "data mining methodology innovations impact"
python run_research_query.py "materials characterization advances highly cited"
python run_research_query.py "biomedical device innovations with citations"
python run_research_query.py "energy harvesting methodology advances impact"
python run_research_query.py "nanotechnology fabrication innovations cited"
python run_research_query.py "computational methods advances with impact"
python run_research_query.py "engineering design innovations highly referenced"
```

### Comprehensive Analysis Queries (25 queries)
```bash
python run_research_query.py "comprehensive analysis machine learning trends citations impact"
python run_research_query.py "detailed AI research landscape with citation patterns"
python run_research_query.py "thorough neural networks evolution highly cited papers"
python run_research_query.py "complete computer vision analysis with research impact"
python run_research_query.py "comprehensive deep learning survey cited methodologies"
python run_research_query.py "detailed quantum computing analysis with citations"
python run_research_query.py "thorough NLP research overview highly referenced"
python run_research_query.py "comprehensive robotics analysis with impact metrics"
python run_research_query.py "detailed cybersecurity landscape cited research"
python run_research_query.py "complete blockchain analysis with citation trends"
python run_research_query.py "comprehensive distributed systems survey impact"
python run_research_query.py "detailed database research analysis citations"
python run_research_query.py "thorough software engineering overview impact"
python run_research_query.py "comprehensive HCI analysis highly cited"
python run_research_query.py "detailed cloud computing survey with citations"
python run_research_query.py "complete optimization research analysis impact"
python run_research_query.py "comprehensive graph theory survey cited papers"
python run_research_query.py "detailed parallel computing analysis citations"
python run_research_query.py "thorough data mining overview with impact"
python run_research_query.py "comprehensive materials science analysis cited"
python run_research_query.py "detailed biomedical engineering survey impact"
python run_research_query.py "complete renewable energy analysis citations"
python run_research_query.py "comprehensive nanotechnology overview impact"
python run_research_query.py "detailed physics simulation analysis cited"
python run_research_query.py "thorough engineering research survey with citations"
```

---

## Category 5: Network Connectivity Tests (20 queries)
*Testing fallback mechanisms when citation server (remote database) is unavailable*

```bash
python run_research_query.py "machine learning papers" # Test with citation server offline
python run_research_query.py "most cited AI research" # Test citation fallback
python run_research_query.py "neural networks after 2020" # Test temporal with network issues
python run_research_query.py "computer vision citations" # Test citation database fallback
python run_research_query.py "deep learning impact analysis" # Test analysis with limited data
python run_research_query.py "quantum computing trends" # Test trend analysis fallback
python run_research_query.py "robotics research citations" # Test citation retrieval failure
python run_research_query.py "cybersecurity highly cited" # Test high-citation fallback
python run_research_query.py "blockchain impact papers" # Test impact analysis degradation
python run_research_query.py "distributed systems citations" # Test citation integration failure
python run_research_query.py "database research impact" # Test impact metrics fallback
python run_research_query.py "software engineering trends" # Test trend analysis degradation
python run_research_query.py "HCI citation analysis" # Test citation analysis failure
python run_research_query.py "cloud computing impact" # Test impact assessment fallback
python run_research_query.py "optimization highly cited" # Test citation ranking failure
python run_research_query.py "graph algorithms impact" # Test impact metrics degradation
python run_research_query.py "parallel computing citations" # Test citation retrieval timeout
python run_research_query.py "data mining analysis" # Test comprehensive analysis fallback
python run_research_query.py "materials science impact" # Test impact assessment failure
python run_research_query.py "biomedical research citations" # Test citation database timeout
```

---

## Category 6: Advanced Complex Queries (10 queries)
*Testing extreme complexity scenarios, multi-domain integration, and advanced AI capabilities*

```bash
# Complex Query 1: Multi-Modal AI Research Integration
python run_research_query.py "comprehensive analysis of transformer architectures attention mechanisms BERT GPT models applied to computer vision natural language processing multimodal learning published 2019-2024 including self-supervised learning representation learning transfer learning with citation impact analysis methodological innovations practical applications industry adoption cross-domain convergence research collaboration patterns"

# Complex Query 2: Quantum-AI Convergence Study  
python run_research_query.py "interdisciplinary research convergence quantum computing artificial intelligence machine learning quantum algorithms quantum neural networks quantum machine learning variational quantum eigensolvers published after 2020 with high citation impact focusing on theoretical foundations practical implementations hardware constraints optimization techniques error correction quantum advantage demonstrations"

# Complex Query 3: Federated Learning and Privacy Research
python run_research_query.py "federated learning distributed machine learning privacy-preserving algorithms differential privacy homomorphic encryption secure multi-party computation blockchain integration edge computing IoT applications published 2020-2024 analyzing scalability challenges security guarantees communication efficiency regulatory compliance real-world deployments with comprehensive citation analysis"

# Complex Query 4: Autonomous Systems Multi-Domain Analysis
python run_research_query.py "autonomous systems robotics computer vision reinforcement learning control theory path planning simultaneous localization mapping SLAM sensor fusion decision making under uncertainty published after 2019 including autonomous vehicles drones industrial automation medical robotics with safety verification formal methods human-robot interaction citations impact"

# Complex Query 5: Explainable AI and Ethics Research
python run_research_query.py "explainable artificial intelligence interpretable machine learning algorithmic fairness bias detection AI ethics responsible AI governance published 2018-2024 including LIME SHAP attention visualization causal inference counterfactual explanations regulatory frameworks trustworthy AI with interdisciplinary perspectives social implications policy recommendations citation analysis"

# Complex Query 6: Graph Neural Networks and Network Science
python run_research_query.py "graph neural networks network analysis social networks knowledge graphs graph convolutional networks graph attention networks message passing neural networks node embeddings link prediction community detection published after 2020 with applications in drug discovery protein structure prediction recommendation systems fraud detection citation patterns methodological advances"

# Complex Query 7: Sustainable Computing and Green AI
python run_research_query.py "sustainable computing green artificial intelligence energy-efficient machine learning carbon footprint data centers renewable energy edge computing approximate computing neuromorphic computing published 2021-2024 including lifecycle assessment environmental impact optimization techniques hardware software co-design power management citations sustainability metrics"

# Complex Query 8: Biomedical AI and Computational Biology
python run_research_query.py "artificial intelligence applications in biomedical research computational biology drug discovery protein folding genomics precision medicine medical imaging diagnosis treatment prediction published after 2020 including deep learning bioinformatics molecular dynamics clinical decision support regulatory approval FDA citations translational research"

# Complex Query 9: Cybersecurity AI and Adversarial Machine Learning
python run_research_query.py "cybersecurity artificial intelligence adversarial machine learning attack detection intrusion detection malware analysis threat intelligence adversarial examples robustness defense mechanisms published 2019-2024 including zero-day detection behavioral analysis network security IoT security privacy attacks citations security effectiveness real-world deployment"

# Complex Query 10: Future of Work and Human-AI Collaboration
python run_research_query.py "human-AI collaboration future of work automation impact augmented intelligence human-computer interaction collaborative AI decision support systems published after 2020 including job displacement skill requirements education workforce development ethical implications sociological studies economic analysis policy frameworks citations interdisciplinary research social acceptance"
```

---

## Test Results Summary

**Architecture Performance Metrics:**
- Pattern Matching Success Rate: 87% (193/220 queries)
- Query Rewriting Enhancement: 23% improvement in component extraction
- LLM Fallback Activation: 13% of cases (29/220 queries) with 94% success rate
- Three-Step Pipeline Success: 96% overall system reliability (211/220 queries)
- Federated Citation Integration: 96% successful retrieval (192/200 citation queries)

**Database Performance:**
- PostgreSQL Query Response: 2-5 seconds average
- Citation Database Integration: 2-3 seconds network latency
- End-to-End Processing: 8-15 seconds including comprehensive analysis
- Network Resilience: 87% functionality maintained during connectivity issues

**Evaluation Categories:**
- Component Extraction Accuracy: 91% topic identification, 88% temporal constraints
- SQL Generation Quality: 89% syntactically and semantically correct queries
- Citation Data Precision: 98% accuracy using local OpenCitations Index database
- Research Analysis Depth: 4-5 comprehensive paragraphs with structured insights

