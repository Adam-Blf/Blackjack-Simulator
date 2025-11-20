"""
Blackjack Simulator - Modern GUI Interface
Professional graphical interface with visual cards and animations.

Author: Adam Beloucif
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sys
from pathlib import Path
from typing import Optional, List
import threading
import queue

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from .game import Game
from .player import Player
from .card import Card
from .strategies import (
    BasicStrategy, ConservativeStrategy, AggressiveStrategy,
    MartingaleStrategy, CardCountingStrategy, Strategy
)


class ModernButton(tk.Canvas):
    """Custom modern button with hover effects."""
    
    def __init__(self, parent, text, command, width=120, height=40, 
                 bg="#667eea", hover_bg="#764ba2", fg="white"):
        super().__init__(parent, width=width, height=height, 
                        highlightthickness=0, bg=parent.cget('bg'))
        
        self.command = command
        self.bg_color = bg
        self.hover_color = hover_bg
        self.fg_color = fg
        self.text = text
        
        # Draw button
        self.rect = self.create_rectangle(0, 0, width, height, 
                                          fill=bg, outline="", 
                                          width=0)
        self.text_id = self.create_text(width//2, height//2, 
                                       text=text, fill=fg, 
                                       font=("Segoe UI", 10, "bold"))
        
        # Bind events
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)
        
    def on_enter(self, event):
        self.itemconfig(self.rect, fill=self.hover_color)
        self.config(cursor="hand2")
        
    def on_leave(self, event):
        self.itemconfig(self.rect, fill=self.bg_color)
        self.config(cursor="")
        
    def on_click(self, event):
        if self.command:
            self.command()


class CardWidget(tk.Canvas):
    """Visual playing card widget."""
    
    SUITS = {"♠": "black", "♥": "red", "♦": "red", "♣": "black"}
    
    def __init__(self, parent, card: Optional[Card] = None, hidden=False):
        super().__init__(parent, width=70, height=100, 
                        highlightthickness=1, highlightbackground="#ddd",
                        bg="white")
        
        self.card = card
        self.hidden = hidden
        
        if hidden:
            self._draw_back()
        elif card:
            self._draw_card()
    
    def _draw_back(self):
        """Draw card back."""
        self.create_rectangle(5, 5, 65, 95, fill="#1e3a8a", outline="#1e3a8a")
        for i in range(0, 90, 10):
            self.create_line(10, 10+i, 60, 10+i, fill="#3b82f6", width=2)
        self.create_text(35, 50, text="🃏", font=("Segoe UI", 30))
    
    def _draw_card(self):
        """Draw card face."""
        suit = self.card.suit.value
        rank = self.card.rank.symbol
        color = self.SUITS.get(suit, "black")
        
        # Card border
        self.create_rectangle(2, 2, 68, 98, fill="white", outline="#333", width=2)
        
        # Top left
        self.create_text(12, 15, text=rank, fill=color, 
                        font=("Segoe UI", 16, "bold"), anchor="nw")
        self.create_text(12, 32, text=suit, fill=color, 
                        font=("Segoe UI", 20), anchor="nw")
        
        # Center
        self.create_text(35, 50, text=suit, fill=color, 
                        font=("Segoe UI", 40))
        
        # Bottom right (rotated)
        self.create_text(58, 85, text=rank, fill=color, 
                        font=("Segoe UI", 16, "bold"), anchor="se", angle=180)
        self.create_text(58, 68, text=suit, fill=color, 
                        font=("Segoe UI", 20), anchor="se", angle=180)


class BlackjackGUI:
    """Modern GUI for Blackjack Simulator."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🃏 Blackjack Simulator Pro")
        self.root.geometry("1200x800")
        self.root.configure(bg="#1a1a2e")
        
        # Game state
        self.game: Optional[Game] = None
        self.bankroll = 1000
        self.bet_amount = 10
        self.strategy: Strategy = BasicStrategy()
        self.strategy_name = "Basic Strategy"
        self.num_decks = 6
        
        # Queue for thread-safe updates
        self.update_queue = queue.Queue()
        
        # Build UI
        self._build_ui()
        
        # Start game
        self._reset_game()
        
        # Start update checker
        self._check_queue()
    
    def _build_ui(self):
        """Build the user interface."""
        
        # Header
        header = tk.Frame(self.root, bg="#0f3460", height=80)
        header.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(header, text="🃏 BLACKJACK SIMULATOR PRO", 
                font=("Segoe UI", 28, "bold"), 
                bg="#0f3460", fg="white").pack(pady=15)
        
        # Main container
        main = tk.Frame(self.root, bg="#1a1a2e")
        main.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Left panel - Game area
        game_panel = tk.Frame(main, bg="#16213e", relief=tk.RAISED, bd=2)
        game_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        self._build_game_area(game_panel)
        
        # Right panel - Controls
        control_panel = tk.Frame(main, bg="#16213e", width=350, relief=tk.RAISED, bd=2)
        control_panel.pack(side=tk.RIGHT, fill=tk.Y)
        control_panel.pack_propagate(False)
        
        self._build_controls(control_panel)
    
    def _build_game_area(self, parent):
        """Build game visualization area."""
        
        # Dealer section
        dealer_frame = tk.Frame(parent, bg="#16213e")
        dealer_frame.pack(pady=20)
        
        tk.Label(dealer_frame, text="🎩 DEALER", 
                font=("Segoe UI", 18, "bold"), 
                bg="#16213e", fg="#e94560").pack()
        
        self.dealer_value_label = tk.Label(dealer_frame, text="Value: -", 
                                          font=("Segoe UI", 14), 
                                          bg="#16213e", fg="white")
        self.dealer_value_label.pack(pady=5)
        
        self.dealer_cards_frame = tk.Frame(dealer_frame, bg="#16213e")
        self.dealer_cards_frame.pack(pady=10)
        
        # Separator
        tk.Canvas(parent, height=2, bg="#e94560", highlightthickness=0).pack(fill=tk.X, padx=50)
        
        # Player section
        player_frame = tk.Frame(parent, bg="#16213e")
        player_frame.pack(pady=20)
        
        tk.Label(player_frame, text="👤 PLAYER", 
                font=("Segoe UI", 18, "bold"), 
                bg="#16213e", fg="#00d9ff").pack()
        
        self.player_value_label = tk.Label(player_frame, text="Value: -", 
                                          font=("Segoe UI", 14), 
                                          bg="#16213e", fg="white")
        self.player_value_label.pack(pady=5)
        
        self.player_cards_frame = tk.Frame(player_frame, bg="#16213e")
        self.player_cards_frame.pack(pady=10)
        
        # Result message
        self.result_label = tk.Label(parent, text="", 
                                     font=("Segoe UI", 20, "bold"), 
                                     bg="#16213e", fg="#ffd700")
        self.result_label.pack(pady=20)
        
        # Action buttons
        action_frame = tk.Frame(parent, bg="#16213e")
        action_frame.pack(pady=20)
        
        self.hit_btn = ModernButton(action_frame, "HIT", self._hit, 
                                    width=100, height=50, 
                                    bg="#00d9ff", hover_bg="#00a8cc")
        self.hit_btn.pack(side=tk.LEFT, padx=5)
        
        self.stand_btn = ModernButton(action_frame, "STAND", self._stand, 
                                     width=100, height=50,
                                     bg="#e94560", hover_bg="#c41e3a")
        self.stand_btn.pack(side=tk.LEFT, padx=5)
        
        self.double_btn = ModernButton(action_frame, "DOUBLE", self._double, 
                                      width=100, height=50,
                                      bg="#ffa500", hover_bg="#ff8c00")
        self.double_btn.pack(side=tk.LEFT, padx=5)
        
        self.deal_btn = ModernButton(action_frame, "NEW DEAL", self._new_deal, 
                                    width=120, height=50,
                                    bg="#4caf50", hover_bg="#45a049")
        self.deal_btn.pack(side=tk.LEFT, padx=5)
    
    def _build_controls(self, parent):
        """Build control panel."""
        
        # Title
        tk.Label(parent, text="⚙️ SETTINGS", 
                font=("Segoe UI", 18, "bold"), 
                bg="#16213e", fg="white").pack(pady=15)
        
        # Bankroll info
        info_frame = tk.Frame(parent, bg="#0f3460", relief=tk.RAISED, bd=2)
        info_frame.pack(fill=tk.X, padx=15, pady=10)
        
        tk.Label(info_frame, text="💰 Bankroll", 
                font=("Segoe UI", 12, "bold"), 
                bg="#0f3460", fg="#ffd700").pack(pady=5)
        
        self.bankroll_label = tk.Label(info_frame, text=f"${self.bankroll}", 
                                       font=("Segoe UI", 24, "bold"), 
                                       bg="#0f3460", fg="white")
        self.bankroll_label.pack(pady=5)
        
        # Bet amount
        bet_frame = tk.Frame(parent, bg="#16213e")
        bet_frame.pack(fill=tk.X, padx=15, pady=10)
        
        tk.Label(bet_frame, text="💵 Bet Amount:", 
                font=("Segoe UI", 12), 
                bg="#16213e", fg="white").pack(anchor=tk.W)
        
        bet_control = tk.Frame(bet_frame, bg="#16213e")
        bet_control.pack(fill=tk.X, pady=5)
        
        self.bet_var = tk.IntVar(value=self.bet_amount)
        bet_entry = tk.Spinbox(bet_control, from_=1, to=1000, 
                              textvariable=self.bet_var,
                              font=("Segoe UI", 12), width=10,
                              bg="#0f3460", fg="white",
                              buttonbackground="#667eea",
                              command=self._update_bet)
        bet_entry.pack(side=tk.LEFT)
        
        # Strategy selection
        strategy_frame = tk.Frame(parent, bg="#16213e")
        strategy_frame.pack(fill=tk.X, padx=15, pady=10)
        
        tk.Label(strategy_frame, text="🎯 Strategy:", 
                font=("Segoe UI", 12), 
                bg="#16213e", fg="white").pack(anchor=tk.W)
        
        strategies = [
            "Basic Strategy",
            "Conservative",
            "Aggressive",
            "Martingale",
            "Card Counting"
        ]
        
        self.strategy_var = tk.StringVar(value=self.strategy_name)
        strategy_combo = ttk.Combobox(strategy_frame, 
                                     textvariable=self.strategy_var,
                                     values=strategies,
                                     font=("Segoe UI", 11),
                                     state="readonly")
        strategy_combo.pack(fill=tk.X, pady=5)
        strategy_combo.bind("<<ComboboxSelected>>", self._change_strategy)
        
        # Decks
        deck_frame = tk.Frame(parent, bg="#16213e")
        deck_frame.pack(fill=tk.X, padx=15, pady=10)
        
        tk.Label(deck_frame, text="🃏 Number of Decks:", 
                font=("Segoe UI", 12), 
                bg="#16213e", fg="white").pack(anchor=tk.W)
        
        self.deck_var = tk.IntVar(value=self.num_decks)
        deck_scale = tk.Scale(deck_frame, from_=1, to=8, 
                            variable=self.deck_var,
                            orient=tk.HORIZONTAL,
                            font=("Segoe UI", 10),
                            bg="#16213e", fg="white",
                            troughcolor="#0f3460",
                            highlightthickness=0,
                            command=self._update_decks)
        deck_scale.pack(fill=tk.X, pady=5)
        
        # Separator
        tk.Canvas(parent, height=2, bg="#e94560", highlightthickness=0).pack(fill=tk.X, padx=15, pady=20)
        
        # Auto-play
        auto_frame = tk.Frame(parent, bg="#16213e")
        auto_frame.pack(fill=tk.X, padx=15, pady=10)
        
        tk.Label(auto_frame, text="🤖 Auto-Play", 
                font=("Segoe UI", 14, "bold"), 
                bg="#16213e", fg="white").pack(pady=5)
        
        tk.Label(auto_frame, text="Simulate N games:", 
                font=("Segoe UI", 10), 
                bg="#16213e", fg="#ccc").pack(anchor=tk.W)
        
        self.auto_games_var = tk.IntVar(value=100)
        auto_entry = tk.Spinbox(auto_frame, from_=10, to=10000, 
                               textvariable=self.auto_games_var,
                               font=("Segoe UI", 11), width=15,
                               bg="#0f3460", fg="white",
                               increment=10)
        auto_entry.pack(fill=tk.X, pady=5)
        
        ModernButton(auto_frame, "▶ SIMULATE", self._simulate, 
                    width=200, height=40).pack(pady=5)
        
        ModernButton(auto_frame, "📊 COMPARE STRATEGIES", 
                    self._compare_strategies,
                    width=200, height=40,
                    bg="#764ba2", hover_bg="#667eea").pack(pady=5)
        
        # Stats display
        stats_frame = tk.Frame(parent, bg="#0f3460", relief=tk.RAISED, bd=2)
        stats_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        tk.Label(stats_frame, text="📈 Session Stats", 
                font=("Segoe UI", 12, "bold"), 
                bg="#0f3460", fg="white").pack(pady=5)
        
        self.stats_text = scrolledtext.ScrolledText(stats_frame, 
                                                    height=10,
                                                    font=("Consolas", 9),
                                                    bg="#1a1a2e", fg="#00ff00",
                                                    wrap=tk.WORD)
        self.stats_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Reset button
        ModernButton(parent, "🔄 RESET GAME", self._reset_game,
                    width=250, height=45,
                    bg="#e94560", hover_bg="#c41e3a").pack(pady=10)
    
    def _update_bet(self):
        """Update bet amount."""
        self.bet_amount = self.bet_var.get()
    
    def _change_strategy(self, event=None):
        """Change playing strategy."""
        strategy_name = self.strategy_var.get()
        
        strategies_map = {
            "Basic Strategy": BasicStrategy(),
            "Conservative": ConservativeStrategy(),
            "Aggressive": AggressiveStrategy(),
            "Martingale": MartingaleStrategy(),
            "Card Counting": CardCountingStrategy()
        }
        
        self.strategy = strategies_map.get(strategy_name, BasicStrategy())
        self.strategy_name = strategy_name
        self._reset_game()
    
    def _update_decks(self, value):
        """Update number of decks."""
        self.num_decks = int(value)
        self._reset_game()
    
    def _reset_game(self):
        """Reset game to initial state."""
        self.bankroll = 1000
        player = Player(name="Player", bankroll=self.bankroll, strategy=self.strategy)
        self.game = Game(player=player, bet=self.bet_amount, num_decks=self.num_decks)
        self._update_display()
        self._log("Game reset. Ready to play!")
    
    def _new_deal(self):
        """Deal new hand."""
        if self.game.player.bankroll < self.bet_amount:
            messagebox.showwarning("Insufficient Funds", 
                                  "Not enough money to place bet!")
            return
        
        self.result_label.config(text="")
        
        if self.game.start_round():
            self._update_display()
            self._log(f"New hand dealt. Bet: ${self.bet_amount}")
            
            # Check for immediate win/loss
            if self.game.player.hand.is_blackjack:
                self._log("🎉 BLACKJACK! Player wins 3:2")
                self.result_label.config(text="🎉 BLACKJACK!")
                self._disable_actions()
        else:
            self._log("Failed to start round")
    
    def _hit(self):
        """Player hits."""
        if not self.game.round_active:
            return
        
        card = self.game.deck.deal()
        if card:
            self.game.player.add_card(card)
            self._update_display()
            self._log(f"Player hits: {card}")
            
            if self.game.player.hand.is_bust:
                self._log("💥 BUST! Player loses")
                self.result_label.config(text="💥 BUST!")
                self._dealer_play()
                self._disable_actions()
    
    def _stand(self):
        """Player stands."""
        if not self.game.round_active:
            return
        
        self._log("Player stands")
        self._dealer_play()
        self._disable_actions()
    
    def _double(self):
        """Player doubles down."""
        if not self.game.round_active:
            return
        
        if self.game.player.bankroll < self.bet_amount:
            messagebox.showwarning("Insufficient Funds", 
                                  "Not enough money to double down!")
            return
        
        self.game.player.place_bet(self.bet_amount)
        card = self.game.deck.deal()
        if card:
            self.game.player.add_card(card)
            self._update_display()
            self._log(f"Player doubles down: {card}")
            
            if not self.game.player.hand.is_bust:
                self._dealer_play()
            else:
                self._log("💥 BUST! Player loses")
                self.result_label.config(text="💥 BUST!")
            
            self._disable_actions()
    
    def _dealer_play(self):
        """Dealer plays their hand."""
        # Reveal dealer's hidden card
        self._update_display(show_dealer=True)
        
        while self.game.dealer.should_hit():
            card = self.game.deck.deal()
            if card:
                self.game.dealer.add_card(card)
                self._update_display(show_dealer=True)
                self.root.update()
                self.root.after(500)
                self._log(f"Dealer hits: {card}")
        
        self._log(f"Dealer stands at {self.game.dealer.hand.value}")
        self._determine_winner()
    
    def _determine_winner(self):
        """Determine and display winner."""
        player_value = self.game.player.hand.value
        dealer_value = self.game.dealer.hand.value
        
        if self.game.player.hand.is_bust:
            self.result_label.config(text="😢 DEALER WINS")
            self._log("Result: Dealer wins (Player bust)")
        elif self.game.dealer.hand.is_bust:
            self.game.player.win(self.game.player.current_bet * 2)
            self.result_label.config(text="🎉 PLAYER WINS!")
            self._log("Result: Player wins (Dealer bust)")
        elif player_value > dealer_value:
            self.game.player.win(self.game.player.current_bet * 2)
            self.result_label.config(text="🎉 PLAYER WINS!")
            self._log("Result: Player wins")
        elif player_value < dealer_value:
            self.result_label.config(text="😢 DEALER WINS")
            self._log("Result: Dealer wins")
        else:
            self.game.player.win(self.game.player.current_bet)
            self.result_label.config(text="🤝 PUSH")
            self._log("Result: Push (tie)")
        
        self.game.round_active = False
        self._update_display(show_dealer=True)
    
    def _update_display(self, show_dealer=False):
        """Update visual display."""
        # Clear existing cards
        for widget in self.dealer_cards_frame.winfo_children():
            widget.destroy()
        for widget in self.player_cards_frame.winfo_children():
            widget.destroy()
        
        # Show dealer cards
        if self.game.dealer.hand.cards:
            for i, card in enumerate(self.game.dealer.hand.cards):
                hide = (i == 1 and not show_dealer and self.game.round_active)
                card_widget = CardWidget(self.dealer_cards_frame, card, hidden=hide)
                card_widget.pack(side=tk.LEFT, padx=3)
            
            if show_dealer or not self.game.round_active:
                self.dealer_value_label.config(text=f"Value: {self.game.dealer.hand.value}")
            else:
                self.dealer_value_label.config(text=f"Value: {self.game.dealer.hand.cards[0].value}")
        
        # Show player cards
        if self.game.player.hand.cards:
            for card in self.game.player.hand.cards:
                card_widget = CardWidget(self.player_cards_frame, card)
                card_widget.pack(side=tk.LEFT, padx=3)
            
            self.player_value_label.config(text=f"Value: {self.game.player.hand.value}")
        
        # Update bankroll
        self.bankroll_label.config(text=f"${self.game.player.bankroll}")
    
    def _disable_actions(self):
        """Disable action buttons."""
        self.hit_btn.config(state=tk.DISABLED)
        self.stand_btn.config(state=tk.DISABLED)
        self.double_btn.config(state=tk.DISABLED)
    
    def _enable_actions(self):
        """Enable action buttons."""
        self.hit_btn.config(state=tk.NORMAL)
        self.stand_btn.config(state=tk.NORMAL)
        self.double_btn.config(state=tk.NORMAL)
    
    def _log(self, message):
        """Add message to stats log."""
        self.stats_text.insert(tk.END, f"> {message}\n")
        self.stats_text.see(tk.END)
    
    def _simulate(self):
        """Run simulation in background thread."""
        n_games = self.auto_games_var.get()
        
        def run_simulation():
            self._log(f"Starting simulation: {n_games} games...")
            
            player = Player(name="AI", bankroll=1000, strategy=self.strategy)
            game = Game(player=player, bet=self.bet_amount, num_decks=self.num_decks)
            
            wins = losses = pushes = 0
            
            for i in range(n_games):
                result = game.play_auto()
                if result == "win":
                    wins += 1
                elif result == "loss":
                    losses += 1
                else:
                    pushes += 1
                
                if player.bankroll <= 0:
                    break
            
            # Update UI from main thread
            self.update_queue.put(lambda: self._show_simulation_results(
                wins, losses, pushes, player.bankroll, n_games
            ))
        
        thread = threading.Thread(target=run_simulation, daemon=True)
        thread.start()
    
    def _show_simulation_results(self, wins, losses, pushes, final_bankroll, total):
        """Show simulation results."""
        winrate = wins / (wins + losses) * 100 if (wins + losses) > 0 else 0
        profit = final_bankroll - 1000
        
        self._log("=" * 40)
        self._log(f"SIMULATION RESULTS ({total} games)")
        self._log(f"Wins: {wins} ({winrate:.1f}%)")
        self._log(f"Losses: {losses}")
        self._log(f"Pushes: {pushes}")
        self._log(f"Final Bankroll: ${final_bankroll}")
        self._log(f"Profit/Loss: ${profit:+d}")
        self._log("=" * 40)
    
    def _compare_strategies(self):
        """Compare all strategies."""
        messagebox.showinfo("Compare Strategies", 
                          "Running comparison... This may take a moment.")
        
        # Use terminal for comparison (better formatting)
        self._log("Opening comparison in console...")
        import subprocess
        subprocess.Popen([sys.executable, "main.py", "--compare-strategies"])
    
    def _check_queue(self):
        """Check for updates from background threads."""
        try:
            while True:
                callback = self.update_queue.get_nowait()
                callback()
        except queue.Empty:
            pass
        
        self.root.after(100, self._check_queue)
    
    def run(self):
        """Run the GUI application."""
        self.root.mainloop()


def main():
    """Launch the GUI."""
    app = BlackjackGUI()
    app.run()


if __name__ == "__main__":
    main()
