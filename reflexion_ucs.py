import warnings
from lazzzy.ucs import ucs
from utils import write_jsonl, parse_body
from executors import py_evaluate, py_execute
from generators import py_generate_func_impl, py_generate_self_reflection, py_generate_internal_tests

from typing import List, Set, Tuple


DEBUG = True

def debug_print(*args):
    if DEBUG:
        print(*args, flush=True)

class State:
    def __init__(self, code: str, feedback: str, reflection: str, state: Tuple[bool]):
        self.code = code
        self.feedback = feedback
        self.reflection = reflection
        self.state = state

    def __repr__(self):
        return f"State(code={self.code}, feedback={self.feedback}, reflection={self.reflection}, state={self.state})"

    def is_goal(self):
        return all(self.state)

    def __hash__(self):
        return hash((self.code, self.feedback, self.reflection))

    def get_unique_id(self):
        res = 0
        for i in range(len(self.state)):
            res += self.state[i] * (2**i)

        return res


def run_reflexion_ucs(
    dataset: List[dict],
    model: str,
    language: str,
    max_iters: int,
    pass_at_k: int,
    log_path: str,
    verbose: bool,
    expansion_factor: int
) -> None:
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
            debug_print(f"item {i} pass {cur_pass}")
            tests_i = internal_test_generator(item["prompt"], model, 1)
            if len(tests_i) == 0:
                warnings.warn(f"no internal tests generated for item {i}")

            # first attempt
            debug_print("first attempt")
            cur_func_impl = parse_body(
                func_impl_generator(item["prompt"], model, "simple"))
            assert isinstance(cur_func_impl, str)  # num_comps of 1
            is_passing, feedback, state = execute(cur_func_impl, tests_i)

            debug_print(f"first attempt: \n{cur_func_impl}\n{feedback}\n{state}")

            # if solved, exit early
            if is_passing:
                debug_print("solved at first attempt")
                is_solved = True
                num_success += 1
                break

            reflection = self_reflection_generator(
                cur_func_impl, feedback, model)
            reflections.append(reflection)

            start = State(cur_func_impl, feedback, reflection, state)

            def expand(state: State) -> Set[Tuple[State, float]]:
                nonlocal max_iters
                nonlocal expansion_factor
                nonlocal item
                nonlocal model
                nonlocal tests_i
                nonlocal reflections

                new_states: Set[Tuple[State, float]] = set()

                debug_print(f"start expansion of: {state.state}")
                new_funcs = func_impl_generator(
                    func_sig=item["prompt"],
                    model=model,
                    strategy="reflexion",
                    prev_func_impl=state.code,
                    feedback=state.feedback,
                    self_reflection=state.reflection,
                    num_comps=expansion_factor,
                    temperature=0.75
                )
                assert isinstance(new_funcs, list)
                debug_print(f"generated num of funcs: {len(new_funcs)}")

                already_seen = set()

                for new_func in new_funcs:
                    if new_func in already_seen:
                        debug_print(f"skipping a func because already seen.")
                        continue

                    already_seen.add(new_func)

                    is_passing, feedback, new_state = execute(new_func, tests_i)
                    debug_print(f"expanding: \n{new_func}\n{feedback}\n{new_state}")

                    if is_passing:
                        # return immediately if solved
                        return set([(State(new_func, feedback, "", new_state), 0)])

                    new_reflection = self_reflection_generator(new_func, feedback, model)
                    reflections.append(new_reflection)

                    num_failing = len([x for x in new_state if not x])
                    new_states.add(
                        (State(new_func, feedback, new_reflection, new_state), num_failing))


                debug_print(f"returning new states: {new_states}")

                return new_states

            def when_none(l: List[State]) -> State:
                debug_print(f"when_none called on: {l}")
                return min(l, key=lambda x: len([y for y in x.state if not y]))

            # this is either the goal state, or if not found, the current best state (lowest failed tests)
            best = ucs(
                start=start,
                expand=expand,
                is_goal=lambda x: x.is_goal(),
                # NOTE: this way we reduce our search space significantly
                # the maximum number of nodes is 2^num_tests,
                # which is 2^5 = 32
                get_unique_id=lambda x: x.get_unique_id(),
                when_none=when_none
            )
            assert best is not None  # impossible due to our when_none

            is_passing = evaluate(
                item["entry_point"], best.code, item["test"], timeout=5)
            if is_passing:
                item["solution"] = best.code
                is_solved = True
                num_success += 1
                break  # breaking pass@k loop

            cur_pass += 1

        item["is_solved"] = is_solved
        item["reflections"] = reflections
        item["solution"] = cur_func_impl
        write_jsonl(log_path, [item], append=True)

        if verbose:
            print(
                f'completed {i+1}/{num_items}: acc = {round(num_success/(i+1), 2)}')
