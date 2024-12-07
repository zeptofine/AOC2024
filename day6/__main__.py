from dataclasses import dataclass
from pathlib import Path
from typing import Union

from tqdm import tqdm

type Anglemask = int
type Angle = int

UP = 1 << 0
RIGHT = 1 << 1
DOWN = 1 << 2
LEFT = 1 << 3
DIR_UP = (-1, 0)
DIR_RIGHT = (0, 1)
DIR_DOWN = (1, 0)
DIR_LEFT = (0, -1)


def dir_to_mask(direction: tuple[int, int]) -> Anglemask:
    return (
        (direction[0] == -1) * (UP)
        | (direction[0] == +1) * (DOWN)
        | (direction[1] == -1) * (LEFT)
        | (direction[1] == +1) * (RIGHT)
    )


@dataclass(frozen=True)
class Guard:
    position: tuple[int, int]
    direction: tuple[int, int] = (-1, 0)

    def rotated(self) -> "Guard":
        return Guard(self.position, (self.direction[1], -self.direction[0]))

    def predict_next_pos(self) -> tuple[int, int]:
        return (
            self.position[0] + self.direction[0],
            self.position[1] + self.direction[1],
        )

    def moved(self, board: list[str]) -> Union["Guard", None]:
        newpos = self.predict_next_pos()
        if not (0 <= newpos[0] < len(board) and 0 <= newpos[1] < len(board[0])):
            return None

        if board[newpos[0]][newpos[1]] != ".":  # rotate
            return self.rotated()

        # move forward
        return Guard(newpos, self.direction)

    def copy(self) -> "Guard":
        return Guard(self.position, self.direction)


def get_input() -> tuple[list[str], Guard | None]:
    grid = (Path(__file__).parent / "input").read_text().splitlines()
    player = None
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if c == "^":
                player = Guard((y, x), (-1, 0))
                grid[y] = row[:x] + "." + row[x + 1 :]
                return grid, player

    return grid, player


grid, guard = get_input()
assert guard is not None


def find_loop(grid: list[str], guard: Guard) -> dict[tuple[int, int], Anglemask] | None:
    searched_spots: dict[tuple[int, int], Anglemask] = {
        guard.position: dir_to_mask(guard.direction)
    }
    newguard = guard
    while (newguard := newguard.moved(grid)) is not None:
        m = dir_to_mask(newguard.direction)
        if m & searched_spots.get(newguard.position, 0):
            return None

        searched_spots[newguard.position] = searched_spots.get(newguard.position, 0) | m

    return searched_spots


searched_spots = find_loop(
    grid,
    guard,
)  # there should not be one in the first instance
assert isinstance(searched_spots, dict)

print(f"TOTAL POSITIONS: {len(searched_spots)}")


def insert_artificial_obstacle(grid: list[str], pos: tuple[int, int]) -> list[str]:
    grid[pos[0]] = grid[pos[0]][: pos[1]] + "O" + grid[pos[0]][pos[1] + 1 :]
    return grid


loops = 0
# create Players for every position the guard was initially in
guards: list[Guard] = []
for spot, mask in searched_spots.items():
    if mask & UP:
        guards.append(Guard(spot, DIR_UP))
    if mask & RIGHT:
        guards.append(Guard(spot, DIR_RIGHT))
    if mask & DOWN:
        guards.append(Guard(spot, DIR_DOWN))
    if mask & LEFT:
        guards.append(Guard(spot, DIR_LEFT))

original_guard = guard
newgrids = list(
    {
        newobstacle.position: insert_artificial_obstacle(
            grid.copy(), newobstacle.position
        )
        for guard in guards
        if (newobstacle := guard.moved(grid)) is not None
        and newobstacle.position != original_guard.position
    }.values()
)

loops = sum(1 for g in tqdm(newgrids) if find_loop(g, original_guard) is None)
print(f"LOOPS: {loops}")
