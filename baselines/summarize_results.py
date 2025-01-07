import argparse
import json
from swebench_docker.utils import get_eval_refs
from generate_report import get_preds_report

def summarize_results(report_full, preds, preds_path, instances, ids_file):
    """
    Summarize results, reporting both:
      1) totals over all IDs in report_full,
      2) totals over a subset specified by ids_file,
      3) a second preds report for just that subset.
    """
    # 1) Build the final (total) report from predictions on ALL instances
    final_report = get_preds_report(preds_path, instances)

    # Read subset IDs from file (if provided). 
    # If no file or empty file, subset_ids = empty set => no subset reporting
    subset_ids = set()
    if ids_file:
        with open(ids_file, "r") as f:
            subset_ids = {line.strip() for line in f if line.strip()}

    # 2) Build a separate preds report for only the subset of IDs
    #    - filter the instances so we only keep those whose "id" is in subset_ids
    subset_instances = [inst for inst in instances if inst.get("id") in subset_ids]
    subset_report = get_preds_report(preds_path, subset_instances)

    # --- Calculate metrics over ALL IDs (Total) ---
    total_cov = []
    total_mut = []
    total_pass = []

    for pred_id, datum in report_full.items():
        # coverage/mutation_score are always counted
        total_cov.append(datum["full"]["coverage"][0])
        total_mut.append(datum["full"]["mutation_score"][0])
        # pass@1 is 1 if unfiltered_tests_passed is True, else 0
        total_pass.append(1 if datum["full"]["unfiltered_tests_passed"][0] else 0)

    # Avoid division by zero if empty
    final_report["total_av_coverage"] = (
        sum(total_cov) / len(total_cov) if total_cov else 0
    )
    final_report["total_av_mutation_score"] = (
        sum(total_mut) / len(total_mut) if total_mut else 0
    )
    final_report["total_av_pass_at_one"] = (
        sum(total_pass) / len(total_pass) if total_pass else 0
    )

    # --- Calculate metrics over the SUBSET of IDs from ids_file ---
    subset_cov = []
    subset_mut = []
    subset_pass = []

    for pred_id, datum in report_full.items():
        if pred_id in subset_ids:
            subset_cov.append(datum["full"]["coverage"][0])
            subset_mut.append(datum["full"]["mutation_score"][0])
            subset_pass.append(1 if datum["full"]["unfiltered_tests_passed"][0] else 0)

    # Store subset metrics in the subset_report object
    if subset_cov:
        subset_report["av_coverage"] = sum(subset_cov) / len(subset_cov)
    else:
        subset_report["av_coverage"] = 0

    if subset_mut:
        subset_report["av_mutation_score"] = sum(subset_mut) / len(subset_mut)
    else:
        subset_report["av_mutation_score"] = 0

    if subset_pass:
        subset_report["av_pass_at_one"] = sum(subset_pass) / len(subset_pass)
    else:
        subset_report["av_pass_at_one"] = 0

    # Finally, put the subset report inside the final_report so we return everything together
    final_report["subset_report"] = subset_report

    # Print the combined final report
    print(json.dumps(final_report, indent=4))
    return final_report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Summarize results for total and subset of IDs.")
    parser.add_argument(
        "--input_file", 
        type=str, 
        help="Path to report input file", 
        required=True
    )
    parser.add_argument(
        "--preds_file", 
        type=str, 
        help="Path to predictions file", 
        required=True
    )
    parser.add_argument(
        "--output_file", 
        type=str, 
        help="Path to output file", 
        required=True
    )
    parser.add_argument(
        "--dataset", 
        type=str, 
        help="dataset", 
        default="kjain14/testgeneval"
    )
    parser.add_argument(
        "--ids_file", 
        type=str, 
        help="Path to a text file containing a subset of IDs (one per line)",
        required=False
    )

    args = parser.parse_args()

    # Load the "net" report
    with open(args.input_file, "r") as f:
        report_net = json.load(f)

    # Load predictions
    preds = []
    with open(args.preds_file, "r") as f:
        for line in f:
            preds.append(json.loads(line))

    # Retrieve references (instances)
    instances = get_eval_refs(args.dataset)

    # Summarize results for both total and subset
    summary = summarize_results(
        report_full=report_net,
        preds=preds,
        preds_path=args.preds_file,
        instances=instances,
        ids_file=args.ids_file
    )
    
    # Write summary to output file
    with open(args.output_file, "w") as f:
        f.write(json.dumps(summary, indent=4))