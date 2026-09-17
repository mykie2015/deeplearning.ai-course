# ADP Module 3: Tool Use Design Pattern

## Module summary
This module dives into the use of tools within agentic workflows, covering paradigms that include defining tool sets and instructing AI on tool calls. It explores syntaxes like the OpenAI and AI Suite open-source package syntaxes, and discusses emerging paradigms where AIs execute code (e.g., Python) to interface with tools.


## Proposed videos
- Video 1: Unpacking Tool Use in Agentic Workflows
- Video 2: Functions into tools
- Video 3: Tool use in AISuite
- Video 4: OpenAI function calling
- Video 5: Pydantic and tool use (Optional)
- Video 6: MCP as the future of tools?
- Video 7: Implementing tools in research workflow

## Proposed teaching notebooks
- Video 3 notebook (aisuite)
- Video 4 notebook (OpenAI function calling)

## Proposed labs
- Ungraded lab 1 (Functions to tools)
- Graded lab 1 (Implement functions)
- Graded lab 2 (Implement tools for research agent)

## Proposed Activities

### email_agent
Focused LLM tool implementation with `aisuite`, including frontend UI and notebook interface for backend interaction. Demonstrates how to build function calling tools for email operations (send, search, read, mark as read/unread) with a complete FastAPI service integration.

### graded_labs
Research agent implementation using external API tools for web search and academic research. Shows how to define and register tools for information gathering, with structured output generation and quality evaluation mechanisms.

### sql-agent
Database interaction through tool use, comparing OpenAI function calling vs AISuite approaches. Demonstrates dynamic schema exploration tools, SQL query generation functions, and safe database operation patterns with multiple notebook implementations.

