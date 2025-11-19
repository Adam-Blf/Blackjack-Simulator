"""Deck module - Represents a deck of playing cards."""

import random
from typing import List, Optional
from .card import Card, Rank, Suit


class Deck:
    """Represents a deck of playing cards with shuffle and deal capabilities."""
    
    def __init__(self, num_decks: int = 1, shuffle_on_init: bool = True):
        """
        Initialize deck with specified number of standard 52-card decks.
        
        Args:
            num_decks: Number of standard decks to use (default: 1)
            shuffle_on_init: Whether to shuffle immediately (default: True)
        """
        if num_decks < 1:
            raise ValueError("Number of decks must be at least 1")
        
        self.num_decks = num_decks
        self._cards: List[Card] = []
        self._dealt_cards: List[Card] = []
        self.reset()
        
        if shuffle_on_init:
            self.shuffle()
    
    def reset(self) -> None:
        """Reset deck to full set of cards."""
        self._cards = []
        for _ in range(self.num_decks):
            for suit in Suit:
                for rank in Rank:
                    self._cards.append(Card(rank, suit))
        self._dealt_cards = []
    
    def shuffle(self) -> None:
        """Shuffle the deck."""
        random.shuffle(self._cards)
    
    def deal(self) -> Optional[Card]:
        """
        Deal one card from the deck.
        
        Returns:
            Card if deck has cards, None if empty
        """
        if not self._cards:
            return None
        
        card = self._cards.pop()
        self._dealt_cards.append(card)
        return card
    
    def deal_multiple(self, count: int) -> List[Card]:
        """
        Deal multiple cards from the deck.
        
        Args:
            count: Number of cards to deal
            
        Returns:
            List of dealt cards
        """
        cards = []
        for _ in range(count):
            card = self.deal()
            if card is None:
                break
            cards.append(card)
        return cards
    
    @property
    def remaining(self) -> int:
        """Get number of cards remaining in deck."""
        return len(self._cards)
    
    @property
    def dealt_count(self) -> int:
        """Get number of cards already dealt."""
        return len(self._dealt_cards)
    
    @property
    def total_cards(self) -> int:
        """Get total number of cards in deck (dealt + remaining)."""
        return self.num_decks * 52
    
    @property
    def cards(self) -> List[Card]:
        """Get copy of remaining cards."""
        return self._cards.copy()
    
    @property
    def dealt_cards(self) -> List[Card]:
        """Get copy of dealt cards."""
        return self._dealt_cards.copy()
    
    def needs_shuffle(self, threshold: float = 0.25) -> bool:
        """
        Check if deck needs reshuffling based on remaining cards.
        
        Args:
            threshold: Percentage of cards remaining to trigger reshuffle (default: 25%)
            
        Returns:
            True if remaining cards <= threshold * total cards
        """
        return self.remaining <= (self.total_cards * threshold)
    
    def __len__(self) -> int:
        """Get number of remaining cards."""
        return self.remaining
    
    def __str__(self) -> str:
        """String representation of deck."""
        return f"Deck(remaining={self.remaining}, dealt={self.dealt_count}, decks={self.num_decks})"
    
    def __repr__(self) -> str:
        """Developer-friendly representation."""
        return f"Deck(num_decks={self.num_decks}, remaining={self.remaining})"
