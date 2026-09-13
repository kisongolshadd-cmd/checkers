
import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils import auth


@pytest.fixture(autouse=True)
def temp_users_file(tmp_path, monkeypatch):
    fake_file = tmp_path / "users.json"
    monkeypatch.setattr(auth, "USERS_FILE", str(fake_file))
    yield fake_file


def test_load_users_returns_empty_dict_when_no_file():
    assert auth.load_users() == {}


def test_hash_password_is_consistent():
    assert auth.hash_password("mypassword") == auth.hash_password("mypassword")


def test_hash_password_differs_for_different_input():
    assert auth.hash_password("abc123") != auth.hash_password("xyz789")


def test_register_new_user_succeeds():
    success, message = auth.register_user("shadrack", "pass123")
    assert success is True

    users = auth.load_users()
    assert "shadrack" in users
    assert users["shadrack"]["password"] != "pass123"


def test_register_duplicate_username_fails():
    auth.register_user("shadrack", "pass123")
    success, message = auth.register_user("shadrack", "differentpass")
    assert success is False
    assert "taken" in message.lower()


def test_register_short_password_fails():
    success, message = auth.register_user("newplayer", "abc")
    assert success is False


def test_register_empty_username_fails():
    success, message = auth.register_user("", "pass123")
    assert success is False


def test_new_account_starts_with_zero_stats():
    auth.register_user("shadrack", "pass123")
    users = auth.load_users()
    assert users["shadrack"]["wins"] == 0
    assert users["shadrack"]["losses"] == 0
    assert users["shadrack"]["games_played"] == 0


def test_login_with_correct_credentials():
    auth.register_user("shadrack", "pass123")
    success, message = auth.login_user("shadrack", "pass123")
    assert success is True


def test_login_with_wrong_password():
    auth.register_user("shadrack", "pass123")
    success, message = auth.login_user("shadrack", "wrongpass")
    assert success is False


def test_login_with_unknown_username():
    success, message = auth.login_user("ghost", "whatever")
    assert success is False


def test_user_exists_true_and_false_cases():
    auth.register_user("shadrack", "pass123")
    assert auth.user_exists("shadrack") is True
    assert auth.user_exists("nobody") is False
