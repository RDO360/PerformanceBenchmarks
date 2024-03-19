import argparse
from matplotlib import pyplot
import pandas

from common import presets

# Arguments
parser = argparse.ArgumentParser(description="Plots the bitrate in Mbps of different codecs and presets. Produces one figure for each codec and resolution combination.")
parser.add_argument("data", help="Path of the CSV file with the bitrate and the distortion.")
parser.add_argument("figure", nargs="+", help="Paths and filenames of the figures. There must be one path per combination of codec and resolution in the data.")

args = parser.parse_args()

# Load data
frame = pandas.read_csv(args.data)
frame = frame.groupby(["codec", "preset", "cq", "height"], as_index=False).mean(numeric_only=True)
frame.bitrate = frame.bitrate.div(1000 * 1000)

minBitrate = frame.bitrate.min() - 0.5
maxBitrate = frame.bitrate.max() + 0.5

i = 0

for codec in frame.codec.unique():
    for height in frame.height.unique():
        pyplot.figure()

        for preset in frame.preset.unique():
            series = frame.query("codec == @codec & height == @height & preset == @preset")
            x = series.cq
            y = series.bitrate

            pyplot.scatter(x, y, label=preset, facecolors="none", edgecolors=presets[preset]["color"])
        
        pyplot.xlabel("Facteur de qualité")
        pyplot.xticks(frame.cq.unique())

        pyplot.ylabel("Débit (Mbps)")
        pyplot.ylim(ymin=minBitrate, ymax=maxBitrate)

        pyplot.legend(title="Préréglage")
        pyplot.savefig(args.figure[i], bbox_inches="tight")

        i += 1
