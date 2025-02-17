import argparse
import json
from tqdm import tqdm

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

    pass_baseline = 0
    pass_total = 0

    for i, curr in tqdm(enumerate(curr_data)):
        coverage_total += curr['test_result']['report']['coverage']
        mutation_total += curr['test_result']['report']['mutation_score']


        instance_id = curr['test_result']['id']

        baseline = baseline_full[instance_id]
        coverage_baseline_curr = baseline['full']['coverage'][0]
        mutation_baseline_curr = baseline['full']['mutation_score'][0]

        coverage_baseline += coverage_baseline_curr if coverage_baseline_curr != -1 else 0
        mutation_baseline += mutation_baseline_curr if mutation_baseline_curr != -1 else 0

        pass_baseline += 1 if coverage_baseline_curr != -1 else 0
        pass_total += 1 if curr['test_result']['report']['tests_pass'] else 0

        # baseline_pred = ''
        # for pred in baseline_preds:
        #     if pred['id'] == instance_id:
        #         baseline_pred = pred['preds']['full'][0]
        #         break

        # print('Baseline Prediction:\n', baseline_pred)
        # print('Baseline Coverage:', coverage_baseline_curr, 'Baseline Mutation:', mutation_baseline_curr)
        # input()

    print('Coverage Total:', coverage_total/len(curr_data))
    print('Coverage Baseline:', coverage_baseline/len(curr_data))
    print('Mutation Total:', mutation_total/len(curr_data))
    print('Mutation Baseline:', mutation_baseline/len(curr_data))
    print('Pass Total:', pass_total/len(curr_data)*100)
    print('Pass Baseline:', pass_baseline/len(curr_data)*100)
