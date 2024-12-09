from collections import Counter
from pathlib import Path


def get_input() -> tuple[list[int], list[int]]:
    pth = Path(__file__).parent / "input"

    lst1 = []
    lst2 = []

    with pth.open() as f:
        for line in f:
            x, y = line.split("   ")
            lst1.append(int(x))
            lst2.append(int(y))

    return lst1, lst2


def get_sorted_input() -> tuple[list[int], list[int]]:
    l1, l2 = get_input()
    l1.sort()
    l2.sort()
    return l1, l2


if __name__ == "__main__":
    l1, l2 = get_sorted_input()
    total = 0
    similarity = 0
    for n1, n2 in zip(l1, l2):
        distance = abs(n1 - n2)
        total += distance
    print(f"TOTAL: {total}")

    l2_count = Counter(l2)

    for num in l1:
        if num in l2_count:
            similarity += num * l2_count[num]

    print(f"SIMILARITY: {similarity}")
