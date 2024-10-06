# Source: https://github.com/HackerCupAI/starter-kits/blob/main/sample_data_solver/generate_programs.py

import sys
from pathlib import Path

import torch
import transformers
from loguru import logger
from transformers import AutoTokenizer
from yaml import load
from yaml.loader import SafeLoader

# Setup Logger
logger.add(
    sys.stdout,
    format="{time} | {level} | {file}:{function}:{line} - {message}",
    level="INFO",
)
logging_dir = "logs/generation"
Path(logging_dir).mkdir(parents=True, exist_ok=True)
logger.add(f"{logging_dir}/" + "{time}.log")

# Load Config
with open("config.yaml", encoding="utf-8") as f:
    conf = load(f, Loader=SafeLoader)
logger.info("Config loaded!")


def generate_func(
    pipeline: transformers.Pipeline,
    tokenizer: transformers.PreTrainedTokenizer | transformers.PreTrainedTokenizerFast,
    ins: list[str],
    outs: list[str],
    desc: str,
) -> str:
    """Generates solution's function

    Args:
        pipeline (transformers.Pipeline): pipeline to generate the solution.
        tokenizer (transformers.PreTrainedTokenizer | transformers.PreTrainedTokenizerFast): tokenizer for the pipeline.
        ins (list[str]): problem's input.
        outs (list[str]): problem's output.
        desc (str): problem's description

    Returns:
        str: function
    """

    code = '"""Problem Description:\n'
    for line in desc.splitlines():
        code += f"    {line}\n"
    code += '"""\n'
    code = "def f(a):\n"
    code += '    """Problem Inputs and Outputs:\n'
    for i, o in zip(ins, outs):
        code += f"    >>> f({i})\n"
        code += f"    {o}\n"
    code += '    """\n'
    logger.debug(f"Code Input: {code}")

    prompt = "".join(conf["system_prompt"]) + code + conf["end_of_instruction"]
    logger.debug(f"Prompt: {prompt}")
    logger.info(f"Input Tokens: {tokenizer(prompt, return_tensors='pt', return_length=True)['length']}")

    seq = pipeline(
        prompt,
        do_sample=True,
        temperature=0.1,
        num_return_sequences=1,
        eos_token_id=tokenizer.eos_token_id,
        max_new_tokens=conf["max_new_tokens"],
        tokenizer=tokenizer,
        stop_strings=[conf["end_of_sequence"]],
        max_time=conf["max_time"],
        return_full_text=False,
    )[0]
    raw_result: str = seq["generated_text"]
    logger.debug(f"Result [Raw]: {raw_result}")
    logger.info(f"Output Tokens: {tokenizer(raw_result, return_tensors='pt', return_length=True)['length']}")

    result = ""
    append_flag = False
    for line in raw_result.splitlines():
        if append_flag:
            if line.startswith("```"):
                append_flag = False
                break
            result = result + line + "\n"
        else:
            if line.startswith("def"):
                append_flag = True
                result = result + line + "\n"

    logger.debug(f"Result [Processed]: {result}")
    return result


template = """
T = int(input())
for case_num in range(1, T + 1):
    a = input().split()
    for i in range(len(a)):
        try:
            a[i] = float(a[i])
        except ValueError:
            pass
        try:
            a[i] = int(a[i])
        except ValueError:
            pass
    if len(a) == 1:
        a = a[0]
    else:
        if isinstance(a[0], int) and isinstance(a[1], str):
            if (len(a) - 1) == a[0]:
                a = a[1:]
    print(f"Case #{case_num}: {f(a)}")
"""


def _process_line(line: str) -> str | list[str]:
    """Line Processing Helper Function for problem's inputs or outputs.

    Args:
        line (str): line of text from problem's inputs or outputs.

    Returns:
        str | list[str]: processed line
    """
    
    a = line.split()
    for i in range(len(a)):
        try:
            a[i] = float(a[i])
        except ValueError:
            pass
        try:
            a[i] = int(a[i])
        except ValueError:
            pass
    if len(a) == 1:
        a = a[0]
    else:
        # Simplify when first item is number of strings in list
        if isinstance(a[0], int) and isinstance(a[1], str):
            if (len(a) - 1) == a[0]:
                a = a[1:]
    return a


def get_sample_data() -> list[tuple[Path, str, str, str]]:
    """Extracts Problem's Data.

    Returns:
        list[tuple[Path, str, str, str]]: Problem's path, input, output, and description.
    """
    results = []

    # Find problems where each test case
    # is one input line and one output line.
    suitable_problems = []
    for p_in in Path(conf["dataset_dir"]).glob("**/*_sample_input.txt"):
        with open(p_in, "r") as f:
            num_cases = int(f.readline())
            num_lines = len(f.readlines())

        p_out = str(p_in).replace("input.txt", "output.txt")
        try:
            with open(p_out, "r") as f:
                num_lines_out = len(f.readlines())
            if num_cases == num_lines == num_lines_out:
                suitable_problems.append(p_in)
        except FileNotFoundError:
            pass

        p_desc = str(p_in).replace("_sample_input.txt", ".md")
        try:
            with open(p_desc, "r") as f:
                desc = f.read()
        except FileNotFoundError:
            pass

    for p_in in suitable_problems:
        max_line_len = 100

        ins = []
        outs = []
        too_large = False
        with open(p_in, "r") as f:
            num_cases = int(f.readline())
            for _ in range(num_cases):
                line = f.readline()
                if len(line) > max_line_len:
                    too_large = True
                ins.append(_process_line(line))

        p_out = str(p_in).replace("input.txt", "output.txt")
        with open(p_out, "r") as f:
            for _ in range(num_cases):
                line = f.readline()[len("Case #1: ") :]  # Remove Case num prefix
                outs.append(_process_line(line))

        if not too_large:
            results.append((p_in, ins, outs, desc))

    return results


def main():
    tokenizer = AutoTokenizer.from_pretrained(conf["model_dir"])
    pipeline = transformers.pipeline(
        "text-generation",
        model=conf["model_dir"],
        torch_dtype=torch.float16,
        device_map="auto",
    )

    data = get_sample_data()
    for p_in, ins, outs, desc in data:
        logger.info(f"Generating solution for {p_in}...")
        f = generate_func(pipeline, tokenizer, ins, outs, desc)
        p_program = (
            conf["programs_dir"]
            + str(p_in)[len(conf["dataset_dir"]) : -len("_sample_input.txt")]
            + ".py"
        )
        p_program = Path(p_program)
        p_program.parent.mkdir(parents=True, exist_ok=True)
        p_program.write_text(f + template)
        logger.info(f"Wrote program {p_program}!")


if __name__ == "__main__":
    import time

    logger.info("Started Generation Script!")
    start_time = time.time()
    main()
    logger.info(f"Execution Time: {time.time() - start_time} seconds")
