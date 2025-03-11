import argparse
import json
import os
import re
from collections import Counter

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from datasets import load_dataset


def analyze_unit_test_dataset(lens, plot_dir):
    os.makedirs(plot_dir, exist_ok=True)



    sns.set_style("whitegrid")  # Clean grid style
    sns.set_context("paper", font_scale=1.75)  
    sns.histplot(lens["testgeneval"][0], bins=30, alpha=0.5,     
    color="#87CEFA",  # Light blue color (LightSkyBlue)
    edgecolor="white",  # White edge for better definition
    linewidth=1,
    label="TestGenEval")
    plt.title("Code length distribution")
    plt.xlabel("Lines of code")
    plt.ylabel("Frequency")
    plt.legend()
    plot_path = os.path.join(plot_dir, "code_length_distribution.eps")
    plt.tight_layout()
    plt.savefig(plot_path)
    plt.close()

    sns.histplot(lens["testgeneval"][1], bins=30, alpha=0.5,     
    color="#87CEFA",  # Light blue color (LightSkyBlue)
    edgecolor="white",  # White edge for better definition
    linewidth=1,
    label="TestGenEval")
    plt.title("Test length distribution")
    plt.xlabel("Lines of code")
    plt.ylabel("Frequency")
    plt.legend()
    plot_path = os.path.join(plot_dir, "test_length_distribution.eps")
    plt.tight_layout()
    plt.savefig(plot_path)
    plt.close()



def main():
    parser = argparse.ArgumentParser(
        description="Analyze unit test dataset and coverage"
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        required=True,
        help="Directory to save plots and statistics",
    )
    args = parser.parse_args()

    testgeneval = load_dataset("kjain14/testgeneval")
    lens = {"testgeneval": [], "humanevalfix": []}
    lens["testgeneval"].append([len(code.split("\n")) for code in testgeneval["test"]["code_src"]])
    lens["testgeneval"].append([len(test.split("\n")) for test in testgeneval["test"]["test_src"]])

    humanevalfix = load_dataset("bigcode/humanevalpack", "python")["test"]
    lens["humanevalfix"].append([len(code.split("\n")) for code in humanevalfix["prompt"]])
    lens["humanevalfix"].append([len(test.split("\n")) for test in humanevalfix["test"]])

    with open("visualization/leetcode-py.jsonl", "r") as f:
        testeval = [json.loads(line) for line in f]
    lens["testeval"].append([len(test["python_solution"].split("\n")) for test in testeval])
    analyze_unit_test_dataset(lens, args.output_dir)


if __name__ == "__main__":
    main()
