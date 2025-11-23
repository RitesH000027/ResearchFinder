# LLM-based post-processing for research results using Groq AI (Free)
import os
import requests
import json
from typing import List, Union, Any

# Groq API configuration (Free)
GROQ_API_BASE_URL = "https://api.groq.com/openai/v1"
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
GROQ_MODEL = "llama-3.1-8b-instant"  # Current free model

def _call_groq_analysis(prompt: str, max_tokens: int = 400) -> str:
    """Call Groq AI API for research analysis (Free)."""
    if not GROQ_API_KEY:
        return "Groq API key not configured. Get free key from https://console.groq.com/"
    
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
                    "content": "You are an expert research analyst specializing in academic paper analysis. Provide insightful, concise analysis of research trends, methodologies, and key findings. Focus on identifying patterns, innovations, and research directions."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            "max_tokens": max_tokens,
            "temperature": 0.3,
            "stream": False
        }
        
        response = requests.post(
            f"{GROQ_API_BASE_URL}/chat/completions",
            headers=headers,
            json=data,
            timeout=45
        )
        
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"].strip()
        else:
            return f"Groq API error: {response.status_code} - {response.text[:100]}"
            
    except Exception as e:
        return f"Analysis unavailable: {str(e)[:100]}"

def postprocess_with_llm(papers: Union[List[str], List[Any]], instruction: str) -> str:
    """Process research papers using Groq AI based on the user's instruction."""
    
    # Prepare paper data for analysis
    if isinstance(papers, list) and len(papers) > 0:
        # Handle list of paper titles or paper objects
        if isinstance(papers[0], str):
            papers_text = papers[:5]  # Top 5 paper titles
        else:
            # Extract titles from paper objects/dictionaries
            papers_text = []
            for paper in papers[:5]:
                if isinstance(paper, dict):
                    title = paper.get('title', 'Unknown Title')
                    year = paper.get('pub_date', 'Unknown Year')
                    citations = paper.get('citation_count', 0)
                    papers_text.append(f"'{title}' ({year}) - {citations} citations")
                else:
                    papers_text.append(str(paper))
    else:
        return "No papers available for analysis."
    
    # Create comprehensive analysis prompt
    papers_list = "\n".join([f"{i+1}. {paper}" for i, paper in enumerate(papers_text)])
    
    prompt = f"""As an expert research analyst, provide a comprehensive analysis of these research papers for {instruction}:

{papers_list}

Generate a detailed research summary with the following sections:

**RESEARCH OVERVIEW & THEMES:**
- Identify main research domains and emerging themes
- Highlight cross-cutting methodological approaches
- Note publication timeline and research evolution

**KEY FINDINGS & INNOVATIONS:**
- Summarize major breakthroughs or novel contributions
- Identify methodological innovations and technical advances
- Highlight practical applications and industry impact

**RESEARCH LANDSCAPE ANALYSIS:**
- Analyze citation patterns and research impact
- Identify leading research venues and publication trends
- Note collaboration patterns and geographic distribution

**FUTURE DIRECTIONS & GAPS:**
- Identify research gaps and unexplored areas
- Suggest future research directions based on current trends
- Highlight emerging challenges and opportunities

Provide detailed, insightful analysis in 4-5 well-structured paragraphs that would be valuable for academic presentations and research planning."""

        # Call Groq AI for comprehensive analysis
    analysis = _call_groq_analysis(prompt, max_tokens=800)    # Validate and return analysis
    if len(analysis) > 50 and "error" not in analysis.lower()[:20]:
        return analysis
    else:
        # Fallback analysis
        paper_count = len(papers_text)
        total_citations = 0
        
        # Calculate citation stats if available
        for paper in papers[:5]:
            if isinstance(paper, dict) and 'citation_count' in paper:
                total_citations += paper.get('citation_count', 0)
        
        fallback = f"""Research Analysis Summary:
        
Found {paper_count} relevant papers spanning recent research developments. """
        
        if total_citations > 0:
            avg_citations = total_citations / paper_count
            fallback += f"These papers have received {total_citations} total citations (average: {avg_citations:.1f} per paper), indicating significant research impact. "
        
        fallback += f"The papers represent diverse approaches and methodologies in the field, contributing to our understanding of current research directions and emerging trends."
        
        return fallback
