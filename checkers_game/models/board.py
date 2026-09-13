import random

class Piece:
    """Represents a checkers piece"""

    def __init__(self, player_color):
        self.player_color = player_color  # 'red' or 'black'
        self.is_king = False

    def __str__(self):
        if self.player_color == "red":
            return "R" if self.is_king else "r"
        else:
            return "B" if self.is_king else "b"

    def __repr__(self):
        return f"Piece({self.player_color}, king={self.is_king})"
class Board:
    """checkers board and game state"""
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.setup_pieces()
        self.captured_pieces = {"red": 0, "black": 0}

    def setup_pieces(self):
        for row in range(3):
            for col in range(8):
                if (row + col) % 2 == 1:
                    self.grid[row][col] = Piece("red")
        for row in range(5, 8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    self.grid[row][col] = Piece("black")

    def display(self):
        print("\n    0  1  2  3  4  5  6  7")
        print("  +-----------------------+")
        for row in range(8):
            row_str = f"{row} |"
            for col in range(8):
                piece = self.grid[row][col]
                if piece:
                    row_str += f" {piece} "
                else:
                    row_str += " . "
            row_str += "|"
            print(row_str)
        print("  +-----------------------+")
        print("  guide: r = Red | b = Black | R = Red King | B = Black King\n")

    def get_piece(self, row, col):
        if 0 <= row < 8 and 0 <= col < 8:
            return self.grid[row][col]
        return None

    def move_piece(self, from_row, from_col, to_row, to_col):
        piece = self.grid[from_row][from_col]
        if not piece:
            return False, "No piece at that position"

        captured = None

        # Regular move
        if abs(from_row - to_row) == 1 and abs(from_col - to_col) == 1:
            if self.grid[to_row][to_col] is not None:
                return False, "position occupied"
            self.grid[to_row][to_col] = piece
            self.grid[from_row][from_col] = None

        # Capture move
        elif abs(from_row - to_row) == 2 and abs(from_col - to_col) == 2:
            mid_row = (from_row + to_row) // 2
            mid_col = (from_col + to_col) // 2
            target = self.grid[mid_row][mid_col]

            if target is None or target.player_color == piece.player_color:
                return False, "Invalid capture"

            if self.grid[to_row][to_col] is not None:
                return False, "position occupied"

            self.grid[to_row][to_col] = piece
            self.grid[from_row][from_col] = None
            self.grid[mid_row][mid_col] = None
            captured = target
            self.captured_pieces[target.player_color] += 1
        else:
            return False, "Invalid move"

        # Check king promotion
        if piece.player_color == "red" and to_row == 7:
            piece.is_king = True
        elif piece.player_color == "black" and to_row == 0:
            piece.is_king = True

        return True, captured

    def is_valid_move(self, from_row, from_col, to_row, to_col, player_color):
        piece = self.get_piece(from_row, from_col)
        if not piece or piece.player_color != player_color:
            return False
        # Check boundaries
        if not (0 <= to_row < 8 and 0 <= to_col < 8):
            return False
        # Check destination
        if self.get_piece(to_row, to_col) is not None:
            return False

        return True

    def get_available_moves(self, row, col):
        piece = self.get_piece(row, col)
        if not piece:
            return []

        moves = []
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        for dr, dc in directions:
            # Regular move
            new_row, new_col = row + dr, col + dc
            if self.is_valid_move(row, col, new_row, new_col, piece.player_color):
                moves.append(("regular", new_row, new_col))

            # Capture move
            new_row, new_col = row + 2 * dr, col + 2 * dc
            mid_row, mid_col = row + dr, col + dc
            mid_piece = self.get_piece(mid_row, mid_col)

            if (
                0 <= new_row < 8
                and 0 <= new_col < 8
                and mid_piece
                and mid_piece.player_color != piece.player_color
                and self.get_piece(new_row, new_col) is None
            ):
                moves.append(("capture", new_row, new_col))

        return moves

    def has_valid_moves(self, player_color):
        for row in range(8):
            for col in range(8):
                piece = self.get_piece(row, col)
                if piece and piece.player_color == player_color:
                    if self.get_available_moves(row, col):
                        return True
        return False

    def reset(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.setup_pieces()
        self.captured_pieces = {"red": 0, "black": 0}

    def play_game(self, game_instance):
        current_turn = "red"

        # Safely resolve players from game_instance.players (list or dict)
        if hasattr(game_instance, "players") and isinstance(game_instance.players, list):
            p1, p2 = game_instance.players[0], game_instance.players[1]
        elif hasattr(game_instance, "players") and isinstance(game_instance.players, dict):
            p1, p2 = list(game_instance.players.values())[:2]
        else:
            p1 = getattr(game_instance, "player1", None)
            p2 = getattr(game_instance, "player2", None)

        ai = None
        if p2 and getattr(p2, "username", "") == "Computer":
            ai = AIPlayer(getattr(p2, "color", "black"))

        while True:
            self.display()

            if not self.has_valid_moves(current_turn):
                winner = p2 if current_turn == getattr(p1, "color", "red") else p1
                print(f"\nGame Over! {getattr(winner, 'username', 'Opponent')} wins!")
                break

            current_player = p1 if current_turn == getattr(p1, "color", "red") else p2
            player_name = getattr(current_player, "username", "Player")
            print(f"Current Turn: {player_name} ({current_turn.upper()})")

            # AI Turn
            if ai and current_turn == ai.color:
                print("Computer is thinking...")
                move = ai.get_best_move(self)
                if not move:
                    print("Computer has no valid moves!")
                    break
                (from_r, from_c), (to_r, to_c), _ = move
                success, msg = self.move_piece(from_r, from_c, to_r, to_c)
                print(f"Computer moved from ({from_r}, {from_c}) to ({to_r}, {to_c})")

            # Human Turn
            else:
                user_input = input(
                    "Enter move (from_row from_col to_row to_col) or 'q' to quit: "
                ).strip()
                if user_input.lower() == "q":
                    print("Game quit.")
                    break

                try:
                    from_r, from_c, to_r, to_c = map(int, user_input.split())
                except ValueError:
                    print(
                        "Invalid input format. Enter 4 numbers separated by spaces (e.g., '2 1 3 2')."
                    )
                    continue

                piece = self.get_piece(from_r, from_c)
                if not piece or piece.player_color != current_turn:
                    print("You must select one of your own pieces!")
                    continue

                success, result = self.move_piece(from_r, from_c, to_r, to_c)
                if not success:
                    print(f"Invalid move: {result}")
                    continue

            # Switch turns
            current_turn = "black" if current_turn == "red" else "red"


class AIPlayer:

    def __init__(self, color):
        self.color = color

    def get_best_move(self, board):
        possible_moves = []

        # Find all possible moves
        for row in range(8):
            for col in range(8):
                piece = board.get_piece(row, col)
                if piece and piece.player_color == self.color:
                    moves = board.get_available_moves(row, col)
                    for move_type, new_row, new_col in moves:
                        possible_moves.append(
                            ((row, col), (new_row, new_col), move_type)
                        )

        if not possible_moves:
            return None

        # Prioritize capture moves
        capture_moves = [m for m in possible_moves if m[2] == "capture"]
        if capture_moves:
            return random.choice(capture_moves)

        return random.choice(possible_moves)