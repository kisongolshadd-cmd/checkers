
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models import game
from models import board
from utils import auth


def print_main_menu():
    """Display the main game menu options."""
    print("\n" + "=" * 40)
    print("   MAIN MENU")
    print("=" * 40)
    print("1. Play vs Player")
    print("2. Play vs Computer")
    print("3. View My Stats")
    print("4. View Leaderboard")
    print("5. Logout")
    print("=" * 40)


def start_pvp_game(player1_username):
    
    print("\n--- Player vs Player Mode ---")
    player2_username = input("Opponent's username: ").strip()
    
    # Verify opponent exists
    if not auth.user_exists(player2_username):
        print("Opponent not found. Returning to menu...")
        return
    
    if player2_username == player1_username:
        print("You cannot play against yourself!")
        return
    
    # Create and start game
    new_game = game.Game(player1_username, player2_username, "pvp")
    print(f"\nStarting game: {player1_username} vs {player2_username}")
    new_game.start_game()
    
    # Play the game 
    print("Game in progress...")
    
    # Save game record
    game.GameManager.save_game(new_game)
    print("Game saved!")


def start_pvc_game(player_username):
    
    print("\n--- Player vs Computer Mode ---")