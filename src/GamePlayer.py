from src.ActionModels.ActionModel import ActionModel
from src.GameState import GameState


class GamePlayer:
    def __init__(self, action_model1: ActionModel, action_model2: ActionModel = None, alternate=False):
        self.actionModel1 = action_model1
        if action_model2 is None:
            action_model2 = action_model1
        self.actionModel2 = action_model2
        self.alternate = alternate

    def play(self, game: GameState, verbose=False):
        if self.alternate:
            temp = self.actionModel1
            self.actionModel1 = self.actionModel2
            self.actionModel2 = temp

        states = []
        hs = []

        if verbose:
            print(game)

        while not game.game_over():
            actingModel = self.actionModel1 if game.turn() else self.actionModel2
            move, h = actingModel.action(game)
            states.append(game.__copy__())
            hs.append(h)
            game.push(move)

            if verbose:
                print("move: " + str(move) + " h: " + str(h))
                print(game)

        return game.winner(), states, hs
