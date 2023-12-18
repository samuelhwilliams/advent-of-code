#!/usr/bin/env python3
import re

from rich import print

from aoc.ds import t
from helpers import load_input


U = t((-1, 0))
D = t((1, 0))
L = t((0, -1))
R = t((0, 1))

DIRMAP = {"0": R, "1": D, "2": L, "3": U}


def parse_file_contents(file_contents: str):
    for line in file_contents.strip().splitlines():
        direction, distance, colour = line.strip().split(" ")
        yield globals()[direction], int(distance), colour[1:-1]


def segments(p):
    return zip(p, p[1:] + [p[0]])


def shoelace_formula_area(p):
    return 0.5 * abs(sum(x0 * y1 - x1 * y0 for ((x0, y0), (x1, y1)) in segments(p)))


def picks_theorem_area(coords, circumference_length):
    return int(shoelace_formula_area(coords) + (circumference_length // 2) + 1)


def part1(file_contents: str) -> int:
    coord = t((0, 0))
    coords = [(0, 0)]
    circumference_length = 0

    # Get coord points of all vertices
    for direction, distance, colour in parse_file_contents(file_contents):
        coord += direction * distance
        coords.append(coord)
        circumference_length += distance

    return picks_theorem_area(coords, circumference_length)


def parse_file_contents_part2(file_contents: str):
    for line in file_contents.strip().splitlines():
        hexpart = re.search("\(\#(.{6})\)", line).group(1)
        yield DIRMAP[hexpart[5]], int(hexpart[:5], 16)


def part2(file_contents: str) -> int:
    coord = t((0, 0))
    coords = [(0, 0)]
    circumference_length = 0

    # Get coord points of all vertices
    for direction, distance in parse_file_contents_part2(file_contents):
        coord += direction * distance
        coords.append(coord)
        circumference_length += distance

    return picks_theorem_area(coords, circumference_length)


if __name__ == "__main__":
    answer1 = part1(load_input(__file__))
    answer2 = part2(load_input(__file__))
    print(f"The answer is: {answer1=}, {answer2=}")


test_data = """
R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
"""


def test_part1():
    assert part1(test_data) == 62


def test_part1_real():
    assert part1(load_input(__file__)) == 47045


def test_part2():
    assert part2(test_data) == 952408144115


def test_part2_real():
    assert part2(load_input(__file__)) == 147839570293376
