from executor import execute
from utils import gpt_completion, gpt_chat, write_jsonl, parse_body, build_asserts_from_human_eval

from typing import List

SIMPLE_COMPLETION_INSTRUCTION = "# Write the body of this function only."
SIMPLE_CHAT_INSTRUCTION = "You are CodexGPT. You will be given a function signature and docstring. You should fill in the following text of the missing function body. For example, the first line of the completion should have 4 spaces for the indendation so that it fits syntactically with the preceding signature."

def run_simple(
        dataset: List[dict],
        model: str,
        pass_at_k: int,
        log_path: str,
        verbose: bool
    ) -> None:
    num_items = len(dataset)
    num_success = 0
    for i, item in enumerate(dataset):
        cur_pass = 0
        is_solved = False
        unit_tests_static = build_asserts_from_human_eval(item["test"], item["entry_point"])
        while cur_pass < pass_at_k:
            if model == "gpt-4" or model == "gpt-3.5-turbo":
                soln = parse_body(gpt_chat(model, SIMPLE_CHAT_INSTRUCTION, item["prompt"]))
            else:
                soln = parse_body(gpt_completion(model, f'{SIMPLE_COMPLETION_INSTRUCTION}\n{item["prompt"]}'))
            func = item["prompt"] + soln
            _, failed_tests = execute(func, unit_tests_static)
            if len(failed_tests) == 0:
                item["solution"] = soln
                is_solved = True
                num_success += 1
                break
            cur_pass += 1
        
        if is_solved:
            item["is_solved"] = True
        else:
            item["is_solved"] = False
            item["solution"] = ""
        write_jsonl(log_path, [item], append=True)

        if verbose:
            print(f'completed {i+1}/{num_items}: acc = {round(num_success/(i+1), 2)}')
