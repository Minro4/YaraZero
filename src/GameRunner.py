from copy import copy

from src.Checkers.CheckerState import CheckerState
from src.FirstLayerActionModel import FirstLayerActionModel
from src.GamePlayer import GamePlayer
from src.HumanActionModel import HumanActionModel
from src.NnHeuristic import NnHeuristic
from src.RandomActionModel import RandomActionModel
from src.WinCounter import WinCounter


def test(heuristic):
    res = heuristic.test_path("D:/OneDrive/_Uni/Personnal/ChessAI/src/Checkers/test_data/checkers_count_heuristic")
    print("--- Tests - average loss:" + str(res) + " ---")


def play(player, start_state, games_per_train, heuristic=None, verbose=False):
    winCount = WinCounter()
    while True:
        a_states = []
        a_hs = []

        for i in range(games_per_train):
            game = copy(start_state)
            winner, states, hs = player.play(game, verbose)
            winCount.add(winner)
            results = [winner] * len(states)
            a_states.extend(states)
            a_hs.extend(results)

        print(winCount)
        if heuristic:
            heuristic.train(a_states, a_hs, 1)
            heuristic.save()


def train_on_random_games(heuristic: NnHeuristic):
    player = GamePlayer(RandomActionModel())
    play(player, 250, heuristic)


def train_against_random(heuristic: NnHeuristic):
    player = GamePlayer(RandomActionModel(), FirstLayerActionModel(heuristic), alternate=False)
    play(player, 25, heuristic)


def train_against_itself(heuristic: NnHeuristic):
    player = GamePlayer(FirstLayerActionModel(heuristic, variance=True), alternate=False)
    play(player, 25, heuristic)


def play_against_human(heuristic: NnHeuristic):
    player = GamePlayer(HumanActionModel(), FirstLayerActionModel(heuristic, variance=False), alternate=False)
    play(player, 1, heuristic)
