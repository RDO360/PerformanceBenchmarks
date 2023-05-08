import pandas
from matplotlib import pyplot

video_frames = 3632

frame = pandas.read_csv("data/encodingSpeedRockets1_28.csv")

frame = frame.groupby(["codec", "effort", "cq", "height"], as_index=False).mean(numeric_only=True)

frame["speed"] = video_frames / frame["time"]

codecs = {"hevc_nvenc", "h264_nvenc"}
heights = {0, 320}

efforts = {"p1": "C0", "p2": "C1", "p3": "C2", "p4": "C3", "p5": "C4", "p6": "C5", "p7": "C7"}

min_speed = frame["speed"].min() - 50
max_speed = frame["speed"].max() + 50

for codec in codecs:
    for height in heights:
        pyplot.figure()

        for effort in efforts:

            series = frame.query("codec == @codec & effort == @effort & height == @height")
            x = series["cq"]
            y = series["speed"]

            pyplot.scatter(x=x, y=y, label=effort, facecolors='None', edgecolors=efforts[effort])

        pyplot.xlabel("Facteur de qualité")
        pyplot.xticks(frame["cq"].unique())

        pyplot.ylabel("Vitesse d'encodage (images par seconde)")
        pyplot.ylim(ymin=min_speed, ymax=max_speed)

        pyplot.legend(loc="upper left", bbox_to_anchor=(1, 1))
        pyplot.savefig(f"plots/encoding_speed_codec_{codec}_height_{height}.svg", bbox_inches="tight")
