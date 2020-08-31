from src import GameState
from src.ActionModel import ActionModel
from src.Heuristic import Heuristic


class SuperMiniMax(ActionModel):
    def __init__(self, heuristic: Heuristic, max_depth):
        self.heuristic = heuristic
        self.max_depth = max_depth

    def action(self, game: GameState):
        if game.game_over():
            return None

        b_list = []
        hs = []
        self.tour_max_calc(game, b_list, 0) if game.turn() else self.tour_min_calc(game, b_list, 0)
        if b_list:
            hs = self.heuristic.hs(b_list)

        u, b, count = self.tour_max(game, hs, 0, 0) if game.turn() else self.tour_min(game, hs, 0, 0)

        return b.pop(), u

    def tour_max_calc(self, board: GameState, b_list, depth):
        if board.game_over():
            return

        if depth >= self.max_depth:
            b_list.append(board)
            return

        for child in board.children():
            self.tour_min_calc(child, b_list, depth + 1)

    def tour_min_calc(self, board: GameState, b_list, depth):
        if board.game_over():
            return

        if depth >= self.max_depth:
            b_list.append(board)
            return

        for child in board.children():
            self.tour_max_calc(child, b_list, depth + 1)

    def tour_max(self, board: GameState, h_list, depth, count):
        if board.game_over():
            return board.winner(), None, count

        if depth >= self.max_depth:
            return h_list[count], None, count + 1

        b = None
        u = float("-inf")

        for child in board.children():
            util, _, count = self.tour_min(child, h_list, depth + 1, count)
            if util > u:
                b = child
                u = util

        return u, b, count

    def tour_min(self, board: GameState, h_list, depth, count):
        if board.game_over():
            return board.winner(), None, count

        if depth >= self.max_depth:
            return h_list[count], None, count + 1

        b = None
        u = float("inf")
        for child in board.children():
            util, _, count = self.tour_max(child, h_list, depth + 1, count)
            if util < u:
                b = child
                u = util

        return u, b, count
