import numpy as np
import pickle

class Player:
    def __init__(self, name, config):
        #print ('---- : ', config.lr)
        self.name = name
        self.states = []  # record all positions taken
        self.grid_size = config.grid_size
        self.lr = config.lr
        self.exp_rate = config.exp_rate
        self.decay_rate = config.decay_rate
        self.states_value = {}  # state -> value

    def getHash(self, grid):
        gridHash = str(grid.reshape(self.grid_size * self.grid_size))
        return gridHash

    def chooseAction(self, positions, current_grid, symbol):
        if np.random.uniform(0, 1) <= self.exp_rate:
            # take random action
            idx = np.random.choice(len(positions))
            action = positions[idx]
        else:
            value_max = -999999
            for p in positions:
                next_grid = current_grid.copy()
                next_grid[p] = symbol
                next_gridHash = self.getHash(next_grid)
                value = 0 if self.states_value.get(next_gridHash) is None else self.states_value.get(next_gridHash)
                # print("value", value)
                if value >= value_max:
                    value_max = value
                    action = p
        # print("{} takes action {}".format(self.name, action))
        return action

    # append a hash state
    def addState(self, state):
        self.states.append(state)

    # at the end of game, backpropagate and update states value
    def feedbackReward(self, reward):
        for st in reversed(self.states):
            if self.states_value.get(st) is None:
                self.states_value[st] = 0
            self.states_value[st] += self.lr * (self.decay_rate * reward - self.states_value[st])
            reward = self.states_value[st]

    def reset(self):
        self.states = []

    def savePolicy(self):
        fw = open('policy_' + str(self.name), 'wb')
        pickle.dump(self.states_value, fw)
        fw.close()

    def loadPolicy(self, file):
        fr = open(file, 'rb')
        self.states_value = pickle.load(fr)
        fr.close()


class HumanPlayer:
    def __init__(self, name):
        self.name = name

    def chooseAction(self, positions, current_grid=None, symbol=None):
        while True:
            row = int(input("Input your action grid row:"))
            col = int(input("Input your action grid col:"))
            action = (row, col)
            if action in positions:
                return action
                
                
