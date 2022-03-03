from sys import path
from pathlib import Path
path[0] = str(Path(path[0]).parent)
from typing import Callable, List
from Poker.card import Card
del path


class Player:
    """Represents a player in the game."""
    def __init__(self, name: str, money: int = 10000) -> None:
        """Takes player name and optional starting money, default is 1000."""
        self._name = name
        self._hand = []
        self._money = money
        self._pass = False
        self._all_in = False
        self._current_bet = 0
        self._ready = False
        self._current_pot = 0
        self._already_raised = False
        # self._player_options = [self.bet, self.passRound, ]
        # self._available_options =

    def reset(self) -> None:
        """Resets some variables to default values. Meant for use after round end.
            Resets: _pass, _all_in, _current_bet, _current_pot, _already_raised"""
        self._pass = False
        self._all_in = False
        self._current_bet = 0
        self._ready = False
        self._current_pot = 0
        self._already_raised = False

    def resetHand(self) -> List[Card]:
        """Clears the player's hand and returns its contents."""
        ret = self._hand.copy()
        self._hand.clear()
        return ret

    def getName(self) -> str:
        return self._name

    def __str__(self) -> str:
        return self.getName()

    def __repr__(self) -> str:
        return self.getName()

    def getHand(self) -> List[Card]:
        return self._hand

    def getMoney(self) -> int:
        return self._money

    def getBlind(self) -> int:
        return self._blind

    def getCurrentBet(self) -> int:
        return self._current_bet

    def setCurrentBet(self, amount: int) -> None:
        self._current_bet = amount

    def reserCurrentBet(self) -> None:
        self._current_bet = 0

    def addToHand(self, card: 'Card') -> None:
        self._hand.append(card)

    def passRound(self) -> None:
        self._pass = True

    def isPass(self) -> bool:
        return self._pass

    def addMoney(self, amount: int) -> None:
        self._money += amount

    def getAllIn(self) -> bool:
        return self._all_in

    def setAllIn(self) -> None:
        self._all_in = True

    def setBlind(self, blind: int) -> None:
        self._blind = blind

    def getCurrentPot(self) -> int:
        return self._current_pot

    def incrementPot(self) -> None:
        self._current_pot += 1

    def getAlreadyRaised(self) -> bool:
        return self._already_raised

    def resetAlreadyRaised(self) -> None:
        self._already_raised = False

   