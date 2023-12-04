from pathlib import Path


def load_input(filename):
    day_number = Path(filename).name[4:-3]
    with open(f"input/{day_number}.txt") as f:
        return f.read()
