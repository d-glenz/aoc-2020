import re
import fileinput
from itertools import takewhile, dropwhile
from typing import List, Union, Tuple, Dict
from copy import deepcopy

MAXDEPTH = 10


class PossibilityListList:
    def __init__(self) -> None:
        self.list_of_lists: List[List[int]] = [[]]

    def __repr__(self) -> str:
        return "\n".join(map(lambda x: "".join(map(str, x)), self.list_of_lists))

    def append(self, element: Union[int, List[int]]) -> None:
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


class Rule:
    def __init__(self, name: int) -> None:
        self.name: int = name
        self.subrules: List[List[int]] = []
        self.terminals: List[str] = []
        self.expansions: List[int] = []

    def __repr__(self) -> str:
        return f"[{' | '.join(map(lambda x: ' '.join(map(str, x)),self.subrules))}] [{' '.join(self.terminals)}]"

    def add_subrule(self, data: List[int]) -> None:
        self.subrules.append(data)

    def add_terminal(self, data: str) -> None:
        self.terminals.append(data)


def parse_file(part2: bool = False) -> Tuple[Dict[int, Rule], List[str]]:
    messages = []
    all_rules = {}

    rules_section = True
    for i, line in enumerate(fileinput.input()):
        line = line.strip()
        if part2:
            if line.startswith('8: '):
                line = '8: 42 | 42 8'
            if line.startswith('11: '):
                line = '11: 42 31 | 42 11 31'
        data = re.findall(r'\d+|\||"[a-z]"', line)

        if not line:
            rules_section = False
        elif not rules_section:
            messages.append(line)

        if rules_section:
            new_rule = Rule(name=int(data[0]))
            if '"' in data[1]:
                new_rule.add_terminal(data[1].strip('"'))
            else:
                if '|' in data:
                    first, second = takewhile(lambda x: x != '|', data[1:]), dropwhile(lambda x: x != '|', data[1:])
                    new_rule.add_subrule(list(map(int, first)))
                    new_rule.add_subrule(list(map(int, list(second)[1:])))
                else:
                    new_rule.add_subrule(list(map(int, data[1:])))
            all_rules[new_rule.name] = new_rule
    return all_rules, messages


def expand_rule(all_rules: Dict[int, Rule], num: int, depth: int = 0,
                prefix: str = '', suffix: str = '', part2: bool = False) -> str:
    if not all_rules[num].subrules:
        return '|'.join(all_rules[num].terminals)
    if depth > MAXDEPTH:
        return ''
    subrules = []
    for subrule in all_rules[num].subrules:
        options = []
        for option in subrule:
            d = depth + 1 if option == num else depth
            options.append(expand_rule(all_rules, option, depth=d))
        subrules.append(''.join(options))

    return prefix + '(' + '|'.join(subrules) + ')' + suffix


def main(part2: bool) -> None:
    all_rules, messages = parse_file(part2=part2)
    pattern = re.compile(expand_rule(all_rules, 0, prefix='^', suffix='$', part2=part2))

    total = 0
    for message in messages:
        if re.match(pattern, message):
            total += 1

    print(total)


if __name__ == "__main__":
    print("Solution 1: ", end="")
    main(False)
    print("Solution 2: ", end="")
    main(True)
