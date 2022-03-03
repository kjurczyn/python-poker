from Poker.card import Card
import Poker.hand


def test_isInRow():
    a = Card(1, 2)
    b = Card(2, 3)
    c = Card(3, 4)
    d = Card(2, 5)
    e = Card(1, 6)

    f = Card(4, 14)

    assert Poker.hand.isInRow([e, d, c, b, a])
    assert not Poker.hand.isInRow([a, b, c, d, f])


def test_isSameSuit():
    a = Card(1, 2)
    b = Card(1, 2)
    c = Card(1, 3)
    d = Card(1, 2)
    e = Card(1, 7)

    f = Card(3, 13)

    assert Poker.hand.isSameSuit([a, b, c, d, e])
    assert not Poker.hand.isSameSuit([a, b, c, d, f])


def test_isSameValue():
    a = Card(1, 2)
    b = Card(2, 2)
    c = Card(3, 2)
    d = Card(4, 2)
    e = Card(1, 7)

    assert Poker.hand.isSameValue([a, b, c, d])
    assert not Poker.hand.isSameValue([a, b, c, e])


def test_determine_hand_type():
    a = Card(1, 10)
    b = Card(1, 11)
    c = Card(1, 12)
    d = Card(1, 13)
    e = Card(1, 14)
    f = Card(4, 14)
    g = Card(1, 9)
    h = Card(2, 14)
    i = Card(3, 14)
    j = Card(2, 9)
    k = Card(1, 6)
    l_card = Card(1, 4)
    m = Card(2, 10)
    n = Card(3, 11)

    assert Poker.hand.determineHandType([a, b, c, d, e, f, g])[0] == 1
    assert Poker.hand.determineHandType([a, b, c, d, g, h, n])[0] == 2
    assert Poker.hand.determineHandType([f, h, i, d, e, n, a])[0] == 3
    assert Poker.hand.determineHandType([f, h, g, j, e, n, a])[0] == 4
    assert Poker.hand.determineHandType([a, l_card, c, d, e, h, i])[0] == 5
    assert Poker.hand.determineHandType([m, n, c, d, f, k, l_card])[0] == 6
    assert Poker.hand.determineHandType([Card(1, 2), Card(2, 2), Card(3, 2), Card(4, 5), Card(4, 10), Card(3, 14)])[0] == 7
    assert Poker.hand.determineHandType([g, j, e, f, n, Card(4, 3), Card(4, 10)])[0] == 8
    assert Poker.hand.determineHandType([a, b, c, f, e, Card(2, 3), Card(4, 2)])[0] == 9
    assert Poker.hand.determineHandType([a, b, j, k, e, Card(4, 5), Card(3, 4)])[0] == 10
