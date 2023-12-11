#!/usr/bin/env python3
import itertools
from typing import Iterable

import pytest

from rich import print

from helpers import load_input, parse_grid


def parse_file_contents(file_contents: str) -> list[list[str]]:
    grid = parse_grid(file_contents)
    return grid


def yield_star_coords(universe: list[list[str]]) -> Iterable[list[tuple[int, int]]]:
    yield from ((x, y) for x in range(len(universe)) for y in range(len(universe[x])) if universe[x][y] == "#")


def get_star_pairs(star_coords: list[tuple[int, int]]) -> Iterable[tuple[tuple[int, int], tuple[int, int]]]:
    return itertools.combinations(star_coords, 2)


def find_universal_expansions(universe) -> tuple[tuple[int], tuple[int]]:
    x_expansions = tuple(x for x in range(len(universe)) if all(p == "." for p in universe[x]))
    y_expansions = tuple(y for y in range(len(universe[0])) if all(universe[x][y] == "." for x in range(len(universe))))
    return x_expansions, y_expansions


def find_distances_between_stars(star_coords, x_expansions, y_expansions, expansion_factor):
    for s1, s2 in get_star_pairs(star_coords):
        yield abs(s1[0] - s2[0]) + abs(s1[1] - s2[1]) + (
            (
                len([x for x in x_expansions if min(s1[0], s2[0]) < x < max(s1[0], s2[0])])
                + len([y for y in y_expansions if min(s1[1], s2[1]) < y < max(s1[1], s2[1])])
            )
            * (expansion_factor - 1)
        )


def part1(file_contents: str) -> int:
    universe = parse_file_contents(file_contents)
    x_expansions, y_expansions = find_universal_expansions(universe)
    return sum(
        find_distances_between_stars(yield_star_coords(universe), x_expansions, y_expansions, expansion_factor=2)
    )


def part2(file_contents: str, expansion_factor: int = 1_000_000) -> int:
    universe = parse_file_contents(file_contents)
    x_expansions, y_expansions = find_universal_expansions(universe)
    return sum(
        find_distances_between_stars(
            yield_star_coords(universe), x_expansions, y_expansions, expansion_factor=expansion_factor
        )
    )


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


@pytest.mark.parametrize(
    "expansion_factor, expected_sum_distance",
    (
        (10, 1030),
        (100, 8410),
    ),
)
def test_part2(expansion_factor, expected_sum_distance):
    assert part2(test_data, expansion_factor=expansion_factor) == expected_sum_distance
