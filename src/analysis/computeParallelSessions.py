import pandas

video_frames = 3632

frame = pandas.read_csv("data/rocketsParallelSessions.csv")

frame = frame.groupby(["repetition", "tile"], as_index=False).mean(numeric_only=True)

frame["speed"] = video_frames / frame.time

print(frame)
print(frame.groupby(["repetition"], as_index=False).sum(numeric_only=True))
