#!/usr/bin/env python
"""
Direct query runner - bypasses all input issues
Just edit the QUERY variable below and run!
"""
import os
os.environ['PYTHONUNBUFFERED'] = '1'

from deep_research_flow.main import DeepResearchFlow
from unittest.mock import patch

# ============================================================================
# EDIT YOUR QUERY HERE:
# ============================================================================
QUERY = "Why is playing tennis hard? Check the latest things happening in tennis world of 2025 November and give me the report"

# Auto-skip clarifications? (True = skip, False = ask for clarification)
AUTO_SKIP_CLARIFICATIONS = True
# ============================================================================

def run_direct():
    """Run flow with pre-set query"""
    print("="*70)
    print("🚀 DIRECT QUERY MODE")
    print("="*70)
    print(f"\n📋 Query: {QUERY}")
    print(f"⚙️  Auto-skip clarifications: {AUTO_SKIP_CLARIFICATIONS}")
    print("\n" + "="*70 + "\n")
    
    # Prepare mock inputs
    inputs = [QUERY]
    if AUTO_SKIP_CLARIFICATIONS:
        inputs.append("skip")  # Auto-skip any clarifications
    
    input_iter = iter(inputs)
    
    def mock_readline():
        """Mock stdin.readline"""
        try:
            value = next(input_iter)
            print(f"[AUTO-PROVIDED: {value}]")
            return value + "\n"
        except StopIteration:
            return "skip\n"  # Default to skip
    
    with patch('sys.stdin.readline', mock_readline):
        flow = DeepResearchFlow(tracing=True)
        flow.kickoff(inputs={"id": "direct-query-flow"})

if __name__ == "__main__":
    print("\n" + "🔧 " + "="*68)
    print("   To change the query, edit QUERY variable at the top of this file")
    print("   " + "="*68 + "\n")
    
    try:
        run_direct()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        raise

