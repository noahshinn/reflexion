from utils import write_jsonl
from executors import executor_factory
from generators import generator_factory

from typing import List

SIMPLE_COMPLETION_INSTRUCTION = "# Write the body of this function only."
SIMPLE_CHAT_INSTRUCTION = "You are CodexGPT. You will be given a function signature and docstring. You should fill in the following text of the missing function body. For example, the first line of the completion should have 4 spaces for the indendation so that it fits syntactically with the preceding signature."

def run_simple(
        dataset: List[dict],
        model: str,
        language: str,
        pass_at_k: int,
        log_path: str,
        verbose: bool
    ) -> None:
    exe = executor_factory(language)
    gen = generator_factory(language)
    
    num_items = len(dataset)
    num_success = 0
    for i, item in enumerate(dataset):
        cur_pass = 0
        is_solved = False
        cur_func_impl = ""
        while cur_pass < pass_at_k:
            cur_func_impl = gen.func_impl(item["prompt"], model, "simple")
            assert isinstance(cur_func_impl, str)
            is_passing = exe.evaluate(item["entry_point"], cur_func_impl, item["test"], timeout=10)
            if is_passing:
                is_solved = True
                num_success += 1
                break
            cur_pass += 1
        item["solution"] = cur_func_impl
        
        item["is_solved"] = is_solved
        write_jsonl(log_path, [item], append=True)

        if verbose:
            print(f'completed {i+1}/{num_items}: acc = {round(num_success/(i+1), 2)}')
