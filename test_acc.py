from utils import enumerate_resume, write_jsonl, make_printv
from executors import executor_factory
from generators import generator_factory

from typing import List


def run_test_acc(
    dataset: List[dict],
    model: str,
    language: str,
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
        tests_i = []
        while cur_pass < pass_at_k:
            tests_i = gen.internal_tests(item["prompt"], model, 1)
            print_v(tests_i)

            cur_func_impl = item["prompt"] + item["canonical_solution"]
            print_v(cur_func_impl, flush=True)

            is_passing, _, _ = exe.execute(cur_func_impl, tests_i)
            if is_passing:
                is_solved = True
                num_success += 1
                break
            cur_pass += 1
        item["solution"] = tests_i

        item["is_solved"] = is_solved
        write_jsonl(log_path, [item], append=True)

        print_v(
            f'completed {i+1}/{num_items}: acc = {round(num_success/(i+1), 2)}')
