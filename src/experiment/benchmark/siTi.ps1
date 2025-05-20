param(
	# An array of tiles to evaluate
	[Parameter(Mandatory=$true)][String[]] $tiles,
	# The csv file that will contain the results
	[Parameter(Mandatory=$true)][String] $resultsFile
)

# The number of evaluations that will be done
$numTiles = $tiles.Length
$currentIteration = 1

# Skip the header line from the siti-tools output, starting from the second tile
$skip = 0

foreach ($tile in $tiles)
{
	Write-Output "Analyzing tile $currentIteration of $numTiles"
	
	# Evaluate the spatial and temporal information and append the data to the results file
	siti-tools $tile -r full -f csv | Select-Object -Skip $skip >> $resultsFile
	
	$skip = 1
	$currentIteration += 1
}
