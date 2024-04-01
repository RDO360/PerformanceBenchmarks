import argparse
from matplotlib import pyplot
import pandas

labels = {0: "1280 par 640", 320: "640 par 320"}

# Arguments
parser = argparse.ArgumentParser(description="Plots the standard deviation of the VMAF or the bitrate of different codecs and presets.")
parser.add_argument("data", help="Path of the CSV file with the bitrate and the distortion.")
parser.add_argument("ydata", choices=["vmafMean", "bitrate"], help="Whether to use the VMAF or the bitrate to calculate the standard deviation.")
parser.add_argument("ylabel", help="The label to use for the y axis in the figure.")
parser.add_argument("figure", help="Path of the resulting figure. Image type is determined by the extension.")

args = parser.parse_args()

# Load data
frame = pandas.read_csv(args.data)
frame.bitrate = frame.bitrate.div(1000 * 1000)
frame = frame.groupby(["cq", "height"], as_index=False).std(numeric_only=True)

pyplot.figure()

heights = frame.height.unique()
offset = -0.25

for height in heights:
    series = frame.query("height == @height")
    x = series.cq
    y = series[args.ydata]

    x += offset

    pyplot.bar(x, y, 0.5, label=labels[height], align="edge")

    offset += 0.5

pyplot.xlabel("Facteur de qualité")
pyplot.xticks(frame.cq.unique())

pyplot.ylabel(args.ylabel)

pyplot.legend(title="Résolution (pixels)")

pyplot.savefig(args.figure, bbox_inches="tight")
