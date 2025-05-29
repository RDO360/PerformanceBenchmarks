import argparse
from matplotlib import pyplot, ticker
import numpy
import pandas

xlabels = {"absoluteError": "Absolute Error", "percentageError": "Percentage Error", "absolutePercentageError": "Absolute Percentage Error"}

# Arguments
parser = argparse.ArgumentParser(description="Plots the error of the visual quality, bitrate and encoding speed estimation methods.")
parser.add_argument("data", help="Path of one or more CSV files to show in the plot.")
parser.add_argument("method", choices=["absoluteError", "percentageError", "absolutePercentageError"], help="The type of error to compute.")
parser.add_argument("predicted", help="Name of the CSV column that contains the predicted values.")
parser.add_argument("actual", help="Name of the CSV column that contains the actual values.")
parser.add_argument("figure", help="Path and filename of the figure.")
parser.add_argument("--xstep", type=int, help="The step frequency for the x axis.")
parser.add_argument("--x-units", dest="xunits", help="The units of the x-axis.")
parser.add_argument("--split", help="The column name used to split the data into labels.")
parser.add_argument("--legend", help="The title of the legend.")

args = parser.parse_args()

# Load the data
frame = pandas.read_csv(args.data)

frame = frame.dropna()

# Compute the error
if (args.method == "absoluteError"):
    # Compute the absolute difference between the predicted values and the actual values
    frame["difference"] = abs(frame[args.predicted] - frame[args.actual])
elif (args.method == "percentageError"):
    # Compute the percentage error between the predicted values and the actual values
    frame["difference"] = ((frame[args.predicted] - frame[args.actual]) / frame[args.actual]) * 100
elif (args.method == "absolutePercentageError"):
    # Compute the absolute percentage error between the predicted values and the actual values
    frame["difference"] = abs(((frame[args.predicted] - frame[args.actual]) / frame[args.actual]) * 100)

# Plot the data
pyplot.figure(figsize=(3.25, 2.5))

if (args.split):
    for value in frame[args.split].unique():
        series = frame.query(f"{args.split} == @value")

        n, bins, patches = pyplot.hist(series.difference, cumulative=True, density=True, bins=100, histtype="step", linewidth=1, label=value)

        # Remove the right line that is added at the end of the histogram
        patches[0].set_xy(patches[0].get_xy()[:-1])
else:
    n, bins, patches = pyplot.hist(frame.difference, cumulative=True, density=True, bins=100, histtype="step", linewidth=1)

    # Remove the right line that is added at the end of the histogram
    patches[0].set_xy(patches[0].get_xy()[:-1])

pyplot.grid(True)

# Labels and legend
label = xlabels[args.method]

if (args.xunits):
    label += f" ({args.xunits})"

pyplot.xlabel(label)

if (args.xstep):
    pyplot.gca().xaxis.set_major_locator(ticker.MultipleLocator(args.xstep))

pyplot.ylabel("Cumulative Probability")
pyplot.yticks(numpy.arange(0, 1.1, step=0.2))

if args.split:
    pyplot.legend(title=args.legend, bbox_to_anchor=(1, 1), loc="upper left", prop={"size": 8}, title_fontsize=8)

pyplot.savefig(args.figure, bbox_inches="tight")
