import abc
from pydealer import Stack
from pubsub import Observer


class Player(Observer, abc.ABC):
    """Player class"""

    __name: str
    __hand: Stack

    def __init__(self, name: str):
        self.__name = name
        self.__hand = Stack()

    @property
    def name(self):
        return self.__name

    def __str__(self):
        return self.__name

    def __repr__(self):
        return str({"name": self.__name, "hand": self.__hand})

    def add_cards(self, cards: Stack):
        self.__hand.add(cards)

    @abc.abstractmethod
    async def play(self, game_state) -> Stack:
        """Return players choice of cards"""

    def __eq__(self, other):
        if not isinstance(other, Player):
            return False
        return self.__name == other.name
