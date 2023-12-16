import datetime
import json
import os
import shutil
import stat
from pathlib import Path
from time import perf_counter
from typing import Optional, Any

import requests

_session = requests.Session()
_session.cookies.set("session", os.environ["AOC_SESSION_COOKIE_DATA"])


def get_input_filepath(day):
    return f"input/{day}.txt"


def load_input(filename):
    day = Path(filename).name[4:-3]
    with open(get_input_filepath(day)) as f:
        return f.read()


def get_current_year():
    return datetime.date.today().year


def get_current_day():
    return datetime.date.today().day


def download_input_data(day):
    filename = get_input_filepath(day)
    if os.path.exists(filename):
        return

    resp = _session.get(f"https://adventofcode.com/{get_current_year()}/day/{day}/input")
    resp.raise_for_status()

    with open(filename, "w") as outfile:
        outfile.write(resp.text)


def submit_answer(day: int, answer: int, part: int) -> bool:
    if has_star(day=day, part=part):
        return True

    resp = _session.post(
        f"https://adventofcode.com/{get_current_year()}/day/{day}/answer", data={"level": part, "answer": str(answer)}
    )

    if "That's the right answer!" in resp.text:
        set_star(day=day, part=part)
        return True

    else:
        print(resp.text)

    return False


def make_star_record():
    if not os.path.exists("stars.json"):
        with open("stars.json", "w") as starfile:
            starfile.write(json.dumps({day: ["-", "-"] for day in range(1, 26)}, indent=2) + "\n")


def has_star(day: int, part: int):
    with open("stars.json") as starfile:
        star_record = json.load(starfile)

    return star_record[str(day)][part - 1] == "*"


def set_star(day: int, part: int):
    with open("stars.json") as starfile:
        star_record = json.load(starfile)

    star_record[str(day)][part - 1] = "*"

    with open("stars.json", "w") as starfile:
        starfile.write(json.dumps(star_record, indent=2) + "\n")


def make_day(day: str | int):
    fname = f"day_{day}.py"
    if os.path.exists(fname):
        return

    shutil.copyfile(".templates/sample-day.py", fname)
    os.chmod(fname, os.stat(fname).st_mode | stat.S_IEXEC)


class RecordTime:
    def __enter__(self):
        self.start = perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Records time taken in milliseconds"""
        t = perf_counter() - self.start
        t *= 1000
        self.time = f"{t:.3f}ms"


def parse_grid(data: str, pad_edges: Optional[str] = None, tile_class=str) -> list[list[Any]]:
    grid = [[tile_class(char) for char in line.strip()] for line in data.strip().splitlines()]

    if pad_edges is not None:
        for i in range(len(grid)):
            grid[i] = [tile_class(pad_edges)] + grid[i] + [tile_class(pad_edges)]
        grid.insert(0, [tile_class(pad_edges)] * len(grid[0]))
        grid.append([tile_class(pad_edges)] * len(grid[0]))

    return grid
