from random import choices, randrange, choice
from typing import Tuple
from sys import path
from pathlib import Path
path[0] = str(Path(path[0]).parent)
from Poker.game import Game
from Poker.card import Card
from Poker.hand import determineHandType
from Poker.player import Player
del path

def makeChoice(player: Player, game: Game) -> Tuple[str, int]:
    """Takse in a Player object and a Game object. Returns a tuple containing the best choice and an amount of money."""
    # choice id: 1 - Fold, 2 - Check, 3 - Call, 4 - Raise, 5 - all in
    money = player.getMoney()
    hand = player.getHand() + game.getTable()
    options = game.getOptionsFor(player)
    hand_type = determineHandType(hand)
    highest_bet = game.getPots()[player.getCurrentPot()][0]
    current_bet = player.getCurrentBet()
    if money > highest_bet-current_bet and 6 < hand_type[0] < 10:
        if 'Call' in options and 'Raise' in options and money > 500:
            bot_choice = choices([3, 4], weights=[9, 1], k=1)
            bet_amount = None
            try:
                bet_amount = randrange(100, money-100, 100)
            except Exception:
                return (3, 0)
            return (bot_choice, bet_amount)
        elif 'Call' in options:
            return (3, 0)
    elif hand_type[0] < 6:
        if money > 100 and 'Raise' in options:
            bet_amount = None
            try:
                bet_amount = randrange(100, player.getMoney(), 100)
            except Exception:
                return (5, 0)
            return (4, bet_amount)
        elif 'All In' in options:
            return (5, 0)
    elif hand_type[0] == 10:
        if 'Fold' in options and 'Call' in options and money > highest_bet-current_bet+1000:
            bot_choice = choices([1, 3], weights=[6, 4], k=1)
            return (*bot_choice, 0)
        elif 'Fold' in options:
            return (1, 0)
    elif 'Check' in options:
        return (2, 0)
    return 'Fold'