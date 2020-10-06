import argparse
import json

from src.ActionModels.ActionModelFactory import ActionModelFactory
from src.GameOptionsFactory import GameOptionsFactory
from src.GamePlayer import GamePlayer
from src.GameRunner import play
from src.NnHeuristic import NnHeuristic

parser = argparse.ArgumentParser(description='Neno 0')
parser.add_argument('config', type=str,
                    help='The game you want to train on:\nCheckers\nChess')

args = parser.parse_args()

with open(args.config) as json_file:
    config = json.load(json_file)

gameOptions = GameOptionsFactory.factory(config['game'])
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
    nnHeuristic = NnHeuristic(model, gameOptions.keras_model()) if model else None
    return ActionModelFactory.from_json(name, params=params, nnHeuristic=nnHeuristic)


actionModels = list(map(convertACConfig, acConfigs))
ac1 = actionModels[0]
ac2 = actionModels[1] if len(actionModels) > 1 else None

player = GamePlayer(ac1, ac2, alternate=alternateColors)

gamesPerTrain = train['gamesPerTrain'] or 1

if train['model']:
    trainedModel = NnHeuristic(train['model'], gameOptions.keras_model())

play(player, gameOptions.start_state(), gamesPerTrain, trainedModel, verbose=verbose)
