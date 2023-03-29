from utils import read_jsonl, write_jsonl
import sys

def generate_dataset(input_file, output_file):
    final = []
    data = read_jsonl(input_file)
    for item in data:
        name = item["name"]
        entry = "_".join(name.split("_")[2:])
        print(entry)
        item["entry_point"] = entry
        item["test"] = item["tests"]
        del item["tests"]
        final.append(item)

    _output_file = open(output_file, "w")
    _output_file.close()

    write_jsonl(output_file, final)


if __name__ == "__main__":
    assert len(sys.argv) == 3, "Usage: python generate_dataset.py input_file output_file"
    assert sys.argv[1].endswith(".jsonl"), "Input file must be a .jsonl file"
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    generate_dataset(input_file, output_file)
