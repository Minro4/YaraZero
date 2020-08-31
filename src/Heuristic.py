from abc import abstractmethod, ABC
import numpy as np

from src.Chess import ChessValidation


class Heuristic(ABC):

    def hs(self, games):
        a = np.zeros(len(games))
        for idx, game in enumerate(games):
            a[idx] = self.h(game)
        return a

    @abstractmethod
    def h(self, game):
        pass

    def test_path(self, path, verbose=0):
        tests = ChessValidation.load_tests(path)
        avg_loss = self.test(tests[0], tests[1], verbose=verbose > 1)
        if verbose > 0:
            print("Tests results: average loss: " + str(avg_loss))
        return avg_loss

    def test(self, states, expected, verbose=False):
        x = np.array(states)
        results = self.hs(x)
        sumr = 0
        for i in range(len(x)):
            sumr += abs(results[i] - expected[i])
        avg = sumr / len(x)

        if verbose:
            print("results: ")
            print(results)
            print("expected: ")
            print(expected)
        return avg
