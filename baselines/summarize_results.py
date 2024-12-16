import argparse
import json
from swebench_docker.utils import get_eval_refs
from generate_report import get_preds_report

def summarize_results(report_full, preds, preds_path, instances):    
    # Print reports for different granularities of patch success/failure
    final_report = get_preds_report(preds_path, instances)

    av_coverage = []
    av_mutation_score = []
    av_pass_at_one = []

    for pred in report_full:
        datum = report_full[pred]
        if datum["full"]["unfiltered_tests_passed"][0]:
            av_coverage.append(datum["full"]["coverage"][0])
            av_mutation_score.append(datum["full"]["mutation_score"][0])
            av_pass_at_one.append(1)
        else:
            av_pass_at_one.append(0)
            av_coverage.append(0)
            av_mutation_score.append(0)
    
    final_report["av_coverage"] = sum(av_coverage) / len(av_coverage)
    final_report["av_mutation_score"] = sum(av_mutation_score) / len(av_mutation_score)
    final_report["av_pass_at_one"] = sum(av_pass_at_one) / len(av_pass_at_one)

    print(final_report)
    return final_report

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input_file", type=str, help="Path to report input file", required=True
    )
    parser.add_argument(
        "--preds_file", type=str, help="Path to predictions file", required=True
    )
    parser.add_argument(
        "--output_file", type=str, help="Path to output file", required=True
    )
    parser.add_argument(
        "--dataset", type=str, help="dataset", default="kjain14/testgeneval"
    )
    args = parser.parse_args()

    report_net = json.load(open(args.input_file))

    with open(args.preds_file) as f:
        preds = []
        for line in f:
            preds.append(json.loads(line))
    instances = get_eval_refs(args.dataset)
    summary = summarize_results(report_net, preds, args.preds_file, instances)
    
    
    with open(args.output_file, "w") as f:
        f.write(json.dumps(summary, indent=4))