#!/usr/bin/env python3

from part1 import yield_games, yield_cubedraws, yield_cubesets


def calculate_game_power(game_cubedraws: str) -> int:
    min_cubes_for_game = {"red": 0, "green": 0, "blue": 0}

    for cubedraw in yield_cubedraws(game_cubedraws):
        for cube_count, cube_colour in yield_cubesets(cubedraw):
            if min_cubes_for_game[cube_colour] < cube_count:
                min_cubes_for_game[cube_colour] = cube_count

    return min_cubes_for_game["red"] * min_cubes_for_game["green"] * min_cubes_for_game["blue"]


def sum_possible_games(lines: list[str]) -> int:
    return sum(calculate_game_power(game_cubedraws) for game_id, game_cubedraws in yield_games(lines))


if __name__ == "__main__":
    f = open("input/input.txt").read()
    answer = sum_possible_games(f.splitlines())
    print(f"Answer is: {answer}")
