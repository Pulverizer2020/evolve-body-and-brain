import time
import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import numpy as np
import random
import constants as c

from world import WORLD
from robot import ROBOT



class SIMULATION:

  def __init__(self, directOrGui: str, solutionId: str, deleteBrainAndBody: str):
    self.directOrGui = directOrGui
    if directOrGui == "DIRECT":
      self.physicsClient = p.connect(p.DIRECT)
    else:
      self.physicsClient = p.connect(p.GUI)
      p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.setGravity(0,0,c.gravityY)

    self.world = WORLD()
    self.robot = ROBOT(solutionId, deleteBrainAndBody=deleteBrainAndBody)

  def __del__(self):

    p.disconnect()
  
  def Run(self):
    
    for i in range(c.SIM_LENGTH):
      basePos, baseOrn = p.getBasePositionAndOrientation(self.robot.robotId)
      p.resetDebugVisualizerCamera( cameraDistance = 5, cameraYaw=75 + i/6, cameraPitch=-30, cameraTargetPosition = basePos)
      # p.resetDebugVisualizerCamera( cameraDistance = 5, cameraYaw=175, cameraPitch=-30, cameraTargetPosition = basePos)

    
      p.stepSimulation()
      self.robot.Sense(i)
      self.robot.Think()
      self.robot.Act(i)
      if self.directOrGui == "GUI":
        time.sleep(1/120)

  def Get_Fitness(self):
    self.robot.Get_Fitness()