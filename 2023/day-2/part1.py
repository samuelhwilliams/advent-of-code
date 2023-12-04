#!/usr/bin/env python3

from typing import Iterable


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


def sum_possible_games(lines: list[str]) -> int:
    return sum(game_id if is_game_possible(game_cubedraws) else 0 for game_id, game_cubedraws in yield_games(lines))


if __name__ == "__main__":
    f = open("input/input.txt").read()
    answer = sum_possible_games(f.splitlines())
    print(f"Answer is: {answer}")
