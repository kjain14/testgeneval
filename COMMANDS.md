Pynguin:
python baselines/pynguin/run_pynguin.py --input_file baselines/ids.txt --output_base_dir baseline_data/outputs/pynguin/ 2>&1 | tee logs/pynguin.log

CodaMosa:
export AUTH_KEY=<YOUR AUTH KEY>
python baselines/codamosa/run_codamosa.py --input_file baselines/ids.txt --output_base_dir baseline_data/outputs/codamosa/