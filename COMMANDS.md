Pynguin:
python baselines/pynguin/run_pynguin.py --input_file baselines/ids.txt --output_base_dir baseline_data/outputs/pynguin/ 2>&1 | tee logs/pynguin.log

CodaMosa:
export AUTH_KEY=<YOUR AUTH KEY>
python baselines/codamosa/run_codamosa.py --input_file baselines/ids.txt --output_base_dir baseline_data/outputs/codamosa/ 2>&1 | tee logs/codamosa.log

CAT-LM:
python run_pipeline.py --results_dir results --dataset_name_or_path kjain14/testgeneval --model nikitharao/catlm --namespace kdjain

Convert Baseline Preds (Pynguin):
python baselines/convert_baseline_preds.py --root_dir baseline_data/outputs/pynguin --model pynguin --output results/testgeneval/preds/pynguin__testgeneval__0.2__test.jsonl

Convert Baseline Preds (CodaMosa):
python baselines/convert_baseline_preds.py --root_dir baseline_data/outputs/codamosa --model codamosa --output results/testgeneval/codamosa__testgeneval__0.2__test.jsonl

Run Baseline Preds (Pynguin):
python run_pipeline.py \
--results_dir results \
--dataset_name_or_path kjain14/testgeneval \
--model pynguin \
--namespace kdjain

Run Baseline Preds (CodaMosa):
python run_pipeline.py \
--results_dir results \
--dataset_name_or_path kjain14/testgeneval \
--model codamosa \
--namespace kdjain

Summarize GPT-4o results:
python baselines/summarize_results.py --input_file /data/kdjain/results/unittest_swebench/gpt-4o-2024-05-13t\=0.2_full.json --preds_file /data/kdjain/results/unittest_swebench/preds/gpt-4o-2024-05-13__unittest_swebench__0.2__test.jsonl --output_file baseline_data/gpt_4o_summary.json --ids_file baselines/ids.txt

Summarize CAT-LM results:
python baselines/summarize_results.py --input_file results/testgeneval/catlmt\=0.2_full.json --preds_file results/testgeneval/preds/catlm__testgeneval__0.2__test.jsonl --output_file baseline_data/catlm_summary.json --ids_file baselines/ids.txt

OpenHands Test Example:
