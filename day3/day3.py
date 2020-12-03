input1 = """\
..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#"""


def replicate_many_times(field: str, many=30):
    rows = field.split('\n')
    return [row*many for row in rows]

def solution1_and_2(input1, y_mult=1, x_mult=3):
    rows = len(input1.split('\n'))
    total_field = replicate_many_times(input1, many=rows*3)

    y, x = 0, 0
    steps = ''
    while y < rows:
        steps += total_field[y][x]
        x += x_mult
        y += y_mult

    return steps.count('#')

with open('input3.real') as day3_input:
    solution = 1
    field = day3_input.read().strip()
    for x,y in [(1,1),(3,1),(5,1),(7,1),(1,2)]:
        solution *= solution1_and_2(field, x_mult=x, y_mult=y)

print(solution)
