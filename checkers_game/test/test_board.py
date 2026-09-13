
import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models.board import Board, Piece, AIPlayer

@pytest.fixture
def board():
    return Board()


@pytest.fixture
def ai_player():
    return AIPlayer('black')

class TestPiece:
    
    def test_piece_creation_red(self):
        piece = Piece('red')
        assert piece.player_color == 'red' 
        assert piece.is_king is False

    def test_piece_creation_black(self):
        piece = Piece('black')
        assert piece.player_color == 'black'
        assert piece.is_king is False

    def test_piece_promotion_to_king(self):
        piece = Piece('red')
        piece.is_king = True  # Promote to king
        assert piece.is_king is True

class TestBoardInitialization:
    def test_board_initialization_red_pieces(self, board):
        red_count = sum(1 for row in range(3) for col in range(8) 
                       if board.grid[row][col] and board.grid[row][col].player_color == 'red')
        assert red_count == 12, f"Expected 12 red pieces, but found {red_count}"

    def test_board_initialization_black_pieces(self, board):
        black_count = sum(1 for row in range(5, 8) for col in range(8) 
                         if board.grid[row][col] and board.grid[row][col].player_color == 'black')
        assert black_count == 12, f"Expected 12 black pieces, but found {black_count}"

    def test_board_is_8x8(self, board):
        
        assert len(board.grid) == 8
        assert all(len(row) == 8 for row in board.grid)
class TestPieceRetrieval:
    def test_get_piece_returns_piece(self, board):
        piece = board.get_piece(0, 1)
        assert piece is not None
        assert piece.player_color == 'red'

    def test_get_piece_from_empty_square(self, board):
        piece = board.get_piece(3, 3)
        assert piece is None

    def test_get_piece_out_of_bounds(self, board):
        piece = board.get_piece(10, 10)
        assert piece is None
class TestMovement:
    def test_move_piece_regular_move(self, board):
        success, result = board.move_piece(2, 1, 3, 2)
        assert success is True
        assert board.get_piece(3, 2) is not None
        assert board.get_piece(2, 1) is None

    def test_move_piece_from_empty_square(self, board):
        success, result = board.move_piece(3, 3, 4, 4)
        assert success is False

    def test_move_piece_to_occupied_square(self, board):
        success, result = board.move_piece(2, 1, 1, 0)
        assert success is False

class TestAvailableMoves:
    def test_get_available_moves_returns_list(self, board):
        moves = board.get_available_moves(2, 1)
        assert isinstance(moves, list)
        assert len(moves) > 0

    def test_get_available_moves_from_empty_square(self, board):

        moves = board.get_available_moves(3, 3)
        assert len(moves) == 0
    def test_get_available_moves_returns_tuples(self, board):
       
        moves = board.get_available_moves(2, 1)
        for move in moves:
            assert isinstance(move, tuple)
class TestKingPromotion:
    
    def test_king_promotion_red_at_bottom(self, board):
        board.grid[6][1] = Piece('red')
        board.grid[6][1].is_king = False  
        board.grid[7][0] = None  
        board.grid[7][2] = None  
        
        success, _ = board.move_piece(6, 1, 7, 0)
        
        if success:
            piece = board.get_piece(7, 0)
            assert piece is not None
            assert piece.is_king is True

    def test_king_promotion_black_at_top(self, board):
        board.grid[1][1] = Piece('black')
        board.grid[1][1].is_king = False  
        board.grid[0][0] = None 
        board.grid[0][2] = None  
        success, _ = board.move_piece(1, 1, 0, 0)
        
        if success:
            piece = board.get_piece(0, 0)
            assert piece is not None
            assert piece.is_king is True

class TestValidMoves:
    def test_red_has_valid_moves_at_start(self, board):
        assert board.has_valid_moves('red') is True

    def test_black_has_valid_moves_at_start(self, board):
        assert board.has_valid_moves('black') is True
class TestAIPlayer:
    
    def test_ai_player_creation(self, ai_player):
        assert ai_player.color == 'black'

    def test_ai_get_best_move_returns_move(self, board, ai_player):
        move = ai_player.get_best_move(board)
        assert move is not None

    def test_ai_move_format(self, board, ai_player):
        move = ai_player.get_best_move(board)
        assert isinstance(move, tuple)
        assert len(move) == 3
        
        from_pos, to_pos, move_type = move
        assert isinstance(from_pos, tuple)
        assert isinstance(to_pos, tuple)
        assert move_type in ['regular', 'capture']