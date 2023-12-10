#!/usr/bin/env python3
from typing import Union
from collections import Counter

from rich import print

from helpers import load_input


def parse_file_contents(file_contents: str) -> list[list[Union[str, int]]]:
    data = [[c for c in line] for line in file_contents.strip().splitlines()]
    for row in data:
        row.insert(0, ".")
        row.append(".")
    width = len(data[0])
    data.insert(0, ["."] * width)
    data.append(["."] * width)
    # print(data)
    return data


def get_starting_coord(grid):
    for x in range(len(grid)):
        for y in range(len(grid)):
            if grid[x][y] == "S":
                return x, y


def find_max_depth(grid: list[list[Union[str, int]]], queue: list[tuple[tuple[int, int], int]]) -> int:
    i = 0
    loops = set()
    while i < len(queue):
        coord, depth = queue[i]

        if isinstance(grid[coord[0]][coord[1]], int):
            i += 1
            continue

        above, left, self, right, below = (
            grid[coord[0] - 1][coord[1]],
            grid[coord[0]][coord[1] - 1],
            grid[coord[0]][coord[1]],
            grid[coord[0]][coord[1] + 1],
            grid[coord[0] + 1][coord[1]],
        )
        if above in {"|", "F", "7"} and self in {"S", "|", "J", "L"}:
            queue.append(((coord[0] - 1, coord[1]), depth + 1))
            grid[coord[0]][coord[1]] = depth
        if left in {"-", "F", "L"} and self in {"S", "-", "J", "7"}:
            queue.append(((coord[0], coord[1] - 1), depth + 1))
            grid[coord[0]][coord[1]] = depth
        if right in {"-", "J", "7"} and self in {"S", "-", "F", "L"}:
            queue.append(((coord[0], coord[1] + 1), depth + 1))
            grid[coord[0]][coord[1]] = depth
        if below in {"|", "L", "J"} and self in {"S", "|", "F", "7"}:
            queue.append(((coord[0] + 1, coord[1]), depth + 1))
            grid[coord[0]][coord[1]] = depth

        c = Counter(filter(lambda x: isinstance(x, int), [above, left, right, below]))
        mc = c.most_common(1)
        if mc and mc[0][1] == 2:
            loops.add(depth)

        i += 1

    with open("map.txt", "w") as outfile:
        outfile.write("\n".join([",".join([str(x) for x in line]) for line in grid]))

    return max(loops)


def part1(file_contents: str) -> int:
    grid = parse_file_contents(file_contents)
    coords = [(get_starting_coord(grid), 0)]
    return find_max_depth(grid, coords)


def part2(file_contents: str) -> int:
    grid = parse_file_contents(file_contents)  # noqa
    return 0


if __name__ == "__main__":
    data = load_input(__file__)
    answer1 = part1(data)
    answer2 = part2(data)
    print(f"The answer is: {answer1=}, {answer2=}")


test_data = """
..F7.
.FJ|.
SJ.L7
|F--J
LJ...
"""


def test_part1():
    assert part1(test_data) == 8


def test_part2():
    assert part2(test_data) == 0
