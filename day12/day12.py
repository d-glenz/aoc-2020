import fileinput
import re
import typing


def parse_line(regex: str, line: str) -> typing.Sequence[typing.Union[str, int]]:
    ret = []
    for match in re.match(regex, line).groups():
        try:
            ret.append(int(match))
        except ValueError:
            ret.append(match)

    return ret


def move_offset(field, current, offset):
    return (current + offset) % len(field)


def left_right(action, value, current_dir):
    offset = int(value / 90) * (-1 if action == 'L' else 1)
    return move_offset(dirs, current_dir, offset)


def rotate_around(action, value, waypoint):
    offset = int(value / 90) * (-1 if action == 'L' else 1)
    if offset in (-3, 1):
        waypoint = -waypoint[1], waypoint[0]
    elif offset in (-2, 2):
        waypoint = -waypoint[0], -waypoint[1]
    elif offset in (-1, 3):
        waypoint = waypoint[1], -waypoint[0]
    return waypoint


def move_object(action, value, current_pos):
    if action == 'N':
        current_pos = current_pos[0] + value, current_pos[1]
    elif action == 'S':
        current_pos = current_pos[0] - value, current_pos[1]
    elif action == 'E':
        current_pos = current_pos[0], current_pos[1] + value
    elif action == 'W':
        current_pos = current_pos[0], current_pos[1] - value
    return current_pos


def manhattan(north, east):
    return abs(north) + abs(east)


dirs = ['north', 'east', 'south', 'west']


def solution1():
    current_dir = 1
    current_pos = (0, 0)
    for i, line in enumerate(fileinput.input()):
        line = line.strip()
        action, value = parse_line(r'^([NSEWLRF])([0-9]*)', line)

        if action in 'LR':
            current_dir = left_right(action, value, current_dir)
        elif action == 'F':
            current_pos = move_object(dirs[current_dir][0].upper(), value, current_pos)
        elif action in 'NSEW':
            current_pos = move_object(action, value, current_pos)

    return manhattan(*current_pos)


def solution2():
    waypoint = (1, 10)
    current_pos = (0, 0)
    for i, line in enumerate(fileinput.input()):
        line = line.strip()
        action, value = parse_line(r'^([NSEWLRF])([0-9]*)', line)

        if action in 'LR':
            waypoint = rotate_around(action, value, waypoint)
        elif action == 'F':
            current_pos = move_object('N', waypoint[0]*value, current_pos)
            current_pos = move_object('E', waypoint[1]*value, current_pos)
        elif action in 'NSEW':
            waypoint = move_object(action, value, waypoint)

    return manhattan(*current_pos)


print(f"Solution 1: {solution1()}")
print(f"Solution 2: {solution2()}")
