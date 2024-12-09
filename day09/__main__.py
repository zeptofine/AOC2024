import time
from pathlib import Path

disc: list[int | None] = []
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
while i < len(disc):
    if disc[i] is None:
        while disc[-1] is None:
            disc.pop()
        disc[i] = disc.pop()

    i += 1


# calculate checksum
checksum = sum(int(c) * idx for idx, c in enumerate(disc) if c is not None)

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
                # cdisc.insert(i, (count, None))
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
