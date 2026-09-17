from types import ModuleType, FunctionType
from typing import Dict, List, Optional
from dlai_grader.grading import test_case, object_to_grade
from dlai_grader.types import grading_function, grading_wrapper, learner_submission

# Neutral inputs
_DRAFT_IN = "x"  # for generate_draft
_DRAFT_TXT = "A" * 120  # a draft with length > 100
_FEEDBACK = "B" * 60  # arbitrary feedback


def part_1(
    learner_mod: learner_submission, solution_mod: Optional[ModuleType] = None
) -> grading_function:
    @object_to_grade(learner_mod, "generate_draft")
    def g(generate_draft: FunctionType) -> List[test_case]:
        t = test_case()
        if not isinstance(generate_draft, FunctionType):
            t.failed = True
            t.msg = "generate_draft has incorrect type"
            t.want = FunctionType
            t.got = type(generate_draft)
            return [t]

        cases: List[test_case] = []

        # Call and basic error/type check (early return on failure)
        t = test_case()
        try:
            out = generate_draft(_DRAFT_IN)
        except Exception as e:
            t.failed = True
            t.msg = f"generate_draft raised {type(e).__name__}: {e}"
            t.want = "no exception"
            t.got = str(e)
            return [t]

        t = test_case()
        if not isinstance(out, str):
            t.failed = True
            t.msg = "generate_draft must return a str"
            t.want = str
            t.got = type(out)
            return [t]

        # Length > 100
        t = test_case()
        if len(out) <= 100:
            t.failed = True
            t.msg = (
                f"generate_draft must return text with length > 100 (got {len(out)})"
            )
            t.want = "> 100 chars"
            t.got = len(out)
        cases.append(t)

        return cases

    return g


def part_2(
    learner_mod: learner_submission, solution_mod: Optional[ModuleType] = None
) -> grading_function:
    @object_to_grade(learner_mod, "reflect_on_draft")
    def g(reflect_on_draft: FunctionType) -> List[test_case]:
        t = test_case()
        if not isinstance(reflect_on_draft, FunctionType):
            t.failed = True
            t.msg = "reflect_on_draft has incorrect type"
            t.want = FunctionType
            t.got = type(reflect_on_draft)
            return [t]

        cases: List[test_case] = []

        # Only check: returns str (early return on failure)
        t = test_case()
        try:
            out = reflect_on_draft(_DRAFT_TXT)
        except Exception as e:
            t.failed = True
            t.msg = f"reflect_on_draft raised {type(e).__name__}: {e}"
            t.want = "no exception"
            t.got = str(e)
            return [t]
        else:
            cases.append(t)

        if not isinstance(out, str):
            t.failed = True
            t.msg = "reflect_on_draft must return a str"
            t.want = str
            t.got = type(out)
            return [t]
        else:
            cases.append(t)

        return cases

    return g


def part_3(
    learner_mod: learner_submission, solution_mod: Optional[ModuleType] = None
) -> grading_function:
    @object_to_grade(learner_mod, "revise_draft")
    def g(revise_draft: FunctionType) -> List[test_case]:
        t = test_case()
        if not isinstance(revise_draft, FunctionType):
            t.failed = True
            t.msg = "revise_draft has incorrect type"
            t.want = FunctionType
            t.got = type(revise_draft)
            return [t]

        cases: List[test_case] = []

        # Call and basic error/type check (early return on failure)
        try:
            out = revise_draft(_DRAFT_TXT, _FEEDBACK)
        except Exception as e:
            t = test_case()
            t.failed = True
            t.msg = f"revise_draft raised {type(e).__name__}: {e}"
            t.want = "no exception"
            t.got = str(e)
            return [t]

        t = test_case()
        if not isinstance(out, str):
            t.failed = True
            t.msg = "revise_draft must return a str"
            t.want = str
            t.got = type(out)
            return [t]

        # Length > 100
        t = test_case()
        if len(out) <= 100:
            t.failed = True
            t.msg = f"revise_draft must return text with length > 100 (got {len(out)})"
            t.want = "> 100 chars"
            t.got = len(out)
        cases.append(t)

        return cases

    return g


def handle_part_id(part_id: str) -> grading_wrapper:
    grader_dict: Dict[str, grading_wrapper] = {
        "1": part_1,
        "2": part_2,
        "3": part_3,
    }
    return grader_dict[part_id]
