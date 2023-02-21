import copy
import os
import numpy as np
from solution import SOLUTION
import constants as c


class PARALLEL_HILL_CLIMBER():
  def __init__(self) -> None:
    # delete all remaining fitness and brain files
    os.system("rm fitness*.nndf")
    os.system("rm brain*.nndf")


    self.nextAvailableID = 0

    self.parents = {}
    for i in range(c.populationSize):
      self.parents[i] = SOLUTION(self.nextAvailableID)
      self.nextAvailableID += 1

  def Evolve(self):
    self.Evaluate(self.parents)
    
    for currentGeneration in range(c.numberOfGenerations):
      self.Evolve_For_One_Generation()

  
  def Evolve_For_One_Generation(self):
    self.Spawn()
    self.Mutate()
    self.Evaluate(self.children)
    self.Print()
    self.Select()
    self.Print()
    

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
      solutions[key].Start_Simulation("DIRECT", parallel=True, deleteBrain="True")
    
    for key in solutions:
      solutions[key].Wait_For_Simulation_To_End()
      
    

  def Select(self):
    half = len(self.parents)//2

    bestprevious = copy.deepcopy(self.parents[0])
    for key in self.parents:
      if self.children[key].fitness > bestprevious.fitness:
        self.parents[key] = copy.deepcopy(self.children[key])
        bestprevious = copy.deepcopy(self.children[key])
      elif bestprevious.fitness > self.parents[key].fitness:
        self.parents[key] = copy.deepcopy(bestprevious)

    # if self.parent.fitness < self.child.fitness:
    #   self.parent = self.child
  
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
    
    bestParent.Start_Simulation("GUI", parallel=False, deleteBrain="False") # don't run this simulation in parallel with other things

  def Write_Best_Brain_To_File(self):
    bestParentFitness = -np.inf
    bestParent = None
    for key in self.parents:
      
      if self.parents[key].fitness > bestParentFitness:
        bestParent = copy.deepcopy(self.parents[key])
        bestParentFitness = self.parents[key].fitness
    
    bestParent.Generate_Brain()
    