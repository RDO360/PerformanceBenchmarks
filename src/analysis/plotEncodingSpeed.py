import argparse
from matplotlib import pyplot
import pandas

from common import presets

# Arguments
parser = argparse.ArgumentParser(description="Plots the encoding speed in frames per second of different codecs and presets. Produces one figure for each codec and resolution combination.")
parser.add_argument("data", help="Path of the CSV file with the encoding time.")
parser.add_argument("numFrames", type=int, help="The number of frames in the video sequences.")
parser.add_argument("figure", nargs="+", help="Paths and filenames of the figures. There must be one path per combination of codec and resolution in the data.")

args = parser.parse_args()

# Load data
frame = pandas.read_csv(args.data)
frame = frame.groupby(["codec", "preset", "cq", "height"], as_index=False).mean(numeric_only=True)
frame["speed"] = args.numFrames / frame.time

minSpeed = frame.speed.min() - 50
maxSpeed = frame.speed.max() + 50

i = 0

for codec in frame.codec.unique():
    for height in frame.height.unique():
        pyplot.figure()

        for preset in frame.preset.unique():
            series = frame.query("codec == @codec & preset == @preset & height == @height")
            x = series.cq
            y = series.speed

            pyplot.scatter(x=x, y=y, label=preset, facecolors="None", edgecolors=presets[preset]["color"])

        pyplot.xlabel("Facteur de qualité")
        pyplot.xticks(frame.cq.unique())

        pyplot.ylabel("Vitesse d'encodage (images par seconde)")
        pyplot.ylim(ymin=minSpeed, ymax=maxSpeed)

        pyplot.legend(title="Préréglage", loc="upper left", bbox_to_anchor=(1, 1))
        pyplot.savefig(args.figure[i], bbox_inches="tight")

        i += 1
