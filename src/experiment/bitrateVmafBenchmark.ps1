param(
	# An array of tiles to encode
	[Parameter(Mandatory=$true)][String[]] $tiles,
	# An array of codecs. Codecs must be supported by the hardware encoder
	[Parameter(Mandatory=$true)][String[]] $codecs,
	# An array of presets
	[Parameter(Mandatory=$true)][String[]] $presets,
	# An array of constant quality factor (CRF) between 0 and 51
	[Parameter(Mandatory=$true)][int[]] $cqs,
	# An array of heights. The aspect ratio is kept. An height of 0 means no resizing
	[Parameter(Mandatory=$true)][int[]] $heights,
	# The duration in seconds of each segment
	[Parameter(Mandatory=$true)][int] $segmentTime,
	# Inserts a key frame every $segmentGOP frames
	[Parameter(Mandatory=$true)][int] $segmentGOP,
	# The directory to save the temporary segments
	[Parameter(Mandatory=$true)][String] $segmentDirectory,
	# The csv file where the data will be saved to
	[Parameter(Mandatory=$true)][String] $dataFile,
    # The directory where the VMAF logs will be saved to
    [Parameter(Mandatory=$true)][String] $vmafLogDirectory
)

# Calculate the number of encodings that will be done
$currentIteration = 1
$totalIterations = $tiles.Length * $codecs.Length * $presets.Length * $cqs.Length * $heights.Length

# Create the directory where the VMAF logs of the segments will be saved
New-Item -ItemType Directory -Path $vmafLogDirectory | Out-Null

# Save the header of the csv file. Data is added to the file and never overwritten
Write-Output "tile,codec,preset,cq,height,bitrate,vmafMean,logFile" >> $dataFile

foreach ($tile in $tiles)
{
    # Probe tile to get its duration in seconds and its width and height in pixels
    $probe = ffprobe -select_streams v -show_entries stream=width,height,duration -print_format json -loglevel warning -i $tile | ConvertFrom-Json
    $tileDuration = $probe.streams[0].duration -as [double]
    $tileWidth  = $probe.streams[0].width -as [int]
    $tileHeight  = $probe.streams[0].height -as [int]

	foreach ($codec in $codecs)
	{
		foreach ($preset in $presets)
		{
			foreach ($cq in $cqs)
			{
				foreach ($height in $heights)
				{
                    Write-Output "Iteration $currentIteration out of $totalIterations"
                    Write-Output "Params : $tile, $codec, $preset, $cq, $height"

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
                        Write-Output "Processing segment $segment out of $numSegments"

                        $rawSegmentPath = Join-Path -Path $segmentDirectory -ChildPath "output_$segment.y4m"
                        $segmentPath = Join-Path -Path $segmentDirectory -ChildPath "output_$segment.mp4"

                        # We cant use Join-Path, since libvmaf only accepts / as a path separator, even on Windows
                        $vmafLogFile = "vmaf_tile_${tile}_segment_${segment}_codec_${codec}_preset_${preset}_cq_${cq}_height_${height}.json"
                        $vmafLogPath = $vmafLogDirectory + "/" + $vmafLogFile

                        # Encode the segment and get the VMAF
                        if ($height -eq 0)
                        {
                            ffmpeg -loglevel error -vsync passthrough -hwaccel cuda -hwaccel_output_format cuda `
                            -i $rawSegmentPath -c:v $codec -cq $cq -b:v 0 -preset $preset -rc vbr -g $segmentGOP -movflags faststart $segmentPath

                            ffmpeg -loglevel error -i $segmentPath -i $rawSegmentPath -filter_complex "libvmaf=feature=name=psnr:phone_model=1:n_threads=8:log_path=$vmafLogPath\:log_fmt=json" -f null -
                        }
                        else
                        {
                            ffmpeg -loglevel error -vsync passthrough -hwaccel cuda -hwaccel_output_format cuda `
                            -i $rawSegmentPath -vf "hwupload,scale_cuda=-2:$heights" -c:v $codec -cq $cq -b:v 0 -preset $preset -rc vbr -g $segmentGOP -movflags faststart $segmentPath

                            ffmpeg -loglevel error -i $segmentPath -i $rawSegmentPath -filter_complex "[0]scale=${tileWidth}x${tileHeight},libvmaf=feature=name=psnr:phone_model=1:n_threads=8:log_path=$vmafLogPath\:log_fmt=json" -f null -
                        }

                        # Get the mean VMAF
                        $vmaf = Get-Content -Raw $vmafLogPath | ConvertFrom-Json
                        $vmafMean = $vmaf.pooled_metrics.vmaf.mean

                        # Get bitrate
                        $probe = ffprobe -select_streams v -show_entries stream=bit_rate -print_format json -loglevel warning -i $segmentPath | ConvertFrom-Json
                        $bitrate = $probe.streams[0].bit_rate

                        # Save the data to the data file
                        Write-Output "$tile,$codec,$preset,$cq,$height,$bitrate,$vmafMean,$logFile" >> $dataFile
                    }

                    # Delete the videos
                    Remove-Item $segmentDirectory -Recurse | Out-Null

                    $currentIteration += 1
				}
			}
		}
	}
}
