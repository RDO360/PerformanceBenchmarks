param(
	# An array of tiles to evaluate
	[Parameter(Mandatory=$true)][String[]] $tiles,
	# The directory to save the results
	[Parameter(Mandatory=$true)][String] $resultsDirectory
)

# The number of evaluations that will be done
$numTiles = $tiles.Length
$currentIteration = 1

# Create the directory where the results will be saved
New-Item -ItemType Directory -Path $resultsDirectory | Out-Null

foreach ($tile in $tiles)
{
	Write-Output "Analyzing tile $currentIteration of $numTiles"

	# The path where the results will be saved
	$resultPath = Join-Path -Path $resultsDirectory -ChildPath "siti_${tile}.json"
	
	# Evaluate the spatial and temporal information
	siti-tools $tile -r full -f json > $resultPath
	
	$currentIteration += 1
}
