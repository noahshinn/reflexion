python main.py \
  --run_name "reflexion_run_logs" \
  --root_dir "root" \
  --dataset_path ./benchmarks/humaneval-rs.jsonl \
  --strategy "reflexion" \
  --language "rs" \
  --model "gpt-4" \
  --pass_at_k "1" \
  --max_iters "2" \
  --verbose
