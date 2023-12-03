#!/usr/bin/env python3
import itertools
import string
from typing import Iterator


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


def sum_engine_parts(schematic: str):
    grid = make_grid(schematic)
    all_part_numbers = [
        part_number for part_number in yield_valid_parts(grid, yield_all_possible_parts_with_boundaries(grid))
    ]
    return sum(all_part_numbers)


if __name__ == "__main__":
    data = open("input/input.txt").read()
    answer = sum_engine_parts(data)
    print(f"Answer is: {answer}")
