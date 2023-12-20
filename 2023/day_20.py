#!/usr/bin/env python3
import collections
import dataclasses
from typing import Optional, Tuple, Iterable

import math
import pytest
from rich import print

from helpers import load_input


@dataclasses.dataclass
class Module:
    id: str
    on: bool = False
    inputs: list["Module"] = dataclasses.field(default_factory=list)
    outputs: list["Module"] = dataclasses.field(default_factory=list)

    def pulse(self, from_module: str, high: bool) -> Iterable[Tuple[bool, "Module"]]:
        pulse = self.behave(from_module, high)
        if pulse is not None:
            return ((pulse, output) for output in self.outputs)
        return tuple()

    def behave(self, from_module: str, high: bool) -> Optional[bool]:
        # Default for broadcast modules - echo what was passed in
        return high

    def __str__(self):
        return f"{self.id}-{self.on}"

    def __repr__(self):
        return str(self)


@dataclasses.dataclass
class FlipFlopModule(Module):
    def behave(self, from_module: str, high: bool):
        if high:
            return None

        self.on = not self.on
        return self.on


@dataclasses.dataclass
class ConjunctionModule(Module):
    memory: dict[str, bool] = dataclasses.field(default_factory=dict)

    def behave(self, from_module: str, high: bool):
        self.memory[from_module] = high
        if all(v is True for v in self.memory.values()):
            return False

        return True

    def __str__(self):
        return f"{self.id}-{self.on}-{self.memory}"


def parse_file_contents(file_contents: str):
    lines = file_contents.strip().splitlines()
    modules = {}
    module_outputs = {}
    for line in lines:
        match line[0]:
            case "%":
                module_type = FlipFlopModule
                ident = line[1 : line.index(" -> ")]
            case "&":
                module_type = ConjunctionModule
                ident = line[1 : line.index(" -> ")]
            case _:
                module_type = Module
                ident = line[: line.index(" -> ")]

        outputs = line[line.index(" -> ") + 4 :].split(", ")
        modules[ident] = module_type(id=ident)
        module_outputs[ident] = outputs

    for module in list(modules.values()):
        for o in module_outputs[module.id]:
            if o not in modules:
                modules[o] = Module(id=o)
            module.outputs.append(modules[o])
        for output in module.outputs:
            if output.id in modules:
                modules[output.id].inputs.append(module)

    for module in modules.values():
        if isinstance(module, ConjunctionModule):
            for inp in module.inputs:
                module.memory[inp.id] = False

    return modules


def part1(file_contents: str) -> int:
    modules = parse_file_contents(file_contents)
    queue: collections.deque[Tuple[bool, Module, str]] = collections.deque()

    high, low = 0, 0
    for _ in range(1_000):
        queue.append((False, modules["broadcaster"], "button"))
        loop = 0
        while queue:
            pulse, module, from_module = queue.popleft()
            if pulse:
                high += 1
            else:
                low += 1
            for next_pulse, next_module in module.pulse(from_module=from_module, high=pulse):
                queue.append((next_pulse, next_module, module.id))
            loop += 1

    return high * low


def part2(file_contents: str) -> int:
    modules = parse_file_contents(file_contents)
    queue: collections.deque[Tuple[bool, Module, str]] = collections.deque()

    input_to_end = modules["rx"].inputs[0]  # there is only 1
    inputs_to_penultimate = {m.id for m in input_to_end.inputs}  # there are 4
    presses_to_activate = {}

    high, low = 0, 0
    button_presses = 0
    while True:
        button_presses += 1
        queue.append((False, modules["broadcaster"], "button"))
        while queue:
            pulse, module, from_module = queue.popleft()
            if pulse:
                high += 1

                # If we've got a high pulse at one of the inputs which activates the penultimate module, record
                # how many presses it took to get there. From input spelunking, we know they are all conjunction
                # modules.
                # From reddit threads and from iterative checks, they activate on prime number button presses.
                # Working out when they would all trigger a high pulse together is therefore just a case of LCM;
                # with prime numbers that's just multiplying them all together.
                if from_module in inputs_to_penultimate and from_module not in presses_to_activate:
                    presses_to_activate[from_module] = button_presses

                if len(presses_to_activate) == len(inputs_to_penultimate):
                    return math.prod(presses_to_activate.values())
            else:
                low += 1
            for next_pulse, next_module in module.pulse(from_module=from_module, high=pulse):
                if next_pulse is False and next_module.id == "rx":
                    return button_presses
                queue.append((next_pulse, next_module, module.id))


if __name__ == "__main__":
    answer1 = part1(load_input(__file__))
    answer2 = part2(load_input(__file__))
    print(f"The answer is: {answer1=}, {answer2=}")


test_data = [
    (
        """
broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a
""",
        32_000_000,
    ),
    (
        """
broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output
""",
        11687500,
    ),
]


@pytest.mark.parametrize("test_input, expected_output", test_data)
def test_part1(test_input, expected_output):
    assert part1(test_input) == expected_output


def test_part1_real():
    assert part1(load_input(__file__)) == 886347020


def test_part2_real():
    assert part2(load_input(__file__)) == 233283622908263
