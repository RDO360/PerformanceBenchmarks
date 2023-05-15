import pandas
from matplotlib import pyplot
import math
import numpy

from common import presets

frame = pandas.read_parquet("data/bitrateVmafRockets.parquet")

vmaf_q5 = frame.groupby(["codec", "preset", "cq", "height"], as_index=False).quantile(0.05, numeric_only=True)["vmaf_min"]

vmaf_q100 = frame.groupby(["codec", "preset", "cq", "height"], as_index=False).quantile(1, numeric_only=True)["vmaf_max"]

frame = frame.groupby(["codec", "preset", "cq", "height"], as_index=False)["vmaf_mean"].mean()
frame["vmaf_q5"] = vmaf_q5
frame["vmaf_q100"] = vmaf_q100

minVmaf = max(
    math.floor(frame.vmaf_q5.min() - 2),
    0
)

maxVmaf = min(
    math.ceil(frame.vmaf_q100.max() + 2),
    100
)

yticks = numpy.arange(minVmaf, maxVmaf, step=5)

for codec in frame.codec.unique():
    for height in frame.height.unique():
        k = -3

        pyplot.figure()

        for preset in frame.preset.unique():
            series = frame.query("codec == @codec & height == @height & preset == @preset")

            x = series["cq"]
            x += 0.1 * k
            y = series["vmaf_mean"]

            y_error_min = y - series["vmaf_q5"]
            y_error_max = series["vmaf_q100"] - y

            pyplot.errorbar(x, y, yerr=[y_error_min, y_error_max], label=preset, fmt="o", color=presets[preset]["color"], markerfacecolor="none")
            pyplot.xlabel("Facteur de qualité")
            pyplot.xticks(frame["cq"].unique())

            pyplot.ylabel("VMAF")
            pyplot.yticks(yticks)

            k += 1
        
        pyplot.legend(title="Préréglage", loc="upper left", bbox_to_anchor=(1, 1))
        pyplot.savefig(f"plots/vmaf_mean_q5_q100_codec_{codec}_height_{height}.svg", bbox_inches="tight")
