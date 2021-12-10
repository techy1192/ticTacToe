# ticTacToe
TicTacToe game using Reinforcement Learning


Prerequisites to run the project
python3*


There are two ways to execute this project

1. Run from the command line
2. Run using jupyter notebook

## **1. Run from the command line**

The game has two phases
1. Training
2. Playing

play_ticTacToe.py is the main file to train and test the game. config.py, player.py, state.py have helper functions. stats.py is to generate statistics of the game.

The follwoing steps describe how to train the model and test

### 1. Training
```python
$ cd src
$ python3 play_ticTacToe.py -train 1 --train-epochs 50000 --learning-rate 0.2 --start-player computer --grid-size 3 --win-reward-p1 1.0
```		

all these arguments are optional and you can modify them based on your need.
Once the training is done, the models policlies are saved into policy files.
policy_p1 for player 1,
policy_p2 for player 2,

### 2. Testing
```python
$ python3 play_ticTacToe.py -train 0 --start-player human --policy-p1 policies/policy_p1
```
the argument train should be set 1 to train the model & 0 to test.


## **2. Run using jupyter notebook**

open the jupyer notebook file *ticTacToe_RL.ipynb* in the browser and run.
you can adjust the training parameters in Config class or using Config class object 


## **Stats Generation**

Run *stats.py* or *ticTacToe_stats_generation.ipynb* for stats generation

```
$ python3 stats.py -sm 1 -p1 policy_p1 -p2 policy_p2 --test-epochs 100
```


