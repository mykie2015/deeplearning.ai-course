#!/usr/bin/env python
"""
Alternative runner with visible input handling
Uses readline for better terminal interaction
"""
import sys
import os

# Ensure unbuffered output
os.environ['PYTHONUNBUFFERED'] = '1'

# Try to enable readline for better input handling
try:
    import readline
    readline.parse_and_bind('tab: complete')
except ImportError:
    pass

# Import and run the flow
from deep_research_flow.main import kickoff

if __name__ == "__main__":
    print("Starting Deep Research Flow with visible input mode...")
    print("(If you still can't see input, try running in a different terminal)")
    print()
    
    try:
        kickoff()
    except KeyboardInterrupt:
        print("\n\nFlow interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError running flow: {e}")
        sys.exit(1)

