import copy
import fileinput

from utils import lmap
from typing import List, Dict


def is_in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols


def neighbors(grid, i, j, line_of_sight=False) -> List[str]:
    if line_of_sight:
        dist = 1
        dirs_remaining = set(range(0, 8))
        tmp = neighbors2(grid, i, j, dist, dirs_remaining=dirs_remaining)
        result = list(tmp.values())
        dirs_remaining -= set(tmp.keys())
        # print(f"({i=},{j=})[{dist=}]: {tmp=} {dirs_remaining=}")
        while len(result) < 8 or dirs_remaining:
            dist += 1
            try:
                tmp = neighbors2(grid, i, j, dist, dirs_remaining=dirs_remaining)
            except StopIteration:
                break
            result += list(tmp.values())
            dirs_remaining -= set(tmp.keys())
            # print(f"({i=},{j=})[{dist=}]: {tmp=} {dirs_remaining=}")
        return result
    return [grid[i-1][j-1] if is_in_bounds(i-1, j-1, len(grid), len(grid[0])) else None,
            grid[i-1][j] if is_in_bounds(i-1, j, len(grid), len(grid[0])) else None,
            grid[i-1][j+1] if is_in_bounds(i-1, j+1, len(grid), len(grid[0])) else None,
            grid[i][j-1] if is_in_bounds(i, j-1, len(grid), len(grid[0])) else None,
            grid[i][j+1] if is_in_bounds(i, j+1, len(grid), len(grid[0])) else None,
            grid[i+1][j-1] if is_in_bounds(i+1, j-1, len(grid), len(grid[0])) else None,
            grid[i+1][j] if is_in_bounds(i+1, j, len(grid), len(grid[0])) else None,
            grid[i+1][j+1] if is_in_bounds(i+1, j+1, len(grid), len(grid[0])) else None]


DIRS = {
    0: (-1, -1),
    1: (0, -1),
    2: (1, -1),
    3: (1, 0),
    4: (1, 1),
    5: (0, 1),
    6: (-1, 1),
    7: (-1, 0)
}


def neighbors2(grid, i, j, dist, dirs_remaining) -> Dict[int, str]:
    result = {}
    at_least_one_in_bounds = False
    for direction in dirs_remaining:
        row, col = DIRS[direction]
        row, col = row*dist + i, col*dist + j
        if is_in_bounds(row, col, len(grid), len(grid[0])):
            at_least_one_in_bounds = True
            if grid[row][col] != '.':
                result[direction] = grid[row][col]
    if not at_least_one_in_bounds:
        raise StopIteration()
    return result


def decide_on_occupancy(grid, num, line_of_sight):
    new_grid = copy.deepcopy(grid)
    for i, row in enumerate(grid):
        for j, col in enumerate(row):
            # print(f"decide_row{i}_col{j}")
            if col == '#' and neighbors(grid, i, j, line_of_sight).count('#') >= num:
                new_grid[i][j] = 'L'
            elif col == 'L' and neighbors(grid, i, j, line_of_sight).count('#') == 0:
                new_grid[i][j] = '#'
            else:
                new_grid[i][j] = col
    return new_grid


def print_field(_input):
    print('\n'.join(lmap(lambda x: "".join(x), _input)))
    print()


def count_occupied(_input):
    return (''.join(lmap(lambda x: "".join(x), _input))).count('#')


def read_input(fname):
    result = []
    with open(fname, 'r') as in_file:
        for i, line in enumerate(in_file):
            line = line.strip()
            result.append(line)
    return result


def play_game(field, adjacent=True):
    stable = False
    prev = None

    # init
    # print_field(result)
    field = lmap(list, ('\n'.join(field)).replace('L', '#').split('\n'))
    # print_field(result)

    k = 1
    while not stable:
        prev = copy.deepcopy(field)
        if adjacent:
            field = decide_on_occupancy(prev, 4, False)
        else:
            field = decide_on_occupancy(prev, 5, True)
        # print_field(field)
        if prev == field:
            stable = True
        # print(f"Generation {k}")
        k += 1

    # print_field(field)
    return count_occupied(field)


total = 0
result = []

for i, line in enumerate(fileinput.input()):
    line = line.strip()
    result.append(line)

print(f"Solution 1: {play_game(result, adjacent=True)=}")
print(f"Solution 2: {play_game(result, adjacent=False)=}")
