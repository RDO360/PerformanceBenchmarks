import argparse
from matplotlib import pyplot
import pandas

from src.analysis.common.keyPairArg import parseKeyPair
from src.analysis.common import common
from src.analysis.benchmark.bdRate import bdRate

# Arguments
parser = argparse.ArgumentParser(description="Plots the BD-rate performance for all tiles, codecs and presets.")
parser.add_argument("data", help="Path of the CSV file with the bitrate and the distortion.")
parser.add_argument("anchorCodec", help="The reference codec to calculate the BD-rate.")
parser.add_argument("anchorPreset", help="The reference preset to calculate the BD-rate.")
parser.add_argument("figure", help="Path and filename of the figure.")
parser.add_argument("--heightLabels", nargs="+", help="The labels for the resolutions in key-value pairs (e.g. 0='Label 1' 500='Label 2').")

args = parser.parse_args()
heightLabels = parseKeyPair(args.heightLabels, int, str)

# Load data
frame = pandas.read_csv(args.data)
frame = frame.groupby(["tile", "codec", "preset", "qp", "height"], as_index=False).mean(numeric_only=True)

# Compute BD-rate
bdRates = []

for tile in frame.tile.unique():
    for height in frame.height.unique():
        original = frame.query("tile == @tile and height == @height and codec == @args.anchorCodec and preset == @args.anchorPreset")

        for codec in frame.codec.unique():
            for preset in frame.preset.unique():
                compared = frame.query("tile == @tile and height == @height and codec == @codec and preset == @preset")

                rate = bdRate(list(original.bitrate), list(original.vmafMean), list(compared.bitrate), list(compared.vmafMean))

                bdRates.append({
                    "tile": tile,
                    "codec": codec,
                    "preset": preset,
                    "height": height,
                    "bdrate": rate
                })

bdRates = pandas.DataFrame(bdRates)

# Plot data
tiles = bdRates.tile.unique()
numTiles = len(tiles)

heights = bdRates.height.unique()

codecs = bdRates.codec.unique()

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
            series = bdRates.query("tile == @tile and height == @height and codec == @codec")

            x = series.preset.unique()
            y = series.bdrate

            color = common.codecs[codec]["color"]
            marker = common.markers[k]
            
            axis.scatter(x, y, label=codec, facecolors="None", edgecolors=color, marker=marker)

# Label the axes
subfigures[numTiles - 1].supxlabel("Preset", y=-0.15)
subfigures[numTiles // 2].supylabel("BD-rate (%)", x=-0.01)

# Label the resolutions
for i, height in enumerate(heights):
    label = heightLabels[height]
    subfigures[0].axes[i].set_title(label, y=1.3)

# Build the legend
subfigures[0].axes[0].legend(title="Codec", ncol=2, bbox_to_anchor=(0.5, 1.07), bbox_transform=figure.transFigure, loc="upper center", prop={"size": 8}, title_fontsize=8)

pyplot.savefig(args.figure, bbox_inches="tight")
