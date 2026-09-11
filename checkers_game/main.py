"""
Entry point for the checkers game.
Shows the login/register screen, then hands off to the game menu
once someone is signed in.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils import auth
from cli import menu


def print_welcome():
    print("=" * 40)
    print("   WELCOME TO PYTHON CHECKERS")
    print("=" * 40)


def login_or_register():
    """
    Keeps asking until the player logs in, registers, or quits.
    Returns the username on success, or None if they quit.
    """
    while True:
        print("\n1. Login")
        print("2. Register")
        print("3. Quit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            success, message = auth.login_user(username, password)
            print(message)
            if success:
                return username

        elif choice == "2":
            username = input("Choose a username: ").strip()
            password = input("Choose a password: ").strip()
            success, message = auth.register_user(username, password)
            print(message)
            if success:
                return username

        elif choice == "3":
            return None

        else:
            print("Invalid option, try again.")


def main():
    print_welcome()
    username = login_or_register()

    if username is None:
        print("Goodbye!")
        return

    print(f"\nWelcome, {username}!")
    menu.main_menu(username)


if __name__ == "__main__":
    main()
