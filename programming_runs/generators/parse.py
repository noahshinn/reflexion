import re
from typing import Optional


def parse_code_block(string: str, lang: str) -> Optional[str]:
    code_pattern = fr"```{lang}\n(.*?)\n```"
    match = re.search(code_pattern, string, re.DOTALL)

    if match:
        return match.group(1)

    generic_code_pattern = r"```\n(.*?)\n```"
    match = re.search(generic_code_pattern, string, re.DOTALL)

    if match:
        return match.group(1)

    return parse_first_func(string, lang)


def parse_first_func(code: str, lang: str) -> Optional[str]:
    assert lang == "python", "Only python is supported for now. TODO: Rust"
    code_lines = code.split("\n")
    def_i = -1
    last_i = 0
    got_return = False
    for i, line in enumerate(code_lines):
        if line.startswith("def "):
            if def_i == -1:
                def_i = i
            else:
                break
        elif "return" in line and def_i != -1:
            got_return = True
        if line == "" and def_i != -1 and got_return:
            last_i = i
            break

    if last_i == 0:
        last_i = len(code_lines) - 1

    if def_i == -1:
        return None

    return "\n".join(code_lines[def_i:last_i+1]).rstrip("[/PYTHON]")


def add_code_block(string: str, lang: str) -> str:
    return f"```{lang}\n{string}\n```"


if __name__ == "__main__":
    CODE = """
aldaas
sub_parser = parser.add_subparsers().add_parser("frf
a")

def my_wonderful_func():
    def useless_helper():
        return 1
    if 1:
        return 1
    else:
        return (
            1,
            2,
        )

sadsadsa
2023-08-04dsa
dsa

def bleh():
    return aaa
"""
    print(parse_code_block(CODE, "python"))
    CODE = """def total_match(lst1: List[str], lst2: List[str]) -> List[str]:
    \"\"\"
    Write a function that accepts two lists of strings and returns the list that has
    total number of chars in the all strings of the list less than the other list.
    
    if the two lists have the same number of chars, return the first list.
    
    Examples
    >>> total_match([], [])
    []
    >>> total_match(['hi', 'admin'], ['hI', 'Hi'])
    ['hI', 'Hi']
    >>> total_match(['hi', 'admin'], ['hi', 'hi', 'admin', 'project'])
    ['hi', 'admin']
    >>> total_match(['hi', 'admin'], ['hI', 'hi', 'hi'])
    ['hI', 'hi', 'hi']
    >>> total_match(['4'], ['1', '2', '3', '4', '5'])
    ['4']
    \"\"\"
    total_chars_lst1 = sum(len(word) for word in lst1)
    total_chars_lst2 = sum(len(word) for word in lst2)
    
    if total_chars_lst1 < total_chars_lst2:
        return lst1
    elif total_chars_lst1 > total_chars_lst2:
        return lst2
    else:
        return lst1
    """
    print(parse_code_block(CODE, "python"))
