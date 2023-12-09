#!/usr/bin/env python3

from rich import print

from helpers import load_input


def parse_file_contents(file_contents: str) -> list[list[int]]:
    data = file_contents.strip().splitlines()
    return [[int(i) for i in line.split(" ")] for line in data]


def calculate_next_value(data: list[int]) -> tuple[int, int]:
    diffs = [(b - a) for a, b in zip(data[:-1], data[1:])]
    delta = 0 if all(x == 0 for x in diffs) else calculate_next_value(diffs)[1]
    return data[-1] + diffs[-1] + delta, diffs[-1] + delta


def part1(file_contents: str) -> int:
    return sum(calculate_next_value(line)[0] for line in parse_file_contents(file_contents))


def part2(file_contents: str) -> int:
    return sum(calculate_next_value(line[::-1])[0] for line in parse_file_contents(file_contents))


if __name__ == "__main__":
    data = load_input(__file__)
    answer1 = part1(data)
    answer2 = part2(data)
    print(f"The answer is: {answer1=}, {answer2=}")


test_data = """
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
"""


def test_part1():
    assert part1(test_data) == 114


def test_part2():
    assert part2(test_data) == 2
