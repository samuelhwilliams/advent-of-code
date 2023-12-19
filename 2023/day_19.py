#!/usr/bin/env python3


from rich import print

from helpers import load_input


def part1(file_contents: str) -> int:
    para1, para2 = file_contents.strip().split("\n\n")
    workflows = {}
    for line in para1.splitlines():
        name = line[: line.index("{")]
        conditions = [
            ((cond[0], cond[1], int(cond[2 : cond.index(":")])), cond[cond.index(":") + 1 :])
            if ":" in cond
            else (None, cond)
            for cond in line[line.index("{") + 1 : -1].split(",")
        ]
        workflows[name] = conditions

    total = 0
    for line in para2.splitlines():
        part = eval(f"dict({line[1:-1]})")  # EWWWW lol
        curr_workflow = "in"
        while curr_workflow not in "AR":
            for condition, next_workflow in workflows[curr_workflow]:
                if condition:
                    check_attr, check_cond, check_val = condition
                    if (check_cond == ">" and part[check_attr] <= check_val) or (
                        check_cond == "<" and part[check_attr] >= check_val
                    ):
                        continue
                curr_workflow = next_workflow
                break

        if curr_workflow == "A":
            total += sum(part.values())
    return total


def part2(file_contents: str) -> int:
    # data = parse_file_contents(file_contents)  # noqa
    return 0


if __name__ == "__main__":
    answer1 = part1(load_input(__file__))
    answer2 = part2(load_input(__file__))
    print(f"The answer is: {answer1=}, {answer2=}")


test_data = """
px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
"""


def test_part1():
    assert part1(test_data) == 19114


def test_part1_real():
    assert part1(load_input(__file__)) == 399284


def test_part2():
    assert part2(test_data) == 0


# def test_part2_real():
#     assert part2(load_input(__file__)) == 0
