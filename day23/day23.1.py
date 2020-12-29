import fileinput
from typing import Callable, TypeVar, List, Tuple

S = TypeVar('S')
T = TypeVar('T')


def lmap(func: Callable[[S], T], *iterables: List[S]) -> List[T]:
    return list(map(func, *iterables))


def print_cups(cups: List[int], idx: int) -> str:
    return ' '.join([f" {cup} " if i != idx else f"({cup})" for i, cup in enumerate(cups)])


def aidx(idx: int, cups: List[int]) -> int:
    return idx % len(cups)


def shift(cups: List[int], dist: int) -> List[int]:
    return cups[-dist:] + cups[:-dist]


def one_move(cups: List[int], current_idx: int) -> Tuple[List[int], int]:
    current = cups[aidx(current_idx, cups)]
    max_cup, min_cup = max(cups), min(cups)

    # 1. pick up three cups clockwise of current
    three_cups = []
    cidx = current_idx
    for i in range(3):
        print(f"aidx({cidx=}+1, cups)={aidx(cidx+1, cups)}  == {cups=}")
        print(f"{cups[aidx(cidx+1, cups):][:3]=} - idx={cidx}")
        idx_ = aidx(cidx+1, cups)
        spare = cups.pop(idx_)
        three_cups.append(spare)
        if idx_ == 0:
            cidx -= 1

    print(f"pick up: {', '.join(map(str, three_cups))}")

    # 2. select destination cup
    destination_label = current - 1
    while True:
        try:
            destination_idx = cups.index(destination_label)
            break
        except ValueError:
            # print(f"inc {destination_label}")
            old = destination_label
            destination_label = (destination_label - 1) if destination_label - 1 >= min_cup else max_cup
            print(f"destination {old} not found, changing label to {destination_label}")

    print(f"destination: {destination_label}")

    # 3. place three cups clockwise of destination
    cups.insert(destination_idx + 1, three_cups[0])
    cups.insert(destination_idx + 2, three_cups[1])
    cups.insert(destination_idx + 3, three_cups[2])

    # -> shift back
    wrong_idx = cups.index(current)
    cups = shift(cups, current_idx - wrong_idx)

    # 4. select new current cup
    current_idx = aidx(current_idx+1, cups)

    return cups, current_idx


def main() -> None:
    for i, line in enumerate(fileinput.input()):
        line = line.strip()
        cups: List[int] = lmap(int, list(line))

    NUM_MOVES = 99
    move = 1
    current_idx = 0
    while move <= 1+NUM_MOVES:
        print(f"-- move {move} --")
        print(f"cups={print_cups(cups, current_idx)}")
        cups, current_idx = one_move(cups, current_idx)
        print()
        move += 1

    cups = shift(cups, -cups.index(1)-1)
    print(''.join(map(str, cups[:-1])))


if __name__ == "__main__":
    main()
