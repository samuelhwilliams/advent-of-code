#!/usr/bin/env python3
import dataclasses
import enum
from itertools import combinations
from typing import Optional

import pytest
from rich import get_console
from rich.style import Style

from helpers import load_input


console = get_console()


@dataclasses.dataclass
class Node:
    char: str
    depth: Optional[int] = None
    inside: Optional[bool] = None
    walked: bool = False

    @property
    def pipe(self):
        return self.depth is not None


def print_grid(grid: list[list[Node]], max_depth: int = 10_000, cur_coord: Optional[tuple[int, int]] = None):
    for x, row in enumerate(grid):
        for y, node in enumerate(row):
            if node.depth is not None:
                gradient = min(128, node.depth * 128 // max_depth)
                if cur_coord and cur_coord == (x, y):
                    style = Style(color="white", bgcolor="green", blink=True, blink2=True)
                elif node.walked:
                    style = Style(bgcolor="yellow")
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
                        else "rgb(255, 0, 255)"
                        if node.inside is not None
                        else "#000000",
                    )
                console.print(" ", end="", style=style)
        console.print("\n", end="")


def parse_file_contents(file_contents: str) -> list[list[Node]]:
    data = [[Node(c) for c in line.strip()] for line in file_contents.strip().splitlines()]
    for row in data:
        row.insert(0, Node("."))
        row.append(Node("."))
    width = len(data[0])
    data.insert(0, [Node(".") for _ in range(width)])
    data.append([Node(".") for _ in range(width)])
    return data


def get_starting_coord(grid):
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            if grid[x][y].char == "S":
                return x, y


def flood_fill_depths(grid: list[list[Node]], queue: list[tuple[tuple[int, int], int]]) -> int:
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

        if any(x == y for x, y in combinations([above.depth, left.depth, right.depth, below.depth], 2)):
            loops.add(depth)

        i += 1

    return max(loops)


def part1(file_contents: str) -> int:
    grid = parse_file_contents(file_contents)
    coords = [(get_starting_coord(grid), 0)]
    return flood_fill_depths(grid, coords)


class Direction(enum.Enum):
    ABOVE = (-1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)
    BELOW = (1, 0)

    def opposite(self):
        return Direction((self.value[0] * -1, self.value[1] * -1))


def get_node(grid: list[list[Node]], coord: tuple[int, int]) -> Node:
    return grid[coord[0]][coord[1]]


def get_adjacent_coord(coord: tuple[int, int], direction: Direction) -> tuple[int, int]:
    return coord[0] + direction.value[0], coord[1] + direction.value[1]


def next_step(
    grid, coord: tuple[int, int], from_direction: Direction, inside_direction: Direction
) -> tuple[tuple[int, int], Direction, Direction]:
    node = get_node(grid, coord)
    node.walked = True

    if node.char == "-" and from_direction in {Direction.LEFT, Direction.RIGHT}:
        next_direction = from_direction.opposite()
    elif node.char == "|" and from_direction in {Direction.ABOVE, Direction.BELOW}:
        next_direction = from_direction.opposite()
    else:
        if from_direction == Direction.LEFT:
            assert inside_direction in {Direction.ABOVE, Direction.BELOW}
            if node.char == "7":
                next_direction = Direction.BELOW
                inside_direction = Direction.RIGHT if inside_direction == Direction.ABOVE else Direction.LEFT
            else:  # J
                next_direction = Direction.ABOVE
                inside_direction = Direction.LEFT if inside_direction == Direction.ABOVE else Direction.RIGHT

        elif from_direction == Direction.ABOVE:
            assert inside_direction in {Direction.LEFT, Direction.RIGHT}
            if node.char == "J":
                next_direction = Direction.LEFT
                inside_direction = Direction.ABOVE if inside_direction == Direction.LEFT else Direction.BELOW
            else:  # L
                next_direction = Direction.RIGHT
                inside_direction = Direction.BELOW if inside_direction == Direction.LEFT else Direction.ABOVE

        elif from_direction == Direction.RIGHT:
            assert inside_direction in {Direction.ABOVE, Direction.BELOW}
            if node.char == "L":
                next_direction = Direction.ABOVE
                inside_direction = Direction.RIGHT if inside_direction == Direction.ABOVE else Direction.LEFT
            else:  # F
                next_direction = Direction.BELOW
                inside_direction = Direction.LEFT if inside_direction == Direction.ABOVE else Direction.RIGHT

        elif from_direction == Direction.BELOW:
            assert inside_direction in {Direction.LEFT, Direction.RIGHT}
            if node.char == "7":
                next_direction = Direction.LEFT
                inside_direction = Direction.BELOW if inside_direction == Direction.LEFT else Direction.ABOVE
            else:  # F
                next_direction = Direction.RIGHT
                inside_direction = Direction.ABOVE if inside_direction == Direction.LEFT else Direction.BELOW

        else:
            raise RuntimeError("ohno")

    return get_adjacent_coord(coord, next_direction), next_direction.opposite(), inside_direction


def mark_and_fill(grid, queue: list[tuple[int, int]], inside: bool) -> int:
    marked = 0
    while queue:
        coord = queue.pop()
        if coord[0] < 0 or coord[0] >= len(grid) or coord[1] < 0 or coord[1] >= len(grid[0]):
            continue
        node = get_node(grid, coord)
        if node.depth is not None or node.inside is not None:
            continue

        node.inside = inside
        marked += 1

        for adjacent in [Direction.ABOVE, Direction.LEFT, Direction.RIGHT, Direction.BELOW]:
            adjacent_coord = get_adjacent_coord(coord, adjacent)
            if (
                adjacent_coord[0] < 0
                or adjacent_coord[0] >= len(grid)
                or adjacent_coord[1] < 0
                or adjacent_coord[1] >= len(grid[0])
            ):
                continue

            adjacent_node = get_node(grid, adjacent_coord)
            if adjacent_node and adjacent_node.depth is None and adjacent_node.inside is None:
                queue.append(adjacent_coord)

    return marked


def mark_nodes_inside_or_outside(grid, coord: tuple[int, int], from_direction: Direction, inside_direction: Direction):
    queue = [get_adjacent_coord(coord, inside_direction)]
    mark_and_fill(grid, queue, inside=True)

    queue = [get_adjacent_coord(coord, inside_direction.opposite())]
    mark_and_fill(grid, queue, inside=False)

    node = get_node(grid, coord)
    if from_direction == Direction.LEFT:
        if node.char == "7":
            queue = [get_adjacent_coord(coord, Direction.ABOVE), get_adjacent_coord(coord, Direction.RIGHT)]
            mark_and_fill(grid, queue, inside=inside_direction != Direction.BELOW)
        elif node.char == "J":
            queue = [get_adjacent_coord(coord, Direction.BELOW), get_adjacent_coord(coord, Direction.RIGHT)]
            mark_and_fill(grid, queue, inside=inside_direction != Direction.ABOVE)
    elif from_direction == Direction.RIGHT:
        if node.char == "F":
            queue = [get_adjacent_coord(coord, Direction.ABOVE), get_adjacent_coord(coord, Direction.LEFT)]
            mark_and_fill(grid, queue, inside=inside_direction != Direction.BELOW)
        elif node.char == "L":
            queue = [get_adjacent_coord(coord, Direction.BELOW), get_adjacent_coord(coord, Direction.LEFT)]
            mark_and_fill(grid, queue, inside=inside_direction != Direction.ABOVE)

    elif from_direction == Direction.ABOVE:
        if node.char == "L":
            queue = [get_adjacent_coord(coord, Direction.BELOW), get_adjacent_coord(coord, Direction.LEFT)]
            mark_and_fill(grid, queue, inside=inside_direction != Direction.RIGHT)
        elif node.char == "J":
            queue = [get_adjacent_coord(coord, Direction.BELOW), get_adjacent_coord(coord, Direction.LEFT)]
            mark_and_fill(grid, queue, inside=inside_direction != Direction.LEFT)

    elif from_direction == Direction.BELOW:
        if node.char == "F":
            queue = [get_adjacent_coord(coord, Direction.ABOVE), get_adjacent_coord(coord, Direction.LEFT)]
            mark_and_fill(grid, queue, inside=inside_direction != Direction.RIGHT)
        elif node.char == "7":
            queue = [get_adjacent_coord(coord, Direction.ABOVE), get_adjacent_coord(coord, Direction.LEFT)]
            mark_and_fill(grid, queue, inside=inside_direction != Direction.LEFT)


def count_inside_tiles(grid, start: tuple[int, int], max_depth: int) -> int:
    from_direction = Direction.LEFT
    inside_direction = Direction.BELOW
    next_coord = (start[0], start[1] + 1)
    i = 0
    while next_coord != start:
        mark_nodes_inside_or_outside(grid, next_coord, from_direction=from_direction, inside_direction=inside_direction)
        next_coord, from_direction, inside_direction = next_step(
            grid, next_coord, from_direction=from_direction, inside_direction=inside_direction
        )
        i += 1

    print_grid(grid, max_depth=max_depth)

    return sum([1 if node.inside else 0 for row in grid for node in row])


def replace_start_with_pipe(grid: list[list[Node]]):
    for x, row in enumerate(grid):
        for y, node in enumerate(grid[x]):
            if node.char == "S":
                above, left, right, below = (
                    get_node(grid, get_adjacent_coord((x, y), Direction.ABOVE)),
                    get_node(grid, get_adjacent_coord((x, y), Direction.LEFT)),
                    get_node(grid, get_adjacent_coord((x, y), Direction.RIGHT)),
                    get_node(grid, get_adjacent_coord((x, y), Direction.BELOW)),
                )
                above_chars = {"|", "F", "7"}
                left_chars = {"-", "F", "L"}
                right_chars = {"-", "7", "J"}
                below_chars = {"|", "J", "L"}
                if above.char in above_chars and left.char in left_chars:
                    node.char = "J"
                elif above.char in above_chars and right.char in right_chars:
                    node.char = "L"
                elif above.char in above_chars and below.char in below_chars:
                    node.char = "|"
                elif left.char in left_chars and right.char in right_chars:
                    node.char = "-"
                elif left.char in left_chars and below.char in below_chars:
                    node.char = "7"
                elif below.char in below_chars and right.char in right_chars:
                    node.char = "F"


def part2(file_contents: str) -> int:
    grid = parse_file_contents(file_contents)
    coords = [(get_starting_coord(grid), 0)]
    max_depth = flood_fill_depths(grid, coords)
    replace_start_with_pipe(grid)

    for x in range(len(grid)):
        for y in range(len(grid[x])):
            if grid[x][y].pipe:
                return count_inside_tiles(grid, start=(x, y), max_depth=max_depth)
            else:
                grid[x][y].inside = False

    raise RuntimeError("didn't find edge")


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
