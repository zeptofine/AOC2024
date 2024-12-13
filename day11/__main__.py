import math
from collections import defaultdict
from pathlib import Path


def get_input() -> list[int]:
    with (Path(__file__).parent / "input").open() as f:
        return [int(c) for row in f for c in row.split(" ")]


def num_of_stones(nums: list[int], times: int) -> int:
    number_count = {float(n): 1 for n in nums}
    for _ in range(times):
        ns = defaultdict(float)

        ns[1] += number_count.pop(0, 0)
        for number, count in number_count.items():
            length = int(math.log10(number)) + 1
            if length % 2 == 0:
                a, b = divmod(number, 10 ** (length / 2))
                ns[a] += count
                ns[b] += count
            else:
                ns[number * 2024] += count
        number_count = ns
    return int(sum(number_count.values()))


if __name__ == "__main__":
    nums = get_input()

    print(nums)
    print()

    print(f"P1: {num_of_stones(nums, 25)}")
    print(f"P2: {num_of_stones(nums, 75)}")
