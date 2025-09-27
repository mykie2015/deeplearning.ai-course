# Building and Evaluating Data Agents

A comprehensive DeepLearning.AI course on creating sophisticated multi-agent systems that can work with various data sources and evaluate their performance using advanced metrics.

## 🎯 Course Overview

This course teaches you how to build production-ready data agents that can:
- **Research and analyze data** from multiple sources (web, databases, documents)
- **Generate visualizations** and charts from structured data
- **Evaluate agent performance** using the Goal-Plan-Act (GPA) framework
- **Handle complex queries** requiring coordination between multiple specialized agents

## 🏗️ Architecture

The system implements a **planner-executor-agent pattern**:

### Core Components

1. **Planner**: Creates step-by-step plans to answer user queries
2. **Executor**: Decides which agent to run next and handles dynamic replanning
3. **Specialized Agents**:
   - **Web Researcher**: Uses Tavily to search public information
   - **Cortex Researcher**: Queries private enterprise data in Snowflake
   - **Chart Generator**: Creates visualizations using Python
   - **Chart Summarizer**: Generates captions for visualizations
   - **Synthesizer**: Combines results into coherent final answers

### Advanced Features

- **Dynamic replanning**: Agents can revise their approach if initial plans fail
- **State management**: Shared memory across all agents in the workflow
- **Enterprise integration**: Real connection to Snowflake for business data
- **Comprehensive evaluation**: Multiple metrics for agent performance assessment

## 🧠 Agent's GPA Framework

![Agent GPA Framework](gpa-framework.png)

The course introduces the **Goal-Plan-Act (GPA) alignment framework** for evaluating agent effectiveness:

### Evaluation Metrics

- **Plan Quality**: How well-structured and logical is the agent's plan?
- **Plan Adherence**: Does the agent follow its planned steps?
- **Execution Efficiency**: How efficiently does the agent complete tasks?
- **Logical Consistency**: Are the agent's actions logically coherent?

### RAG Triad Metrics

- **Groundedness**: Are responses supported by retrieved context?
- **Answer Relevance**: How relevant are answers to the user's question?
- **Context Relevance**: How relevant is retrieved context to the question?

## 🛠️ Technologies Used

- **LangGraph** - Multi-agent workflow orchestration
- **OpenAI GPT models** (including o3 for advanced reasoning)
- **Snowflake Cortex** - Enterprise data access (structured & unstructured)
- **TruLens** - Agent evaluation and monitoring
- **Tavily Search** - Web research capabilities
- **Python visualization libraries** - Chart generation

## 📚 Course Structure

### Lesson 2: Construct a Multi-Agent Workflow
- Build a planning system that breaks down complex queries
- Create specialized agents for different data tasks
- Implement an executor for agent coordination
- Handle replanning when approaches fail

### Lesson 3: Expand Data Agent Capabilities
- Add Snowflake Cortex agents for enterprise data
- Combine structured (CRM) and unstructured (meeting notes) data
- Create sophisticated data analysis capabilities

### Lesson 5: Measure Agent's GPA
- Evaluate Goal-Plan-Act alignment
- Implement comprehensive evaluation metrics
- Use LLM judges for agent performance assessment

## 🚀 Real-World Applications

These agents can be applied to:
- **Business Intelligence**: Answer complex analytical questions
- **Executive Reporting**: Generate reports combining multiple data sources
- **Dashboard Creation**: Build interactive visualizations with explanatory text
- **Iterative Analysis**: Handle follow-up questions and exploratory data analysis
- **Data Lineage**: Provide citations and maintain traceability

## 📋 Requirements

See `requirements.txt` for detailed package dependencies. Key requirements include:

- Python 3.11+
- LangChain ecosystem packages
- Snowflake connectors
- TruLens evaluation framework
- Visualization libraries

## 🔧 Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Configure environment variables (see `env.template`)
4. Set up Snowflake credentials for enterprise data access

## 📊 Example Use Cases

```python
# Complex business query
query = "Chart the current market capitalization of the top 5 banks in the US?"

# Regulatory research
query = "Identify current regulatory changes for the financial services industry in the US."

# Enterprise data analysis
query = "What were the key action items from last quarter's sales meetings?"
```

## 🎓 Learning Outcomes

After completing this course, you'll be able to:
- Design and implement sophisticated multi-agent systems
- Integrate multiple data sources (web, databases, documents)
- Evaluate agent performance using advanced metrics
- Build production-ready agents for enterprise environments
- Apply Goal-Plan-Act alignment principles to improve agent effectiveness

## 📝 Course Files

- `helper.py` - Core agent implementations and utilities
- `prompts.py` - Prompt templates for planner and executor
- `L2/`, `L3/`, `L5/`, `L6/` - Individual lesson notebooks and resources
- `requirements.txt` - Python package dependencies
- `env.template` - Environment variable template

---

*This course represents a sophisticated approach to building production-ready data agents that can handle enterprise-scale challenges while maintaining reliability and explainability.*
