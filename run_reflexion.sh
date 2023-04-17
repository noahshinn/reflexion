python main.py \
  --run_name "reflexion_humaneval_py_hardest50" \
  --root_dir "root" \
  --dataset_path ./benchmarks/humaneval-py_hardest50.jsonl \
  --strategy "reflexion" \
  --language "py" \
  --model "gpt-4" \
  --pass_at_k "1" \
  --max_iters "5" \
  --verbose
