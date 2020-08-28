import chess
import chess.engine
import math
import random
from src.Chess.ChessState import ChessState
import pickle
import numpy as np


def generate_tests(nbr_tests):
    states = []
    results = []
    for i in range(nbr_tests):
        board = ChessState.random_board(random.randint(1, 50))
        states.append(board)
        if board.game_over():
            results.append(board.winner())
        else:
            results.append(stockfish_eval(board.board))
    return states, results


def random_board(nbr_moves):
    board = chess.Board()
    i = 0
    while not board.is_game_over() and i < nbr_moves:
        i += 1
        moves = list(board.legal_moves)
        idx = random.randint(0, len(moves) - 1)
        board.push(moves[idx])
    return board


def random_end_board():
    return random_board(ChessState.max_moves_per_game)


def random_winning_board():
    board = random_end_board()
    while not board.is_checkmate():
        board = random_end_board()
    return board


def stockfish_eval(board, eval_time=1):
    engine = chess.engine.SimpleEngine.popen_uci(
        "D:\OneDrive\_Uni\Personnal\ChessAI\Stockfish\Windows\stockfish_20011801_x64.exe")
    limit = chess.engine.Limit(time=eval_time)
    # res = engine.play(board, limit)
    res = engine.analyse(board, limit)
    engine.quit()

    score = res['score']
    value = 0
    if hasattr(score.relative, 'cp'):
        value = sigmoid(score.relative.cp / 100) * 2 - 1
    elif hasattr(score.relative, 'moves'):
        value = -1 if score.turn else 1

    # print(value)
    return value


def generate_winning_training_set(nbr_boards):
    x = np.zeros((nbr_boards, ChessState.input_size))
    y = np.zeros(nbr_boards)
    for i in range(nbr_boards):
        board = random_winning_board()
        state = ChessState(board)
        y[i] = state.winner()
        state.pop()
        x[i] = state.state()
        print("done: " + str(i))
    return x, y


def sigmoid(x):
    return 1 / (1 + math.exp(-x))


def save_tests(tests, path):
    pickle_out = open(path, "wb")
    pickle.dump(tests, pickle_out)
    pickle_out.close()


def load_tests(path):
    pickle_in = open(path, "rb")
    return pickle.load(pickle_in)


# tests = generate_tests(10)
# print(tests)
# save_tests(tests,"./test_data/stockfish_1.1_10.txt")




