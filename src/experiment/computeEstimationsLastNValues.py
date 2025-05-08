import argparse
import pandas

# Arguments
parser = argparse.ArgumentParser(description="Estimates the visual quality, bitrate and encoding speed of the segments.")
parser.add_argument("data", help="Path and filename of the CSV file containing the data.")
parser.add_argument("numSegments", type=int, help="The number of previous segments used to estimate the visual quality.")
parser.add_argument("results", help="Where to write the CSV results.")

args = parser.parse_args()

# Load the data
data = pandas.read_csv(args.data)

# Estimate the visual quality
data["predictedVmafMean"] = data.groupby(["tile", "codec", "preset", "qp", "height"], as_index=False)["vmafMean"].transform(lambda x: x.rolling(window=args.numSegments, min_periods=1, closed="left").mean())

# Save the data
data.to_csv(args.results, index=False)
