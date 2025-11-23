import streamlit as st
import sys
from pathlib import Path
import time

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.game import Game
from src.player import Player
from src.strategies import Action

# Page Config
st.set_page_config(
    page_title="Blackjack Pro",
    page_icon="♠️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Roboto:wght@400;700&display=swap');

    /* Global Styles */
    .stApp {
        background-color: #0f172a;
        background-image: radial-gradient(circle at 50% 0%, #1e293b 0%, #0f172a 100%);
        color: #e2e8f0;
        font-family: 'Roboto', sans-serif;
    }
    
    h1, h2, h3 {
        font-family: 'Playfair Display', serif;
        color: #f1f5f9;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }

    /* Card Styles */
    .card-container {
        display: flex;
        justify-content: center;
        gap: 15px;
        flex-wrap: wrap;
        min-height: 180px;
        padding: 20px;
        perspective: 1000px;
    }

    .card {
        display: inline-block;
        width: 110px;
        height: 160px;
        background: linear-gradient(135deg, #ffffff 0%, #f1f5f9 100%);
        border-radius: 12px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.4), inset 0 0 0 1px rgba(0,0,0,0.1);
        position: relative;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        user-select: none;
        transform-style: preserve-3d;
    }
    
    .card:hover {
        transform: translateY(-15px) rotate(2deg) scale(1.05);
        box-shadow: 0 20px 40px rgba(0,0,0,0.5);
        z-index: 10;
    }
    
    .card-top-left {
        position: absolute;
        top: 10px;
        left: 10px;
        font-size: 20px;
        font-weight: bold;
        line-height: 1;
    }
    
    .card-center {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        font-size: 52px;
    }
    
    .card-bottom-right {
        position: absolute;
        bottom: 10px;
        right: 10px;
        font-size: 20px;
        font-weight: bold;
        transform: rotate(180deg);
        line-height: 1;
    }
    
    .red { color: #dc2626; }
    .black { color: #1e293b; }
    
    /* Game Area */
    .game-table {
        background-color: #14532d;
        background-image: 
            radial-gradient(circle at 50% 50%, rgba(255,255,255,0.05) 0%, transparent 60%),
            repeating-linear-gradient(45deg, rgba(0,0,0,0.02) 0px, rgba(0,0,0,0.02) 2px, transparent 2px, transparent 4px);
        border-radius: 40px;
        padding: 50px;
        border: 16px solid #5D4037; /* Rich Wood border */
        box-shadow: 
            inset 0 0 100px rgba(0,0,0,0.8), 
            0 30px 60px rgba(0,0,0,0.6),
            0 0 0 2px #3E2723; /* Inner border detail */
        margin-bottom: 40px;
        text-align: center;
        position: relative;
    }
    
    .dealer-section {
        margin-bottom: 50px;
        border-bottom: 2px dashed rgba(255,255,255,0.15);
        padding-bottom: 30px;
    }
    
    .score-badge {
        background: linear-gradient(180deg, #fbbf24 0%, #d97706 100%);
        color: #451a03;
        padding: 8px 20px;
        border-radius: 30px;
        font-weight: 800;
        font-size: 1.1rem;
        display: inline-block;
        margin-top: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.4);
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Stats Box */
    .stats-container {
        display: flex;
        gap: 20px;
        justify-content: center;
        margin-bottom: 30px;
    }

    .stat-card {
        background: rgba(30, 41, 59, 0.8);
        backdrop-filter: blur(10px);
        padding: 20px 30px;
        border-radius: 16px;
        border: 1px solid rgba(148, 163, 184, 0.1);
        text-align: center;
        min-width: 140px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    }
    
    .stat-value {
        font-size: 28px;
        font-weight: 800;
        background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .stat-label {
        color: #94a3b8;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 5px;
    }
    
    /* Buttons */
    .stButton button {
        width: 100%;
        border-radius: 8px;
        font-weight: bold;
        background: linear-gradient(180deg, #334155 0%, #1e293b 100%);
        color: #e2e8f0;
        border: 1px solid #475569;
        padding: 0.5rem 1.5rem;
        transition: all 0.2s;
    }
    
    .stButton button:hover {
        background: linear-gradient(180deg, #475569 0%, #334155 100%);
        border-color: #64748b;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
        padding: 12px;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.2s;
    }
    
    /* Custom Button Colors via Streamlit config or CSS injection is tricky, 
       relying on theme primary color */
    
    </style>
""", unsafe_allow_html=True)

# Initialize Session State
if 'game' not in st.session_state:
    st.session_state.game = Game(Player("Player", bankroll=1000))
    st.session_state.game_active = False
    st.session_state.message = "Welcome to Blackjack Pro. Place your bet to start."
    st.session_state.message_type = "info" # info, success, error, warning

def get_suit_color(suit_symbol):
    return "red" if suit_symbol in ["♥", "♦"] else "black"

def render_card(card):
    if not card: # Hidden card
        return """
        <div class="card" style="background: repeating-linear-gradient(45deg, #1e293b, #1e293b 10px, #334155 10px, #334155 20px); border: 2px solid #475569;">
            <div class="card-center" style="color: #64748b;">♠️</div>
        </div>
        """
    
    rank = card.rank.value[0]
    suit = card.suit.value
    color = get_suit_color(suit)
    
    return f"""
    <div class="card">
        <div class="card-top-left {color}">{rank}<br>{suit}</div>
        <div class="card-center {color}">{suit}</div>
        <div class="card-bottom-right {color}">{rank}<br>{suit}</div>
    </div>
    """

# Header
col_h1, col_h2, col_h3 = st.columns([1, 2, 1])
with col_h2:
    st.markdown("<h1 style='text-align: center; margin-bottom: 30px;'>♠️ BLACKJACK PRO</h1>", unsafe_allow_html=True)

# Stats Bar
st.markdown(f"""
    <div class="stats-container">
        <div class="stat-card">
            <div class="stat-value">${st.session_state.game.player.bankroll}</div>
            <div class="stat-label">Bankroll</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{st.session_state.game.bet}</div>
            <div class="stat-label">Current Bet</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Main Game Area
col_game, col_controls = st.columns([3, 1])

with col_game:
    st.markdown("<div class='game-table'>", unsafe_allow_html=True)
    
    # Dealer Section
    st.markdown("<div class='dealer-section'>", unsafe_allow_html=True)
    st.markdown("<h3>DEALER</h3>", unsafe_allow_html=True)
    
    dealer_cards_html = "<div class='card-container'>"
    if st.session_state.game_active:
        # Show first card, hide second if round active
        if st.session_state.game.dealer.hand.cards:
            dealer_cards_html += render_card(st.session_state.game.dealer.hand.cards[0])
            if st.session_state.game.round_active:
                 dealer_cards_html += render_card(None) # Hidden card
            else:
                 for card in st.session_state.game.dealer.hand.cards[1:]:
                     dealer_cards_html += render_card(card)
    else:
        # Show empty slots or previous hand
        if st.session_state.game.dealer.hand.cards:
             for card in st.session_state.game.dealer.hand.cards:
                 dealer_cards_html += render_card(card)
        else:
            dealer_cards_html += "<div style='height: 145px; display: flex; align-items: center; color: rgba(255,255,255,0.3);'>Ready to deal</div>"
    
    dealer_cards_html += "</div>"
    st.markdown(dealer_cards_html, unsafe_allow_html=True)
    
    if not st.session_state.game.round_active and st.session_state.game.dealer.hand.cards:
        st.markdown(f"<div class='score-badge'>{st.session_state.game.dealer.hand.value}</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True) # End Dealer Section
    
    # Player Section
    st.markdown("<h3>PLAYER</h3>", unsafe_allow_html=True)
    
    player_cards_html = "<div class='card-container'>"
    if st.session_state.game.player.hand.cards:
        for card in st.session_state.game.player.hand.cards:
            player_cards_html += render_card(card)
    else:
        player_cards_html += "<div style='height: 145px; display: flex; align-items: center; color: rgba(255,255,255,0.3);'>Place your bet</div>"
        
    player_cards_html += "</div>"
    st.markdown(player_cards_html, unsafe_allow_html=True)
    
    if st.session_state.game.player.hand.cards:
        st.markdown(f"<div class='score-badge'>{st.session_state.game.player.hand.value}</div>", unsafe_allow_html=True)
        
    st.markdown("</div>", unsafe_allow_html=True) # End Game Table

with col_controls:
    st.markdown("### Actions")
    
    # Message Box
    if st.session_state.message:
        if st.session_state.message_type == "success":
            st.success(st.session_state.message)
        elif st.session_state.message_type == "error":
            st.error(st.session_state.message)
        else:
            st.info(st.session_state.message)
    
    st.markdown("---")
    
    if not st.session_state.game.round_active:
        bet_amount = st.number_input("Bet Amount", min_value=10, max_value=max(10, st.session_state.game.player.bankroll), value=10, step=10)
        
        if st.button("DEAL CARDS", type="primary"):
            st.session_state.game.bet = bet_amount
            # Start round logic
            if st.session_state.game.player.bankroll < bet_amount:
                st.session_state.message = "Insufficient funds!"
                st.session_state.message_type = "error"
            else:
                # Reset deck if needed
                if st.session_state.game.deck.needs_shuffle():
                    st.session_state.game.deck.reset()
                    st.session_state.game.deck.shuffle()
                
                # Place bet
                st.session_state.game.player.place_bet(bet_amount)
                
                # Deal
                st.session_state.game.player.clear_hands()
                st.session_state.game.dealer.clear_hand()
                
                st.session_state.game.player.add_card(st.session_state.game.deck.deal())
                st.session_state.game.dealer.add_card(st.session_state.game.deck.deal())
                st.session_state.game.player.add_card(st.session_state.game.deck.deal())
                st.session_state.game.dealer.add_card(st.session_state.game.deck.deal())
                
                st.session_state.game_active = True
                st.session_state.game.round_active = True
                
                # Check Blackjack
                if st.session_state.game.player.hand.is_blackjack:
                    if st.session_state.game.dealer.hand.is_blackjack:
                        st.session_state.game.player.win(bet_amount) # Push
                        st.session_state.message = "Push! Both have Blackjack."
                        st.session_state.message_type = "info"
                    else:
                        st.session_state.game.player.win(int(bet_amount * 2.5))
                        st.session_state.message = "BLACKJACK! You win!"
                        st.session_state.message_type = "success"
                    st.session_state.game.round_active = False
                elif st.session_state.game.dealer.hand.is_blackjack:
                    st.session_state.message = "Dealer has Blackjack. You lose."
                    st.session_state.message_type = "error"
                    st.session_state.game.round_active = False
                else:
                    st.session_state.message = "Your turn. Hit or Stand?"
                    st.session_state.message_type = "info"
            st.rerun()
            
        if st.button("RESET GAME"):
            st.session_state.game = Game(Player("Player", bankroll=1000))
            st.session_state.game_active = False
            st.session_state.message = "Game Reset."
            st.session_state.message_type = "info"
            st.rerun()
            
    else:
        # In Game Controls
        if st.button("HIT", type="primary"):
            st.session_state.game.player.add_card(st.session_state.game.deck.deal())
            if st.session_state.game.player.hand.is_bust:
                st.session_state.message = "BUST! You went over 21."
                st.session_state.message_type = "error"
                st.session_state.game.round_active = False
            st.rerun()
            
        if st.button("STAND"):
            # Dealer Turn
            while st.session_state.game.dealer.should_hit():
                st.session_state.game.dealer.add_card(st.session_state.game.deck.deal())
                time.sleep(0.5) # Small delay for effect (won't animate in Streamlit but good for logic)
            
            # Determine Winner
            result = st.session_state.game._determine_winner()
            
            if result == "win":
                st.session_state.message = "YOU WIN!"
                st.session_state.message_type = "success"
            elif result == "loss":
                st.session_state.message = "DEALER WINS."
                st.session_state.message_type = "error"
            else:
                st.session_state.message = "PUSH (Tie)."
                st.session_state.message_type = "info"
                
            st.session_state.game.round_active = False
            st.rerun()
            
        if st.button("DOUBLE DOWN", disabled=len(st.session_state.game.player.hand.cards) != 2):
            if st.session_state.game.player.bankroll >= st.session_state.game.bet:
                st.session_state.game.player.place_bet(st.session_state.game.bet) # Double bet
                st.session_state.game.player.add_card(st.session_state.game.deck.deal())
                
                if st.session_state.game.player.hand.is_bust:
                    st.session_state.message = "BUST! You went over 21."
                    st.session_state.message_type = "error"
                else:
                    # Dealer Turn
                    while st.session_state.game.dealer.should_hit():
                        st.session_state.game.dealer.add_card(st.session_state.game.deck.deal())
                    
                    result = st.session_state.game._determine_winner()
                    if result == "win":
                        st.session_state.message = "YOU WIN! (Double Down)"
                        st.session_state.message_type = "success"
                    elif result == "loss":
                        st.session_state.message = "DEALER WINS."
                        st.session_state.message_type = "error"
                    else:
                        st.session_state.message = "PUSH."
                        st.session_state.message_type = "info"
                
                st.session_state.game.round_active = False
                st.rerun()
            else:
                st.warning("Insufficient funds to double down!")

