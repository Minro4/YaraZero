from src.Checkers.CheckersOptions import CheckersOptions
from src.Chess.ChessOptions import ChessOptions


class GameOptionsFactory:
    @staticmethod
    def factory(name):
        name = name.lower()
        if name == 'chess':
            return ChessOptions()
        elif name == 'checkers':
            return CheckersOptions()
        else:
            raise Exception('Invalid game name')
