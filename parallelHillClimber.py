import copy
import os
import numpy as np
from solution import SOLUTION
import constants as c
import pickle


class PARALLEL_HILL_CLIMBER():
  def __init__(self, saveData:bool, epoch:int | None, population=None) -> None:
    # delete all remaining fitness and brain files
    os.system("rm fitness*.nndf")
    os.system("rm brain*.nndf")
    os.system("rm body*.nndf")

    self.saveData = saveData
    self.epoch = epoch # how many times parallel hill climber has been run


    self.nextAvailableID = 0

    if population:
      self.parents = population
      self.nextAvailableID = max(population, key=lambda key: population[key].myID) + 1
    else:
      self.parents = {}
      
      for i in range(c.populationSize):
        self.parents[i] = SOLUTION(self.nextAvailableID)
        self.nextAvailableID += 1

  def Evolve(self):
    self.Evaluate(self.parents)
    
    for currentGeneration in range(c.numberOfGenerations+1):
      self.currentGeneration = currentGeneration
      self.Evolve_For_One_Generation()

  
  def Evolve_For_One_Generation(self):
    self.Spawn()
    self.Mutate()
    self.Evaluate(self.children)
    self.Print()
    bestFitness = self.Select()
    self.Print()
    if self.saveData:
      self.Save_Data(thisRoundBestFitness=bestFitness)
    

  def Spawn(self):
    self.children = {}
    for key in self.parents:
      self.children[key] = copy.deepcopy(self.parents[key])
      self.children[key].Set_ID(self.nextAvailableID)
      self.nextAvailableID += 1

  def Mutate(self):
    for key in self.children:
      self.children[key].Mutate()

  def Evaluate(self, solutions):
    for key in solutions:
      solutions[key].Start_Simulation("DIRECT", parallel=True, deleteBrainAndBody="True")
    
    for key in solutions:
      solutions[key].Wait_For_Simulation_To_End()
      
    

  def Select(self):
    bestFitness = -np.inf
    bestcreature = copy.deepcopy(self.parents[0])

    for key in self.parents:
      # find best fitness & which children will die or live on
      if self.children[key].fitness >= bestFitness:
        bestFitness = self.children[key].fitness
        bestcreature = copy.deepcopy(self.children[key])
      if self.parents[key].fitness > bestFitness:
        bestFitness = self.parents[key].fitness
        bestcreature = copy.deepcopy(self.parents[key])
        # self.parents[key] = copy.deepcopy(self.children[key])
      # else:
      self.parents[key] = copy.deepcopy(bestcreature)
        

    return bestFitness
  
  def Print(self):
    print("")
    for key in self.parents:
      print(self.parents[key].fitness, self.children[key].fitness)
    print("")
      
      
    # print(self.parent.fitness, self.child.fitness)

  def Show_Best(self):
    bestParentFitness = -np.inf
    bestParent = None
    for key in self.parents:
      
      if self.parents[key].fitness > bestParentFitness:
        bestParent = copy.deepcopy(self.parents[key])
        bestParentFitness = self.parents[key].fitness
    
    print("best fitness:", bestParentFitness)
    
    bestParent.Start_Simulation("GUI", parallel=False, deleteBrainAndBody="False") # don't run this simulation in parallel with other things

  def Show_Worst(self):
    worstParentFitness = np.inf
    worseParent = None
    for key in self.parents:
      
      if self.parents[key].fitness < worstParentFitness:
        worseParent = copy.deepcopy(self.parents[key])
        worstParentFitness = self.parents[key].fitness
    
    print("worst fitness:", worstParentFitness)
    
    worseParent.Start_Simulation("GUI", parallel=False, deleteBrainAndBody="False") # don't run this simulation in parallel with other things

  def Save_Data(self, thisRoundBestFitness:float):
    if self.saveData:
      # save the best fitness every generation
      if not os.path.exists(f"saved_data"):
        os.makedirs(f"saved_data")
      if not os.path.exists(f"saved_data/epoch{self.epoch}"):
        os.makedirs(f"saved_data/epoch{self.epoch}")
      # if not os.path.exists(f"saved_data/epoch{self.epoch}/best_fitnesses"):
      #   os.makedirs(f"saved_data/epoch{self.epoch}/best_fitnesses")
      with open(f"saved_data/epoch{self.epoch}/best_fitnesses.txt", "a") as f:
        f.write(str(thisRoundBestFitness) + "\n")


      # save population every so often
      if self.currentGeneration % 50 == 0:
        if not os.path.exists(f"saved_data"):
          os.makedirs(f"saved_data")
        if not os.path.exists(f"saved_data/epoch{self.epoch}"):
          os.makedirs(f"saved_data/epoch{self.epoch}")
        if not os.path.exists(f"saved_data/epoch{self.epoch}/populations"):
          os.makedirs(f"saved_data/epoch{self.epoch}/populations")
        pickle.dump(self.parents, open(f"saved_data/epoch{self.epoch}/populations/population_gen{self.currentGeneration}.p", "wb"))
    