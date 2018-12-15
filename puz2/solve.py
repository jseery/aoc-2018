from collections import Counter
import pandas as pd
import funcs

with open('./puz2-data.txt', 'r') as infile:
    data = infile.read().splitlines()

box_collection = {}

for box_id in data:
    box_collection[box_id] = dict(Counter(box_id))

df = pd.DataFrame.from_dict(box_collection, orient='index')

has_counts = df.fillna(0) \
    .astype(int) \
    .assign(two = lambda x: (x.values == 2).any(axis=1)) \
    .assign(three = lambda x: (x.values == 3).any(axis=1))

answer1 = has_counts[['two','three']].sum().product()

print(f"puz2, part1: {answer1}")

sboxes = sorted(data)

for zipped_elems in funcs.pairwise(sboxes):
    same_chars = ''.join([x for x, y in zip(*zipped_elems) if x.lower() == y.lower()])
    if len(same_chars) == 25:
        answer2 = same_chars

print(f"puz2: part2: {answer2}")