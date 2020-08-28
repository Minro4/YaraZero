from src import GameState
from src.ActionModel import ActionModel


class RandomActionModel(ActionModel):

    def action(self, game: GameState):
        return game.random_move(), 0

