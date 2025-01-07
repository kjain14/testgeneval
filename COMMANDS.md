Pynguin:
python baselines/pynguin/run_pynguin.py --input_file baselines/ids.txt --output_base_dir baseline_data/outputs/pynguin/ 2>&1 | tee logs/pynguin.log

CodaMosa:
export AUTH_KEY=<YOUR AUTH KEY>
python baselines/codamosa/run_codamosa.py --input_file baselines/ids.txt --output_base_dir baseline_data/outputs/codamosa/

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