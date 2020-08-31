import chess
import chess.engine
import math
import random

from src.Checkers.CheckerState import CheckerState
from src.Checkers.CountHeuristic import CountHeuristic
from src.Chess.ChessState import ChessState
import pickle
import numpy as np


def generate_tests(nbr_tests, heuristic):
    states = []
    results = []
    for i in range(nbr_tests):
        board = CheckerState.random_board(random.randint(1, 75))
        states.append(board)
        if board.game_over():
            results.append(board.winner())
        else:
            results.append(heuristic.h(board))
    return states, results


def save_tests(tests, path):
    pickle_out = open(path, "wb")
    pickle.dump(tests, pickle_out)
    pickle_out.close()


def load_tests(path):
    pickle_in = open(path, "rb")
    return pickle.load(pickle_in)


heuristic = CountHeuristic()
tests = generate_tests(1000, heuristic)
save_tests(tests, "./test_data/checkers_count_heuristic")
