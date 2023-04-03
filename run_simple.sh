python main.py \
  --run_name "simple_mbpp_py" \
  --root_dir "root" \
  --dataset_path ./benchmarks/mbpp-py.jsonl \
  --strategy "simple" \
  --language "py" \
  --model "gpt-4" \
  --pass_at_k "1" \
  --max_iters "1" \
  --verbose
