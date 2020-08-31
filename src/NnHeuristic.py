import random

import tensorflow as tf
from tensorflow import keras

from src.GameState import GameState
import numpy as np

from src.Heuristic import Heuristic

config = tf.compat.v1.ConfigProto(gpu_options=
                                  tf.compat.v1.GPUOptions(per_process_gpu_memory_fraction=0.8)
                                  # device_count = {'GPU': 1}
                                  )
config.gpu_options.allow_growth = True
session = tf.compat.v1.Session(config=config)
tf.compat.v1.keras.backend.set_session(session)


def games_to_inputs(games: GameState):
    return [game.state() for game in games]


class NnHeuristic(Heuristic):

    def __init__(self, path, model):
        self.model_path = path
        try:
            self.model = keras.models.load_model(path)
        except OSError:
            self.model = model()

    # game_states: numpy array of inputs
    def hs(self, games):
        inputs = games_to_inputs(games)
        res = self.model(np.array(inputs))
        return np.array(res)

    # game_states: numpy array of inputs
    def h(self, game: GameState):
        return self.hs([game])

    def h_batch(self, game_states: np.ndarray):
        predictions = self.model.predict(game_states)
        return np.array(predictions)

    # board, winning for white 0 if lost, 0.5 if draw, 1 if win
    def train(self, games, results, epochs: int = 1):
        x = np.array(games_to_inputs(games))
        y = np.array(results)
        self.model.fit(x=x, y=y, epochs=epochs)

    def save(self):
        self.model.save(self.model_path)
