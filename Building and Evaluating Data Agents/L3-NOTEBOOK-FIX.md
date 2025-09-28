# L3 Notebook Quick Fix

## Issue
The L3 notebook defines its own `CortexAgentTool` class that doesn't work with the local PostgreSQL setup.

## Solution
Replace the notebook's `CortexAgentTool` definition with an import from helper.

### Step 1: Modify Cell 7 (Import Cell)
Change this cell from:
```python
from snowflake.snowpark import Session
from snowflake.core import Root
from pydantic import BaseModel, PrivateAttr
from snowflake.core.cortex.lite_agent_service import AgentRunRequest
from typing import Any, Type
from langchain.schema import HumanMessage
from langgraph.graph import END
from langgraph.types import Command
from typing import Literal, Dict
import json
```

To:
```python
from snowflake.snowpark import Session
from snowflake.core import Root
from pydantic import BaseModel, PrivateAttr
from snowflake.core.cortex.lite_agent_service import AgentRunRequest
from typing import Any, Type
from langchain.schema import HumanMessage
from langgraph.graph import END
from langgraph.types import Command
from typing import Literal, Dict
import json

# Import the compatible CortexAgentTool from helper
from helper import CortexAgentTool
```

### Step 2: Remove Cell 8 (CortexAgentTool Definition)
**Delete or comment out the entire Cell 8** that contains:
```python
class CortexAgentTool:
    name: str = "CortexAgent"
    description: str = "answers questions using sales conversations and metrics"
    args_schema: Type[CortexAgentArgs] = CortexAgentArgs

    _session: Session = PrivateAttr()
    _root: Root = PrivateAttr()
    _agent_service: Any = PrivateAttr()

    def __init__(self, session: Session):
        # ... rest of the class definition
```

### Step 3: Keep Cell 9 (Tool Creation)
Cell 9 should work as-is:
```python
cortex_agent_tool = CortexAgentTool(session=snowpark_session)
```

## Alternative Quick Fix (No Cell Modification)
If you don't want to modify the notebook cells, you can run this in a new cell before Cell 8:

```python
# Override the CortexAgentTool with the compatible version
from helper import CortexAgentTool
```

This will import the compatible version that works with both local and Snowflake sessions.

## Verification
After making the changes, Cell 9 should execute successfully and create a working `cortex_agent_tool` that can handle both structured (PostgreSQL) and unstructured (Chroma/fallback) data queries.
