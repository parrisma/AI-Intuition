param (
    [String[]]$BuildFiles = @(),
    [String]$RootDir = ".",
    [switch]$Interactive,
    [switch]$All,
    [switch]$NoCache
)

. ..\..\ps1\GlobalDefaults.ps1
. ..\..\ps1\BuildDockerFile.ps1

#
# Estbalish list of dirs to process. If -All then recurse down. Always add current dir [.] as first
# dir to process.
#
$all_dirs = @()
$all_dirs += $RootDir
if ($All)
{
    if ($BuildFiles.Count -gt 0)
    {
        Write-Output "** WARNING :: Mode [-All] selected any specified [-BuildFiles] will be ignored"
    }

    $all_dirs += GetAllSubDirectories -RootDir $RootDir
    #
    # Iterate all directories starting at the top and working down
    #
    foreach ($build_dir in $all_dirs)
    {
        Write-Output "Processing build-<?>.csv files in location [$build_dir]"
        $BuildFiles = $BuildFiles = GetBuildFileNames -BuildDir "$build_dir"
        BuildDockerFiles -BuildFiles $BuildFiles -Location $build_dir -Interactive $Interactive -NoCache $NoCache
        Write-Output "Done in location [$build_dir]"
    }
}
else
{
    if ($BuildFiles.Count -eq 0)
    {
        Write-Output "Processing all build files in current diractory"
        $BuildFiles = GetBuildFileNames -BuildDir "$all_dirs[0]"
    }
    else
    {
        Write-Output "Processing Specified build files."
    }
    BuildDockerFiles -BuildFiles $BuildFiles -Location $all_dirs[0] -Interactive $Interactive -NoCache $NoCache
    Write-Output "Done"
}