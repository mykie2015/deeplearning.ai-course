from types import ModuleType, FunctionType
from typing import Dict, List, Optional
from dlai_grader.grading import test_case, object_to_grade
from dlai_grader.types import grading_function, grading_wrapper, learner_submission

# ===== Neutral fixtures =====
_PROMPT = "Radio observations of recurrent novae"
_DUMMY_REPORT = (
    "This is a dummy research report about recurrent novae. "
    "It should include claims that would normally require citations."
)

# ========= Part 1 =========
# Function under test: generate_research_report_with_tools(prompt_: str, model: str = "gpt-4o") -> str
def part_1(
    learner_mod: learner_submission, solution_mod: Optional[ModuleType]
) -> grading_function:
    @object_to_grade(learner_mod, "generate_research_report_with_tools")
    def g(generate_research_report_with_tools: FunctionType) -> List[test_case]:
        cases: List[test_case] = []

        # Type check
        t = test_case()
        if not isinstance(generate_research_report_with_tools, FunctionType):
            t.failed = True
            t.msg = "generate_research_report_with_tools has incorrect type"
            t.want = FunctionType
            t.got = type(generate_research_report_with_tools)
            return [t]

        # Call and error handling
        try:
            out = generate_research_report_with_tools(_PROMPT)
        except Exception as e:
            t = test_case()
            t.failed = True
            t.msg = f"generate_research_report_with_tools raised {type(e).__name__}: {e}"
            t.want = "no exception"
            t.got = str(e)
            return [t]

        # Must return str
        t = test_case()
        if not isinstance(out, str):
            t.failed = True
            t.msg = "generate_research_report_with_tools must return a str"
            t.want = str
            t.got = type(out)
            return [t]
        else:
            t.failed = False
            t.msg = "returns str"
            t.want = str
            t.got = type(out)
            cases.append(t)

        # Non-trivial content (length > 50)
        t = test_case()
        if len(out.strip()) <= 50:
            t.failed = True
            t.msg = f"report text should be non-trivial (length > 50). Got {len(out.strip())}"
            t.want = "> 50 chars"
            t.got = len(out.strip())
        else:
            t.failed = False
            t.msg = "length > 50"
            t.want = "> 50 chars"
            t.got = len(out.strip())
        cases.append(t)

        return cases
    return g


# ========= Part 2 =========
# Function under test: reflection_and_rewrite(text_or_messages, ...) -> dict with keys "reflection", "revised_report"
def part_2(
    learner_mod: learner_submission, solution_mod: Optional[ModuleType]
) -> grading_function:
    @object_to_grade(learner_mod, "reflection_and_rewrite")
    def g(reflection_and_rewrite: FunctionType) -> List[test_case]:
        cases: List[test_case] = []

        # Type check
        t = test_case()
        if not isinstance(reflection_and_rewrite, FunctionType):
            t.failed = True
            t.msg = "reflection_and_rewrite has incorrect type"
            t.want = FunctionType
            t.got = type(reflection_and_rewrite)
            return [t]

        # Call and error handling
        try:
            out = reflection_and_rewrite(_DUMMY_REPORT)
        except Exception as e:
            t = test_case()
            t.failed = True
            t.msg = f"reflection_and_rewrite raised {type(e).__name__}: {e}"
            t.want = "no exception"
            t.got = str(e)
            return [t]

        # Must return dict with specific keys
        t = test_case()
        if not isinstance(out, dict):
            t.failed = True
            t.msg = "reflection_and_rewrite must return a dict"
            t.want = dict
            t.got = type(out)
            return [t]
        if not {"reflection", "revised_report"} <= set(out.keys()):
            t.failed = True
            t.msg = "dict must include keys 'reflection' and 'revised_report'"
            t.want = {"reflection", "revised_report"}
            t.got = set(out.keys())
            return [t]
        t.failed = False
        t.msg = "dict with required keys"
        t.want = {"reflection", "revised_report"}
        t.got = set(out.keys())
        cases.append(t)

        # Both values must be strings
        t = test_case()
        if not isinstance(out["reflection"], str) or not isinstance(out["revised_report"], str):
            t.failed = True
            t.msg = "'reflection' and 'revised_report' must be strings"
            t.want = "str, str"
            t.got = (type(out["reflection"]), type(out["revised_report"]))
            return [t]
        t.failed = False
        t.msg = "values are strings"
        t.want = "str"
        t.got = "str"
        cases.append(t)

        # Minimal content checks
        ref = out["reflection"].lower()
        t = test_case()
        # Encourage the expected headings but don't require exact formatting
        expected_markers = ["strengths", "limitations", "suggestions", "opportunities"]
        has_all = all(marker in ref for marker in expected_markers)
        if not has_all:
            t.failed = True
            t.msg = "reflection should mention Strengths, Limitations, Suggestions, Opportunities"
            t.want = expected_markers
            t.got = [m for m in expected_markers if m in ref]
        else:
            t.failed = False
            t.msg = "reflection includes key sections"
            t.want = expected_markers
            t.got = expected_markers
        cases.append(t)

        # Revised report should be non-trivial
        t = test_case()
        if len(out["revised_report"].strip()) <= 50:
            t.failed = True
            t.msg = "revised_report should be non-trivial (length > 50)"
            t.want = "> 50 chars"
            t.got = len(out["revised_report"].strip())
        else:
            t.failed = False
            t.msg = "revised_report length > 50"
            t.want = "> 50 chars"
            t.got = len(out["revised_report"].strip())
        cases.append(t)

        return cases
    return g


# ========= Part 3 =========
# Function under test: convert_report_to_html(text_or_messages, ...) -> str (HTML)
def part_3(
    learner_mod: learner_submission, solution_mod: Optional[ModuleType]
) -> grading_function:
    @object_to_grade(learner_mod, "convert_report_to_html")
    def g(convert_report_to_html: FunctionType) -> List[test_case]:
        cases: List[test_case] = []

        # Type check
        t = test_case()
        if not isinstance(convert_report_to_html, FunctionType):
            t.failed = True
            t.msg = "convert_report_to_html has incorrect type"
            t.want = FunctionType
            t.got = type(convert_report_to_html)
            return [t]

        # Call and basic checks
        try:
            out = convert_report_to_html(_DUMMY_REPORT)
        except Exception as e:
            t = test_case()
            t.failed = True
            t.msg = f"convert_report_to_html raised {type(e).__name__}: {e}"
            t.want = "no exception"
            t.got = str(e)
            return [t]

        # Must be str and look like HTML
        t = test_case()
        if not isinstance(out, str):
            t.failed = True
            t.msg = "convert_report_to_html must return a str"
            t.want = str
            t.got = type(out)
            return [t]

        lower = out.lower()
        looks_like_html = ("<html" in lower) or ("</" in lower) or ("<h1" in lower) or ("<p" in lower)
        if not looks_like_html:
            t.failed = True
            t.msg = "Output should look like HTML (e.g., contain <html>, <h1>, <p>, or closing tags)"
            t.want = "HTML-like string"
            t.got = out[:80]
            return [t]
        else:
            t.failed = False
            t.msg = "returns HTML-like string"
            t.want = "HTML-like"
            t.got = out[:80]
            cases.append(t)

        return cases
    return g


# ========= Orchestrator =========
def handle_part_id(part_id: str) -> grading_wrapper:
    grader_dict: Dict[str, grading_wrapper] = {
        "1": part_1,  # generate_research_report_with_tools
        "2": part_2,  # reflection_and_rewrite
        "3": part_3,  # convert_report_to_html
    }
    return grader_dict[part_id]
