python main.py \
  --run_name "reflexion_test_run" \
  --root_dir "root" \
  --dataset_path ./human-eval/data/HumanEval.jsonl.gz \
  --strategy "reflexion" \
  --model "text-davinci-003" \
  --pass_at_k "1" \
  --max_iters "10" \
  --verbose
