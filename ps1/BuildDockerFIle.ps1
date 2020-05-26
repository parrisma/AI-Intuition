Function BuildDockerFile
{
    [cmdletbinding()]
    Param (
        [Parameter(Mandatory = $true)][string]$Source,
        [Parameter(Mandatory = $true)][string]$Target,
        [Parameter(Mandatory = $true)][String]$Location,
        [Boolean]$Interactive = $false,
        [Boolean]$NoCache = $false,
        [Boolean]$Passive = $false,
        [String]$Indent = ""
    )
    Process {
        New-Variable -Name _Res -Value "" -Scope Local
        New-Variable -Name _No_cache -Value "" -Scope Local
        New-Variable -Name _Interactive -Value "" -Scope Local
        New-Variable -Name _Cmd -Value "" -Scope Local
        New-Variable -Name _Err -Value "" -Scope Local

        if ($NoCache)
        {
            $_No_cache = "--no-cache"
        }
        $_interactive = ""
        if ($Interactive)
        {
            $_Interactive = "--build-arg interactive_build"
        }

        Write-Output "$Indent . . . . . Building : [$Source] . . . . ."
        $_Cmd = "docker build -f $Location\$Source $Location -t $Target $_Interactive $_No_cache"
        Write-Output "$Indent . . . . . [$_Cmd]"
        if (-Not$Passive)
        {
            Invoke-Expression $_Cmd *>&1 | Tee-Object -Variable '_Res'
            if ($_Res -match "(.*)Successfully built(.*)(\d+)(.*)")
            {
                Write-Output "$Indent . . . . . Built & Tagged OK: [$Source] to [$Target] . . . . ."
            }
            else
            {
                $_Err = "Docker Build Failed for: [$Source] to [$Target]"
                throw $_Err
            }
        }
        return
    }
}

Function BuildDockerFiles
{
    [cmdletbinding()]
    Param (
        [Parameter(Mandatory = $true)][AllowEmptyCollection()][Array]$BuildFiles,
        [Parameter(Mandatory = $true)][String]$Location,
        [Boolean]$Interactive = $false,
        [Boolean]$NoCache = $false,
        [Boolean]$Passive = $false,
        [String]$Indent = "   "
    )
    Process {
        if ($BuildFiles.Count -eq 0)
        {
            Write-Output "`r`n$Indent - - - - < Nothing to do"
        }
        else
        {
            New-Variable -Name _Source -Value $null -Scope Local
            New-Variable -Name _Rep -Value $null -Scope Local
            New-Variable -Name _Target -Value $null -Scope Local
            New-Variable -Name _Ver -Value $null -Scope Local
            Foreach ($build_file in $BuildFiles)
            {
                Write-Output "`r`n$Indent - - - - < Processing: [$build_file] - - - - -"
                $build_options = Import-Csv -path $build_file
                Foreach ($line in $build_options)
                {
                    $_Source = $line | Select-Object -ExpandProperty "Dockerfile"
                    $_Rep = $line | Select-Object -ExpandProperty "Repository"
                    $_Target = $line | Select-Object -ExpandProperty "Target"
                    $_Ver = $line | Select-Object -ExpandProperty "Version"
                    BuildDockerFile -Source $_Source -Location $Location -Target "${_Rep}/${_Target}:${_Ver}" -Interactive $Interactive -NoCache $NoCache -Indent $Indent+"   " -Passive $Passive
                }
            }
        }
        Write-Output "$Indent - - - - > Done: [$build_file] - - - - -`r`n"
        return
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
        New-Variable -Name _Res -Value $null -Scope Local
        New-Variable -Name _File -Value $null -Scope Local
        $_Res = @()
        $_Files = Get-ChildItem -Path $BuildDir -Filter $Filter
        foreach ($f in $_Files)
        {
            $_Res += $f.FullName
        }
        return ,$_Res
    }
}

Function GetAllSubDirectories
{
    [cmdletbinding()]
    Param (
        [Parameter(Mandatory = $true)][String]$RootDir
    )
    Process {
        New-Variable -Name _Res -Value $null -Scope Local
        New-Variable -Name _Dirs -Value $null -Scope Local
        $_Res = @()
        $_Dirs = Get-ChildItem -Directory -Recurse $RootDir
        foreach ($d in $_Dirs)
        {
            $_Res += $d.FullName
        }
        return ,$_Res
    }
}
