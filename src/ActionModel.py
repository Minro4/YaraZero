from src.GameState import GameState


# def moves_to_states(game: GameState, moves):
#     return np.array([game.state_move(move) for move in moves])
#
# def moves_to_boards(game: GameState, moves):
#     return np.array([game.__copy__().push(move) for move in moves])
#
# def boards_to_states(games: GameState):
#     return np.array([game.state() for game in games])

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

    # def simulate_move(self, game: GameState, move: str):
    #     value = 0
    #     color = board.turn
    #     board.push(move)
    #     if board.is_game_over():
    #         if board.is_checkmate():
    #             value = 1 if color == chess.WHITE else -1
    #     else:
    #         value = self.heuristic.h(board)
    #
    #     board.pop()
    #     return value
