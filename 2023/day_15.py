#!/usr/bin/env python3
import re
from functools import reduce
from itertools import chain

import pytest
from rich import print

from helpers import load_input


def parse_file_contents(file_contents: str) -> list[str]:
    data = file_contents.strip().split(",")
    return data


def hash(s: str) -> int:
    return reduce(lambda a, b: ((a + ord(b)) * 17) % 256, chain([0], s))


def part1(file_contents: str) -> int:
    parts = parse_file_contents(file_contents)
    return sum(hash(part) for part in parts)


def part2(file_contents: str) -> int:
    boxes = [{} for _ in range(256)]  # take advantage of modern python dicts being insertion-ordered
    for step in parse_file_contents(file_contents):
        label, focus = re.split(r"[-=]", step)
        box = hash(label)
        if label in boxes[box]:
            if focus:
                boxes[box][label] = int(focus)
            else:
                boxes[box].pop(label)
        elif focus:
            boxes[box][label] = int(focus)

    return sum((b + 1) * (i + 1) * focus for b in range(len(boxes)) for i, focus in enumerate(boxes[b].values()))


if __name__ == "__main__":
    data = load_input(__file__)
    answer1 = part1(data)
    answer2 = part2(data)
    print(f"The answer is: {answer1=}, {answer2=}")


@pytest.mark.parametrize(
    "data, expected_output", (("HASH", 52), ("rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7", 1320))
)
def test_part1(data, expected_output):
    assert part1(data) == expected_output


def test_part1_real():
    assert part1(load_input(__file__)) == 507291


def test_part2():
    assert part2("rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7") == 145


def test_part2_real():
    assert part2(load_input(__file__)) == 296921
