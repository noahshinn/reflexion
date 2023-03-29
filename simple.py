from utils import write_jsonl
from executors import py_evaluate, rs_evaluate
from generators import py_generate_func_impl, rs_generate_func_impl

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
    # someone implement more languages
    evaluate = None
    func_impl_generator = None
    if language == "python" or language == "py":
        evaluate = py_evaluate
        func_impl_generator = py_generate_func_impl
    elif language == "rust" or language == "rs":
        evaluate = rs_evaluate
        func_impl_generator = rs_generate_func_impl
    else:
        raise NotImplementedError(f"language {language} not supported")
    
    assert not evaluate is None
    assert not func_impl_generator is None

    num_items = len(dataset)
    num_success = 0
    for i, item in enumerate(dataset):
        cur_pass = 0
        is_solved = False
        cur_func_impl = ""
        while cur_pass < pass_at_k:
            cur_func_impl = func_impl_generator(item["prompt"], model, "simple")
            assert isinstance(cur_func_impl, str)
            is_passing = evaluate(item["entry_point"], cur_func_impl, item["test"], timeout=10)
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
