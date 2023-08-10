from matplotlib import pyplot
import os
import pandas

from bdRate import bdRate
from common import codecs

# Create the directory where the plots will be saved
os.makedirs("plots", exist_ok=True)

frame = pandas.read_csv("data/rocketsBitrateVmaf.csv")

frame = frame.groupby(["tile", "codec", "preset", "height", "cq"], as_index=False).mean(numeric_only=True)

bdrates = []

for heght in frame.height.unique():
    for tile in frame.tile.unique():
        original = frame.query("tile == @tile & codec == 'h264_nvenc' & preset == 'p1' & height == @heght")
        
        for codec in frame.codec.unique():
            for preset in frame.preset.unique():
                compared = frame.query("tile == @tile & codec == @codec & preset == @preset & height == @heght")

                rate = bdRate(list(original.bitrate), list(original.vmafMean), list(compared.bitrate), list(compared.vmafMean))

                bdrates.append({
                    "tile": tile,
                    "codec": codec,
                    "preset": preset,
                    "height": heght,
                    "bdrate": rate
                })

bdrates = pandas.DataFrame(bdrates)

bdrates = bdrates.groupby(["codec", "preset", "height"], as_index=False).mean(numeric_only=True)

for height in bdrates.height.unique():
    pyplot.figure()

    for codec in bdrates.codec.unique():
        series = bdrates.query("codec == @codec & height == @height")

        x = series.preset.unique()
        y = series.bdrate
        
        pyplot.scatter(x, y, label=codec, facecolors="None", edgecolors=codecs[codec]["color"])
        
    pyplot.xlabel("Préréglage")
    pyplot.ylabel("BD-rate (%)")

    pyplot.legend(title="Codec")
    pyplot.savefig(f"plots/bd_rate_height_{height}.svg", bbox_inches="tight")
