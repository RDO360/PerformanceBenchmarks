import argparse
from matplotlib import pyplot
import pandas

# Arguments
parser = argparse.ArgumentParser(description="Plots the computing speed of VMAF according to the subsampling value.")
parser.add_argument("data", help="Path of one or more CSV files to show in the plot.")
parser.add_argument("figure", help="Path and filename of the figure.")

args = parser.parse_args()

# Load the data
frame = pandas.read_csv(args.data)

# Plot the data
pyplot.figure(figsize=(3.25, 2.5))

pyplot.bar(frame.subsampling, frame.speed)

pyplot.xticks(frame.subsampling.unique())
pyplot.xlabel("Subsampling value")
pyplot.ylabel("Speed (frames per second)")

pyplot.savefig(args.figure, bbox_inches="tight")
