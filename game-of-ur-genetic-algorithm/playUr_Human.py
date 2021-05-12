import sys
import math
from random import randint
from enum import IntEnum
from copy import deepcopy
# Local Imports
from agent import *
from winGame import *

DEBUG = False

def playGame(genes, gamesToPlay, debug):

    win = False
    blackWon = False
    whiteWon = False
    board = []

    whiteTeam = Agent(genes, 'w')

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
                print("Rolled a zero: Active player loses turn.")
                continue

            # play Turn
            if isBlackTurn: # player's turn
                print("Player's turn, die roll is: " + str(state[3]))
                playerState = whiteTeam.readNextState()
                print("Player moved:")
                whiteTeam.prettyPrintState(playerState)
                extraTurn = False
                state = playerState if playerState is not None else state # handle cases where no moves are available
            else: # white's turn
                whiteMove, extraTurn = whiteTeam.playTurn(state, debug)
                print("White AI rolled " + str(state[3]) + " and moved:")
                whiteTeam.prettyPrintState(whiteMove)
                if extraTurn:
                    print("White earned an extra move.")
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
                print("Player Won Game! #" + str(gameIndex))
            else: #whiiteWon
                print("White Genetic Agent Won Game #" + str(gameIndex))

    return blackWon # return True if black won, and False if White won
        

def rollDie():
    #helper to generate a game of ur die roll
    dieRoll = 0
    for index in range(0, 4):
        dieRoll += randint(0, 1)

    return dieRoll



def main():

    agentFile = sys.argv[1]
    with open(agentFile) as f:
        genes = f.read().splitlines()

    playGame(genes, 1, False)

main()
