param(
    # The encoding parameters for the first tile in this order : tile path, codec, preset, quality factor, height
    # The height is in pixels. Use 0 if you dont want to resize. Aspect ratio is kept and width will be even.
    [Parameter(Mandatory=$true)][String[]] $tile1,
    # The encoding parameter for the second tile. See $tile1 for their order.
    [Parameter(Mandatory=$true)][String[]] $tile2,
	# The number of times to repeat each encoding
	[Parameter(Mandatory=$true)][int] $repetitions,
    # The duration in seconds of each segment
	[Parameter(Mandatory=$true)][int] $segmentTime,
	# Inserts a key frame every $segmentGOP frames
	[Parameter(Mandatory=$true)][int] $segmentGOP,
	# The directory to save the temporary segments
	[Parameter(Mandatory=$true)][String] $segmentDirectory
)

# Transfer all parameters in a PSCustomObject that can be passed to the ForEach-Object loop
$temp = $tile1, $tile2

$params = for ($i = 0; $i -lt $temp.Length; $i++)
{
    [PSCustomObject]@{
        Tile = $temp[$i][0]
        Codec = $temp[$i][1]
        Preset = $temp[$i][2]
        Cq = $temp[$i][3]
        Height = $temp[$i][4]
        Segments = Join-Path -Path $segmentDirectory -ChildPath "output${i}_%d.mp4"
    }
}

# Output the header of the csv file
Write-Output "tile,repetition,codec,preset,cq,height,speed"

$outputs = @()

for ($i = 0; $i -lt $repetitions; $i++)
{
    # Create the temporary directory where the segments will be saved
    New-Item -ItemType Directory -Path $segmentDirectory | Out-Null

    # Execute the FFmpeg commands in parallel
    $outputs = $params | ForEach-Object -ThrottleLimit $params.Length -Parallel {

        if ($_.Height -eq 0)
        {
            $ffmpegOutput = ffmpeg -loglevel error -progress pipe:1 -benchmark -vsync passthrough -hwaccel cuda -hwaccel_output_format cuda -i $_.Tile -c:v $_.Codec -cq $_.Cq -b:v 0 -preset $_.Preset -rc vbr -g $using:segmentGOP -f segment -segment_time $using:segmentTime -reset_timestamps 1 -movflags faststart $_.Segments | Out-String
        }
        else
        {
            $height = $_.Height # Need to use this variable for the command to work
            $ffmpegOutput = ffmpeg -loglevel error -progress pipe:1 -benchmark -vsync passthrough -hwaccel cuda -hwaccel_output_format cuda -i $_.Tile -vf "hwupload,scale_cuda=-2:$height" -c:v $_.Codec -cq $_.Cq -b:v 0 -preset $_.Preset -rc vbr -g $using:segmentGOP -f segment -segment_time $using:segmentTime -reset_timestamps 1 -movflags faststart $_.Segments | Out-String
        }

        # Save the results in a custom object
        [PSCustomObject]@{
            Tile = $_.Tile
            Codec = $_.Codec
            Preset = $_.Preset
            Cq = $_.Cq
            Height = $_.Height
            Segments = $_.Segments
            Output = $ffmpegOutput
        }
    }

    # Delete all the videos. This must be done since overwritting the videos with FFmpeg slows down the process
    Remove-Item $segmentDirectory -Recurse | Out-Null

    # Extract the encoding speed for each output
    foreach ($output in $outputs)
    {
        $tile = $output.Tile
        $codec = $output.Codec
        $preset = $output.Preset
        $cq = $output.Cq
        $height = $output.Height
        $results = [RegEx]::Matches($output.Output, "fps=(?<fps>.+)")

        foreach ($match in $results)
        {
            $fps = [double]$match.Groups["fps"].Value

            Write-Output "$tile,$i,$codec,$preset,$cq,$height,$fps"
        }
    }
}
