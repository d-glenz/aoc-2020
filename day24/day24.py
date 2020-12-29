import re
import fileinput
from collections import defaultdict
import copy
from typing import DefaultDict, Set, Dict, Tuple, List


directions = {
    "nw": (-1, -2),
    "ne": (1, -2),
    "e": (2, 0),
    "w": (-2, 0),
    "sw": (-1, 2),
    "se": (1, 2)
}


def neighbor_values(tiles: Dict[Tuple[int, int], int], x: int, y: int) -> List[int]:
    return [tiles[(x+nx, y+ny)] for nx, ny in directions.values()]


def neighbors(tiles: Dict[Tuple[int, int], int], x: int, y: int) -> List[Tuple[int, int]]:
    return [(x+nx, y+ny) for nx, ny in directions.values()]


def one_day(tiles: Dict[Tuple[int, int], int], tiles_visited: Set[Tuple[int, int]]) -> Tuple[Dict[Tuple[int, int], int],
                                                                                             Set[Tuple[int, int]]]:
    prev = copy.deepcopy(tiles)
    all_tiles = set((x, y) for tile in tiles_visited for x, y in neighbors(tiles, tile[0], tile[1]))

    for x, y in all_tiles:
        black_neighbors = sum(neighbor_values(prev, x, y))
        if tiles[(x, y)] == 1 and (black_neighbors == 0 or black_neighbors > 2):
            tiles[(x, y)] = 0
        elif tiles[(x, y)] == 0 and black_neighbors == 2:
            tiles[(x, y)] = 1
    return tiles, all_tiles


def count(tiles: Dict[Tuple[int, int], int], tiles_visited: Set[Tuple[int, int]]) -> int:
    black_tiles = 0
    for x, y in tiles_visited:
        black_tiles += tiles[(x, y)]
    return black_tiles


def main() -> None:
    tiles: DefaultDict[Tuple[int, int], int] = defaultdict(lambda: 0)
    tiles_visited = set()

    for i, line in enumerate(fileinput.input()):
        line = line.strip()
        data = re.findall('(ne|nw|se|sw|e|w)', line)

        x, y = (0, 0)

        for direction in data:
            x += directions[direction][0]
            y += directions[direction][1]

        tiles[(x, y)] = 1 if tiles[(x, y)] == 0 else 0
        tiles_visited.add((x, y))

    tiles_visited = set((x, y) for tile in tiles_visited for x, y in neighbors(tiles, tile[0], tile[1]))
    tiles2 = dict(tiles)

    for i in range(100):
        tiles2, tiles_visited = one_day(tiles2, tiles_visited)
        print(f"Day {i+1}: {count(tiles2, tiles_visited)}")


if __name__ == "__main__":
    main()
