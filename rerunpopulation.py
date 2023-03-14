import pickle
import os

from parallelHillClimber import PARALLEL_HILL_CLIMBER

# rerun the best in a picked population
population = pickle.load(open("saved_data/epoch6/populations/population_gen500.p", "rb"))

phc = PARALLEL_HILL_CLIMBER(saveData=False, epoch=0, population=population)
phc.Show_Best()



# 10 galloping
# 11 large hops with 2 large wings
# 3 mini hops with front appendage to keep balance
# 12 thrusting and side-swiping snake
# 13 rolling snake
# 14 prancing snake
# 15 side-slithering snake
# 16 mini-galloping snake
# 17 galloping 3 legged creature