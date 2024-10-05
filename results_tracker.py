import csv
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
logging_dir = "logs/results"
Path(logging_dir).mkdir(parents=True, exist_ok=True)
logger.add(f"{logging_dir}/" + "{time}.log")

# Load Config
with open("config.yaml", encoding="utf-8") as f:
    conf = load(f, Loader=SafeLoader)
logger.info("Config loaded!")


class ResultsTracker:
    def __init__(self, results_dir):
        self.results_dir = Path(results_dir)

    def parse_score(self, score):
        if score == "TIMEOUT" or score == "FAIL":
            return -1
        return int(score.split("/")[0])

    def get_all_results(self):
        all_results = {}
        for csv_file in self.results_dir.glob("*.csv"):
            with csv_file.open("r") as f:
                reader = csv.reader(f)
                next(reader)  # Skip header
                run_results = {}
                for row in reader:
                    _, problem, score = row
                    run_results[problem] = self.parse_score(score)
                all_results[csv_file.stem] = run_results
        return all_results

    def compare_all_results(self):
        all_results = self.get_all_results()
        if not all_results:
            logger.warning("No results found.")

        best_run = max(all_results, key=lambda x: sum(all_results[x].values()))

        logger.info(f"Best overall run: {best_run}")
        logger.info("Problem-wise best scores:")

        all_problems = set(problem for run in all_results.values() for problem in run)

        for problem in sorted(all_problems):
            best_score = max(
                (all_results[run].get(problem, -1) for run in all_results), default=-1
            )
            best_runs = [
                run
                for run in all_results
                if all_results[run].get(problem, -1) == best_score
            ]

            if best_score == -1:
                score_str = "TIMEOUT/FAIL"
            else:
                score_str = str(best_score)

            logger.info(f"{problem}: {score_str} (Best in: {', '.join(best_runs)})")


def main():
    tracker = ResultsTracker(conf["results_dir"])
    tracker.compare_all_results()


if __name__ == "__main__":
    main()
