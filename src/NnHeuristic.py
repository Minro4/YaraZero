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

            # print("No model found for path: " + path)
            # print("Initializing new model")
            # self.model = keras.Sequential([
            #     keras.layers.Flatten(input_shape=input_shape),
            #     keras.layers.Dense(1024, activation='relu'),
            #     keras.layers.Dense(1024, activation='relu'),
            #     keras.layers.Dense(1024, activation='relu'),
            #     keras.layers.Dense(1)
            # ])
            #
            # self.model.compile(optimizer='adam',
            #                    loss='mean_squared_error',
            #                    metrics=['accuracy'])

    # game_states: numpy array of inputs
    def hs(self, games):
        # predictions = self.probability_model.predict(game_states)
        # predictions = self.model.predict(game_states)
        inputs = games_to_inputs(games)
        return self.model(inputs)

    # game_states: numpy array of inputs
    def h(self, game: GameState):
        return self.hs([game])

    def h_batch(self, game_states: np.ndarray):
        predictions = self.model.predict(game_states)
        return np.array(predictions)

    # board, winning for white 0 if lost, 0.5 if draw, 1 if win
    def train(self, states, results, epochs: int = 1):
        x = np.array(states)
        y = np.array(results)
        self.model.fit(x=x, y=y, epochs=epochs)

    # test_loss, test_acc = self.model.evaluate(x, y, verbose=2)
    # print("loss: " + str(test_loss))
    # print("acc: " + str(test_acc))

    def save(self):
        self.model.save(self.model_path)
