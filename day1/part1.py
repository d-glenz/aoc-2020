import fileinput
from typing import Set, TextIO, Optional, Union

def main(input_file: Union[TextIO, fileinput.FileInput]) -> Optional[int]:
    expenses: Set[int] = set()
    target_number = 2020

    for line in input_file:
        num = int(line)
        if (target_number - num) in expenses:
            return num*(target_number-num)

        expenses.add(num)
    return None

if __name__ == "__main__":
    assert main(open("input1.test")) == 514579, "Test case did not pass"
    print(main(fileinput.input()))
