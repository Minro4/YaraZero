import random
from copy import deepcopy, copy

from tensorflow import keras
import tensorflow as tf
from tensorflow.python.keras import Input, Model
from tensorflow.python.keras.layers import Dense, concatenate, Conv2D

from src.Checkers.Checkers.game import Game
from src.GameState import GameState
import numpy as np


class CheckerState(GameState):
    # 1 pour le tour 1 pour le nombre de piece rouge et 1 pour le nombre de piece noir
    input_shape_features = (3,)  # (3,)

    # 8 slot pour les rouge, 8 pour les noirs, pour chaque, on a (normal, roi, pos x, pos y)
    input_shape_board = (8, 2, 4)

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
        moves = self.board.moves
        return moves[len(moves) - 1]

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
        return hash(frozenset(self.board.board.pieces))

    def __eq__(self, other):
        return self.board.board.pieces == other.board.board.pieces

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

    def state(self):
        a = np.zeros(CheckerState.input_shape_board, dtype=float)
        b = np.zeros(CheckerState.input_shape_features, dtype=float)
        return [a, b]

    @staticmethod
    def keras_model():
        input_board = Input(shape=CheckerState.input_shape_board)
        input_features = Input(shape=CheckerState.input_shape_features)

        x = Conv2D(128, (1, 1), activation="relu")(input_board)
        x = Model(inputs=input_board, outputs=x)

        y = Dense(128, activation="relu")(input_features)
        y = Model(inputs=input_features, outputs=y)

        combined = concatenate([x.output, y.output])

        z = Dense(128, activation="relu")(combined)
        z = Dense(128, activation="relu")(z)
        z = Dense(1, activation="relu")(z)

        model = Model(inputs=[x.input, y.input], outputs=z)

        model.compile(optimizer='adam',
                      loss='mean_squared_error',
                      metrics=['accuracy'])

        return model
