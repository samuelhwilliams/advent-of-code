#!/usr/bin/env python3


def main(file_contents: str) -> int:
    return 0


if __name__ == '__main__':
    with open('input.txt') as f:
        answer = main(f.read())

    print(f"The answer is {answer}")
