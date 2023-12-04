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
    with open("input.txt") as f:
        data = f.read()

    answer1 = part1(data)
    answer2 = part2(data)

    print(f"The answer is {answer1=}, {answer2=}")
