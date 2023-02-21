import numpy as np

SIM_LENGTH = 3000
gravityY = -9.8

# amplitudeBackLeg = np.pi/4
# frequencyBackLeg = 10
# phaseOffsetBackLeg = 0
# amplitudeFrontLeg = np.pi/4
# frequencyFrontLeg = 15
# phaseOffsetFrontLeg = np.pi/4

# x = np.linspace(0, 2*np.pi, SIM_LENGTH)
# targetAnglesBackLeg = amplitudeBackLeg * np.sin(frequencyBackLeg * x + phaseOffsetBackLeg)
# targetAnglesFrontLeg = amplitudeFrontLeg * np.sin(frequencyFrontLeg * x + phaseOffsetFrontLeg)

motorJointRange = 1


# evolution parameters
numberOfGenerations = 1
populationSize = 1


# robot body parameters
# # quadruped
# numSensorNeurons = 4
# numMotorNeurons = 8
# humanoid
numSensorNeurons = 4
numHiddenNeurons = 16
numMotorNeurons = 6
