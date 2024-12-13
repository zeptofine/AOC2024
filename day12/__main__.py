from collections import defaultdict
from pathlib import Path

type Point = tuple[int, int]
type Grid = list[list[str]]


def get_input() -> Grid:
    with (Path(__file__).parent / "input").open() as f:
        return [list(r) for row in f if (r := row.strip())]


def count_corners(memory: set[Point], pt: Point) -> int:
    corner_count = 0
    for corner_test in [
        [(1, 0), (1, 1), (0, 1)],  # bottom right
        [(1, 0), (1, -1), (0, -1)],  # bottom left
        [(0, -1), (-1, -1), (-1, 0)],  # top left
        [(-1, 0), (-1, 1), (0, 1)],  # top right
    ]:
        b = None
        corner_count += (
            (a := (pt[0] + corner_test[0][0], pt[1] + corner_test[0][1]) in memory)
            and (b := (pt[0] + corner_test[2][0], pt[1] + corner_test[2][1]) in memory)
            and (pt[0] + corner_test[1][0], pt[1] + corner_test[1][1]) not in memory
        ) or (
            not a
            and (
                b
                if b is not None
                else (pt[0] + corner_test[2][0], pt[1] + corner_test[2][1])
                not in memory
            )
        )
    return corner_count


def search_area(
    grid: Grid,
    pt: Point,
    target: str,
) -> tuple[set[Point], dict[Point, set[Point]], int]:
    memory = {pt}
    point_neighbors = defaultdict(set, {pt: set()})
    points: list[Point] = [pt]

    while len(points):
        pt = points.pop()
        for neighbor in {
            (pt[0] - 1, pt[1]),
            (pt[0] + 1, pt[1]),
            (pt[0], pt[1] - 1),
            (pt[0], pt[1] + 1),
        }:
            if neighbor in memory:
                point_neighbors[pt].add(neighbor)
            elif (
                # check bounds
                0 <= neighbor[0] < len(grid)
                and 0 <= neighbor[1] < len(grid[0])
                # check value
                and grid[neighbor[0]][neighbor[1]] == target
            ):
                points.append(neighbor)
                memory.add(neighbor)
                point_neighbors[pt].add(neighbor)
                point_neighbors[neighbor].add(pt)
    num_of_sides = sum(count_corners(memory, point) for point in memory)
    return memory, point_neighbors, num_of_sides


if __name__ == "__main__":
    inp = get_input()
    # pprint(inp)
    searched_points = set()
    ap_price = 0
    side_price = 0
    for y, row in enumerate(inp):
        for x, c in enumerate(row):
            if (y, x) in searched_points:
                continue
            points, point_neighbors, sides = search_area(inp, (y, x), c)
            searched_points.update(points)
            perimeter = sum(
                [4 - len(neighbors) for neighbors in point_neighbors.values()]
            )
            area = len(points)
            ap_price += area * perimeter
            side_price += area * sides
            # print(f"AREA: {area}")
            # print(f"PERIMETER: {perimeter}")
            # print(f"SIDES: {sides}")
    print(f"TOTAL AREA * PERIMETER PRICE: {ap_price}")
    print(f"TOTAL AREA * SIDE PRICE: {side_price}")
