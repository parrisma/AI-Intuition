param (
    [String[]]$BuildFiles = @(), # Comma separated list of build-<?>.csv file in $RootDir - cannotu use with $All
    [String]$RootDir = ".", # The directory to look for the build-<?>.csv files
    [Switch]$Interactive, # Set the [interactive_build] build Arg and pass to Docker build
    [Switch]$All, # Run every build-<?>.csv file in $RootDir and all it's sub directories
    [Switch]$NoCache, # Pass the --no-cache flag to Docker build
    [Switch]$Passive, # Show but do not execute the Docker commands
    [Switch]$PushToHub, # Push the built image to Docker Hub *IF* it's push attribute os True in build-</>.csv
    [String]$BuildFilter = "build-*.csv" # The file pattern to use to find the build csv file(s)
)

. ..\..\ps1\GlobalDefaults.ps1
. ..\..\ps1\BuildDockerFile.ps1

New-Variable -Name _All_dirs -Value $null -Scope Local
New-Variable -Name _Build_dir -Value $null -Scope Local

#
# Estbalish list of dirs to process. If -All then recurse down. Always add current dir [.] as first
# dir to process.
#
$_All_dirs = @()
$_All_dirs += $RootDir
if ($All)
{
    if ($BuildFiles.Count -gt 0)
    {
        Write-Output "** WARNING :: Mode [-All] => any specified [-BuildFiles] will be ignored"
    }

    $_All_dirs += GetAllSubDirectories -RootDir $RootDir
    #
    # Iterate all directories starting at the top and working down
    #
    foreach ($_Build_dir in $_All_dirs)
    {
        Write-Output "= = = = = < Processing build-<?>.csv files in location [$_Build_dir] = = = = ="
        $BuildFiles = GetBuildFileNames -BuildDir $_Build_dir -Filter $BuildFilter
        BuildDockerFiles -BuildFiles $BuildFiles -Location $_Build_dir -Interactive $Interactive -NoCache $NoCache -Passive $Passive -Indent "  " -PushToHub $PushToHub
        Write-Output "= = = = = > Done in location [$_Build_dir] = = = = ="
    }
}
else
{
    if ($BuildFiles.Count -eq 0) # If no build files passed exec all in the root directory given
    {
        Write-Output "+ + + + + < Processing all build files in directory + + + + +"
        $BuildFiles = GetBuildFileNames -BuildDir $_All_dirs[0]
    }
    else
    {
        Write-Output "+ + + + + < Processing Specified build files. + + + + +"
    }
    BuildDockerFiles -BuildFiles $BuildFiles -Location $_All_dirs[0] -Interactive $Interactive -NoCache $NoCache -Indent "  " -PushToHub $PushToHub -Passive $Passive
    Write-Output "+ + + + + > Done + + + + +"
}