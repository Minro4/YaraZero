from abc import ABC, abstractmethod


class GameOptions(ABC):
    @abstractmethod
    def keras_model(self):
        pass

    @abstractmethod
    def start_state(self):
        pass
