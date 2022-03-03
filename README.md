# 21Z PIPR Poker
Implementation of Texas Hold'em Poker in Python

# Documentation
Modules: 
- [card.py](#cardpy): class representing playing cards from a starndard 52-card deck
- [game.py](#gamepy): game logic 
- [hand.py](#handpy): hand identification methods
- main.py: ui and main processes 
- [player.py](#playerpy): class representing players
- [pokerbot.py](#pokerbotpy): method for decision-making by bots

# game.py
Help on module game:

NAME
    game
    
    class Game(builtins.object)
     |  Game(players: List[Poker.player.Player]) -> None
     |  
     |  Represents a game of Texas Hold'em Poker.
     |  
     |  Methods defined here:
     |  
     |  __init__(self, players: List[Poker.player.Player]) -> None
     |      Initializes a Game object from a list of Player objects. At least 2 players in list.
     |  
     |  __str__(self) -> str
     |      Return str(self).
     |  
     |  bet(self, player: Poker.player.Player, amount: int) -> None
     |      Takes in a Player object and an amount integer, and places a bet of that amount for the Player.
     |      Creates side pot automaticall if necessary.
     |  
     |  bettingRoundLoop(self, game_waiting_event: threading.Event, game_continue_event: threading.Event, current_player_queue: queue.Queue)
     |  
     |  dealNextCard(self) -> None
     |      Deals a new card onto the table
     |  
     |  determinePlayerWithHighestKicker(self, players_sorted: List[Poker.player.Player]) -> Union[Poker.player.Player, List]
     |      Takes in a list of Player objects and returns a Player or list of Players with the highest kickers.
     |  
     |  determineWinner(self, players: List[Poker.player.Player]) -> Union[Poker.player.Player, List[Poker.player.Player]]
     |      Takes in a list of Player objects and Returns a Player or list of Players with the highest hand.
     |  
     |  endRound(self, winner_queue: queue.Queue)
     |      Determines the round winner and puts them in winner_queue.
     |      Splits the pot(s).
     |      Removes players who were busted out from the game.
     |  
     |  getBigBlind(self) -> Poker.player.Player
     |  
     |  getBlindMultiplier(self) -> int
     |      Returns the current blind multiplier.
     |  
     |  getCardFromDeck(self) -> Poker.card.Card
     |      Removes a card from the top of the deck and returns it. Adds stack to deck and shuffles if neccesary.
     |  
     |  getOptionsFor(self, player: Poker.player.Player) -> List[str]
     |      Takes a Player object and returns a list of available options for it as strings.
     |  
     |  getPlayers(self) -> List[Poker.player.Player]
     |      Returns a list of players in the game.
     |  
     |  getPots(self) -> List
     |      Returns list of pots in the current round.
     |  
     |  getSmallBlind(self) -> Poker.player.Player
     |  
     |  getTable(self) -> List[Poker.card.Card]
     |      Returns list of cards currently on the table.
     |  
     |  isCorrectBetAmount(self) -> bool
     |      Checks whether all players bet the same amount or have gone all in in the current round of betting.
     |  
     |  newRound(self) -> None
     |      New round of game. Reshuffles players' cards and moves the blind markers.
     |  
     |  playGame(self, game_waiting_event: threading.Event, game_continue_event: threading.Event, current_player_queue: queue.Queue, 
     |  winner_queue: queue.Queue) -> None
     |      Represents the process of the Poker game. 
     |      game_waiting_event is set when the process is waiting for response. 
     |      game_continue_event must be set for the process to continue.
     |      current_player_queue is the queue where the player whose turn it is is put.
     |      winner_queue is the queue where the round winner(s) are put
     |  
     |  resetAlreadyRaised(self) -> None
     |  
     |  resetCurrentBets(self) -> None
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)

# card.py
Help on module card:

NAME
    card
    
    class Card(builtins.object)
     |  Card(suit: int, value: int) -> None
     |  
     |  Represents a card from the standard 52-card deck.
     |  Suits: 1: 'Clubs', 2: 'Diamonds', 3: 'Hearts', 4: 'Spades
     |  Values:
     |       2: 'Two'
     |       3: 'Three'
     |       4: 'Four'
     |       5: 'Five'
     |       6: 'Six'
     |       7: 'Seven
     |       8: 'Eight
     |       9: 'Nine'
     |       10: 'Ten'
     |       11: 'Jack'
     |       12: 'Queen'
     |       13: 'King'q
     |       14: 'Ace'
     |  
     |  Methods defined here:
     |  
     |  __eq__(self, other: 'Card')
     |      Return self==value.
     |  
     |  __ge__(self, other: 'Card')
     |      Return self>=value.
     |  
     |  __gt__(self, other: 'Card')
     |      Return self>value.
     |  
     |  __init__(self, suit: int, value: int) -> None
     |      Suit range: 1 - 4, value range: 2 - 14
     |      Suits: 1 - Clubs | 2- Diamonds | 3 - Hearts | 4 - Spades
     |      Values: 2 - Two -> 14 - Ace
     |  
     |  __le__(self, other: 'Card')
     |      Return self<=value.
     |  
     |  __lt__(self, other: 'Card')
     |      Return self<value.
     |  
     |  __ne__(self, other: 'Card')
     |      Return self!=value.
     |  
     |  __repr__(self) -> str
     |      Return repr(self).
     |  
     |  __str__(self) -> str
     |      Return str(self).
     |  
     |  getSuit(self) -> int
     |  
     |  getSuitString(self) -> str
     |      Returns a string representation of the card's suit.
     |  
     |  getValue(self) -> int
     |  
     |  getValueString(self) -> str
     |      Returns a string representation of the card's value.
     |  
     |  ----------------------------------------------------------------------
     |  Static methods defined here:
     |  
     |  getSuits()
     |      Returns a list of all card suits.
     |  
     |  getVals()
     |      Returns a list of all card values.
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
     |  
     |  ----------------------------------------------------------------------
     |  Data and other attributes defined here:
     |  
     |  __hash__ = None

# hand.py
Help on module hand:

NAME
    hand

FUNCTIONS
    
    checkForFlush(cards: List[Poker.card.Card]) -> tuple
    
    checkForFour(cards: List[Poker.card.Card]) -> tuple
    
    checkForFullHouse(cards: List[Poker.card.Card], pairs: List, three: tuple) -> tuple
    
    checkForPairs(cards: List[Poker.card.Card], three: tuple) -> List[Poker.card.Card]
    
    checkForRoyalAndStraightFlush(cards: List[Poker.card.Card])
    
    checkForStraight(cards: List[Poker.card.Card]) -> tuple
    
    checkForThree(cards: List[Poker.card.Card]) -> tuple
    
    determineHandType(cards: List[Poker.card.Card]) -> Tuple[int, Union[tuple, int]]
        Takes in a list of at least 5 cards and returns the hand type and value of high card/s of the hand.
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
           10: High Card
    
    isInRow(cards: List[Poker.card.Card]) -> bool
        Takes a list of cards sorted in descending order and checks wether they're in row.
    
    isSameSuit(cards: List[Poker.card.Card]) -> bool
        Takes a list of cards and checks whether they're of the same suit.
    
    isSameValue(cards: List[Poker.card.Card]) -> bool
        Takes a list of cards and checks whether they're the same value.

# player.py
Help on module player:

NAME
    player

    class Player(builtins.object)
     |  Player(name: str, money: int = 10000) -> None
     |  
     |  Represents a player in the game.
     |  
     |  Methods defined here:
     |  
     |  __init__(self, name: str, money: int = 10000) -> None
     |      Takes player name and optional starting money, default is 1000.
     |  
     |  __repr__(self) -> str
     |      Return repr(self).
     |  
     |  __str__(self) -> str
     |      Return str(self).
     |  
     |  addMoney(self, amount: int) -> None
     |  
     |  addToHand(self, card: 'Card') -> None
     |  
     |  getAllIn(self) -> bool
     |  
     |  getAlreadyRaised(self) -> bool
     |  
     |  getBlind(self) -> int
     |  
     |  getCurrentBet(self) -> int
     |  
     |  getCurrentPot(self) -> int
     |  
     |  getHand(self) -> List[Poker.card.Card]
     |  
     |  getMoney(self) -> int
     |  
     |  getName(self) -> str
     |  
     |  incrementPot(self) -> None
     |  
     |  isPass(self) -> bool
     |  
     |  passRound(self) -> None
     |  
     |  reserCurrentBet(self) -> None
     |  
     |  reset(self) -> None
     |      Resets some variables to default values. Meant for use after round end.
     |      Resets: _pass, _all_in, _current_bet, _current_pot, _already_raised
     |  
     |  resetAlreadyRaised(self) -> None
     |  
     |  resetHand(self) -> List[Poker.card.Card]
     |      Clears the player's hand and returns its contents.
     |  
     |  setAllIn(self) -> None
     |  
     |  setBlind(self, blind: int) -> None
     |  
     |  setCurrentBet(self, amount: int) -> None
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)

# pokerbot.py
Help on module pokerbot:

NAME
    pokerbot

FUNCTIONS

    makeChoice(player: Poker.player.Player, game: Poker.game.Game) -> Tuple[str, int]
        Takse in a Player object and a Game object. Returns a tuple containing the best choice and an amount of money.
