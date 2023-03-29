import json

from typing import List

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
    def __init__(self, left, right, line, column):
        self.left = left
        self.right = right
        self.line = line
        self.column = column

    def __str__(self):
        return f"assertion failed: {self.left} == {self.right} at line {self.line}, column {self.column}"

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
    for line in split:
        if "left:" in line:
            curr_left = line.split("`")[1]
        elif "right:" in line:
            curr_right = line.split("`")[1]
            # get the line and column number
            fileinto = line.split(",")[-1]
            line = int(fileinto.split(":")[1])
            column = int(fileinto.split(":")[2])
            failed_asserts.append(RuntimeErr(curr_left, curr_right, line, column))





    return failed_asserts


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
