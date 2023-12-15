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


class Boxes:
    def __init__(self, size=256):
        self.size = size
        self.slots = [{} for _ in range(size)]

    def __setitem__(self, key, value):
        self.slots[hash(key)][key] = int(value)

    def __iter__(self):
        # Takes advantage of the fact that modern python dicts have stable ordering on insertion
        yield from ((i, j, slot[label]) for i, slot in enumerate(self.slots) for j, label in enumerate(slot))

    def pop(self, key):
        self.slots[hash(key)].pop(key, None)


def part2(file_contents: str) -> int:
    boxes = Boxes()
    for step in parse_file_contents(file_contents):
        if step[-1] == "-":
            boxes.pop(step[:-1])
        else:
            boxes[step[:-2]] = step[-1]
    return sum((box + 1) * (slot + 1) * focus for box, slot, focus in boxes)


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
