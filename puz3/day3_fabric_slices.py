import re
from typing import List
from itertools import product
from collections import Counter

with open('./data.txt','r') as infile:
    lines = infile.read().splitlines()


#1045 @ 558,269: 18x29

CLAIM_REGEX = re.compile("#([0-9]+) @ ([0-9]+),([0-9]+): ([0-9]+)x([0-9]+)")

def parse_claim(claim_string: str) -> dict:
    
    claim_match = re.search(CLAIM_REGEX, claim_string)
    
    if not claim_match:
        print("No match!")
        return {}
    else:
        parsed_claim = {
            'claim_id':claim_match.group(1),
            'left_edge':claim_match.group(2),
            'top_edge':claim_match.group(3),
            'width':claim_match.group(4),
            'height':claim_match.group(5)
        }
        return parsed_claim

TEST_CLAIM_STRINGS = [
    "#1 @ 1,3: 4x4",
    "#2 @ 3,1: 4x4",
    "#3 @ 5,5: 2x2",
]

TEST_CLAIM_IDS = [
    {"claim_id":'1', 'left_edge':'1', 'top_edge':'3', 'width':'4', 'height':'4'},
    {"claim_id":'2', 'left_edge':'3', 'top_edge':'1', 'width':'4', 'height':'4'},
    {"claim_id":'3', 'left_edge':'5', 'top_edge':'5', 'width':'2', 'height':'2'},
]

TEST_OVERLAPPED_SQS = [
    (4, 4),
    (4, 5),
    (5, 4),
    (5, 5)
]

test_parsed_claims = [parse_claim(x) for x in TEST_CLAIM_STRINGS]
# print(*test_parsed_claims, sep='\n')


for claim, answer in zip(test_parsed_claims, TEST_CLAIM_IDS):
    for key in claim:
        assert claim[key] == answer[key]


class Claim(object):

    def __init__(self, claim_string):
        self.params = parse_claim(claim_string)

        self.claim_id = int(self.params.get('claim_id'))
        self.left_edge = int(self.params.get('left_edge'))
        self.top_edge = int(self.params.get('top_edge'))
        self.width = int(self.params.get('width'))
        self.height = int(self.params.get('height'))

    def __repr__(self):
        return "#{claim_id} @ {left_edge},{top_edge}: {width}x{height}".format(**self.params)

    def claim_area(self):

        self.x_range = [x for x in range(self.left_edge+1, self.left_edge + self.width + 1)]

        self.y_range = [y for y in range(self.top_edge + 1, self.top_edge + self.height + 1)]

        self.coordinates = list(product(self.x_range, self.y_range))

        return self.coordinates

def test_claim_class(claim_strings):

    list_rectangles = [Claim(claim_string) for claim_string in claim_strings]

    for l_r, c_s in zip(list_rectangles, claim_strings):
        assert str(l_r) == c_s

    return

try:
    test_claim_class(TEST_CLAIM_STRINGS)
    print("Claim() tests pass.")
except AssertionError:
    print("error")

def calculate_overlaps(claims: List[Claim]) -> dict:

    squares_claimed = Counter()

    for claim in claims:
        coords = claim.claim_area()
        squares_claimed.update(coords)

    return squares_claimed

def test_overlaps():

    list_claims = [Claim(claim_string) for claim_string in TEST_CLAIM_STRINGS]

    sq_claim_counts = calculate_overlaps(list_claims)

    # overlapped squares are key with a count > 1
    ov_squares = list(filter(lambda x: sq_claim_counts[x] > 1, sq_claim_counts.keys()))


    assert set(ov_squares) == set(TEST_OVERLAPPED_SQS)

    return

test_overlaps()


list_claims = [Claim(claim_string) for claim_string in lines]
sq_claim_counts = calculate_overlaps(list_claims)

ov_squares = list(filter(lambda x: sq_claim_counts[x] > 1, sq_claim_counts.keys()))

answer1 = len(ov_squares)
print(answer1)


    



