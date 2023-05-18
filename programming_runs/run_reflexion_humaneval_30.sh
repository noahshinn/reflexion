python main.py \
  --run_name "reflexion_humaneval30_py" \
  --root_dir "root" \
  --dataset_path ./benchmarks/humaneval-py_sample30.jsonl \
  --strategy "reflexion" \
  --language "py" \
  --model "gpt-4" \
  --pass_at_k "1" \
  --max_iters "5" \
  --verbose
