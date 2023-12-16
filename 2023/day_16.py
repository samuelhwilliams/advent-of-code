#!/usr/bin/env python3
import itertools

from rich import print

from helpers import load_input


NORTH = (-1, 0)
SOUTH = (1, 0)
WEST = (0, -1)
EAST = (0, 1)


def energise_grid(grid, beams):
    visited = set()
    while beams:
        coord, direction = beams[0]
        new_direction = direction

        if coord not in grid:
            beams.pop(0)
            continue

        if (coord, direction) in visited:
            beams.pop(0)
            continue

        visited.add((coord, direction))
        match grid[coord]:
            case "|" if direction[0] == 0:
                new_direction = NORTH
                beams.append(((beams[0][0][0] + SOUTH[0], beams[0][0][1] + SOUTH[1]), SOUTH))
            case "-" if direction[1] == 0:
                new_direction = WEST
                beams.append(((beams[0][0][0] + EAST[0], beams[0][0][1] + EAST[1]), EAST))
            case "/":
                new_direction = (-direction[1], -direction[0])
            case "\\":
                new_direction = (direction[1], direction[0])

        beams[0] = ((coord[0] + new_direction[0], coord[1] + new_direction[1]), new_direction)

    return len(set(coord for coord, direction in visited))


def part1(file_contents: str) -> int:
    lines = file_contents.strip().splitlines()
    grid = {(x, y): c for x, line in enumerate(lines) for y, c in enumerate(line)}
    return energise_grid(grid, [((0, 0), EAST)])


def part2(file_contents: str) -> int:
    max_energy = 0
    lines = file_contents.strip().splitlines()
    m, n = len(lines), len(lines[0])
    grid = {(x, y): c for x, line in enumerate(lines) for y, c in enumerate(line)}

    for x, y, direction in itertools.chain(
        itertools.product(range(m), [0], [EAST]),
        itertools.product(range(m), [n - 1], [WEST]),
        itertools.product([0], range(n), [SOUTH]),
        itertools.product([m - 1], range(n), [NORTH]),
    ):
        max_energy = max(max_energy, energise_grid(grid, [((x, y), direction)]))

    return max_energy


if __name__ == "__main__":
    answer1 = part1(load_input(__file__))
    answer2 = part2(load_input(__file__))
    print(f"The answer is: {answer1=}, {answer2=}")


test_data = r"""
.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
"""


def test_part1():
    assert part1(test_data) == 46


def test_part1_real():
    assert part1(load_input(__file__)) == 8249


def test_part2():
    assert part2(test_data) == 51


def test_part2_real():
    assert part2(load_input(__file__)) == 8444
