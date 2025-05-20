param(
	# The path of the CSV file to read
	[Parameter(Mandatory=$true)][String] $in,
    # The path of the CSV file to write
    [Parameter(Mandatory=$true)][String] $out
)

# Read the CSV
$csv = Import-Csv $in
$r = 1

foreach ($row in $csv)
{
    Write-Output "Processing row $($r) of $($csv.count)"
    $r++

    $vmaf = 0

    # Decode the VMAF log
    $path = "../vmafLogs/" + $row.vmafLogFile
    $json = Get-Content -Raw -Path $path | ConvertFrom-Json
    $numFrames = 0
    $i = 0

    # Compute the subsampled VMAF
    foreach ($frame in $json.frames)
    {
        # Skip every 2 frames
        if ($i % 10 -eq 0)
        {
            $vmaf += [double]$frame.metrics.vmaf
            $numFrames++
        }

        $i++
    }

    $vmaf /= $numFrames

    # Add the result to the CSV file
    $row | Add-Member -NotePropertyName "vmafMean10" -NotePropertyValue $vmaf.ToString([System.Globalization.CultureInfo]::InvariantCulture)
}

# Write the CSV file
$csv | Export-Csv -Path $out -NoTypeInformation -Encoding UTF8 -UseQuotes AsNeeded
