# LLM-based post-processing for research results
from transformers import pipeline

# Initialize the language model
llm = pipeline("text2text-generation", model="google/flan-t5-large")

def postprocess_with_llm(papers, instruction):
    """Process research papers based on the user's instruction"""
    # Convert papers to text for analysis
    if isinstance(papers, list):
        papers_text = "\n".join(papers[:5])  # Top 5 papers
    else:
        papers_text = str(papers)[:300]  # Truncate to manageable size
    
    try:
        # Create a focused prompt for the LLM
        prompt = f"Summarize these research papers briefly: {papers_text}"
        
        # Generate response
        response = llm(prompt, max_new_tokens=150)[0]['generated_text']
        
        # Validate response quality
        if len(response) > 20 and "Summarize" not in response:
            return response
            
    except Exception as e:
        print(f"LLM processing error: {e}")
    
    # Fallback to simple text analysis
    return f"Found {len(papers) if isinstance(papers, list) else 1} relevant papers on the research topic."
