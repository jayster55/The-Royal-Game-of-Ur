import math
import numpy as np
from playUr_RvG import playGame
from randomagent import Piece

# global constant
AGENT_DIR = "agentFiles/" # directory for agent files
NUM_GAMES_PER_PAIR = 50 # number of games played between each pair of agents
DEBUG = False
ROUND_DIGIT = 3
WINRATE_THRESHOLD = float(1)

# gene constants
NUM_GENES = 10
GENE_VAL_MIN = 0
GENE_VAL_MAX = 50

# child constants
NUM_CHILD_MUTATE = 12
NUM_CHILD_RANDOM = 5
NUM_CHILD_ELITE = 3

def printWinRate(agentWinRate): # prints out agent winrate
    for i in range(len(agentWinRate)):
        print("Agent " + str(i) + " winrate", end=': ')
        print(str(round(agentWinRate[i] * 100, ROUND_DIGIT)) + "%")



# main ---------------------------
# agentList is a list of genes for each agent
def playGenerationGames(agentList):

    agentWinCount = np.zeros(len(agentList)) # init wincount array
    agentPlayCount = np.zeros(len(agentList)) # init playcount array
    agentWinRate = np.zeros(len(agentList)) # init winrate array
    randomWinCount = np.zeros(len(agentList)) # init wincount array
    randomPlayCount = np.zeros(len(agentList)) # init playcount array
    randomWinRate = np.zeros(len(agentList)) # init winrate array 

    for index in range(len(agentList) - 1): # iterate
            genes = agentList[index]
            
            for x in range(NUM_GAMES_PER_PAIR): # play x games
                # set player colour
                if x % 2 == 0:
                    colour = Piece.White
                else:
                    colour = Piece.Black

                blackWon = playGame(colour, genes, 1, DEBUG)
                agentPlayCount[index] += 1
                randomPlayCount[index] += 1

                if(colour == Piece.Black): 
                    agentWinCount[index] += blackWon
                    randomWinCount[index] += (1 - blackWon)
                else:
                    agentWinCount[index] += (1 - blackWon)
                    randomWinCount[index] += blackWon

    for i in range(len(agentList)):
        agentWinRate[i] = agentWinCount[i] / agentPlayCount[i]

    return list(agentWinRate)

def normalizeList(listOfNums):
    total = 0
    for value in listOfNums:
        total += value

    normalizedList = list(map(lambda x: round(float(x / total), 5), listOfNums))

    #to be properly normalized we must make sure they sum to 1
    normalizedList[len(normalizedList) - 1] = 1 - sum(normalizedList[:-1])
    return normalizedList


def mutateAgent(genes, rnGenerator):
    mutateChance = 0.25
    mutateMultiplier = 0.15

    for index in range(NUM_GENES):
        mutate = rnGenerator.integers(0, 100)
        if mutate < int(mutateChance * 100):
            mutationAmount = rnGenerator.choice([1 + mutateMultiplier, 1 - mutateMultiplier])
            genes[index] = genes[index] * mutationAmount

def evolveAgents():
    #a list of lists of floats, each list corresponding to an agent
    listOfGenes = []
    with open(AGENT_DIR + "agentList") as f:
        agentList = f.read().splitlines() # read agent filenames from "/agentList"
        for agentFile in agentList:
            with open(AGENT_DIR + agentFile) as f2:
                #read in the genes as a list and convert each entry to a float
                listOfGenes.append([float(i) for i in f2.read().splitlines()])
    
    generationIndex = 0
    lastWinRate = 0

    bestWinRate = 0
    bestAgent = []
    # a numpy RNG used for parent selection
    generator = np.random.default_rng()
    while True:
        #each generation we do as follows:
        #increment the index for debugging
        #play the generation games to get all the winrates
        #compute the winrate delta of the best agent
        #if the delta is too small, stop and return the best agent
        #else, normalize the winrates of each agent and use it to pick parents
        #make 7 new kids and take the 4 highest rated agents from last generation
        #repeat
        generationIndex += 1
        print("Beginning generation " + str(generationIndex) + " with winrate " + str(lastWinRate))
        #print("Generation is as follows:")
        #for item in listOfGenes:
        #    print(item)


        genWinRates = playGenerationGames(listOfGenes)
        originalWinRate = max(genWinRates)
        genWinRate = round(originalWinRate * 100, 3)
        
        if genWinRate > bestWinRate:
            bestWinRate = genWinRate
            bestIndex = genWinRates.index(originalWinRate)
            bestAgent = listOfGenes[bestIndex]

        if genWinRate >= lastWinRate and genWinRate - lastWinRate < WINRATE_THRESHOLD:
            #stop now
            f = open("FinalAgent", 'w')
            for gene in bestAgent:
                f.write(str(gene) + '\n')
            f.close()
            print("Final agent discovered, winrate of " + str(bestWinRate) 
                    + "% was below improvement threshold")
            return
        
        #else, new generation        
        lastWinRate = genWinRate
        normalizedList = normalizeList(genWinRates)
        nextGeneration = []
    
        for newChild in range(0, NUM_CHILD_MUTATE):
            child = [0] * NUM_GENES
            #this chooses 2 parents without replacement, using the final list as probabilities
            parents = generator.choice(listOfGenes, 2, False, normalizedList)
            for gene in range(NUM_GENES):
                #each gene is the average of its parents
                child[gene] = round((parents[0][gene] + parents[1][gene]) / 2, 3)
            
            #mutate each child, potentially
            mutateAgent(child, generator)
            nextGeneration.append(child)

        # generate new children with random genes
        for newChild in range(0, NUM_CHILD_RANDOM):
            child = [0] * NUM_GENES
            for gene in range(NUM_GENES):
                child[gene] = (GENE_VAL_MAX - GENE_VAL_MIN) * np.random.random_sample() + GENE_VAL_MIN # generate random gene in range [GENE_VAL_MIN, GENE_VAL_MAX)

            nextGeneration.append(child)

        #now we apply our elitism, taking the 4 best members of this generation
        #this sorts the list and produces the 4 highest (original) indices
        eliteIndices = sorted( [(x, i) for (i,x) in enumerate(genWinRates)], reverse=True )[:NUM_CHILD_ELITE]
        for index in range(NUM_CHILD_ELITE):
            nextGeneration.append(listOfGenes[eliteIndices[index][1]])

        #the next generation is now complete
        listOfGenes = nextGeneration


evolveAgents()
