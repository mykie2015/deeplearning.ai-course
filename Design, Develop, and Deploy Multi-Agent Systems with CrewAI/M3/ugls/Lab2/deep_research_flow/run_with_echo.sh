#!/bin/bash
# Alternative runner that ensures input echoing is enabled

cd "$(dirname "$0")"

# Enable terminal echoing
stty echo 2>/dev/null || true

# Activate virtual environment
source venv/bin/activate

# Run with unbuffered output
python -u -c "from deep_research_flow.main import kickoff; kickoff()"

