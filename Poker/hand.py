from sys import path
from pathlib import Path
from typing import List, Tuple, Union
from itertools import combinations
path[0] = str(Path(path[0]).parent)
from Poker.card import Card
del path


hands = {
    1: "Royal Flush",
    2: "Straight Flush",
    3: "Four of a Kind",
    4: "Full House",
    5: "Flush",
    6: "Straight",
    7: "Three of a Kind",
    8: "Two Pair",
    9: "One Pair",
    10: "High Card"
}


def isSameSuit(cards: List[Card]) -> bool:
    """Takes a list of cards and checks whether they're of the same suit."""
    first_card_suit = cards[0].getSuit()
    for i in cards[1:]:
        if i.getSuit() != first_card_suit:
            return False
    return True


def isSameValue(cards: List[Card]) -> bool:
    """Takes a list of cards and checks whether they're the same value."""
    for i in cards[1:]:
        if i != cards[0]:
            return False
    return True


def isInRow(cards: List[Card]) -> bool:
    """Takes a list of cards sorted in descending order and checks wether they're in row."""
    for i in range(len(cards)-1):
        if cards[i].getValue()-1 != cards[i+1].getValue():
            return False
    return True


def determineHandType(cards: List[Card]) -> Tuple[int, Union[tuple, int]]:
    """Takes in a list of at least 5 cards and returns the hand type and value of high card/s of the hand.
     Hand types:
        1: Royal Flush
        2: Straight Flush
        3: Four of a Kind
        4: Full House
        5: Flush
        6: Straight
        7: Three of a Kind
        8: Two Pair
        9: One Pair
        10: High Card"""
    cards.sort(reverse=True)
    # check for royal  and straight flushes
    if x := checkForRoyalAndStraightFlush(cards):
        return x
    # 4 of a kind
    if x := checkForFour(cards):
        return x
    # detect 3 and pairs
    # three
    three = checkForThree(cards)
    # pairs
    pairs = checkForPairs(cards, three)
    # full house
    if x := checkForFullHouse(cards, pairs, three):
        return x
    # flush
    if x := checkForFlush(cards):
        return x
    # straight
    if x := checkForStraight(cards):
        return x
    # three
    if three:
        return 7, cards[three[0]].getValue()
    # two pair
    if len(pairs) >= 2:
        return 8, (pairs[0].getValue(), pairs[1].getValue())
    # one pair
    if len(pairs) == 1:
        return 9, pairs[0].getValue()
    # high card
    return 10, cards[0].getValue()


def checkForPairs(cards: List[Card], three: tuple) -> List[Card]:
    pairs: List[Card] = []
    for i in range(len(cards)-1):
        if isSameValue(cards[i:i+2]) and (not three or (three and not(three[0] <= i and three[1] >= i+2))):
            pairs.append(cards[i])
    pairs.sort(reverse=True)
    return pairs


def checkForThree(cards: List[Card]) -> tuple:
    three: tuple = None
    for i in range(len(cards)-2):
        if isSameValue(cards[i:i+3]) and (not three or cards[i].getValue() > cards[three[0]].getValue()):
            three = (i, i+3)
    return three


def checkForRoyalAndStraightFlush(cards: List[Card]):
    cards_in_row_same_suit = []
    for i in range(1, 5):
        temp = [y for y in cards if y.getSuit() == i]
        if len(temp) >= 5:
            for i in range(len(temp)-4):
                if isInRow(temp[i:i+5]):
                    cards_in_row_same_suit.append(temp[i:i+5])
    if len(cards_in_row_same_suit) > 0:
        temp = max([i[0] for i in cards_in_row_same_suit]).getValue()
        return (1, 14) if temp == 14 else (2, temp)
    return None


def checkForFour(cards: List[Card]) -> tuple:
    for i in range(len(cards)-3):
        if isSameValue(cards[i:i+4]):
            return 3, cards[i].getValue()


def checkForFullHouse(cards: List[Card], pairs: List, three: tuple) -> tuple:
    if three and len(pairs) > 0:
        return 4, (cards[three[0]].getValue(), pairs[0].getValue())


def checkForFlush(cards: List[Card]) -> tuple:
    cards_with_same_suit = []
    for i in combinations(cards, 5):
        if isSameSuit(i):
            cards_with_same_suit.append(sorted(i, reverse=True))
    if len(cards_with_same_suit) > 0:
        return 5, max(cards_with_same_suit, key=lambda i: i[0])[0].getValue()


def checkForStraight(cards: List[Card]) -> tuple:
    for i in range(len(cards)-4):
        if isInRow(cards[i:i+5]):
            return 6, cards[i].getValue()
