import math
import numpy as np
from playUr_GvG import playGame

# global constant
AGENT_DIR = "agentFiles/" # directory for agent files
NUM_GAMES_PER_PAIR = 10 # number of games played between each pair of agents
DEBUG = False
ROUND_DIGIT = 3

def printWinRate(agentList, agentWinRate): # prints out agent winrate
    if len(agentList) != len(agentWinRate):
        print("size of agentList and agentWinRate do not match")
        return

    for i in range(len(agentList)):
        print(agentList[i] + " winrate", end=': ')
        print(str(round(agentWinRate[i] * 100, ROUND_DIGIT)) + "%")

# main ---------------------------

def main():

    with open("agentList") as f:
        agentList = f.read().splitlines() # read agent filenames from "/agentList"

    agentWinCount = np.zeros(len(agentList)) # init wincount array
    agentPlayCount = np.zeros(len(agentList)) # init playcount array
    agentWinRate = np.zeros(len(agentList)) # init winrate array

    for indexA in range(len(agentList) - 1): # iterate
        for indexB in range(indexA + 1, len(agentList)):
            # open gene files
            with open(AGENT_DIR + agentList[indexA]) as f:
                genesA = f.read().splitlines()
            with open(AGENT_DIR + agentList[indexB]) as f:
                genesB = f.read().splitlines()

            for x in range(NUM_GAMES_PER_PAIR): # play x games
                # set player colour
                if x % 2 == 0:
                    colourA, colourB = 'w', 'b'
                else:
                    colourA, colourB = 'b', 'w'

                blackWon = playGame(colourA, genesA, colourB, genesB, 1, DEBUG)
                agentPlayCount[indexA] += 1
                agentPlayCount[indexB] += 1

                if(colourA == 'b'): 
                    agentWinCount[indexA] += blackWon
                    agentWinCount[indexB] += (1 - blackWon)
                else:
                    agentWinCount[indexB] += blackWon
                    agentWinCount[indexA] += (1 - blackWon)

    for i in range(len(agentList)):
        agentWinRate[i] = agentWinCount[i] / agentPlayCount[i]

    printWinRate(agentList, agentWinRate)

if __name__ == "__main__":
    main()

