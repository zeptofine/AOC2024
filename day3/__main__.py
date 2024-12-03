from pathlib import Path

import re2

RE = re2.compile(r"(mul\((\d{1,3}),(\d{1,3})\)|do(n\'t)?\(\))")
print(RE)

def get_input() -> str:
    return (Path(__file__).parent / "input").read_text()





expression = get_input()

total_unphased = 0
total_phased = 0 # total affected by do()s and don't()s
do = True
for match in RE.finditer(expression):
    print(match)
    print(match.groups())

    g1: str | None = match.group(2) # type: ignore[reportAssignmentType]
    g2: str | None = match.group(3) # type: ignore[reportAssignmentType]
    g3: str | None = match.group(4) # type: ignore[reportAssignmentType]
    if g1 is None and g2 is None:
        do = g3 is None
    elif g1 is not None and g2 is not None:
        n1 = int(g1)
        n2 = int(g2)
        total_unphased+=n1*n2
        if do:
            total_phased+=n1*n2

print(f"TOTAL DO IGNORED: {total_unphased}")
print(f"TOTAL: {total_phased}")
