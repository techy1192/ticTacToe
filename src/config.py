
class Config:
    def __init__(self, args):
        self.grid_size = args.grid_size
        self.epochs = args.train_epochs
        self.lr= args.learning_rate
        self.exp_rate= args.exp_rate
        self.decay_rate = args.decay_rate
        self.win_reward_p1 = args.win_reward_p1
        self.win_reward_p2 = args.win_reward_p2
        self.stats_mode = args.stats_mode
        self.start_player = args.start_player
        #print ('In config : ', self.grid_size, self.epochs )
