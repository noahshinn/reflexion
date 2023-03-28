import os
import argparse

from simple import run_simple
from reflexion import run_reflexion
from reflexion_ucs import run_reflexion_ucs
from utils import read_jsonl, read_jsonl_gz


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run_name", type=str, help="The name of the run")
    parser.add_argument("--root_dir", type=str,
                        help="The root logging directory", default="root")
    parser.add_argument("--dataset_path", type=str,
                        help="The path to the benchmark dataset", default="root")
    parser.add_argument("--strategy", type=str,
                        help="Strategy: `simple`, `reflexion`")
    parser.add_argument("--language", type=str, help="Strategy: `py`")
    parser.add_argument(
        "--model", type=str, help="OpenAI models only for now. For best results, use GPT-4")
    parser.add_argument("--pass_at_k", type=int,
                        help="Pass@k metric", default=1)
    parser.add_argument("--max_iters", type=int,
                        help="The maximum number of self-improvement iterations", default=10)
    parser.add_argument("--expansion_factor", type=int,
                        help="The expansion factor for the reflexion UCS and A* strategy", default=3)
    parser.add_argument("--verbose", action='store_true',
                        help="To print live logs")
    # TODO: implement this
    # parser.add_argument("--is_resume", action='store_true', help="To resume run")
    # parser.add_argument("--resume_dir", type=str, help="If resume, the logging directory", default="")
    args = parser.parse_args()
    return args


def main(args):
    # check if the root dir exists and create it if not
    if not os.path.exists(args.root_dir):
        os.makedirs(args.root_dir)

    # check if log path already exists
    log_dir = os.path.join(args.root_dir, args.run_name)
    log_path = os.path.join(
        log_dir, f"{args.strategy}_{args.max_iters}_{args.model}_pass_at_k_{args.pass_at_k}.jsonl")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    if os.path.exists(log_path):
        raise ValueError(
            f"Log path `{log_path}` already exists in `{log_dir}`")

    # check if the strategy is valid
    if args.strategy not in ["simple", "reflexion", "reflexion-ucs"]:
        raise ValueError(f"Strategy `{args.strategy}` is not supported")

    # print starting message
    if args.verbose:
        print(f"""
Starting run with the following parameters:
strategy: {args.strategy}
pass@k: {args.pass_at_k}
""")
    else:
        print(f"Logs will be saved in `{log_dir}`")

    # load the dataset
    print(f'Loading the dataset...')
    if args.dataset_path.endswith(".jsonl"):
        dataset = read_jsonl(args.dataset_path)
    elif args.dataset_path.endswith(".jsonl.gz"):
        dataset = read_jsonl_gz(args.dataset_path)
    else:
        raise ValueError(
            f"Dataset path `{args.dataset_path}` is not supported")

    print(f"Loaded {len(dataset)} examples")
    # start the run
    # evaluate with pass@k
    if args.strategy == "simple":
        run_simple(
            dataset=dataset,
            model=args.model,
            language=args.language,
            pass_at_k=args.pass_at_k,
            log_path=log_path,
            verbose=args.verbose
        )
    elif args.strategy == "reflexion":
        run_reflexion(
            dataset=dataset,
            model=args.model,
            language=args.language,
            max_iters=args.max_iters,
            pass_at_k=args.pass_at_k,
            log_path=log_path,
            verbose=args.verbose
        )
    elif args.strategy == "reflexion-ucs":
        run_reflexion_ucs(
            dataset=dataset,
            model=args.model,
            language=args.language,
            max_iters=args.max_iters,
            pass_at_k=args.pass_at_k,
            log_path=log_path,
            verbose=args.verbose,
            expansion_factor=args.expansion_factor
        )

    print(f"Done! Check out the logs in `{log_path}`")


if __name__ == "__main__":
    args = get_args()
    main(args)
