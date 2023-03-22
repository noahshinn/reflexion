import ast
import signal
import astunparse

from typing import List, Tuple

def timeout_handler(_, __):
    raise TimeoutError()

def execute(func: str, tests: List[str], with_output: bool = False, timeout: int = 5) -> Tuple[List[str], List[str]]:
    # Combine function code and assert statement
    func_test_list = [f'{func}\n{test}' for test in tests]

    # Run the tests and collect the results
    success_tests = []
    failed_tests = []
    num_tests = len(func_test_list)
    for i in range(num_tests):
        try:
            # Set the alarm
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(timeout)

            # Run the test and disable the alarm
            exec(func_test_list[i], globals())
            signal.alarm(0)

            success_tests += [tests[i]]
        except Exception as e:
            if with_output:
                output = get_output(func, tests[i], timeout=timeout)
                failed_tests += [f"{tests[i]} # output: {output}"]
            else:
                failed_tests += [tests[i]]

    return success_tests, failed_tests

def get_call_str(assert_statement: str) -> str:
    call_str = ast.parse(assert_statement).body[0].test.left # type: ignore
    return astunparse.unparse(call_str).strip()

def get_output(func: str, assert_statement: str, timeout: int = 5) -> str:
    try:
        func_call = get_call_str(assert_statement)
        exec(func, globals())

        # set the alarm
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(timeout)
        # Run the test and disable the alarm
        output = eval(func_call)
        signal.alarm(0)
        return output
    except TimeoutError:
        return "TIMEOUT"
    except Exception as e:
        return str(type(e).__name__)

def execute_with_feedback(func: str, tests: List[str], timeout: int = 5) -> Tuple[str, List[str], List[str]]:
    """
    Returns a feedback string with the following structure:

    Tests passed:
    <test0>
    ...
    <testN>

    Tests failed:
    <test0> # output: <output0>
    ...
    <testN> # output: <outputN>

    """
    success_tests, failed_tests = execute(func, tests, with_output=True, timeout=timeout)
    feedback = "Tested passed:"
    for test in success_tests:
        feedback += f"\n{test}"
    feedback += "\n\nTests failed:"
    for test in failed_tests:
        feedback += f"\n{test}"

    return feedback, success_tests, failed_tests

if __name__ == "__main__":
    # Test the function
    func = "def add(a, b):\n    while True:\n        x = 1\n    return a + b"
    tests = ["assert add(1, 2) == 3", "assert add(1, 2) == 4"]
    print(execute_with_feedback(func, tests, timeout=1))
