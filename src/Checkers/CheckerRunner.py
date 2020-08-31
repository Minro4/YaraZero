import time

from src.Checkers.CheckerState import CheckerState
from src.FirstLayerActionModel import FirstLayerActionModel
from src.GamePlayer import GamePlayer
from src.HumanActionModel import HumanActionModel
from src.MCST import MCST
from src.NnHeuristic import NnHeuristic
from src.RandomActionModel import RandomActionModel
from src.SuperMiniMax import SuperMiniMax
from src.WinCounter import WinCounter

nnHeuristic = NnHeuristic("./models/chercker_keras_model_3", CheckerState.keras_model)


# actionModel1 = FirstLayerActionModel(nnHeuristic)  # MCST(10)
#
# actionModel2 = RandomActionModel()  # SuperMiniMax(heuristic, 4)
# #player = GamePlayer(actionModel2)
def test(heuristic):
    res = heuristic.test_path("D:/OneDrive/_Uni/Personnal/ChessAI/src/Checkers/test_data/checkers_count_heuristic")
    print("--- Tests - average loss:" + str(res) + " ---")


def play(heuristic, player, games_per_train, train=False):
    winCount = WinCounter()
    while True:
        # test(heuristic)

        a_states = []
        a_hs = []

        for i in range(games_per_train):
            game = CheckerState()
            winner, states, hs = player.play(game, False)
            winCount.add(winner)
            results = [winner] * len(states)
            a_states.extend(states)
            a_hs.extend(results)

        print(winCount)
        if train:
            heuristic.train(a_states, a_hs, 1)
            heuristic.save()


def train_on_random_games(heuristic: NnHeuristic):
    player = GamePlayer(RandomActionModel())
    play(heuristic, player, 250, train=True)


def train_against_random(heuristic: NnHeuristic):
    player = GamePlayer(RandomActionModel(), FirstLayerActionModel(heuristic), alternate=False)
    play(heuristic, player, 25, train=True)


def train_against_itself(heuristic: NnHeuristic):
    player = GamePlayer(FirstLayerActionModel(heuristic, variance=True), alternate=False)
    play(heuristic, player, 25, train=True)


def play_against_human(heuristic: NnHeuristic):
    player = GamePlayer(HumanActionModel(), FirstLayerActionModel(heuristic, variance=False), alternate=False)
    play(heuristic, player, 1, train=False)


train_against_itself(nnHeuristic)
