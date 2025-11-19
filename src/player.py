"""Player module - Player logic and betting."""

from typing import Optional, List
from .hand import Hand
from .card import Card
from .strategies import Strategy, BasicStrategy


class Player:
    """Blackjack player with strategy and bankroll management."""
    
    def __init__(self, name: str = "Player", bankroll: int = 1000, 
                 strategy: Optional[Strategy] = None):
        """
        Initialize player.
        
        Args:
            name: Player name
            bankroll: Initial bankroll
            strategy: Playing strategy (defaults to BasicStrategy)
        """
        self.name = name
        self.bankroll = bankroll
        self.initial_bankroll = bankroll
        self.strategy = strategy or BasicStrategy()
        self.hand = Hand()
        self.hands: List[Hand] = [self.hand]  # Support for splits
        self.current_bet = 0
    
    def place_bet(self, amount: int) -> bool:
        """
        Place a bet.
        
        Args:
            amount: Bet amount
            
        Returns:
            True if bet placed successfully
        """
        if amount > self.bankroll:
            return False
        
        self.bankroll -= amount
        self.current_bet += amount
        return True
    
    def win(self, amount: int):
        """
        Win money (add to bankroll).
        
        Args:
            amount: Amount won
        """
        self.bankroll += amount
    
    def add_card(self, card: Card):
        """
        Add card to current hand.
        
        Args:
            card: Card to add
        """
        self.hand.add_card(card)
    
    def clear_hands(self):
        """Clear all hands for new round."""
        self.hand = Hand()
        self.hands = [self.hand]
        self.current_bet = 0
    
    def split_hand(self) -> bool:
        """
        Split current hand if it's a pair.
        
        Returns:
            True if split successful
        """
        if not self.hand.is_pair:
            return False
        
        # Create second hand with second card
        card2 = self.hand.cards.pop()
        new_hand = Hand([card2])
        self.hands.append(new_hand)
        
        return True
    
    @property
    def total_profit(self) -> int:
        """Get total profit/loss."""
        return self.bankroll - self.initial_bankroll
    
    def __str__(self) -> str:
        """String representation."""
        cards_str = " ".join(str(card) for card in self.hand.cards)
        return f"{self.name}: {cards_str} (Value: {self.hand.value})"
