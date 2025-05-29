import argparse
import pandas

# Arguments
parser = argparse.ArgumentParser(description="Estimates the visual quality, bitrate and encoding speed of the segments.")
parser.add_argument("data", help="Path and filename of the CSV file containing the bitrate and the visual quality of all segments (training and simulation).")
parser.add_argument("actual", help="Name of the CSV column that contains the values used for prediction.")
parser.add_argument("predicted", help="Name of the CSV column that will contain the predicted values.")
parser.add_argument("numSegments", type=int, help="The number of segments used to estimate the visual quality.")
parser.add_argument("results", help="Where to write the CSV results.")

args = parser.parse_args()

# Load the data
data = pandas.read_csv(args.data)

# Extract the segments used for estimation
grouped = data.groupby(["tile", "codec", "preset", "qp", "height"], as_index=False)

training = grouped.head(args.numSegments)
evaluation = data[~data.index.isin(training.index)]

# Estimate
predicted = training.groupby(["tile", "codec", "preset", "qp", "height"], as_index=False).mean(numeric_only=True)
predicted = predicted.rename(columns={args.actual: args.predicted})

evaluation = evaluation.merge(predicted[["tile", "codec", "preset", "qp", "height", args.predicted]], on=["tile", "codec", "preset", "qp", "height"])

# Save the data
evaluation.to_csv(args.results, index=False)
