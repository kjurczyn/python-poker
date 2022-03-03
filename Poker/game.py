from sys import path
from pathlib import Path  
path[0] = str(Path(path[0]).parent)
from Poker.hand import determineHandType
from Poker.player import Player
from Poker.card import Card
from typing import List, Union
from random import shuffle
from threading import Event
from queue import Queue
del path

class Game:
    """Represents a game of Texas Hold'em Poker."""
    def __init__(self, players: List[Player]) -> None:
        """Initializes a Game object from a list of Player objects. At least 2 players in list."""
        self._players = players
        self._starting_players = self._players.copy()
        self._small_blind = players[0]
        self._big_blind = players[1]
        self._deck = []
        for i in range(1, 5):
            for y in range(2, 15):
                self._deck.append(Card(i, y))
        shuffle(self._deck)
        self._table = []
        self._stack = []
        self._pots = [[0, 0]]
        self._round_no = 0
        self._blind_multiplier = 1

    def newRound(self) -> None:
        """New round of game. Reshuffles players' cards and moves the blind markers."""
        self._stack.extend(self._table)
        self._table.clear()
        for i in self._players+self._players:
            i.addToHand(self.getCardFromDeck())
        for _ in range(3):
            self.dealNextCard()
        self._small_blind = self._starting_players[(self._starting_players.index(self._small_blind)+1) % len(self._starting_players)]
        self._big_blind = self._starting_players[(self._starting_players.index(self._big_blind)+1) % len(self._starting_players)]
        self.current_highest_bet = 0
        self._current_players = self._players.copy()

    def endRound(self, winner_queue: Queue):
        """Determines the round winner and puts them in winner_queue.
            Splits the pot(s).
            Removes players who were busted out from the game."""
        winner_list = []
        for i in range(len(self._pots)):
            winner = self.determineWinner([player for player in self._current_players if player.getCurrentPot() >= i])
            winner_list.append(winner)
            if isinstance(winner, Player):
                winner.addMoney(self._pots[i][1])
            else:
                prize = self._pots[i][1]/len(self._winner)
                for player in winner:
                    player.addMoney(prize)
            winner_queue.put(winner_list)
        self._pots = [[0, 0]]
        for i in self._players:
            self._stack.extend(i.resetHand())
            i.reset()
            if i.getMoney() <= 0:
                self._players.remove(i)

    def playGame(self, game_waiting_event: Event, game_continue_event: Event, current_player_queue: Queue, winner_queue: Queue) -> None:
        """Represents the process of the Poker game. 
            game_waiting_event is set when the process is waiting for response. 
            game_continue_event must be set for the process to continue.
            current_player_queue is the queue where the player whose turn it is is put.
            winner_queue is the queue where the round winner(s) are put 
            """
        while len(self.getPlayers()) > 1:
            self._round_no += 1
            if self._round_no % 5 == 0:
                self._blind_multiplier += 1
            self.newRound()
            if self.getSmallBlind() in self.getPlayers():
                self.bet(self._small_blind, 100*self._blind_multiplier)
            if self.getBigBlind() in self.getPlayers():
                self.bet(self._big_blind, 200*self._blind_multiplier)

            game_waiting_event.set()
            game_continue_event.wait()
            game_continue_event.clear()
            self.bettingRoundLoop(game_waiting_event, game_continue_event, current_player_queue)
            for _ in range(2):
                self.resetAlreadyRaised()
                self.dealNextCard()
                self.bettingRoundLoop(game_waiting_event, game_continue_event, current_player_queue)
            self.endRound(winner_queue)
            game_waiting_event.set()
            game_continue_event.wait()
            game_continue_event.clear()
        winner_queue.put(self.getPlayers()[0])
        game_waiting_event.set()
        game_continue_event.wait()
        game_continue_event.clear()

    def bettingRoundLoop(self, game_waiting_event: Event, game_continue_event: Event, current_player_queue: Queue):
        while True:
            for player in [i for i in self.getPlayers() if not i.isPass()]:
                if player.getAlreadyRaised() and self._pots[player._current_pot][0] == player.getCurrentBet():
                    player.resetAlreadyRaised()
                else:
                    player.resetAlreadyRaised()
                    current_player_queue.put(player)
                    game_waiting_event.set()
                    game_continue_event.wait()
                    game_continue_event.clear()
                if self.isCorrectBetAmount():
                    return

    def getCardFromDeck(self) -> Card:
        """Removes a card from the top of the deck and returns it. Adds stack to deck and shuffles if neccesary."""
        if len(self._deck) <= 1:
            shuffle(self._stack)
            self._deck.extend(self._stack)
            self._stack = []
        return self._deck.pop()

    def dealNextCard(self) -> None:
        """Deals a new card onto the table"""
        self._table.append(self.getCardFromDeck())

    def determineWinner(self, players: List[Player]) -> Union[Player, List[Player]]:
        """Takes in a list of Player objects and Returns a Player or list of Players with the highest hand."""
        # player list is sorted by hand types from hand.py, then players with a 
        # hand different than the first element on the list are removed
        players_sorted = []
        for i in players:
            players_sorted.append((i, *determineHandType(i.getHand()+self._table)))
        players_sorted.sort(key=lambda i: i[1])
        del players_sorted[[i[1] for i in players_sorted].count(players_sorted[0][1]):]
        # if lenght of the list is 1, there was only one player with the highest hand type and they are returned 
        if len(players_sorted) == 1:
            return players_sorted[0][0]
        # player list is sorted by the highest card/s in their hand
        # players with different hand types than the first element on the list are removed
        players_sorted.sort(key=lambda i: i[2], reverse=True)
        del players_sorted[[i[2] for i in players_sorted].count(players_sorted[0][2]):]
        # if lenght of the list is 1, there was only one player with the highest card in their hand and they are returned 
        if len(players_sorted) == 1:
            return players_sorted[0][0]
        # if there are two or more players with identical highest cards and their hand types 
        # are straight or royal or straight flush, according to poker rules the players tie and the pot is split
        if players_sorted[0][1] in {1, 2, 4, 6}:
            return [item[0] for item in players_sorted]
        # if the hands of the players aren't straight or royal or straight flush, the winner is determined using kickers
        return self.determinePlayerWithHighestKicker(players_sorted)

    def determinePlayerWithHighestKicker(self, players_sorted: List[Player]) -> Union[Player, List]:
        """Takes in a list of Player objects and returns a Player or list of Players with the highest kickers."""
        player_kickers = []
        # each element in player_kickers is a list of each players' kickers
        # the loop filters out cards that are a part of the players' cards and truncates the sorted list to 5 elements
        # if statement determines whether to use != or not in, as the hand info can be passed as int or tuple
        if isinstance(players_sorted[0][2], int):
            for i in players_sorted:
                player_kickers.append([y.getValue() for y in sorted(i[0].getHand()+self._table, reverse=True)[:5] if y.getValue() != i[2]])
        else:
            for i in players_sorted:
                player_kickers.append([y.getValue() for y in sorted(i[0].getHand()+self._table, reverse=True)[:5] if y.getValue() not in i[2]])
        # loops through each column of player_kickers and if there's a column where every player has a different card,
        # returns the player with the highest card in that column  
        for i in range(len(player_kickers[0])):
            if set([item[i] for item in player_kickers]) == len(player_kickers):
                return players_sorted[player_kickers.index(max(player_kickers, key=lambda item: item[i]))][0]
        # at least 2 identical hands
        for i in range(len(players_sorted)):
            if player_kickers.count(player_kickers[i]) == 1:
                players_sorted[i] = None
        return [item[0] for item in players_sorted if item]

    def getOptionsFor(self, player: Player) -> List[str]:
        """Takes a Player object and returns a list of available options for it as strings."""
        options = []
        if not player.getAllIn():
            options.append('Fold')
        if player.getCurrentBet() == self.getPots()[player.getCurrentPot()][0] - player.getCurrentBet() or player.getAllIn():
            options.append('Check')
        elif player.getMoney() > self.getPots()[player.getCurrentPot()][0] - player.getCurrentBet() and not player.getAllIn():
            options.append('Call')
        if player.getMoney() > 100 + self.getPots()[player.getCurrentPot()][0] - player.getCurrentBet() and not player.getAllIn():
            options.append('Raise')
        if not player.getAllIn():
            options.append('All In')
        return options

    def isCorrectBetAmount(self) -> bool:
        """Checks whether all players bet the same amount or have gone all in in the current round of betting."""
        for player in self.getPlayers():
            if player.getCurrentBet() != self.getPots()[player.getCurrentPot()][0] and not player.getAllIn() and not player.isPass():
                return False
        return True

    def bet(self, player: Player, amount: int) -> None:
        """Takes in a Player object and an amount integer, and places a bet of that amount for the Player.
            Creates side pot automaticall if necessary.
            """
        if amount > player.getMoney():
            raise Exception("Bet exceeds player's money")
        if amount == player.getMoney():
            # sets current_pot of all players to +1 if they have enough money
            player.setAllIn()
            if self.getPots()[player.getCurrentPot()][1] > amount:
                side_pot = [[], self.getPots()[player.getCurrentPot()][1], 0]
                self.getPots()[player.getCurrentPot][1] = amount
                for i in [player for player in self.getPlayers() if player != self and not player.isPass()]:
                    if i.getCurrentPot() == len(self.getPots())-1 and not i.getAllIn() and i.getMoney() > amount:
                        i.incrementPot()
                    self.getPots()[player.getCurrentPot()][1] -= i.getHighestBet()
                    self.getPots()[player.getCurrentPot()][1] += amount
                    side_pot[1] += i.getCurrentBet() - amount
                self.getPots().append(side_pot)
        player.setCurrentBet(player.getCurrentBet()+amount)
        if amount + player.getCurrentBet() > self.getPots()[player.getCurrentPot()][0]:
            self.getPots()[player.getCurrentPot()][0] = amount
            self._already_raised = True
        player.addMoney(-1*amount)
        self.getPots()[player.getCurrentPot()][1] += amount

    def resetCurrentBets(self) -> None:
        for player in self._current_players:
            player.reserCurrentBet()

    def resetAlreadyRaised(self) -> None:
        for player in self.getPlayers():
            player.resetAlreadyRaised()

    def getTable(self) -> List[Card]:
        """Returns list of cards currently on the table."""
        return self._table

    def getSmallBlind(self) -> Player:
        return self._small_blind

    def getBigBlind(self) -> Player:
        return self._big_blind

    def getBlindMultiplier(self) -> int:
        """Returns the current blind multiplier."""
        return self._blind_multiplier

    def getPlayers(self) -> List[Player]:
        """Returns a list of players in the game."""
        return self._players

    def getPots(self) -> List:
        """Returns list of pots in the current round."""
        return self._pots

    def __str__(self) -> str:
        return_string = 'Cards on table: '
        for i in self._table:
            return_string += str(i) + ' | '
        return_string += '\nPlayers in game:'
        for i in self._players:
            return_string += i.getName() + ' | '
        return return_string