#!/usr/bin/env python3


from rich import print

from aoc.ds import t
from helpers import load_input


N = t((-1, 0))
S = t((1, 0))
W = t((0, -1))
E = t((0, 1))


def parse_file_contents(file_contents: str) -> list[str]:
    data = file_contents.splitlines()
    return data


def make_queue(queue, min_length):
    if len(queue) < min_length + 1:
        queue.extend(list() for _ in range(min_length - len(queue) + 1))
    return queue


def part1(file_contents: str) -> int:
    grid = {t((x, y)): int(c) for x, line in enumerate(file_contents.strip().splitlines()) for y, c in enumerate(line)}
    start, end = min(grid), max(grid)
    queue = make_queue([], 10)
    # Queue items are tuples of (coord, from_direction, stride)
    queue[0].append((start, None, 1))
    distance = -1
    visited = {}
    while True:
        distance += 1
        for item in queue[distance]:
            coord, from_direction, stride = item

            if coord == end:
                return distance

            if item in visited and visited[item] < distance:
                continue

            next_directions = (
                (S, E)
                if from_direction is None
                else ((from_direction[1], from_direction[0]), (-from_direction[1], -from_direction[0]))
            )
            for next_direction in next_directions:
                next_coord = coord
                next_distance = distance
                for steps in range(1, 4):
                    next_coord += next_direction
                    if next_coord in grid:
                        next_distance += grid[next_coord]
                        next_item = (next_coord, (-next_direction[0], -next_direction[1]), steps)
                        if next_item not in visited or visited[next_item] > next_distance:
                            make_queue(queue, min_length=next_distance)
                            queue[next_distance].append(next_item)
                            visited[next_item] = next_distance


def part2(file_contents: str) -> int:
    data = parse_file_contents(file_contents)  # noqa
    return 0


if __name__ == "__main__":
    answer1 = part1(load_input(__file__))
    answer2 = part2(load_input(__file__))
    print(f"The answer is: {answer1=}, {answer2=}")


test_data = """
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
"""


def test_part1():
    assert part1(test_data) == 102


def test_part1_real():
    assert part1(load_input(__file__)) == 694


def test_part2():
    assert part2(test_data) == 0


# def test_part2_real():
#     assert part2(load_input(__file__)) == 0
