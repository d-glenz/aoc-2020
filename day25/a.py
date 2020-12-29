import fileinput


def transform_subject_number(subject_number, loop_size):
    return pow(subject_number, loop_size, 20201227)


card_public_key, door_public_key = [int(line.strip()) for i, line in enumerate(fileinput.input())]

for bignum in [10000, 100000, 1000000, 10000000]:
    try:
        for card_loop_size in range(bignum):
            card_public_key_attempt = transform_subject_number(7, card_loop_size)
            if card_public_key_attempt == card_public_key:
                break
        else:
            raise ValueError()
        print(f"{card_loop_size=}")

        for door_loop_size in range(bignum):
            door_public_key_attempt = transform_subject_number(7, door_loop_size)
            if door_public_key_attempt == door_public_key:
                break
        else:
            raise ValueError()
        print(f"{door_loop_size=}")
        break
    except ValueError:
        print(f"{bignum=} not correct")


encryption_key = transform_subject_number(door_public_key, card_loop_size)
print(f"{encryption_key}")

encryption_key2 = transform_subject_number(card_public_key, door_loop_size)
print(f"{encryption_key2}")

assert encryption_key == encryption_key2
