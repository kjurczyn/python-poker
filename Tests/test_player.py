from Poker.player import Player


def test_player_constructor():
    player1 = Player("Jan Kowalski")
    assert player1.getMoney() == 10000
    assert player1.getName() == "Jan Kowalski"
    assert player1.getHand() == []

# TODO: add more tests for bet
def test_bet():
    player1 = Player("Jan Kowalski")
    a = player1.bet(3000)
    assert a == 3000
    assert player1.getMoney() == 7000