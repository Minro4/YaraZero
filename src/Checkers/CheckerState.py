import random
from copy import deepcopy, copy

from tensorflow import keras
import tensorflow as tf
from tensorflow.python.keras import Input, Model
from tensorflow.python.keras.layers import Dense, concatenate, Conv2D

from src.Checkers.Checkers.game import Game
from src.Checkers.Checkers.piece import Piece
from src.GameState import GameState
import numpy as np


class CheckerState(GameState):
    nbr_attributes = 4
    board_input_size = 8 * 4 * nbr_attributes

    input_size = board_input_size + 3

    input_shape = (input_size,)

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
            return 0.5
        return 1 if winner == 1 else 0

    def move_count(self):
        return len(self.board.moves)

    def nbr_epochs(self):
        # n = round(self.max_moves_per_game / self.move_count())
        # n *= 1 if self.winner() == 0 else 3
        return 1

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
        while board.winner() == 0.5:
            board = CheckerState.random_board()
        return board

    def state(self):
        a = np.zeros(CheckerState.input_size, dtype=float)
        pieces = self.board.board.pieces

        nbr_p1 = 0
        nbr_p2 = 0

        for p in pieces:
            if p.captured or p.position is None or p.player is None:
                continue
            if p.player == 1:
                nbr_p1 += 1
            else:
                nbr_p2 += 1

            idx = (p.position - 1) * CheckerState.nbr_attributes
            a[idx + p.player - 1] = 1 if p.king else 0.5
            a[idx + 2] = len(p.get_possible_capture_moves()) / 2
            a[idx + 3] = p.nbr_possible_get_captured() / 2

        a[CheckerState.board_input_size] = 1 if self.turn() else 0
        a[CheckerState.board_input_size + 1] = float(nbr_p1) / 12
        a[CheckerState.board_input_size + 2] = float(nbr_p2) / 12

        return a

    @staticmethod
    def keras_model():
        model = keras.Sequential([
            keras.layers.Input(shape=CheckerState.input_shape),
            keras.layers.Dense(128, activation='relu'),
            keras.layers.Dense(128, activation='relu'),
            keras.layers.Dense(128, activation='relu'),
            keras.layers.Dense(1)
        ])

        model.compile(optimizer='adam',
                      loss='mean_squared_error',
                      metrics=['accuracy'])

        return model

    def moves_str(self):
        moves = self.legal_moves()
        s = ""
        for idx, m in enumerate(moves):
            s += str(idx) + ": " + Piece.position_to_str(self.board.board, m[0]) + " -> " + Piece.position_to_str(
                self.board.board, m[1]) + "\n"
        return s
        # input_board = Input(shape=CheckerState.input_shape_board)
        # input_features = Input(shape=CheckerState.input_shape_features)
        #
        # x = Dense(128, activation="relu")(input_board)
        # x = Model(inputs=input_board, outputs=x)
        #
        # y = Dense(128, activation="relu")(input_features)
        # y = Model(inputs=input_features, outputs=y)
        #
        # combined = concatenate([x.output, y.output])
        #
        # z = Dense(128, activation="relu")(combined)
        # z = Dense(128, activation="relu")(z)
        # z = Dense(1, activation="relu")(z)
        #
        # model = Model(inputs=[x.input, y.input], outputs=z)
        #
        # model.compile(optimizer='adam',
        #               loss='mean_squared_error',
        #               metrics=['accuracy'])
        #
        # return model
