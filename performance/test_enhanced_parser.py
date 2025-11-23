#!/usr/bin/env python3
"""
Test Enhanced Query Parser Performance
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from federated_query.enhanced_query_parser import extract_query_components

def test_enhanced_parser():
    """Test the enhanced parser with the same queries that failed before"""
    
    test_queries = [
        # Basic topic queries (these were failing at 40% rate)
        "machine learning algorithms",
        "neural network research", 
        "computer vision papers",
        "artificial intelligence",
        "deep learning models",
        "quantum computing applications",
        "natural language processing",
        "robotics systems",
        "cybersecurity research",
        "blockchain technology",
        
        # Citation-focused queries
        "most cited machine learning papers",
        "highly cited AI research", 
        "top cited neural networks",
        "best papers in computer vision",
        "influential deep learning studies",
        
        # Temporal queries
        "machine learning papers after 2020",
        "AI research from 2021 to 2024",
        "neural networks published in last 5 years",
        "computer vision research since 2019",
        "quantum computing papers from recent years",
        
        # Complex queries
        "most cited machine learning papers published after 2020",
        "artificial intelligence research with high citations",
        "neural network optimization techniques from 2023",
        "computer vision applications in medical imaging",
        "deep learning for natural language processing"
    ]
    
    print("🚀 Testing Enhanced Query Parser")
    print("=" * 60)
    
    successful = 0
    total = len(test_queries)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\nTest {i}: '{query}'")
        
        try:
            components = extract_query_components(query)
            
            # Success criteria: At least one meaningful component extracted
            success = (
                bool(components.get('topic')) or 
                bool(components.get('year')) or 
                bool(components.get('citation_priority'))
            )
            
            if success:
                successful += 1
                status = "✅ SUCCESS"
                extracted = []
                if components.get('topic'): 
                    extracted.append(f"Topic: '{components['topic']}'")
                if components.get('year'): 
                    extracted.append(f"Year: {components['year']}")
                if components.get('citation_priority'): 
                    extracted.append("Citations: True")
                
                print(f"{status} - {', '.join(extracted)}")
            else:
                status = "❌ FAILED"
                print(f"{status} - No meaningful components extracted")
                
        except Exception as e:
            print(f"❌ ERROR - {e}")
    
    # Calculate results
    success_rate = (successful / total) * 100
    
    print("\n" + "=" * 60)
    print("📊 ENHANCED PARSER RESULTS")
    print("=" * 60)
    print(f"Success Rate: {success_rate:.1f}% ({successful}/{total})")
    print(f"Target: 87%")
    print(f"Status: {'✅ EXCEEDS TARGET' if success_rate >= 87 else '❌ BELOW TARGET'}")
    
    if success_rate >= 87:
        print("\n🎉 Enhanced parser ready for integration!")
        print("This parser can replace the current one to achieve target metrics.")
    else:
        print(f"\n⚠️ Parser needs further improvement to reach 87% target")
    
    return success_rate

if __name__ == "__main__":
    test_enhanced_parser()