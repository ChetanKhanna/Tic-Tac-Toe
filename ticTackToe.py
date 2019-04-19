'''
Roadmap: 1. Build a game where computer randomly makes moves
		 2. Use min-max algo for deciding next move
'''

## Importing required modules
import graph
import random
import os
import copy
from math import inf
from pprint import pprint

board = [
	[None, None, None],
	[None, None, None],
	[None, None, None]
]
HUMAN = 1
COMPUTER = -1
cell_to_pos = {
	1:[0,0], 2:[0,1], 3:[0,2],
	4:[1,0], 5:[1,1], 6:[1,2],
	7:[2,0], 8:[2,1], 9:[2,2]
}

def buildGraph():
	'''
	builds a graph structure for the game
	param: None
	return: A graph object for tic-tac-toe
	'''
	pass

class stateObject:
	"""docstring for stateObject"""
	def __init__(self, state):
		self.state = board
		self.val = None
		self.parent = None
		self.role = None # Maximizer or Minimizer
		

def isWinState(state, player):
	'''
	checks if current state of board is a winning config
	A winning config is when either of three cols or three
	rows or two diagonals have the same player enteries
	'''
	curr_state = state.state
	win_states = [
	[curr_state[0][0], curr_state[0][1], curr_state[0][2]],
	[curr_state[1][0], curr_state[1][1], curr_state[1][2]],
	[curr_state[2][0], curr_state[2][1], curr_state[2][2]],
	[curr_state[0][0], curr_state[1][0], curr_state[2][0]],
	[curr_state[0][1], curr_state[1][1], curr_state[2][1]],
	[curr_state[0][2], curr_state[1][2], curr_state[2][2]],
	[curr_state[0][0], curr_state[1][1], curr_state[2][2]],
	[curr_state[0][2], curr_state[1][1], curr_state[2][0]]
	]

	if [player, player, player] in win_states:
		return True
	else:
		return False

def isDrawState(state):
	for row in state.state:
		if None in row:
			return False
	return True

def declareWinner(player):
	if player == HUMAN:
		print('Congrats! You Won.')
	else:
		print('You lost.')

def displayBoard(state):
	for row in state.state:
		pprint(row)

def isValidMove(state, cell):
	r, c = cell_to_pos[cell]
	if not state.state[r][c]:
		return True
	else:
		return False

def getEmptyCells(state):
	empty_cells = []
	for i in range(1,10):
		r, c = cell_to_pos[i]
		if not state.state[r][c]:
			empty_cells.append(i)
	return empty_cells

def updateMoveOnBoard(state, player, move):
	r, c = cell_to_pos[move]
	state.state[r][c] = player

def aiMove(state, searchMethod = None):
	if not searchMethod:
		randomValidMove(state)
	elif searchMethod == 'min-max':
		minmax(state, COMPUTER)

def randomValidMove(state):
	# Randomly generates a valid move.
	empty_cells = getEmptyCells(state)
	move = random.choice(empty_cells)
	updateMoveOnBoard(state, COMPUTER, move)

def getSuccessors(state,player):
	# generates a list of successors -- possible moves for the 
	# "player" from the given state
	empty_cells = getEmptyCells(state)
	successors = []
	temp_state = copy.deepcopy(state)
	for cell in empty_cells:
		updateMoveOnBoard(temp_state, player, cell)
		successors.append(temp_state)
		temp_state = copy.deepcopy(state)
	return successors

def isLeafNode(state):
	# Checks if node is a leaf node -- is either there is a win, loss or draw
	# situation in the node, the node is a leaf node.
	curr_state = state.state
	win_states = [
	[curr_state[0][0], curr_state[0][1], curr_state[0][2]],
	[curr_state[1][0], curr_state[1][1], curr_state[1][2]],
	[curr_state[2][0], curr_state[2][1], curr_state[2][2]],
	[curr_state[0][0], curr_state[1][0], curr_state[2][0]],
	[curr_state[0][1], curr_state[1][1], curr_state[2][1]],
	[curr_state[0][2], curr_state[1][2], curr_state[2][2]],
	[curr_state[0][0], curr_state[1][1], curr_state[2][2]],
	[curr_state[0][2], curr_state[1][1], curr_state[2][0]]
	]

	if [1,1,1] in win_states:
		return True
	if [-1,-1,-1] in win_states:
		return True
	if isDrawState(state):
		return True
	return False

def evaluate(state):
	## Evaluates wheather leaf node is a Win, Loss or Draw for Human player
	curr_state = state.state
	win_states = [
	[curr_state[0][0], curr_state[0][1], curr_state[0][2]],
	[curr_state[1][0], curr_state[1][1], curr_state[1][2]],
	[curr_state[2][0], curr_state[2][1], curr_state[2][2]],
	[curr_state[0][0], curr_state[1][0], curr_state[2][0]],
	[curr_state[0][1], curr_state[1][1], curr_state[2][1]],
	[curr_state[0][2], curr_state[1][2], curr_state[2][2]],
	[curr_state[0][0], curr_state[1][1], curr_state[2][2]],
	[curr_state[0][2], curr_state[1][1], curr_state[2][0]]
	]
	if [1,1,1] in win_states:
		return 1
	elif [-1,-1,-1] in win_states:
		return -1
	else:
		return 0

def minmax(state, player):
	"Using Depth-First Search and applying min-max"
	min_val = inf # Initialinzing worst val for AI player (minimizer)
	for s in getSuccessors(state, player):
		value = minmaxUtil(s, player*(-1))
		if min_val > value:
			best_move = s
			min_val = value
	for i in range(3):
		for j in range(3):
			state.state[i][j] = best_move.state[i][j]

def minmaxUtil(state, player):
	if isLeafNode(state):
		# if current state is leaf node, we evaluate it - (1, 0 or -1)
		# and return the control to parent node, whose value gets updated accordingly
		return evaluate(state)
	best = -player*inf
	for s in getSuccessors(state, player):
		value = minmaxUtil(s, player*(-1))
		if player == HUMAN: ## MaxPlayer
			if value > best:
				best = value
		else:
			if value < best:
				best = value
	return best

def play(state, player):
	'''
	Main function for running the game.
	'''
	global board
	if player == HUMAN:
		# If player is HUMAN, take input from user (1-9) and display
		# the board with updated move.
		os.system('clear')
		print('Your Turn')
		displayBoard(state)
		move = -1
		while move < 1 or move > 9:
			move = int(input('Select cell 1:9: '))
			if not isValidMove(state, move):
				print('Move invalid! Try again.')
				move = -1
		updateMoveOnBoard(state, player, move)
	else:
		aiMove(state, searchMethod = 'min-max')
	## Checking for win or draw state
	if isWinState(state, player):
		displayBoard(state)
		declareWinner(player)
		return True
	elif isDrawState(state):
		print('Match Tied!')
		displayBoard(state)
		return True
	else:
		return False

def main():
	'''
	Controller function for the game.
	'''
	global board
	done = False
	player = HUMAN
	state = stateObject(board)
	while not done:
		done = play(state, player)
		player *= -1 ## Changing player 

if __name__ == '__main__':
	main()
