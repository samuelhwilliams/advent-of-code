#!/usr/bin/env python3
import functools
import re

from rich import print

from helpers import load_input


def parse_file_contents(file_contents: str, part2: bool = False) -> tuple[tuple[str, tuple[int, ...]], ...]:
    data = []

    for line in file_contents.strip().splitlines():
        report, spring_groups = line.strip().split(" ")  # type: str, str

        if part2 is False:
            data.append((report, tuple(map(int, spring_groups.split(",")))))
        else:
            data.append(("?".join([report] * 5), tuple(map(int, spring_groups.split(","))) * 5))

    return tuple(data)


def all_unknown_combinations(report: str):
    if "?" not in report:
        yield report

    else:
        yield from all_unknown_combinations(report.replace("?", "#", 1))
        yield from all_unknown_combinations(report.replace("?", ".", 1))


def count_valid_groups(original_report, spring_groups):
    count = 0

    for i, report in enumerate(all_unknown_combinations(original_report)):
        if tuple([len(group) for group in filter(lambda x: x, re.split(r"\.+", report))]) == spring_groups:
            count += 1

    return count


def part1(file_contents: str) -> int:
    data = parse_file_contents(file_contents)
    return sum(count_valid_groups(report, spring_groups) for report, spring_groups in data)


@functools.cache
def recurse_reports(report, spring_groups):
    if len(spring_groups) == 0:
        return 0 if "#" in report else 1

    total = 0
    min_length_required = sum(spring_groups) + len(spring_groups) - 1
    for i in range(0, len(report) - min_length_required + 1):
        if i > 0 and report[i - 1] == "#":
            break

        if "." not in report[i : i + spring_groups[0]]:
            if i + spring_groups[0] == len(report) and len(spring_groups) == 1:
                total += 1
            elif report[i + spring_groups[0]] != "#":
                total += recurse_reports(report[i + spring_groups[0] + 1 :], spring_groups[1:])

    return total


def part2(file_contents: str) -> int:
    data = parse_file_contents(file_contents, part2=True)
    return sum(recurse_reports(report, spring_groups) for report, spring_groups in data)


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
    assert part2(test_data) == 525152
