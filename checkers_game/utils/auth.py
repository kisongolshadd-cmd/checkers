

import json
import os
import hashlib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USERS_FILE = os.path.join(BASE_DIR, "data", "users.json")


def load_users():
    if not os.path.exists(USERS_FILE):
        return {}

    with open(USERS_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}


def save_users(users):
    os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def user_exists(username):
    users = load_users()
    return username in users


def register_user(username, password):
    
    username = username.strip()

    if not username or not password:
        return False, "Username and password cannot be empty"

    if len(password) < 4:
        return False, "Password must be at least 4 characters long"

    users = load_users()
    if username in users:
        return False, "That username is already taken"

    users[username] = {
        "password": hash_password(password),
        "games_played": 0,
        "wins": 0,
        "losses": 0,
    }
    save_users(users)
    return True, "Account created successfully"


def login_user(username, password):
    
    users = load_users()

    if username not in users:
        return False, "No account found with that username"

    if users[username]["password"] != hash_password(password):
        return False, "Incorrect password"

    return True, "Login successful"
