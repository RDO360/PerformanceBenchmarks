import pandas

frame = pandas.read_csv("data/testParallel.csv")

# Ignore rows where the speed is zero
frame = frame[frame.speed != 0]

# Keep the same amount of rows for each group
groups = frame.groupby(["tile", "repetition", "codec", "preset", "cq"], as_index=False)

groupSizes = groups.size()
minGroupSize = min(groupSizes["size"])

frame = groups.head(minGroupSize)

# Calculate the mean speed and drop the repetition column
frame = frame.groupby(["tile", "codec", "preset", "cq"], as_index=False).mean(numeric_only=True).drop("repetition", axis=1)

# Calculate the ratios
totalSpeed = frame.speed.sum()
frame["ratio"] = frame.speed / totalSpeed

print(frame)
