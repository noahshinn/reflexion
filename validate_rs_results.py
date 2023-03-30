import sys
import signal

from utils import read_jsonl
from executors.rs_executor import rs_evaluate

TIMEOUT = 5  # seconds

assert len(sys.argv) == 2, "Please provide a log file"
LOG_PATH = sys.argv[1]

def red_text(text: str) -> str:
    return f"\033[91m{text}\033[0m"

def green_text(text: str) -> str:
    return f"\033[92m{text}\033[0m"

def count_test_cases(test_str: str) -> int:
    # dumb way to do this but works
    return test_str.count("assert_eq")


def validate_rs_results(log_path: str):
    if not log_path.endswith(".jsonl"):
        raise ValueError("Please provide a valid log file")
    data = read_jsonl(log_path)
    num_success = 0
    for i, item in enumerate(data):
        if item["is_solved"]:
            func_impl = item["solution"]
            num_tests = count_test_cases(item["test"])

            res = rs_evaluate(item["entry_point"], func_impl, item["test"])   
            if res is None:
                red_text_out = red_text(f"failed but should have passed!")
                print(f"Test {i}: {red_text_out}")
            else:
                green_text_out = green_text(f"passes {num_tests}/{num_tests} test cases")
                print(f"Test {i}: {green_text_out}")
                num_success += 1
        else:
            red_text_out = red_text(f"failed!")
            print(f"Test {i}: {red_text_out}")
    print(f"Summary: {num_success}/{len(data)} tests passed")
    print(f"Acc: {round(num_success/len(data), 2)} tests passed")

if __name__ == "__main__":
    validate_rs_results(LOG_PATH)
