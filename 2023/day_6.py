#!/usr/bin/env python3
import dataclasses
import re
from functools import reduce

from rich import print

from helpers import load_input


@dataclasses.dataclass
class Race:
    time: int
    distance: int


def parse_racelist(file_contents: str) -> list[Race]:
    times, distances = file_contents.strip().splitlines()
    return [Race(int(t), int(d)) for t, d in zip(re.split("\s+", times)[1:], re.split("\s+", distances)[1:])]


def part1(file_contents: str) -> int:
    races = parse_racelist(file_contents)
    ways_to_beat = []
    for race in races:
        ways_to_beat.append(len([t for t in range(race.time) if t * (race.time - t) > race.distance]))
    return reduce(lambda x, y: x * y, ways_to_beat)


def parse_racelist_part2(file_contents: str) -> Race:
    times, distances = file_contents.strip().splitlines()
    return Race(int(times.split(":")[1].replace(" ", "")), int(distances.split(":")[1].replace(" ", "")))


def part2(file_contents: str) -> int:
    race = parse_racelist_part2(file_contents)
    ways_to_beat = len([t for t in range(race.time) if t * (race.time - t) > race.distance])
    return ways_to_beat


if __name__ == "__main__":
    data = load_input(__file__)
    answer1 = part1(data)
    answer2 = part2(data)
    print(f"The answer is: {answer1=}, {answer2=}")


test_data = """
Time:      7  15   30
Distance:  9  40  200
"""


def test_part1():
    assert part1(test_data) == 288


def test_part2():
    assert part2(test_data) == 71503
