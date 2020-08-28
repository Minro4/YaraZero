import time

from src.Checkers.CheckerState import CheckerState
from src.FirstLayerActionModel import FirstLayerActionModel
from src.GamePlayer import GamePlayer
from src.MCST import MCST
from src.NnHeuristic import NnHeuristic
from src.RandomActionModel import RandomActionModel

heuristic = NnHeuristic("./models/chercker_keras_model_1", CheckerState.keras_model)
actionModel1 = FirstLayerActionModel(heuristic) #MCST(10)
actionModel2 = RandomActionModel()  # FirstLayerActionModel(heuristic)
player = GamePlayer(actionModel1, actionModel2)

white = 0
black = 0
draw = 0

for i in range(100):
    print("iteration: " + str(i + 1))

    start_time = time.time()
    game = CheckerState()
    winner, states, hs = player.play(game, True)

    if winner == 1:
        white += 1
        print("White won")
    elif winner == -1:
        black += 1
        print("Black won")
    else:
        draw += 1
        print("Draw")

    # print(game)

    print("Game time: " + str(time.time() - start_time))
    print("Nbr Moves: " + str(game.move_count()))
    print("white: " + str(white))
    print("black: " + str(black))
    print("draw: " + str(draw))

#     history = game.history()
#     results = [winner] * len(history)
#     heuristic.train(history, results, game.nbr_epochs())
#
# heuristic.save()
