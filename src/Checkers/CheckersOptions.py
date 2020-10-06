from src.Checkers.CheckerState import CheckerState
from src.GameOptions import GameOptions


class CheckersOptions(GameOptions):
    def keras_model(self):
        return CheckerState.keras_model()

    def start_state(self):
        return CheckerState()
