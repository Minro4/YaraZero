import numpy as np

from src.ActionModel import ActionModel
from src.GameState import GameState


class FirstLayerActionModel(ActionModel):
    def __init__(self, heuristic):
        self.heuristic = heuristic

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
        if game.turn():
            bestIdx = np.argmax(evals)
        else:
            bestIdx = np.argmin(evals)
        bestMove = possibleMoves[bestIdx]

        return bestMove, evals[bestIdx]
