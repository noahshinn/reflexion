from utils import enumerate_resume, make_printv, write_jsonl
from executors import executor_factory
from generators import generator_factory

from typing import List


def run_immediate_reflexion(
    dataset: List[dict],
    model: str,
    language: str,
    max_iters: int,
    pass_at_k: int,
    log_path: str,
    verbose: bool
) -> None:
    exe = executor_factory(language)
    gen = generator_factory(language)

    print_v = make_printv(verbose)

    num_items = len(dataset)
    num_success = 0
    for i, item in enumerate_resume(dataset, log_path):
        cur_pass = 0
        is_solved = False
        reflections = []
        cur_func_impl = ""
        while cur_pass < pass_at_k and not is_solved:
            # first attempt
            cur_func_impl = gen.func_impl(item["prompt"], model, "simple")
            assert isinstance(cur_func_impl, str)

            # use self-reflection to iteratively improve
            cur_iter = 1
            feedback = "Test cases omitted"
            while cur_iter < max_iters:
                # get self-reflection
                reflection = gen.self_reflection(
                    cur_func_impl, feedback, model)
                reflections += [reflection]

                # apply self-reflection in the next attempt
                cur_func_impl = gen.func_impl(
                    func_sig=item["prompt"],
                    model=model,
                    strategy="reflexion",
                    prev_func_impl=cur_func_impl,
                    feedback=feedback,
                    self_reflection=reflection
                )
                assert isinstance(cur_func_impl, str)

                cur_iter += 1
            cur_pass += 1

        is_solved = exe.evaluate(
            item["entry_point"], cur_func_impl, item["test"], timeout=10)
        if is_solved:
            num_success += 1

        item["is_solved"] = is_solved
        item["reflections"] = reflections
        item["solution"] = cur_func_impl
        write_jsonl(log_path, [item], append=True)

        print_v(
            f'completed {i+1}/{num_items}: acc = {round(num_success/(i+1), 2)}')
