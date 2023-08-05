import re
from typing import Optional


def parse_code_block(string: str, lang: str) -> Optional[str]:
    code_pattern = fr"```{lang}\n(.*?)\n```"
    match = re.search(code_pattern, string, re.DOTALL)
    if match:
        return match.group(1)
    else:
        return parse_first_func(string, lang)


def parse_first_func(code: str, lang: str) -> Optional[str]:
    assert lang == "python", "Only python is supported for now. TODO: Rust"
    code_lines = code.split("\n")
    def_i = 0
    last_i = 0
    for i, line in enumerate(code_lines):
        if line.startswith("def "):
            if def_i == 0:
                def_i = i
            else:
                break
        if line == "" and def_i != 0:
            last_i = i
            break

    if last_i == 0:
        last_i = len(code_lines) - 1

    if def_i == 0:
        return None

    return "\n".join(code_lines[def_i:last_i+1])

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
