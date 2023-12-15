#!/usr/bin/env python3
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
    parse_file_contents(file_contents)
    return 0


if __name__ == "__main__":
    data = load_input(__file__)
    answer1 = part1(data)
    answer2 = part2(data)
    print(f"The answer is: {answer1=}, {answer2=}")


test_data = [("HASH", 52), ("rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7", 1320)]


@pytest.mark.parametrize("data, expected_output", test_data)
def test_part1(data, expected_output):
    assert part1(data) == expected_output


def test_part1_real():
    assert part1(load_input(__file__)) == 507291


def test_part2():
    assert part2(test_data) == 0
