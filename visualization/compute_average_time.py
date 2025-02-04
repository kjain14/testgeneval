import json
from tqdm import tqdm

if __name__ == "__main__":
    OUTPUT_JSONL = "../OpenHands/evaluation/evaluation_outputs/outputs/kjain14__testgeneval-test/CodeActAgent/gpt-4o_maxiter_25_N_v0.20.0-no-hint-run_1/output.jsonl"

    with open(OUTPUT_JSONL, "r") as f:
        data = [json.loads(line) for line in f]
    
    total_time = 0
    for datum in tqdm(data):
        total_time += datum["test_result"]["elapsed_time"]
    print(total_time / len(data))