# This module handles formatting and processing of query results
# I've separated this to keep the presentation logic distinct from the data retrieval logic

import json
import os
import re
import sys
import time
from datetime import datetime
from typing import Dict, Any, List, Optional, Union

def format_paper_result(paper: Dict[str, Any], include_citation: bool = False) -> str:
    """
    Format a paper result as a readable string.
    
    Args:
        paper: Dictionary with paper details
        include_citation: Whether to include citation information
        
    Returns:
        A formatted string with paper details
    """
    # Start with the paper title
    result = f"Title: {paper.get('title', 'Unknown')}\n"
    
    # Add author information if available
    author = paper.get('author', '')
    if author:
        result += f"Authors: {author}\n"
    
    # Add publication details
    pub_info = []
    if paper.get('venue'):
        pub_info.append(paper.get('venue'))
    if paper.get('pub_date'):
        pub_info.append(str(paper.get('pub_date')))
    if pub_info:
        result += f"Published in: {', '.join(pub_info)}\n"
    
    # Add paper type if available
    if paper.get('type'):
        result += f"Type: {paper.get('type')}\n"
    
    # Add DOI if available
    if paper.get('doi'):
        result += f"DOI: {paper.get('doi')}\n"
    
    # Add citation count if requested and available
    if include_citation and 'citation_count' in paper:
        result += f"Citations: {paper.get('citation_count', 0)}\n"
    
    return result

def format_results_as_text(papers: List[Dict[str, Any]], 
                          query: str, 
                          include_citation: bool = False) -> str:
    """
    Format a list of paper results as a readable text.
    
    Args:
        papers: List of paper dictionaries
        query: The original query string
        include_citation: Whether to include citation information
        
    Returns:
        A formatted text with all results
    """
    if not papers:
        return "No papers found matching your query."
    
    result = f"Found {len(papers)} papers matching your query: \"{query}\"\n\n"
    
    for i, paper in enumerate(papers):
        result += f"--- Result {i+1} ---\n"
        result += format_paper_result(paper, include_citation)
        result += "\n"
    
    return result

def format_results_as_json(papers: List[Dict[str, Any]]) -> str:
    """
    Format papers as a JSON string.
    
    Args:
        papers: List of paper dictionaries
        
    Returns:
        A JSON string representation of the papers
    """
    # Convert datetime objects to strings for JSON serialization
    papers_copy = []
    for paper in papers:
        paper_copy = paper.copy()
        for key, value in paper_copy.items():
            if isinstance(value, datetime):
                paper_copy[key] = value.isoformat()
        papers_copy.append(paper_copy)
    
    return json.dumps(papers_copy, indent=2)

def save_results_to_file(papers: List[Dict[str, Any]], 
                        query: str, 
                        format_type: str = 'text') -> str:
    """
    Save query results to a file.
    
    Args:
        papers: List of paper dictionaries
        query: The original query string
        format_type: The output format ('text' or 'json')
        
    Returns:
        Path to the saved file
    """
    # Create a timestamp for the filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Sanitize the query for use in a filename
    sanitized_query = re.sub(r'[^\w\s-]', '', query)
    sanitized_query = re.sub(r'[-\s]+', '_', sanitized_query)
    sanitized_query = sanitized_query[:30]  # Limit length
    
    # Create the filename
    filename = f"query_results_{sanitized_query}_{timestamp}"
    
    # Format the content based on the requested format
    if format_type.lower() == 'json':
        content = format_results_as_json(papers)
        filename += ".json"
    else:  # Default to text
        content = format_results_as_text(papers, query, include_citation=True)
        filename += ".txt"
    
    # Create the results directory if it doesn't exist
    results_dir = os.path.join(os.getcwd(), 'query_results')
    os.makedirs(results_dir, exist_ok=True)
    
    # Save the file
    file_path = os.path.join(results_dir, filename)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return file_path

def get_result_statistics(papers: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculate statistics about the result set.
    
    Args:
        papers: List of paper dictionaries
        
    Returns:
        Dictionary with statistics about the papers
    """
    stats = {
        'total_papers': len(papers),
        'years': {},
        'venues': {},
        'citation_count': 0
    }
    
    for paper in papers:
        # Track years
        pub_date = paper.get('pub_date')
        if pub_date:
            if hasattr(pub_date, 'year'):
                year = pub_date.year
            else:
                year = str(pub_date).split('-')[0]
            stats['years'][year] = stats['years'].get(year, 0) + 1
        
        # Track venues
        if paper.get('venue'):
            venue = paper.get('venue')
            stats['venues'][venue] = stats['venues'].get(venue, 0) + 1
        
        # Track citation count - only count if citation_count exists and is > 0
        citation_count = paper.get('citation_count', 0)
        if citation_count and citation_count > 0:
            stats['citation_count'] += citation_count
    
    # Calculate the average citations per paper
    if stats['total_papers'] > 0:
        stats['avg_citations'] = stats['citation_count'] / stats['total_papers']
    else:
        stats['avg_citations'] = 0
    
    # Sort years and venues by frequency
    stats['years'] = dict(sorted(stats['years'].items(), key=lambda x: x[1], reverse=True))
    stats['venues'] = dict(sorted(stats['venues'].items(), key=lambda x: x[1], reverse=True))
    
    return stats

def print_summary_statistics(papers: List[Dict[str, Any]], query: str) -> None:
    """
    Print a summary of statistics about the result set.
    
    Args:
        papers: List of paper dictionaries
        query: The original query string
    """
    if not papers:
        print("No papers found to generate statistics.")
        return
    
    stats = get_result_statistics(papers)
    
    # All citation data is now real from secondary machine
    
    print(f"\n--- Summary Statistics for Query: \"{query}\" ---")
    print(f"Total papers found: {stats['total_papers']}")
    
    # All citation data is real now, always show stats
    print(f"Total citations: {stats['citation_count']}")
    print(f"Average citations per paper: {stats['avg_citations']:.2f}")
    
    print("\nPublication Years:")
    for year, count in list(stats['years'].items())[:5]:  # Show top 5 years
        print(f"  {year}: {count} papers")
    
    print("\nTop Venues:")
    for venue, count in list(stats['venues'].items())[:3]:  # Show top 3 venues
        print(f"  {venue}: {count} papers")
    
    print("\n" + "-" * 50)