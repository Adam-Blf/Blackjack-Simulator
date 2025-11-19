"""Card module - Represents a playing card."""

from dataclasses import dataclass
from enum import Enum
from typing import Union


class Suit(Enum):
    """Card suits."""
    SPADES = "♠"
    HEARTS = "♥"
    DIAMONDS = "♦"
    CLUBS = "♣"


class Rank(Enum):
    """Card ranks with their values."""
    TWO = ("2", 2)
    THREE = ("3", 3)
    FOUR = ("4", 4)
    FIVE = ("5", 5)
    SIX = ("6", 6)
    SEVEN = ("7", 7)
    EIGHT = ("8", 8)
    NINE = ("9", 9)
    TEN = ("10", 10)
    JACK = ("J", 10)
    QUEEN = ("Q", 10)
    KING = ("K", 10)
    ACE = ("A", 11)  # Can also be 1
    
    @property
    def symbol(self) -> str:
        """Get the card symbol."""
        return self.value[0]
    
    @property
    def numeric_value(self) -> int:
        """Get the numeric value."""
        return self.value[1]


@dataclass
class Card:
    """Represents a playing card with rank and suit."""
    
    rank: Rank
    suit: Suit
    
    @property
    def value(self) -> int:
        """Get the card's numeric value."""
        return self.rank.numeric_value
    
    @property
    def is_ace(self) -> bool:
        """Check if card is an Ace."""
        return self.rank == Rank.ACE
    
    @property
    def is_face_card(self) -> bool:
        """Check if card is a face card (J, Q, K)."""
        return self.rank in (Rank.JACK, Rank.QUEEN, Rank.KING)
    
    @property
    def is_ten_value(self) -> bool:
        """Check if card has value of 10."""
        return self.value == 10
    
    def __str__(self) -> str:
        """String representation of card."""
        return f"{self.rank.symbol}{self.suit.value}"
    
    def __repr__(self) -> str:
        """Developer-friendly representation."""
        return f"Card({self.rank.name}, {self.suit.name})"
    
    def __lt__(self, other: 'Card') -> bool:
        """Compare cards by value."""
        return self.value < other.value
    
    def __eq__(self, other: object) -> bool:
        """Check if two cards are equal."""
        if not isinstance(other, Card):
            return NotImplemented
        return self.rank == other.rank and self.suit == other.suit
    
    def __hash__(self) -> int:
        """Make card hashable."""
        return hash((self.rank, self.suit))
