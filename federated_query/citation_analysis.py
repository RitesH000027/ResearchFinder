# This module handles all citation-related functionality
# I designed this to abstract away the complexity of different citation sources

import json
import os
import random
import time
from typing import Dict, Any, List, Optional, Union

import requests

# Define the citation API base URL and API key
CITATION_API_BASE_URL = "https://api.opencitations.net/index/v1"
# Secondary laptop API server (running citation database)
# Updated with the actual IP address of your secondary laptop
LOCAL_API_BASE_URL = "http://192.168.41.167:5000"
# In a real-world scenario, API keys would be stored in environment variables
# but for this academic project, hardcoding is acceptable
CITATION_API_KEY = "d79399f6-349e-49dd-9d01-6e6f4db51595-1764354007"

class CitationClient:
    """
    Client for retrieving citation data from various sources.
    Returns 0 citations when APIs are unavailable.
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
        Returns zero citations if the API call fails or no DOI is found.
        
        Args:
            paper_id: The paper identifier (might contain a DOI or other identifiers)
            
        Returns:
            A dictionary with citation count and details
        """
        if not paper_id or paper_id.lower() == "none" or paper_id.strip() == "":
            return {'citation_count': 0, 'citations': [], 'source': 'no_identifier'}
        
        try:
            # NOTE: removed fixed sleep to improve throughput. Use concurrent fetching instead.
            
            # Paper IDs might be in various formats:
            # - "doi:10.1234/abcd meta:something"  (contains explicit DOI)
            # - "10.1234/abcd"                     (raw DOI)
            # - "orcid:0000-0003-1414-3507 meta:ra/0614082260"  (no DOI)
            # - "meta:ra/061010322262"             (metadata only)
            # - "isbn:9789400767386 doi:10.1007/978-94-007-6738-6"  (DOI after other identifiers)
            
            doi_value = None
            
            # Enhanced DOI extraction with OpenCitations compatibility
            standard_doi = None  # For OpenCitations API
            local_id = None      # For local citation API
            
            # Method 1: Check if paper_id contains OpenCitations ID (meta:br/ format)
            if "meta:br/" in paper_id.lower():
                # Extract the OpenCitations ID after "meta:"
                meta_parts = paper_id.lower().split("meta:")[1].split()
                if meta_parts:
                    local_id = "omid:" + meta_parts[0]  # For local API
            
            # Method 2: Extract standard DOI for OpenCitations (look for "doi:" prefix)
            if "doi:" in paper_id.lower():
                # Extract just the DOI value between "doi:" and the next space or end
                doi_parts = paper_id.lower().split("doi:")[1].split()
                if doi_parts and doi_parts[0].startswith("10."):
                    standard_doi = doi_parts[0]  # For OpenCitations API
                    if not local_id:  # Use as local ID if no meta:br/ found
                        local_id = standard_doi
            
            # Method 3: Check if it looks like a raw DOI (starts with 10.)
            elif paper_id.startswith("10.") and "/" in paper_id:
                standard_doi = paper_id
                local_id = paper_id
            
            # Choose appropriate ID based on API being used
            if self.base_url == LOCAL_API_BASE_URL:
                doi_value = local_id or standard_doi
            else:
                # For OpenCitations, prefer standard DOI format
                doi_value = standard_doi if standard_doi else local_id
            
            # If no identifier found, return zero citations
            if not doi_value:
                print(f"No valid identifier found in: {paper_id}")
                return {'citation_count': 0, 'citations': [], 'source': 'no_identifier'}
            
            # Store the standard DOI for fallback use
            fallback_doi = standard_doi
            
            # Prepare the API endpoint and headers
            # Try both metadata and citations endpoints
            if self.base_url == LOCAL_API_BASE_URL:
                # Local API has a different endpoint structure
                # This matches the routes in your api_server.py
                endpoint = f"{self.base_url}/api/paper/citations/{doi_value}"
            else:
                # OpenCitations API endpoint for citation count
                endpoint = f"{self.base_url}/citation-count/{doi_value}"
                
            headers = {"Accept": "application/json"}
            if self.api_key and self.base_url != LOCAL_API_BASE_URL:
                headers["authorization"] = self.api_key
            
            # Debug info to see what IDs we're using
            print(f"Requesting citation data for ID: {doi_value} (from {paper_id})")
            print(f"Standard DOI extracted: {standard_doi}, Local ID: {local_id}, Fallback DOI: {fallback_doi}")
            
            # Make the API call (timeout configurable via CITATION_TIMEOUT env var)
            timeout_val = int(os.environ.get('CITATION_TIMEOUT', '10'))
            response = requests.get(endpoint, headers=headers, timeout=timeout_val)
            
            if response.status_code == 200:
                data = response.json()
                print(f"API Response for {doi_value}: {data}")
                
                # Handle different response formats based on the API source
                if self.base_url == LOCAL_API_BASE_URL:
                    # Your local API format includes status, count, and citations
                    if data.get('status') == 'ok':
                        citation_count = data.get('count', 0)
                        # If local API returns 0 citations, try OpenCitations as fallback
                        if citation_count == 0 and fallback_doi and fallback_doi.startswith('10.') and '/' in fallback_doi:
                            print(f"Local API returned 0 citations, trying OpenCitations fallback for DOI: {fallback_doi}")
                            opencitations_result = self._get_opencitations_citations(fallback_doi)
                            if opencitations_result['citation_count'] > 0:
                                print(f"OpenCitations fallback found {opencitations_result['citation_count']} citations")
                                return opencitations_result
                        
                        return {
                            'citation_count': citation_count,
                            'citations': data.get('citations', []),
                            'source': 'local_api'
                        }
                else:
                    # OpenCitations API format - returns list with count field
                    if data and isinstance(data, list) and len(data) > 0:
                        raw_count = data[0].get('count', 0)
                        citation_count = int(raw_count)
                        print(f"Parsed citation count: {raw_count} -> {citation_count}")
                        return {
                            'citation_count': citation_count,
                            'citations': [],  # OpenCitations citation-count endpoint doesn't return citation details
                            'source': 'opencitations_api'
                        }
                    else:
                        return {
                            'citation_count': 0,
                            'citations': [],
                            'source': 'opencitations_api'
                        }
            else:
                print(f"Citation API returned status code {response.status_code}")
                
                # Enhanced fallback chain: Local API → OpenCitations → Zero citations
                if self.base_url == CITATION_API_BASE_URL:
                    # Try local API first
                    try:
                        fallback_endpoint = f"{LOCAL_API_BASE_URL}/api/paper/citations/{doi_value}"
                        print(f"Trying local API fallback: {fallback_endpoint}")
                        fallback_timeout = int(os.environ.get('CITATION_FALLBACK_TIMEOUT', '5'))
                        fallback_response = requests.get(fallback_endpoint, timeout=fallback_timeout)
                        
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
                    
                    # If local API fails and we have a standard DOI, try OpenCitations
                    if fallback_doi and fallback_doi.startswith('10.') and '/' in fallback_doi:
                        print(f"Trying OpenCitations API fallback for standard DOI: {fallback_doi}")
                        return self._get_opencitations_citations(fallback_doi)
                elif self.base_url == LOCAL_API_BASE_URL:
                    # If local API failed, try OpenCitations for standard DOIs
                    if fallback_doi and fallback_doi.startswith('10.') and '/' in fallback_doi:
                        print(f"Trying OpenCitations API fallback for standard DOI: {fallback_doi}")
                        return self._get_opencitations_citations(fallback_doi)
                
                # If all APIs fail, return 0 citations
                return {'citation_count': 0, 'citations': [], 'source': 'none'}
        except Exception as e:
            print(f"Error fetching citations: {str(e)}")
            return {'citation_count': 0, 'citations': [], 'source': 'none'}
    
    def get_citations_for_papers(self, paper_dois: List[str]) -> Dict[str, Dict[str, Any]]:
        """
        Get citation data for multiple papers.
        
        Args:
            paper_dois: List of DOIs
            
        Returns:
            A dictionary mapping DOIs to citation data
        """
        # Use a thread pool to fetch multiple citation records concurrently
        from concurrent.futures import ThreadPoolExecutor, as_completed

        max_workers = int(os.environ.get('CITATION_WORKERS', '8'))
        result: Dict[str, Dict[str, Any]] = {}

        with ThreadPoolExecutor(max_workers=max_workers) as ex:
            future_to_doi = {ex.submit(self.get_citations_for_paper, doi): doi for doi in paper_dois}
            for fut in as_completed(future_to_doi):
                doi = future_to_doi[fut]
                try:
                    result[doi] = fut.result()
                except Exception as e:
                    print(f"[!] Citation fetch failed for {doi}: {e}")
                    result[doi] = {'citation_count': 0, 'citations': [], 'source': 'error'}

        return result
    
    def _get_opencitations_citations(self, doi):
        """
        Get detailed citation data from OpenCitations API
        Returns both citation count and citation details
        """
        try:
            headers = {
                "authorization": "d79399f6-349e-49dd-9d01-6e6f4db51595-1764354007",
                "Accept": "application/json"
            }
            
            # First try to get citation count
            count_url = f"https://api.opencitations.net/index/v1/citation-count/{doi}"
            oc_timeout = int(os.environ.get('OPENCITATIONS_TIMEOUT', '10'))
            count_response = requests.get(count_url, headers=headers, timeout=oc_timeout)
            
            citation_count = 0
            if count_response.status_code == 200:
                count_data = count_response.json()
                if count_data and isinstance(count_data, list) and len(count_data) > 0:
                    citation_count = int(count_data[0].get("count", 0))
            
            # If we have citations, try to get detailed citation data
            citations = []
            if citation_count > 0:
                citations_url = f"https://api.opencitations.net/index/v1/citations/{doi}"
                citations_response = requests.get(citations_url, headers=headers, timeout=oc_timeout)
                
                if citations_response.status_code == 200:
                    citations_data = citations_response.json()
                    if citations_data and isinstance(citations_data, list):
                        # Convert OpenCitations format to our format
                        citations = [
                            {
                                'citing_paper': citation.get('citing', ''),
                                'citation_date': citation.get('creation', ''),
                                'source': 'opencitations'
                            }
                            for citation in citations_data[:50]  # Limit to first 50 citations
                        ]
            
            return {
                'citation_count': citation_count,
                'citations': citations,
                'source': 'opencitations_api'
            }
            
        except Exception as e:
            print(f"OpenCitations API error for {doi}: {e}")
            return {
                'citation_count': 0,
                'citations': [],
                'source': 'opencitations_error'
            }
    
    def sort_papers_by_citations(self, papers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Sort a list of papers by their citation counts.
        Papers should already have citation data attached.
        
        Args:
            papers: List of paper dictionaries with citation data
            
        Returns:
            The list of papers sorted by citation count (descending)
        """
        # Papers already have citation data attached by main.py
        # Just sort by existing citation_count field
        return sorted(papers, key=lambda p: p.get('citation_count', 0), reverse=True)
    
