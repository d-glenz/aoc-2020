import fileinput
from collections import Counter
import typing

T = typing.TypeVar('T')

def filter_keys_by_value(mydict: typing.Dict[T, int], number: int) -> typing.List[T]:
    return [key for key, value in mydict.items() if value == number]


def main() -> None:
    solution_1 = 0
    solution_2 = 0

    group_answers_ctr: typing.Counter[str] = Counter()
    group_size = 0

    for line in fileinput.input():
        individual_answers = line.strip()
        for answer in individual_answers:
            group_answers_ctr[answer] += 1

        if individual_answers == "":
            solution_1 += len(group_answers_ctr.keys())
            solution_2 += len(filter_keys_by_value(group_answers_ctr, group_size))

            group_size = 0
            group_answers_ctr = Counter()
        else:
            group_size += 1
    else:
        solution_1 += len(group_answers_ctr.keys())
        solution_2 += len(filter_keys_by_value(group_answers_ctr, group_size))

    print(f"Solution 1: {solution_1}")
    print(f"Solution 1: {solution_2}")

if __name__ == "__main__":
        main()
