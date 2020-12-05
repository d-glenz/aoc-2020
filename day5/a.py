import os
import sys
import re
import math
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
result = []
table = new_table(None, width=3, height=4)

def subdivide(min_, max_, chr_):
    #print(f"{chr_}: {min_=}, {max_=}")
    if (max_ - min_ ) == 1:
    #    print(f"end: {min_ if chr_ in ('F', 'L') else max_}")
        return min_ if chr_ in ("F", "L") else max_

    half = round((max_ - min_) / 2)
    if chr_ in ("F", "L"):
        return min_, min_ + int(half) - 1
    return max_ - int(half) + 1, max_

for i, line in enumerate(fileinput.input()):
    line = line.strip()
    nums = ints(line)
    data = parse_line(r'', line)

    row = line[:7]
    col = line[7:]

    seat_row = (0, 127)
    for c in row:
        seat_row = subdivide(*seat_row, c)
    #    print(f"{seat_row=} with {c}")

    seat = (0, 7)
    for c in col:
        seat = subdivide(*seat, c)
    #    print(f"{seat=} with {c}")

    seat_id = seat_row * 8 + seat
    #print(f"{seat_row}, {seat}, {seat_id=}")
    result.append(seat_id)

    #if i == 0:
    #    print(data)

min_seat = min(result)
max_seat = max(result)
print(max_seat)

print(set(range(min_seat, max_seat)) - set(result))
