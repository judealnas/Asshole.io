from __future__ import annotations
import typing
from pydealer import Card, Deck, Stack
import itertools as it
import abc


class InvalidPlayError(RuntimeError):
    pass


class Player(abc.ABC):
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
    def play(self, game_state) -> Stack:
        """Return players choice of cards"""

    def __eq__(self, other: Player):
        if not isinstance(other, Player):
            return False
        return self.__name == other.name


class Dealer:
    """Mediator between players and the game state.
    Responsible for dealing cards, validating plays, and enforcing rules.
    """

    __deck: Deck
    __players: typing.List[Player]

    def __init__(self, deck: Deck, players: typing.List[Player]):
        self.deck = deck
        self.deck.empty()
        self.deck.build()
        self.players = list(players)
        self.top_cards = Stack()
        self.__game_state = Game()
        self._current_player: typing.Optional[Player] = None

    def add_player(self, name: str):
        new_player = Player(name)
        if new_player in self.players:
            raise ValueError("Player already exists")
        self.players.append(new_player)

    def remove_player(self, name: str):
        for player in self.players:
            if player.name == name:
                self.players.remove(player)
                break

    def deal(self):
        """Distribute cards to start game"""
        cyc_players = it.cycle(self.players)
        while len(self.deck) > 0:
            self.deal_player(next(cyc_players), self.deck.deal(1))

    def deal_player(self, player: Player, cards: Stack):
        """Give cards to a player"""
        player.add_cards(cards)

    def init_deck(self):
        self.deck.empty()
        self.deck.build()
        self.deck.shuffle()

    def validate_play(self, cards: Stack):
        if (
            len(cards) != len(self.top_cards)
            or not cards[0].rank >= self.top_cards[0].rank
        ):
            raise InvalidPlayError(
                f"{len(self.top_cards)} of rank equal or higher than {self.top_cards[0].rank} must be played"
            )


class Game:
    """Current game state"""

    __turn: int
    __top_cards: Stack

    def __init__(self):
        self.__turn = 0
        self.__top_cards: Stack = Stack()

    @property
    def top_cards(self):
        return self.__top_cards

    @property
    def turn(self):
        return self.__turn
