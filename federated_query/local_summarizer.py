# Local summarization without external APIs
import re
from typing import List, Dict, Any, Union
from collections import Counter

def extract_keywords(text: str) -> List[str]:
    """Extract important keywords from text."""
    # Remove common stop words
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
        'by', 'from', 'up', 'about', 'into', 'through', 'during', 'before', 'after',
        'above', 'below', 'between', 'among', 'is', 'are', 'was', 'were', 'be', 'been',
        'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
        'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those'
    }
    
    # Extract words (alphanumeric sequences)
    words = re.findall(r'\b[a-zA-Z][a-zA-Z0-9]*\b', text.lower())
    
    # Filter out stop words and short words
    keywords = [word for word in words if len(word) > 3 and word not in stop_words]
    
    return keywords

def find_common_themes(papers: List[Dict[str, Any]]) -> Dict[str, int]:
    """Find common themes across paper titles."""
    all_keywords = []
    
    for paper in papers:
        title = paper.get('title', '')
        keywords = extract_keywords(title)
        all_keywords.extend(keywords)
    
    # Count keyword frequency
    keyword_counts = Counter(all_keywords)
    
    # Return top themes
    return dict(keyword_counts.most_common(10))

def analyze_temporal_trends(papers: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze publication trends over time."""
    year_counts = {}
    recent_papers = []
    
    for paper in papers:
        pub_date = paper.get('pub_date')
        if pub_date:
            if hasattr(pub_date, 'year'):
                year = pub_date.year
            else:
                year = int(str(pub_date).split('-')[0]) if str(pub_date).split('-')[0].isdigit() else None
            
            if year:
                year_counts[year] = year_counts.get(year, 0) + 1
                if year >= 2020:  # Recent papers
                    recent_papers.append(paper)
    
    return {
        'year_distribution': year_counts,
        'recent_papers_count': len(recent_papers),
        'publication_span': max(year_counts.keys()) - min(year_counts.keys()) if year_counts else 0
    }

def analyze_venues(papers: List[Dict[str, Any]]) -> Dict[str, int]:
    """Analyze publication venues."""
    venue_counts = {}
    
    for paper in papers:
        venue = paper.get('venue', '')
        if venue:
            # Clean venue name
            venue_clean = re.sub(r'\[.*?\]', '', venue).strip()
            venue_counts[venue_clean] = venue_counts.get(venue_clean, 0) + 1
    
    return dict(Counter(venue_counts).most_common(5))

def generate_local_summary(papers: List[Dict[str, Any]], instruction: str) -> str:
    """Generate a summary using local analysis without external APIs."""
    
    if not papers:
        return "No papers found to analyze."
    
    # Extract basic statistics
    total_papers = len(papers)
    
    # Analyze themes
    common_themes = find_common_themes(papers)
    
    # Analyze temporal trends
    temporal_analysis = analyze_temporal_trends(papers)
    
    # Analyze venues
    venue_analysis = analyze_venues(papers)
    
    # Calculate citation statistics (if available)
    total_citations = sum(paper.get('citation_count', 0) for paper in papers)
    avg_citations = total_citations / total_papers if total_papers > 0 else 0
    
    # Generate summary based on instruction type
    summary_parts = []
    
    # Header
    if "summarize" in instruction.lower() or "summary" in instruction.lower():
        summary_parts.append(f"**Research Summary: {total_papers} Papers Analyzed**")
    elif "analyze" in instruction.lower():
        summary_parts.append(f"**Research Analysis: {total_papers} Papers**")
    else:
        summary_parts.append(f"**Research Overview: {total_papers} Papers**")
    
    # Key themes
    if common_themes:
        theme_list = [f"{theme} ({count})" for theme, count in list(common_themes.items())[:5]]
        summary_parts.append(f"**Key Research Themes:** {', '.join(theme_list)}")
    
    # Temporal trends
    if temporal_analysis['year_distribution']:
        years = sorted(temporal_analysis['year_distribution'].keys())
        year_range = f"{min(years)}-{max(years)}" if len(years) > 1 else str(years[0])
        recent_count = temporal_analysis['recent_papers_count']
        summary_parts.append(f"**Publication Timeline:** {year_range} ({recent_count} papers from 2020 onwards)")
    
    # Top venues
    if venue_analysis:
        top_venues = list(venue_analysis.keys())[:3]
        summary_parts.append(f"**Primary Venues:** {', '.join(top_venues)}")
    
    # Citation impact
    if total_citations > 0:
        summary_parts.append(f"**Research Impact:** {total_citations:,} total citations, averaging {avg_citations:.1f} per paper")
    
    # Research insights based on themes
    insights = []
    theme_words = list(common_themes.keys())[:10]
    
    if any(word in theme_words for word in ['neural', 'network', 'deep', 'learning']):
        insights.append("Strong focus on neural networks and deep learning methodologies")
    
    if any(word in theme_words for word in ['machine', 'algorithm', 'classification']):
        insights.append("Emphasis on machine learning algorithms and classification techniques")
    
    if any(word in theme_words for word in ['medical', 'clinical', 'patient', 'diagnosis']):
        insights.append("Significant medical and clinical applications")
    
    if any(word in theme_words for word in ['optimization', 'performance', 'efficiency']):
        insights.append("Focus on optimization and performance improvement")
    
    if insights:
        summary_parts.append(f"**Research Insights:** {'; '.join(insights)}")
    
    # Construct final summary
    summary = "\n\n".join(summary_parts)
    
    # Add a conclusion
    if temporal_analysis['recent_papers_count'] > total_papers * 0.5:
        summary += f"\n\n**Conclusion:** This represents active, contemporary research with {temporal_analysis['recent_papers_count']} recent publications, indicating ongoing development in this field."
    else:
        summary += f"\n\n**Conclusion:** This research spans {temporal_analysis['publication_span']} years, showing the evolution and maturity of the field."
    
    return summary

def postprocess_with_local_llm(papers: Union[List[str], List[Any]], instruction: str) -> str:
    """Process research papers using local analysis instead of external APIs."""
    
    # Convert paper titles to paper objects if needed
    if isinstance(papers, list) and len(papers) > 0:
        if isinstance(papers[0], str):
            # Convert titles to basic paper objects
            paper_objects = []
            for i, title in enumerate(papers[:10]):  # Limit to first 10
                paper_objects.append({
                    'title': title,
                    'pub_date': '2023-01-01',  # Default date
                    'citation_count': 0
                })
            papers = paper_objects
    
    return generate_local_summary(papers, instruction)