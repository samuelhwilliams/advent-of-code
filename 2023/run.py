#!/usr/bin/env python3
import webbrowser
from contextlib import redirect_stdout
import importlib
import sys
from io import StringIO

import pytest
from rich import print

from helpers import (
    load_input,
    get_current_day,
    download_input_data,
    make_day,
    RecordTime,
    make_star_record,
    has_star,
    submit_answer,
)

if __name__ == "__main__":
    current_day = sys.argv[1] if len(sys.argv) >= 2 else get_current_day()
    make_star_record()
    make_day(current_day)
    download_input_data(current_day)
    solution_filename = f"day_{current_day}.py"
    print(f"Running day {current_day}:")

    data = load_input(solution_filename)
    stdout = StringIO()

    for part in [1, 2]:
        with redirect_stdout(stdout):
            retval = pytest.main([solution_filename, "-k", f"test_part{part}"])
        print(f"\nPart {part}:")

        if retval == 0:
            print("\t Tests:", "✅")
        else:
            print("\t Tests:", "❌")
            retval = pytest.main([solution_filename, "-k", f"test_part{part}", "-vvvs"])
            sys.exit(part)

        if part == 2 or has_star(current_day, 2):
            solution_module = importlib.import_module(solution_filename[:-3])

            with RecordTime() as rt:
                answer = getattr(solution_module, f"part{part}")(data)

            print(
                f"\tAnswer: {answer}",
            )
            print(f"\t  Took: {rt.time}")

            if not has_star(current_day, part):
                print("\n\t[bold]Submit?[/bold] ", end="")
                submit = input()
                if submit.lower() in {"y", "yes"}:
                    if submit_answer(current_day, answer=answer, part=part):
                        print("\t  Star: 🌟")
                        webbrowser.open(f"https://adventofcode.com/2023/day/{current_day}")
                    else:
                        print("\t  Star: ❌")
