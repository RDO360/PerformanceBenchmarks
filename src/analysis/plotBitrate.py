import pandas
from matplotlib import pyplot

from common import presets

frame = pandas.read_csv("data/rocketsbitrateVmaf.csv")

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
