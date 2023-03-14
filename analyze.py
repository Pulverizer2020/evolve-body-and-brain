import numpy as np
import matplotlib.pyplot



# backLegSensorValues = np.load("data/backLegSensorValues.npy")
# frontLegSensorValues = np.load("data/frontLegSensorValues.npy")
# targetAngles = np.load("data/targetAngles.npy")

# matplotlib.pyplot.plot(targetAngles)

# matplotlib.pyplot.plot(backLegSensorValues, label="Back Leg", linewidth=0.7)
# matplotlib.pyplot.plot(frontLegSensorValues, label="Front Leg", linewidth=0.7)

# matplotlib.pyplot.legend()

# matplotlib.pyplot.show()


with open("saved_data/epoch7/best_fitnesses.txt", "r") as f:
    content = f.read()
    content = content.split()
    content = [float(fitness) for fitness in content]
    matplotlib.pyplot.plot(content)
    matplotlib.pyplot.show()