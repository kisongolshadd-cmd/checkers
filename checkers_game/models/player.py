
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import auth


VALID_COLORS = ("red", "black")


class Player:

    def __init__(self, username, color, is_ai=False):
        if color not in VALID_COLORS:
            raise ValueError(f"color must be one of {VALID_COLORS}, got {color!r}")

        self.username = username
        self.color = color
        self.is_ai = is_ai
        self.captured_count = 0

    def record_capture(self):
        self.captured_count += 1

    def get_stats(self):
        
        if self.is_ai:
            return {"games_played": 0, "wins": 0, "losses": 0}

        users = auth.load_users()
        user = users.get(self.username)
        if user is None:
            return {"games_played": 0, "wins": 0, "losses": 0}

        return {
            "games_played": user.get("games_played", 0),
            "wins": user.get("wins", 0),
            "losses": user.get("losses", 0),
        }

    def __str__(self):
        label = "AI" if self.is_ai else "Player"
        return f"{label} {self.username} ({self.color})"

    def __repr__(self):
        return f"Player(username={self.username!r}, color={self.color!r}, is_ai={self.is_ai})"


def create_players(player1_username=None, player2_username=None, mode="pvp"):

    player1_username = player1_username or "Player A"
    player1 = Player(player1_username, "red", is_ai=False)

    if mode == "pvc":
        player2 = Player("Computer", "black", is_ai=True)
    else:
        player2_username = player2_username or "Player B"
        player2 = Player(player2_username, "black", is_ai=False)

    return player1, player2


def update_stats_after_game(winner_username, loser_username, is_draw=False):

    users = auth.load_users()
    updated = False

    for username in (winner_username, loser_username):
        if username and username in users:
            users[username]["games_played"] = users[username].get("games_played", 0) + 1
            updated = True

    if not is_draw:
        if winner_username in users:
            users[winner_username]["wins"] = users[winner_username].get("wins", 0) + 1
        if loser_username in users:
            users[loser_username]["losses"] = users[loser_username].get("losses", 0) + 1

    if updated:
        auth.save_users(users)

    return updated