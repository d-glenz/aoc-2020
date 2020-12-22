import fileinput
from collections import Counter
# ctr = Counter('abcabb') ; Counter({'b': 3, 'a': 2, 'c': 1})

# product('ABCD', repeat=2)                  AA AB AC AD BA BB BC BD CA CB CC CD DA DB DC DD
# permutations('ABCD', 2)                    AB AC AD BA BC BD CA CB CD DA DB DC
# combinations('ABCD', 2)                    AB AC AD BC BD CD
# combinations_with_replacement('ABCD', 2)   AA AB AC AD BB BC BD CC CD DD

from utils import lmap


total = 0
result = []

allergens_per_ingredient = {}
for i, line in enumerate(fileinput.input()):
    line = line.strip()
    ingredients, allergens = line.split('(')
    ingredients = ingredients.split()
    allergens = lmap(lambda x: x.strip(',').strip(')'), allergens.split()[1:])

    for allergen in allergens:
        allergens_per_ingredient[allergen] = {i: 0 for i in ingredients}
        for ingredient in ingredients:
            allergens_per_ingredient[allergen][ingredient] += 1


allergen_container = {}
to_remove = None
prev_len = 0
while len(allergen_container.keys()) != len(allergens_per_ingredient.keys()):
    for allergen, counter in allergens_per_ingredient.items():
        if to_remove is not None:
            for key in (allergens_per_ingredient.keys() - allergen_container.keys()):
                allergens_per_ingredient[key].subtract({to_remove: allergens_per_ingredient[key][to_remove]})
        [(a, b), (c, d)] = Counter(counter).most_common(2)
        if b != d and allergen not in allergen_container:
            print(f"found unique allergen ingredient: {allergen=}, {a} with count {b}")
            allergen_container[allergen] = a
            to_remove = a
    if len(allergen_container.keys()) == prev_len:
        break
    prev_len = len(allergen_container.keys())

all_ingredients = {k for v in allergens_per_ingredient.values() for k in v.keys()}
non_allergen_ingredients = all_ingredients - set(allergen_container.values())
print(f"{non_allergen_ingredients=}")

for _, counter in allergens_per_ingredient.items():
    for non_allergen in non_allergen_ingredients:
        if non_allergen in counter:
            print(_, non_allergen, counter[non_allergen])
            total += counter[non_allergen]

print(total)
