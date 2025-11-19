"""Hand module - Represents a player's hand of cards."""

from typing import List, Tuple
from .card import Card


class Hand:
    """Represents a hand of cards with Blackjack-specific logic."""
    
    def __init__(self, cards: List[Card] = None):
        """
        Initialize hand with optional initial cards.
        
        Args:
            cards: List of cards to start with (default: empty)
        """
        self._cards: List[Card] = cards if cards else []
        self._is_split: bool = False
        self._is_doubled: bool = False
        self._is_surrendered: bool = False
    
    def add_card(self, card: Card) -> None:
        """Add a card to the hand."""
        self._cards.append(card)
    
    def clear(self) -> None:
        """Clear all cards from hand."""
        self._cards.clear()
        self._is_split = False
        self._is_doubled = False
        self._is_surrendered = False
    
    @property
    def cards(self) -> List[Card]:
        """Get copy of cards in hand."""
        return self._cards.copy()
    
    @property
    def value(self) -> int:
        """
        Calculate best hand value (auto-adjusting Aces).
        
        Returns:
            Best possible value <= 21, or bust value if > 21
        """
        value = 0
        num_aces = 0
        
        # Calculate value treating all Aces as 11
        for card in self._cards:
            value += card.value
            if card.is_ace:
                num_aces += 1
        
        # Convert Aces from 11 to 1 as needed to avoid bust
        while value > 21 and num_aces > 0:
            value -= 10  # Change Ace from 11 to 1
            num_aces -= 1
        
        return value
    
    @property
    def is_blackjack(self) -> bool:
        """Check if hand is a natural blackjack (Ace + 10-value, initial 2 cards)."""
        if len(self._cards) != 2:
            return False
        
        has_ace = any(card.is_ace for card in self._cards)
        has_ten = any(card.is_ten_value for card in self._cards)
        
        return has_ace and has_ten
    
    @property
    def is_bust(self) -> bool:
        """Check if hand is bust (value > 21)."""
        return self.value > 21
    
    @property
    def is_soft(self) -> bool:
        """Check if hand is soft (contains Ace counted as 11)."""
        if not any(card.is_ace for card in self._cards):
            return False
        
        # Check if we can count an Ace as 11 without busting
        value = sum(card.value for card in self._cards)
        return value <= 21
    
    @property
    def is_pair(self) -> bool:
        """Check if hand is a pair (exactly 2 cards with same rank)."""
        if len(self._cards) != 2:
            return False
        return self._cards[0].rank == self._cards[1].rank
    
    @property
    def can_split(self) -> bool:
        """Check if hand can be split."""
        return self.is_pair and not self._is_split
    
    @property
    def can_double_down(self) -> bool:
        """Check if hand can be doubled down (exactly 2 cards)."""
        return len(self._cards) == 2 and not self._is_doubled
    
    @property
    def is_split(self) -> bool:
        """Check if this hand was created from a split."""
        return self._is_split
    
    @property
    def is_doubled(self) -> bool:
        """Check if this hand was doubled down."""
        return self._is_doubled
    
    @property
    def is_surrendered(self) -> bool:
        """Check if this hand was surrendered."""
        return self._is_surrendered
    
    def mark_split(self) -> None:
        """Mark this hand as created from a split."""
        self._is_split = True
    
    def mark_doubled(self) -> None:
        """Mark this hand as doubled down."""
        self._is_doubled = True
    
    def mark_surrendered(self) -> None:
        """Mark this hand as surrendered."""
        self._is_surrendered = True
    
    def __len__(self) -> int:
        """Get number of cards in hand."""
        return len(self._cards)
    
    def __str__(self) -> str:
        """String representation of hand."""
        cards_str = " ".join(str(card) for card in self._cards)
        value_str = f"[{self.value}]"
        
        if self.is_blackjack:
            return f"{cards_str} {value_str} BLACKJACK!"
        elif self.is_bust:
            return f"{cards_str} {value_str} BUST!"
        elif self.is_soft:
            return f"{cards_str} {value_str} (soft)"
        else:
            return f"{cards_str} {value_str}"
    
    def __repr__(self) -> str:
        """Developer-friendly representation."""
        return f"Hand(cards={len(self._cards)}, value={self.value}, blackjack={self.is_blackjack})"
