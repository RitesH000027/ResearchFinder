# LLM Prompt Rewriting Module
# Takes decomposed query results and creates specialized LLM prompts
# This addresses requirement (b) from professor's guidelines

import os
from typing import Dict, Any, List, Optional

def rewrite_prompt_for_analysis(decomposed_query: Dict[str, Any], sql_results: List[Any]) -> str:
    """
    Rewrite decomposed query components into optimized LLM analysis prompt.
    
    Args:
        decomposed_query: Results from query_parser.extract_query_components()
        sql_results: Results from SQL federation queries
    
    Returns:
        Specialized LLM prompt for research analysis
    """
    
    # Extract key components from decomposed query
    topic = decomposed_query.get('topic', 'research area')
    year = decomposed_query.get('year')
    citation_priority = decomposed_query.get('citation_priority', False)
    result_count = decomposed_query.get('result_count', 5)
    want_summary = decomposed_query.get('want_summary', False)
    
    # Build context-aware prompt based on query decomposition
    prompt_parts = []
    
    # 1. Task specification based on decomposed intent
    if citation_priority:
        prompt_parts.append(f"Analyze the citation impact and research influence of papers in {topic}.")
    elif want_summary:
        prompt_parts.append(f"Provide a comprehensive research analysis and summary of developments in {topic}.")
    else:
        prompt_parts.append(f"Analyze key research trends and findings in {topic}.")
    
    # 2. Temporal context from decomposition
    if year:
        prompt_parts.append(f"Focus on research published from {year} onwards, highlighting temporal trends and evolution.")
    else:
        prompt_parts.append("Consider the temporal evolution of research and recent developments.")
    
    # 3. Scope and methodology guidance
    prompt_parts.append(f"Based on {len(sql_results)} papers retrieved from federated database queries:")
    
    # 4. Analysis framework
    analysis_framework = [
        "1. **Research Themes**: Identify dominant research themes and emerging topics",
        "2. **Methodological Approaches**: Analyze research methodologies and technical approaches",
        "3. **Key Innovations**: Highlight breakthrough findings and novel contributions",
        "4. **Research Gaps**: Identify unexplored areas and future research directions"
    ]
    
    if citation_priority:
        analysis_framework.append("5. **Impact Analysis**: Evaluate citation patterns and research influence")
    
    prompt_parts.extend(analysis_framework)
    
    # 5. Output format specification
    prompt_parts.append("\nProvide a structured analysis (2-3 paragraphs) that synthesizes findings across the retrieved papers.")
    
    return "\n".join(prompt_parts)

def rewrite_prompt_for_sql_generation(decomposed_query: Dict[str, Any]) -> str:
    """
    Rewrite decomposed query for specialized SQL generation prompt.
    
    Args:
        decomposed_query: Results from query_parser.extract_query_components()
    
    Returns:
        Specialized LLM prompt for SQL generation
    """
    
    topic = decomposed_query.get('topic', '')
    year = decomposed_query.get('year')
    citation_priority = decomposed_query.get('citation_priority', False)
    specific_paper_title = decomposed_query.get('specific_paper_title')
    result_count = decomposed_query.get('result_count', 5)
    
    prompt_parts = [
        "Generate optimized PostgreSQL queries for federated research database system.",
        f"Query decomposition results: topic='{topic}', year='{year}', citation_priority={citation_priority}",
        "",
        "Available federated databases:",
        "- papers (localhost): id, title, author, pub_date, venue, type",
        "- citations (192.168.1.100): paper_id, citing_paper_id, citation_count, impact_factor", 
        "- authors (192.168.1.101): author_id, author_name, affiliation, h_index",
        ""
    ]
    
    # Specific query construction based on decomposition
    if specific_paper_title:
        prompt_parts.append(f"Generate SQL to find specific paper: '{specific_paper_title}'")
    elif citation_priority:
        prompt_parts.append(f"Generate federated SQL to find papers about '{topic}' with citation analysis")
        prompt_parts.append("Priority: Join with citations database for impact metrics")
    else:
        prompt_parts.append(f"Generate SQL to find papers about '{topic}'")
    
    if year:
        prompt_parts.append(f"Include temporal filter: pub_date >= '{year}-01-01'")
    
    prompt_parts.append(f"Limit results to {result_count} papers")
    prompt_parts.append("\nReturn only the SQL query, no explanations.")
    
    return "\n".join(prompt_parts)

def rewrite_prompt_for_federation_strategy(decomposed_query: Dict[str, Any]) -> Dict[str, str]:
    """
    Create database-specific prompts for federated query execution.
    
    Args:
        decomposed_query: Results from query_parser.extract_query_components()
    
    Returns:
        Dictionary mapping database names to specialized prompts
    """
    
    topic = decomposed_query.get('topic', '')
    year = decomposed_query.get('year')
    citation_priority = decomposed_query.get('citation_priority', False)
    result_count = decomposed_query.get('result_count', 5)
    
    federation_prompts = {}
    
    # Papers database prompt (primary)
    papers_prompt = f"""
    Query papers database for research about '{topic}'.
    Schema: papers(id, title, author, pub_date, venue, type)
    Filter: title ILIKE '%{topic}%'
    """
    if year:
        papers_prompt += f" AND pub_date >= '{year}-01-01'"
    papers_prompt += f"\nLimit: {result_count}"
    
    federation_prompts["papers"] = papers_prompt
    
    # Citations database prompt (if citation priority)
    if citation_priority:
        citations_prompt = f"""
        Query citations database for impact analysis.
        Schema: citations(paper_id, citing_paper_id, citation_count, impact_factor)
        Join with paper IDs from primary query results.
        Focus: High-impact papers with citation_count > 10
        """
        federation_prompts["citations"] = citations_prompt
    
    # Authors database prompt (for comprehensive analysis)
    authors_prompt = f"""
    Query authors database for researcher information.
    Schema: authors(author_id, author_name, affiliation, h_index)
    Match authors from paper results for institutional analysis.
    """
    federation_prompts["authors"] = authors_prompt
    
    return federation_prompts

def create_integrated_prompt(decomposed_query: Dict[str, Any], 
                           papers_results: List[Any],
                           citations_results: List[Any] = None,
                           authors_results: List[Any] = None) -> str:
    """
    Create integrated analysis prompt combining all federated query results.
    
    This addresses the integration requirement from guideline (c).
    """
    
    topic = decomposed_query.get('topic', 'research area')
    
    prompt = f"""
Comprehensive Research Analysis: {topic}

FEDERATED QUERY RESULTS INTEGRATION:

1. PAPERS DATA ({len(papers_results)} results):
"""
    
    # Add paper summaries
    for i, paper in enumerate(papers_results[:5]):
        if isinstance(paper, dict):
            title = paper.get('title', 'Unknown')
            year = paper.get('pub_date', 'Unknown')
            prompt += f"   - {title} ({year})\n"
        else:
            prompt += f"   - Paper {i+1}: {str(paper)[:100]}\n"
    
    # Add citation data if available
    if citations_results:
        prompt += f"\n2. CITATION IMPACT DATA ({len(citations_results)} citations):\n"
        prompt += "   - Citation patterns and impact metrics integrated\n"
    
    # Add author data if available
    if authors_results:
        prompt += f"\n3. AUTHOR NETWORK DATA ({len(authors_results)} authors):\n"
        prompt += "   - Research collaboration and institutional analysis\n"
    
    prompt += f"""

ANALYSIS REQUIREMENTS:
1. Synthesize findings across all federated data sources
2. Identify research trends and methodological patterns
3. Evaluate research impact using integrated citation metrics
4. Highlight key innovations and breakthrough contributions
5. Suggest future research directions based on gap analysis

Provide a comprehensive analysis that demonstrates the value of federated query processing.
"""
    
    return prompt

def get_prompt_rewriting_config():
    """Get configuration for prompt rewriting optimization."""
    return {
        "max_prompt_length": int(os.environ.get("MAX_PROMPT_LENGTH", "2000")),
        "analysis_depth": os.environ.get("ANALYSIS_DEPTH", "comprehensive"),
        "federation_strategy": os.environ.get("FEDERATION_STRATEGY", "parallel"),
        "prompt_template_version": os.environ.get("PROMPT_TEMPLATE_VERSION", "v2.0")
    }