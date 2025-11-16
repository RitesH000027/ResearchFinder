# LLM-based query parsing using Groq AI (Free)
import re
import os
import requests
import json
from typing import Dict, Any, Optional

# Groq API configuration (Free)
GROQ_API_BASE_URL = "https://api.groq.com/openai/v1"
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
GROQ_MODEL = "llama-3.1-8b-instant"  # Current free model

def _call_groq_api(prompt: str, max_tokens: int = 256) -> Optional[str]:
    """Call Groq AI API for text generation (Free)."""
    if not GROQ_API_KEY:
        print("Groq API key not found. Get free key from https://console.groq.com/")
        return None
    
    try:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": GROQ_MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": "You are an expert SQL generator for academic paper databases. Generate clean, syntactically correct PostgreSQL queries. Only return the SQL query without explanations."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": max_tokens,
            "temperature": 0.1,
            "stream": False
        }
        
        response = requests.post(
            f"{GROQ_API_BASE_URL}/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"].strip()
        else:
            print(f"Groq API error: {response.status_code} - {response.text[:100]}")
            return None
            
    except Exception as e:
        print(f"Groq API call failed: {e}")
        return None


def parse_query_with_llm(query):
    """Parse a natural language query using Groq AI to generate SQL.

    If Groq AI is not available, this function returns an empty `structured` SQL 
    value and a simple `unstructured` fallback so the rest of the pipeline can 
    continue using pattern-based parsing.
    """
    # Enhanced prompt for better SQL generation
    prompt = f"""Convert this natural language query into a PostgreSQL SELECT statement.

Query: "{query}"

Database Schema:
- Table: papers
- Columns: id (TEXT), title (TEXT), author (TEXT), pub_date (DATE), venue (TEXT), type (TEXT)

Rules:
1. Use only the 'papers' table
2. ALWAYS search the 'title' field for topics/keywords: title ILIKE '%keyword%'
3. Use ILIKE for case-insensitive text matching on titles
4. For multiple keywords, use OR: title ILIKE '%word1%' OR title ILIKE '%word2%'
5. ALWAYS include LIMIT clause (default 5): LIMIT 5
6. Extract number from queries like "find 10 papers" for LIMIT clause: LIMIT 10
7. For date filters with specific years, use: AND pub_date >= '2020-01-01'
8. For citation-related queries (most cited, highly cited), add /* SORT_BY_CITATIONS */ comment at start BUT do NOT add date filters
9. For citation queries, use larger LIMIT (10-20) to get more papers for citation sorting
10. Return only the SQL query, no explanation or markdown
11. Example: "machine learning" → SELECT id, title, author, pub_date, venue, type FROM papers WHERE title ILIKE '%machine%' OR title ILIKE '%learning%' LIMIT 5
12. Example: "most cited machine learning" → /* SORT_BY_CITATIONS */ SELECT id, title, author, pub_date, venue, type FROM papers WHERE title ILIKE '%machine%' OR title ILIKE '%learning%' LIMIT 15

SQL Query:"""

    try:
        # Call Groq AI API
        result = _call_groq_api(prompt, max_tokens=200)
        
        if result:
            # Clean up the result - remove markdown formatting if present
            sql = result.replace('```sql', '').replace('```', '').strip()
            
            # Remove any trailing semicolon
            if sql.endswith(';'):
                sql = sql[:-1]
            
            # Validate that it's a proper SQL query
            if "SELECT" in sql.upper() and "FROM" in sql.upper() and "papers" in sql.lower():
                # Additional validation - ensure no invalid table references
                if ('citations' not in sql.lower() or 'join' not in sql.lower()) and 'T1.' not in sql:
                    # Extract intent for result analysis
                    unstructured = extract_intent_from_query(query)
                    return {"structured": sql, "unstructured": unstructured}
        
        # If validation fails, return empty structured query
        print("Groq AI generated invalid SQL or API unavailable, falling back to pattern-based parsing")
        return {"structured": "", "unstructured": f"Summarize papers about {query}"}
        
    except Exception as e:
        print(f"Groq AI parsing error: {e}")
        return {"structured": "", "unstructured": f"Summarize papers about {query}"}

def extract_intent_from_query(query):
    """Extract the research intent from a natural language query"""
    query_lower = query.lower()
    
    # Enhanced topic extraction patterns
    topic_patterns = [
        r'(?:papers|research|articles)\s+(?:about|on)\s+([\w\s-]+?)(?:\s+published|\s+in|\s+from|\s+and|\s+$)',
        r'about\s+([\w\s-]+?)(?:\s+published|\s+in|\s+from|\s+and|\s+$)',
        r'(?:find|get)\s+(?:papers\s+)?(?:about|on)\s+([\w\s-]+?)(?:\s|$)',
        r'most cited papers about\s+([\w\s-]+?)(?:\s|$)'
    ]
    
    topic = "this research area"
    for pattern in topic_patterns:
        topic_match = re.search(pattern, query_lower)
        if topic_match:
            topic = topic_match.group(1).strip()
            break
    
    # Determine analysis type based on query
    if any(word in query_lower for word in ['summarize', 'analyze', 'trends', 'insights']):
        return f"Provide detailed analysis and key insights about {topic} research"
    elif any(word in query_lower for word in ['citations', 'cited', 'impact']):
        return f"Analyze citation patterns and research impact in {topic}"
    else:
        return f"Summarize key findings and developments in {topic}"
