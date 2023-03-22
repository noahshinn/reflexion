from executor import execute

from typing import List

def contains_valid_func(funcs: List[str], tests: List[str]) -> bool:
    for func in funcs:
        success_tests, _ = execute(func, tests, with_output=False)
        if len(success_tests) > 0:
            return True
    return False

def evaluate(solutions: List[dict], pass_at_k: int) -> None:
    """
    Evaluate the solutions.

    `solutions` should have the shape:
    [
        {
            "task_id": str (The task id of the function.)
            "prompt": str (The signature and docstring of the function.)
            "entry_point": str (The function name.)
            "test": str (The test code.)
            "solutions": List[str] (The function bodies.)
        }
    ]

    """
    success_task_ids: List[str] = []
    failed_task_ids: List[str] = []
    for solution in solutions:
        tests: List[str] = [test.strip().replace("candidate", solution["entry_point"]) for test in solution["test"].split("\n") if "assert" in test]
        funcs: List[str] = [solution["prompt"] + func_body for func_body in solution["solutions"]]
        if contains_valid_func(funcs, tests):
            success_task_ids += [solution["task_id"]]
        else:
            failed_task_ids += [solution["task_id"]]
    
    print(f"pass@{pass_at_k}: {round(len(success_task_ids) / len(solutions))}")

    # TODO: logging
