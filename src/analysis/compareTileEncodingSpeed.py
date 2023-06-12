from matplotlib import pyplot
from matplotlib.lines import Line2D
import os
import pandas

from common import presets, compareEncodingSpeed

# Create the directory where the plots will be saved
os.makedirs("plots", exist_ok=True)

video_frames = 3632

frame = pandas.read_csv("data/encodingSpeedRockets.csv")

frame = frame.groupby(["tile", "codec", "preset", "cq", "height"], as_index=False).mean(numeric_only=True)

frame["speed"] = video_frames / frame.time

legendElements = []

for preset in frame.preset.unique():
    element = Line2D([0], [0], marker="o", color="None", markeredgecolor="None", markerfacecolor=presets[preset]["color"], label=preset)
    legendElements.append(element)

min_speed = frame["speed"].min() - 50
max_speed = frame["speed"].max() + 50

for codec in frame.codec.unique():
    for height in frame.height.unique():
        pyplot.figure()

        for preset in frame.preset.unique():
            for tile in compareEncodingSpeed:
                series = frame.query("tile == @tile & codec == @codec & preset == @preset & height == @height")
                x = series.cq
                y = series.speed
                
                scatter = pyplot.scatter(x=x, y=y, label=preset, marker=compareEncodingSpeed[tile]["marker"], c=presets[preset]["color"])

        pyplot.xlabel("Facteur de qualité")
        pyplot.xticks(frame.cq.unique())

        pyplot.ylabel("Vitesse d'encodage (trames par seconde)")
        pyplot.ylim(ymin=min_speed, ymax=max_speed)
        
        pyplot.legend(handles=legendElements, title="Préréglage", loc="upper left", bbox_to_anchor=(1, 1))
        pyplot.savefig(f"plots/compare_encoding_speed_codec_{codec}_height_{height}.svg", bbox_inches="tight")
