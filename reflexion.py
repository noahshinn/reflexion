from executor import execute_with_feedback, execute
from test_generation import generate_internal_unit_tests
from utils import gpt_completion, gpt_chat, write_jsonl, parse_body, build_asserts_from_human_eval

from typing import List

SIMPLE_COMPLETION_INSTRUCTION = "# Write the body of this function only."
REFLEXION_COMPLETION_INSTRUCTION = "You are CodexGPT. You will be given your past function implementation, a series of unit tests, and a hint to change the implementation appropriately. Apply the changes below by writing the body of this function only.\n\n-----"
SELF_REFLECTION_COMPLETION_INSTRUCTION = "You are CodexGPT. You will be given a function implementation and a series of unit tests. Your goal is to write a few sentences to explain why your implementation is wrong as indicated by the tests. You will need this as a hint when you try again later. Only provide the few sentence description in your answer, not the implementation.\n\n-----"
SIMPLE_CHAT_INSTRUCTION = "You are CodexGPT. You will be given a function signature and docstring. You should fill in the following text of the missing function body. For example, the first line of the completion should have 4 spaces for the indendation so that it fits syntactically with the preceding signature."
REFLEXION_CHAT_INSTRUCTION = "You are CodexGPT. You will be given your past function implementation, a series of unit tests, and a hint to change the implementation appropriately. Apply the changes below by writing the body of this function only. You should fill in the following text of the missing function body. For example, the first line of the completion should have 4 spaces for the indendation so that it fits syntactically with the preceding signature."
SELF_REFLECTION_CHAT_INSTRUCTION = "You are CodexGPT. You will be given a function implementation and a series of unit tests. Your goal is to write a few sentences to explain why your implementation is wrong as indicated by the tests. You will need this as a hint when you try again later. Only provide the few sentence description in your answer, not the implementation."

def get_reflection(func: str, feedback: str, model: str) -> str:
    if model == "gpt-4" or model == "gpt-3.5-turbo":
        reflection = gpt_chat(model, SELF_REFLECTION_CHAT_INSTRUCTION, f'{func}\n\n{feedback}\n\nExplanation:')
    else:
        reflection = gpt_completion(model, f'{SELF_REFLECTION_COMPLETION_INSTRUCTION}\n{func}\n\n{feedback}\n\nExplanation:')

    return reflection # type: ignore

def run_reflexion(
        dataset: List[dict],
        model: str,
        max_iters: int,
        pass_at_k: int,
        log_path: str,
        verbose: bool
    ) -> None:
    num_items = len(dataset)
    num_success = 0
    for i, item in enumerate(dataset):
        cur_pass = 0
        is_solved = False
        unit_tests_static: List[str] = build_asserts_from_human_eval(item["test"], item["entry_point"])
        reflections = []
        while cur_pass < pass_at_k and not is_solved:
            # generate internal unit tests
            internal_unit_tests_static: List[str] = generate_internal_unit_tests(model, item["prompt"])

            # first attempt
            if model == "gpt-4" or model == "gpt-3.5-turbo":
                soln = parse_body(gpt_chat(model, SIMPLE_CHAT_INSTRUCTION, item["prompt"]))
            else:
                soln = parse_body(gpt_completion(model, f'{SIMPLE_COMPLETION_INSTRUCTION}\n{item["prompt"]}'))
            func = item["prompt"] + soln
            _, failed_tests = execute(func, unit_tests_static)

            # solved, exit early
            if len(failed_tests) == 0:
                item["solution"] = soln
                is_solved = True
                num_success += 1
                break

            # if not, use internal unit tests to get feedback on unit tests
            feedback, _, _ = execute_with_feedback(func, internal_unit_tests_static)

            # use self-reflection to iteratively improve
            cur_iter = 1
            cur_func = func
            cur_feedback = feedback
            while cur_iter < max_iters:
                # get self-reflection
                reflection = get_reflection(cur_func, cur_feedback, model)
                reflections += [reflection]

                # apply self-reflection in the next attempt
                if model == "gpt-4" or model == "gpt-3.5-turbo":
                    message = f'previous implementation:\n{cur_func}\n\nunit tests:\n{cur_feedback}\n\nhint:\n{reflection}\n\n# improved implementation\n{item["prompt"]}'
                    soln = parse_body(gpt_chat(model, REFLEXION_CHAT_INSTRUCTION, message))
                else:
                    prompt = f'{REFLEXION_COMPLETION_INSTRUCTION}\n{cur_func}\n\nunit tests:\n{cur_feedback}\n\nhint:\n{reflection}\n\n# improved implementation\n{item["prompt"]}'
                    soln = parse_body(gpt_completion(model, prompt))
                cur_func = item["prompt"] + soln

                # check if all internal unit tests pass
                cur_feedback, _, failed_internal_tests = execute_with_feedback(cur_func, internal_unit_tests_static)

                # if solved, check if it passes the real tests, exit early
                if len(failed_internal_tests) == 0:
                    _, failed_tests = execute(cur_func, unit_tests_static)
                    if len(failed_tests) == 0:
                        item["solution"] = soln
                        is_solved = True
                        num_success += 1
                    break

                # if it's the last attempt, check if the current solution passes the real tests
                if cur_iter == max_iters - 1:
                    _, failed_tests = execute(cur_func, unit_tests_static)
                    if len(failed_tests) == 0:
                        item["solution"] = soln
                        is_solved = True
                        num_success += 1

                cur_iter += 1
            cur_pass += 1

        if is_solved:
            item["is_solved"] = True
        else:
            item["is_solved"] = False
            item["solution"] = ""
        item["reflections"] = reflections
        write_jsonl(log_path, [item], append=True)

        if verbose:
            print(f'completed {i+1}/{num_items}: acc = {round(num_success/(i+1), 2)}')
