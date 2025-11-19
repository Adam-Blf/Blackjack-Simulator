"""Statistics module - Track and analyze game performance."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Optional
import json
from pathlib import Path


@dataclass
class GameRecord:
    """Record of a single game."""
    timestamp: datetime
    result: str  # "win", "loss", "push"
    bet: int
    payout: int
    bankroll_after: int
    was_blackjack: bool = False
    was_split: bool = False
    was_doubled: bool = False
    dealer_busted: bool = False
    player_busted: bool = False


@dataclass
class Statistics:
    """Track and analyze game statistics."""
    
    games: List[GameRecord] = field(default_factory=list)
    total_wagered: int = 0
    total_won: int = 0
    total_lost: int = 0
    
    def record_game(self, record: GameRecord):
        """Record a game result."""
        self.games.append(record)
        self.total_wagered += record.bet
        
        if record.result == "win":
            self.total_won += record.payout
        elif record.result == "loss":
            self.total_lost += record.bet
    
    @property
    def games_played(self) -> int:
        """Total games played."""
        return len(self.games)
    
    @property
    def wins(self) -> int:
        """Number of wins."""
        return sum(1 for g in self.games if g.result == "win")
    
    @property
    def losses(self) -> int:
        """Number of losses."""
        return sum(1 for g in self.games if g.result == "loss")
    
    @property
    def pushes(self) -> int:
        """Number of pushes."""
        return sum(1 for g in self.games if g.result == "push")
    
    @property
    def winrate(self) -> float:
        """Win rate percentage."""
        total = self.wins + self.losses
        return (self.wins / total * 100) if total > 0 else 0.0
    
    @property
    def net_profit(self) -> int:
        """Net profit/loss."""
        return self.total_won - self.total_lost
    
    @property
    def roi(self) -> float:
        """Return on investment percentage."""
        return (self.net_profit / self.total_wagered * 100) if self.total_wagered > 0 else 0.0
    
    @property
    def blackjacks(self) -> int:
        """Number of blackjacks."""
        return sum(1 for g in self.games if g.was_blackjack)
    
    @property
    def player_busts(self) -> int:
        """Number of player busts."""
        return sum(1 for g in self.games if g.player_busted)
    
    @property
    def dealer_busts(self) -> int:
        """Number of dealer busts."""
        return sum(1 for g in self.games if g.dealer_busted)
    
    def format_summary(self) -> str:
        """Format statistics summary."""
        summary = f"""
╔══════════════════════════════════════╗
║       📊 SESSION STATISTICS          ║
╚══════════════════════════════════════╝

Games Played       : {self.games_played:,}
Wins               : {self.wins} ({self.winrate:.1f}%)
Losses             : {self.losses} ({self.losses/self.games_played*100 if self.games_played > 0 else 0:.1f}%)
Pushes             : {self.pushes} ({self.pushes/self.games_played*100 if self.games_played > 0 else 0:.1f}%)

Blackjacks         : {self.blackjacks} ({self.blackjacks/self.games_played*100 if self.games_played > 0 else 0:.1f}%)
Player Busts       : {self.player_busts} ({self.player_busts/self.games_played*100 if self.games_played > 0 else 0:.1f}%)
Dealer Busts       : {self.dealer_busts} ({self.dealer_busts/self.games_played*100 if self.games_played > 0 else 0:.1f}%)

Total Wagered      : ${self.total_wagered:,}
Net Profit/Loss    : ${self.net_profit:,}
ROI                : {self.roi:.2f}%
"""
        return summary
    
    def save_to_file(self, filepath: str = "data/stats/history.json") -> bool:
        """Save statistics to JSON file."""
        try:
            path = Path(filepath)
            path.parent.mkdir(parents=True, exist_ok=True)
            
            data = {
                "timestamp": datetime.now().isoformat(),
                "games_played": self.games_played,
                "wins": self.wins,
                "losses": self.losses,
                "pushes": self.pushes,
                "total_wagered": self.total_wagered,
                "total_won": self.total_won,
                "total_lost": self.total_lost,
                "net_profit": self.net_profit,
                "roi": self.roi,
                "games": [
                    {
                        "timestamp": g.timestamp.isoformat(),
                        "result": g.result,
                        "bet": g.bet,
                        "payout": g.payout,
                        "bankroll_after": g.bankroll_after,
                        "was_blackjack": g.was_blackjack
                    }
                    for g in self.games
                ]
            }
            
            with open(path, 'w') as f:
                json.dump(data, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error saving stats: {e}")
            return False
    
    def load_from_file(self, filepath: str = "data/stats/history.json") -> bool:
        """Load statistics from JSON file."""
        try:
            path = Path(filepath)
            if not path.exists():
                return False
            
            with open(path, 'r') as f:
                data = json.load(f)
            
            self.total_wagered = data["total_wagered"]
            self.total_won = data["total_won"]
            self.total_lost = data["total_lost"]
            
            # Reconstruct game records
            self.games = [
                GameRecord(
                    timestamp=datetime.fromisoformat(g["timestamp"]),
                    result=g["result"],
                    bet=g["bet"],
                    payout=g["payout"],
                    bankroll_after=g["bankroll_after"],
                    was_blackjack=g.get("was_blackjack", False)
                )
                for g in data["games"]
            ]
            
            return True
        except Exception as e:
            print(f"Error loading stats: {e}")
            return False
    
    def plot_bankroll_evolution(self):
        """Plot bankroll evolution over time (requires matplotlib)."""
        try:
            import matplotlib.pyplot as plt
            
            if not self.games:
                print("No games to plot")
                return
            
            bankrolls = [g.bankroll_after for g in self.games]
            
            plt.figure(figsize=(12, 6))
            plt.plot(bankrolls, linewidth=2)
            plt.title("Bankroll Evolution", fontsize=16, fontweight='bold')
            plt.xlabel("Game Number", fontsize=12)
            plt.ylabel("Bankroll ($)", fontsize=12)
            plt.grid(True, alpha=0.3)
            plt.axhline(y=bankrolls[0], color='r', linestyle='--', alpha=0.5, label='Initial')
            plt.legend()
            plt.tight_layout()
            plt.show()
            
        except ImportError:
            print("Matplotlib not installed. Install with: pip install matplotlib")
