
import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models import player
from utils import auth


@pytest.fixture(autouse=True)
def temp_users_file(tmp_path, monkeypatch):
    fake_file = tmp_path / "users.json"
    monkeypatch.setattr(auth, "USERS_FILE", str(fake_file))
    yield fake_file


@pytest.fixture
def registered_players():
    auth.register_user("shadrack", "pass123")
    auth.register_user("devine", "pass123")



def test_create_human_player():
    
    p = player.Player("shadrack", "red")
    assert p.username == "shadrack"
    assert p.color == "red"
    assert p.is_ai is False


def test_create_ai_player():
    
    p = player.Player("Computer", "black", is_ai=True)
    assert p.username == "Computer"
    assert p.color == "black"
    assert p.is_ai is True


def test_player_starts_with_zero_captures():
    
    p = player.Player("shadrack", "red")
    assert p.captured_count == 0


def test_invalid_color_raises_value_error():

    with pytest.raises(ValueError):
        player.Player("shadrack", "green")




def test_record_capture_increments_count():

    p = player.Player("shadrack", "red")
    p.record_capture()
    assert p.captured_count == 1


def test_record_capture_multiple_times():
    
    p = player.Player("shadrack", "red")
    p.record_capture()
    p.record_capture()
    p.record_capture()
    assert p.captured_count == 3


# STATS TESTS

def test_get_stats_for_ai_player_is_zeroed():

    p = player.Player("Computer", "black", is_ai=True)
    stats = p.get_stats()
    assert stats == {"games_played": 0, "wins": 0, "losses": 0}


def test_get_stats_for_unknown_user_is_zeroed():
    
    p = player.Player("ghost", "red")
    stats = p.get_stats()
    assert stats == {"games_played": 0, "wins": 0, "losses": 0}


def test_get_stats_for_registered_user(registered_players):
    
    p = player.Player("shadrack", "red")
    stats = p.get_stats()
    assert stats == {"games_played": 0, "wins": 0, "losses": 0}


# CREATE_PLAYERS TESTS

def test_create_players_pvp_with_usernames():
    
    p1, p2 = player.create_players("shadrack", "devine", mode="pvp")
    assert p1.username == "shadrack"
    assert p1.color == "red"
    assert p1.is_ai is False
    assert p2.username == "devine"
    assert p2.color == "black"
    assert p2.is_ai is False


def test_create_players_pvp_defaults_to_player_a_and_b():
    
    p1, p2 = player.create_players(mode="pvp")
    assert p1.username == "Player A"
    assert p2.username == "Player B"


def test_create_players_pvc_creates_computer_opponent():
    
    p1, p2 = player.create_players("shadrack", mode="pvc")
    assert p1.username == "shadrack"
    assert p1.is_ai is False
    assert p2.username == "Computer"
    assert p2.is_ai is True


def test_create_players_pvc_defaults_player1_to_player_a():
    
    p1, p2 = player.create_players(mode="pvc")
    assert p1.username == "Player A"
    assert p2.username == "Computer"


def test_create_players_assigns_red_and_black():
    
    p1, p2 = player.create_players("shadrack", "devine")
    assert {p1.color, p2.color} == {"red", "black"}



def test_update_stats_after_game_increments_games_played(registered_players):
    
    player.update_stats_after_game("shadrack", "devine")
    users = auth.load_users()
    assert users["shadrack"]["games_played"] == 1
    assert users["devine"]["games_played"] == 1


def test_update_stats_after_game_records_win_and_loss(registered_players):
    
    player.update_stats_after_game("shadrack", "devine")
    users = auth.load_users()
    assert users["shadrack"]["wins"] == 1
    assert users["shadrack"]["losses"] == 0
    assert users["devine"]["losses"] == 1
    assert users["devine"]["wins"] == 0


def test_update_stats_after_draw_does_not_record_win_or_loss(registered_players):
    
    player.update_stats_after_game("shadrack", "devine", is_draw=True)
    users = auth.load_users()
    assert users["shadrack"]["games_played"] == 1
    assert users["devine"]["games_played"] == 1
    assert users["shadrack"]["wins"] == 0
    assert users["devine"]["losses"] == 0


def test_update_stats_skips_unregistered_computer_opponent(registered_players):
    
    result = player.update_stats_after_game("shadrack", "Computer")
    users = auth.load_users()
    assert result is True
    assert users["shadrack"]["wins"] == 1
    assert "Computer" not in users


def test_update_stats_returns_false_when_no_known_users():
    
    result = player.update_stats_after_game("ghost1", "ghost2")
    assert result is False


def test_update_stats_accumulates_across_multiple_games(registered_players):
    
    player.update_stats_after_game("shadrack", "devine")
    player.update_stats_after_game("shadrack", "devine")
    player.update_stats_after_game("devine", "shadrack")

    users = auth.load_users()
    assert users["shadrack"]["games_played"] == 3
    assert users["shadrack"]["wins"] == 2
    assert users["shadrack"]["losses"] == 1
    assert users["devine"]["games_played"] == 3
    assert users["devine"]["wins"] == 1
    assert users["devine"]["losses"] == 2


# STRING REPRESENTATION TESTS

def test_str_for_human_player():
    
    p = player.Player("shadrack", "red")
    assert str(p) == "Player shadrack (red)"


def test_str_for_ai_player():

    p = player.Player("Computer", "black", is_ai=True)
    assert str(p) == "AI Computer (black)"


def test_repr_includes_key_fields():
    
    p = player.Player("shadrack", "red")
    r = repr(p)
    assert "shadrack" in r
    assert "red" in r
    assert "False" in r