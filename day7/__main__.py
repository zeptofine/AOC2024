from dataclasses import dataclass
from itertools import (
    product,
)
from pathlib import Path

from tqdm import tqdm


@dataclass
class Eqn:
    value: int
    operands: list[int]

    def try_combo(self, combo: tuple[str, ...]) -> bool:
        it = iter(self.operands)
        ct = iter(combo)
        val = next(it)
        for n in it:
            match next(ct):
                case "*":
                    val *= n
                case "+":
                    val += n
                case "|":
                    val = int(f"{val}{n}")
        return val == self.value

    def find_operators(self) -> tuple[str, ...] | None:
        ops = "+*"
        combos = product(ops, repeat=len(self.operands) - 1)
        for combo in combos:
            if self.try_combo(combo):
                return combo

        return None

    def find_operators_concat(self) -> tuple[str, ...] | None:
        ops = "+*|"
        combos = product(ops, repeat=len(self.operands) - 1)
        for combo in combos:
            if self.try_combo(combo):
                return combo

        return None


def get_input() -> list[Eqn]:
    lines = (Path(__file__).parent / "input").read_text().splitlines()

    eqns = []
    for line in lines:
        val, ops = line.split(": ")
        eqns.append(Eqn(int(val), list(map(int, ops.split(" ")))))

    return eqns


eqns = get_input()

s = 0
for eqn in tqdm(eqns):
    if eqn.find_operators():
        s += eqn.value

print(f"SUM: {s}")

s = 0
for eqn in tqdm(eqns):
    if eqn.find_operators_concat():
        s += eqn.value

print(f"SUM AFTER CONCATS: {s}")
