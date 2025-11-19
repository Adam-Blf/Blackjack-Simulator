"""Dealer module - Dealer logic for Blackjack."""

from .hand import Hand
from .card import Card


class Dealer:
    """Blackjack dealer with standard casino rules."""
    
    def __init__(self):
        """Initialize dealer."""
        self.hand = Hand()
    
    def add_card(self, card: Card):
        """
        Add a card to dealer's hand.
        
        Args:
            card: Card to add
        """
        self.hand.add_card(card)
    
    def should_hit(self) -> bool:
        """
        Determine if dealer should hit based on standard rules.
        Dealer must hit on 16 or less, must stand on 17 or more.
        
        Returns:
            True if dealer should take another card
        """
        return self.hand.value < 17
    
    def clear_hand(self):
        """Clear dealer's hand for new round."""
        self.hand = Hand()
    
    def show_hand(self, hide_second: bool = False) -> str:
        """
        Display dealer's hand.
        
        Args:
            hide_second: If True, hide second card (face down)
            
        Returns:
            String representation of hand
        """
        if hide_second and len(self.hand.cards) >= 2:
            visible = [str(self.hand.cards[0]), "??"]
            return f"Dealer: {visible[0]} ?? (Value: {self.hand.cards[0].value})"
        else:
            cards_str = " ".join(str(card) for card in self.hand.cards)
            return f"Dealer: {cards_str} (Value: {self.hand.value})"
    
    @property
    def upcard(self) -> Card:
        """
        Get dealer's face-up card (first card).
        
        Returns:
            Dealer's visible card
        """
        return self.hand.cards[0] if self.hand.cards else None
    
    def __str__(self) -> str:
        """String representation."""
        return self.show_hand()
