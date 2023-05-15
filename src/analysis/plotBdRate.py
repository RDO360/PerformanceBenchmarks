import pandas
from matplotlib import pyplot

from bdRate import bdRate
from common import codecs

frame = pandas.read_parquet("data/bitrateVmafRockets.parquet")

for height in frame.height.unique():
    original = frame.query("codec == 'h264_nvenc' & preset == 'p1' & height == @height").groupby("cq", as_index=False).mean(numeric_only=True).sort_values("bitrate", ascending=True)

    pyplot.figure()

    for codec in frame.codec.unique():
        presets = []
        bdRates = []

        for preset in frame.preset.unique():
            presets.append(preset)
            compared = frame.query("codec == @codec & preset == @preset & height == @height").groupby("cq", as_index=False).mean(numeric_only=True).sort_values("bitrate", ascending=True)

            rate = bdRate(list(original.bitrate), list(original.psnr_mean), list(compared.bitrate), list(compared.psnr_mean))
            bdRates.append(rate)
        
        pyplot.scatter(x=presets, y=bdRates, label=codecs[codec]["niceName"], facecolors="None", edgecolors=codecs[codec]["color"])
        
    pyplot.xlabel("Préréglage")
    pyplot.ylabel("BD-rate (%)")

    pyplot.legend(title="Codec")
    pyplot.savefig(f"plots/bd_rate_height_{height}.svg", bbox_inches="tight")
