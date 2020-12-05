import fileinput
from typing import List, Tuple, Union


def subdivide_last(lower: int, upper: int, partition: str) -> int:
    return lower if partition in ("F", "L") else upper

def subdivide(lower: int, upper: int, partition: str) -> Tuple[int, int]:
    half = round((upper - lower) / 2)
    if partition in ("F", "L"):
        return lower, lower + int(half) - 1
    return upper - int(half) + 1, upper

def subdivide_by_key(lower: int, upper: int, key: str) -> int:
    for r in key[:-1]:
        (lower, upper) = subdivide(lower, upper, r)
    return subdivide_last(lower, upper, key[-1])

def determinte_seat(key: str) -> Tuple[int, int, int]:
    row_characters = key[:7]
    col_characters = key[7:]

    row = subdivide_by_key(0, 127, row_characters)
    col = subdivide_by_key(0, 7, col_characters)

    return (row, col, row * 8 + col)

def main() -> None:
    all_seats = []
    for i, line in enumerate(fileinput.input()):
        line = line.strip()
        row, col, seat_id = determinte_seat(line)
        all_seats.append(seat_id)

    min_seat = min(all_seats)
    max_seat = max(all_seats)
    print(f"Solution 1: {max_seat}")

    all_empty_seats = set(range(min_seat, max_seat)) - set(all_seats)
    if all_empty_seats:
        (empty_seat,) = all_empty_seats
        print(f"Solution 2: {empty_seat}")

if __name__ == "__main__":
    main()
