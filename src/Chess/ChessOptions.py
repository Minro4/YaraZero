from src.Chess.ChessState import ChessState
from src.GameOptions import GameOptions


class ChessOptions(GameOptions):
    def keras_model(self):
        return ChessState.keras_model()

    def start_state(self):
        return ChessState()