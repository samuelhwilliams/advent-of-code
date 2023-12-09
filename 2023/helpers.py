import datetime
import os
import shutil
import stat
from pathlib import Path
from time import perf_counter

import requests


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

    s = requests.Session()
    s.cookies.set("session", os.environ["AOC_SESSION_COOKIE_DATA"])

    resp = s.get(f"https://adventofcode.com/{get_current_year()}/day/{day}/input")
    resp.raise_for_status()

    with open(filename, "w") as outfile:
        outfile.write(resp.text)


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
