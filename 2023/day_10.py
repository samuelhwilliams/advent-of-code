#!/usr/bin/env python3
import dataclasses
from itertools import combinations
from typing import Optional

from rich import print

from helpers import load_input


@dataclasses.dataclass
class Node:
    char: str
    depth: Optional[int] = None


def parse_file_contents(file_contents: str) -> list[list[Node]]:
    data = [[Node(c) for c in line] for line in file_contents.strip().splitlines()]
    for row in data:
        row.insert(0, Node("."))
        row.append(Node("."))
    width = len(data[0])
    data.insert(0, [Node(".") for _ in range(width)])
    data.append([Node(".") for _ in range(width)])
    return data


def get_starting_coord(grid):
    for x in range(len(grid)):
        for y in range(len(grid)):
            if grid[x][y].char == "S":
                return x, y


def find_max_depth(grid: list[list[Node]], queue: list[tuple[tuple[int, int], int]]) -> int:
    i = 0
    loops = set()
    while i < len(queue):
        coord, depth = queue[i]

        if isinstance(grid[coord[0]][coord[1]].depth, int):
            i += 1
            continue

        above, left, self, right, below = (
            grid[coord[0] - 1][coord[1]],
            grid[coord[0]][coord[1] - 1],
            grid[coord[0]][coord[1]],
            grid[coord[0]][coord[1] + 1],
            grid[coord[0] + 1][coord[1]],
        )
        if above.char in {"|", "F", "7"} and self.char in {"S", "|", "J", "L"}:
            queue.append(((coord[0] - 1, coord[1]), depth + 1))
            grid[coord[0]][coord[1]].depth = depth
        if left.char in {"-", "F", "L"} and self.char in {"S", "-", "J", "7"}:
            queue.append(((coord[0], coord[1] - 1), depth + 1))
            grid[coord[0]][coord[1]].depth = depth
        if right.char in {"-", "J", "7"} and self.char in {"S", "-", "F", "L"}:
            queue.append(((coord[0], coord[1] + 1), depth + 1))
            grid[coord[0]][coord[1]].depth = depth
        if below.char in {"|", "L", "J"} and self.char in {"S", "|", "F", "7"}:
            queue.append(((coord[0] + 1, coord[1]), depth + 1))
            grid[coord[0]][coord[1]].depth = depth

        if any(x == y for x, y in combinations([above, left, right, below], 2)):
            loops.add(depth)

        i += 1

    # with open("map.txt", "w") as outfile:
    #     outfile.write("\n".join([",".join([x.char if x.depth is not None else "." for x in line]) for line in grid]))

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


def test_part1_real():
    assert part1(load_input(__file__)) == 6942


def test_part2():
    assert part2(test_data) == 0
