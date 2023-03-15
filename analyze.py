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


data = []
for i in range(18):
    with open(f"saved_data/epoch{i}/best_fitnesses.txt", "r") as f:
        content = f.read()
        content = content.split()
        content = [float(fitness) for fitness in content]
        matplotlib.pyplot.plot(content, label=f"{i}")

average = [np.average(l) for l in zip(*data)]
# print(average)
# matplotlib.pyplot.plot(average)

matplotlib.pyplot.title("Multiple Epochs Fitness")
matplotlib.pyplot.xlabel("generation")
matplotlib.pyplot.ylabel("fitness improvement compared to initial fitness")
matplotlib.pyplot.legend()
matplotlib.pyplot.show()