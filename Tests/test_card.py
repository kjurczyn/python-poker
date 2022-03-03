from Poker.player import Player
from Poker.card import Card


def test_init():
    card1 = Card(2, 4)

def test_str():
    card1 = Card(1, 2)
    assert str(card1) == 'Clubs Two'