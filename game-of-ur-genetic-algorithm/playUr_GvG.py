import sys
import math
from random import randint
from enum import IntEnum
from copy import deepcopy
# Local Imports
from agent import *
from winGame import *

DEBUG = False

def playGame(colourToPlay1, genes1, colourToPlay2, genes2, gamesToPlay, debug):

    win = False
    blackWon = False
    whiteWon = False
    board = []

    if colourToPlay1 == Piece.Black:
        blackTeam = Agent(genes1, colourToPlay1)
        whiteTeam = Agent(genes2, colourToPlay2)
    else:
        whiteTeam = Agent(genes1, colourToPlay1)
        blackTeam = Agent(genes2, colourToPlay2)

    for gameIndex in range(0, gamesToPlay):
        #initialize empty board
        state = [[0] * 20, 7, 7, 0]
        isBlackTurn = True # True if it's black's turn, False otherwise

        while not win:
            #roll the die and return the move
            #it's possible to have no moves, in this case
            #return the current state so as to not take a turn
            state[3] = rollDie()
            if(state[3] == 0):
                isBlackTurn = not isBlackTurn # skip turn if die roll is 0
                continue

            # play Turn
            if isBlackTurn: # black's turn
                blackMove, extraTurn = blackTeam.playTurn(state, debug)
                state = blackMove if blackMove is not None else state # handle cases where no moves are available
            else: # white's turn
                whiteMove, extraTurn = whiteTeam.playTurn(state, debug)
                state = whiteMove if whiteMove is not None else state

            # check if last turn finished the game
            if winGame(state):
                blackWon = True if isBlackTurn else False
                win = True
                break
            else: # game not yet over
                isBlackTurn = not isBlackTurn if not extraTurn else isBlackTurn # swap turns if extraturn == False, grant extra turn if extraTurn == True
        
        #for sake of fairness, swap agents after each game
        temp = whiteTeam
        whiteTeam = blackTeam
        blackTeam = temp

        if DEBUG: # debug print
            if blackWon:
                print("Black Genetic Agent Won Game " + str(gameIndex))
            else: #whiiteWon
                print("White Genetic Agent Won Game " + str(gameIndex))

    return blackWon # return True if black won, and False if White won
        

def rollDie():
    #helper to generate a game of ur die roll
    dieRoll = 0
    for index in range(0, 4):
        dieRoll += randint(0, 1)

    return dieRoll


# commented out main because command line args are no longer given to playUr_GvG

# def main():

#     # agentFile1 = sys.argv[1]
#     # colourToPlay1 = sys.argv[2]
#     # agentFile2 = sys.argv[3]
#     # colourToPlay2 = sys.argv[4]
#     # gamesToPlay = int(sys.argv[5])

#     # with open(agentFile1) as f:
#     #     genes1 = f.read().splitlines()

#     # with open(agentFile2) as f:
#     #     genes2 = f.read().splitlines()

#     # playGame(colourToPlay1, genes1, colourToPlay2, genes2, gamesToPlay, True)

# main()
