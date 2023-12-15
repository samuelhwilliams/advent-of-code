#!/usr/bin/env python3


from rich import print

from helpers import load_input


def parse_file_contents(file_contents: str) -> list[str]:
    data = file_contents.splitlines()
    return data


def part1(data: list[str]) -> int:
    return 0


def part2(data: list[str]) -> int:
    return 0


if __name__ == "__main__":
    INPUT = parse_file_contents(load_input(__file__))
    answer1 = part1(INPUT)
    answer2 = part2(INPUT)
    print(f"The answer is: {answer1=}, {answer2=}")


test_data = """
"""


def test_part1():
    assert part1(parse_file_contents(test_data)) == 0


# def test_part1_real():
#     assert part1(parse_file_contents(load_input(__file__))) == 0


def test_part2():
    assert part2(parse_file_contents(test_data)) == 0


# def test_part2_real():
#     assert part2(parse_file_contents(load_input(__file__))) == 0
