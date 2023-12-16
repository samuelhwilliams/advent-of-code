#!/usr/bin/env python3
import dataclasses
import math
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
    return [Race(int(t), int(d)) for t, d in zip(re.split(r"\s+", times)[1:], re.split(r"\s+", distances)[1:])]


def solve_quadratic(a, b, c) -> list[float]:
    return [(-b + (one * math.sqrt(b**2 - (4 * a * c)))) / (2 * a) for one in [1, -1]]


def part1(file_contents: str) -> int:
    races = parse_racelist(file_contents)
    ways_to_beat = []
    for race in races:
        ways_to_beat.append(len([t for t in range(race.time) if t * (race.time - t) > race.distance]))
    return reduce(lambda x, y: x * y, ways_to_beat)


def part1_quadratic(file_contents: str) -> int:
    races = parse_racelist(file_contents)
    ways_to_beat = []
    for race in races:
        quickest, slowest = sorted(solve_quadratic(-1, race.time, -race.distance))  # type: float, float
        ways_to_beat.append(math.ceil(slowest) - math.floor(quickest) - 1)
    return reduce(lambda x, y: x * y, ways_to_beat)


def parse_racelist_part2(file_contents: str) -> Race:
    times, distances = file_contents.strip().splitlines()
    return Race(int(times.split(":")[1].replace(" ", "")), int(distances.split(":")[1].replace(" ", "")))


def part2(file_contents: str) -> int:
    race = parse_racelist_part2(file_contents)
    ways_to_beat = len([t for t in range(race.time) if t * (race.time - t) > race.distance])
    return ways_to_beat


def part2_quadratic(file_contents: str) -> int:
    race = parse_racelist_part2(file_contents)
    quickest, slowest = sorted(solve_quadratic(-1, race.time, -race.distance))  # type: float, float
    return math.ceil(slowest) - math.floor(quickest) - 1


if __name__ == "__main__":
    data = load_input(__file__)
    answer1 = part1_quadratic(data)
    answer2 = part2_quadratic(data)
    print(f"The answer is: {answer1=}, {answer2=}")


test_data = """
Time:      7  15   30
Distance:  9  40  200
"""


def test_part1():
    assert part1(test_data) == 288


def test_part2():
    assert part2(test_data) == 71503


def test_part1_quadratic():
    assert part1_quadratic(test_data) == 288


def test_part2_quadratic():
    assert part2_quadratic(test_data) == 71503
