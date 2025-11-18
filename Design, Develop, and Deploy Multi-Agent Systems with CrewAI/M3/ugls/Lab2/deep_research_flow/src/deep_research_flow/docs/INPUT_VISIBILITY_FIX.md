# Input Visibility Fix Guide

If you can't see your input when typing, try these solutions:

## Solution 1: Use the Enhanced Runner (RECOMMENDED)

```bash
cd deep_research_flow
source venv/bin/activate
python run_visible_input.py
```

This uses `sys.stdin.readline()` with `sys.stdout.flush()` which should show your input.

## Solution 2: Use the Shell Script with Echo Enabled

```bash
cd deep_research_flow
./run_with_echo.sh
```

This explicitly enables terminal echo before running.

## Solution 3: Try a Different Terminal

The issue might be with your current terminal's configuration:

### Option A: Use macOS Terminal (instead of iTerm2 or vice versa)
```bash
# Open Terminal.app, then:
cd "/Users/mykielee/GitHub/deeplearning.ai-course/Design, Develop, and Deploy Multi-Agent Systems with CrewAI/M3/ugls/Lab2/deep_research_flow"
source venv/bin/activate
crewai run
```

### Option B: Use VS Code's integrated terminal
```bash
# In VS Code, open terminal (Cmd+`), then:
cd deep_research_flow
source venv/bin/activate
crewai run
```

## Solution 4: Check Terminal Settings

Before running, ensure echo is enabled:

```bash
stty echo
stty -a  # Check all terminal settings
```

## Solution 5: Run with Script Command

This creates a typescript that forces proper terminal handling:

```bash
cd deep_research_flow
source venv/bin/activate
script -q /dev/null crewai run
```

## What Was Changed in the Code

The code now uses:
```python
sys.stdout.write(">> ")
sys.stdout.flush()
user_input = sys.stdin.readline().strip()
```

Instead of:
```python
user_input = input(">> ")
```

This gives more control over input/output buffering.

## Debugging: Check If Input Is Actually Working

Even if you can't see it, your input IS being captured (as shown in your terminal output). The query "why playing tennis is hard..." was received correctly.

To verify:
1. Type blindly at the `>>` prompt
2. Press Enter
3. Look for the line that says: `✅ Query received: "your text here"`

Your input **is working**, it's just not being displayed.

## Platform-Specific Issues

### macOS Issue
Some macOS terminals have issues with Python's `input()` when running through certain frameworks. The `sys.stdin.readline()` method should fix this.

### Virtual Environment Issue
If running from `.venv` (as shown in your output), the virtual environment might be interfering. Try:

```bash
cd deep_research_flow
deactivate  # If in another venv
source venv/bin/activate  # Use the local venv
python run_visible_input.py
```

## Last Resort: Run with Input File

If nothing works, you can pre-specify the query:

```python
# Edit main.py temporarily and add at the top of start_conversation():
def start_conversation(self):
    # TEMPORARY: Skip interactive input
    if not self.state.user_query:
        self.state.user_query = "What are the latest developments in AI agents?"
        print(f"Using pre-set query: {self.state.user_query}")
        return
    # ... rest of the function
```

## Testing Different Methods

Try each method and see which one shows your input:

1. **Method 1**: `./run_visible_input.py` 
2. **Method 2**: `./run_with_echo.sh`
3. **Method 3**: Different terminal app
4. **Method 4**: `script -q /dev/null crewai run`

One of these should work for your terminal setup!

## Contact

If none of these work, the issue is likely:
- Your terminal emulator's configuration
- macOS security/privacy settings blocking TTY
- Terminal color/formatting conflicts

Try running in the basic macOS Terminal.app with default settings.

