#!/usr/bin/env python3

import os
import shutil
import sys


def make_day(day: str):
    dirname = f"day-{day}"
    os.mkdir(dirname)
    shutil.copyfile(".templates/sample-day.py", f"{dirname}/day.py")
    shutil.copyfile(".templates/sample-test-day.py", f"{dirname}/test_day.py")


if __name__ == '__main__':
    make_day(sys.argv[1])
    print("Done.")
