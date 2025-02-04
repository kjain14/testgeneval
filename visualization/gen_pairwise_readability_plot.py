from compute_readability import compute_readability
import json
import matplotlib.pyplot as plt
import numpy as np


def plot_data(data):

    models = [entry['model'] for entry in data]
    agent_scores = [entry['readability_scores_agent'] for entry in data]
    pred_scores = [entry['readability_scores_pred'] for entry in data]

    # Bar width and positions
    bar_width = 0.4
    x = np.arange(len(models))

    # Plot
    plt.figure(figsize=(8, 5))
    plt.bar(x - bar_width/2, agent_scores, width=bar_width, label='Agent Scores', color='blue', alpha=0.7)
    plt.bar(x + bar_width/2, pred_scores, width=bar_width, label='Baseline Scores', color='orange', alpha=0.7)

    # Labels and Title
    plt.xlabel("")
    plt.ylabel("Readability Score")
    plt.title("Pairwise Readability Scores Comparison")
    plt.xticks(ticks=x, labels=models)
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.6)

    # Show Plot
    plt.savefig("plots/pairwise_readability_scores.png")


if __name__ == "__main__":
    PREDS_PATHS = {
        "GPT-4o (0-shot)": "results/testgeneval/preds/gpt-4o-2024-08-06__testgeneval__0.2__test.jsonl",
        "CodaMosa": "results/testgeneval/preds/codamosa__testgeneval__0.2__test.jsonl",
        "Pynguin": "results/testgeneval/preds/pynguin__testgeneval__0.2__test.jsonl",
    }

    REPORT_PATHS = {
        "GPT-4o (0-shot)": "results/testgeneval/gpt-4o-2024-08-06t=0.2_full.json",
        "CodaMosa": "results/testgeneval/codamosa_full.json",
        "Pynguin": "results/testgeneval/pynguin_full.json",
    }

    preds = {}
    for k, v in PREDS_PATHS.items():
        print(v)
        with open(v, "r") as f:
            curr_mapping = {}
            for line in f:
                line_json = json.loads(line)
                curr_mapping[line_json["id"]] = line_json
            preds[k] = curr_mapping

    reports = {}
    for k, v in REPORT_PATHS.items():
        print(k,v)
        with open(v, "r") as f:
            reports[k] = json.load(f)

    AGENT_FP = "../OpenHands/evaluation/evaluation_outputs/outputs/kjain14__testgeneval-test/CodeActAgent/gpt-4o_maxiter_25_N_v0.20.0-no-hint-run_1/output.testgeneval.jsonl"

    with open(AGENT_FP, "r") as f:
        agent_data = {}
        for line in f:
            line_json = json.loads(line)
            agent_data[line_json["instance_id"]] = line_json
    
    pairwise_data = []

    for k, report in reports.items():
        subset_report = []
        for id, datum in report.items():
            if datum['full']['tests_passed'][0]:
                subset_report.append(id)
        
        final_subset = []
        readability_scores_agent = []
        readability_scores_pred = []
        for id in agent_data:
            if id in subset_report and agent_data[id]['test_result']['report']['tests_pass']:
                final_subset.append(id)
                readability_scores_agent.append(compute_readability(agent_data[id]['test_result']['test_suite']))
                readability_scores_pred.append(compute_readability(preds[k][id]['preds']['full'][0]))
        
        
        pairwise_data.append({
            "model": k,
            "readability_scores_agent": np.median(readability_scores_agent),
            "readability_scores_pred": np.median(readability_scores_pred),
        })

    plot_data(pairwise_data)