#!/usr/bin/env python


def sum_calibration_values(data: list[str]) -> int:
    def _yield_values():
        for line in data:
            first_seen, latest_seen = None, None

            for char in line:
                if char.isdigit():
                    if first_seen is None:
                        first_seen = char
                    latest_seen = char

            last_seen = latest_seen
            yield int(first_seen + last_seen)

    return sum(_yield_values())


if __name__ == "__main__":
    data = open("input/input.txt").read()
    answer = sum_calibration_values(data.splitlines())
    print(f"Answer is: {answer}")
