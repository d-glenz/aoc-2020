import fileinput
import re

def valid_passport(passport):
    fields = 'byr iyr eyr hgt hcl ecl pid cid'.split()
    required_fields = 'byr iyr eyr hgt hcl ecl pid'.split()

    """byr (Birth Year) - four digits; at least 1920 and at most 2002.
    iyr (Issue Year) - four digits; at least 2010 and at most 2020.
    eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
    hgt (Height) - a number followed by either cm or in:
    If cm, the number must be at least 150 and at most 193.
    If in, the number must be at least 59 and at most 76.
    hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
    ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
    pid (Passport ID) - a nine-digit number, including leading zeroes.
    cid (Country ID) - ignored, missing or not."""
    if len([field for field in required_fields if field in current_data.keys()]) < len(required_fields):
        print("not all fields")
        return False
    if len(passport['byr']) != 4 or not (1920 <= int(passport['byr']) <= 2002):
        print(f"{passport['byr']=}")
        return False
    if len(passport['iyr']) != 4 or not (2010 <= int(passport['iyr']) <= 2020):
        print(f"{passport['iyr']=}")
        return False
    if len(passport['eyr']) != 4 or not (2020 <= int(passport['eyr']) <= 2030):
        print(f"{passport['eyr']=}")
        return False

    try:
        unit = passport['hgt'][-2:]
        height = int(passport['hgt'][:-2])
        if unit not in 'cm in'.split():
            print(f"{unit=}")
            return False
        if unit == "cm":
            if not (150 <= height <= 193):
                print(f"cm {height=}")
                return False
        else:
            if not (59 <= height <= 76):
                print(f"in {height=}")
                return False
    except:
        print(f"{height=}")
        return False


    if len(passport['hcl']) !=7 or passport['hcl'][0] != "#" or not re.match('^[0-9a-f]{6}$', passport['hcl'][1:]):
        print(f"{passport['hcl']=}")
        return False
    if passport['ecl'] not in "amb blu brn gry grn hzl oth".split():
        print(f"{passport['ecl']=}")
        return False
    try:
        int(passport['pid'])
        if len(passport['pid']) != 9:
            print(f"len {passport['pid']=}")
            return False
    except:
        print(f"{passport['pid']=}")
        return False

    return True



valid_passports = 0
all_identities = []
current_data = {}
for line in fileinput.input():
    line = line.strip()
    if line == "":
        if valid_passport(current_data):
            valid_passports +=1
        all_identities.append(current_data)
        current_data = {}
        continue
    for item in line.split():
        k,v = item.split(':')
        current_data[k]=v

print(valid_passports)
