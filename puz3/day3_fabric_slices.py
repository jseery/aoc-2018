import re
from typing import List
from itertools import product, filterfalse
from collections import Counter
from functools import partial

# Pattern:
# 1045 @ 558,269: 18x29
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

### TEST CLAIM PARSING ###
test_parsed_claims = [parse_claim(x) for x in TEST_CLAIM_STRINGS]
for claim, answer in zip(test_parsed_claims, TEST_CLAIM_IDS):
    for key in claim:
        assert claim[key] == answer[key]
##########################

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


def test_claim_class():

    list_rectangles = [Claim(claim_string) for claim_string in TEST_CLAIM_STRINGS]

    for l_r, c_s in zip(list_rectangles, claim_strings):
        assert str(l_r) == c_s

    return

def calculate_coord_counts(claims: List[Claim]) -> dict:

    squares_claimed = Counter()

    for claim in claims:
        coords = claim.claim_area()
        squares_claimed.update(coords)

    return squares_claimed

def overlapping_squares(square_claim_clounts: dict) -> list:
    """filter Counter to only overlapping coord keys"""

    # overlapped squares are key with a count > 1
    ov_squares = list(filter(lambda x: square_claim_clounts[x] > 1, square_claim_clounts.keys()))

    return ov_squares

def claim_disputed(claim: Claim, coordinate_counts: Counter) -> bool:

    ### for one claim, cycle through all of its coordinates
    ### lookup in coordinate counter
    ### if > 1, return False

    has_dispute = any([coordinate_counts[coordinate] for coordinate in claim.coordinates if coordinate_counts[coordinate] > 1])

    return has_dispute


if __name__ == "__main__":
    
    with open('./data.txt','r') as infile:
        lines = infile.read().splitlines()
    
    claims = [Claim(claim_string) for claim_string in lines]

    coordinate_counts = calculate_coord_counts(claims)
    disputed_squares = overlapping_squares(coordinate_counts)
    
    answer1 = len(disputed_squares)
    print(answer1)

    puz3 = partial(claim_disputed, coordinate_counts=coordinate_counts)

    undisputed_claims = filterfalse(puz3, claims)

    for c in undisputed_claims:
        print(c)


    pass
