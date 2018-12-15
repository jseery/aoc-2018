from itertools import *
from functools import reduce
from collections import defaultdict

with open('./data.txt','r') as infile:
    data = [int(x) for x in infile.read().split('\n')]

answer1 = list(accumulate(data))[-1]

print(f"puz1, answer1: {answer1}")

frequencies_ordered = list(accumulate(chain.from_iterable(repeat(data, 1000))))

d = defaultdict(int)

for freq in frequencies_ordered:
    d[freq] += 1
    if d[freq] > 1:
        answer2 = freq
        break


print(f"puz2, answer2: {answer2}")
