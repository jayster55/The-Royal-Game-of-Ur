import sys
import random

NUM_AGENTS = 20
NUM_GENES = 10

GENE_VAL_MIN = 1
GENE_VAL_MAX = 50

AGENT_LIST_FILE = "agentList"

# minRange = float(sys.argv[1])
# maxRange = float(sys.argv[2])

for agentIndex in range(1, NUM_AGENTS + 1):
    with open("a" + f'{agentIndex:02}', 'w') as f:
        for gene in range(0, NUM_GENES):
            f.write(str(round(random.uniform(GENE_VAL_MIN, GENE_VAL_MAX), 2)) + '\n')
        f.close()

with open("agentList", 'w') as f:
    for i in range(1, NUM_AGENTS + 1):
        f.write('a' + f'{i:02}' + '\n')
    f.close()
