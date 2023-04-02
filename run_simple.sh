python main.py \
  --run_name "simple_mbpp_rs" \
  --root_dir "root" \
  --dataset_path ./benchmarks/mbpp-rs.jsonl \
  --strategy "simple" \
  --language "rs" \
  --model "gpt-4" \
  --pass_at_k "1" \
  --max_iters "1" \
  --verbose
