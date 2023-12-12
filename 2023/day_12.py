#!/usr/bin/env python3
import re

from rich import print

from helpers import load_input


def parse_file_contents(file_contents: str) -> list[list[str, list[int]]]:
    data = [
        [line.strip().split(" ")[0], list(map(int, line.strip().split(" ")[1].split(",")))]
        for line in file_contents.strip().splitlines()
    ]
    return data


def all_unknown_combinations(report: str):
    if "?" not in report:
        yield report

    else:
        yield from all_unknown_combinations(report.replace("?", "#", 1))
        yield from all_unknown_combinations(report.replace("?", ".", 1))


def count_valid_groups(original_report, spring_groups):
    count = 0

    for i, report in enumerate(all_unknown_combinations(original_report)):
        if [len(group) for group in filter(lambda x: x, re.split(r"\.+", report))] == spring_groups:
            count += 1

    return count


def part1(file_contents: str) -> int:
    data = parse_file_contents(file_contents)
    return sum(count_valid_groups(report, spring_groups) for report, spring_groups in data)


def part2(file_contents: str) -> int:
    parse_file_contents(file_contents)
    return 0


if __name__ == "__main__":
    data = load_input(__file__)
    answer1 = part1(data)
    answer2 = part2(data)
    print(f"The answer is: {answer1=}, {answer2=}")


test_data = """
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""


def test_part1():
    assert part1(test_data) == 21


def test_part2():
    assert part2(test_data) == 0
