from pathlib import Path


def get_input() -> list[list[int]]:
    with (Path(__file__).parent / "input").open() as f:
        return [list(map(int, line.split(" "))) for line in f]


MAX_DISTANCE = 3


def rules(report: list[int]) -> bool:
    """
    The levels are either all increasing or all decreasing.
    Any two adjacent levels differ by at least one and at most three.
    """

    first = report[0]
    second = report[1]
    increasing = first < second
    for idx, item in enumerate(report[:-1]):
        next_item = report[idx + 1]
        if (
            # rule 1
            (item > next_item and increasing)
            or (item < next_item and not increasing)
            # rule 2
            or (distance := abs(item - next_item)) < 1
            or distance > MAX_DISTANCE
        ):
            return False
    return True


reports = get_input()
safe_reports = 0
for report in reports:
    if rules(report):
        safe_reports += 1
        continue

    # check if rules are valid if a random item is removed
    for i in range(len(report)):
        without_i = report[:i] + report[i + 1 :]

        if rules(without_i):
            safe_reports += 1
            break

print(f"SAFE REPORTS: {safe_reports}")
