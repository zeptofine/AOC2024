import itertools
from collections.abc import Generator
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Antenna:
    symbol: str
    position: tuple[int, int]


def get_input() -> tuple[list[str], list[Antenna]]:
    grid = (Path(__file__).parent / "input").read_text().splitlines()
    ants: list[Antenna] = []
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if c != ".":
                ants.append(Antenna(symbol=c, position=(y, x)))

    return grid, ants


grid, ants = get_input()

yrange = range(len(grid))
xrange = range(len(grid[0]))


def in_bounds(pt: tuple[int, int]) -> bool:
    return (0 <= pt[0] < len(grid)) and (0 <= pt[1] < len(grid[0]))


ants.sort(key=lambda a: a.symbol)
# Part1
antinode_positions = set()
for _char, antennas in itertools.groupby(ants, lambda a: a.symbol):
    for a, b in itertools.combinations(antennas, 2):
        ap = a.position
        bp = b.position
        ydiff = abs(ap[0] - bp[0])
        xdiff = abs(ap[1] - bp[1])

        if ap[0] < bp[0]:
            # get y coords of antinodes
            antinode0y = ap[0] - ydiff
            antinode1y = bp[0] + ydiff
        else:
            antinode0y = ap[0] + ydiff
            antinode1y = bp[0] - ydiff

        if ap[1] < bp[1]:
            # get x coords of antinodes
            antinode0x = ap[1] - xdiff
            antinode1x = bp[1] + xdiff
        else:
            antinode0x = ap[1] + xdiff
            antinode1x = bp[1] - xdiff

        antinode0 = (antinode0y, antinode0x)
        antinode1 = (antinode1y, antinode1x)

        if in_bounds(antinode0):
            antinode_positions.add(antinode0)
        if in_bounds(antinode1):
            antinode_positions.add(antinode1)


print(f"ANTINODES WITHOUT HARMONICS: {len(antinode_positions)}")


# Part2
def generate_points_on_line(
    a: tuple[int, int], b: tuple[int, int]
) -> Generator[tuple[int, int], None, None]:
    if a[1] > b[1]:
        a, b = b, a
    slope = b[0] - a[0]
    step = b[1] - a[1]

    inc = 1
    while True:
        pt = (a[0] - slope * inc, a[1] - step * inc)
        if not in_bounds(pt):
            break
        yield pt
        inc += 1

    inc = 1
    while True:
        pt = (b[0] + slope * inc, b[1] + step * inc)
        if not in_bounds(pt):
            break
        yield pt
        inc += 1


antinode_positions = set()
for _char, antennas in itertools.groupby(ants, lambda a: a.symbol):
    for a, b in itertools.combinations(antennas, 2):
        for pt in generate_points_on_line(a.position, b.position):
            antinode_positions.add(pt)
        antinode_positions.add(a.position)
        antinode_positions.add(b.position)

print(f"ANTINODES WITH HARMONICS: {len(antinode_positions)}")
