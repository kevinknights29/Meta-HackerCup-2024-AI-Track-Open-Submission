# Source: https://github.com/HackerCupAI/starter-kits/blob/main/sample_data_solver/evaluate_programs.py

import csv
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from loguru import logger
from yaml import load
from yaml.loader import SafeLoader

# Setup Logger
logger.add(
    sys.stdout,
    format="{time} | {level} | {file}:{function}:{line} - {message}",
    level="INFO",
)
logging_dir = "logs/evaluation"
Path(logging_dir).mkdir(parents=True, exist_ok=True)
logger.add(f"{logging_dir}/" + "{time}.log")

# Load Config
with open("config.yaml", encoding="utf-8") as f:
    conf = load(f, Loader=SafeLoader)
logger.info("Config loaded!")


def main():
    results = []

    for p_program in Path(conf["programs_dir"]).glob("**/*.py"):
        p_program = str(p_program)
        logger.info(f"Evalutation program {p_program}...")
        problem = p_program[len(conf["programs_dir"]) : -len(".py")]
        p_program_out = conf["programs_dir"] + problem + ".out"
        p_in = conf["dataset_dir"] + problem + ".in"
        p_out = conf["dataset_dir"] + problem + ".out"
        run_str = f"python {p_program} < {p_in} > {p_program_out}"
        logger.debug(run_str)
        try:
            subprocess.run(run_str, shell=True, timeout=60)
        except subprocess.TimeoutExpired:
            results.append((problem, "TIMEOUT"))
            continue

        with open(p_program_out, "r") as f_program_out:
            program_out = f_program_out.readlines()
        with open(p_out, "r") as f_out:
            out = f_out.readlines()
        if len(program_out) != len(out):
            results.append((problem, "FAIL"))
            continue

        good = 0
        for i in range(len(out)):
            if program_out[i] == out[i]:
                good += 1

        results.append((problem, f"{good}/{len(out)}"))

    logger.info("| Problem | Score |")
    logger.info("| ------- | ----- |")
    for p, score in results:
        logger.info(f"| {p} | {score} |")

    # Write results to CSV
    csv_filename = create_csv_filename(conf["results_dir"], conf["model_dir"])
    write_results_to_csv(csv_filename, results)


def create_csv_filename(results_dir, model_dir):
    model_path = Path(model_dir)
    model_name = (
        model_path.name or model_path.parent.name
    )  # Use parent name if model_dir ends with '/'
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return Path(results_dir) / f"{model_name}_{timestamp}.csv"


def write_results_to_csv(filename, results):
    filepath = Path(filename)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    with filepath.open("w", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Timestamp", "Problem", "Score"])
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for problem, score in results:
            csv_writer.writerow([timestamp, problem, score])

    logger.info(f"Results written to {filepath}")


if __name__ == "__main__":
    main()
