import argparse
import json

from src.Checkers.CheckerState import CheckerState
from src.Chess.ChessState import ChessState
from src.FirstLayerActionModel import FirstLayerActionModel
from src.GamePlayer import GamePlayer
from src.GameRunner import play
from src.HumanActionModel import HumanActionModel
from src.MCST import MCST
from src.NnHeuristic import NnHeuristic
from src.RandomActionModel import RandomActionModel
from src.SuperMiniMax import SuperMiniMax

parser = argparse.ArgumentParser(description='Neno 0')
parser.add_argument('config', type=str,
                    help='The game you want to train on:\nCheckers\nChess')

args = parser.parse_args()

with open(args.config) as json_file:
    config = json.load(json_file)

    game = config['game'].lower()
    train = config['train']
    verbose = config['verbose'] if 'verbose' in config else False
    acConfigs = config['actionModels']
    alternateColors = config['alternateColors'] if 'alternateColors' in config else False

    if acConfigs is None or len(acConfigs) == 0:
        raise Exception("Action models must be specified")


    def convertACConfig(config):
        name = config['name'].lower()
        params = config['params'] if 'params' in config else None
        model = params['model'] if params and 'model' in params else None
        if model:
            if game == 'checkers':
                nnHeuristic = NnHeuristic(model, CheckerState.keras_model)
            elif game == 'chess':
                nnHeuristic = NnHeuristic(model, ChessState.keras_model)

        if name == 'firstlayer':
            return FirstLayerActionModel.from_json(nnHeuristic, params)
        if name == 'minimax':
            return SuperMiniMax.from_json(nnHeuristic, params)
        if name == 'mcst':
            return MCST.from_json(nnHeuristic, params)
        if name == 'human':
            return HumanActionModel.from_json()
        if name == 'random':
            return RandomActionModel.from_json()


    actionModels = list(map(convertACConfig, acConfigs))
    ac1 = actionModels[0]
    ac2 = actionModels[1] if len(actionModels) > 1 else None

    player = GamePlayer(ac1, ac2, alternate=alternateColors)

    if game == 'checkers':
        startState = CheckerState()
    elif game == 'chess':
        startState = ChessState()

    gamesPerTrain = train['gamesPerTrain'] or 1

    if train['model']:
        if game == 'checkers':
            trainedModel = NnHeuristic(train['model'], CheckerState.keras_model)
        elif game == 'chess':
            trainedModel = NnHeuristic(train['model'], CheckerState.keras_model)

    play(player, startState, gamesPerTrain, trainedModel, verbose=verbose)

# train_against_itself(nnHeuristic)


# "./models/chercker_keras_model_3"
