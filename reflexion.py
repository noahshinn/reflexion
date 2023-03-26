from utils import write_jsonl, parse_body
from executors import py_evaluate, py_execute
from generators import py_generate_func_impl, py_generate_self_reflection, py_generate_internal_tests

from typing import List


def run_reflexion(
        dataset: List[dict],
        model: str,
        language: str,
        max_iters: int,
        pass_at_k: int,
        log_path: str,
        verbose: bool
    ) -> None:
    # should handle more languages later
    # someone do this but arrange it better
    evaluate = None
    execute = None
    self_reflection_generator = None
    func_impl_generator = None
    internal_test_generator = None
    if language == "python" or language == "py":
        evaluate = py_evaluate
        execute = py_execute
        self_reflection_generator = py_generate_self_reflection
        func_impl_generator = py_generate_func_impl
        internal_test_generator = py_generate_internal_tests
    else:
        raise NotImplementedError(f"language {language} not supported")

    assert not evaluate is None
    assert not execute is None
    assert not self_reflection_generator is None
    assert not func_impl_generator is None
    assert not internal_test_generator is None

    num_items = len(dataset)
    num_success = 0
    for i, item in enumerate(dataset):
        cur_pass = 0
        is_solved = False
        reflections = []
        cur_func_impl = ""
        while cur_pass < pass_at_k and not is_solved:
            tests_i = internal_test_generator(item["prompt"], model, 1)

            # first attempt
            cur_func_impl = parse_body(func_impl_generator(item["prompt"], model, "simple"))
            is_passing, feedback = execute(cur_func_impl, tests_i)

            # if solved, exit early
            if is_passing:
                is_solved = True
                num_success += 1
                break

            # use self-reflection to iteratively improve
            cur_iter = 1
            cur_feedback = feedback
            while cur_iter < max_iters:
                # get self-reflection
                reflection = self_reflection_generator(cur_func_impl, cur_feedback, model)
                reflections += [reflection]

                # apply self-reflection in the next attempt
                cur_func_impl = parse_body(func_impl_generator(
                    func_sig=item["prompt"],
                    model=model,
                    strategy="reflexion",
                    prev_func_impl=cur_func_impl,
                    feedback=cur_feedback,
                    self_reflection=reflection
                ))

                # check if all internal unit tests pass
                is_passing, cur_feedback = execute(cur_func_impl, tests_i)

                # if solved, check if it passes the real tests, exit early
                if is_passing or cur_iter == max_iters - 1:
                    is_passing = evaluate(item["entry_point"], cur_func_impl, item["test"], timeout=10)
                    if is_passing:
                        item["solution"] = cur_func_impl
                        is_solved = True
                        num_success += 1
                    break

                cur_iter += 1
            cur_pass += 1

        item["is_solved"] = is_solved
        item["reflections"] = reflections
        item["solution"] = cur_func_impl
        write_jsonl(log_path, [item], append=True)

        if verbose:
            print(f'completed {i+1}/{num_items}: acc = {round(num_success/(i+1), 2)}')
