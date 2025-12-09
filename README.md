![Dernier commit](https://img.shields.io/badge/Dernier%20commit-23/11/2025-brightgreen) ![Langage principal](https://img.shields.io/badge/Langage%20principal-Python-blue) ![Nombre de langages](https://img.shields.io/badge/Nombre%20de%20langages-2-orange)

### Construit avec les outils et technologies : 
![Python](https://img.shields.io/badge/-Python-lightgrey) ![Batchfile](https://img.shields.io/badge/-Batchfile-lightgrey)

🇫🇷 Français | 🇬🇧 Anglais | 🇪🇸 Espagnol | 🇮🇹 Italien | 🇵🇹 Portugais | 🇷🇺 Russe | 🇩🇪 Allemand | 🇹🇷 Turc

# 🃏 Blackjack Simulator

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-pytest-orange.svg)](https://pytest.org/)
[![Coverage](https://img.shields.io/badge/Coverage-95%25-brightgreen.svg)]()

> Simulateur de Blackjack professionnel en Python avec POO avancée, gestion d'états, stratégies IA, et tests unitaires complets.

[English](#english) | [Français](#français)

---

## 🇫🇷 Français

### 📝 Description

Simulateur de Blackjack complet implémentant les règles officielles du casino avec :
- Architecture orientée objet robuste (10+ classes)
- Machine à états pour le déroulement des parties
- Stratégies de jeu configurables (Basic Strategy, Martingale, etc.)
- Interface CLI colorée avec Rich
- Statistiques détaillées et historique des parties
- Tests unitaires exhaustifs (pytest, >95% coverage)
- Sauvegarde/chargement de parties

### ⚡ Fonctionnalités Principales

#### 🎮 Gameplay
- ✅ Règles officielles Blackjack (Hit, Stand, Double Down, Split, Insurance)
- ✅ Dealer automatique avec stratégie standard (hit jusqu'à 17)
- ✅ Gestion multi-mains (après split)
- ✅ Blackjack naturel (3:2 payout)
- ✅ Assurance contre Blackjack du dealer (1:2)

#### 🧠 Stratégies IA
- ✅ **Basic Strategy** : stratégie mathématiquement optimale
- ✅ **Conservative** : minimiser les risques
- ✅ **Aggressive** : maximiser les gains potentiels
- ✅ **Martingale** : doubler la mise après perte
- ✅ **Card Counting** : Hi-Lo strategy (optionnel)

#### 📊 Statistiques & Analyse
- ✅ Winrate, profit/loss, ROI
- ✅ Historique complet des parties
- ✅ Graphiques évolution bankroll (matplotlib)
- ✅ Export CSV/JSON
- ✅ Comparaison stratégies

#### 🎨 Interface
- ✅ CLI interactive avec Rich (couleurs, tableaux, progress bars)
- ✅ **GUI Tkinter moderne** (mode graphique complet)
- ✅ Affichage cartes Unicode (♠️♥️♣️♦️)
- ✅ Animations (distribution cartes, résultats)
- ✅ Aide contextuelle

### 🛠️ Technologies

- **Langage** : Python 3.10+
- **POO** : dataclasses, enums, abstract base classes
- **CLI** : Rich (terminal formatting)
- **Tests** : pytest, pytest-cov, unittest.mock
- **Data** : pandas (stats), matplotlib (graphs)
- **State Management** : Custom FSM (Finite State Machine)
- **Persistence** : JSON, pickle

### 📂 Architecture

```
Blackjack-Simulator/
├── src/
│   ├── __init__.py
│   ├── card.py              # Classe Card (valeur, couleur)
│   ├── deck.py              # Classe Deck (mélange, distribution)
│   ├── hand.py              # Classe Hand (calcul score, actions)
│   ├── player.py            # Classe Player (bankroll, stratégie)
│   ├── dealer.py            # Classe Dealer (stratégie fixe)
│   ├── game.py              # Classe Game (FSM, logique principale)
│   ├── strategies.py        # Stratégies IA (ABC + implémentations)
│   ├── state_machine.py     # FSM pour états de jeu
│   ├── stats.py             # Classe Statistics (analyse)
│   └── ui.py                # Interface CLI Rich
├── tests/
│   ├── __init__.py
│   ├── test_card.py
│   ├── test_deck.py
│   ├── test_hand.py
│   ├── test_player.py
│   ├── test_dealer.py
│   ├── test_game.py
│   ├── test_strategies.py
│   ├── test_state_machine.py
│   └── test_integration.py  # Tests end-to-end
├── data/
│   ├── games/               # Sauvegardes parties
│   └── stats/               # Exports statistiques
├── docs/
│   ├── ARCHITECTURE.md      # Documentation architecture
│   ├── STRATEGIES.md        # Explication stratégies
│   └── RULES.md             # Règles Blackjack
├── main.py                  # Point d'entrée
├── requirements.txt
├── requirements-dev.txt
├── pytest.ini
├── .gitignore
├── LICENSE
└── README.md
```

### 🚀 Installation

#### Prérequis
- Python 3.10 ou supérieur
- pip

#### Installation Rapide

```bash
# Cloner le repository
git clone https://github.com/Adam-Blf/Blackjack-Simulator.git
cd Blackjack-Simulator

# Créer environnement virtuel
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Installer dépendances
pip install -r requirements.txt

# Lancer le jeu
python main.py
```

#### Installation Développeur

```bash
# Installer dépendances dev (tests, linting)
pip install -r requirements-dev.txt

# Lancer tests
pytest

# Lancer tests avec coverage
pytest --cov=src --cov-report=html

# Linting
black src/ tests/
flake8 src/ tests/
mypy src/
```

### 🎮 Utilisation

#### Mode Graphique (GUI)

```bash
python main.py --gui
```

Interface Tkinter complète avec :
- 🎨 Thème sombre moderne
- 🃏 Cartes visuelles avec couleurs (♠️♥️♣️♦️)
- 🎮 Contrôles : Hit, Stand, Double Down, Deal
- 💰 Gestion bankroll et paris en temps réel
- 🎯 Sélection stratégie (5 IA disponibles)
- 🤖 Mode auto-play avec simulation
- 📊 Statistiques session en direct
- ⚙️ Configuration decks, mise, stratégie

#### Mode Interactif (CLI)

```bash
python main.py
```

Menu principal :
```
╔════════════════════════════════════╗
║     🃏 BLACKJACK SIMULATOR 🃏     ║
╚════════════════════════════════════╝

1. 🎲 Nouvelle partie
2. 📊 Statistiques
3. 🤖 Simuler N parties (IA)
4. 💾 Charger partie
5. ⚙️  Configuration
6. ❌ Quitter

Votre choix: _
```

#### Mode Simulation (IA)

```bash
# Simuler 1000 parties avec Basic Strategy
python main.py --simulate 1000 --strategy basic

# Comparer stratégies
python main.py --compare-strategies --games 500
```

#### Exemples d'utilisation

```python
from src.game import Game
from src.strategies import BasicStrategy

# Partie simple
game = Game(bankroll=1000, bet=10)
game.start()

# Partie avec stratégie IA
player = Player(bankroll=1000, strategy=BasicStrategy())
game = Game(player=player)
game.auto_play()  # Joue automatiquement selon stratégie

# Analyse statistiques
from src.stats import Statistics
stats = Statistics()
stats.load_from_file("data/stats/history.json")
print(stats.summary())
stats.plot_bankroll_evolution()
```

### 📊 Stratégies Disponibles

#### 1. **Basic Strategy** (Recommandée)
Stratégie mathématiquement optimale basée sur probabilités :
- Hit si score < 12
- Stand si score >= 17
- Double Down sur 10-11 face à dealer 2-9
- Split paires 8-8, A-A
- **Avantage maison** : ~0.5%

#### 2. **Conservative Strategy**
Minimise les risques :
- Stand dès 12+
- Jamais de Double Down ou Split
- Toujours assurance si dealer Ace
- **Avantage maison** : ~2-3%

#### 3. **Aggressive Strategy**
Maximise les gains :
- Hit jusqu'à 18+
- Double Down agressif (9-12)
- Split toutes paires
- **Variance élevée**, avantage maison ~1-2%

#### 4. **Martingale Strategy**
Double la mise après chaque perte :
- Récupère pertes + 1 unité à chaque gain
- **Risque** : bankroll insuffisant après série de pertes
- Nécessite limite de mise table

#### 5. **Card Counting (Hi-Lo)**
Compte les cartes sorties :
- +1 pour 2-6 (favorable joueur)
- 0 pour 7-9 (neutre)
- -1 pour 10-A (favorable dealer)
- Ajuste mises selon True Count
- **Avantage théorique** : jusqu'à +1.5%

### 🧪 Tests

Le projet inclut **50+ tests unitaires** couvrant :

#### Tests Unitaires
```bash
# Tous les tests
pytest

# Tests spécifiques
pytest tests/test_hand.py
pytest tests/test_strategies.py

# Avec coverage
pytest --cov=src --cov-report=term-missing
```

#### Tests d'Intégration
```bash
# Scénarios complets end-to-end
pytest tests/test_integration.py -v
```

#### Exemples de tests

```python
# test_hand.py
def test_blackjack_natural():
    hand = Hand()
    hand.add_card(Card(Rank.ACE, Suit.SPADES))
    hand.add_card(Card(Rank.KING, Suit.HEARTS))
    assert hand.is_blackjack() == True
    assert hand.value == 21

# test_strategies.py
def test_basic_strategy_hit_on_16():
    strategy = BasicStrategy()
    hand = Hand([Card(Rank.TEN, Suit.SPADES), Card(Rank.SIX, Suit.HEARTS)])
    dealer_card = Card(Rank.SEVEN, Suit.DIAMONDS)
    action = strategy.decide(hand, dealer_card)
    assert action == Action.HIT
```

### 📈 Statistiques & Métriques

#### Exemple de sortie

```
╔══════════════════════════════════════╗
║       📊 SESSION STATISTICS          ║
╚══════════════════════════════════════╝

Games Played       : 1,000
Wins               : 432 (43.2%)
Losses             : 498 (49.8%)
Pushes             : 70 (7.0%)

Blackjacks         : 48 (4.8%)
Busts              : 156 (15.6%)
Dealer Busts       : 201 (20.1%)

Initial Bankroll   : $1,000
Final Bankroll     : $956
Total Wagered      : $10,000
Net Profit/Loss    : -$44
ROI                : -0.44%
House Edge         : 0.88%

Longest Win Streak : 8
Longest Loss Streak: 12
Avg Bet Size       : $10.00
Max Bet Size       : $80.00 (Martingale)
```

### 🎯 Cas d'Usage

1. **Apprentissage Blackjack** : Comprendre les règles et stratégies
2. **Test Stratégies** : Comparer efficacité différentes approches
3. **Simulation Monte Carlo** : Analyser variance et espérance
4. **Éducation Probabilités** : Visualiser avantage maison
5. **Développement IA** : Base pour algorithmes ML (RL, DQN)

### 🗺️ Roadmap

#### ✅ Version 1.0 (Actuelle)
- [x] Règles Blackjack complètes
- [x] 5 stratégies IA
- [x] CLI Rich interactive
- [x] **GUI Tkinter moderne** 🆕
- [x] Tests unitaires >95%
- [x] Statistiques détaillées

#### 🔄 Version 1.1 (Q1 2025)
- [ ] Mode multijoueur local
- [ ] Variantes règles (European, Vegas Strip)
- [ ] Tutoriel interactif
- [ ] Amélioration GUI (animations, sons)

#### 🚀 Version 2.0 (Q2 2025)
- [ ] IA Deep Reinforcement Learning (DQN)
- [ ] Mode online multijoueur
- [ ] Leaderboard global
- [ ] Application mobile (Kivy)
- [ ] API REST pour intégrations

### 📄 Licence

Ce projet est sous licence MIT. Voir [LICENSE](LICENSE) pour détails.

### 👤 Auteur

**Adam Beloucif**
- GitHub : [@Adam-Blf](https://github.com/Adam-Blf)
- Email : Via GitHub Issues

### 🤝 Contribuer

Les contributions sont bienvenues ! Pour contribuer :

1. Fork le projet
2. Créez une branche feature (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

Voir [CONTRIBUTING.md](CONTRIBUTING.md) pour guidelines détaillées.

---

## 🇬🇧 English

### 📝 Description

Professional Blackjack simulator in Python featuring:
- Robust object-oriented architecture (10+ classes)
- State machine for game flow
- Configurable play strategies (Basic Strategy, Martingale, etc.)
- Colorful CLI with Rich
- Detailed statistics and game history
- Comprehensive unit tests (pytest, >95% coverage)
- Save/load game functionality

### ⚡ Key Features

- ✅ Official Blackjack rules (Hit, Stand, Double Down, Split, Insurance)
- ✅ Automatic dealer with standard strategy
- ✅ Multi-hand management (after split)
- ✅ Natural Blackjack (3:2 payout)
- ✅ 5 AI strategies (Basic, Conservative, Aggressive, Martingale, Card Counting)
- ✅ Rich CLI interface with animations
- ✅ Statistics & analysis (winrate, ROI, graphs)
- ✅ 50+ unit tests with >95% coverage

### 🚀 Quick Start

```bash
git clone https://github.com/Adam-Blf/Blackjack-Simulator.git
cd Blackjack-Simulator
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
python main.py
```

### 🧪 Testing

```bash
pytest --cov=src --cov-report=html
```

### 📊 Strategies

1. **Basic Strategy** - Mathematically optimal (~0.5% house edge)
2. **Conservative** - Minimize risks (~2-3% house edge)
3. **Aggressive** - Maximize potential gains (high variance)
4. **Martingale** - Double bet after loss (risky)
5. **Card Counting** - Hi-Lo strategy (up to +1.5% player edge)

### 📄 License

MIT License - see [LICENSE](LICENSE)

---

<div align="center">

**🃏 Made with ♠️♥️♣️♦️ and Python**

⭐ **Star this project if you find it useful!** ⭐

</div>

---

*Last updated: November 19, 2025*