python main.py \
  --run_name "simple_rust_run" \
  --root_dir "root" \
  --dataset_path ./benchmarks/human_eval_rs.jsonl \
  --strategy "simple" \
  --language "rs" \
  --model "gpt-4" \
  --pass_at_k "1" \
  --max_iters "1" \
  --verbose
