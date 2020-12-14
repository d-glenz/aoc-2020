import fileinput
from typing import List


def apply_mask(num: int, mask: str) -> int:
    num_b = f"{num:0>{len(mask)}b}"
    out = ''
    for i in range(len(mask)):
        if mask[i] == '0':
            out += '0'
        elif mask[i] == '1':
            out += '1'
        else:
            out += num_b[i]
    return int(out, base=2)


def apply_mask2(num: int, mask: str) -> List[int]:
    num_b = f"{num:0>{len(mask)}b}"
    out_arr = ['']
    for i in range(len(mask)):
        tmp = []
        for j in range(len(out_arr)):
            if mask[i] == '0':
                out_arr[j] = out_arr[j] + num_b[i]
            elif mask[i] == '1':
                out_arr[j] = out_arr[j] + '1'
            else:
                tmp.append(out_arr[j]+'0')
                out_arr[j] = out_arr[j] + '1'
        out_arr += tmp
    return [int(out, base=2) for out in out_arr]


def main() -> None:
    memory1 = {}
    memory2 = {}
    for line in fileinput.input():
        line = line.strip()
        words = line.split()

        if words[0] == 'mask':
            mask = words[2]

        else:
            num = int(words[2])
            position = int(words[0].split('[')[1].split(']')[0])
            new_num = apply_mask(num, mask)
            positions = apply_mask2(position, mask)
            memory1[position] = new_num
            for position2 in positions:
                memory2[position2] = num

    print(f"Solution 1: {sum(memory1.values())}")
    print(f"Solution 2: {sum(memory2.values())}")


if __name__ == "__main__":
    main()
