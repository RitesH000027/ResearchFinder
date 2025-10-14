# This is the central coordinator for my ResearchFinder federated query system
# It handles the flow from user query to structured search and result processing
import sys
import os

# I need to set up the import paths correctly so it works both when run directly 
# and when imported as a module - this was tricky to get right!
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(os.path.dirname(current_dir))

# Import the newly refactored modules - using relative imports
# since we're already in the federated_query package
from .query_parser import extract_query_components
from .sql_builder import build_sql_query
from .citation_analysis import CitationClient
from .results_processor import (
    print_summary_statistics
)

try:
    # Import my other components - each handles a specific part of the pipeline
    from .user_interface import get_user_query
    from .llm_parser import parse_query_with_llm
    from .federated_engine import query_papers_db
    from .llm_postprocess import postprocess_with_llm
except ImportError as e:
    print(f"Import error: {e}")
    print(f"Current sys.path: {sys.path}")
    sys.exit(1)

# This is the central coordinator for my ResearchFinder federated query system
# It handles the flow from user query to structured search and result processing
    
    # Check if this is a citation-focused query
    citation_priority = parsed_query.get('citation_priority', False)
    specific_paper_lookup = parsed_query.get('specific_paper_lookup', False)
    specific_paper_title = parsed_query.get('specific_paper_title', None)
    
    if citation_priority:
        print("🔍 Citation data prioritized for this query")
    
    if specific_paper_lookup and specific_paper_title:
        print(f"🔍 Specific citation lookup for paper: '{specific_paper_title}'")
    
    # Try to use the LLM to parse the query
    llm_parsed = parse_query_with_llm(query)
    structured_query = llm_parsed.get('structured', '').strip()
    
    # Check if the LLM query is valid, otherwise use our pattern-based approach
    if not structured_query or ('citations' in structured_query.lower() and 'join' in structured_query.lower()):
        print("⚠️ Using pattern-based SQL generation instead of LLM")
        structured_query = build_sql_query(parsed_query, query)
    
    print(f"SQL query: {structured_query}")

def run_query():
    """
    Main function for processing research queries.
    """
    # Get the query from command line or user input
    if len(sys.argv) > 1:
        query = ' '.join(sys.argv[1:])
        print(f"Using command line query: {query}")
    else:
        query = get_user_query()
    
    # Parse the query to extract structured components
    parsed_query = extract_query_components(query)
    
    # Check if this is a citation-focused query
    citation_priority = parsed_query.get('citation_priority', False)
    specific_paper_lookup = parsed_query.get('specific_paper_lookup', False)
    specific_paper_title = parsed_query.get('specific_paper_title', None)
    
    if citation_priority:
        print("🔍 Citation data prioritized for this query")
    
    if specific_paper_lookup and specific_paper_title:
        print(f"🔍 Specific citation lookup for paper: '{specific_paper_title}'")
    
    # Try to use the LLM to parse the query
    llm_parsed = parse_query_with_llm(query)
    structured_query = llm_parsed.get('structured', '').strip()
    
    # Check if the LLM query is valid
    use_pattern_based = False
    if not structured_query:
        print("⚠️ LLM did not generate a SQL query. Using pattern-based approach.")
        use_pattern_based = True
    elif 'citations' in structured_query.lower() and 'join' in structured_query.lower():
        print("⚠️ LLM generated SQL with 'citations' table reference. Using pattern-based approach.")
        use_pattern_based = True
    elif 'T1.' in structured_query or 'paper_id' in structured_query.lower():
        print("⚠️ LLM generated SQL with incorrect column references. Using pattern-based approach.")
        use_pattern_based = True
        
    # Use our pattern-based SQL builder if the LLM query has issues
    if use_pattern_based:
        structured_query = build_sql_query(parsed_query, query)
    
    print(f"SQL query: {structured_query}")
    
    # Query the papers database
    papers_results = query_papers_db(structured_query)
    
    # Get paper IDs from the result for citation analysis
    paper_ids = []
    if papers_results:
        paper_ids = [str(row[0]) for row in papers_results if len(row) > 0]
    
    # Initialize the citation client
    citation_client = CitationClient()
    
    # Process citations if we have paper IDs
    papers_with_citations = []
    if paper_ids:
        print(f"🔍 Finding citations for {len(paper_ids)} papers...")
        
        # Determine how many papers to process for citations based on priority
        sample_size = 10 if citation_priority else 5
        
        try:
            # Process each paper and add citation data
            for i, row in enumerate(papers_results[:sample_size]):
                # Make sure we have results and the row has content
                if not row or len(row) < 1:
                    continue
                    
                paper_id = str(row[0]) if len(row) > 0 else None
                
                if paper_id:
                    # Create a dictionary from the row - with careful handling of null values
                    paper_dict = {
                        'id': paper_id,
                        'title': str(row[1]) if len(row) > 1 and row[1] is not None else 'Unknown',
                        'author': str(row[2]) if len(row) > 2 and row[2] is not None else '',
                        'pub_date': row[3] if len(row) > 3 and row[3] is not None else None,
                        'venue': str(row[4]) if len(row) > 4 and row[4] is not None else '',
                        'type': str(row[5]) if len(row) > 5 and row[5] is not None else '',
                    }
                    
                    # Get citation data for this paper using the paper ID
                    # since the DOI field doesn't exist in the database
                    if paper_dict.get('id'):
                        citation_data = citation_client.get_citations_for_paper(paper_dict['id'])
                        paper_dict['citation_count'] = citation_data.get('citation_count', 0)
                        paper_dict['citations'] = citation_data.get('citations', [])
                        paper_dict['citation_source'] = citation_data.get('source', 'unknown')
                    
                    papers_with_citations.append(paper_dict)
            
            # Sort papers by citations if this is a citation priority query
            if citation_priority:
                papers_with_citations = citation_client.sort_papers_by_citations(papers_with_citations)
                print("📊 Results sorted by citation count (highest first)")
        
        except Exception as e:
            print(f"⚠️ Error processing citations: {e}")
    
    # Print the raw results for reference
    print("\n=== PAPERS FOUND ===")
    if papers_results:
        for i, row in enumerate(papers_results[:10]):  # Show up to 10 papers
            title = str(row[1])[:100] if len(row) > 1 else 'N/A'
            pub_date = str(row[3])[:10] if len(row) > 3 else 'N/A'
            print(f"[{i+1}] {title} ({pub_date})")
    else:
        print("No papers found matching your query.")
    
    # For specific paper citation lookup, show focused results
    if specific_paper_lookup and specific_paper_title:
        # Filter papers that match the requested title
        matching_papers = [p for p in papers_with_citations 
                          if specific_paper_title.lower() in p.get('title', '').lower()]
        
        if matching_papers:
            print(f"\n🔍 CITATION COUNT FOR REQUESTED PAPER(S):")
            for paper in matching_papers:
                print(f"\nPaper: {paper.get('title', 'Unknown')}")
                print(f"Citation count: {paper.get('citation_count', 0)} (Source: {paper.get('citation_source', 'unknown')})")
                
                # Show a few citing papers if available
                citations = paper.get('citations', [])
                if citations:
                    print("Sample citing papers:")
                    for i, citation in enumerate(citations[:3]):  # Show up to 3 citations
                        cite_title = citation.get('title', citation.get('citing_paper_title', 'Unknown paper'))
                        cite_date = citation.get('citation_date', citation.get('citing_paper_year', 'Unknown date'))
                        print(f"  - {cite_title} ({cite_date})")
            print("\n" + "-"*50)  # Add a separator line
    
    # Extract time period information for display
    year = parsed_query.get('year')
    time_period = f"from {year} onwards" if year else "in recent years"
    
    # Extract topic for display
    topic = parsed_query.get('topic', 'this research area')
    
    # Display formatted results
    print(f"Found {len(papers_results)} papers about '{topic}' published {time_period}.\n")
    
    # Print each paper in a readable format
    for i, paper in enumerate(papers_with_citations[:10]):
        print(f"[{i+1}] Title: {paper.get('title', 'N/A')}")
        print(f"    Date: {paper.get('pub_date', 'N/A')}")
        author = paper.get('author', '')
        if author:
            print(f"    Author: {author[:100]}")
        if citation_priority and 'citation_count' in paper:
            print(f"    Citations: {paper.get('citation_count', 0)}")
        print("")
    
    # Process unstructured query part with LLM for research analysis
    print("=== RESEARCH ANALYSIS ===")
    unstructured_instruction = llm_parsed.get('unstructured', f"Summarize papers about {topic}")
    print(f"Analysis goal: {unstructured_instruction}")
    
    # Create a list of paper titles for analysis
    paper_titles = [p.get('title', '') for p in papers_with_citations]
    
    # Use the LLM for analysis
    llm_analysis = postprocess_with_llm(paper_titles, unstructured_instruction)
    print(llm_analysis)
    
    # Print summary statistics
    print_summary_statistics(papers_with_citations, query)
    
    return papers_with_citations

def main():
    """
    Entry point for the script.
    """
    try:
        results = run_query()
        print("\nQuery processed successfully!")
        return results
    except Exception as e:
        print(f"Error processing query: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return None

if __name__ == "__main__":
    # If this module is run directly, use absolute imports
    # This allows the module to be run as: python -m federated_query.main
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    try:
        # Try absolute imports for direct execution
        from federated_query.user_interface import get_user_query
        from federated_query.llm_parser import parse_query_with_llm
        from federated_query.federated_engine import query_papers_db
        from federated_query.llm_postprocess import postprocess_with_llm
    except ImportError as e:
        print(f"Error when importing modules for direct execution: {e}")
        sys.exit(1)
    
    main()
