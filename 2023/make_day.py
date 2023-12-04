#!/usr/bin/env python3

import os
import shutil
import stat
import sys


def make_day(day: str):
    fname = f"day_{day}.py"
    shutil.copyfile(".templates/sample-day.py", fname)
    os.chmod(fname, os.stat(fname).st_mode | stat.S_IEXEC)


if __name__ == "__main__":
    make_day(sys.argv[1])
    print("Done.")
