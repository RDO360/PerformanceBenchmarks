param(
	# An array of tiles to encode
	[Parameter(Mandatory=$true)][String[]] $tiles,
	# An array of codecs. Codecs must be supported by FFmpeg
	[Parameter(Mandatory=$true)][String[]] $codecs,
	# An array of presets
	[Parameter(Mandatory=$true)][String[]] $presets,
	# An array of constant quantization parameters between 0 and 51
	[Parameter(Mandatory=$true)][int[]] $qps,
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

# Calculate the number of encodings that will be done
$currentIteration = 1
$totalIterations = $tiles.Length * $codecs.Length * $presets.Length * $qps.Length * $heights.Length

# Save the header of the csv file. Data is added to the file and never overwritten
Write-Output "tile,segment,repetition,codec,preset,qp,height,encodingTime" >> $dataFile

foreach ($tile in $tiles)
{
    # Probe tile to get its duration in seconds and its width and height in pixels
    $probe = ffprobe -select_streams v -show_entries stream=width,height,duration -print_format json -loglevel warning -i $tile | ConvertFrom-Json
    $tileDuration = $probe.streams[0].duration -as [double]

	foreach ($codec in $codecs)
	{
		foreach ($preset in $presets)
		{
			foreach ($qp in $qps)
			{
				foreach ($height in $heights)
				{
                    for ($i = 0; $i -lt $repetitions; $i++)
					{
                        Write-Output "Iteration $currentIteration out of $totalIterations"
                        Write-Output "Params : $tile, $segment, $codec, $preset, $qp, $height, $i"

                        # Create the temporary directory where the segments will be saved
                        New-Item -ItemType Directory -Path $segmentDirectory | Out-Null

                        # Create the raw segments
                        $rawSegmentsPath = Join-Path -Path $segmentDirectory -ChildPath "output_%d.y4m"

                        ffmpeg -loglevel error -vsync passthrough -hwaccel cuda -hwaccel_output_format cuda -i $tile -f segment -segment_time $segmentTime -reset_timestamps 1 $rawSegmentsPath

                        # Find the amount of segments (ignore segments that are less than $segmentTime by flooring the value)
                        $numSegments = [math]::floor($tileDuration / $segmentTime)

                        # Encode the segment and get its bitrate and VMAF
                        for ($segment = 0; $segment -lt $numSegments; $segment++)
                        {
                            $segmentPlusOne = $segment + 1

                            Write-Output "Processing segment $segmentPlusOne out of $numSegments"

                            $rawSegmentPath = Join-Path -Path $segmentDirectory -ChildPath "output_$segment.y4m"
                            $segmentPath = Join-Path -Path $segmentDirectory -ChildPath "output_$segment.mp4"

                            # Encode the segment
                            if ($height -eq 0)
                            {
                                $output = ffmpeg -benchmark -hide_banner -vsync passthrough -hwaccel cuda -hwaccel_output_format cuda -i $rawSegmentPath -c:v $codec -qp $qp -b:v 0 -preset $preset -rc constqp -g $segmentGOP -movflags faststart $segmentPath 2>&1 | Out-String
                            }
                            else
                            {
                                $output = ffmpeg benchmark -hide_banner -vsync passthrough -hwaccel cuda -hwaccel_output_format cuda -i $rawSegmentPath -vf "hwupload,scale_cuda=-2:$height" -c:v $codec -qp $qp -b:v 0 -preset $preset -rc constqp -g $segmentGOP -movflags faststart $segmentPath 2>&1 | Out-String
                            }

                            # Get the time needed to encode the video
                            $output -match "rtime=(\d+\.{0,1}\d+)s" | Out-Null
                            $rtime = $matches[1]

                            # Save the data to the data file
                            Write-Output "$tile,$segment,$i,$codec,$preset,$qp,$height,$rtime" >> $dataFile
                        }

                        # Delete the videos
                        Remove-Item $segmentDirectory -Recurse | Out-Null

                        $currentIteration += 1
                    }
				}
			}
		}
	}
}
