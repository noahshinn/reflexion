python main.py \
  --run_name "reflexion_ucs_with_output2" \
  --root_dir "root" \
  --dataset_path ./benchmarks/human_eval_py.jsonl.gz \
  --strategy "reflexion-ucs" \
  --language "py" \
  --model "gpt-4" \
  --pass_at_k "1" \
  --max_iters "5" \
  --verbose
