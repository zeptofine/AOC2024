import time
from collections import deque
from pathlib import Path

disc: deque[int | None] = deque()
cdisc: list[tuple[int, int | None]] = []
with (Path(__file__).parent / "input").open() as f:
    empty = False
    id_ = 0
    while True:
        c = f.read(1).strip()
        if not c:
            break
        if empty:
            disc.extend([None] * int(c))
            cdisc.append((int(c), None))
        else:
            disc.extend([id_] * int(c))
            cdisc.append((int(c), id_))
            id_ += 1

        empty = not empty

t = time.perf_counter()
# Part 1
# move the blocks
i = 0
checksum = 0
while len(disc):
    item = disc.popleft()
    if item is None:
        while (lastitem := disc.pop()) is None:
            ...
        item = lastitem
    checksum += i * item
    i += 1

print(f"FRAGMENTED CHECKSUM: {checksum}")
print(f"{time.perf_counter() - t}s")

t = time.perf_counter()
# Part 2
# move the blocks
for i in range(len(cdisc) - 1, -1, -1):
    if cdisc[i][1] is None:
        continue
    for j in range(i):
        if cdisc[j][1] is None:
            if cdisc[j][0] == cdisc[i][0]:
                cdisc[j] = cdisc[i]
                cdisc[i] = (cdisc[i][0], None)
                break

            if cdisc[j][0] > cdisc[i][0]:
                cdisc[j] = (cdisc[j][0] - cdisc[i][0], cdisc[j][1])
                cdisc.insert(j, cdisc.pop(i))
                # We don't need this for some reason?
                # cdisc.insert(i, (cnt, None))
                break


# calculate checksum
checksum = 0
idx = 0
for cnt, c in cdisc:
    if c is None:
        idx += cnt
        continue

    for _ in range(cnt):
        checksum += c * idx
        idx += 1

print(f"MOVED AS WHOLE CHECKSUM: {checksum}")
print(f"{time.perf_counter() - t}s")
