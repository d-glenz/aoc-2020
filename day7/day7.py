import re
import fileinput
from collections import deque
from typing import Dict, List, Set, Generator, Sequence, Deque


def parse_line(regex: str, line: str) -> Sequence[str]:
    ret: List[str] = []

    if not (matches := re.match(regex, line)):
        return ret

    for match in matches.groups():
        ret.append(match)

    return ret


def find_containers(mapping: Dict[str, List[str]],
                    color: str) -> Generator[str, None, None]:
    for key, values in mapping.items():
        if any(color in item for item in values):
            yield key


def solution1(results: Dict[str, List[str]]) -> Set[str]:
    total = set()
    Q: Deque[str] = deque()
    Q.append('shiny gold bag')
    while Q:
        cont = Q.pop()
        element = " ".join(cont.split()[:-1])
        length = 0
        for container in find_containers(results, element):
            length += 1
            Q.append(container)
        total.add(element)

    total -= {'shiny gold'}
    return total


def find_containing(results: Dict[str, List[str]], bags: str) -> int:
    if bags[-1] != 's':
        bags += 's'
    total2 = 0
    for content in results[bags]:
        try:
            num_, adj, color, bags_w = content.split()
            num = int(num_)
            total2 += num * (1 + find_containing(results,
                                                 ' '.join([adj, color,
                                                           bags_w])))
        except ValueError:
            # no other bags
            pass
    return total2


def prepare_input() -> Dict[str, List[str]]:
    results = {}
    for i, line in enumerate(fileinput.input()):
        line = line.strip().strip('.')
        head, body = parse_line(r'^(.*) contain (.*)$', line)
        contents = body.split(', ')
        results[head] = contents
    return results


def main() -> None:
    results = prepare_input()
    total = solution1(results)
    print(f"Solution 1: {len(total)=}")

    total2 = find_containing(results, 'shiny gold bags')
    print(f"Solution 2: {total2=}")


if __name__ == "__main__":
    main()
