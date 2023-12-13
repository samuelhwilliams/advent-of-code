#!/usr/bin/env python3
import itertools

from rich import print

from helpers import load_input, parse_grid


def parse_file_contents(file_contents: str) -> list[list[list[str]]]:
    return [parse_grid(grid) for grid in file_contents.split("\n\n")]


def check_grid_rows(grid):
    for i, pairs in enumerate(itertools.pairwise(grid)):
        r1, r2 = pairs
        mirror_row_pairs = zip(grid[i - 1 :: -1] if i > 0 else [], grid[i + 2 : :])
        if r1 == r2 and all(y1 == y2 for y1, y2 in mirror_row_pairs):
            return (i + 1) * 100

    transposed_grid = list(zip(*grid))
    for i, pairs in enumerate(itertools.pairwise(transposed_grid)):
        r1, r2 = pairs
        mirror_row_pairs = zip(transposed_grid[i - 1 :: -1] if i > 0 else [], transposed_grid[i + 2 : :])
        if r1 == r2 and all(y1 == y2 for y1, y2 in mirror_row_pairs):
            return i + 1


def part1(file_contents: str) -> int:
    grids = parse_file_contents(file_contents)
    return sum(check_grid_rows(grid) for grid in grids)


def part2(file_contents: str) -> int:
    parse_file_contents(file_contents)
    return 0


if __name__ == "__main__":
    data = load_input(__file__)
    answer1 = part1(data)
    answer2 = part2(data)
    print(f"The answer is: {answer1=}, {answer2=}")


test_data = """
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
"""


def test_part1():
    assert part1(test_data) == 405


def test_part1_real():
    assert part1(load_input(__file__)) == 32371


def test_part2():
    assert part2(test_data) == 0
