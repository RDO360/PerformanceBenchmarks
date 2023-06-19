# N commandes identiques en parallèle
param(
    [Parameter(Mandatory=$true)][String[]] $tiles
)

# ffmpeg -benchmark -hide_banner -vsync passthrough -hwaccel cuda -hwaccel_output_format cuda -i $using:tile -c:v hevc_nvenc -cq 18 -b:v 0 -preset p7 -rc vbr -g 60 -f segment -segment_time 2 -reset_timestamps 1 -movflags faststart -f null -

$outputs = @()

$outputs += $tiles | ForEach-Object -Parallel {
    # -stats_period 0.1 pour changer la fréquence des statistiques
    $ffmpegOutput = ffmpeg -loglevel error -progress pipe:1 -benchmark -vsync passthrough -hwaccel cuda -hwaccel_output_format cuda -i $_ -c:v hevc_nvenc -cq 18 -b:v 0 -preset p7 -rc vbr -g 60 -f segment -segment_time 2 -reset_timestamps 1 -movflags faststart -f null - | Out-String

    [PSCustomObject]@{
        "Tile" = $_
        "Output" = $ffmpegOutput
    }
} -ThrottleLimit $tiles.Length

$frequency = 0.5

# Save the header of the csv file. Data is added to the file and never overwritten
Write-Output "tile,timestamp,fps"# >> $dataFile

foreach ($output in $outputs)
{
    $i = 0
    $tile = $output.Tile
    $results = [RegEx]::Matches($output.Output, "fps=(?<fps>.+)")

    foreach ($match in $results)
    {
        $timestamp = $i * $frequency
        $fps = $match.Groups["fps"].Value

        Write-Output "$tile,$timestamp,$fps"

        $i++
    }
}
