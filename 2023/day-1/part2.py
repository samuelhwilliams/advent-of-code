#!/usr/bin/env python3

values = {
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "0",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
}
convert = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def sum_calibration_values(data: list[str]) -> int:
    def _yield_values():
        for line in data:
            first_seen, latest_seen = None, None

            for i in range(len(line)):
                to_check = {
                    line[i : i + 1],
                    line[i : i + 2],
                    line[i : i + 3],
                    line[i : i + 4],
                    line[i : i + 5],
                }
                if match := (values & to_check):
                    found = match.pop()
                    if first_seen is None:
                        first_seen = convert.get(found, found)
                    latest_seen = convert.get(found, found)

            last_seen = latest_seen
            yield int(first_seen + last_seen)

    return sum(_yield_values())


if __name__ == '__main__':
    data = open("input/input.txt").read()
    answer = sum_calibration_values(data.splitlines())
    print(f"Answer is: {answer}")
