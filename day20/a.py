from pprint import pprint
import fileinput
from collections import Counter, defaultdict


def prep():
    result = defaultdict(list)
    field_n = 0
    for i, line in enumerate(fileinput.input()):
        line = line.strip()

        if line == '':
            field_n += 1
        elif line.startswith('Tile'):
            last_title = (line.split()[-1][:-1])
        else:
            result[last_title].append(line)
    return result


def edges(field):
    top, *_, bottom = field
    lr_array = [(row[0], row[-1]) for row in field]
    left = ''.join([a for a, _ in lr_array])
    right = ''.join([b for _, b in lr_array])
    return (top, left, bottom, right)


def inner(field):
    return [[col for col in row[1:-1]] for row in field[1:-1]]


def prep_all_edges(result):
    all_edges = defaultdict(list)
    for tile, field in result.items():
        t, l, b, r = edges(field)
        all_edges[t].append(tile+'t')
        all_edges[l].append(tile+'l')
        all_edges[b].append(tile+'b')
        all_edges[r].append(tile+'r')
        if False:
            all_edges[''.join(reversed(t))].append(tile+'r')
            all_edges[''.join(reversed(l))].append(tile+'r')
            all_edges[''.join(reversed(b))].append(tile+'r')
            all_edges[''.join(reversed(r))].append(tile+'r')
    return all_edges


def unpaired(all_edges):
    return dict(filter(lambda i: len(i[1]) == 1, all_edges.items()))


def solution1():
    all_edges = prep_all_edges()
    # pprint(dict(all_edges))

    unpaired_edges = unpaired(all_edges)

    return Counter(map(str, map(lambda x: x[0], unpaired_edges.values())))


result = prep()
print(f"num tiles {len(result)}")
all_edges = prep_all_edges(result)
tile_edges = defaultdict(dict)
for edge, tiles in all_edges.items():
    for tile in tiles:
        tile_edges[tile[:-1]][tile[-1]] = edge

tiles_from_unpaired = defaultdict(list)
for tile in unpaired(all_edges).values():
    *tile_name, side = tile[0]
    tiles_from_unpaired[''.join(tile_name)].append(side)

pprint(tile_edges)
pprint(all_edges)
pprint(tiles_from_unpaired)


start_tile = None
for tile, _edges in tiles_from_unpaired.items():
    if not start_tile:
        if len(_edges) == 2:
            if _edges in (['t', 'l'], ['l', 't']):
                print(f"Start tile: {tile}")
                start_tile = tile

    if start_tile:
        bottom_edge = tile_edges[start_tile]['b']
        right_edge = tile_edges[start_tile]['r']
        bottom_ext = [tile for tile in all_edges[bottom_edge] if not tile.startswith(start_tile)][0]
        right_ext = [tile for tile in all_edges[right_edge] if not tile.startswith(start_tile)][0]
        print(f"bottom extension of {start_tile} (using {bottom_edge}): {bottom_ext}")
        print(f"right extension of {start_tile} (using {right_edge}): {right_ext}")
        break
