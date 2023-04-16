from utils import write_jsonl, read_jsonl


def main(input_file, output_file):
    # read in the data
    data = read_jsonl(input_file)

    def get_humaneval_number(name):
        # e.g. 'HumanEval_26_remove_duplicates' -> 26
        return int(name.split('_')[1])

    sorted_data = sorted(
        data, key=lambda x: get_humaneval_number(x['name']), reverse=False)

    write_jsonl(output_file, sorted_data)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', type=str)
    parser.add_argument('output_file', type=str)

    args = parser.parse_args()

    main(args.input_file, args.output_file)
