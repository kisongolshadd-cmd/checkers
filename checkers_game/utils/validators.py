

from models.player import VALID_COLORS


VALID_MODES = ("pvp", "pvc")
BOARD_SIZE = 8
MIN_PASSWORD_LENGTH = 4



def validate_username(username):
    
    if username is None:
        return False, "Username cannot be empty"

    if not username.strip():
        return False, "Username cannot be empty"

    return True, ""


def validate_password(password):
    
    if not password:
        return False, "Password cannot be empty"

    if len(password) < MIN_PASSWORD_LENGTH:
        return False, f"Password must be at least {MIN_PASSWORD_LENGTH} characters long"

    return True, ""




def validate_color(color):
    
    if color not in VALID_COLORS:
        return False, f"color must be one of {VALID_COLORS}, got {color!r}"

    return True, ""


def validate_game_mode(mode):
    
    if mode not in VALID_MODES:
        return False, f"mode must be one of {VALID_MODES}, got {mode!r}"

    return True, ""




def validate_coordinates(row, col):
    
    if not (0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE):
        return False, f"Position ({row}, {col}) is out of bounds"

    return True, ""


def validate_move_shape(from_row, from_col, to_row, to_col):
    
    ok, message = validate_coordinates(from_row, from_col)
    if not ok:
        return False, message

    ok, message = validate_coordinates(to_row, to_col)
    if not ok:
        return False, message

    row_diff = abs(from_row - to_row)
    col_diff = abs(from_col - to_col)

    if (row_diff, col_diff) not in ((1, 1), (2, 2)):
        return False, "Move must be a single diagonal step or a two-square capture jump"

    return True, ""