"""Strategies module - AI strategies for Blackjack gameplay."""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional
from .card import Card
from .hand import Hand


class Action(Enum):
    """Possible player actions in Blackjack."""
    HIT = "hit"
    STAND = "stand"
    DOUBLE_DOWN = "double"
    SPLIT = "split"
    SURRENDER = "surrender"
    INSURANCE = "insurance"


class Strategy(ABC):
    """Abstract base class for Blackjack strategies."""
    
    @abstractmethod
    def decide(self, hand: Hand, dealer_card: Card, can_double: bool = True, 
               can_split: bool = True, can_surrender: bool = True) -> Action:
        """
        Decide what action to take based on current hand and dealer's visible card.
        
        Args:
            hand: Player's current hand
            dealer_card: Dealer's face-up card
            can_double: Whether double down is allowed
            can_split: Whether split is allowed
            can_surrender: Whether surrender is allowed
            
        Returns:
            Action to take
        """
        pass
    
    @abstractmethod
    def should_take_insurance(self, hand: Hand, dealer_card: Card) -> bool:
        """
        Decide whether to take insurance when dealer shows Ace.
        
        Args:
            hand: Player's current hand
            dealer_card: Dealer's Ace
            
        Returns:
            True if should take insurance
        """
        pass


class BasicStrategy(Strategy):
    """
    Mathematically optimal Blackjack strategy.
    Based on computer simulations and probability theory.
    Reduces house edge to ~0.5%.
    """
    
    def decide(self, hand: Hand, dealer_card: Card, can_double: bool = True,
               can_split: bool = True, can_surrender: bool = True) -> Action:
        """Decide action based on basic strategy chart."""
        
        player_value = hand.value
        dealer_value = dealer_card.value
        
        # Handle pairs
        if hand.is_pair and can_split:
            if hand.cards[0].rank.name in ("ACE", "EIGHT"):
                return Action.SPLIT  # Always split Aces and 8s
            elif hand.cards[0].rank.name in ("TEN", "JACK", "QUEEN", "KING", "FIVE"):
                pass  # Never split 10s or 5s
            elif hand.cards[0].rank.name == "NINE":
                if dealer_value in (7, 10, 11):
                    pass  # Stand on 9s vs 7, 10, A
                else:
                    return Action.SPLIT
            elif hand.cards[0].rank.name in ("TWO", "THREE", "SEVEN"):
                if 2 <= dealer_value <= 7:
                    return Action.SPLIT
            elif hand.cards[0].rank.name in ("FOUR",):
                if dealer_value in (5, 6):
                    return Action.SPLIT
            elif hand.cards[0].rank.name == "SIX":
                if 2 <= dealer_value <= 6:
                    return Action.SPLIT
        
        # Handle soft hands (with Ace counted as 11)
        if hand.is_soft:
            if player_value >= 19:
                return Action.STAND
            elif player_value == 18:
                if dealer_value <= 8:
                    return Action.STAND if not can_double else Action.DOUBLE_DOWN if dealer_value in (3, 4, 5, 6) else Action.STAND
                else:
                    return Action.HIT
            elif player_value == 17:
                if can_double and dealer_value in (3, 4, 5, 6):
                    return Action.DOUBLE_DOWN
                return Action.HIT
            elif player_value in (15, 16):
                if can_double and dealer_value in (4, 5, 6):
                    return Action.DOUBLE_DOWN
                return Action.HIT
            elif player_value in (13, 14):
                if can_double and dealer_value in (5, 6):
                    return Action.DOUBLE_DOWN
                return Action.HIT
            else:
                return Action.HIT
        
        # Handle hard hands
        if player_value >= 17:
            return Action.STAND
        elif player_value >= 13:
            if dealer_value <= 6:
                return Action.STAND
            else:
                return Action.HIT
        elif player_value == 12:
            if 4 <= dealer_value <= 6:
                return Action.STAND
            else:
                return Action.HIT
        elif player_value == 11:
            if can_double:
                return Action.DOUBLE_DOWN
            return Action.HIT
        elif player_value == 10:
            if can_double and dealer_value <= 9:
                return Action.DOUBLE_DOWN
            return Action.HIT
        elif player_value == 9:
            if can_double and 3 <= dealer_value <= 6:
                return Action.DOUBLE_DOWN
            return Action.HIT
        else:
            return Action.HIT
    
    def should_take_insurance(self, hand: Hand, dealer_card: Card) -> bool:
        """Basic strategy: never take insurance (unless counting cards)."""
        return False


class ConservativeStrategy(Strategy):
    """
    Conservative strategy minimizing risk.
    Stands early, avoids doubling and splitting.
    Higher house edge (~2-3%) but lower variance.
    """
    
    def decide(self, hand: Hand, dealer_card: Card, can_double: bool = True,
               can_split: bool = True, can_surrender: bool = True) -> Action:
        """Conservative decision-making."""
        
        player_value = hand.value
        
        # Only split Aces
        if hand.is_pair and can_split and hand.cards[0].is_ace:
            return Action.SPLIT
        
        # Stand on 12 or higher
        if player_value >= 12:
            return Action.STAND
        
        return Action.HIT
    
    def should_take_insurance(self, hand: Hand, dealer_card: Card) -> bool:
        """Conservative: always take insurance as "protection"."""
        return True


class AggressiveStrategy(Strategy):
    """
    Aggressive strategy maximizing potential gains.
    Hits higher, doubles and splits more often.
    High variance, moderate house edge (~1-2%).
    """
    
    def decide(self, hand: Hand, dealer_card: Card, can_double: bool = True,
               can_split: bool = True, can_surrender: bool = True) -> Action:
        """Aggressive decision-making."""
        
        player_value = hand.value
        dealer_value = dealer_card.value
        
        # Split most pairs
        if hand.is_pair and can_split:
            if hand.cards[0].rank.name not in ("TEN", "JACK", "QUEEN", "KING", "FIVE"):
                return Action.SPLIT
        
        # Double down aggressively
        if can_double and 9 <= player_value <= 12:
            return Action.DOUBLE_DOWN
        
        # Hit up to 18
        if player_value < 18:
            return Action.HIT
        
        return Action.STAND
    
    def should_take_insurance(self, hand: Hand, dealer_card: Card) -> bool:
        """Aggressive: never take insurance (bad bet)."""
        return False


class MartingaleStrategy(Strategy):
    """
    Martingale betting system combined with basic strategy.
    Doubles bet after each loss to recover losses + 1 unit profit.
    Warning: Requires large bankroll, table limits can prevent recovery.
    """
    
    def __init__(self):
        self._basic_strategy = BasicStrategy()
        self._consecutive_losses = 0
    
    def decide(self, hand: Hand, dealer_card: Card, can_double: bool = True,
               can_split: bool = True, can_surrender: bool = True) -> Action:
        """Use basic strategy for gameplay decisions."""
        return self._basic_strategy.decide(hand, dealer_card, can_double, can_split, can_surrender)
    
    def should_take_insurance(self, hand: Hand, dealer_card: Card) -> bool:
        """Never take insurance."""
        return False
    
    def get_bet_multiplier(self) -> int:
        """Get bet multiplier based on consecutive losses."""
        return 2 ** self._consecutive_losses
    
    def record_loss(self) -> None:
        """Record a loss (increases bet multiplier)."""
        self._consecutive_losses += 1
    
    def record_win(self) -> None:
        """Record a win (resets bet multiplier)."""
        self._consecutive_losses = 0
    
    def reset(self) -> None:
        """Reset strategy state."""
        self._consecutive_losses = 0


class CardCountingStrategy(Strategy):
    """
    Hi-Lo card counting strategy.
    Tracks running count: +1 for 2-6, 0 for 7-9, -1 for 10-A.
    Adjusts bets based on true count (running count / decks remaining).
    Theoretical edge up to +1.5% with perfect play.
    """
    
    def __init__(self):
        self._basic_strategy = BasicStrategy()
        self._running_count = 0
        self._cards_seen = 0
    
    def decide(self, hand: Hand, dealer_card: Card, can_double: bool = True,
               can_split: bool = True, can_surrender: bool = True) -> Action:
        """Use basic strategy with count-based deviations."""
        # Use basic strategy as base
        return self._basic_strategy.decide(hand, dealer_card, can_double, can_split, can_surrender)
    
    def should_take_insurance(self, hand: Hand, dealer_card: Card) -> bool:
        """Take insurance if true count >= +3."""
        true_count = self.get_true_count()
        return true_count >= 3
    
    def update_count(self, card: Card) -> None:
        """
        Update running count based on card seen.
        
        Args:
            card: Card that was dealt
        """
        self._cards_seen += 1
        
        value = card.value
        if 2 <= value <= 6:
            self._running_count += 1
        elif value >= 10 or card.is_ace:
            self._running_count -= 1
        # 7-9 are neutral (no change)
    
    def get_running_count(self) -> int:
        """Get current running count."""
        return self._running_count
    
    def get_true_count(self, decks_remaining: float = 4.0) -> float:
        """
        Calculate true count (running count / decks remaining).
        
        Args:
            decks_remaining: Estimated decks left in shoe
            
        Returns:
            True count
        """
        if decks_remaining <= 0:
            return 0.0
        return self._running_count / decks_remaining
    
    def get_bet_multiplier(self, true_count: Optional[float] = None) -> int:
        """
        Get bet multiplier based on true count.
        
        Args:
            true_count: True count (if None, calculates internally)
            
        Returns:
            Bet multiplier (1-8)
        """
        tc = true_count if true_count is not None else self.get_true_count()
        
        if tc >= 5:
            return 8
        elif tc >= 4:
            return 6
        elif tc >= 3:
            return 4
        elif tc >= 2:
            return 2
        else:
            return 1
    
    def reset(self) -> None:
        """Reset count (e.g., when deck is shuffled)."""
        self._running_count = 0
        self._cards_seen = 0
