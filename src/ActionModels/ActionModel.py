from src.GameState import GameState


class ActionModel:
    def action(self, game: GameState):
        pass

    def win_heuristic(self, games):
        for idx, game in enumerate(games):
            if game.game_over():
                return idx
        return -1

    def default_heuristic(self, games, results):
        for idx, game in enumerate(games):
            if game.game_over():
                results[idx] = game.winner()
        return results
