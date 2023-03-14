import constants as c
from parallelHillClimber import PARALLEL_HILL_CLIMBER

# run multiple rounds (or "epochs") of Parallel Hill Climber
for epoch in range(c.numberOfEpochs):
    phc = PARALLEL_HILL_CLIMBER(saveData=True, epoch=epoch)
    phc.Evolve()
    phc.Show_Best()