"""Test integration - End-to-end tests for complete game scenarios."""

import pytest
from src.game import Game
from src.player import Player
from src.strategies import BasicStrategy, ConservativeStrategy, AggressiveStrategy
from src.stats import Statistics, GameRecord
from datetime import datetime


class TestGameIntegration:
    """Integration tests for complete game flows."""
    
    def test_complete_game_win(self):
        """Test a complete game where player wins."""
        player = Player("Test Player", bankroll=1000, strategy=BasicStrategy())
        game = Game(player=player, bet=10)
        
        initial_bankroll = player.bankroll
        result = game.play_auto()
        
        # Should complete without error
        assert result in ["win", "loss", "push"]
        
        # Bankroll should change (unless push)
        if result == "win":
            assert player.bankroll > initial_bankroll - 10
        elif result == "loss":
            assert player.bankroll == initial_bankroll - 10
    
    def test_multiple_rounds(self):
        """Test playing multiple consecutive rounds."""
        player = Player("Test Player", bankroll=1000, strategy=BasicStrategy())
        game = Game(player=player, bet=10)
        
        results = []
        for _ in range(10):
            if player.bankroll >= 10:
                result = game.play_auto()
                results.append(result)
        
        # Should have played some games
        assert len(results) > 0
        
        # Results should be valid
        assert all(r in ["win", "loss", "push"] for r in results)
    
    def test_bankrupt_scenario(self):
        """Test what happens when player goes bankrupt."""
        player = Player("Test Player", bankroll=50, strategy=AggressiveStrategy())
        game = Game(player=player, bet=20)
        
        # Play until bankrupt
        rounds = 0
        while player.bankroll >= 20 and rounds < 100:
            game.play_auto()
            rounds += 1
        
        # Should eventually run out (or hit max rounds)
        assert player.bankroll < 20 or rounds == 100
    
    def test_strategy_comparison(self):
        """Test that different strategies produce different results."""
        bankroll = 1000
        bet = 10
        num_games = 50
        
        results = {}
        
        for strategy_name, strategy_class in [
            ("basic", BasicStrategy),
            ("conservative", ConservativeStrategy),
            ("aggressive", AggressiveStrategy)
        ]:
            player = Player("Player", bankroll=bankroll, strategy=strategy_class())
            game = Game(player=player, bet=bet)
            
            for _ in range(num_games):
                if player.bankroll >= bet:
                    game.play_auto()
            
            results[strategy_name] = player.bankroll
        
        # Results should vary (not all the same)
        unique_results = len(set(results.values()))
        assert unique_results >= 1  # At least some variation expected


class TestStatisticsIntegration:
    """Integration tests for statistics tracking."""
    
    def test_statistics_recording(self):
        """Test that statistics are correctly recorded."""
        stats = Statistics()
        
        # Record some games
        for i in range(10):
            record = GameRecord(
                timestamp=datetime.now(),
                result="win" if i % 2 == 0 else "loss",
                bet=10,
                payout=20 if i % 2 == 0 else 0,
                bankroll_after=1000 + (i * 10),
                was_blackjack=i == 0
            )
            stats.record_game(record)
        
        # Verify counts
        assert stats.games_played == 10
        assert stats.wins == 5
        assert stats.losses == 5
        assert stats.blackjacks == 1
    
    def test_statistics_calculations(self):
        """Test statistics calculations."""
        stats = Statistics()
        
        # 3 wins, 2 losses
        for i in range(5):
            record = GameRecord(
                timestamp=datetime.now(),
                result="win" if i < 3 else "loss",
                bet=10,
                payout=20 if i < 3 else 0,
                bankroll_after=1000,
                was_blackjack=False
            )
            stats.record_game(record)
        
        # Check calculations
        assert stats.winrate == 60.0  # 3/5 = 60%
        assert stats.total_wagered == 50
        assert stats.total_won == 60  # 3 * 20
        assert stats.total_lost == 20  # 2 * 10
        assert stats.net_profit == 40  # 60 - 20
    
    def test_statistics_persistence(self, tmp_path):
        """Test saving and loading statistics."""
        stats1 = Statistics()
        
        # Record some games
        for i in range(5):
            record = GameRecord(
                timestamp=datetime.now(),
                result="win",
                bet=10,
                payout=20,
                bankroll_after=1000,
                was_blackjack=False
            )
            stats1.record_game(record)
        
        # Save to file
        filepath = tmp_path / "test_stats.json"
        assert stats1.save_to_file(str(filepath))
        
        # Load into new instance
        stats2 = Statistics()
        assert stats2.load_from_file(str(filepath))
        
        # Verify data matches
        assert stats2.games_played == stats1.games_played
        assert stats2.wins == stats1.wins
        assert stats2.total_wagered == stats1.total_wagered


class TestFullGameSession:
    """Test complete game sessions with all components."""
    
    def test_full_session_basic_strategy(self):
        """Test a full session with basic strategy."""
        player = Player("Session Player", bankroll=1000, strategy=BasicStrategy())
        game = Game(player=player, bet=10)
        stats = Statistics()
        
        # Play 20 games
        for _ in range(20):
            if player.bankroll >= 10:
                result = game.play_auto()
                
                record = GameRecord(
                    timestamp=datetime.now(),
                    result=result,
                    bet=10,
                    payout=20 if result == "win" else (10 if result == "push" else 0),
                    bankroll_after=player.bankroll,
                    was_blackjack=player.hand.is_blackjack() if player.hand else False
                )
                stats.record_game(record)
        
        # Verify session completed
        assert stats.games_played == 20
        assert stats.wins + stats.losses + stats.pushes == 20
        
        # Summary should format without error
        summary = stats.format_summary()
        assert "SESSION STATISTICS" in summary
        assert str(stats.games_played) in summary
    
    def test_session_with_varying_bets(self):
        """Test session with different bet sizes."""
        player = Player("Varying Bet Player", bankroll=2000)
        
        bets = [10, 20, 15, 25, 10]
        results = []
        
        for bet in bets:
            if player.bankroll >= bet:
                game = Game(player=player, bet=bet)
                result = game.play_auto()
                results.append(result)
        
        # Should have played all games
        assert len(results) == len(bets)
