param(
	# The path of the CSV file to read
	[Parameter(Mandatory=$true)][String] $in,
    # Compute the VMAF every N frame
    [Parameter(Mandatory=$true)][Int32] $subsample,
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
        # Compute the VMAF every N frame
        if ($i % $subsample -eq 0)
        {
            $vmaf += [double]$frame.metrics.vmaf
            $numFrames++
        }

        $i++
    }

    $vmaf /= $numFrames

    # Update VMAF
    $row.vmafMean = $vmaf.ToString([System.Globalization.CultureInfo]::InvariantCulture)

    # Add the result to the CSV file
    $row | Add-Member -NotePropertyName "vmafSubsampling" -NotePropertyValue $subsample
}

# Write the CSV file
$csv | Export-Csv -Path $out -NoTypeInformation -Encoding UTF8 -UseQuotes AsNeeded
