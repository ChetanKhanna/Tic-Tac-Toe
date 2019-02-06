'''
Roadmap: 1. Build a game where computer randomly makes moves
		 2. Use min-max algo for deciding next move
'''

## Importing required modules
import graph
import random
import os

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

def isWinState(state, player):
	'''
	checks if current state of board is a winning config
	A winning config is when either of three cols or three
	rows or two diagonals have the same player enteries
	'''
	win_states = [
		[state[0][0], state[0][1], state[0][2]],
		[state[1][0], state[1][1], state[1][2]],
		[state[2][0], state[2][1], state[2][2]],
		[state[0][0], state[1][0], state[2][0]],
		[state[0][1], state[1][1], state[2][1]],
		[state[0][2], state[1][2], state[2][2]],
		[state[0][0], state[1][1], state[2][2]],
		[state[1][2], state[1][1], state[2][0]]
	]
	if [player, player, player] in win_states:
		return True
	else:
		return False

def isDrawState(state):
	for row in state:
		if None in row:
			return False
	return True

def declareWinner(player):
	if player == HUMAN:
		print('Congrats! You Won.')
	else:
		print('You lost.')

def displayBoard(state):
	for row in state:
		print(row)

def isValidMove(state, cell):
	r, c = cell_to_pos[cell]
	if not state[r][c]:
		return True
	else:
		return False

def getEmptyCells(state):
	empty_cells = []
	for i in range(1,10):
		r, c = cell_to_pos[i]
		if not state[r][c]:
			empty_cells.append(i)
	return empty_cells

def updateMoveOnBoard(state, player, move):
	r, c = cell_to_pos[move]
	state[r][c] = player

def aiMove(state, searchMethod = None):
	if not searchMethod:
		randomValidMove(state)
	elif searchMethod == 'min-max':
		minmax(state, COMPUTER)

def randomValidMove(state):
	empty_cells = getEmptyCells(state)
	move = random.choice(empty_cells)
	updateMoveOnBoard(state, COMPUTER, move)

def getSuccessors(state):
	pass

def isLeafNode(state):
	pass

def evaluate(state):
	pass

def minmax(state, player):
	"Using Depth-First Search and applying min-max"
	fringe = {}
	for s in getSuccessors(state):
		fringe[s] = minmaxUtil(s, player*(-1))
	## Sort the dict by Values

def minmaxUtil(state, player):
	if isLeafNode(state):
		return evaluate(state)

	for s in getSuccessors(state):
		value = minmaxUtil(state, player*(-1))
		if player == HUMAN: ## MaxPlayer
			if value > state.value:
				state.value = value
		else:
			if value < state.value:
				state.value = value
	return state.value

def play(state, player):
	if player == HUMAN:
		os.system('clear')
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
	done = False
	player = random.choice([HUMAN, COMPUTER])
	while not done:
		done = play(board, player)
		player *= -1 ## Changing player 

if __name__ == '__main__':
	main()
