import time
from src.Chess.ChessState import ChessState
from src.Chess import ChessValidation
from src.FirstLayerActionModel import FirstLayerActionModel
from src.GamePlayer import GamePlayer
from src.NnHeuristic import NnHeuristic


def test_heuristic(nnHeuristic: NnHeuristic):
    tests = ChessValidation.load_tests("Stockfish/tests.txt")
    avg_loss = nnHeuristic.test(tests[0], tests[1])
    print("--- Tests - average loss:" + str(avg_loss) + " ---")


heuristic = NnHeuristic("./models/keras_model_1024", ChessState.input_shape())
actionModel = FirstLayerActionModel(heuristic)
player = GamePlayer(actionModel)

white = 0
black = 0
draw = 0

test_heuristic(heuristic)
for i in range(2000):
    print("iteration: " + str(i + 1))

    start_time = time.time()
    game = ChessState()
    winner = player.play(game)

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
    print("white: " + str(white))
    print("black: " + str(black))
    print("draw: " + str(draw))

    history = game.history()
    results = [winner] * len(history)
    heuristic.train(history, results, game.nbr_epochs())

    if i % 100 == 0:
        test_heuristic(heuristic)
        heuristic.save()

test_heuristic(heuristic)
heuristic.save()

# Ai for heuristic (Détermine si un état du jeu est gagnants pour white)
# Réseau de neuronne génétique -> On garde les gagnant et on les mute
# Réseau de neuronne par gradient -> Pour le réseau gagnant, on renforce ses évaluation d'états (Si blanc à gagné on renforce ses états, si noir a gagné, on punis ses états) (punire = favoriser noir)

# Ai for time management
# Ai for exploration (on fait une évaluation chaque état avec l'heuristique et on arrête d'explorer les nodes trop mauvaises)
# Or Montecarlo modified for exploration where a good evaluation is a win
