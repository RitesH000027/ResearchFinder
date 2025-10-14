# I've created this module to handle natural language query parsing
# It's responsible for extracting structured information from user queries
# This separation helps keep the codebase maintainable and focused

import re
import datetime
from typing import Dict, Any, Optional, Tuple

def extract_topic_and_time(query: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Extract research topic and time constraints from a natural language query.
    Returns a tuple of (topic, year) where either could be None if not found.
    
    This is my core parsing logic for getting structured data from natural queries.
    """
    query_lower = query.lower()
    topic = None
    year = None
    
    # I spent a lot of time crafting these patterns to catch different ways users phrase queries
    topic_patterns = [
        r'about\s+([\w\s\-\'"]+?)(?:\s+published|\s+in|\s+from|\s+and|\s+with|\s+since|\s+$)',
        r'on\s+([\w\s\-\'"]+?)(?:\s+published|\s+in|\s+from|\s+and|\s+with|\s+since|\s+$)',
        r'papers\s+(?:on|about)\s+([\w\s\-\'"]+?)(?:\s+published|\s+in|\s+from|\s+and|\s+with|\s+since|\s+$)',
        r'most cited papers about\s+([\w\s\-\'"]+?)(?:\s+published|\s+in|\s+from|\s+since|\s+$)',
        r'papers about\s+([\w\s\-\'"]+?)(?:\s+with|\s+that|\s+published|\s+in|\s+from|\s+since|\s+$)',
        r'top\s+\d+\s+(?:papers|articles)\s+(?:on|about)\s+([\w\s\-\'"]+?)(?:\s+published|\s+in|\s+from|\s+since|\s+$)',
        r'find\s+(?:papers|articles)\s+(?:on|about)\s+([\w\s\-\'"]+?)(?:\s+published|\s+in|\s+from|\s+since|\s+$)'
    ]
    
    # Try each pattern in sequence - stop when we find a match
    for pattern in topic_patterns:
        m = re.search(pattern, query_lower)
        if m:
            topic = m.group(1).strip()
            break
    
    # Special case: If user starts with "find" but doesn't match other patterns
    if not topic and "find" in query_lower:
        m = re.search(r'find\s+(?:papers\s+(?:on|about)\s+)?([\w\s-]+?)(?:\s+published|\s+in|\s+from|\s+and|\s+$)', query_lower)
        if m:
            topic = m.group(1).strip()
    
    # Time constraints are critical for research queries
    # Users often want recent papers, so I handle relative and absolute time references
    if "last 5 years" in query_lower or "past 5 years" in query_lower:
        # Dynamic calculation based on current year - makes the system future-proof
        current_year = datetime.datetime.now().year
        year = str(current_year - 5)
    else:
        # Look for explicit years like "2023" or "published in 2020"
        m = re.search(r'(\d{4})', query_lower)
        if m:
            year = m.group(1)
            
    return (topic, year)

def detect_citation_focus(query: str) -> bool:
    """
    Determine if a query is focused on citation metrics.
    Returns True if the query is asking about citations.
    """
    query_lower = query.lower()
    citation_keywords = [
        'most cited', 'top cited', 'highest cited', 'citation', 
        'citations', 'cited papers', 'with more than', 'at least'
    ]
    
    return any(keyword in query_lower for keyword in citation_keywords)

def extract_specific_paper_title(query: str) -> Optional[str]:
    """
    Extract a specific paper title from queries asking about citation counts for a specific paper.
    Returns the paper title or None if not found.
    """
    query_lower = query.lower()
    
    # These patterns identify queries asking about specific papers' citation counts
    specific_paper_citation_patterns = [
        r'how many citations does (the paper|the article)?\s+[\'"]([^\'"]*)[\'"]\s+have',
        r'citation count (of|for) (the paper|the article)?\s+[\'"]([^\'"]*)[\'"]\s*',
        r'number of citations (of|for) (the paper|the article)?\s+[\'"]([^\'"]*)[\'"]\s*'
    ]
    
    for pattern in specific_paper_citation_patterns:
        match = re.search(pattern, query_lower)
        if match:
            # Extract the paper title from the pattern match
            # If pattern has 3 groups, paper title is in group 2, otherwise it's in group 1
            return match.group(3) if len(match.groups()) > 2 else match.group(2)
            
    return None

def extract_query_components(query: str) -> Dict[str, Any]:
    """
    Main entry point for parsing a natural language query.
    Returns a dictionary with extracted components.
    """
    topic, year = extract_topic_and_time(query)
    citation_priority = detect_citation_focus(query)
    specific_paper_title = extract_specific_paper_title(query) if citation_priority else None
    
    result = {
        'topic': topic,
        'year': year,
        'citation_priority': citation_priority,
        'specific_paper_lookup': specific_paper_title is not None,
        'specific_paper_title': specific_paper_title
    }
    
    return result