import argparse
import json

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseline_full_fp', type=str, required=True)
    parser.add_argument('--baseline_preds', type=str, required=True)

    parser.add_argument('--approach_fp', type=str, required=True)

    args = parser.parse_args()

    # Load the data
    with open(args.baseline_full_fp, 'r') as f:
        baseline_full = json.load(f)

    with open(args.baseline_preds, 'r') as f:
        baseline_preds = [json.loads(line) for line in f]

    with open(args.approach_fp, 'r') as f:
        curr_data = [json.loads(line) for line in f]
    

    coverage_total = 0
    mutation_total = 0

    coverage_baseline = 0
    mutation_baseline = 0

    for i, curr in enumerate(curr_data):
        print(curr['test_result'].keys())
        coverage_total += curr['test_result']['report']['coverage']
        # mutation_total += curr['mutation_score']

        print('Agent Prediction:\n', curr['test_result']['test_suite'])
        print('Coverage:', curr['test_result']['report']['coverage'])#, 'Mutation:', curr['test_result']['report']['coverage'])
        input()

        instance_id = curr['test_result']['id']

        baseline = baseline_full[instance_id]
        coverage_baseline_curr = baseline['full']['coverage'][0]
        mutation_baseline_curr = baseline['full']['mutation_score'][0]

        coverage_baseline += coverage_baseline_curr if coverage_baseline != -1 else 0
        mutation_baseline += mutation_baseline_curr if mutation_baseline != -1 else 0
        
        baseline_pred = ''
        for pred in baseline_preds:
            if pred['id'] == instance_id:
                baseline_pred = pred['preds']['full'][0]
                break

        print('Baseline Prediction:\n', baseline_pred)
        print('Baseline Coverage:', coverage_baseline_curr, 'Baseline Mutation:', mutation_baseline_curr)
        input()
