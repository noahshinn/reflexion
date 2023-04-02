python main.py \
  --run_name "reflexion_mbpp_rs" \
  --root_dir "root" \
  --dataset_path ./benchmarks/mbpp-rs.jsonl \
  --strategy "reflexion" \
  --language "rs" \
  --model "gpt-4" \
  --pass_at_k "1" \
  --max_iters "5" \
  --verbose
