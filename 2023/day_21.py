#!/usr/bin/env python3
import pytest
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

    print(max_x, max_y)

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


def explore_grid(grid, start_coord, until_steps, start_even=True) -> int:
    steps = 0
    even_step_locs = set()
    next_steps = {start_coord}
    visited_steps = set()
    while steps <= until_steps:
        curr_steps = next_steps
        next_steps = set()
        if steps % 2 == (0 if start_even else 1):
            even_step_locs |= curr_steps

        for step in curr_steps:
            visited_steps.add(step)
            for dir in (N, S, W, E):
                next_step = step + dir
                if next_step not in visited_steps and grid.get(next_step, "#") != "#":
                    next_steps.add(next_step)

        steps += 1
        print_grid(grid, even_step_locs, visited_steps)

        # total steps: 26_501_365
        # 131 steps:
        #   1 full centre tile
        #   4 * 1/4 startOdd edge tiles
        # 262 steps:
        #   1 full centre tile
        #   1 * 4 (NWSE) full startOdd edge tiles
        #   1 * 4 (NWSE) 1/4 startEven edge tiles
        #   1 * 4 (NW,NE,SE,SW) 1/2 startEven diagonal tiles
        # 393 steps:
        #   1 full centre tile
        #   1 * 4 (NWSE) full startOdd edge tiles
        #   1 * 4 (NWSE) full startEven edge tiles
        #   1 * 4 (NWSE) 1/4 startOdd edge tiles
        #   1 * 4 (NW,NE,SE,SW) 1/2 startEven diagonal tiles

    print_grid(grid, even_step_locs, visited_steps)
    print(len(even_step_locs))
    #
    # breakpoint()

    return len(even_step_locs)


def part1(file_contents: str, until_steps=64) -> int:
    grid = parse_file_contents(file_contents)
    start_coord = next(coord for coord in grid if grid[coord] == "S")
    print(start_coord)

    return explore_grid(grid, start_coord, until_steps=until_steps)


def part2(file_contents: str, until_steps=26_501_365) -> int:
    grid = parse_file_contents(file_contents)
    start_coord = next(coord for coord in grid if grid[coord] == "S")
    max_x, max_y = max(k[0] for k in grid), max(k[1] for k in grid)
    # print_grid(grid, set(), set())

    # until_steps = 4 * 131 + 65

    assert max_x == max_y
    grid_diameter = max_x + 1
    assert grid_diameter % 2 == 1
    grid_midpoint = (grid_diameter - 1) // 2

    megagrid_diameter = until_steps // grid_diameter
    # if megagrid_diameter == 0:
    return explore_grid(grid, start_coord, until_steps=until_steps)

    print(f"{megagrid_diameter=}")
    # Are the tips of the eventual diamond on even-centred grids?
    tips_even = megagrid_diameter % 2 == 0

    partial_tile_steps = until_steps % grid_diameter

    assert partial_tile_steps == grid_midpoint == 65

    # full_odd_diamonds = list(range(1, megagrid_diameter, 2))
    # full_even_diamonds = list(range(2, megagrid_diameter, 2))
    #
    # print(f"{full_odd_diamonds=}, {full_even_diamonds=}")

    full_odd_diamonds = sum(range(1, megagrid_diameter, 2)) * 4
    full_even_diamonds = sum(range(2, megagrid_diameter, 2)) * 4

    print(f"{full_odd_diamonds=}, {full_even_diamonds=}")

    full_centre_even_tile = explore_grid(grid, start_coord, grid_diameter + 10)
    full_centre_odd_tile = explore_grid(grid, start_coord, grid_diameter + 10, start_even=False)

    start_E_even_tile = explore_grid(grid, (grid_midpoint, max_y), grid_diameter, start_even=tips_even)
    start_W_even_tile = explore_grid(grid, (grid_midpoint, 0), grid_diameter, start_even=tips_even)
    start_N_even_tile = explore_grid(grid, (0, grid_midpoint), grid_diameter, start_even=tips_even)
    start_S_even_tile = explore_grid(grid, (max_x, grid_midpoint), grid_diameter, start_even=tips_even)

    start_SE_3_4_even_tile = explore_grid(grid, (max_x, max_y), grid_diameter + grid_midpoint, start_even=tips_even)
    start_SW_3_4_even_tile = explore_grid(grid, (max_x, 0), grid_diameter + grid_midpoint, start_even=tips_even)
    start_NE_3_4_even_tile = explore_grid(grid, (0, max_y), grid_diameter + grid_midpoint, start_even=tips_even)
    start_NW_3_4_even_tile = explore_grid(grid, (0, 0), grid_diameter + grid_midpoint, start_even=tips_even)

    start_SE_1_4_odd_tile = explore_grid(grid, (max_x, max_y), grid_midpoint, start_even=not tips_even)
    start_SW_1_4_odd_tile = explore_grid(grid, (max_x, 0), grid_midpoint, start_even=not tips_even)
    start_NE_1_4_odd_tile = explore_grid(grid, (0, max_y), grid_midpoint, start_even=not tips_even)
    start_NW_1_4_odd_tile = explore_grid(grid, (0, 0), grid_midpoint, start_even=not tips_even)

    touched_garden_tiles = (
        full_centre_even_tile  # the starting tile
        + (full_odd_diamonds * full_centre_odd_tile)
        + (full_even_diamonds * full_centre_even_tile)
        + (start_E_even_tile + start_S_even_tile + start_W_even_tile + start_N_even_tile)
        + (
            (megagrid_diameter - 1)
            * (start_SE_3_4_even_tile + start_SW_3_4_even_tile + start_NE_3_4_even_tile + start_NW_3_4_even_tile)
        )
        + (
            megagrid_diameter
            * (start_SE_1_4_odd_tile + start_SW_1_4_odd_tile + start_NE_1_4_odd_tile + start_NW_1_4_odd_tile)
        )
    )
    print(touched_garden_tiles)

    return touched_garden_tiles


if __name__ == "__main__":
    # answer1 = part1(load_input(__file__))
    answer2 = part2(load_input(__file__))
    # print(f"The answer is: {answer1=}, {answer2=}")


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


@pytest.mark.parametrize(
    "steps, reached_plots",
    (
        # (6, 16),
        (33, 50),
        # (50, 1594),
        # (100, 6536),
        # (500, 167004),
        # (1000, 668697),
        # (
        #     5000,
        #     (16733044),
        # ),
    ),
)
def test_part2(steps, reached_plots):
    assert (
        part2(
            """
.................................
.....###.#......###.#......###.#.
.###.##..#..###.##..#..###.##..#.
..#.#...#....#.#...#....#.#...#..
....#.#........#.#........#.#....
.##...####..##...####..##...####.
.##..#...#..##..#...#..##..#...#.
.......##.........##.........##..
.##.#.####..##.#.####..##.#.####.
.##..##.##..##..##.##..##..##.##.
.................................
.................................
.....###.#......###.#......###.#.
.###.##..#..###.##..#..###.##..#.
..#.#...#....#.#...#....#.#...#..
....#.#........#.#........#.#....
.##...####..##..S####..##...####.
.##..#...#..##..#...#..##..#...#.
.......##.........##.........##..
.##.#.####..##.#.####..##.#.####.
.##..##.##..##..##.##..##..##.##.
.................................
.................................
.....###.#......###.#......###.#.
.###.##..#..###.##..#..###.##..#.
..#.#...#....#.#...#....#.#...#..
....#.#........#.#........#.#....
.##...####..##...####..##...####.
.##..#...#..##..#...#..##..#...#.
.......##.........##.........##..
.##.#.####..##.#.####..##.#.####.
.##..##.##..##..##.##..##..##.##.
.................................
""",
            until_steps=steps,
        )
        == reached_plots
    )


# def test_part2_real():
#     assert part2(load_input(__file__)) == 0
