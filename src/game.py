"""Game module - Main game logic and state machine."""

from typing import Optional, List
from .player import Player
from .dealer import Dealer
from .deck import Deck
from .hand import Hand
from .strategies import Action


class Game:
    """Main Blackjack game controller."""
    
    def __init__(self, player: Optional[Player] = None, bet: int = 10, num_decks: int = 6):
        """
        Initialize game.
        
        Args:
            player: Player instance (creates default if None)
            bet: Base bet amount
            num_decks: Number of decks in shoe
        """
        self.player = player or Player("Player", bankroll=1000)
        self.dealer = Dealer()
        self.deck = Deck(num_decks=num_decks)
        self.bet = bet
        self.num_decks = num_decks
        
        # Game state
        self.round_active = False
        self.insurance_offered = False
    
    def start_round(self) -> bool:
        """
        Start a new round.
        
        Returns:
            True if round started successfully
        """
        if self.player.bankroll < self.bet:
            return False
        
        # Place bet
        if not self.player.place_bet(self.bet):
            return False
        
        # Reset hands
        self.player.clear_hands()
        self.dealer.clear_hand()
        
        # Deal initial cards
        self.player.add_card(self.deck.deal())
        self.dealer.add_card(self.deck.deal())
        self.player.add_card(self.deck.deal())
        self.dealer.add_card(self.deck.deal())
        
        self.round_active = True
        
        # Check for dealer blackjack
        if self.dealer.hand.is_blackjack():
            return self._resolve_dealer_blackjack()
        
        # Check for player blackjack
        if self.player.hand.is_blackjack():
            return self._resolve_player_blackjack()
        
        return True
    
    def play_auto(self) -> str:
        """
        Play a round automatically using player's strategy.
        
        Returns:
            "win", "loss", or "push"
        """
        if not self.start_round():
            return "loss"
        
        # Player's turn
        while self.player.hand.value < 21:
            action = self.player.strategy.decide(
                self.player.hand,
                self.dealer.hand.cards[0],  # Dealer's visible card
                can_double=True,
                can_split=self.player.hand.is_pair
            )
            
            if action == Action.HIT:
                self.player.add_card(self.deck.deal())
            elif action == Action.STAND:
                break
            elif action == Action.DOUBLE_DOWN:
                self.player.place_bet(self.bet)  # Double the bet
                self.player.add_card(self.deck.deal())
                break
            elif action == Action.SPLIT:
                # Simplified split handling
                break
            else:
                break
        
        # Check if player busted
        if self.player.hand.value > 21:
            return "loss"
        
        # Dealer's turn
        while self.dealer.should_hit():
            self.dealer.add_card(self.deck.deal())
        
        # Determine winner
        return self._determine_winner()
    
    def _determine_winner(self) -> str:
        """
        Determine the winner of the round.
        
        Returns:
            "win", "loss", or "push"
        """
        player_value = self.player.hand.value
        dealer_value = self.dealer.hand.value
        
        if dealer_value > 21:
            # Dealer busted
            self.player.win(self.bet * 2)
            return "win"
        elif player_value > dealer_value:
            # Player has higher value
            self.player.win(self.bet * 2)
            return "win"
        elif player_value < dealer_value:
            # Dealer has higher value
            return "loss"
        else:
            # Push (tie)
            self.player.win(self.bet)  # Return original bet
            return "push"
    
    def _resolve_dealer_blackjack(self) -> bool:
        """Handle dealer blackjack."""
        if self.player.hand.is_blackjack():
            # Push
            self.player.win(self.bet)
            return False
        else:
            # Player loses
            return False
    
    def _resolve_player_blackjack(self) -> bool:
        """Handle player blackjack."""
        # Pay 3:2
        self.player.win(int(self.bet * 2.5))
        return False
    
    def reset(self):
        """Reset game for new session."""
        self.deck = Deck(num_decks=self.num_decks)
        self.player.clear_hands()
        self.dealer.clear_hand()
        self.round_active = False
