"""UI module - Rich-based CLI interface for Blackjack."""

from typing import Optional
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.text import Text
    from rich.prompt import Prompt, Confirm
    from rich import box
    HAS_RICH = True
except ImportError:
    HAS_RICH = False

from .game import Game
from .player import Player
from .strategies import BasicStrategy, ConservativeStrategy, AggressiveStrategy


class BlackjackCLI:
    """Rich-based CLI interface for Blackjack game."""
    
    def __init__(self, bankroll: int = 1000, bet: int = 10, decks: int = 6):
        """
        Initialize CLI.
        
        Args:
            bankroll: Initial player bankroll
            bet: Base bet amount
            decks: Number of decks in shoe
        """
        self.bankroll = bankroll
        self.bet = bet
        self.decks = decks
        
        if HAS_RICH:
            self.console = Console()
        else:
            self.console = None
    
    def run(self):
        """Run the interactive CLI."""
        if not HAS_RICH:
            self._run_simple()
            return
        
        self._show_welcome()
        
        while True:
            choice = self._show_menu()
            
            if choice == "1":
                self._play_game()
            elif choice == "2":
                self._show_stats()
            elif choice == "3":
                self._simulate()
            elif choice == "4":
                self._settings()
            elif choice == "5":
                self._show_rules()
            elif choice == "6":
                self._goodbye()
                break
    
    def _show_welcome(self):
        """Display welcome screen."""
        welcome = Panel(
            Text("🃏 BLACKJACK SIMULATOR 🃏", justify="center", style="bold magenta"),
            box=box.DOUBLE,
            border_style="magenta"
        )
        self.console.print(welcome)
        self.console.print()
    
    def _show_menu(self) -> str:
        """Show main menu and get choice."""
        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column("Option", style="cyan bold")
        table.add_column("Description")
        
        table.add_row("1", "🎲 New Game")
        table.add_row("2", "📊 Statistics")
        table.add_row("3", "🤖 Simulate N Games")
        table.add_row("4", "⚙️  Settings")
        table.add_row("5", "📖 Rules")
        table.add_row("6", "❌ Quit")
        
        self.console.print(Panel(table, title="Main Menu", border_style="cyan"))
        
        return Prompt.ask("\nYour choice", choices=["1", "2", "3", "4", "5", "6"], default="1")
    
    def _play_game(self):
        """Play an interactive game."""
        strategy = self._select_strategy()
        player = Player("You", self.bankroll, strategy)
        game = Game(player, self.bet, self.decks)
        
        self.console.print(f"\n💰 Bankroll: ${player.bankroll}", style="green bold")
        self.console.print(f"💵 Bet: ${self.bet}\n", style="yellow bold")
        
        # Simplified game loop (would need full implementation)
        self.console.print("🎮 Game starting... (Full implementation needed)")
        self.console.print("Press Enter to continue...")
        input()
    
    def _select_strategy(self):
        """Let user select a strategy."""
        table = Table(show_header=False, box=None)
        table.add_column("", style="cyan bold")
        table.add_column("")
        
        table.add_row("1", "Basic Strategy (Optimal)")
        table.add_row("2", "Conservative")
        table.add_row("3", "Aggressive")
        
        self.console.print(Panel(table, title="Select Strategy", border_style="cyan"))
        
        choice = Prompt.ask("Strategy", choices=["1", "2", "3"], default="1")
        
        strategies = {
            "1": BasicStrategy(),
            "2": ConservativeStrategy(),
            "3": AggressiveStrategy()
        }
        
        return strategies[choice]
    
    def _show_stats(self):
        """Show statistics."""
        self.console.print("\n📊 Statistics feature coming soon!", style="yellow")
        self.console.print("Press Enter to continue...")
        input()
    
    def _simulate(self):
        """Simulate multiple games."""
        n = Prompt.ask("\nHow many games to simulate?", default="100")
        self.console.print(f"\n🎲 Simulating {n} games...", style="cyan")
        self.console.print("(Full implementation needed)")
        self.console.print("Press Enter to continue...")
        input()
    
    def _settings(self):
        """Change settings."""
        self.console.print("\n⚙️  Current Settings:", style="cyan bold")
        self.console.print(f"  💰 Bankroll: ${self.bankroll}")
        self.console.print(f"  💵 Bet: ${self.bet}")
        self.console.print(f"  🃏 Decks: {self.decks}")
        
        if Confirm.ask("\nChange settings?", default=False):
            self.bankroll = int(Prompt.ask("New bankroll", default=str(self.bankroll)))
            self.bet = int(Prompt.ask("New bet", default=str(self.bet)))
            self.decks = int(Prompt.ask("New decks", default=str(self.decks)))
            self.console.print("\n✅ Settings updated!", style="green")
        
        self.console.print("Press Enter to continue...")
        input()
    
    def _show_rules(self):
        """Display Blackjack rules."""
        rules = """
[bold cyan]🎯 Blackjack Rules[/bold cyan]

[bold]Objective:[/bold] Beat the dealer by getting as close to 21 as possible without going over.

[bold]Card Values:[/bold]
  • Number cards (2-10): Face value
  • Face cards (J, Q, K): 10
  • Ace: 1 or 11 (player's choice)

[bold]Actions:[/bold]
  • [cyan]Hit[/cyan]: Take another card
  • [cyan]Stand[/cyan]: Keep current hand
  • [cyan]Double Down[/cyan]: Double bet, take one card, then stand
  • [cyan]Split[/cyan]: Split pair into two hands (doubles bet)
  • [cyan]Insurance[/cyan]: Side bet when dealer shows Ace

[bold]Payouts:[/bold]
  • Win: 1:1 (bet × 2)
  • Blackjack (A + 10): 3:2 (bet × 2.5)
  • Insurance: 2:1
  • Push (tie): bet returned

[bold]Dealer Rules:[/bold]
  • Must hit on 16 or less
  • Must stand on 17 or more
        """
        
        self.console.print(Panel(rules, border_style="cyan"))
        self.console.print("Press Enter to continue...")
        input()
    
    def _goodbye(self):
        """Display goodbye message."""
        goodbye = Panel(
            Text("👋 Thanks for playing!\nCome back soon!", justify="center", style="bold green"),
            border_style="green"
        )
        self.console.print(goodbye)
    
    def _run_simple(self):
        """Fallback CLI without Rich."""
        print("\n" + "="*50)
        print(" "*15 + "🃏 BLACKJACK 🃏")
        print("="*50)
        print("\nNote: Install 'rich' for better UI (pip install rich)")
        print("\n1. Play Game")
        print("2. Quit")
        
        choice = input("\nChoice: ").strip()
        
        if choice == "1":
            print("\n💰 Starting game with $1000 bankroll...")
            print("(Full game implementation needed)")
        
        print("\n👋 Goodbye!")
