python main.py \
  --run_name "reflexion_plays_with_the_ferris_crab/" \
  --root_dir "root" \
  --dataset_path ./benchmarks/human_eval_rs.jsonl \
  --strategy "reflexion" \
  --language "rs" \
  --model "gpt-4" \
  --pass_at_k "1" \
  --max_iters "5" \
  --verbose
