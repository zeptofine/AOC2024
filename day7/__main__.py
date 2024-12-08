from dataclasses import dataclass
from pathlib import Path

from tqdm import tqdm


@dataclass
class Eqn:
    value: int
    operands: list[int]

    def f(self, value: int, idx: int, ops: str = "+*|") -> bool:
        if idx >= len(self.operands):
            return self.value == value
        for op in ops:
            if (
                self.f(value + self.operands[idx], idx + 1, ops)
                if op == "+"
                else self.f(value * self.operands[idx], idx + 1, ops)
                if op == "*"
                else self.f(int(f"{value}{self.operands[idx]}"), idx + 1, ops)
                if op == "|"
                else False
            ):
                return True
        return False

    def find(self, ops: str) -> bool:
        return self.f(self.operands[0], 1, ops)


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
    if eqn.find("+*"):
        s += eqn.value

print(f"SUM: {s}")

s = 0
for eqn in tqdm(eqns):
    if eqn.find("+*|"):
        s += eqn.value

print(f"SUM AFTER CONCATS: {s}")
