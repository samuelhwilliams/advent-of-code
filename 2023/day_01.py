#!/usr/bin/env python

from rich import print

from helpers import load_input


def part1(data: list[str]) -> int:
    def _yield_values():
        for line in data:
            first_seen, latest_seen = None, None

            for char in line:
                if char.isdigit():
                    if first_seen is None:
                        first_seen = char
                    latest_seen = char

            last_seen = latest_seen
            yield int(first_seen + last_seen)

    return sum(_yield_values())


values = {
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "0",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
}
convert = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def part2(data: list[str]) -> int:
    def _yield_values():
        for line in data:
            first_seen, latest_seen = None, None

            for i in range(len(line)):
                to_check = {
                    line[i : i + 1],
                    line[i : i + 2],
                    line[i : i + 3],
                    line[i : i + 4],
                    line[i : i + 5],
                }
                if match := (values & to_check):
                    found = match.pop()
                    if first_seen is None:
                        first_seen = convert.get(found, found)
                    latest_seen = convert.get(found, found)

            last_seen = latest_seen
            yield int(first_seen + last_seen)

    return sum(_yield_values())


if __name__ == "__main__":
    data = load_input(__file__).strip().splitlines()
    answer1, answer2 = part1(data), part2(data)
    print(f"Answer is: {answer1=}, {answer2=}")


def test_part1():
    data = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
"""
    assert part1(data.splitlines()) == 142


def test_part2():
    data = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""
    assert part2(data.splitlines()) == 281
