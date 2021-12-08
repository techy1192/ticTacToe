import argparse

from player import *
from state import *
from config import *


parser = argparse.ArgumentParser(description='Team Project - TicTocToe')
parser.add_argument('--train', '-t', required=False, type=int, default=1,
                    help='If training is needed train 1, test 0')
parser.add_argument('--train-epochs', '-e', required=False, type=int, default=100,
                    help='Number of times to train the agent ') 
parser.add_argument('--test-epochs', '-te', required=False, type=int, default=100,
                    help='Number of times to test the agent ')                     
parser.add_argument('--learning-rate', '-lr', required=False, type=float, default=0.2,
                    help='Learning rate to train the agent ')  
parser.add_argument('--exp-rate', '-er', required=False, type=float, default=0.0,
                    help='Exponential rate to train the agent ')
parser.add_argument('--decay-rate', '-dr', required=False, type=float, default=0.9,
                    help='Decay rate to train the agent ')    
parser.add_argument('--grid-size', '-gs', required=False, type=int, default=3,
                    help='Grid size; 3 for a 3x3 grid')      
parser.add_argument('--win-reward-p1', '-rp1', required=False, type=float, default=1.0,
                    help='Win reward for computer ') 
parser.add_argument('--win-reward-p2', '-rp2', required=False, type=float, default=0.0,
                    help='Win reward for computer ') 
parser.add_argument('--stats-mode', '-sm', required=False, type=int, default=0,
                    help='Enabling Stats mode does not print the board messages in the logs') 
parser.add_argument('--start-player', '-sp', required=False, type=str, default=None,
                    help='Start player; computer or human, default -random')                    
                                                                                                                
args = parser.parse_args()


def do_testing (st, test_epochs):
	print("Testing...")
	win_count = 0
	for i in range (test_epochs):
		status = st.play2()
		if status == 1:
			win_count += 1
			
	print ('\n\nPlayer 1 won %d/%d '%(win_count/test_epochs))
	

if __name__ == "__main__":
	config = Config (args)
	# training
	p1 = Player("p1", config=config)
	p2 = Player("p2", config=config)

	st = State(p1, p2, config=config)
	if args.train == 1:
		print("Training...")
		st.play()
		p1.savePolicy()
		p2.savePolicy()
	#do_testing (st, args.test_epochs)
	print("Testing...")
	win_count = 0
	tie_count = 0
	start_player_count = 0
	for i in range (args.test_epochs):
		#print ('epoch : %d , %d'%(i, win_count))
		win, start_player = st.play2()
		if win == 1:
			win_count += 1
		elif win == 0:
			tie_count += 1
			
		if start_player == 1:
			start_player_count += 1
				
	print ('\n')
	print ('-'*80)
	print ('\t\t\t\t\t STATS')
	print ('-'*80)	
	print ('\n\n\t\tPlayer 1 started the match \t: %d/%d '%(start_player_count, args.test_epochs))
	print ('\t\tPlayer 2 started the match \t: %d/%d '%(args.test_epochs - start_player_count, args.test_epochs))
	print ('\n\n\t\tPlayer 1 won \t\t\t: %d/%d '%(win_count, args.test_epochs))
	print ('\t\tPlayer 2 won \t\t\t: %d/%d '%(args.test_epochs-win_count-tie_count, args.test_epochs))
	print ('\t\tTie\t\t\t\t: %d/%d '%(tie_count, args.test_epochs))
	print ()
	print ('-'*80)				
