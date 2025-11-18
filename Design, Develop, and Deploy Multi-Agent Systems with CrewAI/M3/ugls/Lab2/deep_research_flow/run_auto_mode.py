#!/usr/bin/env python
"""
Auto-mode runner - skips clarifications and proceeds automatically
Good for unattended runs or when input visibility is an issue
"""
import sys
import os
from unittest.mock import patch

# Ensure unbuffered output
os.environ['PYTHONUNBUFFERED'] = '1'

from deep_research_flow.main import DeepResearchFlow

def run_auto_research(query):
    """Run research with automatic clarification skipping"""
    print(f"🤖 AUTO MODE: Running research for query:")
    print(f"   \"{query}\"\n")
    print("⚙️  Clarifications will be automatically skipped")
    print("="*70)
    
    # Mock input to automatically provide query and skip clarifications
    inputs = [query, "skip"]  # First input is query, second is "skip" for clarification
    input_iter = iter(inputs)
    
    def mock_readline():
        try:
            value = next(input_iter)
            print(f"[AUTO-PROVIDED: {value}]")
            return value + "\n"
        except StopIteration:
            return "skip\n"  # Default to skip for any additional inputs
    
    with patch('sys.stdin.readline', mock_readline):
        flow = DeepResearchFlow(tracing=True)
        try:
            flow.kickoff(inputs={"id": "auto-research-flow"})
            print("\n" + "="*70)
            print("✅ Auto-mode research completed!")
            print("="*70)
        except Exception as e:
            print(f"\n❌ Error during auto-mode research: {e}")
            raise

if __name__ == "__main__":
    # Check if query provided as command line argument
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        # Interactive query input
        print("🤖 AUTO-MODE RESEARCH RUNNER")
        print("="*70)
        print("This mode will automatically skip clarifications and proceed with research.\n")
        query = input("Enter your research query: ")
    
    if not query.strip():
        print("❌ No query provided. Exiting.")
        sys.exit(1)
    
    try:
        run_auto_research(query)
    except KeyboardInterrupt:
        print("\n\n⚠️  Research interrupted by user.")
        sys.exit(0)

