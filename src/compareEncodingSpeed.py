import pandas
from matplotlib import pyplot

video_frames = 3632

frame = pandas.read_csv("data/encodingSpeedRockets1_28.csv")

frame = frame.groupby(["tile", "codec", "effort", "cq", "height"], as_index=False).mean(numeric_only=True)

frame["speed"] = video_frames / frame["time"]

#print(frame)

tile1 = frame.query("tile == 'Rockets1.y4m'")
tile16 = frame.query("tile == 'Rockets16.y4m'")

#print(tile1)
#print(tile16)
