# Advent of Code 2023

## Installing dependencies

1. Create a virtual environment (based on `.python-version`); activate it.
2. Run `make install`

## Starting a new day

Run `./make_day.py`. If run with no arguments, will setup for the current day:

* Today's challenge data will be downloaded to `input/#.txt`
* A template solution will be created at `day_#.txt`

## Running a day

Run `./run.py`. If run with no arguments, will run the current day's challenge:

* Runs tests for part 1
  * If those pass, runs the part 1 implementation against today's input and prints the answer.
  * If they fail, test failures are printed out.

* Runs tests for part 2
  * If those pass, runs the part 2 implementation against today's input and prints the answer.
  * If they fail, test failures are printed out.
