from collections import defaultdict
from pathlib import Path


def get_input() -> list[str]:
    return (Path(__file__).parent / "input").read_text().splitlines()


type POINT = tuple[int, int]
type DIRECTION = tuple[int, int]
straight_dirs: tuple[DIRECTION, ...] = (
    (0, +1),  # right
    (0, -1),  # left
    (+1, 0),  # down
    (-1, 0),  # up
)
diag_dirs: tuple[DIRECTION, ...] = (
    (+1, +1),  # down right
    (+1, -1),  # down left
    (-1, -1),  # up left
    (-1, +1),  # up right
)
directions: tuple[DIRECTION, ...] = straight_dirs + diag_dirs


def string_exists(
    search: list[str],
    point: POINT,
    direction: DIRECTION,
    remaining: str,
) -> bool:
    if (
        point[0] < 0
        or point[0] >= len(search)
        or point[1] < 0
        or point[1] >= len(search[point[0]])
    ):
        return False
    if search[point[0]][point[1]] == remaining[0]:  # correct character
        if new_rem := remaining[1:]:
            return string_exists(
                search,
                (point[0] + direction[0], point[1] + direction[1]),
                direction,
                new_rem,
            )
        return True
    return False

search = get_input()


# Find all the XMAS strings

# points that start a MAS combination, and the direction that it creates
mases: set[tuple[POINT, DIRECTION]] = set()
count = 0

# Find all the X-MAS combinations
centers: dict[POINT, int] = defaultdict(int)

for y in range(len(search)):
    for x in range(len(search[y])):
        point = (y, x)
        if search[y][x] == "X":
            for direction in directions:
                ex = string_exists(search, point, direction, "XMAS")
                count += ex
        elif search[y][x] == "M":
            for direction in diag_dirs:
                if string_exists(search, point, direction, "MAS"):
                    mases.add((point, direction))
                    center = point[0] + direction[0], point[1] + direction[1]
                    centers[center] += 1


PAIR = 2

# find all centers that have multiple mases associated
proper_count = sum(1 for cnt in centers.values() if cnt == PAIR)

print(f"XMASes: {count}")
print(f"Diagonal X-MASes: {proper_count}")
