import sys
import signal

from utils import read_jsonl

TIMEOUT = 5  # seconds

assert len(sys.argv) == 2, "Please provide a log file"
LOG_PATH = sys.argv[1]

def red_text(text: str) -> str:
    return f"\033[91m{text}\033[0m"

def green_text(text: str) -> str:
    return f"\033[92m{text}\033[0m"

def count_test_cases(test_str: str) -> int:
    # dumb way to do this but works
    return test_str.count("assert")


def validate_py_results(log_path: str):
    if not log_path.endswith(".jsonl"):
        raise ValueError("Please provide a valid log file")
    data = read_jsonl(log_path)
    num_success = 0
    for i, item in enumerate(data):
        if item["is_solved"]:
            func_impl = item["solution"]
            code = f'{item["prompt"]}{func_impl}\n\n{item["test"]}\n\ncheck({item["entry_point"]})'
            num_tests = count_test_cases(item["test"])
            try:
                def handler(signum, frame):
                    nonlocal i
                    raise Exception("timeout on test case" + str(i))

                signal.signal(signal.SIGALRM, handler)
                signal.alarm(TIMEOUT)
                exec(code, globals()) 
                signal.alarm(0)
                green_text_out = green_text(f"passes {num_tests}/{num_tests} test cases")
                print(f"Test {i}: {green_text_out}")
                num_success += 1
            except Exception:
                red_text_out = red_text(f"failed but should have passed!")
                print(f"Test {i}: {red_text_out}")
        else:
            red_text_out = red_text(f"failed!")
            print(f"Test {i}: {red_text_out}")
    print(f"Summary: {num_success}/{len(data)} tests passed")
    print(f"Acc: {round(num_success/len(data), 3)} tests passed")

if __name__ == "__main__":
    validate_py_results(LOG_PATH)
