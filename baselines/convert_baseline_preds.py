#!/usr/bin/env python3

import argparse
import os
import re
import json

def parse_args():
    parser = argparse.ArgumentParser(
        description="Create a predictions.jsonl file for each subdirectory of a given root."
    )
    parser.add_argument(
        "--root_dir", 
        required=True,
        help="Path to the root directory containing subdirectories (e.g., pydata__xarray-3114-16452)."
    )
    parser.add_argument(
        "--model_name",
        required=True, 
        help="Name of the model to include in the output JSON."
    )
    parser.add_argument(
        "--output", 
        required=True, 
        help="Path to the output JSONL file (default: predictions.jsonl)."
    )
    return parser.parse_args()

def main():
    args = parse_args()
    root_dir = args.root_dir
    model_name = args.model_name
    out_file = args.output

    # Compile a regex to match subdirectories that end with '-<digits>'
    # We'll use this to strip away the trailing '-number' from the directory name
    trailing_pattern = re.compile(r'^(.*)-\d+$')

    # This will store each JSON object for writing
    json_lines = []

    # Iterate through everything in the root directory
    for entry_name in os.listdir(root_dir):
        full_path = os.path.join(root_dir, entry_name)
        
        if os.path.isdir(full_path):
            # Attempt to find a Python test file
            test_file_path = None
            test_short_path = None
            for fname in os.listdir(full_path):
                if fname.startswith("test_") and fname.endswith(".py"):
                    test_file_path = os.path.join(full_path, fname)
                    test_short_path = fname
                    break

            # Skip if we didn't find a test file
            if not test_file_path:
                continue

            # Read the contents of that test file
            with open(test_file_path, "r") as f:
                file_contents = f.read()

            # Strip the trailing '-<digits>' from the directory name
            match = trailing_pattern.match(entry_name)
            if match:
                instance_id = match.group(1)
            else:
                # Fallback if the directory doesn't match the pattern
                instance_id = entry_name

            # Prepare the JSON object
            obj = {
                "instance_id": instance_id,
                "id": entry_name,
                "preds": {
                    "full": [file_contents]
                },
                "model_name_or_path": model_name,
                "test_file": test_short_path
            }

            # Add to our lines list
            json_lines.append(obj)

    # Write each JSON object on its own line to the output file
    with open(out_file, "w", encoding="utf-8") as f:
        for line_data in json_lines:
            f.write(json.dumps(line_data))
            f.write("\n")

    print(f"Predictions written to: {out_file}")

if __name__ == "__main__":
    main()
