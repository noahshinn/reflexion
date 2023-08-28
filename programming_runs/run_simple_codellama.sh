python main.py \
  --run_name "test_simple_run_codellama" \
  --root_dir "root" \
  --dataset_path ./benchmarks/humaneval-py.jsonl \
  --strategy "simple" \
  --language "py" \
  --model "codellama" \
  --pass_at_k "1" \
  --max_iters "1" \
  --verbose
