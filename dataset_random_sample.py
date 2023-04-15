from utils import read_jsonl, read_jsonl_gz, write_jsonl


def main(args):
    if args.input.endswith(".gz"):
        data = read_jsonl_gz(args.input)
    else:
        data = read_jsonl(args.input)

    # sample the data
    assert args.num_samples <= len(data) and args.num_samples > 0
    sampled_data = random.sample(data, args.num_samples)

    # write the sampled data to the output file
    write_jsonl(args.output, sampled_data, append=True)


if __name__ == "__main__":
    import argparse
    import random
    import os
    # take in the input and output file names, with number of samples
    random.seed(os.urandom(1024))
    parser = argparse.ArgumentParser()

    parser.add_argument("--input", type=str, required=True)
    parser.add_argument("--output", type=str, required=True)
    parser.add_argument("--num_samples", type=int, required=True)
    args = parser.parse_args()

    main(args)
