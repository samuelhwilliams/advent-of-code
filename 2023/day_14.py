#!/usr/bin/env python3
from contextlib import suppress

from rich import print

from helpers import load_input, parse_grid


def parse_file_contents(file_contents: str) -> list[list[str]]:
    grid = parse_grid(file_contents)
    return grid


def serialize_grid(grid):
    return "\n".join("".join(c for c in row) for row in grid) + "\n\n"


def score_grid(grid):
    return sum(len(grid[0]) - x for y in range(len(grid)) for x in range(len(grid[0])) if grid[x][y] == "O")


def _slide_north(grid):
    for col in range(len(grid[0])):
        slot = 0
        for row in range(len(grid)):
            if grid[row][col] == "O":
                grid[row][col] = "."
                grid[slot][col] = "O"
                slot += 1
            elif grid[row][col] == "#":
                slot = row + 1
    return grid


def slide_north(grid):
    grid = _slide_north(grid)
    return grid


def slide_south(grid):
    grid = _slide_north(grid[::-1])[::-1]
    return grid


def slide_west(grid):
    grid = list(map(list, zip(*_slide_north(list(map(list, zip(*grid)))))))
    return grid


def slide_east(grid):
    grid = [row[::-1] for row in map(list, zip(*_slide_north(list(map(list, zip(*[row[::-1] for row in grid]))))))]
    return grid


def part1(file_contents: str) -> int:
    grid = parse_file_contents(file_contents)
    return score_grid(slide_north(grid))


def part2(file_contents: str, cycles=1_000_000_000) -> int:
    grid = parse_file_contents(file_contents)

    grids = []
    grids.append(serialize_grid(grid))
    for i in range(1, cycles + 1):
        grid = slide_north(grid)
        grid = slide_west(grid)
        grid = slide_south(grid)
        grid = slide_east(grid)

        with suppress(ValueError):
            if grid_cycle_starts_at := grids.index(serialize_grid(grid)):
                grid_length = i - grid_cycle_starts_at
                return score_grid(parse_grid(grids[grid_cycle_starts_at + ((cycles - i) % grid_length)]))

        grids.append(serialize_grid(grid))


if __name__ == "__main__":
    data = load_input(__file__)
    answer1 = part1(data)
    answer2 = part2(data)
    print(f"The answer is: {answer1=}, {answer2=}")


test_data = """
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
"""


def test_part1():
    assert part1(test_data) == 136


def test_part1_real():
    assert part1(load_input(__file__)) == 106378


def test_part2():
    assert part2(test_data) == 64


def test_part2_real():
    assert part2(load_input(__file__)) == 90795
