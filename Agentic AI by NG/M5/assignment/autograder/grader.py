# grader_agents.py
from types import ModuleType, FunctionType
from typing import Dict, List, Optional, Tuple, Any
from dlai_grader.grading import test_case, object_to_grade
from dlai_grader.types import grading_function, grading_wrapper, learner_submission

# ===== Neutral fixtures =====
_TOPIC = "The ensemble Kalman filter for time series forecasting"
_TASK_WRITE = "Draft a concise summary (150-250 words) explaining the core idea and typical applications."
_TASK_EDIT  = "Reflect on the draft and suggest improvements in structure, clarity, and citations."
_TASK_RESEARCH = "Find 3 key references and summarize them briefly."

# ========= Part 1 =========
# Function under test: planner_agent(topic: str, model: str = "openai:o4-mini") -> list[str]
def part_1(
    learner_mod: learner_submission, solution_mod: Optional[ModuleType]
) -> grading_function:
    @object_to_grade(learner_mod, "planner_agent")
    def g(planner_agent: FunctionType) -> List[test_case]:
        cases: List[test_case] = []

        # 1) type check
        t = test_case()
        if not isinstance(planner_agent, FunctionType):
            t.failed = True
            t.msg = "planner_agent has incorrect type"
            t.want = FunctionType
            t.got = type(planner_agent)
            return [t]

        # 2) call & error handling
        try:
            out = planner_agent(_topic := _TOPIC)
        except Exception as e:
            t = test_case()
            t.failed = True
            t.msg = f"planner_agent raised {type(e).__name__}: {e}"
            t.want = "no exception"
            t.got = str(e)
            return [t]

        # 3) must return list[str]
        t = test_case()
        if not isinstance(out, list):
            t.failed = True
            t.msg = "planner_agent must return a list"
            t.want = list
            t.got = type(out)
            return [t]
        cases.append(t)

        t = test_case()
        if not all(isinstance(s, str) for s in out):
            t.failed = True
            t.msg = "plan elements must be strings"
            t.want = "list[str]"
            t.got = [type(s) for s in out]
            return [t]
        cases.append(t)

        # 4) at least 3 steps
        t = test_case()
        if len(out) < 3:
            t.failed = True
            t.msg = "plan should include at least 3 steps"
            t.want = "len(plan) >= 3"
            t.got = len(out)
        cases.append(t)

        # 5) final step mentions Markdown
        t = test_case()
        last = (out[-1] if out else "").lower()
        if not any(k in last for k in ("markdown", "md")):
            t.failed = True
            t.msg = "final step should mention generating a Markdown document"
            t.want = "mention of 'Markdown' or 'md'"
            t.got = last
        cases.append(t)

        return cases
    return g


# ========= Part 2 =========
# Function under test: research_agent(task: str, model: str = ..., return_messages: bool = False) -> str | (str, messages)
def part_2(
    learner_mod: learner_submission, solution_mod: Optional[ModuleType]
) -> grading_function:
    @object_to_grade(learner_mod, "research_agent")
    def g(research_agent: FunctionType) -> List[test_case]:
        cases: List[test_case] = []

        # 1) type check
        t = test_case()
        if not isinstance(research_agent, FunctionType):
            t.failed = True
            t.msg = "research_agent has incorrect type"
            t.want = FunctionType
            t.got = type(research_agent)
            return [t]

        # 2) default call -> str
        try:
            out_text = research_agent(_TASK_RESEARCH)
        except Exception as e:
            t = test_case()
            t.failed = True
            t.msg = f"research_agent raised {type(e).__name__} (default): {e}"
            t.want = "no exception"
            t.got = str(e)
            return [t]

        t = test_case()
        if not isinstance(out_text, str):
            t.failed = True
            t.msg = "research_agent must return a str by default (return_messages=False)"
            t.want = str
            t.got = type(out_text)
            return [t]
        cases.append(t)

        t = test_case()
        if len(out_text.strip()) <= 50:
            t.failed = True
            t.msg = "output should be non-trivial (length > 50)"
            t.want = "> 50 chars"
            t.got = len(out_text.strip())
        cases.append(t)

        # 3) return_messages=True -> (str, list)
        try:
            out_tuple = research_agent("Summarize two seminal papers in one paragraph.", return_messages=True)
        except Exception as e:
            t = test_case()
            t.failed = True
            t.msg = f"research_agent raised {type(e).__name__} (return_messages=True): {e}"
            t.want = "no exception"
            t.got = str(e)
            return [t]

        t = test_case()
        ok_tuple = (
            isinstance(out_tuple, tuple) and
            len(out_tuple) == 2 and
            isinstance(out_tuple[0], str) and
            isinstance(out_tuple[1], list)
        )
        if not ok_tuple:
            t.failed = True
            t.msg = "with return_messages=True, must return (str, messages_list)"
            t.want = "(str, list)"
            t.got = type(out_tuple)
            return [t]
        cases.append(t)

        return cases
    return g


# ========= Part 3 =========
# Function under test: writer_agent(task: str, model: str = "openai:o4-mini") -> str
def part_3(
    learner_mod: learner_submission, solution_mod: Optional[ModuleType]
) -> grading_function:
    @object_to_grade(learner_mod, "writer_agent")
    def g(writer_agent: FunctionType) -> List[test_case]:
        cases: List[test_case] = []

        # 1) type check
        t = test_case()
        if not isinstance(writer_agent, FunctionType):
            t.failed = True
            t.msg = "writer_agent has incorrect type"
            t.want = FunctionType
            t.got = type(writer_agent)
            return [t]

        # 2) call & error handling
        try:
            out = writer_agent(_TASK_WRITE)
        except Exception as e:
            t = test_case()
            t.failed = True
            t.msg = f"writer_agent raised {type(e).__name__}: {e}"
            t.want = "no exception"
            t.got = str(e)
            return [t]

        # 3) must return str
        t = test_case()
        if not isinstance(out, str):
            t.failed = True
            t.msg = "writer_agent must return a str"
            t.want = str
            t.got = type(out)
            return [t]
        cases.append(t)

        # 4) non-trivial length
        t = test_case()
        if len(out.strip()) <= 50:
            t.failed = True
            t.msg = "draft should be non-trivial (length > 50)"
            t.want = "> 50 chars"
            t.got = len(out.strip())
        cases.append(t)

        return cases
    return g


# ========= Part 4 =========
# Function under test: editor_agent(task: str, model: str = "openai:o4-mini") -> str
def part_4(
    learner_mod: learner_submission, solution_mod: Optional[ModuleType]
) -> grading_function:
    @object_to_grade(learner_mod, "editor_agent")
    def g(editor_agent: FunctionType) -> List[test_case]:
        cases: List[test_case] = []

        # 1) type check
        t = test_case()
        if not isinstance(editor_agent, FunctionType):
            t.failed = True
            t.msg = "editor_agent has incorrect type"
            t.want = FunctionType
            t.got = type(editor_agent)
            return [t]

        # 2) call & error handling
        try:
            out = editor_agent(_TASK_EDIT)
        except Exception as e:
            t = test_case()
            t.failed = True
            t.msg = f"editor_agent raised {type(e).__name__}: {e}"
            t.want = "no exception"
            t.got = str(e)
            return [t]

        # 3) must return str
        t = test_case()
        if not isinstance(out, str):
            t.failed = True
            t.msg = "editor_agent must return a str"
            t.want = str
            t.got = type(out)
            return [t]
        cases.append(t)

        # 4) non-trivial length
        t = test_case()
        if len(out.strip()) <= 50:
            t.failed = True
            t.msg = "editor output should be non-trivial (length > 50)"
            t.want = "> 50 chars"
            t.got = len(out.strip())
        cases.append(t)

        return cases
    return g


# ========= Orchestrator =========
def handle_part_id(part_id: str) -> grading_wrapper:
    grader_dict: Dict[str, grading_wrapper] = {
        "1": part_1,  # planner_agent
        "2": part_2,  # research_agent
        "3": part_3,  # writer_agent
        "4": part_4,  # editor_agent
    }
    return grader_dict[part_id]
