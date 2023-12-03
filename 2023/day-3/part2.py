#!/usr/bin/env python3
from collections import defaultdict

from part1 import make_grid, yield_all_possible_parts_with_boundaries, get_part_border_coords


def sum_gear_ratios(schematic):
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
    data = open("input/input.txt").read()
    answer = sum_gear_ratios(data)
    print(f"Answer is: {answer}")
