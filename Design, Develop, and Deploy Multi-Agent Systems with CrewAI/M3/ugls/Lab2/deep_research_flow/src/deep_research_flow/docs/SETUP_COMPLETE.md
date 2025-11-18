# Lab 2 Setup Complete ✅

## Overview
Lab 2: **Automatic Deep Research Flow and Observability** is now fully configured and ready to run!

This lab demonstrates how to build an intelligent Flow in CrewAI that:
- **Routes queries** based on complexity (simple vs. research-intensive)
- **Orchestrates a multi-agent crew** for deep research tasks
- **Provides observability** through tracing and monitoring
- **Persists state** across executions

## Architecture

### Flow Structure
```
User Query 
    ↓
Analyze Query (Router)
    ├─→ [SIMPLE] → Direct LLM Answer → Final Answer
    └─→ [RESEARCH] → Clarify Query → Research Crew → Save Report → Final Answer
```

### Multi-Agent Research Crew
When the RESEARCH route is triggered, a 4-agent crew is deployed:

1. **Research Planner** - Breaks query into main and secondary topics
2. **Topic Researcher** - Gathers information using EXA search and web scraping
3. **Fact Checker** - Validates accuracy and identifies misinformation
4. **Report Writer** - Synthesizes findings into comprehensive report

## What Was Completed

### 1. Code Implementation ✅
All missing code in `main.py` has been filled in:
- ✅ Flow state with typed variables (`needs_research`, `research_report`, `final_answer`)
- ✅ `@persist()` decorator for state persistence
- ✅ `@start()` decorator for entry point
- ✅ `@router()` decorator for conditional routing
- ✅ `@listen()` decorators for task dependencies
- ✅ LLM prompts for query analysis and answering
- ✅ Crew kickoff and result handling
- ✅ Report saving and summarization
- ✅ Tracing enabled for monitoring

### 2. Environment Setup ✅
- ✅ `.env` file copied to flow directory
- ✅ Virtual environment created (`venv/`)
- ✅ Dependencies installed (crewai, exa-py, etc.)
- ✅ Project installed in editable mode

### 3. Testing ✅
- ✅ Simple query flow tested successfully
- ✅ Research query flow tested (quantum computing query)
- ✅ All flow paths verified working

## How to Run

### Option 1: Interactive Mode (Recommended for learning)
```bash
cd "/Users/mykielee/GitHub/deeplearning.ai-course/Design, Develop, and Deploy Multi-Agent Systems with CrewAI/M3/ugls/Lab2/deep_research_flow"
./run_interactive.sh
```

This will:
1. Prompt you for a query
2. Analyze complexity
3. Route to appropriate handler
4. Provide final answer with tracing URL

### Option 2: Test Script (Non-interactive)
```bash
cd "/Users/mykielee/GitHub/deeplearning.ai-course/Design, Develop, and Deploy Multi-Agent Systems with CrewAI/M3/ugls/Lab2/deep_research_flow"
source venv/bin/activate

# Test simple query
python test_flow.py simple

# Test research query
python test_flow.py research
```

### Option 3: Direct Command
```bash
cd "/Users/mykielee/GitHub/deeplearning.ai-course/Design, Develop, and Deploy Multi-Agent Systems with CrewAI/M3/ugls/Lab2/deep_research_flow"
source venv/bin/activate
crewai run
```

## Example Queries

### Simple Queries (Direct LLM)
- "Hello, how are you?"
- "What is Python?"
- "Tell me a joke"

### Research Queries (Full Crew)
- "What are the latest developments in quantum computing as of 2024?"
- "Explain recent advancements in AI agents and their applications"
- "What are the current trends in renewable energy technology?"

## Features

### 1. Intelligent Routing
The flow uses GPT-4o-mini to analyze query complexity:
- **SIMPLE**: Quick LLM response (< 1 second)
- **RESEARCH**: Full multi-agent research crew (minutes)

### 2. Clarification Loop
For research queries, the flow may ask clarifying questions:
```
❓ Clarification needed:
Could you specify which aspects of quantum computing you're most interested in?

Please provide more details:
>> 
```

### 3. State Persistence
Each execution is saved with a unique ID:
- Resume conversations across sessions
- Access execution history
- Track state changes

### 4. Observability & Tracing
When tracing is enabled, you get:
- URL to CrewAI platform for monitoring
- Step-by-step execution visualization
- Memory updates and tool usage tracking
- Performance metrics

Example output:
```
╭────────────────────────── Trace Batch Finalization ──────────────────────────╮
│ ✅ Trace batch finalized with session ID:                                    │
│ b30ddc1b-43a0-4e36-b9ea-109b8b8d5145. View here:                             │
│ https://app.crewai.com/crewai_plus/ephemeral_trace_batches/...              │
╰──────────────────────────────────────────────────────────────────────────────╯
```

### 5. Research Output
When research is triggered:
- Parallel research on main and secondary topics
- Multi-source fact-checking
- Comprehensive report saved to `research_report.md`
- Summary provided as final answer

## File Structure
```
deep_research_flow/
├── .env                          # API keys (OpenAI, EXA)
├── venv/                         # Virtual environment
├── run_interactive.sh            # Interactive runner script
├── test_flow.py                  # Non-interactive test script
├── pyproject.toml                # Project configuration
├── knowledge/
│   └── user_preference.txt       # User context for agents
└── src/deep_research_flow/
    ├── main.py                   # Flow definition (✅ COMPLETED)
    ├── utils.py                  # Helper functions
    ├── crews/
    │   └── deep_research_crew/
    │       ├── crew.py           # Crew definition
    │       ├── config/
    │       │   ├── agents.yaml   # Agent configurations
    │       │   └── tasks.yaml    # Task configurations
    │       └── guardrails/
    │           └── guardrails.py # Report validation
    └── tools/
```

## Test Results

### ✅ Simple Query Test
```
Query: "Hello, how are you?"
Route: SIMPLE
Response Time: ~2 seconds
Output: Direct LLM greeting
Status: ✅ PASSED
```

### ✅ Research Query Test
```
Query: "What are the latest developments in quantum computing as of 2024?"
Route: RESEARCH
Steps:
  1. ✅ Research plan created (main + secondary topics)
  2. ✅ Parallel research executed
  3. ✅ Fact-checking completed
  4. ✅ Report generated
Tools Used:
  - EXASearchTool (multiple queries)
  - ScrapeWebsiteTool (content extraction)
Memory: Short-term, long-term, and entity memory utilized
Status: ✅ PASSED
```

## Key Learnings

1. **Flow Decorators** control execution order and dependencies
2. **Router patterns** enable intelligent conditional logic
3. **Persistence** allows resumable conversations
4. **Tracing** provides production-ready monitoring
5. **Parallel execution** improves research efficiency

## Troubleshooting

### SSL Certificate Errors
Some websites (like www.bis.gov) may fail due to SSL issues. The agents handle this gracefully and continue with other sources.

### API Rate Limits
If you see rate limit errors, the flow will retry or use cached results.

### Memory/Performance
Research queries can take 2-5 minutes and use significant tokens. This is expected for comprehensive research.

## Next Steps

1. **Experiment** with different query types
2. **Modify** agent configurations in `agents.yaml`
3. **Customize** task descriptions in `tasks.yaml`
4. **Add** new tools for specialized research
5. **Explore** the tracing dashboard for insights

## Resources

- [CrewAI Documentation](https://docs.crewai.com)
- [CrewAI Flows Guide](https://docs.crewai.com/concepts/flows)
- [Lab 2 Notebook](./C1M3_Lab_2_deep_research_flow.ipynb)

---

**Setup completed by**: Cursor AI Assistant  
**Date**: November 18, 2025  
**Status**: ✅ All tests passing, ready for use

