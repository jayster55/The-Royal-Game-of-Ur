import math
import numpy as np
import copy
from playUr_GvG import playGame

# global constant
AGENT_DIR = "agentFiles/" # directory for agent files
NUM_GAMES_PER_PAIR = 30 # number of games played between each pair of agents
ROUND_DIGIT = 3
WINRATE_THRESHOLD = float(0.1)

# gene constants
NUM_GENES = 10
GENE_VAL_MIN = 0
GENE_VAL_MAX = 50

# child constants
NUM_CHILD_MUTATE = 12
NUM_CHILD_RANDOM = 5
NUM_CHILD_ELITE = 3

# flag
DEBUG = False
USE_BEST_PREVIOUS_GEN = False # True if new generation is to be generated from the best of the previous generations, instead of the immediate preceding generation, and False otherwise

def printWinRate(agentWinRate): # prints out agent winrate
    for i in range(len(agentWinRate)):
        print("Agent " + str(i) + " winrate", end=': ')
        print(str(round(agentWinRate[i] * 100, ROUND_DIGIT)) + "%")

def createBaselineAgents():
    numBaselineAgents = 50
    baselineAgents = []

    for i in range(numBaselineAgents):
        agent = [0] * NUM_GENES
        for gene in range(NUM_GENES):
            agent[gene] = (GENE_VAL_MAX - GENE_VAL_MIN) * np.random.random_sample() + GENE_VAL_MIN

        baselineAgents.append(agent)

    return baselineAgents

def getBaselineWinrate(baselineAgents, agent):
    numBaselineGames = 30
    numBaselineAgents = len(baselineAgents)
    winCount = 0 # init

    for baselineAgent in baselineAgents:
        for i in range(numBaselineGames):
            if i % 2 == 0:
                colourBaseline, colourAgent = 'w', 'b'
            else:
                colourBaseline, colourAgent = 'b', 'w'

            blackWon = playGame(colourBaseline, baselineAgent, colourAgent, agent, 1, DEBUG)

            if(colourAgent == 'b'):
                winCount += blackWon
            else:
                winCount += (1 - blackWon)

    return winCount / (numBaselineGames * numBaselineAgents)

# main ---------------------------
# agentList is a list of genes for each agent
def playGenerationGames(agentList):

    agentWinCount = np.zeros(len(agentList)) # init wincount array
    agentPlayCount = np.zeros(len(agentList)) # init playcount array
    agentWinRate = np.zeros(len(agentList)) # init winrate array

    for indexA in range(len(agentList) - 1): # iterate
        for indexB in range(indexA + 1, len(agentList)):
            genesA = agentList[indexA]
            genesB = agentList[indexB]
            
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

    baselineAgents = createBaselineAgents() # create baseline random agents
    bestBaselineWinrate = 0 # init
    bestGen = 0 # init

    bestWinRate = 0
    bestAgent = []
    bestGenerationGenes = [] # init

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
        print("Beginning generation " + str(generationIndex))
        #print("Generation is as follows:")
        #for item in listOfGenes:
        #    print(item)


        genWinRates = playGenerationGames(listOfGenes)
        originalWinRate = max(genWinRates)
        genWinRate = round(originalWinRate * 100, ROUND_DIGIT)

        print("Best agent of generation " + str(generationIndex) + " winrate of " + str(genWinRate) + "%" + " against the other agent of the same generation")

        bestGenerationAgent = listOfGenes[genWinRates.index(max(genWinRates))]
        baselineWinrate = getBaselineWinrate(baselineAgents, bestGenerationAgent)
        print("Best agent of generation " + str(generationIndex) + " winrate of " + str(round(baselineWinrate * 100, ROUND_DIGIT)) + "%" + " against static baseline agents\n")

        
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

        if baselineWinrate > bestBaselineWinrate:
            bestBaselineWinrate = baselineWinrate
            bestGenerationGenes = copy.deepcopy(listOfGenes)
            bestGen = generationIndex
        elif USE_BEST_PREVIOUS_GEN:
            print("New generation worse; use generation " + str(bestGen) + " to derive children")
            listOfGenes = bestGenerationGenes
        
        # generate children from parents
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

        # generate children by elitism
        #now we apply our elitism, taking the 4 best members of this generation
        #this sorts the list and produces the 4 highest (original) indices
        eliteIndices = sorted( [(x, i) for (i,x) in enumerate(genWinRates)], reverse=True )[:NUM_CHILD_ELITE]
        for index in range(NUM_CHILD_ELITE):
            nextGeneration.append(listOfGenes[eliteIndices[index][1]])

        #the next generation is now complete
        listOfGenes = nextGeneration

        


evolveAgents()
