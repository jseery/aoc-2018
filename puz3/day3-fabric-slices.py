import re
from typing import List

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
    "#123 @ 25,25: 100x450",
    "#12 @ 1,1: 100x100"
]

TEST_CLAIM_IDS = [
    "1",
    "2",
    "3",
    "123",
    "12"
]

test_parsed_claims = [parse_claim(x) for x in TEST_CLAIM_STRINGS]
print(*test_parsed_claims, sep='\n')

for claim, answer in zip(test_parsed_claims, TEST_CLAIM_IDS):
    print(claim['claim_id'], answer)
    assert claim['claim_id'] == answer

