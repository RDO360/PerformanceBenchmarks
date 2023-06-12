from matplotlib import pyplot
import os
import pandas

from common import presets

# Create the directory where the plots will be saved
os.makedirs("plots", exist_ok=True)

video_frames = 3632

frame = pandas.read_csv("data/encodingSpeedRockets.csv")

frame = frame.groupby(["codec", "preset", "cq", "height"], as_index=False).mean(numeric_only=True)

frame["speed"] = video_frames / frame.time

minSpeed = frame.speed.min() - 50
maxSpeed = frame.speed.max() + 50

for codec in frame.codec.unique():
    for height in frame.height.unique():
        pyplot.figure()

        for preset in frame.preset.unique():
            series = frame.query("codec == @codec & preset == @preset & height == @height")
            x = series.cq
            y = series.speed

            pyplot.scatter(x=x, y=y, label=preset, facecolors="None", edgecolors=presets[preset]["color"])

        pyplot.xlabel("Facteur de qualité")
        pyplot.xticks(frame.cq.unique())

        pyplot.ylabel("Vitesse d'encodage (images par seconde)")
        pyplot.ylim(ymin=minSpeed, ymax=maxSpeed)

        pyplot.legend(title="Préréglage", loc="upper left", bbox_to_anchor=(1, 1))
        pyplot.savefig(f"plots/encoding_speed_codec_{codec}_height_{height}.svg", bbox_inches="tight")
