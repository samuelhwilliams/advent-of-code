#!/usr/bin/env python3


from rich import print


def part1(file_contents: str) -> int:
    return 0


def part2(file_contents: str) -> int:
    return 0


if __name__ == "__main__":
    with open("input.txt") as f:
        data = f.read()

    answer1 = part1(data)
    answer2 = part2(data)

    print(f"The answer is: {answer1=}, {answer2=}")
