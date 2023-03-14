from parallelHillClimber import PARALLEL_HILL_CLIMBER

phc = PARALLEL_HILL_CLIMBER(saveData=True, epoch=0)
phc.Evolve()
phc.Show_Best()