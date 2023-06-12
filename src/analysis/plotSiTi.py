from matplotlib import pyplot
import os
import pandas

# Create the directory where the plots will be saved
os.makedirs("plots", exist_ok=True)

frame = pandas.read_csv("data/rocketsSiTi.csv")

pyplot.figure()

pyplot.scatter(x="siMean", y="tiMean", data=frame)

pyplot.xlabel("Information spatiale moyenne")
pyplot.ylabel("Information temporelle moyenne")

pyplot.savefig("plots/si_ti_rockets.svg", bbox_inches="tight")
