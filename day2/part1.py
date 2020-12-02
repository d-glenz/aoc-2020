import fileinput

correct_passwords=0

for line in fileinput.input():
    occ, letter, passw = line.split()
    letter = letter.strip(':')
    min_occ, max_occ = occ.split('-')
    correct_passwords += 1 if int(min_occ) <= passw.count(letter) <= int(max_occ) else 0

print(correct_passwords)
