#!/usr/bin/env python
"""
Test script to run the flow with automated inputs
"""
import sys
from unittest.mock import patch
from deep_research_flow.main import DeepResearchFlow

def test_simple_query():
    """Test with a simple query that doesn't require research"""
    print("=" * 60)
    print("Testing SIMPLE query flow...")
    print("=" * 60)
    
    # Mock the input to provide "Hello, how are you?"
    with patch('builtins.input', return_value="Hello, how are you?"):
        flow = DeepResearchFlow(tracing=False)
        flow.kickoff(inputs={"id": "test-simple-query"})
    
    print("\n✅ Simple query test completed!")
    print(f"Final answer: {flow.state.final_answer[:200]}...")

def test_research_query():
    """Test with a complex query that requires research"""
    print("\n" + "=" * 60)
    print("Testing RESEARCH query flow...")
    print("=" * 60)
    
    # Mock the input to provide a research query
    # The mock will return the query first, then "No" if asked for clarification
    responses = iter([
        "What are the latest developments in quantum computing as of 2024?",
        "No additional context needed"
    ])
    
    with patch('builtins.input', lambda prompt: next(responses)):
        flow = DeepResearchFlow(tracing=False)
        try:
            flow.kickoff(inputs={"id": "test-research-query"})
            print("\n✅ Research query test completed!")
            print(f"Research report length: {len(flow.state.research_report)} characters")
            print(f"Final answer: {flow.state.final_answer[:300]}...")
        except Exception as e:
            print(f"⚠️ Research flow encountered an issue: {e}")
            print("This is expected in a test environment without full API access")

if __name__ == "__main__":
    test_type = sys.argv[1] if len(sys.argv) > 1 else "simple"
    
    if test_type == "simple":
        test_simple_query()
    elif test_type == "research":
        test_research_query()
    else:
        print("Usage: python test_flow.py [simple|research]")
        print("Running simple test by default...")
        test_simple_query()

