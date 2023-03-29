import os
import signal
import subprocess

from rust_errors import grab_compile_errs, grab_runtime_errs, indent_code

from typing import List, Tuple, NamedTuple, Optional, Union


def timeout_handler(_, __):
    raise TimeoutError()


cargo_harness_dir = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), "rs/cargo_harness")


def create_temp_project() -> Tuple[str, str]:
    # get pid of the process
    pid = os.getpid()
    # get random number
    rand = os.urandom(8).hex()
    # create a temp directory
    temp_dir = f"/tmp/cargo_harness-{pid}-{rand}"
    # delete the temp directory if it exists
    if os.path.exists(temp_dir):
        os.system(f"rm -rf {temp_dir}")
    os.mkdir(temp_dir)
    # move the cargo harness into the temp directory
    os.system(f"cp -r {cargo_harness_dir}/* {temp_dir}")
    main_path = os.path.join(temp_dir, "src", "main.rs")
    return temp_dir, main_path


def write_to_file(path: str, code: str):
    prelude = "fn main() {\n"
    postlude = "\n}"
    code = prelude + indent_code(code) + postlude
    # delete the file if it exists
    if os.path.exists(path):
        os.remove(path)
    # write the code to the file
    with open(path, "w") as f:
        f.write(code)

def run_with_timeout(cmd: str, tmp_cargo_path: str, timeout: int = 5) -> Optional[Tuple[str, str]]:
    """
    Runs the given command with a timeout. Produces a tuple of stdout and stderr.
    If the command times out, returns None.
    """
    # set up the timeout handler
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(timeout)

    # run the command
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, cwd=tmp_cargo_path)
    try:
        out, err = p.communicate()
        # reset the timeout handler
        signal.alarm(0)
    except TimeoutError:
        p.kill()
        return None

    # decode the output
    out = out.decode("utf-8")
    err = err.decode("utf-8")
    print(f"errs: {err}")
    print(f"outs: {out}")

    return out, err


class ExecuteResult(NamedTuple):
    success_tests: List[str]
    failed_tests: Union[List[Tuple[str, str]], List[str]]

def execute(func: str, tests: List[str], timeout: int = 15) -> ExecuteResult:
    # Combine function code and assert statement
    func_test_list = [f'{func}\n{test}' for test in tests]

    tmp_dir, temp_file = create_temp_project()

    # run cargo check --message-format=json
    write_to_file(temp_file, func)
    res = run_with_timeout(
        "cargo check --message-format=json", tmp_dir, timeout=timeout)
    assert res is not None, "Timeout in cargo check, wow"

    errs = grab_compile_errs(res[0])  # (check returns stdin)
    if len(errs) > 0:
        # cleanup the temp directory
        os.system(f"rm -rf {tmp_dir}")
        return list(map(str, errs))

    # Run the tests and collect the results
    success_tests = []
    failed_tests = []
    num_tests = len(func_test_list)
    for i in range(num_tests):
        """
        # use some sort of timeout limit to handle infinite loops
        if pass, add to success tests
        if fail, add to failed tests with the log from the compiler
        """
        write_to_file(temp_file, func_test_list[i])

        # run cargo run
        res = run_with_timeout("cargo run", tmp_dir, timeout=timeout)
        if res is None:
            failed_tests.append((tests[i], "Timeout"))
            continue

        # check if we have any failed tests
        errs = grab_runtime_errs(res[1])
        if len(errs) > 0:
            failed_tests.append((tests[i], str(errs[0])))
            continue

        # if we get here, the test passed
        success_tests.append(tests[i])

    # cleanup the temp directory
    os.system(f"rm -rf {tmp_dir}")

    return success_tests, failed_tests


def execute_with_feedback(func: str, tests: List[str], timeout: int = 5) -> Tuple[str, bool]:
    """
    Returns a tuple of the feedback string and whether the code passed the tests.
    If the code failed to compile, the feedback string will contain the compile errors.
    Otherwise, the feedback string will contain the results of the tests, like:
    Tests passed:
    <test0>
    ...
    <testN>

    Tests failed:
    <test0> // output: <output0>
    ...
    <testN> // output: <outputN>
    """
    res = execute(func, tests, timeout=timeout)
    if isinstance(res, list):
        # compile error
        errr = "\n\n".join(res)
        feedback = f"Function failed to compile due to the following errors:\n{errr}"
        return feedback, False

    success_tests, failed_tests = res

    feedback = "Tested passed:"
    for test in success_tests:
        feedback += f"\n{test}"

    feedback += "\n\nTests failed:"
    for test, err in failed_tests:
        feedback += f"\n{test} // output: {err}"

    return feedback, len(failed_tests) == 0


if __name__ == "__main__":
    # Use this to test
    func = r"""
/// For a given number n, find the largest number that divides n evenly, smaller than n
/// >>> largest_divisor(15)
/// 5
fn largest_divisor(n: isize) -> isize {
    for i in (1..n).rev() {
        if n % i == 0 {
            return i;
        }
    }
    // if no divisor is found, return 1
    1
}
"""
    # first test is deliberately wrong
    tests = ["assert_eq!(largest_divisor(3), 2);", "assert_eq!(largest_divisor(7), 1);", "assert_eq!(largest_divisor(10), 5);",
             "assert_eq!(largest_divisor(100), 50);", "assert_eq!(largest_divisor(49), 7);"]
    feedback, passed = execute_with_feedback(func, tests)
    print(feedback)
    print(f"\n\n\n\npassed: {passed}")
