from parallelHillClimber import PARALLEL_HILL_CLIMBER

phc = PARALLEL_HILL_CLIMBER()
phc.Evolve()
print("done evolving")
phc.Show_Best()
phc.Write_Best_Brain_To_File()