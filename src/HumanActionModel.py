from src.ActionModel import ActionModel
from src.GameState import GameState


class HumanActionModel(ActionModel):
    def action(self, game: GameState):
        print(game.__str__())
        moves = game.legal_moves()
        print(game.moves_str())
        inp = int(input())
        return moves[inp], 0
