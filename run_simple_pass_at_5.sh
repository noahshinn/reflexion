python main.py \
  --run_name "simple_humaneval30_py_pass_at_5" \
  --root_dir "root" \
  --dataset_path ./benchmarks/humaneval-py_sample30.jsonl \
  --strategy "simple" \
  --language "py" \
  --model "gpt-4" \
  --pass_at_k "5" \
  --max_iters "1" \
  --verbose
