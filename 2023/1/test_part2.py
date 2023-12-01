from part2 import sum_calibration_values


def test_part2():
    data = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""
    assert sum_calibration_values(data.splitlines()) == 281
