import copy
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


def one_round(p1: List[int], p2: List[int], game: int) -> Tuple[List[int], List[int]]:
    top_p1 = p1[0]
    top_p2 = p2[0]
    player1_wins = False

    if len(p1) - 1 >= top_p1 and len(p2) - 1 >= top_p2:
        p1_prime = copy.deepcopy(p1[1:])[:top_p1]
        p2_prime = copy.deepcopy(p2[1:])[:top_p2]
        player1_wins, _ = new_game(p1_prime, p2_prime, game+1)
    else:
        if top_p1 > top_p2:
            player1_wins = True

    if player1_wins:
        return p1[1:] + [top_p1, top_p2], p2[1:]

    return p1[1:], p2[1:] + [top_p2, top_p1]


def new_game(p1: List[int], p2: List[int], game: int = 1) -> Tuple[bool, int]:
    previous_hands_p1 = set()
    previous_hands_p2 = set()
    p1_wins = False
    while p1 and p2:
        p1, p2 = one_round(p1, p2, game)
        if str(p1) in previous_hands_p1 or str(p2) in previous_hands_p2:
            p1_wins = True
            break
        previous_hands_p1.add(str(p1))
        previous_hands_p2.add(str(p2))
    else:
        p1_wins = bool(p1)
    if p1_wins:
        winning = p1
    else:
        winning = p2
    multipliers = list(reversed(range(len(winning)+1)))[:-1]

    return p1_wins, sum([a*b for a, b in zip(winning, multipliers)])


def main() -> None:
    p1, p2 = prep()
    p1_wins, score = new_game(p1, p2)
    print(f"Solution 2: {score}")


if __name__ == "__main__":
    main()
