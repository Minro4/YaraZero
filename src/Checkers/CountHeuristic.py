from src.Checkers.CheckerState import CheckerState
from src.Heuristic import Heuristic


class CountHeuristic(Heuristic):

    def h(self, game: CheckerState):
        white = 0
        black = 0

        pieces = filter(lambda x: not x.captured, game.board.board.pieces)

        for p in pieces:
            points = 1.5 if p.king else 1
            if p.player == 1:
                white += points
            else:
                black += points

        total = white + black
        if total == 0:
            return 0.5
        return float(white) / total
