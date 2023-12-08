#!/usr/bin/env python3
import functools
import itertools
import math
import re

from frozendict import frozendict
from rich import print

from helpers import load_input


def parse_file(file_contents: str) -> tuple[str, frozendict[str, tuple[str, str]]]:
    lines = file_contents.strip().splitlines()
    directions = lines[0].strip()
    node_map: frozendict[str, tuple[str, str]] = frozendict(
        {nodes[0]: (nodes[1], nodes[2]) for nodes in map(lambda line: re.findall(r"[A-Z0-9]{3}", line), lines[2:])}
    )
    return directions, node_map


def part1(file_contents: str) -> int:
    directions, node_map = parse_file(file_contents)
    cycle = itertools.cycle(directions)
    steps = 0
    curloc = "AAA"
    while curloc != "ZZZ":
        dir = 0 if next(cycle) == "L" else 1
        curloc = node_map[curloc][dir]
        steps += 1

    return steps


@functools.cache
def find_next_z(
    start_location: str, node_map: dict[str, tuple[str, str]], steps: int, directions: str
) -> tuple[str, int]:
    """Returns the next location ending with Z, and the number of steps taken to get there."""
    delta_steps = 0
    next_location = start_location
    while delta_steps == 0 or not next_location.endswith("Z"):
        next_direction = 0 if directions[(steps + delta_steps) % len(directions)] == "L" else 1
        next_location = node_map[next_location][next_direction]
        # print(f"{from_location=} to {next_location=} via {next_direction=} on {steps+delta_steps=}")
        # time.sleep(0.5)
        delta_steps += 1

    # print(f"Found path from {start_location} to {next_location} in {delta_steps} steps")
    return next_location, delta_steps


def part2(file_contents: str) -> int:
    directions, node_map = parse_file(file_contents)
    current_locations = [node for node in node_map.keys() if node.endswith("A")]
    steps_to_location = [0] * len(current_locations)
    for i, current_location in enumerate(current_locations):
        next_location, delta_steps = find_next_z(current_location, node_map=node_map, steps=0, directions=directions)
        current_locations[i] = next_location
        steps_to_location[i] += delta_steps

    # It just so happens to be a fact that, once you reach an end location, the input loops you back to that location
    # in exactly the same number of steps as required to find that end location in the first place. If we rely on that
    # this essentially just becomes a case of 'find the lowest common multiple'.
    #
    # To work this out, I left the below code to run for a while, and it stopped spitting out new paths.
    # When I compared the a-z and z-z paths it became apparent that each a went to a unique z, and each z looped back
    # to itself. So I can just short circuit all of this logic...

    # print(steps_to_location)
    # while not len(set(steps_to_location)) == 1:
    #     min_steps = min(steps_to_location)
    #     # print(f"{min_steps=}")
    #     for i, current_location in enumerate(current_locations):
    #         if steps_to_location[i] == min_steps:
    #             # print(f"finding next for {current_location=} at {min_steps=}")
    #             next_location, delta_steps = find_next_z(
    #                 current_location, node_map=node_map, steps=min_steps % len(directions), directions=directions
    #             )
    #             current_locations[i] = next_location
    #             steps_to_location[i] += delta_steps

    return math.lcm(*steps_to_location)


if __name__ == "__main__":
    data = load_input(__file__)
    answer1 = part1(data)
    answer2 = part2(data)
    print(f"The answer is: {answer1=}, {answer2=}")


test_data = """
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
"""


def test_part1():
    assert part1(test_data) == 2


test_data_part2 = """
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
"""


def test_part2():
    assert part2(test_data_part2) == 6
