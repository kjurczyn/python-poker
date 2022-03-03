from Poker.card import Card
from Poker.game import Game
from Poker.player import Player


def test_init():
    player1 = Player('Jan Kowalski')
    player2 = Player('Janina Kowalska')
    player3 = Player('Adam Nowak')
    player4 = Player('Anna Nowak')
    player5 = Player('Juliusz Cezar')
    player6 = Player('Mieszko I')
    game1 = Game([player1, player2, player3, player4, player5, player6])
    assert game1


def test_newRound():
    player1 = Player('Jan Kowalski')
    player2 = Player('Janina Kowalska')
    player3 = Player('Adam Nowak')
    player4 = Player('Anna Nowak')
    player5 = Player('Juliusz Cezar')
    player6 = Player('Mieszko I')
    game1 = Game([player1, player2, player3, player4, player5, player6])
    game1.newRound()
    assert len(game1._table) == 3
    for i in game1._players:
        assert len(i.getHand()) == 2
    assert player1.getBlind() == 0
    assert player2.getBlind() == 1
    assert player3.getBlind() == 2


def test_determineWinner_straight_flush():
    player1 = Player('Jan Kowalski')
    player2 = Player('Janina Kowalska')
    player3 = Player('Adam Nowak')
    player4 = Player('Anna Nowak')
    player5 = Player('Juliusz Cezar')
    player6 = Player('Mieszko I')
    game1 = Game([player1, player2, player3, player4, player5, player6])
    player1._hand = [Card(1, 9), Card(1, 10)]
    player2._hand = [Card(1, 4), Card(1, 5)]
    player3._hand = [Card(4, 14), Card(3, 10)]
    player4._hand = [Card(3, 5), Card(2, 8)]
    player5._hand = [Card(4, 7), Card(4, 8)]
    player6._hand = [Card(1, 10), Card(2, 13)]
    game1._table = [Card(1, 6), Card(1, 7), Card(1, 8), Card(2, 10), Card(4, 9)]
    assert game1.determineWinner().getName() == player1.getName()


def test_determineWinner_pair():
    player1 = Player('Jan Kowalski')
    player2 = Player('Janina Kowalska')
    player3 = Player('Adam Nowak')
    player4 = Player('Anna Nowak')
    player5 = Player('Juliusz Cezar')
    player6 = Player('Mieszko I')
    game1 = Game([player1, player2, player3, player4, player5, player6])
    player1._hand = [Card(1, 9), Card(1, 6)]
    player2._hand = [Card(1, 4), Card(1, 5)]
    player3._hand = [Card(3, 13), Card(3, 10)]
    player4._hand = [Card(3, 2), Card(2, 3)]
    player5._hand = [Card(4, 5), Card(4, 4)]
    player6._hand = [Card(1, 14), Card(2, 13)]
    game1._table = [Card(2, 14), Card(1, 7), Card(1, 8), Card(2, 10), Card(4, 9)]
    assert game1.determineWinner().getName() == player6.getName()


def test_determineWinner_two_pair():
    player1 = Player('Jan Kowalski')
    player2 = Player('Janina Kowalska')
    player3 = Player('Adam Nowak')
    player4 = Player('Anna Nowak')
    player5 = Player('Juliusz Cezar')
    player6 = Player('Mieszko I')
    game1 = Game([player1, player2, player3, player4, player5, player6])
    player1._hand = [Card(1, 9), Card(1, 6)]
    player2._hand = [Card(1, 4), Card(1, 5)]
    player3._hand = [Card(3, 14), Card(3, 10)]
    player4._hand = [Card(3, 2), Card(2, 3)]
    player5._hand = [Card(4, 5), Card(4, 4)]
    player6._hand = [Card(1, 14), Card(2, 13)]
    game1._table = [Card(2, 14), Card(1, 7), Card(1, 8), Card(2, 10), Card(4, 9)]
    assert game1.determineWinner().getName() == player3.getName()


def test_detrmineWinner_tie_straight():
    player1 = Player('Jan Kowalski')
    player2 = Player('Janina Kowalska')
    player3 = Player('Adam Nowak')
    player4 = Player('Anna Nowak')
    player5 = Player('Juliusz Cezar')
    player6 = Player('Mieszko I')
    game1 = Game([player1, player2, player3, player4, player5, player6])
    player1._hand = [Card(1, 2), Card(1, 6)]
    player2._hand = [Card(1, 4), Card(1, 5)]
    player3._hand = [Card(3, 12), Card(3, 6)]
    player4._hand = [Card(3, 5), Card(2, 3)]
    player5._hand = [Card(4, 5), Card(4, 11)]
    player6._hand = [Card(1, 14), Card(2, 11)]
    game1._table = [Card(2, 13), Card(1, 7), Card(1, 8), Card(2, 10), Card(4, 9)]
    winners = game1.determineWinner()
    for i in [player5, player6]:
        assert i in winners


def test_determineWinner_high_card():
    player1 = Player('Jan Kowalski')
    player2 = Player('Janina Kowalska')
    player3 = Player('Adam Nowak')
    player4 = Player('Anna Nowak')
    player5 = Player('Juliusz Cezar')
    player6 = Player('Mieszko I')
    game1 = Game([player1, player2, player3, player4, player5, player6])
    player1._hand = [Card(1, 2), Card(1, 3)]
    player2._hand = [Card(1, 11), Card(1, 6)]
    player3._hand = [Card(3, 12), Card(3, 6)]
    player4._hand = [Card(2, 8), Card(2, 3)]
    player5._hand = [Card(4, 6), Card(4, 11)]
    player6._hand = [Card(1, 14), Card(2, 11)]
    game1._table = [Card(2, 13), Card(3, 5), Card(4, 7), Card(2, 4), Card(4, 9)]
    assert game1.determineWinner().getName() == player6.getName()


# def test_continueGame():
#     player1 = Player('Jan Kowalski')
#     player2 = Player('Janina Kowalska')
#     player3 = Player('Adam Nowak')
#     player4 = Player('Anna Nowak')
#     player5 = Player('Juliusz Cezar')
#     player6 = Player('Mieszko I')
#     game1 = Game([player1, player2, player3, player4, player5, player6])
#     assert next(game1.continueGame())[0] == player1
#     assert next(game1.continueGame())[0] == player2
#     player2.passRound()
#     assert next(game1.continueGame())[0] == player3
#     assert next(game1.continueGame())[0] == player4
#     assert next(game1.continueGame())[0] == player5
#     assert next(game1.continueGame())[0] == player6
#     assert len(game1._current_players) == 5