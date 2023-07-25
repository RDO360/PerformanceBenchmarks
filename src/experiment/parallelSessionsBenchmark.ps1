param(
    # An array of tiles to encode
    [Parameter(Mandatory=$true)][String[]] $tiles,
    # The max number of sessions to test in parallel
    [Parameter(Mandatory=$true)][int] $sessions,
    # The codec. It must be supported by the hardware encoder
    [Parameter(Mandatory=$true)][String] $codec,
    # The preset
    [Parameter(Mandatory=$true)][String] $preset,
    # The constant quality factor (CRF) between 0 and 51
    [Parameter(Mandatory=$true)][int] $cq,
    # The height of the tiles. The aspect ratio is kept. An height of 0 means no resizing
    [Parameter(Mandatory=$true)][int] $height,
    # The number of times to repeat each encoding
    [Parameter(Mandatory=$true)][int] $repetitions,
    # The duration in seconds of each segment
	[Parameter(Mandatory=$true)][int] $segmentTime,
	# Inserts a key frame every $segmentGOP frames
	[Parameter(Mandatory=$true)][int] $segmentGOP,
	# The directory to save the temporary segments
	[Parameter(Mandatory=$true)][String] $segmentDirectory
)

$outputs = @()

# Save the header of the csv file. Data is added to the file and never overwritten
Write-Output "session,tile,time"

for ($j = 1; $j -le $sessions; $j++)
{
    # Get the tiles that will be encoded in parallel
    $selectedTiles = $tiles | Select-Object -First $j

    for ($i = 0; $i -lt $repetitions; $i++)
    {
        # Create the temporary directory where the segments will be saved
        New-Item -ItemType Directory -Path $segmentDirectory | Out-Null

        # Segments path
        $segmentsPath = Join-Path -Path $segmentDirectory -ChildPath "output_%d.mp4"

        # Execute the FFmpeg commands in parallel
        $outputs = $selectedTiles | ForEach-Object -ThrottleLimit $j -Parallel {
            $output = ffmpeg -benchmark -hide_banner -vsync passthrough -hwaccel cuda -hwaccel_output_format cuda -i $_ -c:v $using:codec -cq $using:cq -b:v 0 -preset $using:preset -rc vbr -g $using:segmentGOP -f segment -segment_time $using:segmentTime -reset_timestamps 1 -movflags faststart $using:segmentsPath 2>&1 | Out-String

            # Get the time needed to encode the video
            $output -match "rtime=(\d+\.{0,1}\d+)s" | Out-Null
            $rtime = $matches[1]

            # Save the results in a custom object
            [PSCustomObject]@{
                tile = $_
                rtime = $rtime
            }
        }

        # Delete all the videos. This must be done since overwritting the videos with FFmpeg slows down the process
        Remove-Item $segmentDirectory -Recurse | Out-Null

        foreach ($output in $outputs)
        {
            $tile = $output.tile
            $rtime = $output.rtime

            Write-Output "$j,$tile,$rtime"
        }
    }
}
