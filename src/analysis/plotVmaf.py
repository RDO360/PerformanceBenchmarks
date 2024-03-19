import argparse
import math
from matplotlib import pyplot
import numpy
import pandas

from common import presets

# Arguments
parser = argparse.ArgumentParser(description="Plots the VMAF of different codecs and presets. Produces one figure for each codec and resolution combination.")
parser.add_argument("data", help="Path of the CSV file with the bitrate and the distortion.")
parser.add_argument("figure", nargs="+", help="Paths and filenames of the figures. There must be one path per combination of codec and resolution in the data.")

args = parser.parse_args()

# Load data
frame = pandas.read_csv(args.data)
frame = frame.groupby(["codec", "preset", "cq", "height"], as_index=False).mean(numeric_only=True)

minVmaf = max(
    math.floor(frame.vmafMean.min() - 2),
    0
)

maxVmaf = min(
    math.ceil(frame.vmafMean.max() + 2),
    100
)

yticks = numpy.arange(minVmaf, maxVmaf, step=2)

i = 0

for codec in frame.codec.unique():
    for height in frame.height.unique():
        k = -3

        pyplot.figure()

        for preset in frame.preset.unique():
            series = frame.query("codec == @codec & height == @height & preset == @preset")

            x = series["cq"]
            x += 0.1 * k
            y = series["vmafMean"]
            
            pyplot.scatter(x=x, y=y, label=preset, facecolors="none", edgecolors=presets[preset]["color"])
            pyplot.xlabel("Facteur de qualité")
            pyplot.xticks(frame["cq"].unique())

            pyplot.ylabel("VMAF moyen")
            pyplot.yticks(yticks)

            k += 1

        pyplot.legend(title="Préréglage", loc="lower left")
        pyplot.savefig(args.figure[i], bbox_inches="tight")

        i += 1
