import random

import numpy as np

from src.ActionModels.ActionModel import ActionModel
from src.GameState import GameState


class FirstLayerActionModel(ActionModel):
    def __init__(self, heuristic, variance=False):
        self.heuristic = heuristic
        self.variance = variance

    @staticmethod
    def from_json(heuristic, json):
        return FirstLayerActionModel(heuristic, json['variance'])

    def action(self, game: GameState):
        if game.game_over():
            return None

        possibleMoves = game.legal_moves()
        boards = game.children()

        win_h = self.win_heuristic(boards)
        if not win_h == -1:
            return possibleMoves[win_h], 1

        evals = self.heuristic.hs(boards)
        evals = self.default_heuristic(boards, evals)

        if self.variance:
            if not game.turn():
                evals = [1 - e for e in evals]
            total = sum(evals)
            evals = [e / total for e in evals]
            choice = random.random()
            s = 0
            for idx, e in enumerate(evals):
                s += e
                if choice <= s:
                    bestIdx = idx
                    break

        else:
            if game.turn():
                bestIdx = np.argmax(evals)
            else:
                bestIdx = np.argmin(evals)

        bestMove = possibleMoves[bestIdx]

        return bestMove, evals[bestIdx]
