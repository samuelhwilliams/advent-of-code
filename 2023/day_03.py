#!/usr/bin/env python3

import itertools
import string
from typing import Iterator
from collections import defaultdict

from rich import print

from helpers import load_input


def yield_all_possible_parts_with_boundaries(
    grid: tuple[tuple[str, ...], ...]
) -> Iterator[tuple[int, tuple[int, int], tuple[int, int]]]:
    """Read the entire schematic and yield ((x, y1), (x, y2)) coords pairs encapsulating all possible part numbers"""
    for x, row in enumerate(grid):
        y1 = None
        for y, char in enumerate(row):
            if char.isdigit():
                if y1 is None:
                    # Starting character of a part number
                    y1 = y
            else:
                if y1 is not None:
                    # We've moved beyond the last character of a part number, yield it and its grid co-ords
                    yield int("".join(row[y1:y])), (x, y1), (x, y)
                    y1 = None
        if y1 is not None:
            # We've moved beyond the last character of a part number, yield it and its grid co-ords
            yield int("".join(row[y1 : y + 1])), (x, y1), (x, y)


def get_part_border_coords(x, y1, y2) -> Iterator[tuple[int, int]]:
    return itertools.chain(
        [(x - 1, y) for y in range(y1 - 1, y2 + 1)],
        [(x, y1 - 1)],
        [(x, y2)],
        [(x + 1, y) for y in range(y1 - 1, y2 + 1)],
    )


def yield_valid_parts(
    grid, parts_with_boundaries: Iterator[tuple[int, tuple[int, int], tuple[int, int]]]
) -> Iterator[int]:
    """
    Take a list of (part_num, (x, y1), (x, y2)) entries and check if any of its border coords is a non-period symbol.
    """
    symbols = set(string.punctuation)
    symbols.remove(".")

    for part_number, start, stop in parts_with_boundaries:  # type: int, tuple[int, int], tuple[int, int]
        for x, y in get_part_border_coords(start[0], start[1], stop[1]):
            if 0 <= x < len(grid) and 0 <= y < len(grid[x]):
                if grid[x][y] in symbols:
                    yield part_number
                    break


def make_grid(schematic: str) -> tuple[tuple[str, ...], ...]:
    return tuple([tuple([char for char in line.strip()]) for line in schematic.strip().split("\n")])


def part1(schematic: str):
    grid = make_grid(schematic)
    all_part_numbers = [
        part_number for part_number in yield_valid_parts(grid, yield_all_possible_parts_with_boundaries(grid))
    ]
    return sum(all_part_numbers)


def part2(schematic):
    grid = make_grid(schematic)
    gear_coords_to_part_numbers = defaultdict(list)

    for part_number, start, stop in yield_all_possible_parts_with_boundaries(grid):
        for x, y in get_part_border_coords(start[0], start[1], stop[1]):
            if 0 <= x < len(grid) and 0 <= y < len(grid[x]):
                if grid[x][y] == "*":
                    gear_coords_to_part_numbers[(x, y)].append(part_number)

    return sum(
        part_numbers[0] * part_numbers[1]
        for part_numbers in gear_coords_to_part_numbers.values()
        if len(part_numbers) == 2
    )


if __name__ == "__main__":
    data = load_input(__file__)
    answer1, answer2 = part1(data), part2(data)
    print(f"Answer is: {answer1=}, {answer2=}")


data = """
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""


def test_part1_make_grid():
    assert make_grid(data) == (
        ("4", "6", "7", ".", ".", "1", "1", "4", ".", "."),
        (".", ".", ".", "*", ".", ".", ".", ".", ".", "."),
        (".", ".", "3", "5", ".", ".", "6", "3", "3", "."),
        (".", ".", ".", ".", ".", ".", "#", ".", ".", "."),
        ("6", "1", "7", "*", ".", ".", ".", ".", ".", "."),
        (".", ".", ".", ".", ".", "+", ".", "5", "8", "."),
        (".", ".", "5", "9", "2", ".", ".", ".", ".", "."),
        (".", ".", ".", ".", ".", ".", "7", "5", "5", "."),
        (".", ".", ".", "$", ".", "*", ".", ".", ".", "."),
        (".", "6", "6", "4", ".", "5", "9", "8", ".", "."),
    )


def test_part1_yield_all_possible_parts_with_boundaries():
    assert list(yield_all_possible_parts_with_boundaries(make_grid(data))) == [
        (467, (0, 0), (0, 3)),
        (114, (0, 5), (0, 8)),
        (35, (2, 2), (2, 4)),
        (633, (2, 6), (2, 9)),
        (617, (4, 0), (4, 3)),
        (58, (5, 7), (5, 9)),
        (592, (6, 2), (6, 5)),
        (755, (7, 6), (7, 9)),
        (664, (9, 1), (9, 4)),
        (598, (9, 5), (9, 8)),
    ]


def test_part1_yield_valid_parts():
    grid = (
        ("1", "2", "3"),
        (".", ".", "*"),
        ("8", ".", "!"),
        (".", ".", "7"),
    )
    assert list(
        yield_valid_parts(
            grid,
            (
                (123, (0, 0), (0, 3)),
                (7, (3, 2), (3, 3)),
            ),
        )
    ) == [123, 7]


def test_part1_e2e():
    assert part1(data) == 4361


def test_part2():
    assert part2(data) == (467 * 35 + 755 * 598)
