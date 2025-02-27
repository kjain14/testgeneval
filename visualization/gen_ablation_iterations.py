import json

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit


# Define the exponential growth function
def exp_growth(x, A, B, C):
    return A * (1 - np.exp(-B * x)) + C


def gen_ablation_iterations(x, y, title):
    # Initial guess: A controls the maximum increase, B controls growth speed, C is the starting point
    initial_guess = [max(y) - min(y), 0.1, min(y)]
    bounds = ([0, 0, 0], [np.inf, np.inf, np.inf])  # Ensure parameters remain positive

    # Perform curve fitting
    popt, _ = curve_fit(exp_growth, x, y, p0=initial_guess, bounds=bounds)
    A, B, C = popt

    # Generate smooth curve for plotting
    x_fit = np.linspace(x[0], x[-1], 200)
    y_fit = exp_growth(x_fit, *popt)

    # Plot data points and best-fit curve
    plt.figure(figsize=(8, 5))
    plt.scatter(x, y, color="blue", label="Data points")
    plt.plot(x_fit, y_fit, "r-", label="Best fit curve")
    plt.xlabel("# Iterations")
    plt.ylabel(title.capitalize())
    plt.title(f"{title.capitalize()} vs # Iterations")
    plt.legend()
    plt.savefig(f"{title}_iterations.png")


if __name__ == "__main__":
    FILES = {
        1: "../OpenHands/evaluation/evaluation_outputs/outputs/kjain14__testgeneval-test/CodeActAgent/gpt-4o_maxiter_25_N_v0.20.0-no-hint-run_1/output_1.testgeneval.jsonl",
        5: "../OpenHands/evaluation/evaluation_outputs/outputs/kjain14__testgeneval-test/CodeActAgent/gpt-4o_maxiter_25_N_v0.20.0-no-hint-run_1/output_5.testgeneval.jsonl",
        10: "../OpenHands/evaluation/evaluation_outputs/outputs/kjain14__testgeneval-test/CodeActAgent/gpt-4o_maxiter_25_N_v0.20.0-no-hint-run_1/output_10.testgeneval.jsonl",
        15: "../OpenHands/evaluation/evaluation_outputs/outputs/kjain14__testgeneval-test/CodeActAgent/gpt-4o_maxiter_25_N_v0.20.0-no-hint-run_1/output_15.testgeneval.jsonl",
        20: "../OpenHands/evaluation/evaluation_outputs/outputs/kjain14__testgeneval-test/CodeActAgent/gpt-4o_maxiter_25_N_v0.20.0-no-hint-run_1/output_20.testgeneval.jsonl",
        25: "../OpenHands/evaluation/evaluation_outputs/outputs/kjain14__testgeneval-test/CodeActAgent/gpt-4o_maxiter_25_N_v0.20.0-no-hint-run_1/output.testgeneval.jsonl",
    }

    MAPPING = {0: {"cov": 34.8, "pass": 64.0}}

    for key, value in FILES.items():
        with open(value, "r") as f:
            data = [json.loads(line) for line in f]

        cov = 0
        tests_pass = 0
        for datum in data:
            cov += datum["test_result"]["report"]["coverage"]
            tests_pass += datum["test_result"]["report"]["tests_pass"]

        MAPPING[key] = {"cov": cov / len(data), "pass": (tests_pass / len(data)) * 100}

    x = [i for i in [0, 1, 5, 10, 15, 25]]
    y_cov = [MAPPING[i]["cov"] for i in x]
    y_pass = [MAPPING[i]["pass"] for i in x]

    gen_ablation_iterations(x, y_cov, "coverage")
    gen_ablation_iterations(x, y_pass, "pass@1")
