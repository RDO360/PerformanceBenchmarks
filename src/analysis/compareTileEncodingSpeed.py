import pandas
from matplotlib import pyplot
from matplotlib.lines import Line2D

video_frames = 3632

frame = pandas.read_csv("data/encodingSpeedRockets.csv")

frame = frame.groupby(["tile", "codec", "effort", "cq", "height"], as_index=False).mean(numeric_only=True)

frame["speed"] = video_frames / frame.time

codecs = {"hevc_nvenc", "h264_nvenc"}
heights = {0, 320}
tiles = {"Rockets1.y4m": "+", "Rockets16.y4m": "x"}

efforts = {"p1": "C0", "p2": "C1", "p3": "C2", "p4": "C3", "p5": "C4", "p6": "C5", "p7": "C7"}

legendElements = []

for effort in frame.effort.unique():
    element = Line2D([0], [0], marker="o", color="None", markeredgecolor="None", markerfacecolor=efforts[effort], label=effort)
    legendElements.append(element)

min_speed = frame["speed"].min() - 50
max_speed = frame["speed"].max() + 50

for codec in frame.codec.unique():
    for height in frame.height.unique():
        pyplot.figure()

        for effort in frame.effort.unique():
            for tile in tiles:
                series = frame.query("tile == @tile & codec == @codec & effort == @effort & height == @height")
                x = series.cq
                y = series.speed
                
                scatter = pyplot.scatter(x=x, y=y, label=effort, marker=tiles[tile], c=efforts[effort])

        pyplot.xlabel("Facteur de qualité")
        pyplot.xticks(frame.cq.unique())

        pyplot.ylabel("Vitesse d'encodage (images par seconde)")
        pyplot.ylim(ymin=min_speed, ymax=max_speed)
        
        pyplot.legend(handles=legendElements, title="Effort", loc="upper left", bbox_to_anchor=(1, 1))
        pyplot.savefig(f"plots/compare_encoding_speed_codec_{codec}_height_{height}.svg", bbox_inches="tight")
