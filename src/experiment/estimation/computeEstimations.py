import argparse
import pandas

# Arguments
parser = argparse.ArgumentParser(description="Estimates the visual quality, bitrate and encoding speed of the segments.")
parser.add_argument("bitrateVisualQuality", help="Path and filename of the CSV file containing the bitrate and the visual quality of all segments (training and simulation).")
# parser.add_argument("encodingSpeed", help="Path and filename of the CSV file containing the encoding speed of the segments.")
parser.add_argument("numSegments", type=int, help="The number of segments used to estimate the visual quality.")
parser.add_argument("results", help="Where to write the CSV results.")

args = parser.parse_args()

# Load the data
bitrateVisualQuality = pandas.read_csv(args.bitrateVisualQuality)
# encodingSpeed = pandas.read_csv(args.encodingSpeed)

# Extract the segments used for estimation
grouped = bitrateVisualQuality.groupby(["tile", "codec", "preset", "qp", "height"], as_index=False)

training = grouped.head(args.numSegments)
evaluation = bitrateVisualQuality[~bitrateVisualQuality.index.isin(training.index)]

# Estimate the visual quality
predictedVisualQuality = training.groupby(["tile", "codec", "preset", "qp", "height"], as_index=False).mean(numeric_only=True)
predictedVisualQuality = predictedVisualQuality.rename(columns={"vmafMean": "predictedVmafMean"})

evaluation = evaluation.merge(predictedVisualQuality[["tile", "codec", "preset", "qp", "height", "predictedVmafMean"]], on=["tile", "codec", "preset", "qp", "height"])

# Estimate the bitrate
"""lowQuality = bitrateDistortion.representation.max()

lq = training.query("representation == @lowQuality")

test = training.merge(lq[["tile", "segment", "bitrate"]], on=["tile", "segment"])
test["factor"] = test.bitrate_x / test.bitrate_y
test = test.groupby(["tile", "representation"], as_index=False).mean(numeric_only=True)

evaluation = evaluation.merge(test[["tile", "representation", "factor"]], on=["tile", "representation"])

lq = evaluation.query("representation == @lowQuality")
evaluation = evaluation.merge(lq[["tile", "segment", "bitrate"]], on=["tile", "segment"], suffixes=["", "_lq"])
evaluation["predictedBitrate"] = evaluation.factor * evaluation.bitrate_lq
evaluation.predictedBitrate = evaluation.predictedBitrate.round(0).astype("int")

evaluation = evaluation.drop(columns=["factor", "bitrate_lq"])"""

# Estimate the encoding time in ms
"""lowestSpeed = encodingSpeed.groupby(["tile", "representation"]).min()

encodingTime = (int) (args.framesPerSegment) / lowestSpeed
encodingTime = encodingTime.rename(columns={"speed": "predictedEncodingTime"})
encodingTime *= 1000
encodingTime = encodingTime.round(0)
encodingTime.predictedEncodingTime = encodingTime.predictedEncodingTime.astype(int)

evaluation = evaluation.merge(encodingTime, on=["tile", "representation"])"""

# Reset the segments number
# evaluation.segment -= evaluation.segment.min()

# Save the data
evaluation.to_csv(args.results, index=False)
