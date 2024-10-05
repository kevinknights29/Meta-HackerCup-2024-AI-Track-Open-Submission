# Source: https://github.com/HackerCupAI/starter-kits/blob/main/sample_data_solver/evaluate_programs.py

import subprocess
import sys
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
        problem = p_program[len(conf["programs_dir"]) : -len(".py")]
        p_program_out = conf["programs_dir"] + problem + ".out"
        p_in = conf["dataset_dir"] + problem + ".in"
        p_out = conf["dataset_dir"] + problem + ".out"
        run_str = f"python {p_program} < {p_in} > {p_program_out}"
        logger.info(run_str)
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


if __name__ == "__main__":
    main()
