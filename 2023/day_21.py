#!/usr/bin/env python3


from rich import get_console
from rich.style import Style

from aoc.ds import t
from helpers import load_input


N = t((-1, 0))
S = t((1, 0))
W = t((0, -1))
E = t((0, 1))

console = get_console()
print = console.print


def parse_file_contents(file_contents: str):
    return {(x, y): c for x, line in enumerate(file_contents.strip().splitlines()) for y, c in enumerate(line.strip())}


def print_grid(grid, even_step_locs, visited_step_locs):
    max_x, max_y = max(k[0] for k in grid), max(k[1] for k in grid)

    x = 0
    while x <= max_x:
        y = 0
        while y <= max_y:
            if (x, y) in even_step_locs:
                style = Style(bgcolor="rgb(0, 0, 255)")
            elif (x, y) in visited_step_locs:
                style = Style(bgcolor="rgb(255, 0, 0)")
            else:
                style = Style()

            print(grid[(x, y)], end="", style=style)
            y += 1
        print("")
        x += 1


def part1(file_contents: str, until_steps=64) -> int:
    grid = parse_file_contents(file_contents)
    start_coord = next(coord for coord in grid if grid[coord] == "S")
    print(start_coord)

    steps = 0
    even_step_locs = set()
    next_steps = {start_coord}
    visited_steps = set()
    while steps <= until_steps:
        curr_steps = next_steps
        next_steps = set()
        if steps % 2 == 0:
            even_step_locs |= curr_steps

        for step in curr_steps:
            visited_steps.add(step)
            for dir in (N, S, W, E):
                next_step = step + dir
                if next_step not in visited_steps and grid.get(next_step, "#") != "#":
                    next_steps.add(next_step)

        steps += 1

    print_grid(grid, even_step_locs, visited_steps)

    return len(even_step_locs)


def part2(file_contents: str) -> int:
    data = parse_file_contents(file_contents)  # noqa
    return 0


if __name__ == "__main__":
    answer1 = part1(load_input(__file__))
    answer2 = part2(load_input(__file__))
    print(f"The answer is: {answer1=}, {answer2=}")


test_data = """
...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
"""


def test_part1():
    assert part1(test_data, until_steps=6) == 16


def test_part1_real():
    assert part1(load_input(__file__)) == 3615


def test_part2():
    assert part2(test_data) == 0


# def test_part2_real():
#     assert part2(load_input(__file__)) == 0
