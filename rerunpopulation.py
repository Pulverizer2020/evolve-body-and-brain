import pickle
import os

from parallelHillClimber import PARALLEL_HILL_CLIMBER

# rerun the best in a picked population
population = pickle.load(open("saved_data/epoch8/populations/population_gen500.p", "rb"))

phc = PARALLEL_HILL_CLIMBER(saveData=False, epoch=0, population=population)
phc.Show_Best()



# 0 hopper
# 1 biped
# 2 hopper with front antenna for balance
# 3 blob... moves slowly
# 4 hopper with 2 front arms for balance
# 5 hopper with 2 front arms for balance
# 6 hopper with 2 front arms for balance
# 7 three-legged hopper (looks like mini octopus)
# 8 slithering snake
# 9 side-swipe hopper


# 10 galloping
# 11 large hops with 2 large wings
# 12 thrusting and side-swiping snake
# 13 rolling snake
# 14 prancing snake
# 15 side-slithering snake
# 16 mini-galloping snake
# 17 galloping 3 legged creature