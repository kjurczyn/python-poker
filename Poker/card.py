class Card:
    """Represents a card from the standard 52-card deck.
       Suits: 1: 'Clubs', 2: 'Diamonds', 3: 'Hearts', 4: 'Spades
       Values:
            2: 'Two'
            3: 'Three'
            4: 'Four'
            5: 'Five'
            6: 'Six'
            7: 'Seven
            8: 'Eight
            9: 'Nine'
            10: 'Ten'
            11: 'Jack'
            12: 'Queen'
            13: 'King'q
            14: 'Ace'"""
    _suits = {
        1: 'Clubs', 2: 'Diamonds', 3: 'Hearts', 4: 'Spades'
    }
    _values = {
             2: 'Two',
             3: 'Three',
             4: 'Four',
             5: 'Five',
             6: 'Six',
             7: 'Seven',
             8: 'Eight',
             9: 'Nine',
             10: 'Ten',
             11: 'Jack',
             12: 'Queen',
             13: 'King',
             14: 'Ace'
    }

    def __init__(self, suit: int, value: int) -> None:
        """Suit range: 1 - 4, value range: 2 - 14
            Suits: 1 - Clubs | 2- Diamonds | 3 - Hearts | 4 - Spades
            Values: 2 - Two -> 14 - Ace
            """
        self._suit = suit
        self._value = value

    def __repr__(self) -> str:
        return self.__str__()

    def __lt__(self, other: 'Card'):
        return self.getValue() < other.getValue()

    def __le__(self, other:  'Card'):
        return self.getValue() <= other.getValue()

    def __gt__(self, other:  'Card'):
        return self.getValue() > other.getValue()

    def __ge__(self, other:  'Card'):
        return self.getValue() >= other.getValue()

    def __eq__(self, other:  'Card'):
        return self.getValue() == other.getValue()

    def __ne__(self, other:  'Card'):
        return self.getValue() != other.getValue()

    def getSuit(self) -> int:
        return self._suit

    def getSuitString(self) -> str:
        """Returns a string representation of the card's suit."""
        return Card._suits.get(self._suit)

    def getValue(self) -> int:
        return self._value

    def getValueString(self) -> str:
        """Returns a string representation of the card's value."""
        return Card._values.get(self._value)

    def __str__(self) -> str:
        return self.getValueString() + " of " + self.getSuitString()

    @staticmethod
    def getVals():
        """Returns a list of all card values."""
        return Card._suits

    @staticmethod
    def getSuits():
        """Returns a list of all card suits."""
        return Card._values
