from models.board import Board
from models.player import Player


class InvalidMoveError(Exception):
    pass


class Game:
    def __init__(self, player_one: Player, player_two: Player):
        self.board = Board()
        self.players = {
            player_one.color: player_one,
            player_two.color: player_two,
        }
        self.current_turn = player_one.color
        self.winner = None
        self.move_history = []
        self.is_over = False

    def start_game(self):
        self.winner = None
        self.is_over = False
        self.move_history = []
        return self.get_state()

    def get_state(self):
        return {
            "board": self.board,
            "current_turn": self.current_turn,
            "winner": self.winner,
            "is_over": self.is_over,
            "move_count": len(self.move_history),
        }

    def make_move(self, player_color: str, pos_from: tuple, pos_to: tuple) -> dict:
        if self.is_over:
            raise InvalidMoveError("Game is already over.")

        if player_color != self.current_turn:
            raise InvalidMoveError(f"It is not {player_color}'s turn.")

        if not self.board.is_valid_move(pos_from, pos_to, player_color):
            raise InvalidMoveError(f"Illegal move: {pos_from} -> {pos_to}")

        captured = self.board.move_piece(pos_from, pos_to)
        self.board.promote_if_needed(pos_to)

        self.move_history.append({
            "player": player_color,
            "from": pos_from,
            "to": pos_to,
            "captured": captured,
        })

        winner = self.check_winner()
        if winner:
            self.winner = winner
            self.is_over = True
        else:
            self._switch_turn()

        return {"success": True, "captured": captured, "winner": self.winner}

    def _switch_turn(self):
        colors = list(self.players.keys())
        self.current_turn = colors[1] if self.current_turn == colors[0] else colors[0]

    def check_winner(self) -> str | None:
        colors = list(self.players.keys())
        for color in colors:
            opponent = colors[1] if color == colors[0] else colors[0]
            if self.board.count_pieces(opponent) == 0:
                return color
            if not self.board.has_legal_moves(opponent):
                return color
        return None

    def get_winner_name(self) -> str | None:
        if self.winner is None:
            return None
        return self.players[self.winner].username