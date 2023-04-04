import os
import signal
import subprocess
import json

from .executor_utils import timeout_handler
from .executor_types import ExecuteResult, Executor

from typing import List, Tuple, Optional


cargo_harness_dir = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), "cargo_harness")


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


def write_to_file_toplevel(path: str, code: str):
    # delete the file if it exists
    if os.path.exists(path):
        os.remove(path)
    # write the code to the file
    with open(path, "w") as f:
        f.write(code)


def run_with_timeout(cmd: str, tmp_cargo_path: str, timeout: int = 5, print_debug: bool = False) -> Optional[Tuple[str, str]]:
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
    if print_debug:
        print("## RUN OUTPUTS ##")
        print("STDOUT:")
        print(out)
        print("STDERR:")
        print(err, flush=True)

    return out, err


class RsExecutor(Executor):
    def execute(self, func: str, tests: List[str], timeout: int = 5) -> ExecuteResult:
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
            state = tuple([False] * len(tests))

            err_str = ""
            for err in errs:
                err_str += f"\n{err}"

            return ExecuteResult(False, err_str, state)

        # Run the tests and collect the results
        tests_res: List[Tuple[bool, str]] = []
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
                tests_res.append((False, "Timeout"))
                continue

            # check if we have any failed tests
            errs = grab_runtime_errs(res[1])
            if len(errs) > 0:
                tests_res.append((False, str(errs[0])))
                continue

            # if we get here, the test passed
            tests_res.append((True, ""))

        # cleanup the temp directory
        os.system(f"rm -rf {tmp_dir}")

        passed_str = ""
        failed_str = ""
        state = []
        for i, (passed, output) in enumerate(tests_res):
            test = tests[i]
            if passed:
                passed_str += f"\n{test}"
            else:
                failed_str += f"\n{test} // output: {output}"
            state.append(passed)

        feedback = "Tested passed:"
        feedback += passed_str
        feedback += "\n\nTests failed:"
        feedback += failed_str

        is_passing = len(failed_str) == 0

        return ExecuteResult(is_passing, feedback, tuple(state))

    def evaluate(self, name: str, func: str, test: str, timeout: int = 5) -> bool:
        """
        Evaluates the implementation on Human-Eval Rust (MultiPL-E generated,

        Federico Cassano, John Gouwar, Daniel Nguyen, Sydney Nguyen, Luna Phipps-Costin, Donald Pinckney, Ming-Ho Yee, Yangtian Zi, Carolyn Jane Anderson, Molly Q Feldman, Arjun Guha, Michael Greenberg, Abhinav Jangda ).
        If you use this function please cite:
        @misc{cassano2022multiple,
          title={MultiPL-E: A Scalable and Extensible Approach to Benchmarking Neural Code Generation}, 
          author={Federico Cassano and John Gouwar and Daniel Nguyen and Sydney Nguyen and Luna Phipps-Costin and Donald Pinckney and Ming-Ho Yee and Yangtian Zi and Carolyn Jane Anderson and Molly Q Feldman and Arjun Guha and Michael Greenberg and Abhinav Jangda},
          year={2022},
          eprint={2208.08227},
          archivePrefix={arXiv},
          primaryClass={cs.LG}
        })

        TODO: do it actually
        """
        tmp_dir, tmp_path = create_temp_project()
        print(f"Evaluating\n{func + test}", flush=True)
        write_to_file_toplevel(tmp_path, func + test)

        res = run_with_timeout(
            "cargo check --message-format=json", tmp_dir, timeout=timeout, print_debug=True)
        assert res is not None, "Timeout in cargo check, wow"

        errs = grab_compile_errs(res[0])  # (check returns stdin)
        if len(errs) > 0:
            # cleanup the temp directory
            os.system(f"rm -rf {tmp_dir}")
            print("Compile errors. Failed eval", flush=True)
            return False

        # compile and run the binary
        res = run_with_timeout("cargo run", tmp_dir,
                               timeout=timeout, print_debug=True)
        os.system(f"rm -rf {tmp_dir}")

        if res is None:
            print("Timeout?. Failed eval", flush=True)
            return False
        else:
            errs = grab_runtime_errs(res[1])
            if len(errs) > 0:
                print("Runtime errors. Failed eval", flush=True)
                return False

            print("Passed eval", flush=True)
            return len(errs) == 0


assert_no_panic = r"""
macro_rules! assert_eq_nopanic {
    ($left:expr, $right:expr) => {
        std::panic::catch_unwind(|| {
            assert_eq!($left, $right);
        }).unwrap_or_else(|_| {});
    };
    () => {};
}
"""


def transform_asserts(code: str) -> str:
    """
    Transform all asserts into assert_eq_nopanic! asserts, inserting the macro
    definition at the top of the code.
    """
    code.replace("assert_eq!", "assert_eq_nopanic!")
    return assert_no_panic + code


def revert_asserts(code: str) -> str:
    """
    Revert all assert_eq_nopanic! asserts back into assert_eq! asserts.
    """
    normal = code.replace("assert_eq_nopanic!", "assert_eq!")
    # remove the macro definition
    return normal[len(assert_no_panic):]


def indent_code(code: str, spaces: int = 4) -> str:
    """
    Indent the code by the given number of spaces.
    """
    return "\n".join([" " * spaces + line for line in code.splitlines()])


class CompileErr:
    def __init__(self, rendered):
        self.rendered = rendered

    def __str__(self):
        return self.rendered

    def __repr__(self):
        return "{" + str(self) + "}"


class RuntimeErr:
    def __init__(self, left, right, line, column, panic_reason):
        # right and left are only used for assert_eq! errors
        self.left = left
        self.right = right
        # NOTE: currently not using the below
        self.line = line
        self.column = column
        self.panic_reason = panic_reason

    def __str__(self):
        if self.left is not None and self.right is not None:
            return f"assertion failed: {self.left} == {self.right}"
        else:
            return self.panic_reason

    def __repr__(self):
        return "{" + str(self) + "}"


# assumes that the input is the stdout of cargo check --message-format=json
# returns a list of compile errors as CompileErr objects
def grab_compile_errs(inp: str) -> List[CompileErr]:
    # we get a stream of json objects, so we need to parse them one by one
    objs = []
    for line in inp.splitlines():
        if line == "":
            continue
        o = json.loads(line)
        if o is not None and o["reason"] == "compiler-message" and \
                o["message"]["level"] == "error" and \
                o["message"]["spans"] != []:
            rendered = o["message"]["rendered"]
            objs.append(CompileErr(rendered))

    return objs

# assumes that the given input is the stderr of cargo run.
# returns a list of failed assertions as RuntimeErr objects


def grab_runtime_errs(inp: str) -> List[RuntimeErr]:
    failed_asserts = []
    split = inp.splitlines()
    curr_left = None
    panic_reason = None
    for line in split:
        if "fatal runtime" in line:
            # we have a panic
            panic_idx = line.index("fatal runtime")
            panic_reason = line[panic_idx + len("fatal runtime") + 1:]
        elif "panicked at" in line:
            panic_idx = line.index("panicked at")
            # strip source line if it exists
            if "src/main.rs" in line:
                line = line[:line.index("src/main.rs")]
            panic_reason = line[panic_idx + len("panicked at") + 1:]
        elif "left:" in line:
            split = line.split("`")
            if len(split) < 2:
                continue
            curr_left = split[1]
        elif "right:" in line:
            split = line.split("`")
            if len(split) < 2:
                continue
            curr_right = split[1]
            # get the line and column number
            fileinto = line.split(",")[-1]
            line = int(fileinto.split(":")[1])
            column = int(fileinto.split(":")[2])
            failed_asserts.append(RuntimeErr(
                curr_left, curr_right, line, column, panic_reason))
            curr_left = None
            panic_reason = None

    if panic_reason is not None:
        failed_asserts.append(RuntimeErr(None, None, None, None, panic_reason))

    return failed_asserts


if __name__ == "__main__":
    test_runtime = r"""
        Finished dev [unoptimized + debuginfo] target(s) in 0.00s
         Running `target/debug/testing`
    thread 'main' panicked at 'assertion failed: `(left == right)`
      left: `1`,
     right: `2`', src/main.rs:11:5
    note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
    thread 'main' panicked at 'assertion failed: `(left == right)`
      left: `3`,
     right: `2`', src/main.rs:12:5
     thread 'main' panicked at 'assertion failed: `(left == right)`
      left: `[5, -3, -4]`,
     right: `[-4, -3, 5]`', src/main.rs:24:5
    note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
     thread 'main' panicked at 'assertion failed: `(left == right)`
      left: `"hello"`,
     right: `"hola"`', src/main.rs:24:5
    note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
    """

    # test input
    test_compiletime = r"""
    {"reason":"compiler-message","package_id":"testing 0.1.0 (path+file:///home/elleven/Downloads/testing)","manifest_path":"/home/elleven/Downloads/testing/Cargo.toml","target":{"kind":["bin"],"crate_types":["bin"],"name":"testing","src_path":"/home/elleven/Downloads/testing/src/main.rs","edition":"2021","doc":true,"doctest":false,"test":true},"message":{"rendered":"error[E0282]: type annotations needed\n --> src/main.rs:2:9\n  |\n2 |     let sakfsdfjfndslv;\n  |         ^^^^^^^^^^^^^^\n  |\nhelp: consider giving `sakfsdfjfndslv` an explicit type\n  |\n2 |     let sakfsdfjfndslv: _;\n  |                       +++\n\n","children":[{"children":[],"code":null,"level":"help","message":"consider giving `sakfsdfjfndslv` an explicit type","rendered":null,"spans":[{"byte_end":34,"byte_start":34,"column_end":23,"column_start":23,"expansion":null,"file_name":"src/main.rs","is_primary":true,"label":null,"line_end":2,"line_start":2,"suggested_replacement":": _","suggestion_applicability":"HasPlaceholders","text":[{"highlight_end":23,"highlight_start":23,"text":"    let sakfsdfjfndslv;"}]}]}],"code":{"code":"E0282","explanation":"The compiler could not infer a type and asked for a type annotation.\n\nErroneous code example:\n\n```compile_fail,E0282\nlet x = \"hello\".chars().rev().collect();\n```\n\nThis error indicates that type inference did not result in one unique possible\ntype, and extra information is required. In most cases this can be provided\nby adding a type annotation. Sometimes you need to specify a generic type\nparameter manually.\n\nA common example is the `collect` method on `Iterator`. It has a generic type\nparameter with a `FromIterator` bound, which for a `char` iterator is\nimplemented by `Vec` and `String` among others. Consider the following snippet\nthat reverses the characters of a string:\n\nIn the first code example, the compiler cannot infer what the type of `x` should\nbe: `Vec<char>` and `String` are both suitable candidates. To specify which type\nto use, you can use a type annotation on `x`:\n\n```\nlet x: Vec<char> = \"hello\".chars().rev().collect();\n```\n\nIt is not necessary to annotate the full type. Once the ambiguity is resolved,\nthe compiler can infer the rest:\n\n```\nlet x: Vec<_> = \"hello\".chars().rev().collect();\n```\n\nAnother way to provide the compiler with enough information, is to specify the\ngeneric type parameter:\n\n```\nlet x = \"hello\".chars().rev().collect::<Vec<char>>();\n```\n\nAgain, you need not specify the full type if the compiler can infer it:\n\n```\nlet x = \"hello\".chars().rev().collect::<Vec<_>>();\n```\n\nApart from a method or function with a generic type parameter, this error can\noccur when a type parameter of a struct or trait cannot be inferred. In that\ncase it is not always possible to use a type annotation, because all candidates\nhave the same return type. For instance:\n\n```compile_fail,E0282\nstruct Foo<T> {\n    num: T,\n}\n\nimpl<T> Foo<T> {\n    fn bar() -> i32 {\n        0\n    }\n\n    fn baz() {\n        let number = Foo::bar();\n    }\n}\n```\n\nThis will fail because the compiler does not know which instance of `Foo` to\ncall `bar` on. Change `Foo::bar()` to `Foo::<T>::bar()` to resolve the error.\n"},"level":"error","message":"type annotations needed","spans":[{"byte_end":34,"byte_start":20,"column_end":23,"column_start":9,"expansion":null,"file_name":"src/main.rs","is_primary":true,"label":null,"line_end":2,"line_start":2,"suggested_replacement":null,"suggestion_applicability":null,"text":[{"highlight_end":23,"highlight_start":9,"text":"    let sakfsdfjfndslv;"}]}]}}
    {"reason":"compiler-message","package_id":"testing 0.1.0 (path+file:///home/elleven/Downloads/testing)","manifest_path":"/home/elleven/Downloads/testing/Cargo.toml","target":{"kind":["bin"],"crate_types":["bin"],"name":"testing","src_path":"/home/elleven/Downloads/testing/src/main.rs","edition":"2021","doc":true,"doctest":false,"test":true},"message":{"rendered":"error: aborting due to previous error\n\n","children":[],"code":null,"level":"error","message":"aborting due to previous error","spans":[]}}
    {"reason":"compiler-message","package_id":"testing 0.1.0 (path+file:///home/elleven/Downloads/testing)","manifest_path":"/home/elleven/Downloads/testing/Cargo.toml","target":{"kind":["bin"],"crate_types":["bin"],"name":"testing","src_path":"/home/elleven/Downloads/testing/src/main.rs","edition":"2021","doc":true,"doctest":false,"test":true},"message":{"rendered":"For more information about this error, try `rustc --explain E0282`.\n","children":[],"code":null,"level":"failure-note","message":"For more information about this error, try `rustc --explain E0282`.","spans":[]}}
    {"reason":"build-finished","success":false}
    """

    assert(len(grab_compile_errs(test_compiletime)) == 1)
    print(grab_runtime_errs(test_runtime))
    assert(len(grab_runtime_errs(test_runtime)) == 4)
