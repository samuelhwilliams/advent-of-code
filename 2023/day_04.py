#!/usr/bin/env python3
from typing import Iterator

from rich import print
import re


def get_matches(file_contents: str) -> Iterator[tuple[int, int]]:
    for i, line in enumerate(file_contents.strip().splitlines()):
        winning_side, matches_side = line.split(":")[1].strip().split("|")
        winning_numbers = set(re.split(r"\s+", winning_side.strip()))
        card_numbers = set(re.split(r"\s+", matches_side.strip()))
        num_matches = len(winning_numbers & card_numbers)
        yield i, num_matches


def part1(file_contents: str) -> int:
    return sum(2 ** (num_matches - 1) if num_matches else 0 for _, num_matches in get_matches(file_contents))


def part2(file_contents: str) -> int:
    num_cards = file_contents.strip().count("\n") + 1
    num_copies_of_each_card = [1] * num_cards

    for i, num_matches in get_matches(file_contents):
        for j in range(num_matches):
            num_copies_of_each_card[i + 1 + j] += num_copies_of_each_card[i]

    return sum(num_copies_of_each_card)


if __name__ == "__main__":
    with open("input/4.txt") as f:
        data = f.read()
    answer1, answer2 = part1(data), part2(data)
    print(f"Answer is: {answer1=}, {answer2=}")


test_data = """
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""


def test_day_part1():
    assert part1(test_data) == 13


def test_day_part2():
    assert part2(test_data) == 30
