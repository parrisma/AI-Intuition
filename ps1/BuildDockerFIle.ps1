Function BuildDockerFile
{
    [cmdletbinding()]
    Param (
        [Parameter(Mandatory = $true)][string]$Source,
        [Parameter(Mandatory = $true)][string]$Target,
        [Parameter(Mandatory = $true)][String]$Location,
        [Boolean]$Interactive = $false,
        [Boolean]$NoCache = $false
    )
    Process {
        $_no_cache = ""
        if ($NoCache)
        {
            $_no_cache = "--no-cache"
        }
        $_interactive = ""
        if ($Interactive)
        {
            $_interactive = "--build-arg interactive_build"
        }

        Write-Output "Building : [$Source]"
        $cmd = "docker build -f $Location\$Source $Location -t $Target $_interactive $_no_cache"
        Write-Output $cmd
        Invoke-Expression $cmd *>&1
        # ToDo: Check image was updated
        #     : docker inspect -f '{{ .Created }}' $Target
        Write-Output "Built : [$Source] to [$Target]"
    }
}

Function BuildDockerFiles
{
    [cmdletbinding()]
    Param (
        [Parameter(Mandatory = $true)][Array]$BuildFiles,
        [Parameter(Mandatory = $true)][String]$Location,
        [Boolean]$Interactive = $false,
        [Boolean]$NoCache = $false
    )
    Process {
        Foreach ($build_file in $BuildFiles)
        {
            Write-Output "Processing: $build_file`r`n"
            $build_options = Import-Csv -path $build_file -Header "Dockerfile", "Repository", "Target", "Version"
            Foreach ($line in $build_options)
            {
                $Source = $line | Select-Object -ExpandProperty "Dockerfile"
                $Rep = $line | Select-Object -ExpandProperty "Repository"
                $Target = $line | Select-Object -ExpandProperty "Target"
                $Ver = $line | Select-Object -ExpandProperty "Version"
                BuildDockerFile -Source $Source -Location $Location -Target "${Rep}/${Target}:${Ver}" -Interactive $Interactive -NoCache $NoCache
            }
            Write-Output "Done: $build_file`r`n"
        }
    }
}

Function GetBuildFileNames
{
    [cmdletbinding()]
    Param (
        [Parameter(Mandatory = $true)][String]$BuildDir,
        [String]$Filter = "build-*.csv"
    )
    Process {
        $res = @()
        $files = Get-ChildItem -Path "$build_dir" -Filter $Filter
        foreach ($f in $files)
        {
            $res+= $f.FullName
        }
        return $res
    }
}

Function GetAllSubDirectories
{
    [cmdletbinding()]
    Param (
        [Parameter(Mandatory = $true)][String]$RootDir
    )
    Process {
        $res = @()
        $dirs = Get-ChildItem -Directory -Recurse $RootDir
        foreach ($d in $dirs)
        {
            $res += $d.FullName
        }
        return $res
    }
}