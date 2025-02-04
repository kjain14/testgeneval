import json
from collections import defaultdict


def gen_runtime(dicts, dict_names, caption, label, totals):
    for dict in dicts:
        for key, value in dict.items():
            if value == -1:
                dict[key] = 0.0

    # Generate Pynguin table
    CURR_TABLE = """\\begin{table}[h!]
\\centering
\\begin{tabular}{@{}lrrr@{}}
\\toprule
\\textbf{Model}           & \\textbf{Pass@1} & \\textbf{Coverage} & \\textbf{Mutation Score} \\\\ \\midrule
"""
    for i, dict in enumerate(dicts):
        print(dict)
        if totals[i]:
            CURR_TABLE += f"\\textbf{{{dict_names[i]}}} & {dict['total_av_pass_at_one'] * 100:.1f}\\% & {dict['total_av_coverage']:.1f}\\% & {dict['total_av_mutation_score']:.1f}\\% \\\\ \n"
        else:
            CURR_TABLE += f"\\textbf{{{dict_names[i]}}} & {dict['av_pass_at_one'] * 100:.1f}\\% & {dict['av_coverage']:.1f}\\% & {dict['av_mutation_score']:.1f}\\% \\\\ \n"
    CURR_TABLE += """\\bottomrule
\\end{tabular}
\\caption{""" + caption + """}
\\label{""" + label + """}
\\end{table}"""

    return CURR_TABLE



def gen_lexical(dicts, dict_names, caption, label):
    for dict in dicts:
        for key, value in dict.items():
            if value == -1:
                dict[key] = 0.0

    # Generate Pynguin table
    CURR_TABLE = """\\begin{table*}[ht]
\\centering
\\begin{tabular}{lrrrrrrrr}
\\toprule
\\textbf{Model} & \\textbf{BLEU} & \\textbf{CodeBLEU} & \\textbf{Readability} & \\textbf{XMatch} & \\textbf{ROUGE-P} & \\textbf{ROUGE-R} & \\textbf{ROUGE-F} & \\textbf{Edit Sim} \\\\
\\midrule
"""
    for i, dict in enumerate(dicts):
        CURR_TABLE += f"\\textbf{{{dict_names[i]}}} & {dict['av_bleu']:.1f} & {dict['av_codebleu']:.1f} & {dict['av_readability']:.1f} & {dict['av_xmatch']:.1f} & {dict['av_rouge_p']:.1f} & {dict['av_rouge_r']:.1f} & {dict['av_rouge_f']:.1f} & {dict['av_edit_sim']:.1f} \\\\ \n"
    CURR_TABLE += """\\bottomrule
\\end{tabular}
\\caption{""" + caption + """}
\\label{""" + label + """}
\\end{table*}"""

    return CURR_TABLE



def average_subset(new_mapping):
    averages = defaultdict(list)

    for d in new_mapping:
        for key, value in d.items():
            averages[key].append(value)

    # Convert lists to mean values
    result = {key: sum(values) / len(values) for key, values in averages.items()}
    return result


def build_agentic_averages(agentic_list):
    new_mapping = {"pynguin": [], "codamosa": [], "subset": [], "all": []}
    with open("baselines/pynguin_ids.txt", "r") as f:
        pynguin_ids = [e.strip() for e in f.readlines()]
    
    with open("baselines/codamosa_ids.txt", "r") as f:
        codamosa_ids = [e.strip() for e in f.readlines()]
    
    with open("baselines/ids.txt", "r") as f:
        ids = [e.strip() for e in f.readlines()]
    
    for entry in agentic_list:
        curr_data = {
            "av_pass_at_one": entry["test_result"]["report"]["tests_pass"],
            "av_all_pass_at_one": entry["test_result"]["report"]["all_tests_pass"],
            "av_coverage": entry["test_result"]["report"]["coverage"],
            "av_mutation_score": entry["test_result"]["report"]["mutation_score"],
            "av_codebleu": entry["test_result"]["lexical"]["code_bleu"],
            "av_loc": entry["test_result"]["lexical"]["pred_loc"],
            "av_num_methods": entry["test_result"]["lexical"]["pred_methods"],
            "av_bleu": entry["test_result"]["lexical"]["bleu"],
            "av_rouge_f": entry["test_result"]["lexical"]["rouge_f"],
            "av_rouge_p": entry["test_result"]["lexical"]["rouge_p"],
            "av_rouge_r": entry["test_result"]["lexical"]["rouge_r"],
            "av_xmatch": entry["test_result"]["lexical"]["xmatch"],
            "av_readability": entry["test_result"]["lexical"]["pred_readability"],
            "av_edit_sim": entry["test_result"]["lexical"]["edit_sim"],
        }

        if entry["test_result"]["id"] in pynguin_ids:
            new_mapping["pynguin"].append(curr_data)
        if entry["test_result"]["id"] in codamosa_ids:
            new_mapping["codamosa"].append(curr_data)
        if entry["test_result"]["id"] in ids:
            new_mapping["subset"].append(curr_data)
        new_mapping["all"].append(curr_data)
    
    result = {"pynguin": average_subset(new_mapping["pynguin"]), "codamosa": average_subset(new_mapping["codamosa"]), "subset": average_subset(new_mapping["subset"]), "all": average_subset(new_mapping["all"])}

    return result


def build_runtime_tables(mapping):
    OUTPUT_DIR = "tables"

    runtime_all_file = f"{OUTPUT_DIR}/runtime_all.tex"
    runtime_subset_file = f"{OUTPUT_DIR}/runtime_subset.tex"
    runtime_codamosa_file = f"{OUTPUT_DIR}/runtime_codamosa.tex"
    runtime_pynguin_file = f"{OUTPUT_DIR}/runtime_pynguin.tex"

    with open(runtime_all_file, "w") as f:
        all_table = gen_runtime(
            [mapping["catlm_subset"], mapping["gpt_subset"], mapping["agentic"]["all"]],
            ["CAT-LM", "GPT-4o (0-shot)", "\\toolname"],
            "Full TestGenEval results.",
            "tab:baseline_comparison_full",
            [True, True, False],
        )
        f.write(all_table)
    
    with open(runtime_subset_file, "w") as f:
        subset_table = gen_runtime(
            [mapping["catlm_subset"]["subset_report"], mapping["gpt_subset"]["subset_report"], mapping["pynguin"], mapping["codamosa"], mapping["agentic"]["subset"]],
            ["CAT-LM", "GPT-4o (0-shot)", "Pynguin", "CodaMosa", "\\toolname"],
            "Subset TestGenEval results.",
            "tab:baseline_comparison_subset",
            [False, False, True, True, False],
        )
        f.write(subset_table)
    
    with open(runtime_codamosa_file, "w") as f:
        codamosa_table = gen_runtime(
            [mapping["catlm_codamosa"]["subset_report"], mapping["gpt_codamosa"]["subset_report"], mapping["codamosa"]["subset_report"], mapping["agentic"]["codamosa"]],
            ["CAT-LM", "GPT-4o (0-shot)", "CodaMosa", "\\toolname"],
            "CodaMosa TestGenEval results.",
            "tab:baseline_comparison_codamosa",
            [False, False, False, False],
        )
        f.write(codamosa_table)

    with open(runtime_pynguin_file, "w") as f:
        pynguin_table = gen_runtime(
            [mapping["catlm_pynguin"]["subset_report"], mapping["gpt_pynguin"]["subset_report"], mapping["pynguin"]["subset_report"], mapping["agentic"]["pynguin"]],
            ["CAT-LM", "GPT-4o (0-shot)", "Pynguin", "\\toolname"],
            "Pynguin TestGenEval results.",
            "tab:baseline_comparison_pynguin",
            [False, False, False, False],
        )
        f.write(pynguin_table)


def build_lexical_tables(mapping):
    OUTPUT_DIR = "tables"

    lexical_all_file = f"{OUTPUT_DIR}/lexical_all.tex"
    lexical_subset_file = f"{OUTPUT_DIR}/lexical_subset.tex"
    lexical_codamosa_file = f"{OUTPUT_DIR}/lexical_codamosa.tex"
    lexical_pynguin_file = f"{OUTPUT_DIR}/lexical_pynguin.tex"

    with open(lexical_all_file, "w") as f:
        all_table = gen_lexical(
            [mapping["catlm_subset"], mapping["gpt_subset"], mapping["agentic"]["all"]],
            ["CAT-LM", "GPT-4o (0-shot)", "\\toolname"],
            "Full TestGenEval lexical results.",
            "tab:lexical_baseline_comparison_full",
        )
        f.write(all_table)
    
    with open(lexical_subset_file, "w") as f:
        subset_table = gen_lexical(
            [mapping["catlm_subset"]["subset_report"], mapping["gpt_subset"]["subset_report"], mapping["pynguin"], mapping["codamosa"], mapping["agentic"]["subset"]],
            ["CAT-LM", "GPT-4o (0-shot)", "Pynguin", "CodaMosa", "\\toolname"],
            "Subset TestGenEval lexical results.",
            "tab:lexical_baseline_comparison_subset",
        )
        f.write(subset_table)
    
    with open(lexical_codamosa_file, "w") as f:
        codamosa_table = gen_lexical(
            [mapping["catlm_codamosa"]["subset_report"], mapping["gpt_codamosa"]["subset_report"], mapping["codamosa"]["subset_report"], mapping["agentic"]["codamosa"]],
            ["CAT-LM", "GPT-4o (0-shot)", "CodaMosa", "\\toolname"],
            "CodaMosa TestGenEval lexical results.",
            "tab:lexical_baseline_comparison_codamosa",
        )
        f.write(codamosa_table)

    with open(lexical_pynguin_file, "w") as f:
        pynguin_table = gen_lexical(
            [mapping["catlm_pynguin"]["subset_report"], mapping["gpt_pynguin"]["subset_report"], mapping["pynguin"]["subset_report"], mapping["agentic"]["pynguin"]],
            ["CAT-LM", "GPT-4o (0-shot)", "Pynguin", "\\toolname"],
            "Pynguin TestGenEval lexical results.",
            "tab:lexical_baseline_comparison_pynguin",
        )
        f.write(pynguin_table)


if __name__ == "__main__":
    FILES = {
        "gpt_pynguin": "baseline_data/gpt_4o_summary_pynguin.json",
        "gpt_codamosa": "baseline_data/gpt_4o_summary_codamosa.json",
        "gpt_subset": "baseline_data/gpt_4o_summary.json",
        "catlm_pynguin": "baseline_data/catlm_summary_pynguin.json",
        "catlm_codamosa": "baseline_data/catlm_summary_codamosa.json",
        "catlm_subset": "baseline_data/catlm_summary.json",
        "codamosa": "baseline_data/codamosa_filtered.json",
        "pynguin": "baseline_data/pynguin_filtered.json",
        "agentic": "../OpenHands/evaluation/evaluation_outputs/outputs/kjain14__testgeneval-test/CodeActAgent/gpt-4o_maxiter_25_N_v0.20.0-no-hint-run_1/output.testgeneval.jsonl",
    }


    MAPPING = {}

    for key, file in FILES.items():
        if file.endswith(".json"):
            with open(file, "r") as f:
                data = json.load(f)
                MAPPING[key] = data
        if key == "agentic":
            with open(file, "r") as f:
                data = [json.loads(line) for line in f]
            MAPPING[key] = build_agentic_averages(data)
    

    build_runtime_tables(MAPPING)
    build_lexical_tables(MAPPING)