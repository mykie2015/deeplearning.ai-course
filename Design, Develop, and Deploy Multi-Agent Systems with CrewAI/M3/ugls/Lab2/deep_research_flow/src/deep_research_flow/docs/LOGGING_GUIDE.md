# Enhanced Logging Guide

The Deep Research Flow now includes detailed logging at every step to help you understand what's happening during execution.

## Log Output Structure

### For SIMPLE Queries

```
======================================================================
🔍 Deep Research Flow started
======================================================================

❓ What would you like to know?
>> Hello!

✅ Query received: "Hello!"
----------------------------------------------------------------------

🤔 STEP 1: Analyzing query complexity...
   Query: "Hello!"
   🔄 Calling LLM to analyze...

💬 DECISION: Simple query - Using SIMPLE route
   ↳ Will use direct LLM answer
----------------------------------------------------------------------

✨ STEP 2: Generating direct answer...
   🔄 Calling GPT-4o-mini...
   ✅ Answer generated successfully
----------------------------------------------------------------------

======================================================================
📝 FINAL ANSWER
======================================================================

📌 Original Query: "Hello!"

----------------------------------------------------------------------

Hello! How can I assist you today?

======================================================================
✨ Deep Research Flow completed!
======================================================================
```

### For RESEARCH Queries

```
======================================================================
🔍 Deep Research Flow started
======================================================================

💭 Previous query: why tennis playing is hard

❓ What would you like to know?
>> What are the latest developments in AI agents?

✅ Query received: "What are the latest developments in AI agents?"
----------------------------------------------------------------------

🤔 STEP 1: Analyzing query complexity...
   Query: "What are the latest developments in AI agents?"
   🔄 Calling LLM to analyze...

📚 DECISION: Complex query - Initiating RESEARCH route
   ↳ Will deploy 4-agent research crew
----------------------------------------------------------------------

🔍 STEP 2: Reviewing query for research clarity...
   🔄 Analyzing if query needs clarification...
   ✅ Query is clear - proceeding to research
----------------------------------------------------------------------

🚀 STEP 3: Executing deep research crew...
======================================================================
📋 RESEARCH QUERY:
   What are the latest developments in AI agents?
======================================================================

👥 Deploying 4-Agent Research Crew:
   1️⃣  Research Planner - Breaking query into topics
   2️⃣  Topic Researcher - Gathering information (EXA + Web Scraping)
   3️⃣  Fact Checker - Validating accuracy
   4️⃣  Report Writer - Synthesizing findings

⏳ This may take 2-5 minutes. Please wait...

----------------------------------------------------------------------

[CrewAI's detailed agent logs will appear here showing:]
- Research Planner creating plan
- Topic Researcher searching and scraping
- Fact Checker validating
- Report Writer synthesizing

======================================================================
✅ Research completed successfully!
   📊 Report length: 15432 characters
======================================================================

💾 STEP 4: Saving report and creating summary...
----------------------------------------------------------------------
✅ Report saved successfully!
   📁 Location: /Users/.../deep_research_flow/src/research_report.md

📝 Generating executive summary...
   🔄 Calling GPT-4o-mini to summarize...
   ✅ Summary generated
----------------------------------------------------------------------

======================================================================
📝 FINAL ANSWER
======================================================================

📌 Original Query: "What are the latest developments in AI agents?"

----------------------------------------------------------------------

This is a summary of the final answer:

Recent developments in AI agents include advances in autonomous decision-making,
improved natural language understanding, multi-agent coordination systems...

A full report has been saved to research_report.md.

======================================================================
✨ Deep Research Flow completed!
======================================================================
```

## Log Sections Explained

### Entry Point
- Shows flow startup
- Displays previous query if resuming
- Prompts for new query
- Confirms receipt

### Step 1: Query Analysis
- Shows the query being analyzed
- Indicates LLM call to router
- Shows routing decision (SIMPLE or RESEARCH)
- Explains which path will be taken

### SIMPLE Path - Step 2
- Shows direct answer generation
- Indicates LLM call
- Confirms answer ready

### RESEARCH Path - Step 2
- Reviews query clarity
- May ask for clarifications
- Updates query with additional context

### RESEARCH Path - Step 3
- Shows full research query
- Lists 4 agents being deployed
- Sets time expectation (2-5 minutes)
- CrewAI shows detailed agent activity
- Confirms completion with report size

### RESEARCH Path - Step 4
- Saves report to file
- Shows absolute file path
- Generates summary
- Confirms summary ready

### Final Step
- Displays original query
- Shows final answer (direct or summary)
- Confirms flow completion

## What Each Icon Means

- 🔍 = Searching/Analyzing
- 🤔 = Thinking/Processing
- 💬 = Simple response
- 📚 = Research required
- ✅ = Success/Complete
- 🔄 = In progress/Working
- ❓ = Question/Input needed
- 🚀 = Starting major operation
- 👥 = Multi-agent crew
- 💾 = Saving data
- 📝 = Writing/Summarizing
- 📊 = Statistics/Metrics
- 📁 = File location
- 📌 = Important info
- ⏳ = Wait time
- ✨ = Completion

## Understanding the Flow Progress

1. **Query received** → You'll see exactly what was captured
2. **Analysis** → Router decides SIMPLE or RESEARCH
3. **Path taken** → Clear indication of which branch executed
4. **Progress updates** → Know what's happening at each step
5. **Results** → See output and file locations
6. **Completion** → Clear end marker

## Troubleshooting with Logs

### If stuck at "Analyzing query complexity..."
- The LLM is being called
- Should complete in 1-3 seconds
- If longer, check API connectivity

### If stuck at "Executing deep research crew..."
- This is normal - takes 2-5 minutes
- Watch for CrewAI agent logs
- Each agent task will show progress

### If "Report saved successfully" doesn't appear
- Check file permissions
- Verify disk space
- Look for error message

### If flow seems frozen
- Look for the "🔄" indicator
- Check last completed "✅" item
- CrewAI shows detailed progress for research

## Tips

1. **Simple queries complete in < 10 seconds**
2. **Research queries take 2-5 minutes**
3. **Watch for the STEP indicators** to track progress
4. **File locations are absolute paths** - easy to find
5. **Report length shown** - verify output size
6. **Previous queries remembered** - context preserved

