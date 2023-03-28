test0 = """    res = 0
    for i in range(len(l)):
        res += l[i] * 2 ** i
    return res"""

test1 = """res = 0
    for i in range(len(l)):
        res += l[i] * 2 ** i
    return res"""

test2 = """res = 0
for i in range(len(l)):
    res += l[i] * 2 ** i
return res"""

test3 = """if x == 5:
        print("x is 5")
    return res"""

DUMMY_FUNC_SIG = "def func():"
DUMMY_FUNC_CALL = "func()"

def handle_first_line_indent(func_body: str) -> str:
    if func_body.startswith("    "):
        return func_body
    split = func_body.splitlines()
    return f"    {split[0]}\n" + "\n".join(split[1:])

def handle_entire_body_indent(func_body: str) -> str:
    split = func_body.splitlines()
    res = "\n".join(["    " + line for line in split])
    return res

def parse_indent(func_body: str) -> str:
    """
    3 cases:
        1. good syntax
        2. first line not good
        3. entire body not good
    """
    def parse_indent_rec(f_body: str, cur_state: int) -> str:
        if cur_state > 1:
            return f_body
        code = f'{DUMMY_FUNC_SIG}\n{f_body}\n{DUMMY_FUNC_CALL}'
        try:
            exec(code)
            return f_body
        except (IndentationError, SyntaxError):
            p_func = handle_first_line_indent if cur_state == 0 else handle_entire_body_indent
            return parse_indent_rec(p_func(func_body), cur_state + 1)
        except Exception as e:
            print(e.args)
            # print kind of error
            print(e.__class__.__name__)
            return f_body
    return parse_indent_rec(func_body, 0)

# for testing
if __name__ == "__main__":
    print(parse_indent(test0))
    print("\n\n\n")
    print(parse_indent(test1))
    print("\n\n\n")
    print(parse_indent(test2))
    print("\n\n\n")
    print(parse_indent(test3))
