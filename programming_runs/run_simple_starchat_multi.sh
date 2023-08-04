CUDA_VISIBLE_DEVICES=$1 python main.py \
  --run_name "simple_run_starchat_$1" \
  --root_dir "root" \
  --dataset_path ./benchmarks/humaneval-py.jsonl \
  --strategy "simple" \
  --language "py" \
  --model "starchat" \
  --pass_at_k "1" \
  --max_iters "1" \
  --verbose | tee ./logs/simple_run_starchat_$1
