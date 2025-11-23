#!/usr/bin/env python3
"""
Quick Performance Test for ResearchFinder

This script performs a focused test of key performance metrics to validate
the system is working and measure actual performance.
"""

import time
from pathlib import Path
import sys

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from federated_query.query_parser import extract_query_components
from federated_query.llm_parser import rewrite_query_with_llm

def test_pattern_matching():
    """Test pattern matching with sample queries"""
    
    test_queries = [
        "machine learning algorithms",
        "most cited papers in neural networks",
        "computer vision research after 2020",
        "artificial intelligence papers published in last 5 years",
        "deep learning optimization techniques",
        "quantum computing applications",
        "natural language processing NLP",
        "robotics autonomous systems",
        "cybersecurity network security",
        "blockchain distributed ledger"
    ]
    
    print("🔍 Testing Pattern Matching Performance...")
    print("-" * 50)
    
    successful = 0
    total_time = 0
    
    for i, query in enumerate(test_queries, 1):
        start_time = time.time()
        
        try:
            components = extract_query_components(query)
            processing_time = time.time() - start_time
            total_time += processing_time
            
            # Check if extraction was successful
            success = bool(components.get('topic')) or bool(components.get('year')) or bool(components.get('citation_priority'))
            
            if success:
                successful += 1
                status = "✅"
            else:
                status = "❌"
            
            print(f"{status} Query {i}: '{query}'")
            print(f"   Components: {components}")
            print(f"   Time: {processing_time:.3f}s")
            print()
            
        except Exception as e:
            print(f"❌ Query {i}: ERROR - {e}")
            print()
    
    success_rate = (successful / len(test_queries)) * 100
    avg_time = total_time / len(test_queries)
    
    print("📊 Pattern Matching Results:")
    print(f"   Success Rate: {success_rate:.1f}% ({successful}/{len(test_queries)})")
    print(f"   Average Time: {avg_time:.3f}s")
    print(f"   Target: 87% success rate")
    print(f"   Status: {'✅ PASS' if success_rate >= 80 else '❌ NEEDS IMPROVEMENT'}")
    
    return success_rate, avg_time

def test_query_rewriting():
    """Test query rewriting enhancement"""
    
    test_queries = [
        "find ML stuff from recent years",
        "show me AI papers with lots of citations", 
        "computer vision research in 2023",
        "neural net optimization methods",
        "quantum stuff published lately"
    ]
    
    print("\n✏️  Testing Query Rewriting Performance...")
    print("-" * 50)
    
    improved = 0
    total_time = 0
    
    for i, query in enumerate(test_queries, 1):
        start_time = time.time()
        
        try:
            # Test original query
            original_components = extract_query_components(query)
            original_score = sum([
                0.5 if original_components.get('topic') else 0,
                0.2 if original_components.get('year') else 0,
                0.2 if original_components.get('citation_priority') else 0,
                0.1 if original_components.get('want_summary') else 0
            ])
            
            # Test rewritten query
            rewritten_query = rewrite_query_with_llm(query)
            processing_time = time.time() - start_time
            total_time += processing_time
            
            if rewritten_query and rewritten_query != query:
                rewritten_components = extract_query_components(rewritten_query)
                rewritten_score = sum([
                    0.5 if rewritten_components.get('topic') else 0,
                    0.2 if rewritten_components.get('year') else 0,
                    0.2 if rewritten_components.get('citation_priority') else 0,
                    0.1 if rewritten_components.get('want_summary') else 0
                ])
                
                improvement = rewritten_score > original_score
                if improvement:
                    improved += 1
                    status = "✅"
                else:
                    status = "➡️"
                
                print(f"{status} Query {i}: '{query}'")
                print(f"   Original: {original_components}")
                print(f"   Rewritten: '{rewritten_query}'")
                print(f"   Rewritten Components: {rewritten_components}")
                print(f"   Score: {original_score:.1f} → {rewritten_score:.1f}")
                print(f"   Time: {processing_time:.3f}s")
                
            else:
                print(f"⚠️  Query {i}: No rewriting occurred")
                print(f"   Original: '{query}'")
                print(f"   Time: {processing_time:.3f}s")
            
            print()
            
        except Exception as e:
            print(f"❌ Query {i}: ERROR - {e}")
            print()
    
    improvement_rate = (improved / len(test_queries)) * 100
    avg_time = total_time / len(test_queries)
    
    print("📊 Query Rewriting Results:")
    print(f"   Improvement Rate: {improvement_rate:.1f}% ({improved}/{len(test_queries)})")
    print(f"   Average Time: {avg_time:.3f}s")
    print(f"   Target: 23% improvement rate")
    print(f"   Status: {'✅ PASS' if improvement_rate >= 15 else '❌ NEEDS IMPROVEMENT'}")
    
    return improvement_rate, avg_time

def main():
    print("🚀 ResearchFinder Quick Performance Test")
    print("=" * 60)
    
    try:
        # Test 1: Pattern Matching
        pattern_success, pattern_time = test_pattern_matching()
        
        # Test 2: Query Rewriting (if Groq API is available)
        try:
            rewriting_success, rewriting_time = test_query_rewriting()
        except Exception as e:
            print(f"\n⚠️  Query Rewriting Test Skipped: {e}")
            print("   (This usually means Groq API key is not configured)")
            rewriting_success, rewriting_time = 0, 0
        
        # Summary
        print("\n🎯 Quick Test Summary:")
        print("=" * 30)
        print(f"Pattern Matching: {pattern_success:.1f}% success, {pattern_time:.3f}s avg")
        if rewriting_success > 0:
            print(f"Query Rewriting: {rewriting_success:.1f}% improvement, {rewriting_time:.3f}s avg")
        
        print(f"\n📋 Next Steps:")
        print("1. For complete evaluation, run: python evaluate_performance.py")
        print("2. Ensure database is running for full database performance tests")
        print("3. Configure citation server for citation integration tests")
        print("4. Set GROQ_API_KEY environment variable for LLM features")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()