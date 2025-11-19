"""Unit tests for Deck class."""

import pytest
from src.deck import Deck
from src.card import Card, Rank, Suit


class TestDeck:
    """Test suite for Deck class."""
    
    def test_deck_creation(self):
        """Test creating a deck."""
        deck = Deck(num_decks=1, shuffle_on_init=False)
        assert deck.num_decks == 1
        assert deck.remaining == 52
        assert deck.dealt_count == 0
    
    def test_deck_invalid_num_decks(self):
        """Test creating deck with invalid number."""
        with pytest.raises(ValueError):
            Deck(num_decks=0)
        
        with pytest.raises(ValueError):
            Deck(num_decks=-1)
    
    def test_multiple_decks(self):
        """Test creating deck with multiple standard decks."""
        deck = Deck(num_decks=6, shuffle_on_init=False)
        assert deck.total_cards == 52 * 6
        assert deck.remaining == 52 * 6
    
    def test_deal_card(self):
        """Test dealing a single card."""
        deck = Deck(num_decks=1, shuffle_on_init=False)
        initial_count = deck.remaining
        
        card = deck.deal()
        
        assert isinstance(card, Card)
        assert deck.remaining == initial_count - 1
        assert deck.dealt_count == 1
    
    def test_deal_multiple_cards(self):
        """Test dealing multiple cards."""
        deck = Deck(num_decks=1, shuffle_on_init=False)
        
        cards = deck.deal_multiple(5)
        
        assert len(cards) == 5
        assert all(isinstance(card, Card) for card in cards)
        assert deck.remaining == 52 - 5
        assert deck.dealt_count == 5
    
    def test_deal_from_empty_deck(self):
        """Test dealing from empty deck returns None."""
        deck = Deck(num_decks=1, shuffle_on_init=False)
        
        # Deal all cards
        deck.deal_multiple(52)
        
        # Try to deal one more
        card = deck.deal()
        assert card is None
    
    def test_shuffle(self):
        """Test shuffling changes card order."""
        deck1 = Deck(num_decks=1, shuffle_on_init=False)
        deck2 = Deck(num_decks=1, shuffle_on_init=False)
        
        cards1_before = deck1.cards
        
        deck1.shuffle()
        cards1_after = deck1.cards
        
        # After shuffle, order should be different (very unlikely to be same)
        assert cards1_before != cards1_after
        
        # But should have same cards
        assert len(cards1_before) == len(cards1_after)
    
    def test_reset_deck(self):
        """Test resetting deck."""
        deck = Deck(num_decks=1)
        
        # Deal some cards
        deck.deal_multiple(10)
        assert deck.remaining < 52
        
        # Reset
        deck.reset()
        assert deck.remaining == 52
        assert deck.dealt_count == 0
    
    def test_needs_shuffle(self):
        """Test needs_shuffle detection."""
        deck = Deck(num_decks=1, shuffle_on_init=False)
        
        # Fresh deck shouldn't need shuffle
        assert deck.needs_shuffle(threshold=0.25) is False
        
        # Deal 75% of cards
        deck.deal_multiple(40)
        
        # Now should need shuffle (< 25% remaining)
        assert deck.needs_shuffle(threshold=0.25) is True
    
    def test_deck_properties(self):
        """Test deck properties."""
        deck = Deck(num_decks=2)
        
        assert deck.total_cards == 104
        assert deck.remaining <= 104
        assert deck.dealt_count >= 0
        assert deck.remaining + deck.dealt_count == 104
    
    def test_dealt_cards_tracking(self):
        """Test that dealt cards are tracked correctly."""
        deck = Deck(num_decks=1, shuffle_on_init=False)
        
        dealt = []
        for _ in range(5):
            card = deck.deal()
            dealt.append(card)
        
        assert len(deck.dealt_cards) == 5
        assert deck.dealt_cards == dealt
    
    def test_cards_property_returns_copy(self):
        """Test that cards property returns a copy."""
        deck = Deck(num_decks=1)
        
        cards = deck.cards
        original_length = len(cards)
        
        # Modifying returned list shouldn't affect deck
        cards.pop()
        
        assert len(deck.cards) == original_length
    
    def test_len_operator(self):
        """Test __len__ operator."""
        deck = Deck(num_decks=1, shuffle_on_init=False)
        
        assert len(deck) == 52
        
        deck.deal()
        assert len(deck) == 51
    
    def test_string_representation(self):
        """Test string representation."""
        deck = Deck(num_decks=2)
        
        str_repr = str(deck)
        assert "remaining" in str_repr
        assert "dealt" in str_repr
        assert "decks=2" in str_repr


class TestDeckIntegration:
    """Integration tests for Deck class."""
    
    def test_full_deck_composition(self):
        """Test that deck contains correct cards."""
        deck = Deck(num_decks=1, shuffle_on_init=False)
        
        # Count each rank
        rank_counts = {rank: 0 for rank in Rank}
        suit_counts = {suit: 0 for suit in Suit}
        
        all_cards = deck.cards
        for card in all_cards:
            rank_counts[card.rank] += 1
            suit_counts[card.suit] += 1
        
        # Should have 4 of each rank
        for count in rank_counts.values():
            assert count == 4
        
        # Should have 13 of each suit
        for count in suit_counts.values():
            assert count == 13
    
    def test_multiple_deck_composition(self):
        """Test multiple deck composition."""
        deck = Deck(num_decks=3, shuffle_on_init=False)
        
        # Count specific card
        ace_of_spades_count = sum(
            1 for card in deck.cards 
            if card.rank == Rank.ACE and card.suit == Suit.SPADES
        )
        
        assert ace_of_spades_count == 3
