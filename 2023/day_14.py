#!/usr/bin/env python3


from rich import print

from helpers import load_input, parse_grid


def parse_file_contents(file_contents: str) -> list[list[str]]:
    grid = parse_grid(file_contents)
    return grid


def yield_loads(grid):
    for col in range(len(grid[0])):
        load = len(grid)
        for row in range(len(grid)):
            if grid[row][col] == "O":
                yield load
                load -= 1
            elif grid[row][col] == "#":
                load = len(grid) - row - 1


def part1(file_contents: str) -> int:
    grid = parse_file_contents(file_contents)
    return sum(yield_loads(grid))


def part2(file_contents: str) -> int:
    parse_file_contents(file_contents)
    return 0


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
    assert part2(test_data) == 0
