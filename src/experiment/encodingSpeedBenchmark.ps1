param(
	# An array of tiles to encode
	[Parameter(Mandatory=$true)][String[]] $tiles,
	# An array of codecs. Codecs must be supported by the hardware encoder
	[Parameter(Mandatory=$true)][String[]] $codecs,
	# An array of efforts (presets)
	[Parameter(Mandatory=$true)][String[]] $efforts,
	# An array of constant quality factor (CRF) between 0 and 51
	[Parameter(Mandatory=$true)][int[]] $cqs,
	# An array of heights. The aspect ratio is kept. An height of 0 means no resizing
	[Parameter(Mandatory=$true)][int[]] $heights,
	# The number of times to repeat each encoding
	[Parameter(Mandatory=$true)][int] $repetitions,
	# The duration in seconds of each segment
	[Parameter(Mandatory=$true)][int] $segmentTime,
	# Inserts a key frame every $segmentGOP frames
	[Parameter(Mandatory=$true)][int] $segmentGOP,
	# The directory to save the temporary segments
	[Parameter(Mandatory=$true)][String] $segmentDirectory,
	# The csv file where the data will be saved to
	[Parameter(Mandatory=$true)][String] $dataFile
)

# Calculate the number of encoding that will be done
$currentIteration = 1
$totalIterations = $tiles.Length * $codecs.Length * $efforts.Length * $cqs.Length * $heights.Length * $repetitions

# Save the header of the csv file. Data is added to the file and never overwritten
echo "tile,codec,effort,cq,height,time" >> $dataFile

foreach ($tile in $tiles)
{
	foreach ($codec in $codecs)
	{
		foreach ($effort in $efforts)
		{
			foreach ($cq in $cqs)
			{
				foreach ($height in $heights)
				{
					for ($i = 0; $i -lt $repetitions; $i++)
					{
						echo "Iteration $currentIteration out of $totalIterations"
						echo "Params : $tile, $codec, $effort, $cq, $height, $i"
						
						# Create the temporary directory where the segments will be saved
						New-Item -Path . -Name $segmentDirectory -ItemType "directory" | Out-Null
						
						$output = ""
						
						if ($height -eq 0)
						{
							$output = ffmpeg -benchmark -hide_banner -vsync passthrough -hwaccel cuda -hwaccel_output_format cuda -i $tile -c:v $codec -cq $cq -b:v 0 -preset $effort -rc vbr -g $segmentGOP -f segment -segment_time $segmentTime -reset_timestamps 1 -movflags faststart $segmentDirectory\output_%d.mp4 2>&1 | Out-String
						}
						else
						{
							$output = ffmpeg -benchmark -hide_banner -vsync passthrough -hwaccel cuda -hwaccel_output_format cuda -i $tile -vf "hwupload,scale_cuda=-2:$heights" -c:v $codec -cq $cq -b:v 0 -preset $effort -rc vbr -g $segmentGOP -f segment -segment_time $segmentTime -reset_timestamps 1 -movflags faststart $segmentDirectory\output_%d.mp4 2>&1 | Out-String
						}
						
						# Delete all the videos. This must be done since overwritting the videos with FFmpeg slows down the process
						Remove-Item $segmentDirectory -Recurse | Out-Null
						
						# Get the time needed to encode the video
						$output -match "rtime=(\d+\.{0,1}\d+)s" | Out-Null
						$rtime = $matches[1]
						
						# Save the data to the data file
						echo "$tile,$codec,$effort,$cq,$height,$rtime" >> $dataFile
						
						$currentIteration += 1
					}
				}
			}
		}
	}
}