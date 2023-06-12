from matplotlib import pyplot
import os
import pandas

from common import presets

# Create the directory where the plots will be saved
os.makedirs("plots", exist_ok=True)

frame = pandas.read_csv("data/rocketsBitrateVmaf.csv")

frame = frame.groupby(["codec", "preset", "cq", "height"], as_index=False).mean(numeric_only=True)

frame.bitrate = frame.bitrate.div(1000 * 1000)

minBitrate = frame.bitrate.min() - 0.5
maxBitrate = frame.bitrate.max() + 0.5

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
        pyplot.savefig(f"plots/bitrate_codec_{codec}_height_{height}.svg", bbox_inches="tight")
