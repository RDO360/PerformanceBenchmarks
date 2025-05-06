import argparse
from matplotlib import pyplot
import numpy
import pandas

xlabels = {"absoluteError": "Erreur absolue", "percentageError": "Pourcentage d'erreur", "absolutePercentageError": "Pourcentage d'erreur"}

# Arguments
parser = argparse.ArgumentParser(description="Plots the error of the visual quality, bitrate and encoding speed estimation methods.")
parser.add_argument("data", help="Path of one or more CSV files to show in the plot.")
# parser.add_argument("--labels", nargs="+", help="Label that will be in the legend for each element of data.", required=True)
parser.add_argument("predicted", help="Name of the CSV column that contains the predicted data.")
parser.add_argument("actual", help="Name of the CSV column that contains the actual data.")
parser.add_argument("method", choices=["absoluteError", "percentageError", "absolutePercentageError"], help="Whether to compute the absolute error or the percentage error.")
parser.add_argument("figure", help="Where to write the figure.")
# parser.add_argument("--xstep", type=int, help="The step for the x scale (error scale).")
# parser.add_argument("--removelq", type=int, help="The name of the low quality representation to remove from the figure (e.g., for the bitrate estimation).")

args = parser.parse_args()

maxError = 0
pyplot.figure()

frame = pandas.read_csv(args.data)

# Remove the data of the low quality representation
# if (args.removelq) :
    # frame = frame.query("representation != @args.removelq")

if (args.method == "absoluteError"):
    # Compute the absolute difference between the predicted values and the actual values
    frame["difference"] = abs(frame[args.predicted] - frame[args.actual])
elif (args.method == "percentageError"):
    # Compute the percentage error between the predicted values and the actual values
    frame["difference"] = ((frame[args.predicted] - frame[args.actual]) / frame[args.actual]) * 100
elif (args.method == "absolutePercentageError"):
    # Compute the absolute percentage error between the predicted values and the actual values
    frame["difference"] = abs(((frame[args.predicted] - frame[args.actual]) / frame[args.actual]) * 100)

frame.groupby(["tile", "codec", "preset", "qp", "height"], as_index=False).mean(numeric_only=True).to_csv("data/excel.csv")

print(frame.groupby("tile", as_index=False).mean(numeric_only=True))

# maxError = max(maxError, frame.difference.max())
# nbPredictions = len(frame.index)

n, bins, patches = pyplot.hist(frame.difference, cumulative=True, density=1, bins=100, histtype="step", linewidth=2)

# Remove the right line that is added at the end of the histogram
patches[0].set_xy(patches[0].get_xy()[:-1])

pyplot.grid(True)

# pyplot.xlabel(xlabels[args.method])

# if (args.xstep):
    # pyplot.xticks(numpy.arange(maxError, step=args.xstep))

pyplot.ylabel("Fréquences cumulées")
pyplot.yticks(numpy.arange(1.1, step=0.1))

# pyplot.show()
pyplot.savefig(args.figure, bbox_inches="tight")
