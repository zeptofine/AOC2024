from pathlib import Path
from time import perf_counter

TOP = 9


def search_point(
    memory: dict[tuple[int, int], list[tuple[int, int]]],
    grid: list[list[int]],
    pt: tuple[int, int],
) -> list[tuple[int, int]]:
    if pt in memory:
        return memory[pt]

    val = grid[pt[0]][pt[1]]
    if val == TOP:
        return [pt]

    s = []
    for neighbor in (
        (pt[0] - 1, pt[1]),
        (pt[0] + 1, pt[1]),
        (pt[0], pt[1] - 1),
        (pt[0], pt[1] + 1),
    ):
        if (
            # check bounds
            0 <= neighbor[0] < len(grid)
            and 0 <= neighbor[1] < len(grid[0])
            # check value
            and grid[neighbor[0]][neighbor[1]] == val + 1
        ):
            result = search_point(memory, grid, neighbor)
            memory[neighbor] = result
            s.extend(result)

    return s


def get_input() -> tuple[list[tuple[int, int]], list[list[int]]]:
    grid = []
    trailheads = []
    with (Path(__file__).parent / "input").open() as f:
        for y, row in enumerate(f):
            r = []
            for x, c in enumerate(row.strip()):
                if c == "0":
                    trailheads.append((y, x))
                r.append(int(c))

            grid.append(r)

    return trailheads, grid


if __name__ == "__main__":
    trailheads, grid = get_input()
    t = perf_counter()
    memory = {}
    all_scores = 0
    all_ratings = 0
    for head in trailheads:
        tails = search_point(
            memory,
            grid,
            head,
        )
        score = len(set(tails))
        rating = len(tails)
        # print(f"HEAD {head} UNIQUESCORE: {unscore} TOTALSCORE: {score} {tails}")
        all_scores += score
        all_ratings += rating

    print(f"TOTAL UNIQUE SCORE: {all_scores}")
    print(f"TOTAL SCORE: {all_ratings}")
    print(f"{(perf_counter() - t)}s")
