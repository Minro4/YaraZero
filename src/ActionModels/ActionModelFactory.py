from src.ActionModels.FirstLayerActionModel import FirstLayerActionModel
from src.ActionModels.HumanActionModel import HumanActionModel
from src.ActionModels.MCST import MCST
from src.ActionModels.RandomActionModel import RandomActionModel
from src.ActionModels.SuperMiniMax import SuperMiniMax


class ActionModelFactory:
    @staticmethod
    def from_json(name, params=None, nnHeuristic=None):
        if name == 'firstlayer':
            return FirstLayerActionModel.from_json(nnHeuristic, params)
        elif name == 'minimax':
            return SuperMiniMax.from_json(nnHeuristic, params)
        elif name == 'mcst':
            return MCST.from_json(nnHeuristic, params)
        elif name == 'human':
            return HumanActionModel.from_json()
        elif name == 'random':
            return RandomActionModel.from_json()
        else:
            raise Exception("Invalid action model name.")
