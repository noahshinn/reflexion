# Usage: python evaluate_leet_results.py <lang> <input_log_path> <output_log_path>
from executors.leetcode_env.leetcode_env.environment import LeetCodeEnv
from executors.leetcode_env.leetcode_env.leetcode_types import LeetCodeSubmission, ProgrammingLanguage
from executors.leetcode_env.leetcode_env.utils import PySubmissionFormatter, RsSubmissionFormatter
from utils import read_jsonl
import sys

assert len(sys.argv) == 3, "Provide a language [py, rs], input and output log file"
lang = sys.argv[1]
input_log_path = sys.argv[2]
output_log_path = sys.argv[3]

if lang == "py":
    formatter = PySubmissionFormatter
    lang = ProgrammingLanguage.PYTHON
elif lang == "rs":
    formatter = RsSubmissionFormatter
    lang = ProgrammingLanguage.RUST
else:
    raise ValueError("Provide a valid language (rs or py)")

lines = read_jsonl(input_log_path)

for line in lines:
    assert "implementations" in line, "Log file must contain implementations"

env = LeetCodeEnv()

for line in lines:
    line["evaluations"] = []
    for impl in line["implementations"]:
        
        submission = LeetCodeSubmission(
            code=formatter.to_leetcode(impl),
            lang=lang,
            question_slug=impl["task_id"],
        )

        status, reward, done, info = env.step(submission)

        line["evaluations"].append({
            "status": status,
            "reward": reward,
            "done": done,
            "info": info,
        })

        env.reset()



