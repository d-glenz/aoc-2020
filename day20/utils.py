import re
import typing
from copy import deepcopy


LETTERS = 'abcdefghijklmnopqrstuvwxyz'
VOWELS = {'a', 'e', 'i', 'o', 'u'}
CONSONANTS = set(x for x in LETTERS if x not in VOWELS)

T = typing.TypeVar('T')
S = typing.TypeVar('S')


def lmap(func, *iterables) -> typing.List[T]:
    return list(map(func, *iterables))


def flatten(lst: typing.List[typing.List[T]]) -> typing.List[T]:
    return [i for x in lst for i in x]


def ints(s: str) -> typing.List[int]:
    return lmap(int, re.findall(r"-?\d+", s))  # thanks mserrano!


def words(s: str) -> typing.List[str]:
    return re.findall(r"[a-zA-Z]+", s)


def fst(x: typing.Tuple[T, S]) -> T:
    return x[0]


def snd(x: typing.Tuple[T, S]) -> S:
    return x[1]


def parse_line_fields(regex: str, line: str) -> typing.Sequence[typing.Union[str, int]]:
    ret = []
    for match in re.findall(regex, line):
        try:
            ret.append(int(match))
        except ValueError:
            ret.append(match)

    return ret


def parse_line(regex: str, line: str) -> typing.Sequence[typing.Union[str, int]]:
    ret = []
    for match in re.match(regex, line).groups():
        try:
            ret.append(int(match))
        except ValueError:
            ret.append(match)

    return ret


def new_table(val: T, width: int, height: int) -> typing.List[typing.List[T]]:
    return [[val for _ in range(width)] for _ in range(height)]


def transposed(matrix: typing.List[typing.List[T]]) -> typing.List[typing.List[T]]:
    """Returns the transpose of the given matrix."""
    return [list(r) for r in zip(*matrix)]


def rotated(matrix: typing.List[typing.List[T]]) -> typing.List[typing.List[T]]:
    """Returns the given matrix rotated 90 degrees clockwise."""
    return [list(r) for r in zip(*matrix[::-1])]


class PossibilityListList:
    def __init__(self) -> None:
        self.list_of_lists: typing.List[typing.List[int]] = [[]]

    def __repr__(self) -> str:
        return "\n".join(map(lambda x: "".join(map(str, x)), self.list_of_lists))

    def append(self, element: typing.Union[int, typing.List[int]]) -> None:
        if isinstance(element, int):
            for lst in self.list_of_lists:
                lst.append(element)

        else:
            factor = len(element)
            out = []
            for lst in self.list_of_lists:
                for i in range(factor):
                    out.append(deepcopy(lst) + [element[i]])
            self.list_of_lists = out
