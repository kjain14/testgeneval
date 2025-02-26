import json
from tqdm import tqdm

if __name__ == "__main__":
    OUTPUT_JSONL = "../OpenHands/evaluation/evaluation_outputs/outputs/kjain14__testgeneval-test/CodeActAgent/gpt-4o_maxiter_25_N_v0.20.0-no-hint-run_1/output_approach.jsonl"

    with open(OUTPUT_JSONL, "r") as f:
        data = [json.loads(line) for line in f]
    
    total_time = 0
    costs = []
    for datum in tqdm(data):
        total_time += datum["test_result"]["elapsed_time"]
        costs_unformatted = datum["metrics"]["costs"]
        costs += [cost["cost"] for cost in costs_unformatted]

    print(sum(costs) / len(costs))
    print(sum(costs) / len(data))
    print(total_time / len(data))