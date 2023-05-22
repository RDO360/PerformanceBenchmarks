import pandas
from matplotlib import pyplot
import math
import numpy

from common import presets

frame = pandas.read_csv("data/rocketsbitrateVmaf.csv")

frame = frame.groupby(["codec", "preset", "cq", "height"], as_index=False).mean(numeric_only=True)

minVmaf = max(
    math.floor(frame.vmafMean.min() - 2),
    0
)

maxVmaf = min(
    math.ceil(frame.vmafMean.max() + 2),
    100
)

yticks = numpy.arange(minVmaf, maxVmaf, step=2)

for codec in frame.codec.unique():
    for height in frame.height.unique():
        k = -3

        pyplot.figure()

        for preset in frame.preset.unique():
            series = frame.query("codec == @codec & height == @height & preset == @preset")

            x = series["cq"]
            x += 0.1 * k
            y = series["vmafMean"]
            
            pyplot.scatter(x=x, y=y, label=preset, facecolors="none", edgecolors=presets[preset]["color"])
            pyplot.xlabel("Facteur de qualité")
            pyplot.xticks(frame["cq"].unique())

            pyplot.ylabel("VMAF moyen")
            pyplot.yticks(yticks)

            k += 1
        
        pyplot.legend(title="Préréglage")
        pyplot.savefig(f"plots/vmaf_codec_{codec}_height_{height}.svg", bbox_inches="tight")
