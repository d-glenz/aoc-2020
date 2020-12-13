import fileinput
from collections import Counter
import functools
from typing import Callable, List, TypeVar
import typing

S = TypeVar('S')
T = TypeVar('T')


def lmap(func: Callable[[S], T], *iterables: typing.Iterable[S]) -> List[T]:
    return list(map(func, *iterables))


def gen_chain(result: List[int]) -> List[int]:
    current_joltage = 0
    OUTLET = 0
    adapter_chain = [OUTLET]
    for adapter in sorted(result):
        if adapter - current_joltage > 3:
            break
        adapter_chain.append(adapter)
        current_joltage = adapter

    device = adapter_chain[-1] + 3
    adapter_chain.append(device)
    return adapter_chain


def solution1(adapter_chain: List[int]) -> typing.Counter[int]:
    print(f"{adapter_chain=}")
    ctr = Counter([b-a for a, b in zip(adapter_chain, adapter_chain[1:])])
    return ctr


@functools.lru_cache(maxsize=None)
def solution2(data: str, limit: int, current_joltage: int) -> int:
    data2 = lmap(int, data.split())
    if current_joltage == limit:
        return 1
    res = 0
    for additional_joltage in [1, 2, 3]:
        if current_joltage + additional_joltage in data2:
            res += solution2(data, limit, current_joltage + 1)
    return res


def main() -> None:
    joltages = []

    for i, line in enumerate(fileinput.input()):
        line = line.strip()
        joltages.append(int(line))

    joltages = sorted(joltages)

    adapter_chain = gen_chain(joltages)
    s1 = solution1(joltages)
    print(f"Solution 1 {s1[1] * s1[3]}")

    limit = adapter_chain[-1]
    s2 = solution2(" ".join(map(str, joltages)), limit-3, 0)
    print(f"solution 2: {s2}")


if __name__ == "__main__":
    main()
