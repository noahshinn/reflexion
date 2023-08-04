python main.py \
  --run_name "test_simple_run" \
  --root_dir "root" \
  --dataset_path ./benchmarks/humaneval-py.jsonl \
  --strategy "simple" \
  --language "py" \
  --model "starchat" \
  --pass_at_k "1" \
  --max_iters "1" \
  --verbose
