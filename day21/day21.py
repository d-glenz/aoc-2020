import fileinput
from collections import defaultdict

import typing


T = typing.TypeVar('T')


def lmap(func, *iterables) -> typing.List[T]:
    return list(map(func, *iterables))


def determine_causes(ingredients_per_allergen:
                     typing.DefaultDict[str, typing.List[typing.Set[str]]]) -> typing.Dict[str, str]:
    allergy_cause = {}
    likely_allergy_cause = {}

    for allergy, sets_of_ingredients in ingredients_per_allergen.items():
        causing_the_allergy = set(sets_of_ingredients[0])
        for ingredient_set in sets_of_ingredients:
            causing_the_allergy = causing_the_allergy.intersection(ingredient_set)
        if len(causing_the_allergy) == 1:
            allergy_cause[allergy] = list(causing_the_allergy)[0]
        else:
            likely_allergy_cause[allergy] = causing_the_allergy

    while True:
        for allergy, likely_causes in likely_allergy_cause.items():
            if len(likely_causes - set(allergy_cause.values())) == 1:
                allergy_cause[allergy] = list(likely_causes - set(allergy_cause.values()))[0]
        if len(list(ingredients_per_allergen.keys())) == len(list(allergy_cause.keys())):
            break
    return allergy_cause


def solution1(all_ingredients: typing.Set[str],
              causes: typing.Dict[str, str],
              ingredient_lists: typing.List[typing.List[str]]) -> int:
    total = 0
    non_allergen = list(all_ingredients - set(causes.values()))

    for ingredients in ingredient_lists:
        for ingredient in ingredients:
            if ingredient in non_allergen:
                total += 1
    return total


def solution2(causes: typing.Dict[str, str]) -> str:
    return ','.join(lmap(lambda a: a[1], sorted(causes.items())))


def main() -> None:
    ingredients_per_allergen: typing.DefaultDict[str, typing.List[typing.Set[str]]] = defaultdict(list)
    all_ingredients: typing.Set[str] = set()
    ingredient_lists: typing.List[typing.List[str]] = []

    for i, line in enumerate(fileinput.input()):
        line = line.strip()
        ing, aller = line.split('(')
        ingredients = ing.split()
        all_ingredients.update(ingredients)
        ingredient_lists.append(ingredients)
        allergens: typing.List[str] = lmap(lambda x: x.strip(',').strip(')'), aller.split()[1:])

        for allergen in allergens:
            ingredients_per_allergen[allergen].append(set(ingredients))

    causes = determine_causes(ingredients_per_allergen)

    print(f"Solution 1: {solution1(all_ingredients, causes, ingredient_lists)}")
    print(f"Solution 2: {solution2(causes)}")


if __name__ == "__main__":
    main()
