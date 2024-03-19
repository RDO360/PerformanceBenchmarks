import argparse
from matplotlib import pyplot
import pandas

from bdRate import bdRate
from common import codecs

# Arguments
parser = argparse.ArgumentParser(description="Plots the BD-rate of different codecs and presets for a specific resolution.")
parser.add_argument("data", help="Path of the CSV file with the bitrate and the distortion.")
parser.add_argument("height", type=int, help="The height in pixels of the data to consider.")
parser.add_argument("anchorCodec", help="The reference codec to calculate the BD-rate.")
parser.add_argument("anchorPreset", help="The reference preset to calculate the BD-rate.")
parser.add_argument("figure", help="Where to write the figure")

args = parser.parse_args()

# Load data
frame = pandas.read_csv(args.data)
frame = frame.query("height == @args.height")
frame = frame.groupby(["tile", "codec", "preset", "cq"], as_index=False).mean(numeric_only=True)

bdrates = []

for tile in frame.tile.unique():
    original = frame.query("tile == @tile & codec == @args.anchorCodec & preset == @args.anchorPreset")
    
    for codec in frame.codec.unique():
        for preset in frame.preset.unique():
            compared = frame.query("tile == @tile & codec == @codec & preset == @preset")

            rate = bdRate(list(original.bitrate), list(original.vmafMean), list(compared.bitrate), list(compared.vmafMean))

            bdrates.append({
                "tile": tile,
                "codec": codec,
                "preset": preset,
                "bdrate": rate
            })

bdrates = pandas.DataFrame(bdrates)
bdrates = bdrates.groupby(["codec", "preset"], as_index=False).mean(numeric_only=True)

pyplot.figure()

for codec in bdrates.codec.unique():
    series = bdrates.query("codec == @codec")

    x = series.preset.unique()
    y = series.bdrate
    
    pyplot.scatter(x, y, label=codec, facecolors="None", edgecolors=codecs[codec]["color"])
    
pyplot.xlabel("Préréglage")
pyplot.ylabel("BD-rate (%)")

pyplot.legend(title="Codec")
pyplot.savefig(args.figure, bbox_inches="tight")
