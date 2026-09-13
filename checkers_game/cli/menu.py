
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models import game
from models import board
from models.player import Player
from utils import auth


def print_main_menu():
    print("\n" + "*" * 20)
    print("   MAIN MENU")
    print("*" * 20)
    print("1. Play vs Player")
    print("2. Play vs Computer")
    print("3. View My Stats")
    print("4. View Leaderboard")
    print("5. Logout")
    print("*" * 40)


def start_pvp_game(player1_username):
    
    print("\n--- Player vs Player Mode ---")
    player2_username = input("Opponent's username: ").strip()

    if not auth.user_exists(player2_username):
        print("Opponent not found. Returning to menu...")
        return

    if player2_username == player1_username:
        print("You cannot play against yourself!")
        return

    player1 = Player(player1_username, "red")
    player2 = Player(player2_username, "black")

    new_game = game.Game(player1, player2)
    print(f"\nStarting game: {player1_username} vs {player2_username}")

    game_board = board.Board()
    game_board.play_game(new_game)


def start_pvc_game(player_username):
    
    print("\n--- Player vs Computer Mode ---")

    # Ask player which color they want
    print("Choose your color:")
    print("1. Red (goes first)")
    print("2. Black (goes second)")
    color_choice = input("Choose: ").strip()

    if color_choice == "1":
        player_color = "red"
        ai_color = "black"
    elif color_choice == "2":
        player_color = "black"
        ai_color = "red"
    else:
        print("Invalid choice. Defaulting to Red.")
        player_color = "red"
        ai_color = "black"

    player = Player(player_username, player_color)
    ai = Player("Computer", ai_color)

    new_game = game.Game(player, ai)
    print(
        f"\nStarting game: {player_username} ({player_color}) vs Computer ({ai_color})"
    )

    game_board = board.Board()
    game_board.play_game(new_game)


def view_player_stats(username):

    stats = auth.get_user_stats(username)

    if stats is None:
        print("Could not load stats.")
        return

    print("\n" + "=" * 40)
    print(f"   STATS FOR {username.upper()}")
    print("=" * 40)
    print(f"Wins:        {stats['wins']}")
    print(f"Losses:      {stats['losses']}")
    print(f"Draws:       {stats['draws']}")
    total = stats["wins"] + stats["losses"] + stats["draws"]
    print(f"Total Games: {total}")

    if total > 0:
        win_rate = (stats["wins"] / total) * 100
        print(f"Win Rate:    {win_rate:.1f}%")
    else:
        print(f"Win Rate:    N/A (no games yet)")

    print("=" * 40)


def view_leaderboard():

    users = auth.load_users()

    if not users:
        print("No users found.")
        return

    sorted_users = sorted(
        users.items(), key=lambda x: x[1]["wins"], reverse=True
    )[:10]

    print("\n" + "=" * 50)
    print("   TOP 10 LEADERBOARD")
    print("=" * 50)
    print(f"{'Rank':<6} {'Username':<20} {'Wins':<8} {'Losses':<8}")
    print("-" * 50)

    for rank, (username, stats) in enumerate(sorted_users, 1):
        print(
            f"{rank:<6} {username:<20} {stats['wins']:<8} {stats['losses']:<8}"
        )

    print("=" * 50)


def main_menu(username):

    while True:
        print_main_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            start_pvp_game(username)

        elif choice == "2":
            start_pvc_game(username)

        elif choice == "3":
            view_player_stats(username)

        elif choice == "4":
            view_leaderboard()

        elif choice == "5":
            print(f"Goodbye, {username}!")
            return

        else:
            print("Invalid option, try again.")


if __name__ == "__main__":
    main_menu("test_player")