import math
import fileinput
import re
from typing import Dict, List, TypeVar, Tuple, Set, NewType

T = TypeVar('T')
S = TypeVar('S')
Ticket = NewType('Ticket', List[int])


def ints(s: str) -> List[int]:
    return list(map(int, re.findall(r"-?\d+", s)))


class Range:
    def __init__(self, _range: List[str]):
        self.start, self.end = int(_range[0]), int(_range[1])

    def __contains__(self, a: int) -> bool:
        return self.start <= a <= self.end

    def __repr__(self) -> str:
        return f"R[{self.start}, {self.end}]"


def parse_field_rules(line: str,
                      ranges: List[Range],
                      field_rules: Dict[str, List[Range]]) -> Tuple[List[Range], Dict[str, List[Range]]]:
    rule_ranges = [Range(_range.split('-')) for _range in line.split(':')[-1].strip().split(' or ')]
    ranges += rule_ranges
    field_rules[line.split(':')[0]] = rule_ranges
    return ranges, field_rules


def filter_ticket(ticket: Ticket,
                  ranges: List[Range],
                  error_nums: List[int],
                  valid_other_tickets: List[Ticket]) -> Tuple[List[int], List[Ticket]]:
    discard_ticket = False
    if ticket == []:
        return (error_nums, valid_other_tickets)

    for entry in ticket:
        no_member = False
        for _range in ranges:
            if entry in _range:
                no_member = True
        if not no_member:
            error_nums.append(entry)
            discard_ticket = True

    if not discard_ticket:
        valid_other_tickets.append(ticket)
    return error_nums, valid_other_tickets


def parse_input() -> Tuple[List[int], Dict[str, List[Range]], List[Ticket], Ticket]:
    error_nums: List[int] = []
    ranges: List[Range] = []
    valid_other_tickets: List[Ticket] = []
    mine: Ticket = Ticket([])
    field_rules: Dict[str, List[Range]] = {}
    current_section = 0
    sections = 'field_rules mine others'.split()
    for i, line in enumerate(fileinput.input()):
        line = line.strip()
        if line == "":
            current_section += 1
            continue

        ticket = Ticket(ints(line))
        if sections[current_section] == 'field_rules':
            ranges, field_rules = parse_field_rules(line, ranges, field_rules)

        elif sections[current_section] == 'mine':
            if ticket == []:
                continue
            mine = ticket

        else:
            error_nums, valid_other_tickets = filter_ticket(ticket, ranges, error_nums, valid_other_tickets)

    return (error_nums, field_rules, valid_other_tickets, mine)


def rule_out_possibilities(field_rules: Dict[str, List[Range]], other_tickets: List[Ticket]) -> Dict[str, Set[str]]:
    fields = list(field_rules.keys())
    column_posssibilities = {str(col): set(fields) for col in range(len(fields))}

    for ticket in other_tickets:
        for column, entry in enumerate(ticket):
            for rule_name, rules in field_rules.items():
                if not any(entry in individual_rule for individual_rule in rules):
                    column_posssibilities[str(column)] -= set([rule_name])
    return column_posssibilities


def assign_fields(column_possibilities: Dict[str, Set[str]]) -> Tuple[Dict[str, str], Set[str]]:
    assigned_fields: Set[str] = set()
    column_assignments = {}
    for column_num, possibilities in sorted(column_possibilities.items(), key=lambda p: len(p[1])):
        possibilities -= assigned_fields
        if len(possibilities) == 1:
            assigned = list(possibilities)[0]
            column_assignments[assigned] = str(column_num)
            assigned_fields.add(assigned)
    return column_assignments, assigned_fields


def main() -> None:
    error_nums, field_rules, other_tickets, mine = parse_input()
    print(f"Solution 1: {sum(error_nums)}")

    column_posssibilities = rule_out_possibilities(field_rules, other_tickets)
    column_assignments, assigned_fields = assign_fields(column_posssibilities)
    solution2 = math.prod([mine[int(entry)]
                           for name, entry in column_assignments.items()
                           if name.startswith('departure')])
    print(f"Solution 2: {solution2}")


if __name__ == "__main__":
    main()
