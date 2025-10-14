# LLM-based query parsing using Flan-T5
from transformers import pipeline
import re

# Initialize the language model
llm = pipeline("text2text-generation", model="google/flan-t5-large")

def parse_query_with_llm(query):
    """Parse a natural language query using LLM to generate SQL"""
    # Use a specific prompt that targets only the papers table
    prompt = f"Convert this research paper query to SQL: '{query}'. The database has a 'papers' table with columns: id, title, author, pub_date, venue, type. Generate a SELECT statement for the papers table only."
    
    try:
        # Generate the SQL query
        result = llm(prompt, max_new_tokens=256)[0]['generated_text']
        
        # Validate that it's a proper SQL query
        if "SELECT" in result.upper() and "FROM" in result.upper():
            sql = result
        else:
            sql = ""
        
        # Extract intent for result analysis
        unstructured = extract_intent_from_query(query)
        
        return {
            "structured": sql,
            "unstructured": unstructured
        }
    except Exception as e:
        print(f"LLM parsing error: {e}")
        return {"structured": "", "unstructured": f"Summarize papers about {query}"}

def extract_intent_from_query(query):
    """Extract the research intent from a natural language query"""
    query_lower = query.lower()
    
    # Extract research topic using regex patterns
    topic_match = re.search(r'(?:papers|research|articles)\s+(?:about|on)\s+([\w\s-]+?)(?:\s+published|\s+in|\s+from|\s+and|\s+$)', query_lower)
    if not topic_match:
        topic_match = re.search(r'about\s+([\w\s-]+?)(?:\s+published|\s+in|\s+from|\s+and|\s+$)', query_lower)
    
    topic = topic_match.group(1).strip() if topic_match else "this research area"
    
    return "summarize key findings"
