#!/usr/bin/env python3
import dataclasses
import itertools

from ordered_set import OrderedSet
from rich import print

from helpers import load_input, parse_grid


@dataclasses.dataclass
class Node:
    char: str
    beams: OrderedSet[tuple[int, int]] = dataclasses.field(default_factory=OrderedSet)

    def reset(self):
        self.beams = OrderedSet()


NORTH = (-1, 0)
SOUTH = (1, 0)
WEST = (0, -1)
EAST = (0, 1)


@dataclasses.dataclass
class BeamTip:
    coord: tuple
    direction: tuple

    def move(self):
        return BeamTip((self.coord[0] + self.direction[0], self.coord[1] + self.direction[1]), self.direction)

    def flip(self, char):
        if char not in "\\/":
            return

        if self.direction is EAST:
            self.direction = NORTH if char == "/" else SOUTH
        elif self.direction is WEST:
            self.direction = NORTH if char == "\\" else SOUTH
        elif self.direction is NORTH:
            self.direction = EAST if char == "/" else WEST
        else:
            self.direction = EAST if char == "\\" else WEST


def parse_file_contents(file_contents: str) -> list[list[Node]]:
    grid = parse_grid(file_contents, tile_class=Node)
    return grid


def energise_grid(grid, beams):
    while beams:
        if (
            beams[0].coord[0] < 0
            or beams[0].coord[0] >= len(grid)
            or beams[0].coord[1] < 0
            or beams[0].coord[1] >= len(grid[0])
        ):
            beams.pop(0)
            continue

        tile = grid[beams[0].coord[0]][beams[0].coord[1]]
        if beams[0].direction in tile.beams:
            beams.pop(0)
            continue

        tile.beams.add(beams[0].direction)
        match tile.char:
            case "|" if beams[0].direction[0] == 0:
                beams[0].direction = NORTH
                beams.append(BeamTip(beams[0].coord + SOUTH, SOUTH))
            case "-" if beams[0].direction[1] == 0:
                beams[0].direction = WEST
                beams.append(BeamTip(beams[0].coord + EAST, EAST))
            case "/" | "\\":
                beams[0].flip(tile.char)

        beams[0] = beams[0].move()

    return sum(1 for x in range(len(grid)) for y in range(len(grid[0])) if grid[x][y].beams)


def part1(file_contents: str) -> int:
    grid = parse_file_contents(file_contents)
    return energise_grid(grid, [BeamTip((0, 0), EAST)])


def reset_grid(grid):
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            grid[x][y].reset()


def part2(file_contents: str) -> int:
    max_energy = 0
    grid = parse_file_contents(file_contents)
    for x, y, direction in itertools.chain(
        itertools.product(range(len(grid)), [0], [EAST]),
        itertools.product(range(len(grid)), [len(grid[0]) - 1], [WEST]),
        itertools.product([0], range(len(grid[0])), [SOUTH]),
        itertools.product([len(grid) - 1], range(len(grid[0])), [NORTH]),
    ):
        beams = [BeamTip((x, y), direction)]
        max_energy = max(max_energy, energise_grid(grid, beams))
        reset_grid(grid)

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
