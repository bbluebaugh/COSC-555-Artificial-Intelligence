#!/usr/bin/env python
#Version: 1.0.0		Author: Brian Bluebaugh		Date: 3/5/19

import random
from sys import stdin

#class for setting up the game parameters
class Tic(object):
	#All of the possible winning combinations i.e. first row, second row, etc....
    winning_combos = (
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6])

    winners = ('X-win', 'Draw', 'O-win')
    #initialize Board State
    def __init__(self, squares=[]):
        if len(squares) == 0:
            self.squares = [None for i in range(9)]
        else:
            self.squares = squares

    #Display the current board iterate through every position for info about it
	#Takes itself as a parameter and displays elements as seen in the board
    def show(self):
        for element in [self.squares[i:i + 3] for i in range(0, len(self.squares), 3)]:
            print(element)

    #need a function for retrieving available moves
	#in this case all the empty spaces left
	#takes in the board as a parameter and determines the empty spaces
    def available_moves(self):
        """what spots are left empty?"""
        return [k for k, v in enumerate(self.squares) if v is None]

    #also need a function for the moves not taken b the opponent
    def available_combos(self, player):
        """what combos are available?"""
        return self.available_moves() + self.get_squares(player)

    #Takes the board in as a parameter
	#if the board is filled or there is a winner return true
	#otherwise return false
    def complete(self):
        """is the game over?"""
        if None not in [v for v in self.squares]:
            return True
        if self.winner() != None:
            return True
        return False

    #takes the board as a parameter and checks to see if the Crosses (X) won
    def X_won(self):
        return self.winner() == 'X'
	#takes the board in as a parameter and checks to see if Noughts (O) won
    def O_won(self):
        return self.winner() == 'O'
	#takes the board as a parameter, and checks to see if the game is over
	#i.e the board is filled and no one has won
    def tied(self):
        return self.complete() == True and self.winner() is None
	
	#The winning function to determine which player is the winner at the current state
	#if there is one
	#takes the board in as a parameter and checks through the winning states
	#i.e. winning_States
    def winner(self):
        for player in ('X', 'O'):
            positions = self.get_squares(player)
            for combo in self.winning_combos:
                win = True
                for pos in combo:
                    if pos not in positions:
                        win = False
                if win:
                    return player
        return None

	#need a function for telling where a player either X or O has gone
	#i.e which positions has this player already taken up
	#takes in the board and the player you are looking for to determine already take positions
    def get_squares(self, player):
        """squares that belong to a player"""
        return [k for k, v in enumerate(self.squares) if v == player]

	#need a function for making moves
	#takes in the board as a parameter the position for where you want to move
	#and the player so it can determine which player is moving
	#basically find the position and input the player into that position
    def make_move(self, position, player):
        """place on square on the board"""
        self.squares[position] = player

	#Alpha-Beta pruning
	#starts and works very similar to minimax but better performance
    def alphabeta(self, node, player, alpha, beta):
        if node.complete():
            if node.X_won():
                return -1
            elif node.tied():
                return 0
            elif node.O_won():
                return 1
        for move in node.available_moves():
            node.make_move(move, player)
            val = self.alphabeta(node, get_enemy(player), alpha, beta)
            node.make_move(move, None)
            if player == 'O':
                if val > alpha:
                    alpha = val
                if alpha >= beta:
                    return beta
            else:
                if val < beta:
                    beta = val
                if beta <= alpha:
                    return alpha
        if player == 'O':
            return alpha
        else:
            return beta

#wrapper calls the algorithm for different positions to choose the best move
#iterate through possible moves and keep track of best one and return that one
def determine(board, player):
    a = -2
    choices = []
    if len(board.available_moves()) == 9:
        return 4
    for move in board.available_moves():
        board.make_move(move, player)
        val = board.alphabeta(board, get_enemy(player), -2, 2)
        board.make_move(move, None)
        print("move:", move + 1, "causes:", board.winners[val + 1])
        if val > a:
            a = val
            choices = [move]
        elif val == a:
            choices.append(move)
    return random.choice(choices)

#gets the opponent player so that we can know which player is which
#if the enemy is X then return O otherwise X
def get_enemy(player):
    if player == 'X':
        return 'O'
    return 'X'

if __name__ == "__main__":
    #board = Tic()
    #board.show()
    print("How to play: \n")
    print("input numbers 0-8 to make your move. \n")
    print("0-2 is the top row. \n")
    print("3-5 is the second and so on. \n")
    print("After the game has concluded you will be asked to play again.")
    print("To play again type 'yes' otherwise type anything else and the game will end.")
    play = True
    while play == True:

	    board = Tic()
	    board.show()
	    while not board.complete():
	        player = 'X'
	        player_move = int(input("Next Move: "))
	        if not player_move in board.available_moves():
	            continue
	        board.make_move(player_move, player)
	        board.show()

	        if board.complete():
	            break
	        player = get_enemy(player)
	        computer_move = determine(board, player)
	        board.make_move(computer_move, player)
	        board.show()
	    print("winner is", board.winner())
	    play_again = input("Would you like to play again?")
	    if play_again == "yes":
	    	play = True
	    else:
	    	break