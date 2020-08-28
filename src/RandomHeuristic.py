import random
from abc import ABC
import numpy as np

from src import GameState
from src.Heuristic import Heuristic


class RandomHeuristic(Heuristic, ABC):
    def h(self, game: GameState):
        return random.random()

    def hs(self, games):
        a = np.zeros(len(games))
        for idx, game in enumerate(games):
            a[idx] = self.h(game)
        return a
