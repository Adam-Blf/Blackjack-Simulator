"""Unit tests for Hand class."""

import pytest
from src.hand import Hand
from src.card import Card, Rank, Suit


class TestHand:
    """Test suite for Hand class."""
    
    def test_empty_hand(self):
        """Test creating an empty hand."""
        hand = Hand()
        assert len(hand) == 0
        assert hand.value == 0
        assert hand.is_bust is False
    
    def test_hand_with_initial_cards(self):
        """Test creating hand with initial cards."""
        cards = [
            Card(Rank.KING, Suit.SPADES),
            Card(Rank.FIVE, Suit.HEARTS)
        ]
        hand = Hand(cards)
        
        assert len(hand) == 2
        assert hand.value == 15
    
    def test_add_card(self):
        """Test adding cards to hand."""
        hand = Hand()
        
        hand.add_card(Card(Rank.TEN, Suit.SPADES))
        assert len(hand) == 1
        assert hand.value == 10
        
        hand.add_card(Card(Rank.SEVEN, Suit.HEARTS))
        assert len(hand) == 2
        assert hand.value == 17
    
    def test_clear_hand(self):
        """Test clearing hand."""
        hand = Hand([
            Card(Rank.KING, Suit.SPADES),
            Card(Rank.FIVE, Suit.HEARTS)
        ])
        
        hand.clear()
        assert len(hand) == 0
        assert hand.value == 0
    
    def test_blackjack_natural(self):
        """Test natural blackjack (Ace + 10)."""
        hand = Hand([
            Card(Rank.ACE, Suit.SPADES),
            Card(Rank.KING, Suit.HEARTS)
        ])
        
        assert hand.is_blackjack is True
        assert hand.value == 21
    
    def test_blackjack_ace_face_card(self):
        """Test blackjack with Ace and face card."""
        for face_rank in [Rank.JACK, Rank.QUEEN, Rank.KING]:
            hand = Hand([
                Card(Rank.ACE, Suit.SPADES),
                Card(face_rank, Suit.HEARTS)
            ])
            assert hand.is_blackjack is True
    
    def test_not_blackjack_three_cards(self):
        """Test that 21 with 3 cards is not blackjack."""
        hand = Hand([
            Card(Rank.SEVEN, Suit.SPADES),
            Card(Rank.SEVEN, Suit.HEARTS),
            Card(Rank.SEVEN, Suit.DIAMONDS)
        ])
        
        assert hand.value == 21
        assert hand.is_blackjack is False
    
    def test_bust(self):
        """Test bust detection."""
        hand = Hand([
            Card(Rank.KING, Suit.SPADES),
            Card(Rank.QUEEN, Suit.HEARTS),
            Card(Rank.FIVE, Suit.DIAMONDS)
        ])
        
        assert hand.value == 25
        assert hand.is_bust is True
    
    def test_ace_adjustment_simple(self):
        """Test Ace value adjustment (11 -> 1)."""
        hand = Hand([
            Card(Rank.ACE, Suit.SPADES),
            Card(Rank.NINE, Suit.HEARTS)
        ])
        
        # Ace + 9 = 20 (Ace as 11)
        assert hand.value == 20
        
        # Add another card
        hand.add_card(Card(Rank.FIVE, Suit.DIAMONDS))
        
        # Ace + 9 + 5 = 15 (Ace as 1)
        assert hand.value == 15
        assert hand.is_bust is False
    
    def test_multiple_aces(self):
        """Test hand with multiple Aces."""
        hand = Hand([
            Card(Rank.ACE, Suit.SPADES),
            Card(Rank.ACE, Suit.HEARTS),
            Card(Rank.NINE, Suit.DIAMONDS)
        ])
        
        # One Ace as 11, one as 1: 11 + 1 + 9 = 21
        assert hand.value == 21
    
    def test_soft_hand(self):
        """Test soft hand detection."""
        hand = Hand([
            Card(Rank.ACE, Suit.SPADES),
            Card(Rank.SIX, Suit.HEARTS)
        ])
        
        # Ace + 6 = soft 17
        assert hand.is_soft is True
        assert hand.value == 17
    
    def test_hard_hand(self):
        """Test hard hand (no Ace or Ace as 1)."""
        hand = Hand([
            Card(Rank.KING, Suit.SPADES),
            Card(Rank.SEVEN, Suit.HEARTS)
        ])
        
        assert hand.is_soft is False
        assert hand.value == 17
    
    def test_soft_becomes_hard(self):
        """Test soft hand becoming hard after hit."""
        hand = Hand([
            Card(Rank.ACE, Suit.SPADES),
            Card(Rank.SIX, Suit.HEARTS)
        ])
        
        assert hand.is_soft is True
        
        # Hit with 10
        hand.add_card(Card(Rank.TEN, Suit.DIAMONDS))
        
        # Now hard 17 (Ace as 1)
        assert hand.is_soft is False
        assert hand.value == 17
    
    def test_is_pair(self):
        """Test pair detection."""
        hand = Hand([
            Card(Rank.EIGHT, Suit.SPADES),
            Card(Rank.EIGHT, Suit.HEARTS)
        ])
        
        assert hand.is_pair is True
    
    def test_not_pair_different_ranks(self):
        """Test non-pair with different ranks."""
        hand = Hand([
            Card(Rank.EIGHT, Suit.SPADES),
            Card(Rank.SEVEN, Suit.HEARTS)
        ])
        
        assert hand.is_pair is False
    
    def test_not_pair_three_cards(self):
        """Test three cards is not a pair."""
        hand = Hand([
            Card(Rank.EIGHT, Suit.SPADES),
            Card(Rank.EIGHT, Suit.HEARTS),
            Card(Rank.EIGHT, Suit.DIAMONDS)
        ])
        
        assert hand.is_pair is False
    
    def test_can_split(self):
        """Test can_split logic."""
        hand = Hand([
            Card(Rank.EIGHT, Suit.SPADES),
            Card(Rank.EIGHT, Suit.HEARTS)
        ])
        
        assert hand.can_split is True
        
        # After marking as split, can't split again
        hand.mark_split()
        assert hand.can_split is False
    
    def test_can_double_down(self):
        """Test can_double_down logic."""
        hand = Hand([
            Card(Rank.FIVE, Suit.SPADES),
            Card(Rank.SIX, Suit.HEARTS)
        ])
        
        assert hand.can_double_down is True
        
        # After third card, can't double
        hand.add_card(Card(Rank.THREE, Suit.DIAMONDS))
        assert hand.can_double_down is False
    
    def test_mark_flags(self):
        """Test marking hand with various flags."""
        hand = Hand([
            Card(Rank.TEN, Suit.SPADES),
            Card(Rank.FIVE, Suit.HEARTS)
        ])
        
        assert hand.is_split is False
        assert hand.is_doubled is False
        assert hand.is_surrendered is False
        
        hand.mark_split()
        assert hand.is_split is True
        
        hand.mark_doubled()
        assert hand.is_doubled is True
        
        hand.mark_surrendered()
        assert hand.is_surrendered is True
    
    def test_string_representation_normal(self):
        """Test string representation of normal hand."""
        hand = Hand([
            Card(Rank.KING, Suit.SPADES),
            Card(Rank.SEVEN, Suit.HEARTS)
        ])
        
        str_repr = str(hand)
        assert "K♠" in str_repr
        assert "7♥" in str_repr
        assert "[17]" in str_repr
    
    def test_string_representation_blackjack(self):
        """Test string representation of blackjack."""
        hand = Hand([
            Card(Rank.ACE, Suit.SPADES),
            Card(Rank.KING, Suit.HEARTS)
        ])
        
        str_repr = str(hand)
        assert "BLACKJACK" in str_repr
    
    def test_string_representation_bust(self):
        """Test string representation of bust."""
        hand = Hand([
            Card(Rank.KING, Suit.SPADES),
            Card(Rank.QUEEN, Suit.HEARTS),
            Card(Rank.FIVE, Suit.DIAMONDS)
        ])
        
        str_repr = str(hand)
        assert "BUST" in str_repr
    
    def test_string_representation_soft(self):
        """Test string representation of soft hand."""
        hand = Hand([
            Card(Rank.ACE, Suit.SPADES),
            Card(Rank.SIX, Suit.HEARTS)
        ])
        
        str_repr = str(hand)
        assert "(soft)" in str_repr


class TestHandEdgeCases:
    """Test edge cases for Hand class."""
    
    def test_four_aces(self):
        """Test hand with four Aces."""
        hand = Hand([
            Card(Rank.ACE, Suit.SPADES),
            Card(Rank.ACE, Suit.HEARTS),
            Card(Rank.ACE, Suit.DIAMONDS),
            Card(Rank.ACE, Suit.CLUBS)
        ])
        
        # One Ace as 11, three as 1: 11 + 1 + 1 + 1 = 14
        assert hand.value == 14
        assert hand.is_bust is False
    
    def test_all_low_cards_no_bust(self):
        """Test many low cards don't cause issues."""
        hand = Hand()
        for _ in range(8):
            hand.add_card(Card(Rank.TWO, Suit.SPADES))
        
        assert hand.value == 16
        assert hand.is_bust is False
    
    def test_cards_property_returns_copy(self):
        """Test that cards property returns a copy."""
        cards = [Card(Rank.KING, Suit.SPADES), Card(Rank.FIVE, Suit.HEARTS)]
        hand = Hand(cards)
        
        returned_cards = hand.cards
        returned_cards.pop()
        
        # Original hand should be unchanged
        assert len(hand) == 2
