param (
    [String[]]$BuildFiles = @(),
    [String]$RootDir = ".",
    [switch]$Interactive,
    [switch]$All,
    [switch]$NoCache,
    [Switch]$Passive,
    [String]$BuildFilter = "build-*.csv"
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
        BuildDockerFiles -BuildFiles $BuildFiles -Location $_Build_dir -Interactive $Interactive -NoCache $NoCache -Passive $Passive -Indent "  "
        Write-Output "= = = = = > Done in location [$_Build_dir] = = = = ="
    }
}
else
{
    if ($BuildFiles.Count -eq 0) # If no build files passed exec all in the root directory given
    {
        Write-Output "+ + + + + < Processing all build files in current diractory + + + + +"
        $BuildFiles = GetBuildFileNames -BuildDir "$_All_dirs[0]"
    }
    else
    {
        Write-Output "+ + + + + < Processing Specified build files. + + + + +"
    }
    BuildDockerFiles -BuildFiles $BuildFiles -Location $_All_dirs[0] -Interactive $Interactive -NoCache $NoCache -Indent "  "
    Write-Output "+ + + + + > Done + + + + +"
}