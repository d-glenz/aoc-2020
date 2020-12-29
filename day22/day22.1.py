import re
import fileinput
from typing import List, TypeVar, Callable, Iterable, Tuple


T = TypeVar('T')
S = TypeVar('S')


def lmap(func: Callable[[S], T], *iterables: Iterable[S]) -> List[T]:
    return list(map(func, *iterables))


def ints(s: str) -> List[int]:
    return lmap(int, re.findall(r"-?\d+", s))  # thanks mserrano!


def prep() -> Tuple[List[int], List[int]]:
    player1 = True

    p1_cards = []
    p2_cards = []

    for i, line in enumerate(fileinput.input()):
        line = line.strip()
        nums = ints(line)

        if line:
            if line.startswith('Player'):
                continue
            if player1:
                p1_cards.append(nums[0])
            else:
                p2_cards.append(nums[0])
        else:
            player1 = False

    return p1_cards, p2_cards


def one_round(p1: List[int], p2: List[int]) -> Tuple[List[int], List[int]]:
    top_p1 = p1[0]
    top_p2 = p2[0]

    if top_p1 > top_p2:
        return p1[1:] + [top_p1, top_p2], p2[1:]

    return p1[1:], p2[1:] + [top_p2, top_p1]


def solution1(p1: List[int], p2: List[int]) -> int:
    while p1 and p2:
        p1, p2 = one_round(p1, p2)

    winning = p1 if p1 else p2
    multipliers = list(reversed(range(len(winning)+1)))[:-1]

    return sum([a*b for a, b in zip(winning, multipliers)])


def main() -> None:
    p1, p2 = prep()
    print(f"Solution 1: {solution1(p1, p2)}")


if __name__ == "__main__":
    main()
