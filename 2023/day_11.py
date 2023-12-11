#!/usr/bin/env python3
import itertools
from typing import Iterable

import numpy as np

from rich import print

from helpers import load_input, parse_grid


def parse_file_contents(file_contents: str) -> np.array:
    grid = parse_grid(file_contents)
    return np.array(grid)


def expand_universe(grid: np.array) -> np.array:
    for rotation in [1, -1]:
        for dupe_row in [x for x, row in enumerate(grid) if all(cell == "." for cell in row)][::-1]:
            grid = np.insert(grid, dupe_row, ".", axis=0)
        grid = np.rot90(grid, k=rotation)
    return grid


def find_star_coords(universe: np.array) -> list[tuple[int, int]]:
    return [(x, y) for x in range(len(universe)) for y in range(len(universe[x])) if universe[x][y] == "#"]


def get_star_pairs(star_coords: list[tuple[int, int]]) -> Iterable[tuple[tuple[int, int], tuple[int, int]]]:
    return itertools.combinations(star_coords, 2)


def part1(file_contents: str) -> int:
    grid = parse_file_contents(file_contents)
    universe = expand_universe(grid)
    star_coords = find_star_coords(universe)
    return sum(abs(s1[0] - s2[0]) + abs(s1[1] - s2[1]) for s1, s2 in get_star_pairs(star_coords))


def part2(file_contents: str) -> int:
    parse_file_contents(file_contents)
    return 0


if __name__ == "__main__":
    data = load_input(__file__)
    answer1 = part1(data)
    answer2 = part2(data)
    print(f"The answer is: {answer1=}, {answer2=}")


test_data = """
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
"""


def test_part1():
    assert part1(test_data) == 374


def test_part1_real():
    assert part1(load_input(__file__)) == 10173804


def test_part2():
    assert part2(test_data) == 0
