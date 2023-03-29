python main.py \
  --run_name "reflexion_scratch" \
  --root_dir "root" \
  --dataset_path ./benchmarks/human_eval_rust.jsonl \
  --strategy "reflexion" \
  --language "rs" \
  --model "gpt-4" \
  --pass_at_k "1" \
  --max_iters "10" \
  --verbose
