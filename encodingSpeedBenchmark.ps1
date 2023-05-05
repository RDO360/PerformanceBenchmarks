param(
	[Parameter(Mandatory=$true)][String[]] $tiles,
	[Parameter(Mandatory=$true)][String[]] $codecs,
	[Parameter(Mandatory=$true)][String[]] $efforts,
	[Parameter(Mandatory=$true)][int[]] $cqs,
	[Parameter(Mandatory=$true)][int[]] $heights,
	[Parameter(Mandatory=$true)][int] $repetitions,
	[Parameter(Mandatory=$true)][int] $segmentTime,
	[Parameter(Mandatory=$true)][int] $segmentGOP,
	[Parameter(Mandatory=$true)][String] $segmentDirectory,
	[Parameter(Mandatory=$true)][String] $dataFile
)

$currentIteration = 1
$totalIterations = $tiles.Length * $codecs.Length * $efforts.Length * $cqs.Length * $heights.Length * $repetitions

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
						
						Remove-Item $segmentDirectory -Recurse | Out-Null
						
						$output -match "rtime=(\d+\.{0,1}\d+)s" | Out-Null
						$rtime = $matches[1]
						
						echo "$tile,$codec,$effort,$cq,$height,$rtime" >> $dataFile
						
						$currentIteration += 1
					}
				}
			}
		}
	}
}