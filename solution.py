import os
import numpy as np
import random
import time
import pyrosim.pyrosim as pyrosim
import constants as c



rootx = 0
rooty = 0
rootz = 2.6

class SOLUTION():
  def __init__(self, nextAvailableID: int) -> None:
    self.firstLayerWeights = np.random.rand(c.numSensorNeurons,c.numHiddenNeurons)*2 - 1

    self.secondLayerWeights = np.random.rand(c.numHiddenNeurons, c.numMotorNeurons)*2 - 1

    self.myID = nextAvailableID

  def Start_Simulation(self, directOrGui: str, parallel: bool, deleteBrain: bool):
    self.Create_World()
    self.Generate_Body()
    self.Generate_Brain()
    if parallel:
      addParallel = "&"
    else:
      addParallel = ""
    os.system(f"python3 simulate.py {directOrGui} {str(self.myID)} {str(deleteBrain)} {addParallel}") # & means run simulation in parallel
    # os.system(f"python3 simulate.py {directOrGui} {str(self.myID)} 2&>1 &") # put errors into a file named "1"

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

    # for i in range(10):
    #   pyrosim.Send_Cube(name="Box", pos=[5*i,0,0.2*i], size=[5,10,0.4*(i+1)])

    pyrosim.End()

  def Generate_Body(self):
    pyrosim.Start_URDF("body.urdf")

    # # QUADRUPED
    # # Torso
    # pyrosim.Send_Cube(name="Torso", pos=[rootx,rooty,rootz] , size=[1,1,1])

    # pyrosim.Send_Joint(name="Torso_FrontLeg", parent="Torso", child ="FrontLeg", type="revolute", position=[rootx,rooty+0.5,rootz], jointAxis="1 0 0")
    # pyrosim.Send_Cube(name="FrontLeg", pos=[0,0.5,0] , size=[0.2,1,0.2])

    # pyrosim.Send_Joint(name="Torso_BackLeg", parent="Torso", child ="BackLeg", type="revolute", position=[rootx,rooty-0.5,rootz], jointAxis="1 0 0")
    # pyrosim.Send_Cube(name="BackLeg", pos=[0,-0.5,0] , size=[0.2,1,0.2])

    # pyrosim.Send_Joint(name="Torso_LeftLeg", parent="Torso", child ="LeftLeg", type="revolute", position=[rootx-0.5,rooty,rootz], jointAxis="0 1 0")
    # pyrosim.Send_Cube(name="LeftLeg", pos=[-0.5,0,0] , size=[1,0.2,0.2])

    # pyrosim.Send_Joint(name="Torso_RightLeg", parent="Torso", child ="RightLeg", type="revolute", position=[rootx+0.5,rooty,rootz], jointAxis="0 1 0")
    # pyrosim.Send_Cube(name="RightLeg", pos=[0.5,0,0] , size=[1,0.2,0.2])


    # pyrosim.Send_Joint(name="FrontLeg_FrontLowerLeg", parent="FrontLeg", child ="FrontLowerLeg", type="revolute", position=[0,1,0], jointAxis="1 0 0")
    # pyrosim.Send_Cube(name="FrontLowerLeg", pos=[0,0,-0.5] , size=[0.2,0.2,1.3])

    # pyrosim.Send_Joint(name="BackLeg_BackLowerLeg", parent="BackLeg", child ="BackLowerLeg", type="revolute", position=[0,-1,0], jointAxis="1 0 0")
    # pyrosim.Send_Cube(name="BackLowerLeg", pos=[0,0,-0.5] , size=[0.2,0.2,1.3])

    # pyrosim.Send_Joint(name="LeftLeg_LeftLowerLeg", parent="LeftLeg", child ="LeftLowerLeg", type="revolute", position=[-1,0,0], jointAxis="0 1 0")
    # pyrosim.Send_Cube(name="LeftLowerLeg", pos=[0,0,-0.5] , size=[0.2,0.2,1.3])

    # pyrosim.Send_Joint(name="RightLeg_RightLowerLeg", parent="RightLeg", child ="RightLowerLeg", type="revolute", position=[1,0,0], jointAxis="0 1 0")
    # pyrosim.Send_Cube(name="RightLowerLeg", pos=[0,0,-0.5] , size=[0.2,0.2,1.3])

    #########################

    # # HUMANOID
    # Torso & Head
    pyrosim.Send_Cube(name="Torso", pos=[rootx,rooty,rootz] , size=[0.5,0.75,1.5])

    pyrosim.Send_Joint(name="Torso_Head", parent="Torso", child ="Head", type="fixed", position=[rootx,rooty,rootz+0.75], jointAxis="1 0 0")
    pyrosim.Send_Cube(name="Head", pos=[0,0,0.15] , size=[0.3,0.3,0.3])

    # Arms
    pyrosim.Send_Joint(name="Torso_RightArm", parent="Torso", child ="RightArm", type="revolute", position=[rootx,rooty-(0.75/2),rootz+(1.5/3.5)], jointAxis="0 0 1")
    pyrosim.Send_Cube(name="RightArm", pos=[0,-0.5,0] , size=[0.2,1,0.2])

    pyrosim.Send_Joint(name="Torso_LeftArm", parent="Torso", child ="LeftArm", type="revolute", position=[rootx,rooty+(0.75/2),rootz+(1.5/3.5)], jointAxis="0 0 1")
    pyrosim.Send_Cube(name="LeftArm", pos=[0,0.5,0] , size=[0.2,1,0.2])


    # leg rotaters 

    # X
    pyrosim.Send_Joint(name="Torso_RightLegXTwist", parent="Torso", child ="RightLegXTwist", type="revolute", position=[rootx,rooty-(0.75/3.5),rootz-(1.5/2)], jointAxis="1 0 0")
    pyrosim.Send_Cube(name="RightLegXTwist", pos=[0,0,-0.05] , size=[0.1,0.1,0.1])

    pyrosim.Send_Joint(name="Torso_LeftLegXTwist", parent="Torso", child ="LeftLegXTwist", type="revolute", position=[rootx,rooty+(0.75/3.5),rootz-(1.5/2)], jointAxis="1 0 0")
    pyrosim.Send_Cube(name="LeftLegXTwist", pos=[0,0,-0.05] , size=[0.1,0.1,0.1])

    # Upper Legs
    pyrosim.Send_Joint(name="RightLegXTwist_RightThigh", parent="RightLegXTwist", child ="RightThigh", type="revolute", position=[0,0,-0.1], jointAxis="0 1 0")
    pyrosim.Send_Cube(name="RightThigh", pos=[0,0,-0.75/2] , size=[0.2,0.2,0.75])

    pyrosim.Send_Joint(name="LeftLegXTwist_LeftThigh", parent="LeftLegXTwist", child ="LeftThigh", type="revolute", position=[0,0,-0.1], jointAxis="0 1 0")
    pyrosim.Send_Cube(name="LeftThigh", pos=[0,0,-0.75/2] , size=[0.2,0.2,0.75])

    # Lower Legs
    pyrosim.Send_Joint(name="RightThigh_RightLowerLeg", parent="RightThigh", child ="RightLowerLeg", type="revolute", position=[0,0,-0.75], jointAxis="0 1 0")
    pyrosim.Send_Cube(name="RightLowerLeg", pos=[0,0,-0.75/2] , size=[0.2,0.2,0.75])

    pyrosim.Send_Joint(name="LeftThigh_LeftLowerLeg", parent="LeftThigh", child ="LeftLowerLeg", type="revolute", position=[0,0,-0.75], jointAxis="0 1 0")
    pyrosim.Send_Cube(name="LeftLowerLeg", pos=[0,0,-0.75/2] , size=[0.2,0.2,0.75])

    # Feet
    pyrosim.Send_Joint(name="RightLowerLeg_RightFoot", parent="RightLowerLeg", child ="RightFoot", type="revolute", position=[0,0,-0.75], jointAxis="0 1 0")
    pyrosim.Send_Cube(name="RightFoot", pos=[(0.2/2),0,0] , size=[0.4,0.2,0.2])

    pyrosim.Send_Joint(name="LeftLowerLeg_LeftFoot", parent="LeftLowerLeg", child ="LeftFoot", type="revolute", position=[0,0,-0.75], jointAxis="0 1 0")
    pyrosim.Send_Cube(name="LeftFoot", pos=[(0.2/2),0,0] , size=[0.4,0.2,0.2])




    pyrosim.End()

  def Generate_Brain(self):
    pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")

    # # Quadruped
    # pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "FrontLowerLeg")
    # pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "BackLowerLeg")
    # pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "LeftLowerLeg")
    # pyrosim.Send_Sensor_Neuron(name = 3 , linkName = "RightLowerLeg")

    # pyrosim.Send_Hidden_Neuron( name = 4 )
    # pyrosim.Send_Hidden_Neuron( name = 5 )
    # pyrosim.Send_Hidden_Neuron( name = 6 )
    # pyrosim.Send_Hidden_Neuron( name = 7 )
    # pyrosim.Send_Hidden_Neuron( name = 8 )
    # pyrosim.Send_Hidden_Neuron( name = 9 )

    # pyrosim.Send_Motor_Neuron( name = 10 , jointName = "Torso_BackLeg")
    # pyrosim.Send_Motor_Neuron( name = 11 , jointName = "Torso_FrontLeg")
    # pyrosim.Send_Motor_Neuron( name = 12 , jointName = "Torso_RightLeg")
    # pyrosim.Send_Motor_Neuron( name = 13 , jointName = "Torso_LeftLeg")
    # pyrosim.Send_Motor_Neuron( name = 14 , jointName = "FrontLeg_FrontLowerLeg")
    # pyrosim.Send_Motor_Neuron( name = 16 , jointName = "BackLeg_BackLowerLeg")
    # pyrosim.Send_Motor_Neuron( name = 17 , jointName = "LeftLeg_LeftLowerLeg")
    # pyrosim.Send_Motor_Neuron( name = 18 , jointName = "RightLeg_RightLowerLeg")


    # HUMANOID!!!!!
    # neurons
    pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "RightFoot")
    pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "LeftFoot")
    pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "RightLowerLeg")
    pyrosim.Send_Sensor_Neuron(name = 3 , linkName = "LeftLowerLeg")
    # pyrosim.Send_Sensor_Neuron(name = 4 , linkName = "RightArm")
    # pyrosim.Send_Sensor_Neuron(name = 5 , linkName = "LeftArm")


    for i in range(c.numHiddenNeurons):
      pyrosim.Send_Hidden_Neuron( name = c.numSensorNeurons + i )

    # motors
    pyrosim.Send_Motor_Neuron( name = 1 + c.numSensorNeurons + c.numMotorNeurons , jointName = "Torso_RightArm")
    pyrosim.Send_Motor_Neuron( name = 2 + c.numSensorNeurons + c.numMotorNeurons, jointName = "Torso_LeftArm")
    pyrosim.Send_Motor_Neuron( name = 3 + c.numSensorNeurons + c.numMotorNeurons, jointName = "RightLegXTwist_RightThigh")
    pyrosim.Send_Motor_Neuron( name = 4 + c.numSensorNeurons + c.numMotorNeurons, jointName = "LeftLegXTwist_LeftThigh")
    pyrosim.Send_Motor_Neuron( name = 5 + c.numSensorNeurons + c.numMotorNeurons, jointName = "RightThigh_RightLowerLeg")
    pyrosim.Send_Motor_Neuron( name = 6 + c.numSensorNeurons + c.numMotorNeurons, jointName = "LeftThigh_LeftLowerLeg")
    pyrosim.Send_Motor_Neuron( name = 7 + c.numSensorNeurons + c.numMotorNeurons, jointName = "RightLowerLeg_RightFoot")
    pyrosim.Send_Motor_Neuron( name = 8 + c.numSensorNeurons + c.numMotorNeurons, jointName = "LeftLowerLeg_LeftFoot")

    

    for currentRow in range(c.numSensorNeurons):
      for currentColumn in range(c.numHiddenNeurons):
        pyrosim.Send_Synapse( sourceNeuronName = currentRow , targetNeuronName = currentColumn+c.numSensorNeurons , weight = self.firstLayerWeights[currentRow][currentColumn] )
    
    for currentRow in range(c.numHiddenNeurons):
      for currentColumn in range(c.numMotorNeurons):
        pyrosim.Send_Synapse( sourceNeuronName = currentRow+c.numSensorNeurons , targetNeuronName = currentColumn+c.numSensorNeurons+c.numHiddenNeurons , weight = self.secondLayerWeights[currentRow][currentColumn] )
    

    pyrosim.End()
    

    

  def Mutate(self):
    firstRandomRow = random.randint(0,c.numSensorNeurons-1)
    firstRandomColumn = random.randint(0,c.numHiddenNeurons-1)
    self.firstLayerWeights[firstRandomRow,firstRandomColumn] = random.random()*2 - 1

    secondRandomRow = random.randint(0,c.numHiddenNeurons-1)
    secondRandomColumn = random.randint(0,c.numMotorNeurons-1)
    self.secondLayerWeights[secondRandomRow,secondRandomColumn] = random.random()*2 - 1

    self.firstLayerWeights[(firstRandomRow + 1) % c.numSensorNeurons,(firstRandomColumn + 1) % c.numHiddenNeurons] = random.random()*2 - 1
    self.secondLayerWeights[(secondRandomRow + 1) % c.numHiddenNeurons,(secondRandomColumn + 1) % c.numSensorNeurons] = random.random()*2 - 1

  def Set_ID(self, newID):
    self.myID = newID
