import fileinput
import itertools
import math
import copy

from typing import List, Dict, Tuple


DIRS = list(set(itertools.product([-1,0,1], repeat=4)) - set([(0,0,0,0)]))


class Board:
    def __init__(self, data: List[str]) -> None:
        z = 0
        w = 0
        self.grid = {}
        for x, row in enumerate(data):
            for y, col in enumerate(row):
                self.grid[(x, y, z, w)] = col
        self.xmin: int = int( math.inf)
        self.xmax: int = int(-math.inf)
        self.ymin: int = int( math.inf)
        self.ymax: int = int(-math.inf)
        self.zmin: int = int( math.inf)
        self.zmax: int = int(-math.inf)
        self.wmin: int = int( math.inf)
        self.wmax: int = int(-math.inf)
        self.update_bounds()


    def update_bounds(self) -> None:
        for key_tuple in self.grid.keys():
            x, y, z, w = key_tuple
            if x < self.xmin:
                self.xmin = int(x)
            if x > self.xmax:
                self.xmax = int(x)
            if y < self.ymin:
                self.ymin = int(y)
            if y > self.ymax:
                self.ymax = int(y)
            if z < self.zmin:
                self.zmin = int(z)
            if z > self.zmax:
                self.zmax = int(z)
            if w < self.wmin:
                self.wmin = int(w)
            if w > self.wmax:
                self.wmax = int(w)


    def __getitem__(self, tup: Tuple[int, int, int, int]) -> str:
        if tup not in self.grid:
            return '.'
        return self.grid[tup]

    def __setitem__(self, tup: Tuple[int, int, int, int], item: str) -> None:
        self.grid[tup] = item
        self.update_bounds()

    def neighbors(self, tup: Tuple[int, int, int, int]) -> List[str]:
        x, y, z, w = tup
        result = []
        for neighbor in DIRS:
            result.append(self.grid.get((x+neighbor[0], y+neighbor[1], z+neighbor[2], w+neighbor[3]), '.'))
        return result

    def num_active(self) -> int:
        return len([x for x in self.grid.values() if x == '#'])


def one_generation(board: Board) -> Board:
    prev = copy.deepcopy(board)
    for x in range(board.xmin-1, board.xmax+2):
        for y in range(board.ymin-1, board.ymax+2):
            for z in range(board.zmin-1, board.zmax+2):
                for w in range(board.wmin-1, board.wmax+2):
                    num_neighbors = prev.neighbors((x, y, z, w)).count('#')
                    if prev[(x, y, z, w)] == '#' and not (num_neighbors == 2 or num_neighbors == 3):
                        board[(x, y, z, w)] = '.'
                    elif prev[(x, y, z, w)] == '.' and num_neighbors == 3:
                        board[(x, y, z, w)] = '#'
    return board


data = []
for line in fileinput.input():
    data.append(line.strip())

board = Board(data)
for k in range(6):
    board = one_generation(board)

print(board.num_active())
