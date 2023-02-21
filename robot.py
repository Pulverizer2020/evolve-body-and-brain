import os
import pybullet as p
import pyrosim.pyrosim as pyrosim
from pyrosim.neuralNetwork import NEURAL_NETWORK
import constants as c

from sensor import SENSOR
from motor import MOTOR

class ROBOT:

  def __init__(self, solutionId: str, deleteBrain: str):

    
    self.solutionId = str(solutionId)

    self.robotId = p.loadURDF("body.urdf")
    

    self.nn = NEURAL_NETWORK("brain" + solutionId + ".nndf")

    pyrosim.Prepare_To_Simulate(self.robotId)
    self.Prepare_To_Sense()
    self.Prepare_To_Act()

    if deleteBrain == "True":
      os.system(f"rm brain{solutionId}.nndf")

  def Prepare_To_Sense(self):
    self.sensors = {}
    for linkName in pyrosim.linkNamesToIndices:
      self.sensors[linkName] = SENSOR(linkName)

  def Prepare_To_Act(self):
    self.motors = {}
    for jointName in pyrosim.jointNamesToIndices:
      self.motors[jointName] = MOTOR(jointName)

  def Sense(self, i):
    for linkName, sensor in self.sensors.items():
      sensor.Get_Value(i)

  def Act(self, i):
    for neuronName in self.nn.Get_Neuron_Names():
      if self.nn.Is_Motor_Neuron(neuronName):
        jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
        desiredAngle = self.nn.Get_Value_Of(neuronName) * c.motorJointRange
        self.motors[jointName].Set_Value(self, desiredAngle)

  def Think(self):
    self.nn.Update()

  def Get_Fitness(self):
    # stateOfLinkZero = p.getLinkState(self.robotId,0)
    # positionOfLinkZero = stateOfLinkZero[0]
    # xCoordinateOfLinkZero = positionOfLinkZero[0]
    basePositionAndOrientation = p.getBasePositionAndOrientation(self.robotId)
    basePosition = basePositionAndOrientation[0]
    xPosition = basePosition[0]
    zPosition = basePosition[2]

    # if zPosition < 2:
    #   fitness = xPosition*zPosition
    # else:
    fitness = xPosition*zPosition + zPosition*2

    f = open(f"tmp{self.solutionId}.txt", "w")
    f.write(str(fitness))
    f.close()
    os.system(f"mv tmp{self.solutionId}.txt fitness{self.solutionId}.txt")
    