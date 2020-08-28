from abc import abstractmethod, ABC
import random
from copy import copy

import numpy as np


class GameState(ABC):

    def __copy__(self):
        pass

    def __str__(self):
        pass

    @abstractmethod
    def legal_moves(self):
        pass

    @abstractmethod
    def push(self, move):
        pass

    @abstractmethod
    def pop(self):
        pass

    # return numpy array of all states
    def history(self):
        history = []
        g = copy(self)
        history.append(copy(g))
        for i in range(len(g.board.move_stack)):
            g.pop()
            history.append(copy(g))
        return history

    @abstractmethod
    def turn(self) -> bool:
        pass

    @abstractmethod
    def state(self):
        pass

    def state_move(self, move):
        self.push(move)
        state = self.state()
        self.pop()
        return state

    @abstractmethod
    def game_over(self) -> bool:
        pass

    def terminal(self):
        return self.game_over()

    @abstractmethod
    def move_count(self):
        pass

    # -1 if player false won, 0 if drawn or not over, 1 if player true won
    @abstractmethod
    def winner(self) -> int:
        pass

    def reward(self):
        winner = self.winner()
        winner *= 1 if self.turn() else -1
        return (winner + 1) / 2

    def nbr_epochs(self):
        return 1

    def random_move(self):
        return random.choice(self.legal_moves())

    def random_child(self):
        return self.__copy__().push(self.random_move())

    def children(self):
        return [self.__copy__().push(move) for move in self.legal_moves()]

    @abstractmethod
    def __hash__(self):
        "Nodes must be hashable"
        return 123456789

    @abstractmethod
    def __eq__(node1, node2):
        "Nodes must be comparable"
        return True

    def apply_random_moves(self, nbr_moves=None):
        i = 0
        while not self.game_over() and (nbr_moves is None or i < nbr_moves):
            i += 1
            move = self.random_move()
            self.push(move)
        return self
