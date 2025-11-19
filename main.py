"""
Blackjack Simulator - Main Entry Point
Professional Blackjack game with AI strategies, statistics, and CLI interface.

Author: Adam Beloucif
GitHub: @Adam-Blf
License: MIT
"""

import argparse
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.ui import BlackjackCLI
from src.game import Game
from src.player import Player
from src.strategies import (
    BasicStrategy,
    ConservativeStrategy,
    AggressiveStrategy,
    MartingaleStrategy,
    CardCountingStrategy
)
from src.stats import Statistics


def main():
    """Main entry point for the Blackjack Simulator."""
    
    parser = argparse.ArgumentParser(
        description="🃏 Blackjack Simulator - Professional casino Blackjack with AI strategies",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                              # Launch interactive CLI
  python main.py --simulate 1000              # Simulate 1000 games with Basic Strategy
  python main.py --simulate 500 --strategy aggressive  # Simulate with Aggressive strategy
  python main.py --compare-strategies         # Compare all strategies performance
  python main.py --bankroll 5000 --bet 25     # Start with custom bankroll and bet
        """
    )
    
    parser.add_argument(
        "--simulate",
        type=int,
        metavar="N",
        help="Simulate N games with AI (non-interactive mode)"
    )
    
    parser.add_argument(
        "--strategy",
        choices=["basic", "conservative", "aggressive", "martingale", "counting"],
        default="basic",
        help="Strategy to use for simulation (default: basic)"
    )
    
    parser.add_argument(
        "--compare-strategies",
        action="store_true",
        help="Compare all strategies performance"
    )
    
    parser.add_argument(
        "--bankroll",
        type=int,
        default=1000,
        help="Initial bankroll (default: 1000)"
    )
    
    parser.add_argument(
        "--bet",
        type=int,
        default=10,
        help="Base bet amount (default: 10)"
    )
    
    parser.add_argument(
        "--decks",
        type=int,
        default=6,
        choices=[1, 2, 4, 6, 8],
        help="Number of decks in shoe (default: 6)"
    )
    
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Show statistics from previous sessions"
    )
    
    args = parser.parse_args()
    
    # Show stats and exit
    if args.stats:
        stats = Statistics()
        if stats.load_from_file():
            print(stats.format_summary())
            stats.plot_bankroll_evolution()
        else:
            print("❌ No statistics found. Play some games first!")
        return
    
    # Compare strategies mode
    if args.compare_strategies:
        compare_strategies(args.bankroll, args.bet, args.simulate or 500, args.decks)
        return
    
    # Simulation mode
    if args.simulate:
        simulate_games(args.simulate, args.strategy, args.bankroll, args.bet, args.decks)
        return
    
    # Interactive CLI mode (default)
    cli = BlackjackCLI(bankroll=args.bankroll, bet=args.bet, decks=args.decks)
    cli.run()


def simulate_games(n_games: int, strategy_name: str, bankroll: int, bet: int, decks: int):
    """Simulate N games with specified strategy."""
    
    print(f"\n🎲 Simulating {n_games} games with {strategy_name.upper()} strategy...")
    print(f"💰 Initial bankroll: ${bankroll}")
    print(f"💵 Base bet: ${bet}")
    print(f"🃏 Decks: {decks}\n")
    
    # Create strategy
    strategies = {
        "basic": BasicStrategy(),
        "conservative": ConservativeStrategy(),
        "aggressive": AggressiveStrategy(),
        "martingale": MartingaleStrategy(),
        "counting": CardCountingStrategy()
    }
    strategy = strategies[strategy_name]
    
    # Create player and game
    player = Player(name="AI Player", bankroll=bankroll, strategy=strategy)
    game = Game(player=player, bet=bet, num_decks=decks)
    
    # Statistics
    stats = Statistics()
    wins = 0
    losses = 0
    pushes = 0
    blackjacks = 0
    
    # Run simulation
    for i in range(n_games):
        result = game.play_auto()
        
        if result == "win":
            wins += 1
        elif result == "loss":
            losses += 1
        elif result == "push":
            pushes += 1
        
        if game.player.hand and game.player.hand.is_blackjack():
            blackjacks += 1
        
        # Progress indicator
        if (i + 1) % 100 == 0:
            print(f"Progress: {i + 1}/{n_games} games ({(i+1)/n_games*100:.1f}%)")
        
        # Check if bankrupt
        if player.bankroll <= 0:
            print(f"\n💸 Player went bankrupt after {i + 1} games!")
            break
    
    # Print results
    print(f"\n{'='*60}")
    print(f"📊 SIMULATION RESULTS")
    print(f"{'='*60}")
    print(f"Games Played:      {wins + losses + pushes}")
    print(f"Wins:              {wins} ({wins/(wins+losses+pushes)*100:.1f}%)")
    print(f"Losses:            {losses} ({losses/(wins+losses+pushes)*100:.1f}%)")
    print(f"Pushes:            {pushes} ({pushes/(wins+losses+pushes)*100:.1f}%)")
    print(f"Blackjacks:        {blackjacks} ({blackjacks/(wins+losses+pushes)*100:.1f}%)")
    print(f"\n💰 Initial Bankroll: ${bankroll}")
    print(f"💰 Final Bankroll:   ${player.bankroll}")
    print(f"💵 Net Profit/Loss:  ${player.bankroll - bankroll}")
    print(f"📈 ROI:              {(player.bankroll - bankroll)/bankroll*100:.2f}%")
    print(f"{'='*60}\n")


def compare_strategies(bankroll: int, bet: int, n_games: int, decks: int):
    """Compare all strategies performance."""
    
    print(f"\n🔬 Comparing all strategies over {n_games} games...")
    print(f"💰 Bankroll: ${bankroll} | 💵 Bet: ${bet} | 🃏 Decks: {decks}\n")
    
    strategies = {
        "Basic Strategy": BasicStrategy(),
        "Conservative": ConservativeStrategy(),
        "Aggressive": AggressiveStrategy(),
        "Martingale": MartingaleStrategy(),
        "Card Counting": CardCountingStrategy()
    }
    
    results = {}
    
    for name, strategy in strategies.items():
        print(f"Testing {name}...")
        
        player = Player(name=name, bankroll=bankroll, strategy=strategy)
        game = Game(player=player, bet=bet, num_decks=decks)
        
        wins = 0
        losses = 0
        pushes = 0
        
        for _ in range(n_games):
            result = game.play_auto()
            if result == "win":
                wins += 1
            elif result == "loss":
                losses += 1
            else:
                pushes += 1
            
            if player.bankroll <= 0:
                break
        
        results[name] = {
            "final_bankroll": player.bankroll,
            "profit": player.bankroll - bankroll,
            "roi": (player.bankroll - bankroll) / bankroll * 100,
            "wins": wins,
            "losses": losses,
            "pushes": pushes,
            "winrate": wins / (wins + losses) * 100 if (wins + losses) > 0 else 0
        }
    
    # Print comparison table
    print(f"\n{'='*80}")
    print(f"📊 STRATEGY COMPARISON")
    print(f"{'='*80}")
    print(f"{'Strategy':<20} {'Final $':<12} {'Profit':<12} {'ROI':<10} {'Winrate':<10}")
    print(f"{'-'*80}")
    
    for name, data in sorted(results.items(), key=lambda x: x[1]['roi'], reverse=True):
        print(f"{name:<20} ${data['final_bankroll']:<11} ${data['profit']:<11} "
              f"{data['roi']:>7.2f}%  {data['winrate']:>7.2f}%")
    
    print(f"{'='*80}\n")
    
    # Best strategy
    best = max(results.items(), key=lambda x: x[1]['roi'])
    print(f"🏆 Best Strategy: {best[0]} with {best[1]['roi']:.2f}% ROI\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Thanks for playing! Goodbye.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
