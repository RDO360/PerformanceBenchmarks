import pandas
from matplotlib import pyplot

from bd_rate import bd_rate

frame = pandas.read_parquet("data/bitrateVmafRockets.parquet")

heights = {0, 320}
codecs = {"h264_nvenc": "C0", "hevc_nvenc": "C1"}

for height in frame.height.unique():
    original = frame.query("codec == 'h264_nvenc' & effort == 'p1' & height == @height").groupby("cq", as_index=False).mean(numeric_only=True).sort_values("bitrate", ascending=True)

    pyplot.figure()

    for codec in frame.codec.unique():
        efforts = []
        bdRates = []

        for effort in frame.effort.unique():
            efforts.append(effort)
            compared = frame.query("codec == @codec & effort == @effort & height == @height").groupby("cq", as_index=False).mean(numeric_only=True).sort_values("bitrate", ascending=True)

            bdRate = bd_rate(list(original.bitrate), list(original.psnr_mean), list(compared.bitrate), list(compared.psnr_mean))
            bdRates.append(bdRate)
        
        pyplot.scatter(x=efforts, y=bdRates, label=codec, facecolors="None", edgecolors=codecs[codec])
        
    pyplot.xlabel("Effort")
    pyplot.ylabel("BD-rate (%)")

    pyplot.legend(title="Codec")
    pyplot.savefig(f"plots/bd_rate_height_{height}.svg", bbox_inches="tight")
