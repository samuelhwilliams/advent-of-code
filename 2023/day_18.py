#!/usr/bin/env python3


from rich import print

from aoc.ds import t
from helpers import load_input


U = t((-1, 0))
D = t((1, 0))
L = t((0, -1))
R = t((0, 1))


def parse_file_contents(file_contents: str):
    for line in file_contents.strip().splitlines():
        direction, distance, colour = line.strip().split(" ")
        yield direction, int(distance), colour[1:-1]


def print_grid(grid):
    print()
    print("\n".join(["".join(c for c in grid[x]) for x in range(len(grid))]))


def has_boundary_below(grid, coord):
    below = coord + D
    if below[0] < len(grid):
        return grid[below[0]][below[1]] == "#"
    return False


def part1(file_contents: str) -> int:
    coord = t((0, 0))
    min_x, max_x, min_y, max_y = 0, 0, 0, 0
    # Work out size of grid
    for direction, distance, colour in parse_file_contents(file_contents):
        coord += globals()[direction] * distance
        min_x, max_x, min_y, max_y = (
            min(min_x, coord[0]),
            max(max_x, coord[0]),
            min(min_y, coord[1]),
            max(max_y, coord[1]),
        )
    start_x, start_y = -min_x, -min_y
    max_x += -min_x
    max_y += -min_y
    grid = [["." for y in range(max_y + 1)] for x in range(max_x + 1)]
    grid[start_x][start_y] = "#"
    coord = t((start_x, start_y))
    # Draw boundary walls
    for direction, distance, colour in parse_file_contents(file_contents):
        for _ in range(distance):
            coord += globals()[direction]
            grid[coord[0]][coord[1]] = "#"

    # Fill inside of boundary walls
    for x in range(len(grid)):
        inside = False

        for y in range(len(grid[x])):
            if grid[x][y] == "#":
                if has_boundary_below(grid, t((x, y))):
                    inside = not inside
            else:
                if inside:
                    grid[x][y] = "#"

    print_grid(grid)

    # Count '#' tiles
    return sum(1 for x in range(len(grid)) for y in range(len(grid[x])) if grid[x][y] == "#")


def part2(file_contents: str) -> int:
    data = parse_file_contents(file_contents)  # noqa
    return 0


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
    assert part2(test_data) == 0


# def test_part2_real():
#     assert part2(load_input(__file__)) == 0
