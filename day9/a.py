import os
import sys
import re
import math
from pprint import pprint
import fileinput
from string import ascii_uppercase, ascii_lowercase
from collections import Counter, defaultdict, deque, namedtuple
# ctr = Counter('abcabb') ; Counter({'b': 3, 'a': 2, 'c': 1})

from itertools import count, product, permutations, combinations, combinations_with_replacement
# product('ABCD', repeat=2)                  AA AB AC AD BA BB BC BD CA CB CC CD DA DB DC DD
# permutations('ABCD', 2)                    AB AC AD BA BC BD CA CB CD DA DB DC
# combinations('ABCD', 2)                    AB AC AD BC BD CD
# combinations_with_replacement('ABCD', 2)   AA AB AC AD BB BC BD CC CD DD

import more_itertools as mi

# Grouping                  chunked, ichunked, sliced, distribute, divide, split_at, split_before, split_after, split_into, split_when, bucket, unzip, grouper, partition
# Lookahead and lookback    spy, peekable, seekable
# Windowing                 windowed, substrings, substrings_indexes, stagger, windowed_complete, pairwise
# Augmenting                count_cycle, intersperse, padded, mark_ends, repeat_last, adjacent, groupby_transform, padnone, ncycles
# Combining                 collapse, sort_together, interleave, interleave_longest, zip_offset, zip_equal, dotproduct, flatten, roundrobin, prepend
# Summarizing               ilen, unique_to_each, sample, consecutive_groups, run_length, map_reduce, exactly_n, is_sorted, all_equal, all_unique, first_true, quantify
# Selecting                 islice_extended, first, last, one, only, strip, lstrip, rstrip, filter_except map_except nth_or_last, nth, take, tail, unique_everseen, unique_justseen
# Combinatorics             distinct_permutations, distinct_combinations, circular_shifts, partitions, set_partitions, powerset, random_product, random_permutation,
#                           random_combination, random_combination_with_replacement, nth_product nth_permutation nth_combination
# Wrapping                  always_iterable, always_reversible, consumer, with_iter, iter_except
# Others                    locate, rlocate, replace, numeric_range, side_effect, iterate, difference, make_decorator, SequenceView, time_limited, consume, tabulate, repeatfunc

from utils import lmap, flatten, ints, words, fst, snd, parse_line, LETTERS, CONSONANTS, VOWELS, new_table, transposed, rotated



total = 0
all_nums = []
result = []
table = new_table(None, width=3, height=4)

length = 25

for i, line in enumerate(fileinput.input()):
    line = line.strip()
    nums = ints(line)
    data = parse_line(r'', line)

    if len(result) == length:
        num = nums[0]
        r_set = set(result)
        valid = False
        for n in r_set:
            if n >= num:
                continue
            if (num - n) in (r_set - {n}):
                # valid
                valid = True
                break
        if not valid:
            invalid = num
            print(f"not valid {num}")

    result.append(nums[0])
    if len(result) > length:
        result.pop(0)

    all_nums.append(nums[0])

chain = []
for i, start_num in enumerate(all_nums):
    target = invalid
    # print("new")
    for j, subtrahend in enumerate(all_nums[i:]):
        target -= subtrahend
        # print(f"{target=} -= {subtrahend=}")
        if target < 0:
            # chain not correct
            break
        elif target == 0:
            # chain correct
            chain = all_nums[i:i+j+1]
            break
    if chain:
        break
print(chain)
print(min(chain) + max(chain))
