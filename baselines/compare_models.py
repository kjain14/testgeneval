import argparse
import json
import os

from tqdm import tqdm


def load_preds(preds_fp):
    """
    Load a predictions file (JSON lines) and return a dictionary keyed by instance id.
    Assumes that the predicted test suite is stored under entry['preds']['full'][0].
    """
    with open(preds_fp, "r") as f:
        lines = [json.loads(line) for line in f]
    preds_dict = {}
    for entry in lines:
        preds_dict[entry["id"]] = entry
    return preds_dict


def load_report(report_fp):
    """Load a report file (a JSON file keyed by instance id)."""
    with open(report_fp, "r") as f:
        return json.load(f)


def load_approach(approach_fp):
    """
    Load the approach file (JSON lines format) and return a dictionary keyed by instance id.
    Each entry is assumed to have its id at entry['test_result']['id'].
    """
    approach_dict = {}
    with open(approach_fp, "r") as f:
        for line in f:
            entry = json.loads(line)
            instance_id = entry["test_result"]["id"]
            approach_dict[instance_id] = entry
    return approach_dict


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # Baseline 1 inputs:
    parser.add_argument(
        "--baseline1_report",
        type=str,
        default="results/testgeneval/pynguin_full.json",
        help="Path to baseline 1 report (JSON keyed by instance id)",
    )
    parser.add_argument(
        "--baseline1_preds",
        type=str,
        default="results/testgeneval/preds/pynguin__testgeneval__0.2__test.jsonl",
        help="Path to baseline 1 predictions (JSON lines)",
    )
    # Baseline 2 inputs:
    parser.add_argument(
        "--baseline2_report",
        type=str,
        default="results/testgeneval/codamosa_full.json",
        help="Path to baseline 2 report (JSON keyed by instance id)",
    )
    parser.add_argument(
        "--baseline2_preds",
        type=str,
        default="results/testgeneval/preds/codamosa__testgeneval__0.2__test.jsonl",
        help="Path to baseline 2 predictions (JSON lines)",
    )
    parser.add_argument(
        "--baseline3_report",
        type=str,
        default="results/testgeneval/gpt-4o-2024-08-06t=0.2_full.json",
        help="Path to baseline 3 report (JSON keyed by instance id)",
    )
    parser.add_argument(
        "--baseline3_preds",
        type=str,
        default="results/testgeneval/preds/gpt-4o-2024-08-06__testgeneval__0.2__test.jsonl",
        help="Path to baseline 3 predictions (JSON lines)",
    )
    # Approach input (single file as before)
    parser.add_argument(
        "--approach_fp",
        type=str,
        default="../OpenHands/evaluation/evaluation_outputs/outputs/kjain14__testgeneval-test/CodeActAgent/gpt-4o_maxiter_25_N_v0.20.0-no-hint-run_1/output.testgeneval.jsonl",
        help="Path to approach file (JSON lines, containing test_result with report)",
    )
    # Output directory for TXT files:
    parser.add_argument(
        "--output_dir",
        type=str,
        default="baseline_data/figure_examples",
        help="Directory to write output TXT files",
    )
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    # Load data
    baseline1_report = load_report(args.baseline1_report)
    baseline2_report = load_report(args.baseline2_report)
    baseline3_report = load_report(args.baseline3_report)

    approach_data = load_approach(args.approach_fp)

    baseline1_preds = load_preds(args.baseline1_preds)
    baseline2_preds = load_preds(args.baseline2_preds)
    baseline3_preds = load_preds(args.baseline3_preds)

    # Determine instance ids present in all sources.
    common_ids = (
        set(baseline1_report.keys())
        & set(baseline1_preds.keys())
        & set(baseline2_report.keys())
        & set(baseline2_preds.keys())
        & set(baseline3_report.keys())
        & set(baseline3_preds.keys())
        & set(approach_data.keys())
    )

    for instance_id in tqdm(common_ids):
        # Baseline 1: Get predicted test suite, coverage, and mutation score.
        b1_pred_entry = baseline1_preds[instance_id]
        b1_pred_suite = b1_pred_entry.get("preds", {}).get("full", [None])[0]
        b1_report_entry = baseline1_report[instance_id]
        b1_coverage = b1_report_entry.get("full", {}).get("coverage", [-1])[0]
        b1_mutation = b1_report_entry.get("full", {}).get("mutation_score", [-1])[0]

        # Baseline 2: Get predicted test suite, coverage, and mutation score.
        b2_pred_entry = baseline2_preds[instance_id]
        b2_pred_suite = b2_pred_entry.get("preds", {}).get("full", [None])[0]
        b2_report_entry = baseline2_report[instance_id]
        b2_coverage = b2_report_entry.get("full", {}).get("coverage", [-1])[0]
        b2_mutation = b2_report_entry.get("full", {}).get("mutation_score", [-1])[0]

        b3_pred_entry = baseline3_preds[instance_id]
        b3_pred_suite = b3_pred_entry.get("preds", {}).get("full", [None])[0]
        b3_report_entry = baseline3_report[instance_id]
        b3_coverage = b3_report_entry.get("full", {}).get("coverage", [-1])[0]
        b3_mutation = b3_report_entry.get("full", {}).get("mutation_score", [-1])[0]

        # Approach: Process using the same method as before.
        a_entry = approach_data[instance_id]
        a_report = a_entry["test_result"]["report"]
        a_coverage = a_report.get("coverage", -1)
        a_mutation = a_report.get("mutation_score", -1)
        # The approach file does not include a separate predictions field, so we mark it as N/A.
        a_pred_suite = a_entry["test_result"]["test_suite"]

        # Prepare the output content.
        content = f"Instance ID: {instance_id}\n\n"
        content += "Baseline 1 (Pynguin):\n"
        content += f"Predicted Test Suite: {b1_pred_suite}\n"
        content += f"Coverage: {b1_coverage}\n"
        content += f"Mutation Score: {b1_mutation}\n\n"

        content += "Baseline 2 (CodaMosa):\n"
        content += f"Predicted Test Suite: {b2_pred_suite}\n"
        content += f"Coverage: {b2_coverage}\n"
        content += f"Mutation Score: {b2_mutation}\n\n"

        content += "Baseline 3 (GPT-4o):\n"
        content += f"Predicted Test Suite: {b3_pred_suite}\n"
        content += f"Coverage: {b3_coverage}\n"
        content += f"Mutation Score: {b3_mutation}\n\n"

        content += "Approach:\n"
        content += f"Predicted Test Suite: {a_pred_suite}\n"
        content += f"Coverage: {a_coverage}\n"
        content += f"Mutation Score: {a_mutation}\n"

        # Write the content to a TXT file for this instance.
        output_fp = os.path.join(args.output_dir, f"{instance_id}.txt")
        with open(output_fp, "w") as f:
            f.write(content)

        if (
            a_coverage - b2_coverage > 10
            and b1_coverage != -1
            and b2_coverage != -1
            and b3_coverage != -1
        ):
            print(f"Approach outperforms baseline 1 for {instance_id} (coverage)")
            input()
