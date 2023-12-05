#!/usr/bin/env python3
import dataclasses

from rich import print

from helpers import load_input


@dataclasses.dataclass
class AlmanacMap:
    entries: list["AlmanacEntry"]

    def lookup(self, number):
        for entry in self.entries:
            if entry.source_start <= number <= entry.source_end:
                offset = number - entry.source_start
                return entry.destination_start + offset

        return number


@dataclasses.dataclass
class AlmanacEntry:
    source_start: int
    destination_start: int
    length: int


def parse_almanac(file_contents: str) -> tuple[list[int], list[AlmanacMap]]:
    paragraphs = file_contents.strip().split("\n\n")
    seeds = [int(seed) for seed in paragraphs[0][7:].split(" ")]

    almanac_maps = []
    for section in paragraphs[1:]:
        entries = []
        for entry in section.splitlines()[1:]:
            destination_start, source_start, length = [int(x) for x in entry.split(" ")]
            entries.append(AlmanacEntry(source_start=source_start, destination_start=destination_start, length=length))
        almanac_maps.append(AlmanacMap(entries=sorted(entries, key=lambda entry: entry.source_start)))

    return seeds, almanac_maps


def part1(file_contents: str) -> int:
    seeds, almanac_maps = parse_almanac(file_contents)

    locations = []
    for seed in seeds:
        lookup = seed
        for almanac_map in almanac_maps:
            lookup = almanac_map.lookup(lookup)
        locations.append(lookup)

    return min(locations)


def part2(file_contents: str) -> int:
    return 0


if __name__ == "__main__":
    data = load_input(__file__)
    answer1 = part1(data)
    answer2 = part2(data)
    print(f"The answer is: {answer1=}, {answer2=}")


test_data = """
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""


def test_part1():
    assert part1(test_data) == 35


def test_part2():
    assert part2(test_data) == 0
