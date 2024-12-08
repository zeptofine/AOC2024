import itertools
from collections.abc import Iterator
from pathlib import Path


def get_input() -> tuple[list[str], Iterator[tuple[str, tuple[int, int]]]]:
    grid = (Path(__file__).parent / "input").read_text().splitlines()
    return (
        grid,
        (
            (c, (y, x))
            for y, row in enumerate(grid)
            for x, c in enumerate(row)
            if c != "."
        ),
    )


grid, ants = get_input()


def in_bounds(pt: tuple[int, int]) -> bool:
    return (0 <= pt[0] < len(grid)) and (0 <= pt[1] < len(grid[0]))


antinode_positions = set()
continuous_antinode = set()
for _char, antennas in itertools.groupby(sorted(ants), lambda a: a[0]):
    for (_, a), (_, b) in itertools.combinations(antennas, 2):
        slope = b[0] - a[0]
        step = b[1] - a[1]

        # part1
        antinode0 = (a[0] - slope, a[1] - step)
        antinode1 = (b[0] + slope, b[1] + step)
        if in_bounds(antinode0):
            antinode_positions.add(antinode0)
        if in_bounds(antinode1):
            antinode_positions.add(antinode1)

        # part2
        # backwards
        inc = 1
        while True:
            pt = (b[0] - slope * inc, b[1] - step * inc)
            if not in_bounds(pt):
                break
            continuous_antinode.add(pt)
            inc += 1

        # forwards
        inc = 1
        while True:
            pt = (a[0] + slope * inc, a[1] + step * inc)
            if not in_bounds(pt):
                break
            continuous_antinode.add(pt)
            inc += 1

print(f"ANTINODES WITHOUT HARMONICS: {len(antinode_positions)}")
print(f"ANTINODES WITH HARMONICS: {len(continuous_antinode)}")
