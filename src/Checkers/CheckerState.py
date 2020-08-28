from copy import deepcopy, copy

from src.Checkers.Checkers.game import Game
from src.GameState import GameState
import numpy as np


class CheckerState(GameState):
    # TODO
    input_size: int = 8 * 8 * 12 + 1
    nb_pieces: int = 12
    max_moves_per_game: int = 75

    def __init__(self, board=None):
        if board is None:
            board = Game()
        self.board = board

    def __copy__(self):
        return CheckerState(board=deepcopy(self.board))

    def __str__(self):
        return self.board.__str__()

    def legal_moves(self):
        return self.board.get_possible_moves()

    def push(self, move):
        self.board.move(move)
        return self

    # TODO
    def pop(self):
        pass

    def history(self):
        history = []
        moves = self.board.moves
        game = CheckerState()
        history.append(copy(game))
        for i in range(len(moves)):
            game.push(moves[i])
            history.append(copy(game))
        return history

    def turn(self) -> bool:
        return self.board.whose_turn() == 1

    # TODO
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
        return self.board.is_over()

    # -1 if player false won, 0 if drawn or not over, 1 if player true won
    def winner(self) -> int:
        winner = self.board.get_winner()
        if winner is None:
            return 0
        return 1 if winner == 1 else -1

    def move_count(self):
        return len(self.board.moves)

    def nbr_epochs(self):
        n = round(self.max_moves_per_game / self.move_count())
        n *= 1 if self.winner() == 0 else 3
        return n

    def __hash__(self):
        return hash(frozenset(self.board.move_stack))

    def __eq__(self, other):
        return self.board.__eq__(other.board)

    @staticmethod
    def input_shape(self):
        return (self.input_size,)

    @staticmethod
    def random_board(nbr_moves=None):
        state = CheckerState()
        return state.apply_random_moves(nbr_moves)

    @staticmethod
    def random_winning_board():
        game = CheckerState.random_board()
        while board.winner() == 0:
            board = CheckerState.random_board()
        return board
