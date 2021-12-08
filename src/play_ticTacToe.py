import argparse

from player import *
from state import *
from config import *


parser = argparse.ArgumentParser(description='Team Project - TicTocToe')
parser.add_argument('--train', '-t', required=False, type=int, default=1,
                    help='If training is needed train 1, test 0')
parser.add_argument('--train-epochs', '-e', required=False, type=int, default=100,
                    help='Number of times to train the agent ') 
parser.add_argument('--learning-rate', '-lr', required=False, type=float, default=0.2,
                    help='Learning rate to train the agent ')  
parser.add_argument('--exp-rate', '-er', required=False, type=float, default=0.0,
                    help='Exponential rate to train the agent ')
parser.add_argument('--decay-rate', '-dr', required=False, type=float, default=0.9,
                    help='Decay rate to train the agent ')    
parser.add_argument('--grid-size', '-gs', required=False, type=int, default=3,
                    help='Grid size; 3 for a 3x3 ; 4 for a 4x4 grid')      
parser.add_argument('--win-reward-p1', '-rp1', required=False, type=float, default=1.0,
                    help='Win reward for computer ') 
parser.add_argument('--win-reward-p2', '-rp2', required=False, type=float, default=0.0,
                    help='Win reward for Human ') 
parser.add_argument('--stats-mode', '-sm', required=False, type=int, default=0,
                    help='Enabling Stats mode does not print the board messages in the logs')
parser.add_argument('--policy-p1', '-p1', required=False, type=str, default='policy_p1',
                    help='Policy file path for the computer/agent to use')
parser.add_argument('--start-player', '-sp', required=False, type=str, default=None,
                    help='Start player; computer or human, default -random')
                                        
args = parser.parse_args()


if __name__ == "__main__":
	config = Config (args)
	# training
	p1 = Player("p1", config=config)
	p2 = Player("p2", config=config)

	st = State(p1, p2, config=config)
	if args.train == 1:
		print("Training started...")
		st.play()
		p1.savePolicy()
		p2.savePolicy()
		print ('\n\t Training Done ! \n')
	
	print("\nTesting...")
	# play with human
	p1 = Player("Computer", config=config)
	p1.loadPolicy(args.policy_p1)

	p2 = HumanPlayer("Human")

	st = State(p1, p2, config=config)
	st.play2()
