#!/usr/bin/env python3
import dataclasses
import enum
from collections import Counter
from typing import Optional

import pytest
from rich import get_console
from rich.style import Style

from helpers import load_input, parse_grid

console = get_console()


@dataclasses.dataclass
class Node:
    char: str
    depth: Optional[int] = None
    inside: Optional[bool] = None

    @property
    def pipe(self):
        return self.depth is not None


class Direction(enum.Enum):
    ABOVE = (-1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)
    BELOW = (1, 0)

    @property
    def pipes(self):
        if self == Direction.ABOVE:
            return {"|", "F", "7"}
        elif self == Direction.LEFT:
            return {"-", "F", "L"}
        elif self == Direction.RIGHT:
            return {"-", "7", "J"}
        else:
            return {"|", "J", "L"}

    @property
    def opposite(self):
        return Direction((self.value[0] * -1, self.value[1] * -1))


def get_node(grid: list[list[Node]], coord: tuple[int, int]) -> Node:
    return grid[coord[0]][coord[1]]


def get_adjacent_coord(coord: tuple[int, int], direction: Direction) -> tuple[int, int]:
    return coord[0] + direction.value[0], coord[1] + direction.value[1]


def parse_file_contents(file_contents: str) -> list[list[Node]]:
    grid = parse_grid(file_contents, pad_edges=".")
    return [[Node(c) for c in row] for row in grid]


def solve_s_piece(grid: list[list[Node]], coord: tuple[int, int]):
    x, y = coord
    above, left, right, below = (
        get_node(grid, get_adjacent_coord((x, y), Direction.ABOVE)),
        get_node(grid, get_adjacent_coord((x, y), Direction.LEFT)),
        get_node(grid, get_adjacent_coord((x, y), Direction.RIGHT)),
        get_node(grid, get_adjacent_coord((x, y), Direction.BELOW)),
    )
    if above.char in Direction.ABOVE.pipes and left.char in Direction.LEFT.pipes:
        return "J"
    elif above.char in Direction.ABOVE.pipes and right.char in Direction.RIGHT.pipes:
        return "L"
    elif above.char in Direction.ABOVE.pipes and below.char in Direction.BELOW.pipes:
        return "|"
    elif left.char in Direction.LEFT.pipes and right.char in Direction.RIGHT.pipes:
        return "-"
    elif left.char in Direction.LEFT.pipes and below.char in Direction.BELOW.pipes:
        return "7"
    elif below.char in Direction.BELOW.pipes and right.char in Direction.RIGHT.pipes:
        return "F"


def find_and_fix_start_tile(grid):
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            if grid[x][y].char == "S":
                grid[x][y].char = solve_s_piece(grid, (x, y))
                return x, y


def follow_pipes_and_record_depths(grid: list[list[Node]], queue: list[tuple[tuple[int, int], int]]):
    i = 0
    while i < len(queue):
        coord, depth = queue[i]

        if isinstance(grid[coord[0]][coord[1]].depth, int):
            i += 1
            continue

        self = get_node(grid, coord)
        neighbours = [(direction, get_adjacent_coord(coord, direction)) for direction in Direction]
        track_neighbour_depths: Counter = Counter()
        for direction, neighbour_coord in neighbours:
            neighbour = get_node(grid, neighbour_coord)
            if neighbour.char in direction.pipes and self.char in direction.opposite.pipes:
                queue.append((neighbour_coord, depth + 1))
                grid[coord[0]][coord[1]].depth = depth
                track_neighbour_depths.update([depth + 1])

        i += 1


def print_grid(grid: list[list[Node]], cur_coord: Optional[tuple[int, int]] = None):
    max_depth = max([node.depth or 0 for row in grid for node in row])
    for x, row in enumerate(grid):
        for y, node in enumerate(row):
            if node.pipe:
                gradient = min(128, (node.depth or 0) * 128 // max_depth)
                if cur_coord and cur_coord == (x, y):
                    style = Style(color="white", bgcolor="green", blink=True, blink2=True)
                elif node.depth == max_depth or node.depth == 0:
                    style = Style(color="black", bgcolor="yellow")
                else:
                    style = Style(color="white", bgcolor=f"rgb(128, 0, {gradient})")
                console.print(str(node.char), end="", style=style)
            else:
                if cur_coord and cur_coord == (x, y):
                    style = Style(color="green", bgcolor="green", blink=True, blink2=True)
                else:
                    style = Style(
                        color="white",
                        bgcolor="rgb(0, 255, 255)"
                        if node.inside
                        else "rgb(0, 0, 0)"
                        if node.inside is not None
                        else "#000000",
                    )
                console.print(" ", end="", style=style)
        console.print("\n", end="")


def part1(file_contents: str) -> int:
    grid = parse_file_contents(file_contents)
    coords = [(find_and_fix_start_tile(grid), 0)]
    follow_pipes_and_record_depths(grid, coords)
    return max(node.depth or 0 for row in grid for node in row)


def part2(file_contents: str) -> int:
    grid = parse_file_contents(file_contents)
    coords = [(find_and_fix_start_tile(grid), 0)]
    follow_pipes_and_record_depths(grid, coords)

    for x in range(len(grid)):
        inside = False
        last_corner = None
        for y in range(len(grid[x])):
            node = get_node(grid, (x, y))
            if not node.pipe:
                node.inside = inside
            else:
                if node.char == "|":
                    inside = not inside
                elif last_corner is None:
                    last_corner = node.char
                elif node.char != "-":
                    corners = {last_corner, node.char}
                    if corners == {"F", "J"} or corners == {"7", "L"}:
                        inside = not inside
                    last_corner = None

    print_grid(grid)
    return sum(1 if node.inside else 0 for row in grid for node in row)


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


@pytest.mark.parametrize(
    "data, num_inside_tiles",
    (
        (
            """
        ...........
        .S-------7.
        .|F-----7|.
        .||.....||.
        .||.....||.
        .|L-7.F-J|.
        .|..|.|..|.
        .L--J.L--J.
        ...........
        """,
            4,
        ),
        (
            """
        .F----7F7F7F7F-7....
        .|F--7||||||||FJ....
        .||.FJ||||||||L7....
        FJL7L7LJLJ||LJ.L-7..
        L--J.L7...LJS7F-7L7.
        ....F-J..F7FJ|L7L7L7
        ....L7.F7||L7|.L7L7|
        .....|FJLJ|FJ|F7|.LJ
        ....FJL-7.||.||||...
        ....L---J.LJ.LJLJ...
        """,
            8,
        ),
        (
            """
        FF7FSF7F7F7F7F7F---7
        L|LJ||||||||||||F--J
        FL-7LJLJ||||||LJL-77
        F--JF--7||LJLJ7F7FJ-
        L---JF-JLJ.||-FJLJJ7
        |F|F-JF---7F7-L7L|7|
        |FFJF7L7F-JF7|JL---7
        7-L-JL7||F7|L7F-7F7|
        L.L7LFJ|||||FJL7||LJ
        L7JLJL-JLJLJL--JLJ.L
        """,
            10,
        ),
    ),
)
def test_part2(data, num_inside_tiles):
    assert part2(data) == num_inside_tiles


def test_part2_real():
    assert part2(load_input(__file__)) == 297
