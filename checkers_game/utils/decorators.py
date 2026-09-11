import json
import functools
from datetime import datetime

from utils.auth import get_current_user
from models.game import InvalidMoveError

HISTORY_FILE = "data/game_history.json"


def login_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        user = get_current_user()
        if user is None:
            print("You must be logged in to do that.")
            return None
        return func(*args, **kwargs)
    return wrapper


def validate_turn(func):
    @functools.wraps(func)
    def wrapper(game_instance, player_color, *args, **kwargs):
        if player_color != game_instance.current_turn:
            print(f"It's not {player_color}'s turn.")
            return None
        return func(game_instance, player_color, *args, **kwargs)
    return wrapper


def log_action(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        entry = {
            "timestamp": datetime.now().isoformat(),
            "action": func.__name__,
            "result": str(result),
        }
        try:
            try:
                with open(HISTORY_FILE, "r") as f:
                    history = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                history = []
            history.append(entry)
            with open(HISTORY_FILE, "w") as f:
                json.dump(history, f, indent=2)
        except OSError as e:
            print(f"Warning: could not write to game history ({e}).")
        return result
    return wrapper


def handle_errors(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except InvalidMoveError as e:
            print(f"Invalid move: {e}")
            return None
        except Exception as e:
            print(f"Something went wrong: {e}")
            return None
    return wrapper