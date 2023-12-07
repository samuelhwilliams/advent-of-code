#!/usr/bin/env python3
import dataclasses
import enum
from collections import Counter
from functools import cached_property

import pytest
from rich import print

from helpers import load_input


CARD_STRENGTHS: dict[str, int] = {c: 12 - i for i, c in enumerate("AKQJT98765432")}
JOKER_CARD_STRENGTHS: dict[str, int] = {c: 12 - i for i, c in enumerate("AKQT98765432J")}


class HandType(int, enum.Enum):
    FIVE_OAK = 6
    FOUR_OAK = 5
    FULL_HOUSE = 4
    THREE_OAK = 3
    TWO_PAIR = 2
    ONE_PAIR = 1
    HIGH_CARD = 0


@dataclasses.dataclass
class CamelCard:
    hand: str
    bid: int

    @cached_property
    def type(self) -> HandType:
        counter = Counter(self.hand)
        most_common = counter.most_common()
        if most_common[0][1] == 5:
            return HandType.FIVE_OAK
        elif most_common[0][1] == 4:
            return HandType.FOUR_OAK
        elif most_common[0][1] == 3 and most_common[1][1] == 2:
            return HandType.FULL_HOUSE
        elif most_common[0][1] == 3:
            return HandType.THREE_OAK
        elif most_common[0][1] == 2 and most_common[1][1] == 2:
            return HandType.TWO_PAIR
        elif most_common[0][1] == 2:
            return HandType.ONE_PAIR
        else:
            return HandType.HIGH_CARD

    @cached_property
    def strength(self) -> tuple[int, ...]:
        return tuple(CARD_STRENGTHS[card] for card in self.hand)

    @cached_property
    def joker_type(self) -> HandType:
        counter = Counter(self.hand)
        joker_count = counter.pop("J", 0)
        most_common = counter.most_common()
        if joker_count == 5:
            return HandType.FIVE_OAK
        elif most_common[0][1] == 5:
            return HandType.FIVE_OAK
        elif most_common[0][1] + joker_count == 5:
            return HandType.FIVE_OAK
        elif most_common[0][1] == 4:
            return HandType.FOUR_OAK
        elif most_common[0][1] + joker_count == 4:
            return HandType.FOUR_OAK
        elif most_common[0][1] == 3 and most_common[1][1] == 2:
            return HandType.FULL_HOUSE
        elif most_common[0][1] + joker_count == 3 and most_common[1][1] == 2:
            return HandType.FULL_HOUSE
        elif most_common[0][1] == 3 and most_common[1][1] + joker_count == 2:
            return HandType.FULL_HOUSE
        elif most_common[0][1] == 3:
            return HandType.THREE_OAK
        elif most_common[0][1] + joker_count == 3:
            return HandType.THREE_OAK
        elif most_common[0][1] == 2 and most_common[1][1] == 2:
            return HandType.TWO_PAIR
        elif most_common[0][1] == 2 and most_common[1][1] + joker_count == 2:
            return HandType.TWO_PAIR
        elif most_common[0][1] == 2:
            return HandType.ONE_PAIR
        elif most_common[0][1] + joker_count == 2:
            return HandType.ONE_PAIR
        else:
            return HandType.HIGH_CARD

    @cached_property
    def joker_strength(self) -> tuple[int, ...]:
        return tuple(JOKER_CARD_STRENGTHS[card] for card in self.hand)

    @classmethod
    def from_line(cls, line: str):
        hand, bid = line.strip().split(" ")
        return CamelCard(hand=hand, bid=int(bid))


def parse_file(file_contents: str) -> list[CamelCard]:
    return [CamelCard.from_line(line) for line in file_contents.strip().splitlines()]


def part1(file_contents: str) -> int:
    cards = parse_file(file_contents)
    sorted_cards = sorted(cards, key=lambda card: (card.type, card.strength), reverse=True)
    return sum((card.bid * (i + 1)) for i, card in enumerate(sorted_cards[::-1]))


def part2(file_contents: str) -> int:
    cards = parse_file(file_contents)
    sorted_cards = sorted(cards, key=lambda card: (card.joker_type, card.joker_strength), reverse=True)
    return sum((card.bid * (i + 1)) for i, card in enumerate(sorted_cards[::-1]))


if __name__ == "__main__":
    data = load_input(__file__)
    answer1 = part1(data)
    answer2 = part2(data)
    print(f"The answer is: {answer1=}, {answer2=}")


test_data = """
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""


def test_part1():
    assert part1(test_data) == 6440


def test_part1_real_input():
    data = load_input(__file__)
    assert part1(data) == 256448566


def test_part2():
    assert part2(test_data) == 5905


@pytest.mark.parametrize(
    "hand, expected_type",
    (
        ("AAAAJ", HandType.FIVE_OAK),
        ("AAJAJ", HandType.FIVE_OAK),
        ("AAJKJ", HandType.FOUR_OAK),
        ("AAAAK", HandType.FOUR_OAK),
        ("AAJKA", HandType.FOUR_OAK),
        ("AAJKJ", HandType.FOUR_OAK),
        ("AJJKK", HandType.FOUR_OAK),
        ("AAAKK", HandType.FULL_HOUSE),
        ("AAJKK", HandType.FULL_HOUSE),
        ("AAAKK", HandType.FULL_HOUSE),
        ("AAJKK", HandType.FULL_HOUSE),
        ("AKQJJ", HandType.THREE_OAK),
        ("AKQTJ", HandType.ONE_PAIR),
        ("AKQT9", HandType.HIGH_CARD),
    ),
)
def test_part2_joker_hand_types(hand, expected_type):
    assert CamelCard(hand=hand, bid=0).joker_type == expected_type


def test_part2_real_input():
    data = load_input(__file__)
    assert part2(data) == 254412181
