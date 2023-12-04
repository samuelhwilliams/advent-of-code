#!/usr/bin/env python3

from rich import print
from typing import Iterable

from helpers import load_input


def yield_games(lines: list[str]) -> Iterable[tuple[int, str]]:
    for line in lines:
        game, game_cubedraws = line.split(":")
        game_id = int(game[5:])
        yield game_id, game_cubedraws


def yield_cubedraws(game_cubedraws: str) -> Iterable[str]:
    for cubedraw in game_cubedraws.split(";"):
        yield cubedraw


def yield_cubesets(cubedraw: str) -> Iterable[tuple[int, str]]:
    for cubeset in cubedraw.split(","):
        cube_count, cube_colour = cubeset.strip().split()
        yield int(cube_count), cube_colour


def is_game_possible(game_cubedraws: str) -> bool:
    available_cubes = {"red": 12, "green": 13, "blue": 14}

    return all(
        all(
            available_cubes.get(cube_colour, 0) >= int(cube_count)
            for cube_count, cube_colour in yield_cubesets(cubedraw)
        )
        for cubedraw in yield_cubedraws(game_cubedraws)
    )


def part1(lines: list[str]) -> int:
    return sum(game_id if is_game_possible(game_cubedraws) else 0 for game_id, game_cubedraws in yield_games(lines))


def calculate_game_power(game_cubedraws: str) -> int:
    min_cubes_for_game = {"red": 0, "green": 0, "blue": 0}

    for cubedraw in yield_cubedraws(game_cubedraws):
        for cube_count, cube_colour in yield_cubesets(cubedraw):
            if min_cubes_for_game[cube_colour] < cube_count:
                min_cubes_for_game[cube_colour] = cube_count

    return min_cubes_for_game["red"] * min_cubes_for_game["green"] * min_cubes_for_game["blue"]


def part2(lines: list[str]) -> int:
    return sum(calculate_game_power(game_cubedraws) for game_id, game_cubedraws in yield_games(lines))


if __name__ == "__main__":
    data = load_input(__file__).strip().splitlines()
    answer1, answer2 = part1(data), part2(data)
    print(f"Answer is: {answer1=}, {answer2=}")


data = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""


def test_part1():
    assert part1(data.splitlines()) == 8


def test_part2():
    assert part2(data.splitlines()) == 2286
