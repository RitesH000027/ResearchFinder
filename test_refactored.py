#!/usr/bin/env python
"""
Test script for the refactored ResearchFinder system.
This script validates that the modularized code works correctly.
"""

import os
import sys

# Add the parent directory to the system path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from federated_query.query_parser import extract_query_components
from federated_query.sql_builder import build_sql_query
from federated_query.citation_analysis import CitationClient
from federated_query.results_processor import format_paper_result
from federated_query.main import run_query
# Import other required modules
from federated_query.user_interface import get_user_query

def test_query_parser():
    """Test the query parser module."""
    print("\n=== Testing Query Parser ===")
    
    # Test cases
    queries = [
        "Find papers about quantum computing",
        "Show me the most cited papers about neural networks from 2020",
        "How many citations does the paper 'Attention Is All You Need' have?",
        "Research on artificial intelligence in the last 5 years"
    ]
    
    for query in queries:
        print(f"\nQuery: {query}")
        parsed = extract_query_components(query)
        print(f"Extracted topic: {parsed.get('topic')}")
        print(f"Year constraint: {parsed.get('year')}")
        print(f"Citation priority: {parsed.get('citation_priority')}")
        print(f"Specific paper lookup: {parsed.get('specific_paper_lookup')}")
        if parsed.get('specific_paper_title'):
            print(f"Paper title: {parsed.get('specific_paper_title')}")

def test_sql_builder():
    """Test the SQL builder module."""
    print("\n=== Testing SQL Builder ===")
    
    # Test cases
    test_cases = [
        {
            "parsed_query": {"topic": "quantum computing", "year": "2020", "citation_priority": False},
            "original_query": "Find papers about quantum computing published since 2020"
        },
        {
            "parsed_query": {"topic": "neural networks", "year": None, "citation_priority": True},
            "original_query": "Most cited papers about neural networks"
        },
        {
            "parsed_query": {"specific_paper_lookup": True, "specific_paper_title": "Attention Is All You Need"},
            "original_query": "How many citations does the paper 'Attention Is All You Need' have?"
        }
    ]
    
    for tc in test_cases:
        print(f"\nOriginal query: {tc['original_query']}")
        sql = build_sql_query(tc["parsed_query"], tc["original_query"])
        print(f"Generated SQL: {sql}")

def test_citation_analysis():
    """Test the citation analysis module."""
    print("\n=== Testing Citation Analysis ===")
    
    client = CitationClient()
    print("Citation client initialized")
    
    # Test with a real DOI and simulated data
    test_dois = ["10.1038/s41586-020-2649-2", "non-existent-doi"]
    
    for doi in test_dois:
        print(f"\nFetching citations for DOI: {doi}")
        citation_data = client.get_citations_for_paper(doi)
        print(f"Citation count: {citation_data.get('citation_count')}")
        print(f"Data source: {citation_data.get('source')}")
        print(f"Sample citations: {len(citation_data.get('citations', []))}")

def test_result_formatting():
    """Test the result formatting functionality."""
    print("\n=== Testing Result Formatting ===")
    
    # Create a sample paper
    paper = {
        'title': 'Quantum Machine Learning for Data Classification',
        'authors': 'Smith, J., Johnson, M., Williams, R.',
        'pub_date': '2022-06-15',
        'venue': 'Nature Quantum Computing',
        'abstract': 'This paper explores the applications of quantum computing to machine learning tasks, focusing on classification problems.',
        'doi': '10.1234/quantum.2022.123456',
        'citation_count': 42
    }
    
    print("\nFormatted paper result:")
    formatted = format_paper_result(paper, include_citation=True)
    print(formatted)

def main():
    """Run all the tests."""
    print("=== ResearchFinder Modularization Tests ===")
    
    test_query_parser()
    test_sql_builder()
    test_citation_analysis()
    test_result_formatting()
    
    print("\n=== Tests completed ===")
    
    # Run a full query if requested
    if "--run-query" in sys.argv:
        print("\n=== Running a full query test ===")
        try:
            # Import necessary modules for running a query
            from federated_query.user_interface import get_user_query
            from federated_query.llm_parser import parse_query_with_llm
            from federated_query.federated_engine import query_papers_db
            from federated_query.llm_postprocess import postprocess_with_llm
            
            # Now run the query
            run_query()
        except ImportError as e:
            print(f"Error when importing modules for query: {e}")
            print("Try using the run_research_query.py script instead.")

if __name__ == "__main__":
    main()