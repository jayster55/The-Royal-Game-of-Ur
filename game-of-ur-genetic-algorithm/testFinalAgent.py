import math
import sys
from agent import Piece
from playUr_RvG import playGameRandom

# global constant
AGENT_DIR = "agentFiles/" # directory for agent files
DEBUG = False
ROUND_DIGIT = 3

def playRandom(finalAgent):
    NUM_GAMES = 5000

    gamesWon = 0 # init

    for x in range(NUM_GAMES):
        if x % 2 == 0:
            colour = Piece.White
        else:
            colour = Piece.Black
        blackWon = playGameRandom(colour, finalAgent, 1, DEBUG)

        if (colour == Piece.Black and blackWon) or (colour == Piece.White and not blackWon):
            gamesWon += 1

    print("Winrate of the final agent against random agent over " + str(NUM_GAMES) + " games is " + str(round(gamesWon / NUM_GAMES * 100, ROUND_DIGIT)) + "%")

def main():
    finalAgentFile = sys.argv[1]
    with open(finalAgentFile, 'r') as f:
        finalAgent = [float(i) for i in f.read().splitlines()]

    print(finalAgent)
    playRandom(finalAgent)

if __name__ == "__main__":
    main()
