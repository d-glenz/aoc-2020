import math
import fileinput
from typing import List, Optional


def chinese_remainder(n: List[int], a: List[int]) -> int:
    sum_i = 0
    prod = 1
    for i in n:
        prod *= i

    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum_i += a_i * mul_inv(p, n_i) * p

    return sum_i % prod


def mul_inv(a: int, b: int) -> int:
    b0 = b
    x0, x1 = 0, 1
    if b == 1:
        return 1

    while a > 1:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1 - q * x0, x0

    if x1 < 0:
        x1 += b0

    return x1


def solution1(arrival: int, ids: List[int]) -> int:
    min_waiting_time = math.inf
    optimal_bus_id = None
    for bus_id in ids:
        waiting_time = bus_id - (arrival % bus_id)
        if waiting_time < min_waiting_time:
            min_waiting_time = waiting_time
            optimal_bus_id = bus_id

    if optimal_bus_id is None:
        raise ValueError('no optimal bus ID found')

    return int(min_waiting_time * optimal_bus_id)


def solution2(bus_ids: List[Optional[int]]) -> int:
    n = []
    a = []

    for i, bus_id in enumerate(bus_ids):
        if bus_id is None:
            continue

        n.append(bus_id)
        a.append(bus_id - i)

    return chinese_remainder(n, a)


def main() -> None:
    for i, line in enumerate(fileinput.input()):
        line = line.strip()

        if i == 0:
            arrival = int(line)
        else:
            bus_ids = list(map(lambda a: int(a) if a.isnumeric() else None, line.split(',')))
            ids = list(filter(lambda x: x is not None, bus_ids))

    print(f"Solution 1: {solution1(arrival, ids)}")
    print(f"Solution 2: {solution2(bus_ids)}")


if __name__ == "__main__":
    main()
