import fileinput
import re
from typing import Dict

def validate_passport(passport: Dict[str, str], short: bool=False) -> bool:
    """  Requirements:

    byr (Birth Year) - four digits; at least 1920 and at most 2002.
    iyr (Issue Year) - four digits; at least 2010 and at most 2020.
    eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
    hgt (Height) - a number followed by either cm or in:
    If cm, the number must be at least 150 and at most 193.
    If in, the number must be at least 59 and at most 76.
    hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
    ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
    pid (Passport ID) - a nine-digit number, including leading zeroes.
    cid (Country ID) - ignored, missing or not."""

    fields = 'byr iyr eyr hgt hcl ecl pid cid'.split()
    required_fields = 'byr iyr eyr hgt hcl ecl pid'.split()

    if len([field for field in required_fields if field in passport.keys()]) < len(required_fields):
        print("not all fields")
        return False

    if short:
        return True

    if not check_date(passport, 'byr', 4, 1920, 2002):
        return False
    if not check_date(passport, 'iyr', 4, 2010, 2020):
        return False
    if not check_date(passport, 'eyr', 4, 2020, 2030):
        return False

    try:
        unit = passport['hgt'][-2:]
        height = int(passport['hgt'][:-2])
    except:
        print(f"{passport['hgt'][:-2]=}")
        return False

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


    if len(passport['hcl']) !=7 or passport['hcl'][0] != "#" or not re.match('^[0-9a-f]{6}$', passport['hcl'][1:]):
        print(f"{passport['hcl']=}")
        return False
    if passport['ecl'] not in "amb blu brn gry grn hzl oth".split():
        print(f"{passport['ecl']=}")
        return False

    try:
        int(passport['pid'])
    except:
        print(f"{passport['pid']=}")
        return False

    if len(passport['pid']) != 9:
        print(f"len {passport['pid']=}")
        return False

    return True


def check_date(passport: Dict[str, str], key: str, num_digits: int, min_year: int, max_year: int) -> bool:
    if len(passport[key]) != num_digits or not (min_year <= int(passport[key]) <= max_year):
        print(f"{passport[key]=}")
        return False
    return True



def main() -> None:
    valid_passports_1 = 0
    valid_passports_2 = 0
    current_data: Dict[str, str] = {}
    for line in fileinput.input():
        line = line.strip()
        if line == "":
            if validate_passport(current_data, short=True):
                valid_passports_1 +=1
            if validate_passport(current_data):
                valid_passports_2 +=1
            current_data = {}
            continue
        for item in line.split():
            k,v = item.split(':')
            current_data[k]=v

    print(f"Solution 1: {valid_passports_1}")
    print(f"Solution 2: {valid_passports_2}")

if __name__ == "__main__":
    main()
