import fileinput
from typing import Dict, Set, Union, Optional, TextIO, DefaultDict, List, Tuple
from collections import defaultdict

def main(input_file: Union[TextIO, fileinput.FileInput]) -> Optional[int]:
    expenses: DefaultDict[int, List[Tuple[int, int]]] = defaultdict(list)
    all_individual_expenses: Set[int] = set()
    target_number = 2020

    for line in input_file:
        num = int(line)
        if (target_number - num) in expenses:
            for n2, n3 in expenses[target_number - num]:
                if n3 == 0:
                    print("two-number case")
                    continue
                return num*n2*n3

        if not expenses.values():
            expenses[num].append((num, 0))
            continue

        for expense in all_individual_expenses:
            expenses[num + expense].append((num, expense))

        all_individual_expenses.add(num)

    return None

if __name__ == "__main__":
    assert main(open("input1.test")) == 241861950, "Test case 1 did not pass"
    print(main(fileinput.input()))
