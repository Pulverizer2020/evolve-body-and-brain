import sys
from simulation import SIMULATION

directOrGui = sys.argv[1]
solutionId = sys.argv[2]
deleteBrain = sys.argv[3]

simulation = SIMULATION(directOrGui, solutionId, deleteBrain)

simulation.Run()

simulation.Get_Fitness()
