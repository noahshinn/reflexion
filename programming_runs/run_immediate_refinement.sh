python main.py \
  --run_name "immediate_refinement_humaneval_rs_hardest50" \
  --root_dir "root" \
  --dataset_path ./benchmarks/humaneval-rs-hardest50.jsonl \
  --strategy "immediate-refinement" \
  --language "rs" \
  --model "gpt-4" \
  --pass_at_k "1" \
  --max_iters "5" \
  --verbose
