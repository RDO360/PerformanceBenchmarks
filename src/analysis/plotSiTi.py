import argparse
from matplotlib import pyplot
import os
import pandas

# Arguments
parser = argparse.ArgumentParser(description="Plots the spatial and temporal information of videos.")
parser.add_argument("data", help="Path of the CSV file with the spatial and temporal information for each video.")
parser.add_argument("figure", help="Path and filename of the figure.")

args = parser.parse_args()

# Load data
frame = pandas.read_csv(args.data)
frame = frame.groupby("input_file", as_index=False).mean(numeric_only=True)

pyplot.figure()

pyplot.scatter(x="si", y="ti", data=frame)

pyplot.xlabel("Information spatiale moyenne")
pyplot.ylabel("Information temporelle moyenne")

pyplot.savefig(args.figure, bbox_inches="tight")
