from matplotlib import pyplot
import os
import pandas

from bdRate import bdRate
from common import codecs

# Create the directory where the plots will be saved
os.makedirs("plots", exist_ok=True)

frame = pandas.read_csv("data/rocketsBitrateVmaf.csv")

for height in frame.height.unique():
    original = frame.query("codec == 'h264_nvenc' & preset == 'p1' & height == @height").groupby("cq", as_index=False).mean(numeric_only=True).sort_values("bitrate", ascending=True)

    pyplot.figure()

    for codec in frame.codec.unique():
        presets = []
        bdRates = []

        for preset in frame.preset.unique():
            presets.append(preset)
            compared = frame.query("codec == @codec & preset == @preset & height == @height").groupby("cq", as_index=False).mean(numeric_only=True).sort_values("bitrate", ascending=True)

            rate = bdRate(list(original.bitrate), list(original.vmafMean), list(compared.bitrate), list(compared.vmafMean))
            bdRates.append(rate)
        
        pyplot.scatter(x=presets, y=bdRates, label=codec, facecolors="None", edgecolors=codecs[codec]["color"])
        
    pyplot.xlabel("Préréglage")
    pyplot.ylabel("BD-rate (%)")

    pyplot.legend(title="Codec")
    pyplot.savefig(f"plots/bd_rate_height_{height}.svg", bbox_inches="tight")
