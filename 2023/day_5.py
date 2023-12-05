#!/usr/bin/env python3
import dataclasses
import sys
from typing import Optional

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

    @property
    def source_end(self) -> int:
        return self.source_start + self.length - 1

    @property
    def destination_end(self) -> int:
        return self.destination_start + self.length - 1

    @property
    def offset(self) -> int:
        return self.destination_start - self.source_start


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


# --------- PART 2 ---------------


@dataclasses.dataclass
class RangedAlmanac:
    maps: list["RangedAlmanacMap"]

    def lookup_smallest_location_for_range(self, r: "Range"):
        map_ranges = [r]
        for i, almanac_map in enumerate(self.maps):
            map_ranges = almanac_map.lookup(map_ranges)

        return min(r.first for r in map_ranges)


@dataclasses.dataclass
class Range:
    first: int
    last: int


@dataclasses.dataclass
class RangedAlmanacMap(AlmanacMap):
    def __post_init__(self):
        # Add a catch-all entry for numbers that aren't in explicit ranges
        self.entries.append(AlmanacEntry(source_start=0, destination_start=0, length=sys.maxsize))

    def _overlay_ranges(self, unmapped_range: Range, entry: AlmanacEntry) -> tuple[Optional[Range], list[Range]]:
        """Returns (mapped_range, [unmapped_range, ...]"""
        mapped, unmapped = None, []
        if unmapped_range.first > entry.source_end or unmapped_range.last < entry.source_start:
            unmapped.append(unmapped_range)

        elif unmapped_range.first >= entry.source_start and unmapped_range.last <= entry.source_end:
            mapped = Range(first=unmapped_range.first + entry.offset, last=unmapped_range.last + entry.offset)

        elif unmapped_range.first < entry.source_start and unmapped_range.last > entry.source_end:
            mapped = Range(first=entry.source_start + entry.offset, last=entry.source_end + entry.offset)
            unmapped.append(Range(first=unmapped_range.first, last=entry.source_start - 1))
            unmapped.append(Range(first=entry.source_end + 1, last=unmapped_range.last))

        elif unmapped_range.first < entry.source_start:
            mapped = Range(first=entry.source_start + entry.offset, last=unmapped_range.last + entry.offset)
            unmapped.append(Range(first=unmapped_range.first, last=entry.source_start - 1))

        elif unmapped_range.last > entry.source_end:
            mapped = Range(first=unmapped_range.first + entry.offset, last=entry.source_end + entry.offset)
            unmapped.append(Range(first=entry.source_end + 1, last=unmapped_range.last))

        return mapped, unmapped

    def lookup(self, unmapped_ranges: list[Range]) -> list[Range]:
        mapped_ranges = []

        ranges_to_check = unmapped_ranges.copy()
        while ranges_to_check:
            mapped, unmapped = None, [ranges_to_check.pop()]
            while unmapped:
                for entry in self.entries:
                    mapped, unmapped = self._overlay_ranges(unmapped.pop(), entry)
                    if mapped:
                        mapped_ranges.append(mapped)
                    if not unmapped:
                        break

        mapped_ranges.sort(key=lambda r: r.first)
        return mapped_ranges


def parse_ranged_almanac(file_contents: str) -> tuple[list[Range], RangedAlmanac]:
    paragraphs = file_contents.strip().split("\n\n")

    seed_range_list = [int(seed) for seed in paragraphs[0][7:].split(" ")]
    pairs = zip(seed_range_list[::2], seed_range_list[1::2])
    seeds = [Range(first=x, last=x + y - 1) for x, y in pairs]

    almanac_maps = []
    for section in paragraphs[1:]:
        entries = []
        for entry in section.splitlines()[1:]:
            destination_start, source_start, length = [int(x) for x in entry.split(" ")]
            entries.append(AlmanacEntry(source_start=source_start, destination_start=destination_start, length=length))

        entries = sorted(entries, key=lambda entry: entry.source_start)

        almanac_maps.append(RangedAlmanacMap(entries=entries))

    return seeds, RangedAlmanac(maps=almanac_maps)


def part2(file_contents: str) -> int:
    source_ranges, almanac = parse_ranged_almanac(file_contents)
    smallest_seed_locations = []
    for source_range in source_ranges:
        smallest_seed_locations.append(almanac.lookup_smallest_location_for_range(source_range))

    return min(smallest_seed_locations)


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
    assert part2(test_data) == 46
