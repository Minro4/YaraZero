from abc import ABC
from collections import defaultdict
import math

from src.ActionModels.ActionModel import ActionModel
from src.GameState import GameState
from src.Heuristic import Heuristic


class MCST(Heuristic, ActionModel, ABC):
    "Monte Carlo tree searcher. First rollout the tree then choose a move."

    def __init__(self, nbr_rollouts=50, exploration_weight=1, heuristic: Heuristic = None):
        self.Q = defaultdict(int)  # total reward of each node
        self.N = defaultdict(int)  # total visit count for each node
        self.children = dict()  # children of each node
        self.exploration_weight = exploration_weight
        self.nbr_rollouts = nbr_rollouts
        self.heuristic = heuristic

    @staticmethod
    def from_json(heuristic, json):
        return MCST(json['nbr_rollouts'], json['exploration_weight'], heuristic)

    def h(self, game: GameState):
        if game.terminal():
            return game.winner()

        for _ in range(self.nbr_rollouts):
            self.do_rollout(game)

        return self.h_score(self.choose(game))

    def action(self, game: GameState):
        for _ in range(self.nbr_rollouts):
            self.do_rollout(game)

        choice = self.choose(game)
        move = choice.pop()
        value = self.h_score(choice)
        return move, value

    def choose(self, node: GameState):
        def score(n):
            if self.N[n] == 0:
                return float("-inf")  # avoid unseen moves
            return self.Q[n] / self.N[n]  # average reward

        "Choose the best successor of node. (Choose a move in the game)"
        if node.terminal():
            raise RuntimeError(f"choose called on terminal node {node}")

        if node not in self.children:
            return node.random_child()

        return max(self.children[node], key=score)

    def do_rollout(self, node: GameState):
        node = node.__copy__()
        "Make the tree one layer better. (Train for one iteration.)"
        path = self._select(node)
        leaf = path[-1]
        self._expand(leaf)
        if self.heuristic is None:
            reward = self._simulate(leaf.__copy__())
        else:
            reward = self.heuristic.h(node)
        self._backpropagate(path, reward)

    def _select(self, node: GameState):
        "Find an unexplored descendent of `node`"
        path = []
        while True:
            path.append(node)
            if node not in self.children or not self.children[node]:
                # node is either unexplored or terminal
                return path
            unexplored = self.children[node] - self.children.keys()
            if unexplored:
                n = unexplored.pop()
                path.append(n)
                return path
            node = self._uct_select(node)  # descend a layer deeper

    def _expand(self, node: GameState):
        "Update the `children` dict with the children of `node`"
        if node in self.children:
            return  # already expanded
        self.children[node] = set(node.children())

    def _simulate(self, node: GameState):
        "Returns the reward for a random simulation (to completion) of `node`"
        invert_reward = True
        while True:
            if node.terminal():
                reward = node.reward()
                return 1 - reward if invert_reward else reward
            node = node.push(node.random_move())
            invert_reward = not invert_reward

    def _backpropagate(self, path, reward):
        "Send the reward back up to the ancestors of the leaf"
        for node in reversed(path):
            self.N[node] += 1
            self.Q[node] += reward
            reward = 1 - reward  # 1 for me is 0 for my enemy, and vice versa

    def _uct_select(self, node: GameState):
        "Select a child of node, balancing exploration & exploitation"

        # All children of node should already be expanded:
        assert all(n in self.children for n in self.children[node])

        log_N_vertex = math.log(self.N[node])

        def uct(n):
            "Upper confidence bound for trees"
            return self.Q[n] / self.N[n] + self.exploration_weight * math.sqrt(
                log_N_vertex / self.N[n]
            )

        return max(self.children[node], key=uct)

    def _score(self, n):
        if self.N[n] == 0:
            return float("-inf")  # avoid unseen moves
        return self.Q[n] / self.N[n]  # average reward

    def h_score(self, game: GameState):
        s = self._score(game)
        return 1 - s if game.turn() else s
        # return (s * 2 - 1) * (-1 if game.turn() else 1)
