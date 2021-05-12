import sys
import math
from enum import IntEnum
from copy import deepcopy
from random import randint
# Local Imports
from randomagent import RandomAgent
from agent import Agent
from winGame import *

DEBUG = False

def playGameRandom(colour, genes, gamesToPlay, debug):

    win = False
    blackWon = False
    whiteWon = False
    agentColour = ""

    if colour == Piece.Black:
        blackTeam = Agent(genes, 'b')
        whiteTeam = RandomAgent(Piece.White)
        agentColor = "Black"
    else:
        whiteTeam = Agent(genes, 'w')
        blackTeam = RandomAgent(Piece.Black)
        agentColor = "White"

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

            # blackTeam.prettyPrintState(state)

            # check if last turn finished the game
            if winGame(state):
                blackWon = True if isBlackTurn else False
                win = True
                break
            else: # game not yet over
                isBlackTurn = not isBlackTurn if not extraTurn else isBlackTurn # swap turns if extraturn == False, grant extra turn if extraTurn == True
        
        #for sake of fairness, swap agents after each game
        # temp = whiteTeam
        # whiteTeam = blackTeam
        # blackTeam = temp

        if DEBUG: # debug print
            # if blackWon:
            #     print("Black Genetic Agent Won Game " + str(gameIndex))
            # else: #whiiteWon
            #     print("White Genetic Agent Won Game " + str(gameIndex))


            if (blackWon and agentColour == "Black") or (whiteWon and agentColour == "White"):
                print("Genetic Agent Won Game " + str(gameIndex)) 
            else:
                print("Random Agent Won Game " + str(gameIndex)) 

            return blackWon

    return blackWon # return True if black won, and False if White won
        

def rollDie():
    #helper to generate a game of ur die roll
    dieRoll = 0
    for index in range(0, 4):
        dieRoll += randint(0, 1)

    return dieRoll
