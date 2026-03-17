import argparse
import json
import os
import random
from datasets import load_dataset


def prepend_prompt(row, prompt):
    messages = list(row["messages"])
    for i, msg in enumerate(messages):
        if msg["role"] == "user":
            messages[i] = {**msg, "content": prompt + " " + msg["content"]}
            break
    return {**row, "messages": messages}


def load_rows(dataset_name, prompt, count):
    ds = load_dataset(dataset_name, split="train")
    rows = [prepend_prompt(row, prompt) for row in ds]
    random.shuffle(rows)
    return rows[:count]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-set-1", required=True)
    parser.add_argument("--prompt-1", required=True)
    parser.add_argument("--data-set-2", required=True)
    parser.add_argument("--prompt-2", required=True)
    parser.add_argument("--count", type=int, required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    half = args.count // 2
    rows1 = load_rows(args.data_set_1, args.prompt_1, half)
    rows2 = load_rows(args.data_set_2, args.prompt_2, args.count - half)

    all_rows = rows1 + rows2
    random.shuffle(all_rows)

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, "w") as f:
        for row in all_rows:
            f.write(json.dumps(row) + "\n")

    print(f"Wrote {len(all_rows)} rows to {args.output}")


if __name__ == "__main__":
    main()
