import chess

from src.GameState import GameState
import numpy as np


class ChessState(GameState):
    input_size: int = 8 * 8 * 12 + 1
    nb_pieces: int = 12
    max_moves_per_game: int = 75

    def __init__(self, board=None):
        if board is None:
            board = chess.Board()
        self.board = board

    def __copy__(self):
        return ChessState(board=self.board.copy())

    def __str__(self):
        return self.board.__str__()

    def legal_moves(self):
        return np.array(list(self.board.legal_moves))

    def push(self, move):
        self.board.push(move)
        return self

    def pop(self):
        return self.board.pop()

    def history(self):
        history = []
        g = self.__copy__()
        history.append(g.state())
        for i in range(len(g.board.move_stack)):
            g.pop()
            history.append(g.state())
        return history

    def turn(self) -> bool:
        return self.board.turn

    def state(self):
        a = np.zeros(self.input_size, dtype=float)
        a[0] = 0 if self.turn() else 1
        for i in range(0, 8 * 8):
            p = self.board.piece_at(i)
            if p is not None:
                idx: int = self._piece_to_idx(p) + 1 + i * self.nb_pieces
                a[int(idx)] = 1

        return a

    def game_over(self) -> bool:
        return self.board.is_game_over() or self.move_count() >= self.max_moves_per_game

    # -1 if player false won, 0 if drawn or not over, 1 if player true won
    def winner(self) -> int:
        if self.board.is_checkmate():
            return -1 if self.turn() else 1
        else:
            return 0

    def move_count(self):
        return len(self.board.move_stack)

    def nbr_epochs(self):
        n = round(self.max_moves_per_game / self.move_count())
        n *= 1 if self.winner() == 0 else 3
        return n

    def _piece_to_idx(self, piece: chess.Piece) -> int:
        return piece.piece_type - 1 + (0 if piece.color else self.nb_pieces / 2)

    def __hash__(self):
        return hash(frozenset(self.board.move_stack))

    def __eq__(self, other):
        return self.board.__eq__(other.board)

    @staticmethod
    def input_shape(self):
        return (self.input_size,)

    @staticmethod
    def random_board(nbr_moves):
        state = ChessState()
        return state.apply_random_moves(nbr_moves)

    @staticmethod
    def random_winning_board():
        game = ChessState.random_board()
        while board.winner() == 0:
            board = ChessState.random_board()
        return board
