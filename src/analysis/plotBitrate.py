import pandas
from matplotlib import pyplot

frame = pandas.read_parquet("data/bitrateVmafRockets.parquet")

frame = frame.groupby(["codec", "effort", "cq", "height"], as_index=False).mean(numeric_only=True)

frame.bitrate = frame.bitrate.div(1000 * 1000)

codecs = {"hevc_nvenc", "h264_nvenc"}
heights = {0, 320}

efforts = {"p1": "C0", "p2": "C1", "p3": "C2", "p4": "C3", "p5": "C4", "p6": "C5", "p7": "C7"}

minBitrate = frame.bitrate.min() - 0.5
maxBitrate = frame.bitrate.max() + 0.5

for codec in frame.codec.unique():
    for height in frame.height.unique():
        pyplot.figure()

        for effort in frame.effort.unique():
            series = frame.query("codec == @codec & height == @height & effort == @effort")
            x = series.cq
            y = series.bitrate

            pyplot.scatter(x, y, label=effort, facecolors="none", edgecolors=efforts[effort])
        
        pyplot.xlabel("Facteur de qualité")
        pyplot.xticks(frame.cq.unique())

        pyplot.ylabel("Débit (Mbps)")
        pyplot.ylim(ymin=minBitrate, ymax=maxBitrate)

        pyplot.legend(title="Effort")
        pyplot.savefig(f"plots/bitrate_codec_{codec}_height_{height}.svg", bbox_inches="tight")
