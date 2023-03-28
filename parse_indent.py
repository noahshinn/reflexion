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
    try:
        code = f'{DUMMY_FUNC_SIG}\n{func_body}\n{DUMMY_FUNC_CALL}'
        exec(code)
        return func_body
    except IndentationError:
        split = func_body.splitlines()
        if not split[0].endswith("    ") and not split[1].endswith("    "):
            # likely that the entire body is not indented
            return handle_entire_body_indent(func_body)
        elif not split[0].startswith("    "):
            # likely that only the first line is not indented
            return handle_first_line_indent(func_body)
        else:
            # not sure what to do here
            return func_body
    except Exception:
        # other syntax error likely due to missing identifier definitions
        return func_body

# for testing
if __name__ == "__main__":
    print(parse_indent(test0))
    print(parse_indent(test1))
    print(parse_indent(test2))
