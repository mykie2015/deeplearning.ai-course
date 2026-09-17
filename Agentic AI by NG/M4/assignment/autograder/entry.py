from dlai_grader.config import Config
from dlai_grader.compiler import compile_module
from dlai_grader.io import read_notebook, copy_submission_to_workdir, send_feedback

from dlai_grader.notebook import (
    notebook_to_script,
    keep_tagged_cells,
    notebook_is_up_to_date,
    notebook_version,
    cut_notebook,
    partial_grading_enabled,
)
from dlai_grader.grading import compute_grading_score, graded_obj_missing
from grader import handle_part_id


def main() -> None:
    c = Config()

    copy_submission_to_workdir()

    try:
        nb = read_notebook(c.submission_file_path)
    except Exception as e:
        send_feedback(
            0.0,
            f"There was a problem reading your notebook. Details:\n{str(e)}",
            err=True,
        )

    if not notebook_is_up_to_date(nb):
        msg = f"You are submitting a version of the assignment that is behind the latest version.\nThe latest version is {c.latest_version} and you are on version {notebook_version(nb)}."

        send_feedback(0.0, msg)

    transformations = [cut_notebook(), keep_tagged_cells()]

    for t in transformations:
        nb = t(nb)

    script = notebook_to_script(nb)

    try:
        learner_mod = compile_module(script, "learner_mod", verbose=False)
    except Exception as e:
        send_feedback(
            0.0,
            f"There was a problem compiling the code from your notebook, please check that you saved before submitting. Details:\n{str(e)}",
        )

    solution_nb = read_notebook(c.solution_file_path)

    for t in transformations:
        solution_nb = t(solution_nb)

    solution_script = notebook_to_script(solution_nb)
    solution_mod = compile_module(solution_script, "solution_mod", verbose=False)

    g_func = handle_part_id(c.part_id)(learner_mod, solution_mod)

    try:
        cases = g_func()
    except Exception as e:
        send_feedback(
            0.0,
            f"There was an error grading your submission. Details:\n{str(e)}",
            err=True,
        )

    if graded_obj_missing(cases):
        additional_msg = ""
        if partial_grading_enabled(nb):
            additional_msg = "The # grade-up-to-here comment in the notebook might be causing the problem."

        send_feedback(
            0.0,
            f"Unable to find object required for grading in your code.\n{additional_msg}",
            err=True,
        )

    score, feedback = compute_grading_score(cases)

    send_feedback(score, feedback)


if __name__ == "__main__":
    main()
