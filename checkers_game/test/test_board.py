
import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models.board import Board, Piece, AIPlayer


@pytest.fixture
def board():
    """Create a fresh board for each test"""
    return Board()


@pytest.fixture
def ai_player():
    """Create an AI player for each test"""
    return AIPlayer('black')

# PIECE TESTS
def test_piece_creation_red():
    """Test creating a red piece"""
    piece = Piece('red')
    assert piece.player_color == 'red'
    assert piece.is_king is False


def test_piece_creation_black():
    """Test creating a black piece"""
    piece = Piece('black')
    assert piece.player_color == 'black'
    assert piece.is_king is False


def test_piece_promotion_to_king():
    """Test promoting a piece to king"""
    piece = Piece('red')
    piece.is_king = True
    assert piece.is_king is True

# BOARD INITIALIZATION TESTS
def test_board_initialization_red_pieces(board):
    """Test that board initializes with 12 red pieces"""
    red_count = sum(1 for row in range(3) for col in range(8) 
                   if board.grid[row][col] and board.grid[row][col].player_color == 'red')
    assert red_count == 12


def test_board_initialization_black_pieces(board):
    """Test that board initializes with 12 black pieces"""
    black_count = sum(1 for row in range(5, 8) for col in range(8) 
                     if board.grid[row][col] and board.grid[row][col].player_color == 'black')
    assert black_count == 12


def test_board_is_8x8(board):
    """Test that board is 8x8 grid"""
    assert len(board.grid) == 8
    assert all(len(row) == 8 for row in board.grid)

# PIECE RETRIEVAL TESTS

def test_get_piece_returns_piece(board):
    """Test retrieving an existing piece"""
    piece = board.get_piece(0, 1)
    assert piece is not None
    assert piece.player_color == 'red'


def test_get_piece_from_empty_square(board):
    """Test retrieving from empty square"""
    piece = board.get_piece(3, 3)
    assert piece is None


def test_get_piece_out_of_bounds(board):
    """Test retrieving from out of bounds"""
    piece = board.get_piece(10, 10)
    assert piece is None

# MOVE TESTS

def test_move_piece_regular_move(board):
    """Test making a regular diagonal move"""
    success, result = board.move_piece(2, 1, 3, 2)
    assert success is True
    assert board.get_piece(3, 2) is not None
    assert board.get_piece(2, 1) is None


def test_move_piece_from_empty_square(board):
    """Test moving from empty square fails"""
    success, result = board.move_piece(3, 3, 4, 4)
    assert success is False


def test_move_piece_to_occupied_square(board):
    """Test moving to occupied square fails"""
    success, result = board.move_piece(2, 1, 1, 0)
    assert success is False

# AVAILABLE MOVES TESTS
def test_get_available_moves_returns_list(board):
    """Test that available moves returns non-empty list"""
    moves = board.get_available_moves(2, 1)
    assert isinstance(moves, list)
    assert len(moves) > 0


def test_get_available_moves_from_empty_square(board):
    """Test available moves from empty square returns empty list"""
    moves = board.get_available_moves(3, 3)
    assert len(moves) == 0


def test_get_available_moves_returns_tuples(board):
    """Test that available moves are tuples"""
    moves = board.get_available_moves(2, 1)
    for move in moves:
        assert isinstance(move, tuple)

# KING PROMOTION TESTS
def test_king_promotion_red_at_bottom(board):
    """Test red piece promotion to king at row 7"""
    # Clear the destination to ensure it's empty
    board.grid[6][1] = Piece('red')
    board.grid[6][1].is_king = False
    board.grid[7][0] = None  
    board.grid[7][2] = None  
    success, _ = board.move_piece(6, 1, 7, 0)
    if success:
        piece = board.get_piece(7, 0)
        assert piece is not None
        assert piece.is_king is True


def test_king_promotion_black_at_top(board):
    """Test black piece promotion to king at row 0"""
    # Clear the destination to ensure it's empty
    board.grid[1][1] = Piece('black')
    board.grid[1][1].is_king = False
    board.grid[0][0] = None  
    board.grid[0][2] = None  
    success, _ = board.move_piece(1, 1, 0, 0)
    if success:
        piece = board.get_piece(0, 0)
        assert piece is not None
        assert piece.is_king is True

# HAS VALID MOVES TESTS
def test_red_has_valid_moves_at_start(board):
    """Test red player has valid moves at game start"""
    assert board.has_valid_moves('red') is True


def test_black_has_valid_moves_at_start(board):
    """Test black player has valid moves at game start"""
    assert board.has_valid_moves('black') is True

# AI PLAYER TESTS
def test_ai_player_creation(ai_player):
    """Test creating an AI player"""
    assert ai_player.color == 'black'


def test_ai_get_best_move_returns_move(board, ai_player):
    """Test that AI returns a valid move"""
    move = ai_player.get_best_move(board)
    assert move is not None


def test_ai_move_format(board, ai_player):
    """Test that AI move has correct format"""
    move = ai_player.get_best_move(board)
    assert isinstance(move, tuple)
    assert len(move) == 3
    from_pos, to_pos, move_type = move
    assert isinstance(from_pos, tuple)
    assert isinstance(to_pos, tuple)
    assert move_type in ['regular', 'capture']