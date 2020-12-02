import fileinput

correct_passwords=0

def logical_xor(a, b):
    return (a and not b) or (not a and b)

for line in fileinput.input():
    occ, letter, passw = line.split()
    letter = letter.strip(':')
    first_index, second_index = occ.split('-')
    correct_passwords += 1 if logical_xor(passw[int(first_index)-1] == letter, 
                                          passw[int(second_index)-1] == letter) else 0

print(correct_passwords)
