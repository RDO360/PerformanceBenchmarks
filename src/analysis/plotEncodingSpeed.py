import argparse
from matplotlib import pyplot
import pandas

from analysis.keyPairArg import parseKeyPair
import common

# Arguments
parser = argparse.ArgumentParser(description="Plots the encoding speed in frames per second of different codecs and presets. Produces one figure for each codec and resolution combination.")
parser.add_argument("data", help="Path of the CSV file with the encoding time.")
parser.add_argument("figure", help="Path and filename of the figure.")
parser.add_argument("--heightLabels", nargs="+", help="The labels for the resolutions in key-value pairs (e.g. 0='Label 1' 500='Label 2').")
parser.add_argument("--numFrames", nargs="+", help="The number of frames in each tile in key-value pairs (e.g. tile1=500 tile2=350).")

args = parser.parse_args()
heightLabels = parseKeyPair(args.heightLabels, int, str)
numFrames = parseKeyPair(args.numFrames, str, int)

# Load data
frame = pandas.read_csv(args.data)
frame = frame.groupby(["tile", "codec", "preset", "height"], as_index=False).mean(numeric_only=True)

# Compute encoding speed
frame["speed"] = frame["tile"].map(numFrames) / frame["time"]

# Plot data
tiles = frame.tile.unique()
numTiles = len(tiles)
heights = frame.height.unique()
codecs = frame.codec.unique()

figure = pyplot.figure(figsize=(4.5, 10.5))
subfigures = figure.subfigures(numTiles, 1)

for i, tile in enumerate(tiles):
    subfigure = subfigures[i]
    subfigure.suptitle(tile, size=10)
    subfigure.subplots_adjust(bottom=0.27, top=0.81, wspace=0.1)
    subfigure.patch.set_alpha(0)

    axes = subfigure.subplots(1, len(heights), sharey=True)

    for j, height in enumerate(heights):
        axis = axes[j]

        for k, codec in enumerate(codecs):
            series = frame.query("tile == @tile and height == @height and codec == @codec")

            x = series.preset
            y = series.speed

            color = common.codecs[codec]["color"]
            marker = common.markers[k]
            
            axis.scatter(x, y, label=codec, facecolors="None", edgecolors=color, marker=marker)

# Label the axes
subfigures[numTiles - 1].supxlabel("Preset", y=-0.15)
subfigures[numTiles // 2].supylabel("Encoding speed (frames per second)", x=-0.01)

# Label the resolutions
for i, height in enumerate(heights):
    label = heightLabels[height]
    subfigures[0].axes[i].set_title(label, y=1.3)

# Build the legend
subfigures[0].axes[0].legend(title="Codec", ncol=2, bbox_to_anchor=(0.5, 1.07), bbox_transform=figure.transFigure, loc="upper center", prop={"size": 8}, title_fontsize=8)

pyplot.savefig(args.figure, bbox_inches="tight")
