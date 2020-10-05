from src import GameState
from src.ActionModel import ActionModel


class RandomActionModel(ActionModel):
    @staticmethod
    def from_json():
        return RandomActionModel()

    def action(self, game: GameState):
        return game.random_move(), 0

