#!/usr/bin/env python3
import itertools
import re

from rich import print

from helpers import load_input


def parse_file(file_contents: str) -> tuple["itertools.cycle[str]", dict[str, tuple[str, str]]]:
    lines = file_contents.strip().splitlines()
    directions = itertools.cycle(lines[0].strip())
    node_map: dict[str, tuple[str, str]] = {
        nodes[0]: (nodes[1], nodes[2]) for nodes in map(lambda line: re.findall(r"[A-Z]{3}", line), lines[2:])
    }
    return directions, node_map


def part1(file_contents: str) -> int:
    directions, node_map = parse_file(file_contents)
    steps = 0
    curloc = "AAA"
    while curloc != "ZZZ":
        dir = 0 if next(directions) == "L" else 1
        curloc = node_map[curloc][dir]
        steps += 1

    return steps


def part2(file_contents: str) -> int:
    return 0


if __name__ == "__main__":
    data = load_input(__file__)
    answer1 = part1(data)
    answer2 = part2(data)
    print(f"The answer is: {answer1=}, {answer2=}")


test_data = """
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
"""


def test_part1():
    assert part1(test_data) == 2


def test_part2():
    assert part2(test_data) == 0
