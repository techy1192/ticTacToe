import numpy as np
import random

class State:
    def __init__(self, p1, p2, config):
        #print ('---- : ', config.grid_size)
        self.grid_size = config.grid_size
        self.epochs = config.epochs
        self.stats_mode = config.stats_mode
        self.win_reward_p1 = config.win_reward_p1
        self.win_reward_p2 = config.win_reward_p2
        self.start_player  = config.start_player 
        self.grid = np.zeros((self.grid_size, self.grid_size))
        self.p1 = p1
        self.p2 = p2
        self.isEnd = False
        self.gridHash = None
        # init p1 plays first
        self.playerSymbol = 1

    # get unique hash of current grid state
    def getHash(self):
        self.gridHash = str(self.grid.reshape(self.grid_size * self.grid_size))
        return self.gridHash

    def winner(self):
        # row
        for i in range(self.grid_size):
            if sum(self.grid[i, :]) == self.grid_size:
                self.isEnd = True
                return 1
            if sum(self.grid[i, :]) == -self.grid_size:
                self.isEnd = True
                return -1
        # col
        for i in range(self.grid_size):
            if sum(self.grid[:, i]) == self.grid_size:
                self.isEnd = True
                return 1
            if sum(self.grid[:, i]) == -self.grid_size:
                self.isEnd = True
                return -1
        # diagonal
        diag_sum1 = sum([self.grid[i, i] for i in range(self.grid_size)])
        diag_sum2 = sum([self.grid[i, self.grid_size - i - 1] for i in range(self.grid_size)])
        #print ( 'dia : ', diag_sum1, diag_sum2)
        diag_sum = max(abs(diag_sum1), abs(diag_sum2))
        if diag_sum == self.grid_size:
            self.isEnd = True
            if diag_sum1 == self.grid_size or diag_sum2 == self.grid_size:
                return 1
            else:
                return -1

        # tie or no available positions
        if len(self.availablePositions()) == 0:
            self.isEnd = True
            return 0
        # not end
        self.isEnd = False
        return None

    def availablePositions(self):
        positions = []
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.grid[i, j] == 0:
                    positions.append((i, j))  # need to be tuple
        return positions

    def updateState(self, position):
        self.grid[position] = self.playerSymbol
        # switch to another player
        self.playerSymbol = -1 if self.playerSymbol == 1 else 1

    # only when game ends
    def giveReward(self):
        result = self.winner()
        # backpropagate reward
        if result == 1:
            self.p1.feedbackReward(self.win_reward_p1)
            self.p2.feedbackReward(1-self.win_reward_p1)
        elif result == -1:
            self.p1.feedbackReward(1-self.win_reward_p2)
            self.p2.feedbackReward(self.win_reward_p2)
        else:
            self.p1.feedbackReward(-0.1)
            self.p2.feedbackReward(0.5)

    # grid reset
    def reset(self):
        self.grid = np.zeros((self.grid_size, self.grid_size))
        self.gridHash = None
        self.isEnd = False
        self.playerSymbol = 1

    def play(self):
        for i in range(self.epochs):
            if i % 1000 == 0:
                print("Epochs {}".format(i))
            while not self.isEnd:
                # Player 1
                positions = self.availablePositions()
                p1_action = self.p1.chooseAction(positions, self.grid, self.playerSymbol)
                # take action and upate grid state
                self.updateState(p1_action)
                grid_hash = self.getHash()
                self.p1.addState(grid_hash)
                # check grid status if it is end

                win = self.winner()
                if win is not None:
                    # self.showGrid()
                    # ended with p1 either win or draw
                    self.giveReward()
                    self.p1.reset()
                    self.p2.reset()
                    self.reset()
                    break

                else:
                    # Player 2
                    positions = self.availablePositions()
                    p2_action = self.p2.chooseAction(positions, self.grid, self.playerSymbol)
                    self.updateState(p2_action)
                    grid_hash = self.getHash()
                    self.p2.addState(grid_hash)

                    win = self.winner()
                    if win is not None:
                        # self.showGrid()
                        # ended with p2 either win or draw
                        self.giveReward()
                        self.p1.reset()
                        self.p2.reset()
                        self.reset()
                        break

    def make_action (self, player, win_status):
            if not self.stats_mode:
                if win_status == 1:
                    print ('\nComputer made the move, current board status -->> ')
                else:
                    print ('\nIt is your turn -->>')
            positions = self.availablePositions()
            player_action = player.chooseAction(positions, self.grid, self.playerSymbol)
            # take action and upate grid state
            self.updateState(player_action)
            if not self.stats_mode:
               self.showGrid()
            # check grid status if it is end
            win = self.winner()
            status = 0
            if win is not None:
                if win == win_status:
                    if not self.stats_mode:
                        print ('\n', '-'*80, '\n')
                        print(player.name, " is the WINNER!!")
                        print ('\n', '-'*80)
                    if win_status == 1:
                       status = 1
                    else :
                       status = 2
                else:
                    status = 0
                    if not self.stats_mode:
                       print ('\n', '-'*80, '\n')
                       print("\t\tIt is a TIE! Play again to win! ", win )
                       print ('\n', '-'*80)
                self.reset()
                
            return win, status
                
    # play with human
    def play2(self):
        if self.start_player == 'computer':
            start_player = 1
        elif self.start_player == 'human':
            start_player = 2
        else:
            start_player = random.choice([1,2])
            
        if not self.stats_mode:
            print ('Computer uses letter\t=> \'x\'')
            print ('You use the letter\t=> \'o\'')
        if start_player == 1:
            self.playerSymbol = 1
            if not self.stats_mode:
                print ('\nComputer started the match!')
        else:
            self.playerSymbol = -1
            if not self.stats_mode:
                print ('\nYou started the match!')
                
        while not self.isEnd:
            if start_player == 1:
                # Player 1
                win, status = self.make_action (self.p1, 1)
                if win is not None:
                   return status, start_player
                else:
                   # Player 2
                   win, status = self.make_action (self.p2, -1)
                   if win is not None:
                      return status, start_player
            else:
                # Player 2
                win, status = self.make_action (self.p2, -1)
                if win is not None:
                   return status, start_player
                else:
                   # Player 1
                   win, status = self.make_action (self.p1, 1)
                   if win is not None:
                      return status, start_player       
        return 0 , 0          

    def showGrid(self):
        # p1: x  p2: o
        for i in range(0, self.grid_size):
            divider = (self.grid_size * '----') + '-'
            print(divider)
            out = '| '
            for j in range(0, self.grid_size):
                if self.grid[i, j] == 1:
                    token = 'x'
                if self.grid[i, j] == -1:
                    token = 'o'		    # Player 2
                if self.grid[i, j] == 0:
                    token = ' '
                out += token + ' | '
            print(out)
        print(divider)
        
