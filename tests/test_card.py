"""Unit tests for Card class."""

import pytest
from src.card import Card, Rank, Suit


class TestCard:
    """Test suite for Card class."""
    
    def test_card_creation(self):
        """Test creating a card."""
        card = Card(Rank.ACE, Suit.SPADES)
        assert card.rank == Rank.ACE
        assert card.suit == Suit.SPADES
    
    def test_card_value(self):
        """Test card value property."""
        ace = Card(Rank.ACE, Suit.HEARTS)
        king = Card(Rank.KING, Suit.DIAMONDS)
        five = Card(Rank.FIVE, Suit.CLUBS)
        
        assert ace.value == 11
        assert king.value == 10
        assert five.value == 5
    
    def test_is_ace(self):
        """Test is_ace property."""
        ace = Card(Rank.ACE, Suit.SPADES)
        king = Card(Rank.KING, Suit.HEARTS)
        
        assert ace.is_ace is True
        assert king.is_ace is False
    
    def test_is_face_card(self):
        """Test is_face_card property."""
        jack = Card(Rank.JACK, Suit.SPADES)
        queen = Card(Rank.QUEEN, Suit.HEARTS)
        king = Card(Rank.KING, Suit.DIAMONDS)
        ten = Card(Rank.TEN, Suit.CLUBS)
        
        assert jack.is_face_card is True
        assert queen.is_face_card is True
        assert king.is_face_card is True
        assert ten.is_face_card is False
    
    def test_is_ten_value(self):
        """Test is_ten_value property."""
        ten = Card(Rank.TEN, Suit.SPADES)
        jack = Card(Rank.JACK, Suit.HEARTS)
        queen = Card(Rank.QUEEN, Suit.DIAMONDS)
        king = Card(Rank.KING, Suit.CLUBS)
        nine = Card(Rank.NINE, Suit.SPADES)
        
        assert ten.is_ten_value is True
        assert jack.is_ten_value is True
        assert queen.is_ten_value is True
        assert king.is_ten_value is True
        assert nine.is_ten_value is False
    
    def test_card_string_representation(self):
        """Test string representation."""
        card = Card(Rank.ACE, Suit.SPADES)
        assert str(card) == "A♠"
        
        card = Card(Rank.KING, Suit.HEARTS)
        assert str(card) == "K♥"
    
    def test_card_comparison(self):
        """Test card comparison."""
        five = Card(Rank.FIVE, Suit.SPADES)
        ten = Card(Rank.TEN, Suit.HEARTS)
        
        assert five < ten
        assert not ten < five
    
    def test_card_equality(self):
        """Test card equality."""
        card1 = Card(Rank.ACE, Suit.SPADES)
        card2 = Card(Rank.ACE, Suit.SPADES)
        card3 = Card(Rank.ACE, Suit.HEARTS)
        
        assert card1 == card2
        assert card1 != card3
    
    def test_card_hash(self):
        """Test card is hashable."""
        card1 = Card(Rank.KING, Suit.DIAMONDS)
        card2 = Card(Rank.KING, Suit.DIAMONDS)
        card3 = Card(Rank.QUEEN, Suit.DIAMONDS)
        
        card_set = {card1, card2, card3}
        assert len(card_set) == 2  # card1 and card2 are same


class TestRank:
    """Test suite for Rank enum."""
    
    def test_all_ranks_have_symbol(self):
        """Test all ranks have symbol attribute."""
        for rank in Rank:
            assert hasattr(rank, 'symbol')
            assert isinstance(rank.symbol, str)
    
    def test_all_ranks_have_value(self):
        """Test all ranks have value attribute."""
        for rank in Rank:
            assert hasattr(rank, 'value')
            assert isinstance(rank.value, int)
            assert 1 <= rank.value <= 11
    
    def test_face_cards_value(self):
        """Test face cards have value 10."""
        assert Rank.JACK.value == 10
        assert Rank.QUEEN.value == 10
        assert Rank.KING.value == 10
    
    def test_ace_value(self):
        """Test Ace has value 11."""
        assert Rank.ACE.value == 11


class TestSuit:
    """Test suite for Suit enum."""
    
    def test_all_suits_have_unicode(self):
        """Test all suits have Unicode symbols."""
        expected_symbols = {"♠", "♥", "♦", "♣"}
        actual_symbols = {suit.value for suit in Suit}
        assert actual_symbols == expected_symbols
    
    def test_suit_count(self):
        """Test there are exactly 4 suits."""
        assert len(Suit) == 4
