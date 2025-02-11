import argparse
from matplotlib import pyplot
import pandas

from bdRate import bdRate
from common import codecs, markers

# Arguments
parser = argparse.ArgumentParser(description="Plots the BD-rate performance for all tiles, codecs and presets.")
parser.add_argument("data", help="Path of the CSV file with the bitrate and the distortion.")
parser.add_argument("anchorCodec", help="The reference codec to calculate the BD-rate.")
parser.add_argument("anchorPreset", help="The reference preset to calculate the BD-rate.")
parser.add_argument("figure", help="Where to write the figure")
parser.add_argument("heightsTitles", nargs="+", help="The labels for the resolutions, in order in which they appear in the data.")

args = parser.parse_args()

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
numTiles = len(bdRates.tile.unique())
numHeights = len(bdRates.height.unique())
numCodecs = len(bdRates.codec.unique())

figure = pyplot.figure(figsize=(4.5, 10.5))
subfigures = figure.subfigures(numTiles, 1)

i = 0
k = 0

for tile in bdRates.tile.unique():
    subfigure = subfigures[i]
    subfigure.suptitle(tile, size=10)
    subfigure.subplots_adjust(bottom=0.27, top=0.81, wspace=0.1)
    subfigure.patch.set_alpha(0)

    j = 0
    axes = subfigure.subplots(1, numHeights, sharey=True)

    for height in bdRates.height.unique():
        axis = axes[j]
        j += 1

        for codec in bdRates.codec.unique():
            series = bdRates.query("tile == @tile and height == @height and codec == @codec")

            x = series.preset.unique()
            y = series.bdrate

            marker = markers[k % numCodecs]
            
            axis.scatter(x, y, label=codec, facecolors="None", edgecolors=codecs[codec]["color"], marker=marker)

            k += 1

    i += 1

subfigures[numTiles - 1].supxlabel("Preset", y=-0.15)
subfigures[numTiles // 2].supylabel("Rate-distortion (%)", x=-0.01)

# Set the resolutions labels
for i in range(0, numHeights):
    subfigures[0].axes[i].set_title(args.heightsTitles[i], y=1.3)

subfigures[0].axes[0].legend(title="Codec", ncol=2, bbox_to_anchor=(0.5, 1.07), bbox_transform=figure.transFigure, loc="upper center", prop={"size": 8}, title_fontsize=8)

pyplot.savefig(args.figure, bbox_inches="tight")
