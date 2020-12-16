import fileinput
from collections import defaultdict
import re
import typing


T = typing.TypeVar('T')


def lmap(func, *iterables) -> typing.List[T]:
    return list(map(func, *iterables))


def ints(s: str) -> typing.List[int]:
    return lmap(int, re.findall(r"-?\d+", s))  # thanks mserrano!


def main(limit):
    result = defaultdict(list)

    for i, line in enumerate(fileinput.input()):
        line = line.strip()
        nums = ints(line)

        j = 0
        for num in nums:
            result[num].append(j)
            # print(j, num)
            j += 1

        first_occurrence = True

    i = j
    while i < limit:
        if first_occurrence:
            num = 0
            if num in result:
                first_occurrence = False
            result[num].append(i)
        else:
            num = i - 1 - result[num][-2]
            if num in result:
                first_occurrence = False
            else:
                first_occurrence = True
            result[num].append(i)
        # print(i, num)
        i += 1
    print(i, num)


if __name__ == "__main__":
    main(2020)
    main(30000000)
