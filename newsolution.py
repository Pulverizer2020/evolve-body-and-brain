import os
import numpy as np
import random
import time
import pyrosim.pyrosim as pyrosim
import constants as c
import networkx as nx

from randomgenotype import generateRandomGenotype
from randomgenotype import generateRandomNodeAttributes
from randomgenotype import generateRandomEdgeAttributes
from bodybuilder import BODY_BUILDER

rootx = 0
rooty = 0
rootz = 2.6

class SOLUTION():
  def __init__(self, nextAvailableID: int) -> None:
    self.myID = nextAvailableID

    self.body_builder = BODY_BUILDER(generateRandomGenotype(3,5), self.myID)

  def Start_Simulation(self, directOrGui: str, parallel: bool, deleteBrainAndBody: bool):
    self.Create_World()
    self.Generate_Body_And_Brain()
    print("finished self.Generate_Body_And_Brain", self.myID)
    if parallel:
      addParallel = "&"
    else:
      addParallel = ""
    os.system(f"python3 simulate.py {directOrGui} {str(self.myID)} {str(deleteBrainAndBody)} {addParallel}") # & means run simulation in parallel
    

  def Wait_For_Simulation_To_End(self):
    while not os.path.exists(f"fitness{str(self.myID)}.txt"): # wait for simulate.py to finish
      time.sleep(0.01)
    fitnessFile = open(f"fitness{str(self.myID)}.txt", "r")
    fitnessFileOutput = fitnessFile.read()
    self.fitness = float(fitnessFileOutput)
    fitnessFile.close()
    os.system(f"rm fitness{str(self.myID)}.txt")

  def Create_World(self):
    pyrosim.Start_SDF("world.sdf")

    pyrosim.End()

  def Generate_Body_And_Brain(self):
    self.body_builder.Build_Body()

  def Mutate(self):
    # firstRandomRow = random.randint(0,c.numSensorNeurons-1)
    # firstRandomColumn = random.randint(0,c.numHiddenNeurons-1)
    # self.firstLayerWeights[firstRandomRow,firstRandomColumn] = random.random()*2 - 1

    # secondRandomRow = random.randint(0,c.numHiddenNeurons-1)
    # secondRandomColumn = random.randint(0,c.numMotorNeurons-1)
    # self.secondLayerWeights[secondRandomRow,secondRandomColumn] = random.random()*2 - 1

    # self.firstLayerWeights[(firstRandomRow + 1) % c.numSensorNeurons,(firstRandomColumn + 1) % c.numHiddenNeurons] = random.random()*2 - 1
    # self.secondLayerWeights[(secondRandomRow + 1) % c.numHiddenNeurons,(secondRandomColumn + 1) % c.numSensorNeurons] = random.random()*2 - 1

    #### Mutate parameters of nodes and edges ####
    # nodes
    for i in self.body_builder.genotype.nodes:
      if np.random.rand() > 0.01:
        change = np.random.normal(0,0.1)
        if not self.body_builder.genotype.nodes[i]["length"] + change < 0:
          self.body_builder.genotype.nodes[i]["length"] += change
      if np.random.rand() > 0.01:
        change = np.random.normal(0,0.1)
        if not self.body_builder.genotype.nodes[i]["width"] + change < 0:
          self.body_builder.genotype.nodes[i]["width"] += change
      if np.random.rand() > 0.01:
        change = np.random.normal(0,0.1)
        if not self.body_builder.genotype.nodes[i]["height"] + change < 0:
          self.body_builder.genotype.nodes[i]["height"] += change
      if np.random.rand() > 0.01:
        print("changing sensor!!!!", i, self.body_builder.genotype.nodes[i]["has_sensor"])
        self.body_builder.genotype.nodes[i]["has_sensor"] = not self.body_builder.genotype.nodes[i]["has_sensor"]
        print("done changing sensor!!!!", i, self.body_builder.genotype.nodes[i]["has_sensor"])
      
      # maybe change this so fewer neurons get changed on every generation (maybe 1 chance or something proportional to number of connections)
      for u,v in self.body_builder.genotype.edges:
        if np.random.rand() > 0.01:
          self.body_builder.genotype.nodes[i]["neuron_weights"][(u,v)] += np.random.normal(0,0.1)
    
    # edges
    for u,v in self.body_builder.genotype.edges:
      if np.random.rand() > 0.01:
        change = np.random.normal(0,0.1)
        if not self.body_builder.genotype.edges[(u,v)]["length_proportion"] + change < 0 or not self.body_builder.genotype.edges[(u,v)]["length_proportion"] + change > 1:
          self.body_builder.genotype.edges[(u,v)]["length_proportion"] += change
      if np.random.rand() > 0.01:
        change = np.random.normal(0,0.1)
        if not self.body_builder.genotype.edges[(u,v)]["width_proportion"] + change < 0 or not self.body_builder.genotype.edges[(u,v)]["width_proportion"] + change > 1:
          self.body_builder.genotype.edges[(u,v)]["width_proportion"] += change
      if np.random.rand() > 0.01:
        change = np.random.normal(0,0.1)
        if not self.body_builder.genotype.edges[(u,v)]["height_proportion"] + change < 0 or not self.body_builder.genotype.edges[(u,v)]["height_proportion"] + change > 1:
          self.body_builder.genotype.edges[(u,v)]["height_proportion"] += change
      
      # NEED TO MAKE SURE AT LEAST 1 IS == 1
      if not (self.body_builder.genotype.edges[(u,v)]["length_proportion"] == 1 or self.body_builder.genotype.edges[(u,v)]["width_proportion"] == 1 or self.body_builder.genotype.edges[(u,v)]["height_proportion"] == 1):
        surface_i = np.random.randint(low=0,high=2)
        # make sure the joint is one the surface
        match surface_i:
            case 0:
                self.body_builder.genotype.edges[(u,v)]["length_proportion"] = 1
            case 1:
                self.body_builder.genotype.edges[(u,v)]["width_proportion"] = 1
            case 2:
                self.body_builder.genotype.edges[(u,v)]["height_proportion"] = 1
      

    #### Possible node removal ####
    if np.random.rand() > 0.01:
      # only delete a node if there's more than 2 nodes
      if len(self.body_builder.genotype.nodes) > 2:
        # remove a single node
        for i in self.body_builder.genotype.nodes():
          # this is an outer node, so remove it
          if self.body_builder.genotype.in_degree(i) == 1 and self.body_builder.genotype.out_degree(i) == 0:
            in_edge = list(self.body_builder.genotype.in_edges(i))[0]
            self.body_builder.genotype.remove_node(i)
            break
        
        # now, update all the neuron_weights to remove the weights for this edge
        for i in self.body_builder.genotype.nodes():
          del self.body_builder.genotype.nodes[i]["neuron_weights"][in_edge]
    
    #### Possible node addition ####
    if np.random.rand() > 0.01:
      # add a node
      new_node_id = max(list(self.body_builder.genotype.nodes)) + 1
      self.body_builder.genotype.add_node(new_node_id)

      # connect this node to the rest of the genotype
      parent_node_id = np.random.choice(list(self.body_builder.genotype.nodes))
      self.body_builder.genotype.add_edge(parent_node_id, new_node_id)

      # set the attributes of the new node and edge
      nx.set_node_attributes(self.body_builder.genotype, {new_node_id: generateRandomNodeAttributes(genotype=self.body_builder.genotype)})
      nx.set_edge_attributes(self.body_builder.genotype, {(parent_node_id, new_node_id): generateRandomEdgeAttributes()})


      # now update every node's neuron_weights to include this new node
      for i in self.body_builder.genotype.nodes:
        self.body_builder.genotype.nodes[i]["neuron_weights"][(parent_node_id, new_node_id)] = np.random.uniform(low=-1, high=1)
        

    

  def Set_ID(self, newID):
    self.myID = newID
    self.body_builder.solutionId = newID
