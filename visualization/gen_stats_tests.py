import scipy.stats as stats
import json

def report_to_list(d, key="coverage"):
    return [d[entry]["full"][key][0] for entry in d]

def data_to_list(d, key="coverage"):
    return [entry["test_result"]["report"][key] for entry in d]

if __name__ == "__main__":
    FILES = {
        "codamosa": "results/testgeneval/codamosa_full.json",
        "pynguin": "results/testgeneval/pynguin_full.json",
        "gpt": "results/testgeneval/gpt-4o-2024-08-06t=0.2_full.json",
        "agentic": "../OpenHands/evaluation/evaluation_outputs/outputs/kjain14__testgeneval-test/CodeActAgent/gpt-4o_maxiter_25_N_v0.20.0-no-hint-run_1/output.testgeneval.jsonl",
    }

    MAPPING = {}

    for key, file in FILES.items():
        if file.endswith(".json"):
            with open(file, "r") as f:
                data = json.load(f)
                if key == "gpt":
                    with open("baselines/ids.txt", "r") as f:
                        ids = [line.strip() for line in f]
                    data_subset = {entry: data[entry] for entry in data if entry in ids}
                    MAPPING[key + "_subset"] = report_to_list(data_subset)
                MAPPING[key] = report_to_list(data)
        if key == "agentic":
            with open(file, "r") as f:
                data = [json.loads(line) for line in f]
            with open("baselines/ids.txt", "r") as f:
                ids = [line.strip() for line in f]
            data_subset = [entry for entry in data if entry["test_result"]["id"] in ids]
            MAPPING[key + "_subset"] = data_to_list(data_subset)
            MAPPING[key] = data_to_list(data)


    # **Large sample size (Welch's t-test, assuming independence)**
    t_stat_1, p_value_t1 = stats.ttest_ind(MAPPING["agentic"], MAPPING["gpt"], equal_var=False)
    
    FINAL_STATS = {}

    FINAL_STATS["agentic_full_gpt"] = {
        "t_stat": t_stat_1,
        "p_value": p_value_t1,
    }


    t_stat_2, p_value_t2 = stats.ttest_ind(MAPPING["agentic_subset"], MAPPING["gpt_subset"], equal_var=False)

    FINAL_STATS["agentic_subset_gpt"] = {
        "t_stat": t_stat_2,
        "p_value": p_value_t2,
    }

    t_stat_3, p_value_t3 = stats.ttest_ind(MAPPING["agentic_subset"], MAPPING["pynguin"], equal_var=False)
    t_stat_4, p_value_t4 = stats.ttest_ind(MAPPING["agentic_subset"], MAPPING["codamosa"], equal_var=False)

    FINAL_STATS["agentic_subset_pynguin"] = {
        "t_stat": t_stat_3,
        "p_value": p_value_t3,
    }

    FINAL_STATS["agentic_subset_codamosa"] = {
        "t_stat": t_stat_4,
        "p_value": p_value_t4,
    }

    with open("tables/stats.json", "w") as f:
        json.dump(FINAL_STATS, f)