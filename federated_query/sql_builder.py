# This module handles the conversion from parsed query components to SQL
# I've separated this from the parsing logic to make the code more maintainable
# The SQL builder focuses on generating optimized database queries

import re
from typing import Dict, Any, List, Optional

def build_topic_condition(topic: str) -> str:
    """
    Create SQL condition for a research topic, with special handling for common research areas and misspellings.
    Returns a SQL condition string for use in WHERE clause.
    """
    if not topic:
        return ""
    
    topic_lower = topic.lower()
        
    # Misspelling correction mapping
    misspelling_map = {
        'machien learning': 'machine learning',
        'machin learning': 'machine learning', 
        'masheen learning': 'machine learning',
        'artifical intelligence': 'artificial intelligence',
        'artficial intelligence': 'artificial intelligence',
        'artificial intellgence': 'artificial intelligence',
        'neaural network': 'neural network',
        'neaural networks': 'neural networks',
        'deep learnign': 'deep learning',
        'dep learning': 'deep learning',
        'quantam computing': 'quantum computing',
        'quantum computng': 'quantum computing',
        'computor vision': 'computer vision',
        'natrual language processing': 'natural language processing'
    }
    
    # Apply spelling correction
    normalized_topic = misspelling_map.get(topic_lower, topic_lower)
        
    # My solution for handling domain-specific queries with synonyms and related terms
    if "neural network" in normalized_topic or "neural networks" in normalized_topic:
        return "(title ILIKE '%neural network%' OR title ILIKE '%neural networks%' OR title ILIKE '%deep learning%' OR title ILIKE '%CNN%' OR title ILIKE '%RNN%' OR title ILIKE '%LSTM%')"
    elif "machine learning" in normalized_topic:
        return "(title ILIKE '%machine learning%' OR title ILIKE '%ml%' OR title ILIKE '%data mining%' OR title ILIKE '%supervised learning%' OR title ILIKE '%classification%')"
    elif "quantum computing" in normalized_topic or "quantum computer" in normalized_topic:
        return "(title ILIKE '%quantum%' OR title ILIKE '%qubit%' OR title ILIKE '%quantum computer%' OR title ILIKE '%quantum algorithm%')"
    elif "natural language processing" in normalized_topic or "nlp" in normalized_topic:
        return "(title ILIKE '%natural language%' OR title ILIKE '%nlp%' OR title ILIKE '%language model%' OR title ILIKE '%text mining%' OR title ILIKE '%sentiment analysis%')"
    elif "artificial intelligence" in normalized_topic or "ai" == normalized_topic:
        return "(title ILIKE '%artificial intelligence%' OR title ILIKE '%AI %' OR title ILIKE '% AI %' OR title ILIKE '%machine intelligence%')"
    elif "computer vision" in normalized_topic or "image recognition" in normalized_topic:
        return "(title ILIKE '%computer vision%' OR title ILIKE '%image recognition%' OR title ILIKE '%object detection%' OR title ILIKE '%image classification%')"
    else:
        # For topics without special handling, use a direct ILIKE match
        # Always sanitize inputs to prevent SQL injection
        sanitized_topic = topic.replace("'", "''")
        return f"title ILIKE '%{sanitized_topic}%'"

def build_year_condition(year: str) -> str:
    """
    Create SQL condition for time constraints.
    Returns a SQL condition string for use in WHERE clause.
    """
    if not year:
        return ""
    
    return f"pub_date >= '{year}-01-01' AND pub_date <= '2025-12-31'"

def build_specific_paper_query(paper_title: str, result_count: int = 5) -> str:
    """
    Create a SQL query to find a specific paper by its title.
    Returns a complete SQL query string.
    
    Updated to specify column names explicitly for compatibility with the database schema.
    """
    if not paper_title:
        return ""
    
    # Sanitize the paper title to prevent SQL injection
    sanitized_title = paper_title.replace("'", "''")
    return f"SELECT id, title, author, pub_date, venue, type FROM papers WHERE title ILIKE '%{sanitized_title}%' AND pub_date <= '2025-12-31' LIMIT {result_count}"

def build_fallback_keyword_query(query: str) -> str:
    """
    Create a SQL query using keywords from the original query when structured parsing fails.
    Returns a SQL condition string for use in WHERE clause.
    """
    query_lower = query.lower()
    
    # Extract meaningful words (length > 3) and filter out common stop words
    words = [word for word in re.findall(r'\b\w+\b', query_lower) 
             if len(word) > 3 and word not in (
                 'find', 'about', 'papers', 'and', 'the', 'their', 'explain', 
                 'published', 'most', 'cited', 'with', 'more', 'than', 'least', 
                 'top', 'since', 'from'
             )]
    
    if not words:
        return ""
    
    # Use up to 3 keywords to avoid overly restrictive queries
    like_conditions = [f"title ILIKE '%{word}%'" for word in words[:3]]
    return " OR ".join(like_conditions)

def build_sql_query(parsed_query: Dict[str, Any], original_query: str) -> str:
    """
    Build a complete SQL query from parsed components.
    Returns a SQL query string ready for execution.
    
    Updated to ensure compatibility with the database schema.
    """
    # Handle specific paper lookup as a special case
    if parsed_query.get('specific_paper_lookup'):
        result_count = parsed_query.get('result_count', 5)
        return build_specific_paper_query(parsed_query.get('specific_paper_title', ''), result_count)
    
    # Start building the general query - explicitly list the columns we need
    # Use only the columns that actually exist in the database:
    # id, title, author, pub_date, venue, volume, issue, page, type, publisher, editor
    sql = "SELECT id, title, author, pub_date, venue, type FROM papers"
    conditions = []
    
    # Add topic condition if available
    topic = parsed_query.get('topic')
    if topic:
        conditions.append(build_topic_condition(topic))
    
    # Add year condition if available
    year = parsed_query.get('year')
    if year:
        conditions.append(build_year_condition(year))
    else:
        # Always add date validation to filter out invalid future dates
        conditions.append("pub_date <= '2025-12-31'")
    
    # Add citation priority marker if needed
    if parsed_query.get('citation_priority'):
        sql = "/* SORT_BY_CITATIONS */ " + sql
    
    # Assemble the final query with conditions
    if conditions:
        sql += " WHERE " + " AND ".join(conditions)
    elif original_query:  # Fallback to keywords if no structured conditions
        fallback_condition = build_fallback_keyword_query(original_query)
        if fallback_condition:
            sql += f" WHERE {fallback_condition}"
    
    # Use the user-specified count or default to 5
    result_count = parsed_query.get('result_count', 5)
    
    # Add ORDER BY for citation queries to ensure consistent results
    if parsed_query.get('citation_priority'):
        sql += " ORDER BY pub_date DESC"
    
    sql += f" LIMIT {result_count}"
    
    return sql