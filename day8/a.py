import fileinput


total = 0
result = []


def read_input():
    result = []
    for i, line in enumerate(fileinput.input()):
        line = line.strip()
        data = line.split()
        print(data)
        result.append(data)
    return result


with open("replace.jmp") as jmp_file:
    for line in jmp_file:
        result = read_input()

        if result[int(line)][0] == 'jmp':
            print(f"REPLACING jmp on {line}")
            result[int(line)] = ('nop', result[int(line)][1])
        else:
            print(f'wrong line {result[int(line)][0]}')

        # start
        ip = 0
        prev_ip = None
        run_before = []
        global_var = 0
        while True:
            if ip in run_before:
                print(f"runnning {ip} a second time {prev_ip=}")
                normal = False
                break
            if ip >= len(result):
                print("terminating normally")
                normal = True
                break

            run_before.append(ip)
            instruction, arg = result[ip]
            prev_ip = ip
            print(f"{instruction=}, {arg=}")
            if instruction == 'acc':
                global_var += int(arg)
                print(f"{global_var=} += {int(arg)=}")
                ip += 1
            elif instruction == 'jmp':
                print(f"{ip=} += {int(arg)=}")
                ip += int(arg)
            elif 'nop':
                ip += 1

        if normal:
            print(global_var)
            exit(0)
