# This module handles all citation-related functionality
# I designed this to abstract away the complexity of different citation sources

import json
import os
import random
import time
from typing import Dict, Any, List, Optional, Union

import requests

# Define the citation API base URL and API key
CITATION_API_BASE_URL = "https://api.opencitations.net/v1"
# Secondary laptop API server (running citation database)
# Updated with the actual IP address of your secondary laptop
LOCAL_API_BASE_URL = "http://192.168.41.167:5000"
# In a real-world scenario, API keys would be stored in environment variables
# but for this academic project, hardcoding is acceptable
CITATION_API_KEY = ""

class CitationClient:
    """
    Client for retrieving citation data from various sources.
    Falls back to simulated data when the API is unavailable.
    """
    
    def __init__(self, base_url: Optional[str] = None):
        """
        Initialize the citation client with the API base URL.
        Tries local server first, then falls back to public API.
        """
        # Try to use local server first if available
        if base_url:
            self.base_url = base_url
        else:
            # Try local server first
            try:
                # Use the correct health endpoint from your API server
                response = requests.get(f"{LOCAL_API_BASE_URL}/api/status", timeout=1)
                if response.status_code == 200:
                    print("Using local citation API server at", LOCAL_API_BASE_URL)
                    self.base_url = LOCAL_API_BASE_URL
                else:
                    self.base_url = CITATION_API_BASE_URL
            except Exception as e:
                # If local server not available, use public API
                print(f"Cannot connect to local citation API: {str(e)}")
                self.base_url = CITATION_API_BASE_URL
        
        self.api_key = CITATION_API_KEY
        
    def get_citations_for_paper(self, paper_id: str) -> Dict[str, Any]:
        """
        Get citation count and details for a paper using its identifier.
        Falls back to simulated citation data if the API call fails or no DOI is found.
        
        Args:
            paper_id: The paper identifier (might contain a DOI or other identifiers)
            
        Returns:
            A dictionary with citation count and details
        """
        if not paper_id or paper_id.lower() == "none" or paper_id.strip() == "":
            return self._generate_simulated_citation_data()
        
        try:
            # Add a small delay to avoid overwhelming the API
            time.sleep(0.5)
            
            # Paper IDs might be in various formats:
            # - "doi:10.1234/abcd meta:something"  (contains explicit DOI)
            # - "10.1234/abcd"                     (raw DOI)
            # - "orcid:0000-0003-1414-3507 meta:ra/0614082260"  (no DOI)
            # - "meta:ra/061010322262"             (metadata only)
            # - "isbn:9789400767386 doi:10.1007/978-94-007-6738-6"  (DOI after other identifiers)
            
            doi_value = None
            
            # Method 1: Check if paper_id contains OpenCitations ID (meta:br/ format)
            if "meta:br/" in paper_id.lower():
                # Extract the OpenCitations ID after "meta:"
                meta_parts = paper_id.lower().split("meta:")[1].split()
                doi_value = meta_parts[0] if meta_parts else None
                # Remove "meta:" prefix to get just "br/xxxx"
                if doi_value and doi_value.startswith("br/"):
                    doi_value = "omid:" + doi_value  # Citation DB expects "omid:br/xxxx"
            # Method 2: Check if paper_id contains "doi:" prefix (fallback)
            elif "doi:" in paper_id.lower():
                # Extract just the DOI value between "doi:" and the next space or end
                doi_parts = paper_id.lower().split("doi:")[1].split()
                doi_value = doi_parts[0] if doi_parts else None
            # Method 3: Check if it looks like a raw DOI (starts with 10.)
            elif paper_id.startswith("10."):
                doi_value = paper_id
            
            # If no identifier found, fall back to simulated data
            if not doi_value:
                print(f"No valid identifier found in: {paper_id}")
                return self._generate_simulated_citation_data()
            
            # Prepare the API endpoint and headers
            # Try both metadata and citations endpoints
            if self.base_url == LOCAL_API_BASE_URL:
                # Local API has a different endpoint structure
                # This matches the routes in your api_server.py
                endpoint = f"{self.base_url}/api/paper/citations/{doi_value}"
            else:
                endpoint = f"{self.base_url}/metadata/{doi_value}"
                
            headers = {"Accept": "application/json"}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            
            # Debug info to see what IDs we're using
            print(f"Requesting citation data for ID: {doi_value} (from {paper_id})")
            
            # Make the API call
            response = requests.get(endpoint, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Handle different response formats based on the API source
                if self.base_url == LOCAL_API_BASE_URL:
                    # Your local API format includes status, count, and citations
                    if data.get('status') == 'ok':
                        return {
                            'citation_count': data.get('count', 0),
                            'citations': data.get('citations', []),
                            'source': 'local_api'
                        }
                else:
                    # OpenCitations API format
                    return {
                        'citation_count': data.get('citation_count', 0),
                        'citations': data.get('citations', []),
                        'source': 'citations_api'
                    }
            else:
                print(f"Citation API returned status code {response.status_code}")
                
                # If using the public API, try the local API as fallback
                if self.base_url == CITATION_API_BASE_URL:
                    try:
                        fallback_endpoint = f"{LOCAL_API_BASE_URL}/api/paper/citations/{doi_value}"
                        print(f"Trying local API fallback: {fallback_endpoint}")
                        fallback_response = requests.get(fallback_endpoint, timeout=5)
                        
                        if fallback_response.status_code == 200:
                            data = fallback_response.json()
                            if data.get('status') == 'ok':
                                return {
                                    'citation_count': data.get('count', 0),
                                    'citations': data.get('citations', []),
                                    'source': 'local_api'
                                }
                    except Exception as e:
                        print(f"Local API fallback failed: {str(e)}")
                
                # If all APIs fail, use simulated data
                return self._generate_simulated_citation_data()
                
                # If all APIs fail, use simulated data
                return self._generate_simulated_citation_data()
        except Exception as e:
            print(f"Error fetching citations: {str(e)}")
            return self._generate_simulated_citation_data()
    
    def get_citations_for_papers(self, paper_dois: List[str]) -> Dict[str, Dict[str, Any]]:
        """
        Get citation data for multiple papers.
        
        Args:
            paper_dois: List of DOIs
            
        Returns:
            A dictionary mapping DOIs to citation data
        """
        result = {}
        
        for doi in paper_dois:
            result[doi] = self.get_citations_for_paper(doi)
        
        return result
    
    def sort_papers_by_citations(self, papers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Sort a list of papers by their citation counts.
        
        Args:
            papers: List of paper dictionaries
            
        Returns:
            The list of papers sorted by citation count (descending)
        """
        # Get citation data for each paper that has a DOI
        papers_with_citations = []
        for paper in papers:
            paper_with_citation = paper.copy()
            doi = paper.get('doi', None)
            
            if doi:
                citation_data = self.get_citations_for_paper(doi)
                paper_with_citation['citation_count'] = citation_data.get('citation_count', 0)
            else:
                # No DOI available, use simulated data
                citation_data = self._generate_simulated_citation_data()
                paper_with_citation['citation_count'] = citation_data.get('citation_count', 0)
            
            papers_with_citations.append(paper_with_citation)
        
        # Sort the papers by citation count (higher first)
        return sorted(papers_with_citations, key=lambda p: p.get('citation_count', 0), reverse=True)
    
    def _generate_simulated_citation_data(self) -> Dict[str, Any]:
        """
        Generate simulated citation data when the API is unavailable.
        
        Returns:
            A dictionary with simulated citation count and details
        """
        # Generate a realistic citation count (usually follows a power law distribution)
        citation_count = int(random.paretovariate(2.5) * 10)
        
        # Generate some fake citing papers
        fake_citations = []
        for i in range(min(citation_count, 5)):  # Show at most 5 citations in the fake data
            fake_citations.append({
                'citing_paper_title': f"Simulated citing paper #{i+1}",
                'citing_paper_doi': f"10.1000/sim.{random.randint(1000, 9999)}",
                'citing_paper_year': random.randint(2015, 2023)
            })
        
        return {
            'citation_count': citation_count,
            'citations': fake_citations,
            'source': 'simulated'
        }