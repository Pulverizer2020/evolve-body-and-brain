import numpy as np
import matplotlib.pyplot



backLegSensorValues = np.load("data/backLegSensorValues.npy")
frontLegSensorValues = np.load("data/frontLegSensorValues.npy")
targetAngles = np.load("data/targetAngles.npy")

matplotlib.pyplot.plot(targetAngles)

# matplotlib.pyplot.plot(backLegSensorValues, label="Back Leg", linewidth=0.7)
# matplotlib.pyplot.plot(frontLegSensorValues, label="Front Leg", linewidth=0.7)

# matplotlib.pyplot.legend()

matplotlib.pyplot.show()

