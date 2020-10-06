from src.Chess import ChessValidation
from src.Chess.ChessState import ChessState
from src.Chess.ChessValidation import generate_winning_training_set, \
    save_tests
from src.GamePlayer import GamePlayer
from src.ActionModels.MCST import MCST
# from NnHeuristic import NnHeuristic
from src.ActionModels.RandomActionModel import RandomActionModel
import numpy as np

mate_in_1_training = "training_data/winning_positions.txt"

# game = ChessState()
# nnHeuristic = NnHeuristic("./models/keras_model_1024_2", game)
# monteCarloHeuristic = MonteCarloHeuristic(50)

# monteCarloHeuristic.test_path("./test_data/stockfish_1.1_10.txt", verbose=2)




def train(nnHeuristic, path, epochs=10):
    training = ChessValidation.load_tests(path)
    nnHeuristic.train(training[0], training[1], epochs)
    nnHeuristic.save()

    avg_loss = nnHeuristic.test(training[0], training[1])
    print("--- Tests - average loss:" + str(avg_loss) + " ---")


def mate_in_1_generation(path, set_size):
    training = generate_winning_training_set(set_size)
    save_tests(training, path)


def mc_play_game(nbr_rollouts=100):
    ac1 = MCST(nbr_rollouts, exploration_weight=1)
    ac2 = RandomActionModel()
    chessState = ChessState()
    cp = GamePlayer(chessState, ac1, ac2)
    winner, states, hs = cp.play(True)
    print(winner)
    print(states)
    print(hs)
    return np.array(states[0::2], hs[0::2])


a = [1,2,3,4]
print(a[0::2])

print(mc_play_game())
