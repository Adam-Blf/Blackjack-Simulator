"""Unit tests for Strategy classes."""

import pytest
from src.strategies import (
    Action, Strategy, BasicStrategy, ConservativeStrategy,
    AggressiveStrategy, MartingaleStrategy, CardCountingStrategy
)
from src.hand import Hand
from src.card import Card, Rank, Suit


class TestBasicStrategy:
    """Test suite for BasicStrategy class."""
    
    def test_hit_on_low_value(self):
        """Test basic strategy hits on low values."""
        strategy = BasicStrategy()
        hand = Hand([Card(Rank.FIVE, Suit.SPADES), Card(Rank.THREE, Suit.HEARTS)])
        dealer_card = Card(Rank.SEVEN, Suit.DIAMONDS)
        
        action = strategy.decide(hand, dealer_card)
        assert action == Action.HIT
    
    def test_stand_on_17_or_higher(self):
        """Test basic strategy stands on 17+."""
        strategy = BasicStrategy()
        hand = Hand([Card(Rank.TEN, Suit.SPADES), Card(Rank.SEVEN, Suit.HEARTS)])
        dealer_card = Card(Rank.SIX, Suit.DIAMONDS)
        
        action = strategy.decide(hand, dealer_card)
        assert action == Action.STAND
    
    def test_double_on_11(self):
        """Test basic strategy doubles on 11."""
        strategy = BasicStrategy()
        hand = Hand([Card(Rank.SIX, Suit.SPADES), Card(Rank.FIVE, Suit.HEARTS)])
        dealer_card = Card(Rank.SIX, Suit.DIAMONDS)
        
        action = strategy.decide(hand, dealer_card, can_double=True)
        assert action == Action.DOUBLE_DOWN
    
    def test_split_aces(self):
        """Test basic strategy always splits Aces."""
        strategy = BasicStrategy()
        hand = Hand([Card(Rank.ACE, Suit.SPADES), Card(Rank.ACE, Suit.HEARTS)])
        dealer_card = Card(Rank.SEVEN, Suit.DIAMONDS)
        
        action = strategy.decide(hand, dealer_card, can_split=True)
        assert action == Action.SPLIT
    
    def test_split_eights(self):
        """Test basic strategy always splits 8s."""
        strategy = BasicStrategy()
        hand = Hand([Card(Rank.EIGHT, Suit.SPADES), Card(Rank.EIGHT, Suit.HEARTS)])
        dealer_card = Card(Rank.TEN, Suit.DIAMONDS)
        
        action = strategy.decide(hand, dealer_card, can_split=True)
        assert action == Action.SPLIT
    
    def test_no_insurance(self):
        """Test basic strategy never takes insurance."""
        strategy = BasicStrategy()
        hand = Hand([Card(Rank.TEN, Suit.SPADES), Card(Rank.NINE, Suit.HEARTS)])
        dealer_card = Card(Rank.ACE, Suit.DIAMONDS)
        
        assert strategy.should_take_insurance(hand, dealer_card) is False
    
    def test_soft_18_vs_dealer_9(self):
        """Test basic strategy hits soft 18 vs dealer 9."""
        strategy = BasicStrategy()
        hand = Hand([Card(Rank.ACE, Suit.SPADES), Card(Rank.SEVEN, Suit.HEARTS)])
        dealer_card = Card(Rank.NINE, Suit.DIAMONDS)
        
        action = strategy.decide(hand, dealer_card)
        assert action == Action.HIT


class TestConservativeStrategy:
    """Test suite for ConservativeStrategy class."""
    
    def test_stands_early(self):
        """Test conservative strategy stands on 12+."""
        strategy = ConservativeStrategy()
        hand = Hand([Card(Rank.SEVEN, Suit.SPADES), Card(Rank.FIVE, Suit.HEARTS)])
        dealer_card = Card(Rank.TEN, Suit.DIAMONDS)
        
        action = strategy.decide(hand, dealer_card)
        assert action == Action.STAND
    
    def test_only_splits_aces(self):
        """Test conservative strategy only splits Aces."""
        strategy = ConservativeStrategy()
        
        # Should split Aces
        hand_aces = Hand([Card(Rank.ACE, Suit.SPADES), Card(Rank.ACE, Suit.HEARTS)])
        dealer_card = Card(Rank.SEVEN, Suit.DIAMONDS)
        action = strategy.decide(hand_aces, dealer_card, can_split=True)
        assert action == Action.SPLIT
        
        # Should not split 8s
        hand_eights = Hand([Card(Rank.EIGHT, Suit.SPADES), Card(Rank.EIGHT, Suit.HEARTS)])
        action = strategy.decide(hand_eights, dealer_card, can_split=True)
        assert action == Action.STAND
    
    def test_takes_insurance(self):
        """Test conservative strategy always takes insurance."""
        strategy = ConservativeStrategy()
        hand = Hand([Card(Rank.TEN, Suit.SPADES), Card(Rank.NINE, Suit.HEARTS)])
        dealer_card = Card(Rank.ACE, Suit.DIAMONDS)
        
        assert strategy.should_take_insurance(hand, dealer_card) is True


class TestAggressiveStrategy:
    """Test suite for AggressiveStrategy class."""
    
    def test_hits_high(self):
        """Test aggressive strategy hits up to 18."""
        strategy = AggressiveStrategy()
        hand = Hand([Card(Rank.TEN, Suit.SPADES), Card(Rank.SEVEN, Suit.HEARTS)])
        dealer_card = Card(Rank.NINE, Suit.DIAMONDS)
        
        action = strategy.decide(hand, dealer_card)
        assert action == Action.HIT
    
    def test_doubles_aggressively(self):
        """Test aggressive strategy doubles on 9-12."""
        strategy = AggressiveStrategy()
        hand = Hand([Card(Rank.SIX, Suit.SPADES), Card(Rank.FIVE, Suit.HEARTS)])
        dealer_card = Card(Rank.SIX, Suit.DIAMONDS)
        
        action = strategy.decide(hand, dealer_card, can_double=True)
        assert action == Action.DOUBLE_DOWN
    
    def test_splits_most_pairs(self):
        """Test aggressive strategy splits most pairs."""
        strategy = AggressiveStrategy()
        
        # Should split 7s
        hand = Hand([Card(Rank.SEVEN, Suit.SPADES), Card(Rank.SEVEN, Suit.HEARTS)])
        dealer_card = Card(Rank.EIGHT, Suit.DIAMONDS)
        action = strategy.decide(hand, dealer_card, can_split=True)
        assert action == Action.SPLIT
    
    def test_no_insurance(self):
        """Test aggressive strategy doesn't take insurance."""
        strategy = AggressiveStrategy()
        hand = Hand([Card(Rank.TEN, Suit.SPADES), Card(Rank.NINE, Suit.HEARTS)])
        dealer_card = Card(Rank.ACE, Suit.DIAMONDS)
        
        assert strategy.should_take_insurance(hand, dealer_card) is False


class TestMartingaleStrategy:
    """Test suite for MartingaleStrategy class."""
    
    def test_initial_bet_multiplier(self):
        """Test initial bet multiplier is 1."""
        strategy = MartingaleStrategy()
        assert strategy.get_bet_multiplier() == 1
    
    def test_doubles_after_loss(self):
        """Test bet doubles after loss."""
        strategy = MartingaleStrategy()
        
        strategy.record_loss()
        assert strategy.get_bet_multiplier() == 2
        
        strategy.record_loss()
        assert strategy.get_bet_multiplier() == 4
        
        strategy.record_loss()
        assert strategy.get_bet_multiplier() == 8
    
    def test_resets_after_win(self):
        """Test bet resets to 1 after win."""
        strategy = MartingaleStrategy()
        
        strategy.record_loss()
        strategy.record_loss()
        assert strategy.get_bet_multiplier() == 4
        
        strategy.record_win()
        assert strategy.get_bet_multiplier() == 1
    
    def test_uses_basic_strategy_decisions(self):
        """Test Martingale uses basic strategy for gameplay."""
        strategy = MartingaleStrategy()
        
        # Should hit on 16 vs 10 (basic strategy)
        hand = Hand([Card(Rank.TEN, Suit.SPADES), Card(Rank.SIX, Suit.HEARTS)])
        dealer_card = Card(Rank.TEN, Suit.DIAMONDS)
        action = strategy.decide(hand, dealer_card)
        assert action == Action.HIT
    
    def test_reset(self):
        """Test reset functionality."""
        strategy = MartingaleStrategy()
        
        strategy.record_loss()
        strategy.record_loss()
        assert strategy.get_bet_multiplier() > 1
        
        strategy.reset()
        assert strategy.get_bet_multiplier() == 1


class TestCardCountingStrategy:
    """Test suite for CardCountingStrategy class."""
    
    def test_initial_count(self):
        """Test initial running count is 0."""
        strategy = CardCountingStrategy()
        assert strategy.get_running_count() == 0
    
    def test_count_low_cards(self):
        """Test counting low cards (2-6) adds to count."""
        strategy = CardCountingStrategy()
        
        strategy.update_count(Card(Rank.TWO, Suit.SPADES))
        assert strategy.get_running_count() == 1
        
        strategy.update_count(Card(Rank.SIX, Suit.HEARTS))
        assert strategy.get_running_count() == 2
    
    def test_count_neutral_cards(self):
        """Test neutral cards (7-9) don't change count."""
        strategy = CardCountingStrategy()
        
        strategy.update_count(Card(Rank.SEVEN, Suit.SPADES))
        strategy.update_count(Card(Rank.EIGHT, Suit.HEARTS))
        strategy.update_count(Card(Rank.NINE, Suit.DIAMONDS))
        
        assert strategy.get_running_count() == 0
    
    def test_count_high_cards(self):
        """Test counting high cards (10-A) subtracts from count."""
        strategy = CardCountingStrategy()
        
        strategy.update_count(Card(Rank.TEN, Suit.SPADES))
        assert strategy.get_running_count() == -1
        
        strategy.update_count(Card(Rank.ACE, Suit.HEARTS))
        assert strategy.get_running_count() == -2
    
    def test_true_count_calculation(self):
        """Test true count calculation."""
        strategy = CardCountingStrategy()
        
        # Add 8 to running count
        for _ in range(8):
            strategy.update_count(Card(Rank.TWO, Suit.SPADES))
        
        # With 4 decks remaining: true count = 8 / 4 = 2
        true_count = strategy.get_true_count(decks_remaining=4.0)
        assert true_count == 2.0
        
        # With 2 decks remaining: true count = 8 / 2 = 4
        true_count = strategy.get_true_count(decks_remaining=2.0)
        assert true_count == 4.0
    
    def test_bet_multiplier_based_on_count(self):
        """Test bet multiplier increases with true count."""
        strategy = CardCountingStrategy()
        
        # Low count: multiplier = 1
        assert strategy.get_bet_multiplier(true_count=1) == 1
        
        # True count 2: multiplier = 2
        assert strategy.get_bet_multiplier(true_count=2) == 2
        
        # True count 3: multiplier = 4
        assert strategy.get_bet_multiplier(true_count=3) == 4
        
        # True count 5+: multiplier = 8
        assert strategy.get_bet_multiplier(true_count=5) == 8
    
    def test_insurance_with_high_count(self):
        """Test takes insurance when true count >= 3."""
        strategy = CardCountingStrategy()
        
        # Add cards to get true count >= 3
        for _ in range(12):
            strategy.update_count(Card(Rank.TWO, Suit.SPADES))
        
        hand = Hand([Card(Rank.TEN, Suit.SPADES), Card(Rank.NINE, Suit.HEARTS)])
        dealer_card = Card(Rank.ACE, Suit.DIAMONDS)
        
        # With 4 decks remaining: true count = 12 / 4 = 3
        # Should take insurance
        assert strategy.should_take_insurance(hand, dealer_card) is True
    
    def test_reset_count(self):
        """Test reset functionality."""
        strategy = CardCountingStrategy()
        
        for _ in range(5):
            strategy.update_count(Card(Rank.TWO, Suit.SPADES))
        
        assert strategy.get_running_count() > 0
        
        strategy.reset()
        assert strategy.get_running_count() == 0


class TestAction:
    """Test suite for Action enum."""
    
    def test_all_actions_exist(self):
        """Test all expected actions exist."""
        expected_actions = {
            "HIT", "STAND", "DOUBLE_DOWN", "SPLIT", "SURRENDER", "INSURANCE"
        }
        actual_actions = {action.name for action in Action}
        assert actual_actions == expected_actions
    
    def test_action_values(self):
        """Test action string values."""
        assert Action.HIT.value == "hit"
        assert Action.STAND.value == "stand"
        assert Action.DOUBLE_DOWN.value == "double"
