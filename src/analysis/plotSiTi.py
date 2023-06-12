import json
from matplotlib import pyplot
import os
import pandas

# Create the directory where the plots will be saved
os.makedirs("plots", exist_ok=True)

frame = pandas.read_csv("data/siTiTokyo.csv")
frame = frame.groupby("input_file", as_index=False).mean(numeric_only=True)

pyplot.figure()

pyplot.scatter(x="si", y="ti", data=frame)

pyplot.xlabel("Information spatiale moyenne")
pyplot.ylabel("Information temporelle moyenne")

pyplot.savefig("plots/si_ti_rockets.svg", bbox_inches="tight")
