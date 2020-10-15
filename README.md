# Yara Zero
**Y**et **A**nother **R**einforcement learning **A**i for turn based games!

Yara learns to play the game from scratch by playing againts herself.
She currently uses a neural network as a heuristic to evaluate the quality of a position and uses MiniMax or MCST as the tree traversal algorithm. 
While Yara is currently able to learn and play simple games like checkers really well, more complex games like chess would greatly benefit from an improved neural network model that would recommend the best actions for a given state to enhance the quality of her tree traversal.

### Getting Started
`Yara.py <path_to_config.json>` see [template](./src/Yara_config.template.json)

#### Train (optional)  
   * model: Path to the model to be trained  
   * gamesPerTrain: Number of games played in between training of the model.

#### Action Models (required)
At least 1 action model must be specified. Player 1 will use the first action model, player 2 the second and so on. 
If there are more players than specified action models, it will loop back.
* **MiniMax**  
Your classic* MiniMax. (not using alpha beta pruning because evaluating all states in a batch is a lot quicker)  
params:
    * depth: max depth
    * model: path to the trained Yara model to be used as a heuristic

* **Monte Carlo Search Tree**  
[see](https://en.wikipedia.org/wiki/Monte_Carlo_tree_search)  
params:
    * nbr_rollouts: nomber of rollouts calculated each turn
    * exploration_weight: how much it will explore instead of beeing greedy
    * model: path to the trained Yara model to be used as a heuristic
* **Human**  
If you want to try your luck, this is it!
* **Random**

* **FirstLayer**  
    Is MiniMax with max depth of 1  
    params
    * variance: If set to to true, the action will be randomely selected proportionally to the evaluated chances of winning else, it will always select the action that leads to the best state. 
    * model: path to the trained Yara model to be used as a heuristic

#### Dependencies
[Pyton-Chess](https://python-chess.readthedocs.io/en/latest/)
