#!/bin/bash

# Building and Evaluating Data Agents - Quick Start Script
echo "🚀 Building and Evaluating Data Agents - Course Setup"
echo "======================================================"

# Activate virtual environment
echo "📦 Activating virtual environment..."
source /Users/mykielee/GitHub/deeplearning.ai-course/.venv/bin/activate

# Change to course directory
cd "/Users/mykielee/GitHub/deeplearning.ai-course/Building and Evaluating Data Agents"

# Run environment test
echo ""
echo "🧪 Testing environment..."
python test_environment.py

echo ""
echo "📚 Available lessons:"
echo "  L2: Construct a Multi-Agent Workflow"
echo "  L3: Expand Data Agent Capabilities (requires Snowflake)"
echo "  L4: Additional lesson materials"  
echo "  L5: Measure Agent's GPA (requires Snowflake)"
echo "  L6: Advanced topics"

echo ""
echo "🎯 To start a lesson:"
echo "  cd L2 && jupyter lab L2.ipynb"
echo ""
echo "⚙️  Configuration notes:"
echo "  - OpenAI API: ✅ Configured"
echo "  - Tavily API: ⚠️  Add your key to .env files for web search"
echo "  - Snowflake: ⚠️  Add credentials to .env files for L3+ lessons"
echo ""