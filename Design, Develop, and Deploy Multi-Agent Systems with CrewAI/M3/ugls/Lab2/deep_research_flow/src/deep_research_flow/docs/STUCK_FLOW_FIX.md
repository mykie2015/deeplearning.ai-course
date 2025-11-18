# Stuck Flow Fix - Timeout & Auto-Mode

## Problem
The flow was stuck at line 142 waiting for clarification input, consuming tokens but not progressing because:
1. Input wasn't visible (so you didn't know it was waiting)
2. No timeout mechanism
3. No way to skip clarifications

## Solutions Implemented

### ✅ Solution 1: Timeout Added (60 seconds)

The clarification step now has a **60-second timeout**:
- If you don't respond within 60s, it automatically skips and proceeds
- Prevents infinite waiting
- Saves tokens and time

```python
# Auto-skips after 60 seconds of no input
timeout = 60  # seconds
```

### ✅ Solution 2: Skip Options

You now have 3 ways to handle clarifications:
1. **Provide details** - Type your clarification
2. **Press Enter** - Empty input = skip
3. **Type 'skip'** - Explicitly skip

The flow will show:
```
💡 Options:
   1. Provide more details
   2. Press Enter to skip and proceed anyway
   3. Type 'skip' to proceed with current query
```

### ✅ Solution 3: Auto-Mode Runner

For completely unattended runs, use the new auto-mode script:

```bash
cd deep_research_flow
source venv/bin/activate

# Interactive (will ask for query once)
python run_auto_mode.py

# Or provide query directly
python run_auto_mode.py "What are the latest developments in AI agents?"
```

**Auto-mode features:**
- ✅ Automatically skips all clarifications
- ✅ No waiting for input
- ✅ Perfect for batch processing
- ✅ Good when input visibility is broken
- ✅ Saves time and tokens

## How to Kill a Stuck Flow

If your flow is currently stuck:

### Method 1: Press Ctrl+C
```bash
# In the terminal where flow is running
Ctrl + C
```

### Method 2: Just press Enter
Since we added the skip option, pressing Enter will now make it proceed!

### Method 3: Type "skip" and press Enter
Even though you can't see it, type: `skip` then Enter

## Usage Patterns

### Pattern 1: Regular Interactive Mode (with timeout)
```bash
cd deep_research_flow
source venv/bin/activate
crewai run
```
- Now has 60s timeout on clarifications
- Won't get stuck forever
- Press Enter to skip if needed

### Pattern 2: Auto-Mode (No Interaction)
```bash
cd deep_research_flow
source venv/bin/activate
python run_auto_mode.py "your query here"
```
- Zero interaction needed
- Perfect for scripting
- Fastest execution

### Pattern 3: Visible Input Mode
```bash
cd deep_research_flow  
source venv/bin/activate
python run_visible_input.py
```
- Better input visibility
- Has timeout
- Has skip options

## Token Consumption

### What Happened in Your Stuck Run:
- Flow was waiting at clarification (not consuming tokens while waiting)
- If CrewAI had background processes, they might have been retrying
- Tracing API calls also consume a small amount

### To Monitor Token Usage:
The dashboard you showed (`dashboard.exa.ai/usage`) shows:
- You made 17 search queries on Nov 18
- Costs are very low ($0.00006 - $0.00018 per query)
- Most expensive was $0.00089 (5557 prompt, 106 completion)

This is normal - the flow uses EXA search API which has separate costs from OpenAI.

## Best Practice Going Forward

**For Testing:**
```bash
python run_auto_mode.py "simple test query"
```

**For Real Research:**
```bash
python run_auto_mode.py "What are the latest developments in quantum computing as of 2024?"
```

**For Interactive (if input works):**
```bash
python run_visible_input.py
```

## Summary of All Fixes

| Issue | Fix | File |
|-------|-----|------|
| Invisible input | `sys.stdin.readline()` | `main.py` |
| Stuck waiting | 60s timeout | `main.py` |
| No skip option | Added skip/Enter options | `main.py` |
| Unattended runs | Auto-mode runner | `run_auto_mode.py` |
| Better visibility | Visible input runner | `run_visible_input.py` |
| Terminal issues | Echo-enabled script | `run_with_echo.sh` |

## Quick Commands

Kill current stuck flow:
```bash
# Just press: Ctrl + C
# Or type: skip [Enter]
# Or just press: [Enter]
```

Run new query without getting stuck:
```bash
cd "/Users/mykielee/GitHub/deeplearning.ai-course/Design, Develop, and Deploy Multi-Agent Systems with CrewAI/M3/ugls/Lab2/deep_research_flow"
source venv/bin/activate
python run_auto_mode.py "your query"
```

That's it! No more infinite waiting! 🎉

